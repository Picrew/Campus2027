#!/usr/bin/env python3
from __future__ import annotations

from collections import Counter
from pathlib import Path

LAST_VERIFIED = "2026-07-16"

CATEGORIES = [
    ("platforms", "Internet & AI Platforms", "互联网与 AI 平台"),
    ("ai_programs", "AI Research & Top-Talent Programs", "AI 研究与顶尖人才专项"),
    ("robotics", "Autonomous Driving, Robotics & Embodied AI", "自动驾驶、机器人与具身智能"),
    ("chips", "Chips, Vision & Infrastructure", "芯片、视觉与基础设施"),
    ("other", "Games, Financial Data & Research Institutes", "游戏、金融数据与科研院所"),
]

# Inclusion rule: an application must be open for a Class of 2027 full-time
# graduate role, early batch, or named top-talent program on LAST_VERIFIED.
# Internships, campus ambassadors, "coming soon" pages, and 2026 make-up hiring
# are intentionally excluded.
ENTRIES: list[dict[str, str]] = [
    {
        "cat": "platforms",
        "company": "ByteDance Seed",
        "company_zh": "字节跳动 Seed",
        "focus": "Seed Foundation Model Campus Recruitment",
        "focus_zh": "Seed 大模型人才校招",
        "batch": "Class of 2027 full-time",
        "batch_zh": "2027 届正式岗",
        "audience": "Graduating Sep 2026-Aug 2027 (B/M/PhD)",
        "audience_zh": "2026.09-2027.08 毕业的本/硕/博",
        "location": "Beijing / Shanghai / Shenzhen / Hangzhou",
        "location_zh": "北京 / 上海 / 深圳 / 杭州",
        "opens": "2026-04-01",
        "deadline": "Not announced",
        "deadline_zh": "未公布",
        "url": "https://seed.bytedance.com/zh/seedearlycareer",
        "evidence_url": "https://seed.bytedance.com/zh/blog/bytedance-seed-2027-foundation-model-campus-recruitment-is-now-open-internships-included",
        "evidence": "A: official campaign page",
        "evidence_zh": "A：官网专项页",
    },
    {
        "cat": "platforms",
        "company": "ByteDance",
        "company_zh": "字节跳动",
        "focus": "Frontier Technology Talent Campus Recruitment",
        "focus_zh": "前沿技术领域人才校招",
        "batch": "Class of 2027+ full-time",
        "batch_zh": "2027 届及以后正式岗",
        "audience": "Class of 2027 and later; role-specific requirements",
        "audience_zh": "2027 届及以后；以岗位要求为准",
        "location": "China / Global",
        "location_zh": "中国 / 全球",
        "opens": "Open",
        "deadline": "Not announced",
        "deadline_zh": "未公布",
        "url": "https://jobs.bytedance.com/campus/position",
        "evidence_url": "https://jobs.bytedance.com/campus/page-6272Gc",
        "evidence": "A: official FAQ confirms cohort",
        "evidence_zh": "A：官网 FAQ 明确届别",
    },
    {
        "cat": "platforms",
        "company": "ByteDance",
        "company_zh": "字节跳动",
        "focus": "AI Product Manager Early-Bird Interview",
        "focus_zh": "AI 产品经理早鸟通道",
        "batch": "Fall early batch / interview event",
        "batch_zh": "秋招提前批 / 面试专场",
        "audience": "Graduating Sep 2026-Aug 2027",
        "audience_zh": "2026.09-2027.08 毕业",
        "location": "Beijing / Shanghai / Shenzhen",
        "location_zh": "北京 / 上海 / 深圳",
        "opens": "2026-07-14",
        "deadline": "2026-07-31",
        "deadline_zh": "2026-07-31",
        "url": "https://wj.toutiao.com/q/v2/7657509120173735979/975xOc70/4d7d/#/",
        "evidence_url": "https://career.cuhk.edu.cn/job/view/id/468770",
        "evidence": "B: official form + employer notice repost",
        "evidence_zh": "B：官方问卷 + 企业公告转载",
    },
    {
        "cat": "platforms",
        "company": "Tencent",
        "company_zh": "腾讯",
        "focus": "Qingyun Program 2027",
        "focus_zh": "2027 青云计划",
        "batch": "Top AI talent program",
        "batch_zh": "顶尖 AI 人才专项",
        "audience": "Graduating Jan 2026-Dec 2027 (B/M/PhD)",
        "audience_zh": "2026.01-2027.12 毕业的本/硕/博",
        "location": "China / US / Singapore / Europe",
        "location_zh": "中国 / 美国 / 新加坡 / 欧洲",
        "opens": "2026-07-15",
        "deadline": "Not announced",
        "deadline_zh": "未公布",
        "url": "https://join.qq.com/",
        "evidence_url": "https://www.yicai.com/news/103276437.html",
        "evidence": "B: official portal + launch report",
        "evidence_zh": "B：官网入口 + 启动报道",
    },
    {
        "cat": "platforms",
        "company": "Alibaba",
        "company_zh": "阿里巴巴",
        "focus": "AliStar 2027 Graduate Program",
        "focus_zh": "阿里星 2027 届应届生招聘",
        "batch": "Top research talent program",
        "batch_zh": "顶尖科研人才专项",
        "audience": "Graduating Nov 2026-Oct 2027",
        "audience_zh": "2026.11-2027.10 毕业",
        "location": "China",
        "location_zh": "中国",
        "opens": "2026-06-22",
        "deadline": "Not announced",
        "deadline_zh": "未公布",
        "url": "https://campus-talent.alibaba.com/campus/alistar",
        "evidence_url": "https://campus-talent.alibaba.com/campus/trends",
        "evidence": "A: official campaign page",
        "evidence_zh": "A：官网专项页",
    },
    {
        "cat": "platforms",
        "company": "Baidu",
        "company_zh": "百度",
        "focus": "2027 Campus Recruitment (incl. AIDU / trainee)",
        "focus_zh": "2027 届校招（含 AIDU / 管培生）",
        "batch": "Fall recruitment / talent programs",
        "batch_zh": "秋招 / 人才专项",
        "audience": "Graduating Sep 2026-Aug 2027",
        "audience_zh": "2026.09-2027.08 毕业",
        "location": "Beijing / Shanghai / Shenzhen / others",
        "location_zh": "北京 / 上海 / 深圳 / 其他",
        "opens": "2026-07-09",
        "deadline": "2027-06",
        "deadline_zh": "2027-06",
        "url": "https://talent.baidu.com/jobs/list?recruitType=GRADUATE",
        "evidence_url": "https://talent.baidu.com/jobs/campus",
        "evidence": "A: official campaign page",
        "evidence_zh": "A：官网校招页",
    },
    {
        "cat": "platforms",
        "company": "PDD",
        "company_zh": "拼多多",
        "focus": "2027 Graduate Recruitment / Top Tech Track",
        "focus_zh": "2027 届应届生招聘 / 顶尖技术人才专项",
        "batch": "Fall recruitment",
        "batch_zh": "秋招",
        "audience": "Graduating Sep 2026-Aug 2027",
        "audience_zh": "2026.09-2027.08 毕业",
        "location": "China",
        "location_zh": "中国",
        "opens": "Open by 2026-07-09",
        "deadline": "Not announced",
        "deadline_zh": "未公布",
        "url": "https://careers.pddglobalhr.com/campus/grad",
        "evidence_url": "https://careers.pddglobalhr.com/campus/",
        "evidence": "A: official site shows 2027 project",
        "evidence_zh": "A：官网明确显示 2027 项目",
    },
    {
        "cat": "platforms",
        "company": "Meituan",
        "company_zh": "美团",
        "focus": "Beidou Program 2027",
        "focus_zh": "2027 届北斗计划",
        "batch": "Top AI talent program",
        "batch_zh": "顶尖 AI 人才专项",
        "audience": "Graduating Jan 2026-Dec 2027",
        "audience_zh": "2026.01-2027.12 毕业",
        "location": "Beijing / Shanghai / Shenzhen / Chengdu / Global",
        "location_zh": "北京 / 上海 / 深圳 / 成都 / 全球",
        "opens": "2026-06-11",
        "deadline": "Rolling",
        "deadline_zh": "全年滚动",
        "url": "https://zhaopin.meituan.com/web/campus?bg=BGCLC",
        "evidence_url": "https://pjcareer.dlut.edu.cn/info/1091/44132.htm",
        "evidence": "B: official portal + employer notice repost",
        "evidence_zh": "B：官网入口 + 企业公告转载",
    },
    {
        "cat": "platforms",
        "company": "JD",
        "company_zh": "京东",
        "focus": "TET 2027 Management Trainee",
        "focus_zh": "2027 届 TET 管理培训生",
        "batch": "Early talent program",
        "batch_zh": "人才专项提前批",
        "audience": "Graduating Oct 2026-Sep 2027",
        "audience_zh": "2026.10-2027.09 毕业",
        "location": "Beijing / Suqian / business locations",
        "location_zh": "北京 / 宿迁 / 各业务所在地",
        "opens": "2026-07-01",
        "deadline": "2026-10-31",
        "deadline_zh": "2026-10-31",
        "url": "https://campus.jd.com/#/jobs",
        "evidence_url": "https://www.nowcoder.com/jobs/detail/453018",
        "evidence": "B: official portal + verified employer listing",
        "evidence_zh": "B：官网入口 + 企业认证岗位",
    },
    {
        "cat": "platforms",
        "company": "Xiaomi",
        "company_zh": "小米",
        "focus": "Top-Talent Graduate Recruitment",
        "focus_zh": "顶尖人才应届生招聘",
        "batch": "Top AI talent program",
        "batch_zh": "顶尖 AI 人才专项",
        "audience": "Graduated 2024-2027; postdocs leaving in 2027",
        "audience_zh": "2024-2027 届应届生及 2027 年出站博士后",
        "location": "China / Global",
        "location_zh": "中国 / 全球",
        "opens": "Open",
        "deadline": "Not announced",
        "deadline_zh": "未公布",
        "url": "https://hr.xiaomi.com/campus/",
        "evidence_url": "https://hr.xiaomi.com/website/top-talent.html",
        "evidence": "A: official top-talent page",
        "evidence_zh": "A：官网顶尖人才页",
    },
    {
        "cat": "platforms",
        "company": "Huawei",
        "company_zh": "华为",
        "focus": "Class of 2027 Top AI Talent Initiative",
        "focus_zh": "2027 届顶尖 AI 人才专项",
        "batch": "Top AI talent program",
        "batch_zh": "顶尖 AI 人才专项",
        "audience": "Class of 2027; role-specific degree requirements",
        "audience_zh": "2027 届；学历以岗位要求为准",
        "location": "China / Global",
        "location_zh": "中国 / 全球",
        "opens": "2026-05-19",
        "deadline": "Not announced",
        "deadline_zh": "未公布",
        "url": "https://career.huawei.com/cn/campus-recruitment",
        "evidence_url": "https://career.huawei.com/cn/campus-recruitment",
        "evidence": "A: official activity and apply page",
        "evidence_zh": "A：官网活动及投递页",
    },
    {
        "cat": "ai_programs",
        "company": "iFlytek",
        "company_zh": "科大讯飞",
        "focus": "Feixing Program 2027",
        "focus_zh": "2027 届飞星计划",
        "batch": "Research-algorithm early batch",
        "batch_zh": "研究算法提前批",
        "audience": "Class of 2027 Master's / PhD graduates",
        "audience_zh": "2027 届硕士 / 博士",
        "location": "Hefei / Beijing / Xi'an / Guangzhou / Shanghai",
        "location_zh": "合肥 / 北京 / 西安 / 广州 / 上海",
        "opens": "2026-06-14",
        "deadline": "Not announced",
        "deadline_zh": "未公布",
        "url": "https://iflytek.zhiye.com/4/jobs",
        "evidence_url": "https://career.nankai.edu.cn/correcruit/content/id/116162.html",
        "evidence": "B: official ATS + employer notice repost",
        "evidence_zh": "B：官方 ATS + 企业公告转载",
    },
    {
        "cat": "ai_programs",
        "company": "iFlytek",
        "company_zh": "科大讯飞",
        "focus": "Feifan Program 2027",
        "focus_zh": "2027 届飞凡计划",
        "batch": "Future-leader early batch",
        "batch_zh": "未来领导者提前批",
        "audience": "Class of 2027; major unrestricted",
        "audience_zh": "2027 届；专业不限",
        "location": "Hefei",
        "location_zh": "合肥",
        "opens": "Open by 2026-07-02",
        "deadline": "Not announced",
        "deadline_zh": "未公布",
        "url": "https://iflytek.zhiye.com/5/jobs",
        "evidence_url": "https://ejob.dhu.edu.cn/single/2026/07/02/2607021423534921003320030219103058410002.html",
        "evidence": "B: official ATS + employer notice repost",
        "evidence_zh": "B：官方 ATS + 企业公告转载",
    },
    {
        "cat": "robotics",
        "company": "DJI",
        "company_zh": "大疆",
        "focus": "2027 Pioneer Campus Recruitment",
        "focus_zh": "2027“拓疆者”校园招聘",
        "batch": "Fall recruitment",
        "batch_zh": "秋招",
        "audience": "Class of 2027 graduates",
        "audience_zh": "2027 届高校毕业生",
        "location": "Shenzhen / Shanghai / Xi'an / others",
        "location_zh": "深圳 / 上海 / 西安 / 其他",
        "opens": "2026-06-25",
        "deadline": "Rolling until filled",
        "deadline_zh": "招满即止",
        "url": "https://careers.dji.com/zh-CN/campus/recruitment?from=sec_nav",
        "evidence_url": "https://careers.dji.com/zh-CN/campus/recruitment?from=sec_nav",
        "evidence": "A: official campaign page",
        "evidence_zh": "A：官网专项页",
    },
    {
        "cat": "robotics",
        "company": "XPeng",
        "company_zh": "小鹏集团",
        "focus": "Explorer Program 2027",
        "focus_zh": "2027 届“探索者计划”",
        "batch": "Global campus recruitment",
        "batch_zh": "全球校园招聘",
        "audience": "Graduating Sep 2026-Aug 2027",
        "audience_zh": "2026.09-2027.08 毕业",
        "location": "Guangzhou / Shenzhen / Shanghai / Beijing / Global",
        "location_zh": "广州 / 深圳 / 上海 / 北京 / 全球",
        "opens": "2026-07-07",
        "deadline": "Not announced",
        "deadline_zh": "未公布",
        "url": "https://xiaopeng.jobs.feishu.cn/campus/position/list",
        "evidence_url": "https://career.hebut.edu.cn/correcruit/content/id/78926.html",
        "evidence": "B: official ATS + employer notice repost",
        "evidence_zh": "B：官方 ATS + 企业公告转载",
    },
    {
        "cat": "robotics",
        "company": "Pudu Robotics",
        "company_zh": "普渡机器人",
        "focus": "Class of 2027 Campus Recruitment",
        "focus_zh": "2027 届校园招聘",
        "batch": "Fall recruitment",
        "batch_zh": "秋招",
        "audience": "Graduating Jan-Dec 2027",
        "audience_zh": "2027.01-2027.12 毕业",
        "location": "Shenzhen / Chengdu / others",
        "location_zh": "深圳 / 成都 / 其他",
        "opens": "2026-06-26",
        "deadline": "Rolling",
        "deadline_zh": "滚动招聘",
        "url": "https://pudutech.zhiye.com/campus",
        "evidence_url": "https://career.nankai.edu.cn/correcruit/content/id/116156.html",
        "evidence": "B: official ATS + employer notice repost",
        "evidence_zh": "B：官方 ATS + 企业公告转载",
    },
    {
        "cat": "robotics",
        "company": "Hesai Technology",
        "company_zh": "禾赛科技",
        "focus": "Class of 2027 Fall Early Batch",
        "focus_zh": "2027 届秋招提前批",
        "batch": "Fall early batch",
        "batch_zh": "秋招提前批",
        "audience": "Class of 2027 graduates",
        "audience_zh": "2027 届毕业生",
        "location": "Shanghai / Hangzhou",
        "location_zh": "上海 / 杭州",
        "opens": "2026-06-16",
        "deadline": "2026-08-31",
        "deadline_zh": "2026-08-31",
        "url": "https://kwh0jtf778.jobs.feishu.cn/229043/",
        "evidence_url": "https://hzau.91wllm.cn/news/view/aid/298571/tag/xwzp",
        "evidence": "B: official ATS + employer notice repost",
        "evidence_zh": "B：官方 ATS + 企业公告转载",
    },
    {
        "cat": "robotics",
        "company": "AgiBot",
        "company_zh": "智元机器人",
        "focus": "2027 Outstanding Talent Program",
        "focus_zh": "2027 届优才计划",
        "batch": "Embodied-AI top-talent program",
        "batch_zh": "具身智能顶尖人才专项",
        "audience": "Class of 2027 Master's / PhD graduates",
        "audience_zh": "2027 届硕士 / 博士",
        "location": "Shanghai / Beijing / Shenzhen",
        "location_zh": "上海 / 北京 / 深圳",
        "opens": "Open by 2026-06-26",
        "deadline": "Not announced",
        "deadline_zh": "未公布",
        "url": "https://agirobot.jobs.feishu.cn/946993/position/list",
        "evidence_url": "https://ejob.dhu.edu.cn/pros_wjdc/s/cms/DongHua/single/2026/06/26/26062610362142818624",
        "evidence": "B: official ATS + employer notice repost",
        "evidence_zh": "B：官方 ATS + 企业公告转载",
    },
    {
        "cat": "chips",
        "company": "ZTE",
        "company_zh": "中兴通讯",
        "focus": "2027 Future Leaders Recruitment",
        "focus_zh": "2027 届未来领军人才招聘",
        "batch": "Top-talent early batch",
        "batch_zh": "顶尖人才提前批",
        "audience": "Class of 2027; role-specific requirements",
        "audience_zh": "2027 届；以岗位要求为准",
        "location": "China / Global",
        "location_zh": "中国 / 全球",
        "opens": "2026-06-29",
        "deadline": "Not announced",
        "deadline_zh": "未公布",
        "url": "https://job.zte.com.cn/cn/campus-recruitment",
        "evidence_url": "https://job.zte.com.cn/cn/campus-recruitment/School_Recruitment_Announcement/news/202406061.html",
        "evidence": "A: official announcement",
        "evidence_zh": "A：官网公告",
    },
    {
        "cat": "chips",
        "company": "MediaTek",
        "company_zh": "联发科技",
        "focus": "Class of 2027 Campus Early Batch",
        "focus_zh": "2027 届校园招聘提前批",
        "batch": "Fall early batch",
        "batch_zh": "秋招提前批",
        "audience": "Class of 2027 graduates",
        "audience_zh": "2027 届毕业生",
        "location": "Beijing / Shanghai / Shenzhen / Chengdu / Hefei / Wuhan",
        "location_zh": "北京 / 上海 / 深圳 / 成都 / 合肥 / 武汉",
        "opens": "2026-07-11",
        "deadline": "Not announced",
        "deadline_zh": "未公布",
        "url": "https://mediatek.zhiye.com/campus/jobs",
        "evidence_url": "https://mp.weixin.qq.com/s/7PbNs1897a6QgmWoXYflEA",
        "evidence": "B: official ATS + official account notice",
        "evidence_zh": "B：官方 ATS + 官方号公告",
    },
    {
        "cat": "chips",
        "company": "ASML",
        "company_zh": "ASML 阿斯麦",
        "focus": "Class of 2027 China Campus Recruitment",
        "focus_zh": "2027 届中国校园招聘",
        "batch": "Fall recruitment",
        "batch_zh": "秋招",
        "audience": "Class of 2027 graduates (Bachelor's degree or above)",
        "audience_zh": "2027 届本科及以上毕业生",
        "location": "Beijing / Shanghai / Hefei",
        "location_zh": "北京 / 上海 / 合肥",
        "opens": "Open by 2026-07-07",
        "deadline": "Not announced",
        "deadline_zh": "未公布",
        "url": "https://www.asml.com/en/careers/find-your-job",
        "evidence_url": "https://sfi.cuhk.edu.cn/zh-hans/node/10816",
        "evidence": "B: official job portal + employer notice repost",
        "evidence_zh": "B：官网投递入口 + 企业公告转载",
    },
    {
        "cat": "chips",
        "company": "ArcSoft",
        "company_zh": "虹软科技",
        "focus": "Class of 2027 Fall Early Batch",
        "focus_zh": "2027 届秋招提前批",
        "batch": "CV / AIGC early batch",
        "batch_zh": "视觉 / AIGC 提前批",
        "audience": "Class of 2027 graduates",
        "audience_zh": "2027 届毕业生",
        "location": "Hangzhou / Shanghai / Nanjing / Shenzhen / Global",
        "location_zh": "杭州 / 上海 / 南京 / 深圳 / 全球",
        "opens": "2026-07-10",
        "deadline": "2026-08-20",
        "deadline_zh": "2026-08-20",
        "url": "https://www.arcsoft.com.cn/job/JobList.html",
        "evidence_url": "https://mp.weixin.qq.com/s/soNYJJNGMAkhUxy37vd9xg",
        "evidence": "B: official career page + official notice",
        "evidence_zh": "B：官网投递页 + 官方公告",
    },
    {
        "cat": "chips",
        "company": "Southchip",
        "company_zh": "南芯科技",
        "focus": "Class of 2027 Campus Recruitment",
        "focus_zh": "2027 届校园招聘",
        "batch": "Fall recruitment",
        "batch_zh": "秋招",
        "audience": "Class of 2027 graduates",
        "audience_zh": "2027 届毕业生",
        "location": "Shanghai / Chengdu / Shenzhen / Beijing / others",
        "location_zh": "上海 / 成都 / 深圳 / 北京 / 其他",
        "opens": "2026-07-11",
        "deadline": "Not announced",
        "deadline_zh": "未公布",
        "url": "https://www.southchip.com/recruitment",
        "evidence_url": "https://mp.weixin.qq.com/s/YuEhQAMXIodLyuav0MiwVg",
        "evidence": "B: official career page + official notice",
        "evidence_zh": "B：官网招聘页 + 官方公告",
    },
    {
        "cat": "chips",
        "company": "Silergy",
        "company_zh": "矽力杰",
        "focus": "Class of 2027 Campus Recruitment",
        "focus_zh": "2027 届校园招聘",
        "batch": "Fall recruitment",
        "batch_zh": "秋招",
        "audience": "Class of 2027 graduates",
        "audience_zh": "2027 届毕业生",
        "location": "Suzhou / Hangzhou / Shanghai / Shenzhen / others",
        "location_zh": "苏州 / 杭州 / 上海 / 深圳 / 其他",
        "opens": "2026-07-11",
        "deadline": "Not announced",
        "deadline_zh": "未公布",
        "url": "https://campus.51job.com/m/xz-xlj/",
        "evidence_url": "https://mp.weixin.qq.com/s/mWitINflW-NJAjPlhagDVA",
        "evidence": "B: official campaign site + official notice",
        "evidence_zh": "B：官方校招站 + 官方公告",
    },
    {
        "cat": "other",
        "company": "miHoYo",
        "company_zh": "米哈游",
        "focus": "Class of 2027 Technical Early Batch",
        "focus_zh": "2027 校招技术提前批",
        "batch": "Fall technical early batch",
        "batch_zh": "秋招技术提前批",
        "audience": "Graduating Sep 2026-Aug 2027",
        "audience_zh": "2026.09-2027.08 毕业",
        "location": "Shanghai / Beijing",
        "location_zh": "上海 / 北京",
        "opens": "2026-07-06",
        "deadline": "2026-07-27",
        "deadline_zh": "2026-07-27",
        "url": "https://campus.mihoyo.com/",
        "evidence_url": "https://campus.mihoyo.com/",
        "evidence": "A: official campaign page",
        "evidence_zh": "A：官网专项页",
    },
    {
        "cat": "other",
        "company": "Wind Information",
        "company_zh": "万得信息（Wind）",
        "focus": "2027 Campus Recruitment",
        "focus_zh": "2027 年校园招聘",
        "batch": "Graduate recruitment",
        "batch_zh": "应届生招聘",
        "audience": "Graduating Sep 2026-Aug 2027",
        "audience_zh": "2026.09-2027.08 毕业",
        "location": "Shanghai / Nanjing / Beijing / others",
        "location_zh": "上海 / 南京 / 北京 / 其他",
        "opens": "Open",
        "deadline": "Not announced",
        "deadline_zh": "未公布",
        "url": "https://www.wind.com.cn/portal/zh/JoinUs/recruit.html",
        "evidence_url": "https://www.wind.com.cn/portal/zh/JoinUs/recruit.html",
        "evidence": "A: official page shows 2027 roles",
        "evidence_zh": "A：官网明确显示 2027 岗位",
    },
    {
        "cat": "other",
        "company": "CAS Technology and Engineering Center for Space Utilization",
        "company_zh": "中科院空间应用工程与技术中心",
        "focus": "Class of 2027 Campus Recruitment",
        "focus_zh": "2027 届校园招聘",
        "batch": "Research institute graduate recruitment",
        "batch_zh": "科研院所应届生招聘",
        "audience": "Class of 2027 graduates; role-specific degrees",
        "audience_zh": "2027 届；学历以岗位要求为准",
        "location": "Beijing",
        "location_zh": "北京",
        "opens": "2026-04-21",
        "deadline": "2026-12-31",
        "deadline_zh": "2026-12-31",
        "url": "https://csu.zhiye.com/AllJob",
        "evidence_url": "https://csu.cas.cn/gb/yjdw/rczp/202604/t20260421_8188165.html",
        "evidence": "A: official institute announcement",
        "evidence_zh": "A：研究所官网公告",
    },
]

