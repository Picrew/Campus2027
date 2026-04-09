#!/usr/bin/env python3
"""Validate bilingual README files for Campus2027."""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

TRACKING_KEYS = {"utm_source", "utm_medium", "utm_campaign", "ref", "gh_jid"}
KEY_COMPANIES = ["StepFun", "Apple", "AWS", "Qualcomm", "AMD"]


def normalize_url(url: str) -> str:
    p = urlparse(url.strip())
    kept = [(k, v) for k, v in parse_qsl(p.query, keep_blank_values=True) if k not in TRACKING_KEYS]
    q = urlencode(kept, doseq=True)
    return urlunparse(p._replace(query=q, fragment=""))


def extract_apply_urls(text: str) -> list[str]:
    urls = re.findall(r"\[(?:Apply|投递)\]\((https?://[^)]+)\)", text)
    return urls


def extract_total_entries(text: str) -> int | None:
    for pat in [r"Total entries:\s*\*\*(\d+)\*\*", r"总条目数:\s*\*\*(\d+)\*\*"]:
        m = re.search(pat, text)
        if m:
            return int(m.group(1))
    return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--en", default="README.md")
    parser.add_argument("--zh", default="README_zh.md")
    args = parser.parse_args()

    en_path = Path(args.en)
    zh_path = Path(args.zh)
    if not en_path.exists() or not zh_path.exists():
        print("ERROR: README files not found")
        return 1

    en_text = en_path.read_text(encoding="utf-8")
    zh_text = zh_path.read_text(encoding="utf-8")

    en_urls = extract_apply_urls(en_text)
    zh_urls = extract_apply_urls(zh_text)

    en_total = extract_total_entries(en_text)
    zh_total = extract_total_entries(zh_text)

    en_norm = [normalize_url(u) for u in en_urls]
    zh_norm = [normalize_url(u) for u in zh_urls]

    en_dup = [u for u, c in Counter(en_norm).items() if c > 1]
    zh_dup = [u for u, c in Counter(zh_norm).items() if c > 1]

    errors: list[str] = []

    if en_total is None or zh_total is None:
        errors.append("Could not parse total entries from README headers")
    else:
        if en_total != len(en_urls):
            errors.append(f"English total entries mismatch: header={en_total}, links={len(en_urls)}")
        if zh_total != len(zh_urls):
            errors.append(f"Chinese total entries mismatch: header={zh_total}, links={len(zh_urls)}")
        if en_total != zh_total:
            errors.append(f"Header totals differ: en={en_total}, zh={zh_total}")

    if len(en_urls) != len(zh_urls):
        errors.append(f"Link count differs: en={len(en_urls)}, zh={len(zh_urls)}")

    if set(en_norm) != set(zh_norm):
        errors.append("English/Chinese link sets differ")

    if en_dup:
        errors.append(f"English duplicate normalized links: {len(en_dup)}")
    if zh_dup:
        errors.append(f"Chinese duplicate normalized links: {len(zh_dup)}")

    for name in KEY_COMPANIES:
        if name not in en_text:
            errors.append(f"Missing key company in English README: {name}")

    print("Validation Summary")
    print(f"- English links: {len(en_urls)}")
    print(f"- Chinese links: {len(zh_urls)}")
    print(f"- Unique normalized links: {len(set(en_norm))}")
    print(f"- Key companies checked: {', '.join(KEY_COMPANIES)}")
    print(f"- Errors: {len(errors)}")

    if errors:
        print("\nErrors:")
        for err in errors:
            print(f"- {err}")
        return 1

    print("\nValidation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
