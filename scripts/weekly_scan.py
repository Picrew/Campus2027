#!/usr/bin/env python3
from __future__ import annotations

import argparse
import concurrent.futures
import http.client
import importlib.util
import json
import re
import socket
import ssl
import subprocess
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0 Safari/537.36"
)
TIMEOUT_SECONDS = 20
MAX_BYTES = 2_000_000

STATUS_OPEN = "open"
STATUS_REVIEW = "needs_review"
STATUS_CLOSED = "closed"
STATUS_BROKEN = "broken"

CLOSED_PATTERNS = [
    re.compile(p, re.I)
    for p in [
        r"job (?:is )?no longer available",
        r"position (?:is )?no longer available",
        r"this job is no longer accepting applications",
        r"applications? (?:for this role )?closed",
        r"job has expired",
        r"职位已关闭",
        r"岗位已关闭",
        r"招聘已结束",
        r"已停止招聘",
        r"该职位已下线",
        r"已过期",
        r"停止接受申请",
    ]
]

REVIEW_PATTERNS = [
    re.compile(p, re.I)
    for p in [
        r"access denied",
        r"forbidden",
        r"验证",
        r"captcha",
        r"登录后查看",
        r"请开启(?:浏览器)?javascript",
        r"enable javascript",
        r"redirecting",
    ]
]

DEADLINE_KEYWORDS = [
    "deadline",
    "apply by",
    "application deadline",
    "截止日期",
    "截止时间",
    "投递截止",
    "申请截止",
]

NON_APPLICATION_DEADLINE_PATTERNS = [
    re.compile(p, re.I)
    for p in [
        r"数据.{0,12}截止",
        r"指数.{0,12}截止",
        r"业绩.{0,12}截止",
        r"data.{0,12}(?:as of|through)",
        r"performance.{0,12}(?:as of|through)",
    ]
]

DATE_PATTERNS = [
    re.compile(r"(20\d{2})[-/\.](\d{1,2})[-/\.](\d{1,2})"),
    re.compile(r"(20\d{2})年(\d{1,2})月(\d{1,2})日"),
    re.compile(r"(20\d{2})[-/\.](\d{1,2})"),
    re.compile(r"(20\d{2})年(\d{1,2})月"),
]


class TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        if data.strip():
            self.parts.append(data.strip())

    def text(self) -> str:
        return " ".join(self.parts)


@dataclass
class ScanResult:
    company: str
    focus: str
    url: str
    http_code: int | None
    final_url: str | None
    status: str
    deadline: str | None
    deadline_evidence: str | None
    review_reason: str | None
    error: str | None


def load_generate_module(root: Path):
    target = root / "scripts" / "generate_readmes.py"
    spec = importlib.util.spec_from_file_location("generate_readmes", target)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {target}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def build_opener() -> urllib.request.OpenerDirector:
    ctx = ssl.create_default_context()
    return urllib.request.build_opener(
        urllib.request.HTTPSHandler(context=ctx),
        urllib.request.HTTPRedirectHandler(),
    )


def normalize_space(text: str) -> str:
    return re.sub(r"\s+", " ", unescape(text)).strip()


def extract_text(content_bytes: bytes, content_type: str | None) -> str:
    charset = "utf-8"
    if content_type:
        match = re.search(r"charset=([^\s;]+)", content_type, re.I)
        if match:
            charset = match.group(1).strip("\"'")
    try:
        decoded = content_bytes.decode(charset, errors="ignore")
    except LookupError:
        decoded = content_bytes.decode("utf-8", errors="ignore")
    parser = TextExtractor()
    parser.feed(decoded)
    text = parser.text()
    if not text:
        text = decoded
    return normalize_space(text)


def detect_status(text: str, http_code: int | None, error: str | None) -> tuple[str, str | None]:
    if error:
        return STATUS_BROKEN, error
    if http_code and http_code >= 400:
        return STATUS_BROKEN, f"HTTP {http_code}"
    if http_code and 300 <= http_code < 400:
        return STATUS_REVIEW, f"HTTP {http_code}"
    for pat in CLOSED_PATTERNS:
        hit = pat.search(text)
        if hit:
            return STATUS_CLOSED, hit.group(0)
    for pat in REVIEW_PATTERNS:
        hit = pat.search(text)
        if hit:
            return STATUS_REVIEW, hit.group(0)
    return STATUS_OPEN, None