WATCHLIST: list[dict[str, str]] = [
    {
        "company": "Tencent regular campus hiring",
        "company_zh": "腾讯常规校招",
        "status": "Official site still shows 2026; only Qingyun 2027 is counted above.",
        "status_zh": "官网常规项目仍显示 2026 届；本表仅计入已启动的 2027 青云计划。",
        "url": "https://careers.tencent.com/campusrecruit.html",
    },
    {
        "company": "ByteDance regular graduate hiring",
        "company_zh": "字节跳动常规应届生招聘",
        "status": "Official FAQ still lists the 2026 window; only named 2027 projects are counted.",
        "status_zh": "官网 FAQ 常规应届生仍为 2026 届窗口；仅计入上方 2027 专项。",
        "url": "https://jobs.bytedance.com/campus",
    },
    {
        "company": "Alibaba regular graduate hiring",
        "company_zh": "阿里巴巴常规应届生招聘",
        "status": "AliStar is open; a separate broad 2027 fall batch was not verified.",
        "status_zh": "阿里星已开放；尚未核验到独立的 2027 常规秋招大批次。",
        "url": "https://campus-talent.alibaba.com/",
    },
    {
        "company": "Meituan regular graduate hiring",
        "company_zh": "美团常规应届生招聘",
        "status": "Beidou is open; the regular 2027 full-time list was not verified as open.",
        "status_zh": "北斗计划已开放；常规 2027 正式岗尚未核验为开放。",
        "url": "https://zhaopin.meituan.com/web/campus",
    },
    {
        "company": "Huawei regular graduate hiring",
        "company_zh": "华为常规应届生招聘",
        "status": "Official regular page still targets 2026; only the 2027 top-AI initiative is counted.",
        "status_zh": "官网常规应届生仍面向 2026 届；仅计入 2027 顶尖 AI 专项。",
        "url": "https://career.huawei.com/cn/campus-recruitment",
    },
    {
        "company": "Xiaomi regular graduate hiring",
        "company_zh": "小米常规应届生招聘",
        "status": "Official regular page still shows 2026; only top-talent graduate hiring is counted.",
        "status_zh": "官网常规项目仍显示 2026 届；仅计入顶尖人才应届生招聘。",
        "url": "https://hr.xiaomi.com/campus/",
    },
    {
        "company": "Kuaishou / Xiaohongshu / Bilibili / NetEase Games",
        "company_zh": "快手 / 小红书 / 哔哩哔哩 / 网易游戏",
        "status": "No cohort-specific 2027 full-time fall window verified on official portals.",
        "status_zh": "官方入口尚未核验到明确的 2027 届正式秋招窗口。",
        "url": "https://campus.kuaishou.cn/",
    },
    {
        "company": "OPPO / vivo / Honor",
        "company_zh": "OPPO / vivo / 荣耀",
        "status": "No explicit 2027 full-time fall window verified; current pages are generic or older cohorts.",
        "status_zh": "尚未核验到明确的 2027 届正式秋招窗口；当前为通用入口或旧届别。",
        "url": "https://careers.oppo.com/university/oppo/campus",
    },
    {
        "company": "NIO / Li Auto / Horizon Robotics / Pony.ai",
        "company_zh": "蔚来 / 理想汽车 / 地平线 / 小马智行",
        "status": "Official portals are live, but a 2027 full-time fall cohort was not verified.",
        "status_zh": "官网可访问，但尚未核验到 2027 届正式秋招批次。",
        "url": "https://nio.jobs.feishu.cn/campus/position/",
    },
    {
        "company": "Cambricon / Moore Threads / Biren Technology",
        "company_zh": "寒武纪 / 摩尔线程 / 壁仞科技",
        "status": "Campus portals exist; no explicit open 2027 full-time window verified.",
        "status_zh": "存在校招入口，但尚未核验到明确开放的 2027 届正式岗窗口。",
        "url": "https://joinus.cambricon.com/",
    },
    {
        "company": "DeepSeek / Moonshot AI / MiniMax / Zhipu AI",
        "company_zh": "深度求索 / 月之暗面 / MiniMax / 智谱 AI",
        "status": "General/social or internship channels only; no cohort-specific 2027 fall batch verified.",
        "status_zh": "当前主要为社招/通用或实习入口，尚未核验到 2027 届秋招批次。",
        "url": "https://app.mokahr.com/social-recruitment/high-flyer/140576",
    },
    {
        "company": "SenseTime",
        "company_zh": "商汤科技",
        "status": "A new talent campaign was announced, but cohort eligibility was not explicit on the official landing page; withheld pending confirmation.",
        "status_zh": "已发布新人才专项，但官网落地页未明确 2027 届口径，待确认后再收录。",
        "url": "https://hr.sensetime.com/",
    },
]

# Kept for the weekly scanner's compatibility. Only explicit deadlines belong
# here; "rolling" and "not announced" are intentionally omitted.
DEADLINE_BY_URL = {
    item["url"]: item["deadline"]
    for item in ENTRIES
    if item["deadline"][:4].isdigit()
}


def md_escape(text: str) -> str:
    return text.replace("|", "\\|").strip()


def localize_open_date(value: str) -> str:
    if value == "Open":
        return "已开放"
    if value.startswith("Open by "):
        return "不晚于 " + value.removeprefix("Open by ")
    return value


def count_by_category() -> Counter:
    return Counter(item["cat"] for item in ENTRIES)


def render_header(lines: list[str], *, chinese: bool) -> None:
    lines.append("# Campus2027")
    lines.append("")
    if chinese:
        lines.append("面向 2027 届同学的**秋季校园招聘正式岗**与提前批官方投递入口（中国区、AI/技术方向优先）。")
        lines.append("")
        lines.append(f"- 已确认开放: **{len(ENTRIES)}** 个入口")
        lines.append(f"- 分类数: **{len(CATEGORIES)}**")
        lines.append(f"- 最近核验: **{LAST_VERIFIED}**")
        lines.append("- 语言: [English](./README.md) | [中文](./README_zh.md)")
        lines.append("")
        lines.append("> 口径提醒：这里是**秋招正式岗**清单，不收录仅有实习、校园大使、预告未开放或 2026 届补录的项目。截止日期仅在公开页面明确给出时填写；“未公布”不等于长期有效，请尽早投递。")
    else:
        lines.append("Official application channels for **Class of 2027 full-time fall campus recruitment** and early batches, prioritizing China-based AI and technical roles.")
        lines.append("")
        lines.append(f"- Confirmed open: **{len(ENTRIES)}** application channels")
        lines.append(f"- Categories: **{len(CATEGORIES)}**")
        lines.append(f"- Last verified: **{LAST_VERIFIED}**")
        lines.append("- Language: [English](./README.md) | [中文](./README_zh.md)")
        lines.append("")
        lines.append("> Scope: this is a **full-time fall recruiting** list. Internship-only, campus-ambassador, not-yet-open, and Class of 2026 make-up campaigns are excluded. A deadline is shown only when explicitly published; “not announced” can still mean the role will close without notice.")
    lines.append("")