def extract_deadline(text: str) -> tuple[str | None, str | None]:
    for pattern in [
        re.compile(r'"applicationDeadline":"(20\d{2})-(\d{2})-(\d{2})"'),
        re.compile(r'"applicationDeadline":"(20\d{2})-(\d{2})"'),
    ]:
        match = pattern.search(text)
        if match:
            if len(match.groups()) == 3:
                year, month, day = match.groups()
                return f"{int(year):04d}-{int(month):02d}-{int(day):02d}", match.group(0)
            year, month = match.groups()
            return f"{int(year):04d}-{int(month):02d}", match.group(0)

    lowered = text.lower()
    candidates: list[tuple[str, str]] = []
    for keyword in DEADLINE_KEYWORDS:
        start = 0
        probe = keyword.lower()
        while True:
            idx = lowered.find(probe, start)
            if idx == -1:
                break
            window = text[max(0, idx - 40): idx + 120]
            for pattern in DATE_PATTERNS:
                match = pattern.search(window)
                if match:
                    if "publisheddate" in window.lower():
                        continue
                    if any(skip.search(window) for skip in NON_APPLICATION_DEADLINE_PATTERNS):
                        continue
                    if len(match.groups()) == 3:
                        year, month, day = match.groups()
                        value = f"{int(year):04d}-{int(month):02d}-{int(day):02d}"
                    else:
                        year, month = match.groups()
                        value = f"{int(year):04d}-{int(month):02d}"
                    candidates.append((value, normalize_space(window)))
                    break
            start = idx + len(probe)
    if not candidates:
        return None, None
    candidates.sort(key=lambda item: (len(item[0]), item[0]), reverse=True)
    return candidates[0]


def fetch(entry: dict[str, str]) -> ScanResult:
    req = urllib.request.Request(
        entry["url"],
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
        },
        method="GET",
    )
    opener = build_opener()
    try:
        with opener.open(req, timeout=TIMEOUT_SECONDS) as resp:
            content = resp.read(MAX_BYTES)
            http_code = getattr(resp, "status", None) or resp.getcode()
            final_url = resp.geturl()
            text = extract_text(content, resp.headers.get("Content-Type"))
            status, reason = detect_status(text, http_code, None)
            deadline, evidence = extract_deadline(text)
            return ScanResult(
                company=entry["company"],
                focus=entry["focus"],
                url=entry["url"],
                http_code=http_code,
                final_url=final_url,
                status=status,
                deadline=deadline,
                deadline_evidence=evidence,
                review_reason=reason,
                error=None,
            )
    except urllib.error.HTTPError as exc:
        # Authentication, bot protection, and rate limiting do not prove that
        # a public job page is dead; keep them in the manual-review bucket.
        status = STATUS_REVIEW if exc.code in {401, 403, 429} else STATUS_BROKEN
        result = ScanResult(
            company=entry["company"],
            focus=entry["focus"],
            url=entry["url"],
            http_code=exc.code,
            final_url=entry["url"],
            status=status,
            deadline=None,
            deadline_evidence=None,
            review_reason=f"HTTP {exc.code}",
            error=f"HTTP {exc.code}" if status == STATUS_BROKEN else None,
        )
        return apply_curl_fallback(result)
    except (
        urllib.error.URLError,
        TimeoutError,
        socket.timeout,
        ssl.SSLError,
        http.client.RemoteDisconnected,
    ) as exc:
        result = ScanResult(
            company=entry["company"],
            focus=entry["focus"],
            url=entry["url"],
            http_code=None,
            final_url=entry["url"],
            status=STATUS_BROKEN,
            deadline=None,
            deadline_evidence=None,
            review_reason=str(exc),
            error=str(exc),
        )
        return apply_curl_fallback(result)