def render_overview(lines: list[str], *, chinese: bool) -> None:
    counts = count_by_category()
    lines.append("## 分类总览" if chinese else "## Category Overview")
    lines.append("")
    lines.append("| 分类 | 已开放入口 |" if chinese else "| Category | Open Channels |")
    lines.append("| --- | ---: |")
    for key, en, zh in CATEGORIES:
        lines.append(f"| {zh if chinese else en} | {counts.get(key, 0)} |")
    lines.append("")
    if chinese:
        lines.append("核验等级：**A** = 公司/研究所官网直接写明届别与项目；**B** = 官方投递入口可用，项目窗口由企业官方号公告或高校转载的企业公告交叉核验。")
    else:
        lines.append("Evidence grade: **A** = the company/institute site explicitly states cohort and campaign; **B** = the official application portal is live and the window is cross-checked against an employer notice or its university repost.")
    lines.append("")


def render_entries(lines: list[str], *, chinese: bool) -> None:
    for key, en, zh in CATEGORIES:
        lines.append(f"## {zh if chinese else en}")
        lines.append("")
        if chinese:
            lines.append("| 公司 | 项目/方向 | 批次 | 招聘对象 | 地点 | 开放时间 | 截止日期 | 官方投递 | 核验依据 | 最后核验 |")
        else:
            lines.append("| Company | Program / Focus | Batch | Audience | Location | Opens | Deadline | Official Apply | Evidence | Last Verified |")
        lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
        for item in (entry for entry in ENTRIES if entry["cat"] == key):
            values = [
                item["company_zh"] if chinese else item["company"],
                item["focus_zh"] if chinese else item["focus"],
                item["batch_zh"] if chinese else item["batch"],
                item["audience_zh"] if chinese else item["audience"],
                item["location_zh"] if chinese else item["location"],
                localize_open_date(item["opens"]) if chinese else item["opens"],
                item["deadline_zh"] if chinese else item["deadline"],
                f"[投递]({item['url']})" if chinese else f"[Apply]({item['url']})",
                f"[依据]({item['evidence_url']}) {item['evidence_zh']}" if chinese else f"[Source]({item['evidence_url']}) {item['evidence']}",
                LAST_VERIFIED,
            ]
            lines.append("| " + " | ".join(md_escape(value) for value in values) + " |")
        lines.append("")


def render_watchlist(lines: list[str], *, chinese: bool) -> None:
    lines.append("## 已核验但未计入主表" if chinese else "## Checked but Not Counted as Open")
    lines.append("")
    if chinese:
        lines.append("这些公司不是漏掉，而是截至核验日尚不满足“2027 届正式秋招已开放”的严格口径。")
        lines.append("")
        lines.append("| 公司/组别 | 核验结论 | 官方入口 | 最后核验 |")
    else:
        lines.append("These companies were checked and intentionally withheld because they did not yet meet the strict “open Class of 2027 full-time fall recruitment” rule.")
        lines.append("")
        lines.append("| Company / Group | Finding | Official Portal | Last Verified |")
    lines.append("| --- | --- | --- | --- |")
    for item in WATCHLIST:
        values = [
            item["company_zh"] if chinese else item["company"],
            item["status_zh"] if chinese else item["status"],
            f"[查看]({item['url']})" if chinese else f"[Check]({item['url']})",
            LAST_VERIFIED,
        ]
        lines.append("| " + " | ".join(md_escape(value) for value in values) + " |")
    lines.append("")


def render_methodology(lines: list[str], *, chinese: bool) -> None:
    lines.append("## 核验方法" if chinese else "## Verification Method")
    lines.append("")
    if chinese:
        lines.extend([
            "1. 先检查公司官网、官方招聘站或公司专属 ATS 是否出现 2027 届正式岗/提前批。",
            "2. 对动态页面，再用企业官方号公告或高校转载的企业招聘简章交叉确认开放日期、对象与截止日期。",
            "3. 投递链接只保留公司域名、公司专属 ATS 或公司官方活动问卷；不放个人内推链接和聚合站跳转链接。",
            "4. 如果页面只写“实习可转正”，仍按实习处理，不计入本秋招主表。",
        ])
    else:
        lines.extend([
            "1. Check the company site, official recruiting site, or company-branded ATS for an open Class of 2027 full-time/early-batch campaign.",
            "2. For dynamic pages, cross-check opening dates, eligibility, and deadlines against employer notices or university reposts of those notices.",
            "3. Keep only company domains, company-branded ATS pages, and official event forms as application links; personal referral and aggregator redirects are excluded.",
            "4. An internship with a conversion path remains an internship and is not counted in this fall full-time list.",
        ])
    lines.append("")


def render_english() -> str:
    lines: list[str] = []
    render_header(lines, chinese=False)
    render_overview(lines, chinese=False)
    render_entries(lines, chinese=False)
    render_watchlist(lines, chinese=False)
    render_methodology(lines, chinese=False)
    return "\n".join(lines) + "\n"


def render_chinese() -> str:
    lines: list[str] = []
    render_header(lines, chinese=True)
    render_overview(lines, chinese=True)
    render_entries(lines, chinese=True)
    render_watchlist(lines, chinese=True)
    render_methodology(lines, chinese=True)
    return "\n".join(lines) + "\n"


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    (root / "README.md").write_text(render_english(), encoding="utf-8")
    (root / "README_zh.md").write_text(render_chinese(), encoding="utf-8")
    print(f"Generated README.md and README_zh.md with {len(ENTRIES)} open fall-recruiting entries.")


if __name__ == "__main__":
    main()