def apply_curl_fallback(result: ScanResult) -> ScanResult:
    if result.status != STATUS_BROKEN:
        return result

    def run_curl_probe(extra_args: list[str]) -> tuple[int | None, str | None, bool]:
        try:
            proc = subprocess.run(
                [
                    "curl",
                    "-L",
                    "-A",
                    "Mozilla/5.0",
                    "--max-time",
                    str(TIMEOUT_SECONDS),
                    *extra_args,
                    "-o",
                    "/dev/null",
                    "-sS",
                    "-w",
                    "%{http_code} %{url_effective}",
                    result.url,
                ],
                check=False,
                capture_output=True,
                text=True,
                timeout=TIMEOUT_SECONDS + 5,
            )
        except (OSError, subprocess.TimeoutExpired):
            return None, None, False

        text = proc.stdout.strip()
        match = re.match(r"(\d{3})\s+(.+)", text)
        if not match:
            return None, None, proc.returncode == 0
        return int(match.group(1)), match.group(2), proc.returncode == 0

    def build_result(code: int, final_url: str, review_reason: str) -> ScanResult:
        if 200 <= code < 300:
            return ScanResult(
                company=result.company,
                focus=result.focus,
                url=result.url,
                http_code=code,
                final_url=final_url,
                status=STATUS_OPEN,
                deadline=None,
                deadline_evidence=None,
                review_reason=review_reason,
                error=None,
            )
        if 300 <= code < 400:
            return ScanResult(
                company=result.company,
                focus=result.focus,
                url=result.url,
                http_code=code,
                final_url=final_url,
                status=STATUS_REVIEW,
                deadline=None,
                deadline_evidence=None,
                review_reason=review_reason,
                error=None,
            )
        return result

    code, final_url, ok = run_curl_probe([])
    if ok and code is not None:
        if 200 <= code < 300:
            return build_result(code, final_url or result.url, "curl fallback confirmed")
        if 300 <= code < 400:
            return build_result(code, final_url or result.url, f"curl fallback HTTP {code}")

    # Some ATS pages reject GET probes but still answer HEAD, which is enough to
    # distinguish an actually dead link from a transport-specific false alarm.
    head_code, head_final_url, head_ok = run_curl_probe(["-I"])
    if head_ok and head_code is not None and 200 <= head_code < 400:
        return ScanResult(
            company=result.company,
            focus=result.focus,
            url=result.url,
            http_code=head_code,
            final_url=head_final_url or result.url,
            status=STATUS_REVIEW,
            deadline=None,
            deadline_evidence=None,
            review_reason=f"curl HEAD fallback HTTP {head_code}",
            error=None,
        )

    return result


def summarize_changes(results: list[ScanResult], recorded_deadlines: dict[str, str]) -> dict[str, Any]:
    broken = []
    status_changes = []
    deadline_changes = []
    review_companies: set[str] = set()

    for item in results:
        if item.status in {STATUS_BROKEN, STATUS_CLOSED, STATUS_REVIEW}:
            status_changes.append(
                {
                    "company": item.company,
                    "focus": item.focus,
                    "url": item.url,
                    "status": item.status,
                    "http_code": item.http_code,
                    "reason": item.review_reason,
                }
            )
            review_companies.add(item.company)
        if item.status == STATUS_BROKEN:
            broken.append(
                {
                    "company": item.company,
                    "focus": item.focus,
                    "url": item.url,
                    "http_code": item.http_code,
                    "reason": item.review_reason,
                }
            )
        recorded = recorded_deadlines.get(item.url)
        if item.deadline and item.deadline != recorded:
            deadline_changes.append(
                {
                    "company": item.company,
                    "focus": item.focus,
                    "url": item.url,
                    "old_deadline": recorded,
                    "new_deadline": item.deadline,
                    "evidence": item.deadline_evidence,
                }
            )
            review_companies.add(item.company)

    return {
        "new_links": [],
        "broken_links": broken,
        "status_changes": status_changes,
        "deadline_changes": deadline_changes,
        "manual_review_companies": sorted(review_companies),
    }


def print_human_summary(summary: dict[str, Any], total: int) -> None:
    print(f"Scanned {total} official links.")
    print(f"New links: {len(summary['new_links'])}")
    print(f"Broken links: {len(summary['broken_links'])}")
    print(f"Status changes: {len(summary['status_changes'])}")
    print(f"Deadline changes: {len(summary['deadline_changes'])}")
    print(f"Manual review companies: {len(summary['manual_review_companies'])}")
    print("")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=20)
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    mod = load_generate_module(root)
    entries = list(mod.ENTRIES)
    recorded_deadlines = dict(mod.DEADLINE_BY_URL)

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
        results = list(executor.map(fetch, entries))

    summary = summarize_changes(results, recorded_deadlines)
    print_human_summary(summary, len(entries))

    if summary["broken_links"] or summary["status_changes"] or summary["deadline_changes"]:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
