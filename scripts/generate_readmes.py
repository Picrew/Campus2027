#!/usr/bin/env python3
from __future__ import annotations

from collections import Counter
from pathlib import Path

LAST_VERIFIED = "2026-04-09"

CATEGORIES = [
    [
        "china_internet",
        "China Internet & Cloud Giants",
        "中国互联网与云大厂"
    ],
    [
        "china_llm",
        "China LLM / AI-Native Companies",
        "中国大模型与 AI 原生公司"
    ],
    [
        "autonomous",
        "Autonomous Driving, Robotics & Embodied AI",
        "自动驾驶、机器人与具身智能"
    ],
    [
        "chips_infra",
        "Chips, AI Infrastructure & Systems",
        "芯片、算力基础设施与系统"
    ],
    [
        "international",
        "International Companies with China Internship Channels",
        "外企与国际公司（中国/大中华实习通道）"
    ]
]

# Keep links official only (company career site / official ATS page).
ENTRIES: list[dict[str, str]] = [
    {
        "cat": "china_internet",
        "company": "ByteDance",
        "focus": "Campus internship portal",
        "itype": "Summer / Daily",
        "location": "China",
        "url": "https://jobs.bytedance.com/campus"
    },
    {
        "cat": "china_internet",
        "company": "ByteDance",
        "focus": "Top Seed - LLM Applied Algorithm Intern",
        "itype": "Summer",
        "location": "Beijing / Shanghai / Shenzhen",
        "url": "https://jobs.bytedance.com/campus/position/7483023182024001799/detail"
    },
    {
        "cat": "china_internet",
        "company": "ByteDance",
        "focus": "Recommender LLM Algorithm Intern",
        "itype": "Summer",
        "location": "Beijing / Shanghai",
        "url": "https://jobs.bytedance.com/campus/position/7475203956567591186/detail"
    },
    {
        "cat": "china_internet",
        "company": "Tencent",
        "focus": "Campus intern portal (AI / engineering)",
        "itype": "Summer / Daily",
        "location": "China",
        "url": "https://join.qq.com/post.html?query=p_2,b_14129"
    },
    {
        "cat": "china_internet",
        "company": "Tencent Games",
        "focus": "Game engineering / AI internship portal",
        "itype": "Summer",
        "location": "Shenzhen / Shanghai",
        "url": "https://join.qq.com/post.html?query=p_2"
    },
    {
        "cat": "china_internet",
        "company": "Alibaba",
        "focus": "Campus internship portal",
        "itype": "Summer",
        "location": "China",
        "url": "https://talent.alibaba.com/campus/position-list?campusType=internship"
    },
    {
        "cat": "china_internet",
        "company": "Baidu",
        "focus": "Campus intern portal (AI / LLM)",
        "itype": "Summer",
        "location": "China",
        "url": "https://talent.baidu.com/jobs/list"
    },
    {
        "cat": "china_internet",
        "company": "Baidu",
        "focus": "LLM risk-scenario algorithm intern",
        "itype": "Summer",
        "location": "Beijing",
        "url": "https://talent.baidu.com/jobs/detail/INTERN/1f5d0a4b-e563-41ad-ac96-b0a75cf89d65"
    },
    {
        "cat": "china_internet",
        "company": "Meituan",
        "focus": "Campus internship portal",
        "itype": "Summer",
        "location": "China",
        "url": "https://zhaopin.meituan.com/web/campus"
    },
    {
        "cat": "china_internet",
        "company": "JD",
        "focus": "Campus internship portal",
        "itype": "Summer",
        "location": "China",
        "url": "https://campus.jd.com/#/jobs"
    },
    {
        "cat": "china_internet",
        "company": "Kuaishou",
        "focus": "Campus internship portal",
        "itype": "Summer / Daily",
        "location": "China",
        "url": "https://campus.kuaishou.cn/#/campus/index"
    },
    {
        "cat": "china_internet",
        "company": "Xiaohongshu (RED)",
        "focus": "Campus internship portal",
        "itype": "Summer / Daily",
        "location": "Beijing / Shanghai / Shenzhen / Hangzhou",
        "url": "https://job.xiaohongshu.com/campus"
    },
    {
        "cat": "china_internet",
        "company": "Bilibili",
        "focus": "Campus internship portal",
        "itype": "Summer / Daily",
        "location": "Beijing / Shanghai / Chongqing",
        "url": "https://jobs.bilibili.com/campus/positions?type=0"
    },
    {
        "cat": "china_internet",
        "company": "PDD",
        "focus": "Campus internship portal",
        "itype": "Summer",
        "location": "China",
        "url": "https://careers.pddglobalhr.net/campus"
    },
    {
        "cat": "china_internet",
        "company": "Xiaomi",
        "focus": "Internship portal",
        "itype": "Summer / Daily",
        "location": "China",
        "url": "https://xiaomi.jobs.f.mioffice.cn/internship/"
    },
    {
        "cat": "china_internet",
        "company": "Huawei",
        "focus": "Campus internship portal",
        "itype": "Summer",
        "location": "China",
        "url": "https://career.huawei.com/reccampportal/portal5/campus-recruitment.html"
    },
    {
        "cat": "china_internet",
        "company": "NetEase Leihuo",
        "focus": "Internship portal",
        "itype": "Summer",
        "location": "Hangzhou",
        "url": "https://leihuo.163.com/campus/#/intern"
    },
    {
        "cat": "china_internet",
        "company": "NetEase Games",
        "focus": "Campus internship portal",
        "itype": "Summer",
        "location": "Hangzhou / Guangzhou",
        "url": "https://game.campus.163.com/position"
    },
    {
        "cat": "china_internet",
        "company": "Trip.com (Ctrip)",
        "focus": "Internship portal",
        "itype": "Summer / Daily",
        "location": "China",
        "url": "https://app.mokahr.com/su/qnjubz"
    },
    {
        "cat": "china_internet",
        "company": "360",
        "focus": "Campus internship portal",
        "itype": "Summer / Daily",
        "location": "Beijing / Nanjing / Shenzhen",
        "url": "https://360campus.zhiye.com/jobs"
    },
    {
        "cat": "china_internet",
        "company": "vivo",
        "focus": "Campus / intern portal",
        "itype": "Summer / Daily",
        "location": "China",
        "url": "https://hr.vivo.com"
    },
    {
        "cat": "china_internet",
        "company": "OPPO",
        "focus": "Campus internship portal",
        "itype": "Summer / Daily",
        "location": "China",
        "url": "https://careers.oppo.com/university/oppo/campus/post?recruitType=Intern"
    },
    {
        "cat": "china_internet",
        "company": "Lenovo",
        "focus": "Internship portal",
        "itype": "Summer / Daily",
        "location": "China",
        "url": "https://talent.lenovo.com.cn/position?projectType=2"
    },
    {
        "cat": "china_internet",
        "company": "WPS / Kingsoft",
        "focus": "Campus internship portal",
        "itype": "Summer / Daily",
        "location": "China",
        "url": "https://app.mokahr.com/campus-recruitment/wps/41436#/jobs?project%5B0%5D=100074177&page=1&anchorName=jobsList"
    },
    {
        "cat": "china_internet",
        "company": "Tencent CSIG",
        "focus": "Cloud / AI platform internship portal",
        "itype": "Summer",
        "location": "Shenzhen / Beijing / Shanghai",
        "url": "https://app-tc.mokahr.com/campus-recruitment/csig/20001#/page/%E5%AE%9E%E4%B9%A0%E7%94%9F%E6%8B%9B%E8%81%98"
    },
    {
        "cat": "china_internet",
        "company": "Qiniu Cloud",
        "focus": "Campus internship portal",
        "itype": "Summer / Daily",
        "location": "Shanghai / Beijing / Shenzhen",
        "url": "https://campus.qiniu.com/campus/jobs"
    },
    {
        "cat": "china_internet",
        "company": "Sangfor",
        "focus": "Campus trainee internship portal",
        "itype": "Summer / Daily",
        "location": "China",
        "url": "https://hr.sangfor.com/campucompon/schoolRecruitment/trainee"
    },
    {
        "cat": "china_internet",
        "company": "SmartX",
        "focus": "AI infra internship portal",
        "itype": "Summer / Daily",
        "location": "Beijing / Shanghai",
        "url": "https://app.mokahr.com/campus_apply/smartx/4183#/jobs?zhineng=111480"
    },
    {
        "cat": "china_internet",
        "company": "Fanruan",
        "focus": "Campus / intern portal",
        "itype": "Summer / Daily",
        "location": "China",
        "url": "https://join.fanruan.com/"
    },
    {
        "cat": "china_internet",
        "company": "Beisen",
        "focus": "Internship portal",
        "itype": "Summer / Daily",
        "location": "China",
        "url": "https://beisen.zhiye.com/intern/jobs"
    },
    {
        "cat": "china_internet",
        "company": "miHoYo",
        "focus": "Campus internship portal",
        "itype": "Summer",
        "location": "Shanghai / Shenzhen",
        "url": "https://jobs.mihoyo.com/#/campus/position"
    },
    {
        "cat": "china_internet",
        "company": "Perfect World",
        "focus": "Campus internship portal",
        "itype": "Summer",
        "location": "Beijing",
        "url": "https://recruit.games.wanmei.com/campus-recruitment/perfect-world/94767/#/"
    },
    {
        "cat": "china_internet",
        "company": "Papergames",
        "focus": "Campus internship portal",
        "itype": "Summer",
        "location": "Shanghai",
        "url": "https://career.papegames.com/campus/position/list?keywords=&category=&location=&project=&type=&job_hot_flag=&current=1&limit=10&functionCategory=&tag="
    },
    {
        "cat": "china_llm",
        "company": "Zhipu AI",
        "focus": "Official careers page",
        "itype": "Summer / Daily",
        "location": "Beijing / Shanghai",
        "url": "https://www.zhipuai.cn/joinus"
    },
    {
        "cat": "china_llm",
        "company": "Zhipu AI",
        "focus": "Official careers page (alt)",
        "itype": "Summer / Daily",
        "location": "Beijing / Shanghai",
        "url": "https://www.zhipuai.cn/careers"
    },
    {
        "cat": "china_llm",
        "company": "Moonshot AI",
        "focus": "Official careers page",
        "itype": "Summer / Daily",
        "location": "Beijing",
        "url": "https://www.moonshot.cn/joinus"
    },
    {
        "cat": "china_llm",
        "company": "Moonshot AI",
        "focus": "Official careers page (alt)",
        "itype": "Summer / Daily",
        "location": "Beijing",
        "url": "https://www.moonshot.cn/careers"
    },
    {
        "cat": "china_llm",
        "company": "MiniMax",
        "focus": "Official careers page",
        "itype": "Summer / Daily",
        "location": "Shanghai / Beijing",
        "url": "https://www.minimax.io/careers"
    },
    {
        "cat": "china_llm",
        "company": "StepFun",
        "focus": "Official ATS portal",
        "itype": "Summer / Daily",
        "location": "Shanghai / Beijing",
        "url": "https://app.mokahr.com/social-recruitment/step/94904#/"
    },
    {
        "cat": "china_llm",
        "company": "DeepSeek / High-Flyer",
        "focus": "Official ATS portal",
        "itype": "Summer / Daily",
        "location": "Hangzhou / Beijing / Shanghai",
        "url": "https://app.mokahr.com/social-recruitment/high-flyer/140576"
    },
    {
        "cat": "china_llm",
        "company": "01.AI",
        "focus": "Official Feishu jobs portal",
        "itype": "Summer / Daily",
        "location": "China",
        "url": "https://01ai.jobs.feishu.cn/index/"
    },
    {
        "cat": "china_llm",
        "company": "Shengshu Technology (Vidu)",
        "focus": "Official Feishu jobs portal",
        "itype": "Summer / Daily",
        "location": "China",
        "url": "https://shengshu.jobs.feishu.cn/index/"
    },
    {
        "cat": "china_llm",
        "company": "SenseTime",
        "focus": "Official join-us page",
        "itype": "Summer / Daily",
        "location": "Shanghai / Shenzhen",
        "url": "https://www.sensetime.com/cn/join-us"
    },
    {
        "cat": "china_llm",
        "company": "Megvii",
        "focus": "Official join-us portal",
        "itype": "Summer / Daily",
        "location": "Beijing / Shanghai",
        "url": "https://joinus.megvii.com"
    },
    {
        "cat": "china_llm",
        "company": "Meshy",
        "focus": "Official Ashby job board",
        "itype": "Summer / Daily",
        "location": "Shanghai",
        "url": "https://jobs.ashbyhq.com/meshy"
    },
    {
        "cat": "china_llm",
        "company": "Baichuan AI",
        "focus": "Official company site",
        "itype": "Summer / Daily",
        "location": "China",
        "url": "https://www.baichuan-ai.com"
    },
    {
        "cat": "china_llm",
        "company": "ModelBest",
        "focus": "Official company site",
        "itype": "Summer / Daily",
        "location": "China",
        "url": "https://www.modelbest.cn"
    },
    {
        "cat": "china_llm",
        "company": "iFlytek",
        "focus": "Official career portal",
        "itype": "Summer / Daily",
        "location": "China",
        "url": "https://career.iflytek.com"
    },
    {
        "cat": "autonomous",
        "company": "NIO",
        "focus": "Internship portal",
        "itype": "Summer / Daily",
        "location": "Shanghai / Beijing / Hefei",
        "url": "https://nio.jobs.feishu.cn/intern/position/"
    },
    {
        "cat": "autonomous",
        "company": "NIO",
        "focus": "Campus internship portal",
        "itype": "Summer",
        "location": "China",
        "url": "https://nio.jobs.feishu.cn/campus/position/"
    },
    {
        "cat": "autonomous",
        "company": "XPeng",
        "focus": "Campus internship portal",
        "itype": "Summer",
        "location": "Guangzhou / Shanghai / Beijing",
        "url": "https://xiaopeng.jobs.feishu.cn/campus/position/list"
    },
    {
        "cat": "autonomous",
        "company": "XPeng",
        "focus": "Official careers landing",
        "itype": "Summer / Daily",
        "location": "China",
        "url": "https://www.xpeng.com/join"
    },
    {
        "cat": "autonomous",
        "company": "Li Auto",
        "focus": "Campus internship portal",
        "itype": "Summer",
        "location": "Beijing / Shanghai / Changzhou",
        "url": "https://www.lixiang.com/employ/campus/list.html"
    },
    {
        "cat": "autonomous",
        "company": "Li Auto",
        "focus": "Internship search page",
        "itype": "Daily",
        "location": "China",
        "url": "https://www.lixiang.com/employ/social/list.html?keyword=%E5%AE%9E%E4%B9%A0&fromJob=1"
    },
    {
        "cat": "autonomous",
        "company": "Geely",
        "focus": "Campus internship portal",
        "itype": "Summer",
        "location": "China",
        "url": "https://campus.geely.com/campus-recruitment/geely/78436/#/jobs?commitment%5B0%5D=%E5%AE%9E%E4%B9%A0&page=1&anchorName=jobsList"
    },
    {
        "cat": "autonomous",
        "company": "DJI",
        "focus": "Campus internship portal",
        "itype": "Summer / Daily",
        "location": "Shenzhen / Shanghai",
        "url": "https://we.dji.com/zh-CN/campus"
    },
    {
        "cat": "autonomous",
        "company": "Pony.ai",
        "focus": "Official careers page",
        "itype": "Summer / Daily",
        "location": "Beijing / Shanghai / Guangzhou",
        "url": "https://www.pony.ai/careers"
    },
    {
        "cat": "autonomous",
        "company": "Momenta",
        "focus": "Official join-us page",
        "itype": "Summer / Daily",
        "location": "Suzhou / Shanghai / Beijing",
        "url": "https://www.momenta.cn/join.html"
    },
    {
        "cat": "autonomous",
        "company": "WeRide",
        "focus": "Official careers page",
        "itype": "Summer / Daily",
        "location": "Guangzhou / Beijing / Shanghai",
        "url": "https://www.weride.ai/careers"
    },
    {
        "cat": "autonomous",
        "company": "Horizon Robotics",
        "focus": "Campus recruiting portal",
        "itype": "Summer / Daily",
        "location": "Beijing / Shanghai / Nanjing",
        "url": "https://horizon-campus.hotjob.cn"
    },
    {
        "cat": "autonomous",
        "company": "Unitree",
        "focus": "Official company site",
        "itype": "Summer / Daily",
        "location": "Hangzhou",
        "url": "https://www.unitree.com"
    },
    {
        "cat": "autonomous",
        "company": "UBTECH",
        "focus": "Official company site",
        "itype": "Summer / Daily",
        "location": "Shenzhen",
        "url": "https://www.ubtrobot.com"
    },
    {
        "cat": "autonomous",
        "company": "AutoX",
        "focus": "Official company site",
        "itype": "Summer / Daily",
        "location": "Shenzhen / Shanghai",
        "url": "https://www.autox.ai"
    },
    {
        "cat": "chips_infra",
        "company": "Cambricon",
        "focus": "Official join-us portal",
        "itype": "Summer / Daily",
        "location": "Beijing / Shanghai",
        "url": "https://joinus.cambricon.com"
    },
    {
        "cat": "chips_infra",
        "company": "Cambricon",
        "focus": "Campus recruitment listing",
        "itype": "Summer",
        "location": "China",
        "url": "https://www.cambricon.com/index.php?m=content&c=index&a=lists&catid=185"
    },
    {
        "cat": "chips_infra",
        "company": "Enflame",
        "focus": "Official company site",
        "itype": "Summer / Daily",
        "location": "Shanghai",
        "url": "https://www.enflame-tech.com"
    },
    {
        "cat": "chips_infra",
        "company": "Intel China Campus",
        "focus": "Official campus portal",
        "itype": "Summer",
        "location": "Beijing / Shanghai / Chengdu",
        "url": "https://chinacampus.jobs.intel.cn/"
    },
    {
        "cat": "chips_infra",
        "company": "AMD",
        "focus": "China internship search",
        "itype": "Summer / Daily",
        "location": "China",
        "url": "https://careers.amd.com/careers-home/jobs?keywords=intern&location=China"
    },
    {
        "cat": "chips_infra",
        "company": "AMD",
        "focus": "Official careers home",
        "itype": "Summer / Daily",
        "location": "China",
        "url": "https://careers.amd.com/careers-home/"
    },
    {
        "cat": "chips_infra",
        "company": "Qualcomm",
        "focus": "China careers page",
        "itype": "Summer / Daily",
        "location": "Beijing / Shanghai",
        "url": "https://www.qualcomm.cn/company/careers"
    },
    {
        "cat": "chips_infra",
        "company": "Qualcomm",
        "focus": "Official careers portal",
        "itype": "Summer / Daily",
        "location": "Global / China",
        "url": "https://careers.qualcomm.com/careers"
    },
    {
        "cat": "chips_infra",
        "company": "NVIDIA",
        "focus": "Official careers portal",
        "itype": "Summer / Daily",
        "location": "China",
        "url": "https://www.nvidia.com/en-us/about-nvidia/careers/"
    },
    {
        "cat": "chips_infra",
        "company": "NVIDIA",
        "focus": "AI in Industry intern (Beijing)",
        "itype": "Summer",
        "location": "Beijing",
        "url": "https://nvidia.wd5.myworkdayjobs.com/en-US/nvidiaexternalcareersite/job/China-Beijing/Solution-Architecture-Intern--AI-in-Industry---2026_JR2014186"
    },
    {
        "cat": "chips_infra",
        "company": "NVIDIA",
        "focus": "Deep Learning & HPC intern (Shanghai)",
        "itype": "Summer",
        "location": "Shanghai",
        "url": "https://nvidia.wd5.myworkdayjobs.com/en-US/nvidiaexternalcareersite/job/China-Shanghai/Performance-Engineer-Intern--Deep-Learning-and-HPC---2026_JR2008053"
    },
    {
        "cat": "chips_infra",
        "company": "Arm",
        "focus": "Official careers portal",
        "itype": "Summer / Daily",
        "location": "Shanghai / Shenzhen",
        "url": "https://www.arm.com/company/careers"
    },
    {
        "cat": "chips_infra",
        "company": "Cadence",
        "focus": "Official careers page",
        "itype": "Summer / Daily",
        "location": "Shanghai / Suzhou",
        "url": "https://www.cadence.com/en_US/home/company/careers.html"
    },
    {
        "cat": "chips_infra",
        "company": "Synopsys",
        "focus": "Official careers portal",
        "itype": "Summer / Daily",
        "location": "Shanghai / Beijing",
        "url": "https://careers.synopsys.com/"
    },
    {
        "cat": "chips_infra",
        "company": "Analog Devices",
        "focus": "Official careers portal",
        "itype": "Summer / Daily",
        "location": "China",
        "url": "https://careers.analog.com/"
    },
    {
        "cat": "chips_infra",
        "company": "STMicroelectronics",
        "focus": "Official careers portal",
        "itype": "Summer / Daily",
        "location": "China",
        "url": "https://careers.st.com/"
    },
    {
        "cat": "chips_infra",
        "company": "Infineon",
        "focus": "Official careers portal",
        "itype": "Summer / Daily",
        "location": "China",
        "url": "https://careers.infineon.com/"
    },
    {
        "cat": "chips_infra",
        "company": "TSMC",
        "focus": "Official careers portal",
        "itype": "Summer / Daily",
        "location": "Greater China",
        "url": "https://careers.tsmc.com/"
    },
    {
        "cat": "chips_infra",
        "company": "ASML",
        "focus": "Official careers portal",
        "itype": "Summer / Daily",
        "location": "China",
        "url": "https://www.asml.com/en/careers"
    },
    {
        "cat": "international",
        "company": "Apple",
        "focus": "China internship search",
        "itype": "Summer / Daily",
        "location": "China",
        "url": "https://jobs.apple.com/zh-cn/search?location=china-mainland"
    },
    {
        "cat": "international",
        "company": "Microsoft",
        "focus": "Students & graduates in China",
        "itype": "Summer / Daily",
        "location": "China",
        "url": "https://jobs.careers.microsoft.com/global/en/search?lc=China&exp=Students%20and%20graduates"
    },
    {
        "cat": "international",
        "company": "Amazon",
        "focus": "Internship search in China",
        "itype": "Summer / Daily",
        "location": "China",
        "url": "https://www.amazon.jobs/en/search?base_query=intern&loc_query=China"
    },
    {
        "cat": "international",
        "company": "AWS",
        "focus": "Official careers page",
        "itype": "Summer / Daily",
        "location": "China / Global",
        "url": "https://aws.amazon.com/careers/"
    },
    {
        "cat": "international",
        "company": "Google",
        "focus": "Jobs search with China location",
        "itype": "Summer / Daily",
        "location": "China",
        "url": "https://careers.google.com/jobs/results/?location=China"
    },
    {
        "cat": "international",
        "company": "IBM",
        "focus": "Official careers portal",
        "itype": "Summer / Daily",
        "location": "China",
        "url": "https://careers.ibm.com/"
    },
    {
        "cat": "international",
        "company": "Dell",
        "focus": "China jobs search",
        "itype": "Summer / Daily",
        "location": "China",
        "url": "https://jobs.dell.com/search-jobs/China"
    },
    {
        "cat": "international",
        "company": "Oracle",
        "focus": "Official careers page",
        "itype": "Summer / Daily",
        "location": "China",
        "url": "https://www.oracle.com/careers/"
    },
    {
        "cat": "international",
        "company": "Oracle",
        "focus": "Official job search portal",
        "itype": "Summer / Daily",
        "location": "China",
        "url": "https://careers.oracle.com/jobs/"
    },
    {
        "cat": "international",
        "company": "SAP",
        "focus": "China location search",
        "itype": "Summer / Daily",
        "location": "China",
        "url": "https://jobs.sap.com/search/?q=&locationsearch=China"
    },
    {
        "cat": "international",
        "company": "Siemens",
        "focus": "Official careers portal",
        "itype": "Summer / Daily",
        "location": "China",
        "url": "https://jobs.siemens.com/careers"
    },
    {
        "cat": "international",
        "company": "Bosch",
        "focus": "China jobs portal",
        "itype": "Summer / Daily",
        "location": "China",
        "url": "https://jobs.bosch.com.cn/jobs?locale=zh_CN"
    },
    {
        "cat": "international",
        "company": "Philips",
        "focus": "Official careers portal",
        "itype": "Summer / Daily",
        "location": "China",
        "url": "https://careers.philips.com/global/en"
    },
    {
        "cat": "international",
        "company": "Sony China",
        "focus": "Official careers portal",
        "itype": "Summer / Daily",
        "location": "China",
        "url": "https://careers.sony.com.cn/"
    },
    {
        "cat": "international",
        "company": "Samsung",
        "focus": "Official careers portal",
        "itype": "Summer / Daily",
        "location": "China",
        "url": "https://careers.samsung.com/"
    },
    {
        "cat": "international",
        "company": "Adobe",
        "focus": "China internship keyword search",
        "itype": "Summer / Daily",
        "location": "China",
        "url": "https://careers.adobe.com/us/en/search-results?keywords=intern&location=china"
    },
    {
        "cat": "international",
        "company": "OpenAI",
        "focus": "Official careers portal",
        "itype": "Summer / Daily",
        "location": "Global / China-based roles if open",
        "url": "https://careers.openai.com/"
    },
    {
        "cat": "international",
        "company": "Optiver",
        "focus": "Shanghai ML PhD internship",
        "itype": "Summer",
        "location": "Shanghai",
        "url": "https://optiver.com/working-at-optiver/career-opportunities/8324932002/?gh_jid=8324932002"
    },
    {
        "cat": "international",
        "company": "Jane Street",
        "focus": "Machine Learning Researcher Internship (Hong Kong)",
        "itype": "Winter",
        "location": "Hong Kong",
        "url": "https://www.janestreet.com/join-jane-street/position/8374335002"
    },
    {
        "cat": "international",
        "company": "Jane Street",
        "focus": "Quantitative Trader Internship (Hong Kong)",
        "itype": "Summer / Winter",
        "location": "Hong Kong",
        "url": "https://www.janestreet.com/join-jane-street/position/7982986002"
    },
    {
        "cat": "international",
        "company": "Jane Street",
        "focus": "Quantitative Researcher Internship (Hong Kong)",
        "itype": "Winter",
        "location": "Hong Kong",
        "url": "https://www.janestreet.com/join-jane-street/position/8343131002"
    },
    {
        "cat": "international",
        "company": "Intel",
        "focus": "Data Science & Analytics Undergraduate Intern (Taipei)",
        "itype": "Summer",
        "location": "Taipei",
        "url": "https://intel.wd1.myworkdayjobs.com/en-US/external/job/Taiwan-Taipei/Data-Science-and-Analytics-Undergraduate---Intern_JR0280981-1"
    },
    {
        "cat": "international",
        "company": "Moloco",
        "focus": "Data Scientist Intern - Growth Analytics (Shanghai)",
        "itype": "Fall/Winter/Spring",
        "location": "Shanghai",
        "url": "https://job-boards.greenhouse.io/moloco/jobs/7632942003"
    },
    {
        "cat": "international",
        "company": "Moloco",
        "focus": "Data Scientist Intern - Growth Analytics (Beijing)",
        "itype": "Fall/Winter/Spring",
        "location": "Beijing",
        "url": "https://job-boards.greenhouse.io/moloco/jobs/7632717003"
    },
    {
        "cat": "international",
        "company": "Ekimetrics",
        "focus": "Strategy & Data Science internship (Shanghai)",
        "itype": "Summer",
        "location": "Shanghai",
        "url": "https://jobs.lever.co/ekimetrics/41495c5a-ce21-48b9-8afc-70c968822b42/apply"
    },
    {
        "cat": "international",
        "company": "AlphaGrep Securities",
        "focus": "Quant Research Intern - Equity Factors (Shanghai)",
        "itype": "Summer",
        "location": "Shanghai",
        "url": "https://job-boards.greenhouse.io/alphagrepsecurities/jobs/7958037002"
    },
    {
        "cat": "international",
        "company": "AlphaGrep Securities",
        "focus": "Quant Research Intern - Machine Learning (Shanghai)",
        "itype": "Summer",
        "location": "Shanghai",
        "url": "https://job-boards.greenhouse.io/alphagrepsecurities/jobs/7958042002"
    },
    {
        "cat": "international",
        "company": "Philips",
        "focus": "Data Analyst/Data Mining Intern (Shanghai)",
        "itype": "Summer",
        "location": "Shanghai",
        "url": "https://philips.wd3.myworkdayjobs.com/en-US/jobs-and-careers/job/Shanghai/---_578274"
    },
    {
        "cat": "international",
        "company": "Philips",
        "focus": "AI Data Scientist Intern (Shanghai)",
        "itype": "Summer",
        "location": "Shanghai",
        "url": "https://philips.wd3.myworkdayjobs.com/en-US/jobs-and-careers/job/Shanghai/Intern---AI-data-scientist_572718"
    },
    {
        "cat": "international",
        "company": "Appier",
        "focus": "Data Analyst Intern (Taiwan)",
        "itype": "Summer",
        "location": "Taiwan",
        "url": "https://job-boards.greenhouse.io/appier/jobs/7495834"
    },
    {
        "cat": "international",
        "company": "Meshy",
        "focus": "Generative AI Pipeline Engineer Intern (Shanghai)",
        "itype": "Summer",
        "location": "Shanghai",
        "url": "https://jobs.ashbyhq.com/meshy/8c30a345-2c26-4d72-ae76-91c5834fc435"
    },
    {
        "cat": "international",
        "company": "Meshy",
        "focus": "Generative AI Researcher Intern (Shanghai)",
        "itype": "Summer",
        "location": "Shanghai",
        "url": "https://jobs.ashbyhq.com/meshy/00b6328d-8c32-4b91-aafa-51434e965f37"
    },
    {
        "cat": "china_internet",
        "company": "Ant Group",
        "focus": "Official careers portal",
        "itype": "Summer / Daily",
        "location": "China",
        "url": "https://www.antgroup.com/careers"
    },
    {
        "cat": "china_internet",
        "company": "Didi",
        "focus": "Official talent portal",
        "itype": "Summer / Daily",
        "location": "China",
        "url": "https://talent.didiglobal.com/"
    },
    {
        "cat": "china_internet",
        "company": "Didi",
        "focus": "Campus internship portal",
        "itype": "Summer",
        "location": "China",
        "url": "https://talent.didiglobal.com/campus"
    },
    {
        "cat": "china_internet",
        "company": "WeBank",
        "focus": "Official careers portal",
        "itype": "Summer / Daily",
        "location": "Shenzhen / Beijing",
        "url": "https://www.webank.com/career"
    },
    {
        "cat": "china_internet",
        "company": "Huawei",
        "focus": "Campus recruiting home",
        "itype": "Summer / Daily",
        "location": "China",
        "url": "https://career.huawei.com/reccampportal/portal5/index.html"
    },
    {
        "cat": "china_internet",
        "company": "Alibaba",
        "focus": "Campus recruiting home",
        "itype": "Summer / Daily",
        "location": "China",
        "url": "https://talent.alibaba.com/campus"
    },
    {
        "cat": "china_internet",
        "company": "Tencent",
        "focus": "Campus recruiting home",
        "itype": "Summer / Daily",
        "location": "China",
        "url": "https://join.qq.com/"
    },
    {
        "cat": "china_internet",
        "company": "Bilibili",
        "focus": "Campus positions list",
        "itype": "Summer / Daily",
        "location": "China",
        "url": "https://jobs.bilibili.com/campus/positions"
    },
    {
        "cat": "china_internet",
        "company": "Lenovo",
        "focus": "Talent portal home",
        "itype": "Summer / Daily",
        "location": "China",
        "url": "https://talent.lenovo.com.cn/"
    },
    {
        "cat": "china_llm",
        "company": "StepFun",
        "focus": "Official company site",
        "itype": "Summer / Daily",
        "location": "China",
        "url": "https://www.stepfun.com/"
    },
    {
        "cat": "china_llm",
        "company": "4Paradigm",
        "focus": "Official company site",
        "itype": "Summer / Daily",
        "location": "China",
        "url": "https://www.4paradigm.com/"
    },
    {
        "cat": "china_llm",
        "company": "AISpeech",
        "focus": "Official company site",
        "itype": "Summer / Daily",
        "location": "China",
        "url": "https://www.aispeech.com/"
    },
    {
        "cat": "china_llm",
        "company": "AISpeech",
        "focus": "Join-us portal",
        "itype": "Summer / Daily",
        "location": "Suzhou / Beijing / Shanghai",
        "url": "https://www.aispeech.com/join-us"
    },
    {
        "cat": "china_llm",
        "company": "Mobvoi",
        "focus": "Official company site",
        "itype": "Summer / Daily",
        "location": "China",
        "url": "https://www.mobvoi.com/"
    },
    {
        "cat": "china_llm",
        "company": "Mobvoi",
        "focus": "Official careers page",
        "itype": "Summer / Daily",
        "location": "China",
        "url": "https://www.mobvoi.com/pages/career"
    },
    {
        "cat": "china_llm",
        "company": "CloudWalk",
        "focus": "Official company site",
        "itype": "Summer / Daily",
        "location": "Guangzhou / Shanghai",
        "url": "https://www.cloudwalk.com/"
    },
    {
        "cat": "china_llm",
        "company": "Intellifusion",
        "focus": "Official company site",
        "itype": "Summer / Daily",
        "location": "Shenzhen / Nanjing",
        "url": "https://www.intellif.com/"
    },
    {
        "cat": "china_llm",
        "company": "SmartMore",
        "focus": "Official company site",
        "itype": "Summer / Daily",
        "location": "Shenzhen / Shanghai",
        "url": "https://www.smartmore.com/"
    },
    {
        "cat": "china_llm",
        "company": "Unisound",
        "focus": "Official company site",
        "itype": "Summer / Daily",
        "location": "Beijing / Hefei",
        "url": "https://www.unisound.com/"
    },
    {
        "cat": "autonomous",
        "company": "BYD",
        "focus": "Official jobs portal",
        "itype": "Summer / Daily",
        "location": "Shenzhen / Xi'an / Changsha",
        "url": "https://job.byd.com/"
    },
    {
        "cat": "autonomous",
        "company": "Tesla China",
        "focus": "China careers search",
        "itype": "Summer / Daily",
        "location": "Shanghai / Beijing / Shenzhen",
        "url": "https://www.tesla.cn/careers/search/?site=CN"
    },
    {
        "cat": "autonomous",
        "company": "Hesai Technology",
        "focus": "Official careers page",
        "itype": "Summer / Daily",
        "location": "Shanghai",
        "url": "https://www.hesaitech.com/careers"
    },
    {
        "cat": "chips_infra",
        "company": "AMD",
        "focus": "China AI jobs search",
        "itype": "Summer / Daily",
        "location": "China",
        "url": "https://careers.amd.com/careers-home/jobs?keywords=AI&location=China"
    },
    {
        "cat": "chips_infra",
        "company": "AMD",
        "focus": "Internship keyword search",
        "itype": "Summer / Daily",
        "location": "China / Global",
        "url": "https://careers.amd.com/careers-home/jobs?keywords=intern"
    },
    {
        "cat": "chips_infra",
        "company": "AMD",
        "focus": "China location jobs search",
        "itype": "Summer / Daily",
        "location": "China",
        "url": "https://careers.amd.com/careers-home/jobs?location=China"
    },
    {
        "cat": "chips_infra",
        "company": "Qualcomm",
        "focus": "Intern keyword search",
        "itype": "Summer / Daily",
        "location": "China / Global",
        "url": "https://careers.qualcomm.com/careers?query=intern"
    },
    {
        "cat": "chips_infra",
        "company": "Applied Materials",
        "focus": "Official careers portal",
        "itype": "Summer / Daily",
        "location": "China",
        "url": "https://careers.appliedmaterials.com/careers"
    },
    {
        "cat": "chips_infra",
        "company": "Lam Research",
        "focus": "Official careers portal",
        "itype": "Summer / Daily",
        "location": "China",
        "url": "https://careers.lamresearch.com/"
    },
    {
        "cat": "chips_infra",
        "company": "MediaTek",
        "focus": "Official careers portal",
        "itype": "Summer / Daily",
        "location": "Mainland China / Taiwan",
        "url": "https://careers.mediatek.com/"
    },
    {
        "cat": "chips_infra",
        "company": "Micron",
        "focus": "Official careers portal",
        "itype": "Summer / Daily",
        "location": "China",
        "url": "https://careers.micron.com/careers"
    },
    {
        "cat": "chips_infra",
        "company": "KLA",
        "focus": "Official job search portal",
        "itype": "Summer / Daily",
        "location": "China",
        "url": "https://kla.wd1.myworkdayjobs.com/Search"
    },
    {
        "cat": "chips_infra",
        "company": "Texas Instruments",
        "focus": "Official careers portal",
        "itype": "Summer / Daily",
        "location": "China",
        "url": "https://www.ti.com/careers"
    },
    {
        "cat": "chips_infra",
        "company": "Biren Technology",
        "focus": "Official company site",
        "itype": "Summer / Daily",
        "location": "Shanghai / Beijing",
        "url": "https://www.birentech.com/"
    },
    {
        "cat": "chips_infra",
        "company": "Iluvatar CoreX",
        "focus": "Official company site",
        "itype": "Summer / Daily",
        "location": "Shanghai / Beijing",
        "url": "https://www.iluvatar.com/"
    },
    {
        "cat": "chips_infra",
        "company": "Iluvatar CoreX",
        "focus": "Official careers page",
        "itype": "Summer / Daily",
        "location": "Shanghai / Beijing",
        "url": "https://www.iluvatar.com/careers"
    },
    {
        "cat": "chips_infra",
        "company": "Loongson",
        "focus": "Official company site",
        "itype": "Summer / Daily",
        "location": "Beijing",
        "url": "https://www.loongson.cn/"
    },
    {
        "cat": "chips_infra",
        "company": "Moore Threads",
        "focus": "Official company site",
        "itype": "Summer / Daily",
        "location": "Beijing",
        "url": "https://www.mthreads.com/"
    },
    {
        "cat": "chips_infra",
        "company": "Cambricon",
        "focus": "Official company site",
        "itype": "Summer / Daily",
        "location": "Beijing / Shanghai",
        "url": "https://www.cambricon.com/"
    },
    {
        "cat": "chips_infra",
        "company": "Intel",
        "focus": "Global jobs portal",
        "itype": "Summer / Daily",
        "location": "China / Global",
        "url": "https://www.intel.com/content/www/us/en/jobs/jobs-at-intel.html"
    },
    {
        "cat": "international",
        "company": "Apple",
        "focus": "Apple careers CN home",
        "itype": "Summer / Daily",
        "location": "China",
        "url": "https://www.apple.com/careers/cn/"
    },
    {
        "cat": "international",
        "company": "Apple",
        "focus": "Machine Learning & AI team search",
        "itype": "Summer / Daily",
        "location": "China / Global",
        "url": "https://jobs.apple.com/zh-cn/search?team=machine-learning-and-ai-SFTWR-MLAI"
    },
    {
        "cat": "international",
        "company": "Apple",
        "focus": "China + ML/AI combined search",
        "itype": "Summer / Daily",
        "location": "China",
        "url": "https://jobs.apple.com/zh-cn/search?location=china-mainland&team=machine-learning-and-ai-SFTWR-MLAI"
    },
    {
        "cat": "international",
        "company": "Amazon",
        "focus": "Internships for students",
        "itype": "Summer / Daily",
        "location": "Global / China filter",
        "url": "https://www.amazon.jobs/en/teams/internships-for-students"
    },
    {
        "cat": "international",
        "company": "Amazon",
        "focus": "ML intern search in China",
        "itype": "Summer / Daily",
        "location": "China",
        "url": "https://www.amazon.jobs/en/search?base_query=machine%20learning%20intern&loc_query=China"
    },
    {
        "cat": "international",
        "company": "Amazon",
        "focus": "Applied Scientist intern search in China",
        "itype": "Summer / Daily",
        "location": "China",
        "url": "https://www.amazon.jobs/en/search?base_query=applied%20scientist%20intern&loc_query=China"
    },
    {
        "cat": "international",
        "company": "Amazon",
        "focus": "AWS intern search in China",
        "itype": "Summer / Daily",
        "location": "China",
        "url": "https://www.amazon.jobs/en/search?base_query=aws%20intern&loc_query=China"
    },
    {
        "cat": "international",
        "company": "Amazon",
        "focus": "Internship search in Beijing",
        "itype": "Summer / Daily",
        "location": "Beijing",
        "url": "https://www.amazon.jobs/en/search?base_query=intern&loc_query=Beijing"
    },
    {
        "cat": "international",
        "company": "Amazon",
        "focus": "Internship search in Shanghai",
        "itype": "Summer / Daily",
        "location": "Shanghai",
        "url": "https://www.amazon.jobs/en/search?base_query=intern&loc_query=Shanghai"
    },
    {
        "cat": "international",
        "company": "Amazon / AWS",
        "focus": "AWS business category page",
        "itype": "Summer / Daily",
        "location": "Global / China filter",
        "url": "https://www.amazon.jobs/en/business_categories/amazon-web-services"
    },
    {
        "cat": "international",
        "company": "Amazon / AWS",
        "focus": "Intern search in AWS business category",
        "itype": "Summer / Daily",
        "location": "Global / China filter",
        "url": "https://www.amazon.jobs/en/search?base_query=intern&business_category%5B%5D=amazon-web-services"
    },
    {
        "cat": "international",
        "company": "Google",
        "focus": "Students and graduates portal",
        "itype": "Summer / Daily",
        "location": "Global",
        "url": "https://careers.google.com/students/"
    },
    {
        "cat": "international",
        "company": "Google",
        "focus": "Jobs in Beijing",
        "itype": "Summer / Daily",
        "location": "Beijing",
        "url": "https://careers.google.com/jobs/results/?location=Beijing,%20China"
    },
    {
        "cat": "international",
        "company": "Google",
        "focus": "Jobs in Shanghai",
        "itype": "Summer / Daily",
        "location": "Shanghai",
        "url": "https://careers.google.com/jobs/results/?location=Shanghai,%20China"
    },
    {
        "cat": "international",
        "company": "Cisco",
        "focus": "Official jobs search",
        "itype": "Summer / Daily",
        "location": "China / Global",
        "url": "https://jobs.cisco.com/jobs/SearchJobs/?21178=%5B164%5D&21178_format=6020&listFilterMode=1"
    },
    {
        "cat": "international",
        "company": "SAP",
        "focus": "Intern keyword search in China",
        "itype": "Summer / Daily",
        "location": "China",
        "url": "https://jobs.sap.com/search/?q=intern&locationsearch=China"
    },
    {
        "cat": "international",
        "company": "Siemens",
        "focus": "Jobs search with China location",
        "itype": "Summer / Daily",
        "location": "China",
        "url": "https://jobs.siemens.com/careers?location=China"
    },
    {
        "cat": "international",
        "company": "HPE",
        "focus": "Intern keyword search",
        "itype": "Summer / Daily",
        "location": "China / Global",
        "url": "https://careers.hpe.com/us/en/search-results?keywords=intern"
    },
    {
        "cat": "international",
        "company": "Nokia",
        "focus": "Official jobs portal",
        "itype": "Summer / Daily",
        "location": "China / Global",
        "url": "https://careers.nokia.com/jobs"
    },
    {
        "cat": "international",
        "company": "Salesforce",
        "focus": "Intern keyword search",
        "itype": "Summer / Daily",
        "location": "China / Global",
        "url": "https://careers.salesforce.com/en/jobs/?search=intern"
    },
    {
        "cat": "international",
        "company": "ServiceNow",
        "focus": "Jobs search with China location",
        "itype": "Summer / Daily",
        "location": "China / Global",
        "url": "https://careers.servicenow.com/careers/jobs?location=china"
    },
    {
        "cat": "international",
        "company": "Snowflake",
        "focus": "Official careers portal",
        "itype": "Summer / Daily",
        "location": "China / Global",
        "url": "https://careers.snowflake.com/"
    },
    {
        "cat": "international",
        "company": "Meta",
        "focus": "Job search: China keyword",
        "itype": "Summer / Daily",
        "location": "China / Global",
        "url": "https://www.metacareers.com/jobsearch?q=china"
    },
    {
        "cat": "international",
        "company": "Meta",
        "focus": "Job search: Intern keyword",
        "itype": "Summer / Daily",
        "location": "Global",
        "url": "https://www.metacareers.com/jobsearch?q=intern"
    },
    {
        "cat": "international",
        "company": "Anthropic",
        "focus": "Official careers portal",
        "itype": "Summer / Daily",
        "location": "Global",
        "url": "https://www.anthropic.com/careers"
    },
    {
        "cat": "international",
        "company": "Cohere",
        "focus": "Official careers portal",
        "itype": "Summer / Daily",
        "location": "Global",
        "url": "https://cohere.com/careers"
    },
    {
        "cat": "international",
        "company": "Mistral AI",
        "focus": "Official careers portal",
        "itype": "Summer / Daily",
        "location": "Global",
        "url": "https://mistral.ai/careers"
    },
    {
        "cat": "international",
        "company": "Databricks",
        "focus": "Official careers portal",
        "itype": "Summer / Daily",
        "location": "China / Global",
        "url": "https://www.databricks.com/company/careers"
    },
    {
        "cat": "international",
        "company": "Cloudflare",
        "focus": "Official careers jobs portal",
        "itype": "Summer / Daily",
        "location": "China / Global",
        "url": "https://www.cloudflare.com/careers/jobs/"
    },
    {
        "cat": "international",
        "company": "Palantir",
        "focus": "Official careers portal",
        "itype": "Summer / Daily",
        "location": "Global",
        "url": "https://www.palantir.com/careers/"
    },
    {
        "cat": "international",
        "company": "Perplexity",
        "focus": "Official careers portal",
        "itype": "Summer / Daily",
        "location": "Global",
        "url": "https://www.perplexity.ai/careers"
    },
    {
        "cat": "international",
        "company": "xAI",
        "focus": "Official careers portal",
        "itype": "Summer / Daily",
        "location": "Global",
        "url": "https://x.ai/careers"
    },
    {
        "cat": "international",
        "company": "DeepMind",
        "focus": "Official careers portal",
        "itype": "Summer / Daily",
        "location": "Global",
        "url": "https://www.deepmind.com/careers"
    },
    {
        "cat": "international",
        "company": "Stripe",
        "focus": "Intern keyword search",
        "itype": "Summer / Daily",
        "location": "Global",
        "url": "https://stripe.com/jobs/search?query=intern"
    },
    {
        "cat": "international",
        "company": "ABB",
        "focus": "Official careers portal",
        "itype": "Summer / Daily",
        "location": "China / Global",
        "url": "https://www.abb.com/careers"
    },
    {
        "cat": "international",
        "company": "Mercedes-Benz",
        "focus": "Official careers portal",
        "itype": "Summer / Daily",
        "location": "China / Global",
        "url": "https://careers.mercedes-benz.com/"
    },
    {
        "cat": "international",
        "company": "Keysight",
        "focus": "Official jobs portal",
        "itype": "Summer / Daily",
        "location": "China / Global",
        "url": "https://jobs.keysight.com/"
    }
]


def count_by_category() -> Counter:
    return Counter(item["cat"] for item in ENTRIES)


def md_escape(text: str) -> str:
    return text.replace("|", "\\|").strip()

COMPANY_ZH_MAP: dict[str, str] = {
    "01.AI": "零一万物",
    "360": "360集团",
    "4Paradigm": "第四范式",
    "ABB": "ABB",
    "AISpeech": "思必驰",
    "AMD": "AMD",
    "ASML": "ASML",
    "AWS": "AWS",
    "Adobe": "Adobe",
    "Alibaba": "阿里巴巴",
    "AlphaGrep Securities": "AlphaGrep",
    "Amazon": "亚马逊",
    "Amazon / AWS": "亚马逊 / AWS",
    "Analog Devices": "亚德诺半导体",
    "Ant Group": "蚂蚁集团",
    "Anthropic": "Anthropic",
    "Appier": "沛星互动",
    "Apple": "苹果",
    "Applied Materials": "应用材料",
    "Arm": "Arm",
    "AutoX": "AutoX",
    "BYD": "比亚迪",
    "Baichuan AI": "百川智能",
    "Baidu": "百度",
    "Beisen": "北森",
    "Bilibili": "哔哩哔哩",
    "Biren Technology": "壁仞科技",
    "Bosch": "博世",
    "ByteDance": "字节跳动",
    "Cadence": "Cadence",
    "Cambricon": "寒武纪",
    "Cisco": "思科",
    "CloudWalk": "云从科技",
    "Cloudflare": "Cloudflare",
    "Cohere": "Cohere",
    "DJI": "大疆",
    "Databricks": "Databricks",
    "DeepMind": "DeepMind",
    "DeepSeek / High-Flyer": "深度求索 / 幻方",
    "Dell": "戴尔",
    "Didi": "滴滴",
    "Ekimetrics": "Ekimetrics",
    "Enflame": "燧原科技",
    "Fanruan": "帆软",
    "Geely": "吉利",
    "Google": "谷歌",
    "HPE": "慧与（HPE）",
    "Hesai Technology": "禾赛科技",
    "Horizon Robotics": "地平线",
    "Huawei": "华为",
    "IBM": "IBM",
    "Iluvatar CoreX": "天数智芯",
    "Infineon": "英飞凌",
    "Intel": "英特尔",
    "Intel China Campus": "英特尔中国校园招聘",
    "Intellifusion": "云天励飞",
    "JD": "京东",
    "Jane Street": "Jane Street",
    "KLA": "KLA",
    "Keysight": "是德科技",
    "Kuaishou": "快手",
    "Lam Research": "泛林集团",
    "Lenovo": "联想",
    "Li Auto": "理想汽车",
    "Loongson": "龙芯中科",
    "MediaTek": "联发科",
    "Megvii": "旷视科技",
    "Meituan": "美团",
    "Mercedes-Benz": "梅赛德斯-奔驰",
    "Meshy": "Meshy",
    "Meta": "Meta",
    "Micron": "美光",
    "Microsoft": "微软",
    "MiniMax": "MiniMax",
    "Mistral AI": "Mistral AI",
    "Mobvoi": "出门问问",
    "ModelBest": "面壁智能",
    "Moloco": "Moloco",
    "Momenta": "Momenta",
    "Moonshot AI": "月之暗面",
    "Moore Threads": "摩尔线程",
    "NIO": "蔚来",
    "NVIDIA": "英伟达",
    "NetEase Games": "网易游戏",
    "NetEase Leihuo": "网易雷火",
    "Nokia": "诺基亚",
    "OPPO": "OPPO",
    "OpenAI": "OpenAI",
    "Optiver": "Optiver",
    "Oracle": "甲骨文",
    "PDD": "拼多多",
    "Palantir": "Palantir",
    "Papergames": "叠纸游戏",
    "Perfect World": "完美世界",
    "Perplexity": "Perplexity",
    "Philips": "飞利浦",
    "Pony.ai": "小马智行",
    "Qiniu Cloud": "七牛云",
    "Qualcomm": "高通",
    "SAP": "SAP",
    "STMicroelectronics": "意法半导体",
    "Salesforce": "Salesforce",
    "Samsung": "三星",
    "Sangfor": "深信服",
    "SenseTime": "商汤科技",
    "ServiceNow": "ServiceNow",
    "Shengshu Technology (Vidu)": "生数科技（Vidu）",
    "Siemens": "西门子",
    "SmartMore": "思谋科技",
    "SmartX": "SmartX",
    "Snowflake": "Snowflake",
    "Sony China": "索尼中国",
    "StepFun": "阶跃星辰",
    "Stripe": "Stripe",
    "Synopsys": "新思科技",
    "TSMC": "台积电",
    "Tencent": "腾讯",
    "Tencent CSIG": "腾讯云与智慧产业事业群（CSIG）",
    "Tencent Games": "腾讯游戏",
    "Tesla China": "特斯拉中国",
    "Texas Instruments": "德州仪器",
    "Trip.com (Ctrip)": "携程集团",
    "UBTECH": "优必选",
    "Unisound": "云知声",
    "Unitree": "宇树科技",
    "WPS / Kingsoft": "金山办公（WPS）",
    "WeBank": "微众银行",
    "WeRide": "文远知行",
    "XPeng": "小鹏汽车",
    "Xiaohongshu (RED)": "小红书",
    "Xiaomi": "小米",
    "Zhipu AI": "智谱 AI",
    "iFlytek": "科大讯飞",
    "miHoYo": "米哈游",
    "vivo": "vivo",
    "xAI": "xAI",
}

FOCUS_ZH_MAP: dict[str, str] = {
    "AI Data Scientist Intern (Shanghai)": "AI 数据科学实习生（上海）",
    "AI in Industry intern (Beijing)": "行业 AI 解决方案实习生（北京）",
    "AI infra internship portal": "AI 基础设施实习投递页",
    "AWS business category page": "AWS 业务分类页面",
    "AWS intern search in China": "中国区 AWS 实习检索",
    "Apple careers CN home": "苹果中国招聘首页",
    "Applied Scientist intern search in China": "中国区应用科学家实习检索",
    "Campus / intern portal": "校园/实习投递页",
    "Campus intern portal (AI / LLM)": "校园实习投递页（AI/大模型）",
    "Campus intern portal (AI / engineering)": "校园实习投递页（AI/工程）",
    "Campus internship portal": "校园实习投递页",
    "Campus positions list": "校园岗位列表",
    "Campus recruiting home": "校园招聘首页",
    "Campus recruiting portal": "校园招聘页面",
    "Campus recruitment listing": "校园招聘列表",
    "Campus trainee internship portal": "校园管培/实习投递页",
    "China + ML/AI combined search": "中国区 + ML/AI 联合检索",
    "China AI jobs search": "中国区 AI 岗位检索",
    "China careers page": "中国区招聘页面",
    "China careers search": "中国区招聘检索",
    "China internship keyword search": "中国区实习关键词检索",
    "China internship search": "中国区实习检索",
    "China jobs portal": "中国区岗位页面",
    "China jobs search": "中国区岗位检索",
    "China location jobs search": "中国地区岗位检索",
    "China location search": "中国地区检索",
    "Cloud / AI platform internship portal": "云计算 / AI 平台实习投递页",
    "Data Analyst Intern (Taiwan)": "数据分析实习生（中国台湾）",
    "Data Analyst/Data Mining Intern (Shanghai)": "数据分析/数据挖掘实习生（上海）",
    "Data Science & Analytics Undergraduate Intern (Taipei)": "数据科学与分析本科实习生（台北）",
    "Data Scientist Intern - Growth Analytics (Beijing)": "数据科学实习生-增长分析（北京）",
    "Data Scientist Intern - Growth Analytics (Shanghai)": "数据科学实习生-增长分析（上海）",
    "Deep Learning & HPC intern (Shanghai)": "深度学习与高性能计算实习生（上海）",
    "Game engineering / AI internship portal": "游戏工程 / AI 实习投递页",
    "Generative AI Pipeline Engineer Intern (Shanghai)": "生成式 AI 流水线工程实习生（上海）",
    "Generative AI Researcher Intern (Shanghai)": "生成式 AI 研究实习生（上海）",
    "Global jobs portal": "全球岗位页面",
    "Intern keyword search": "实习关键词检索",
    "Intern keyword search in China": "中国区实习关键词检索",
    "Intern search in AWS business category": "AWS 分类下实习检索",
    "Internship keyword search": "实习关键词检索",
    "Internship portal": "实习投递页",
    "Internship search in Beijing": "北京实习检索",
    "Internship search in China": "中国区实习检索",
    "Internship search in Shanghai": "上海实习检索",
    "Internship search page": "实习检索页面",
    "Internships for students": "学生实习项目页面",
    "Job search: China keyword": "岗位检索：中国关键词",
    "Job search: Intern keyword": "岗位检索：实习关键词",
    "Jobs in Beijing": "北京岗位检索",
    "Jobs in Shanghai": "上海岗位检索",
    "Jobs search with China location": "中国地区岗位检索",
    "Join-us portal": "招聘页面",
    "LLM risk-scenario algorithm intern": "大模型风控场景算法实习生",
    "ML intern search in China": "中国区机器学习实习检索",
    "Machine Learning & AI team search": "机器学习与 AI 团队检索",
    "Machine Learning Researcher Internship (Hong Kong)": "机器学习研究实习（中国香港）",
    "Official ATS portal": "官方 ATS 投递页",
    "Official Ashby job board": "官方 Ashby 岗位页",
    "Official Feishu jobs portal": "官方飞书招聘页面",
    "Official campus portal": "官方校园招聘页面",
    "Official career portal": "官方招聘页面",
    "Official careers home": "官方招聘首页",
    "Official careers jobs portal": "官方招聘岗位页面",
    "Official careers landing": "官方招聘入口",
    "Official careers page": "官方招聘页面",
    "Official careers page (alt)": "官方招聘页面（备用入口）",
    "Official careers portal": "官方招聘页面",
    "Official company site": "官方网站",
    "Official job search portal": "官方岗位检索页面",
    "Official jobs portal": "官方岗位页面",
    "Official jobs search": "官方岗位检索",
    "Official join-us page": "官方招聘页面",
    "Official join-us portal": "官方招聘页面",
    "Official talent portal": "官方人才招聘页面",
    "Quant Research Intern - Equity Factors (Shanghai)": "量化研究实习生-股票因子（上海）",
    "Quant Research Intern - Machine Learning (Shanghai)": "量化研究实习生-机器学习（上海）",
    "Quantitative Researcher Internship (Hong Kong)": "量化研究实习（中国香港）",
    "Quantitative Trader Internship (Hong Kong)": "量化交易实习（中国香港）",
    "Recommender LLM Algorithm Intern": "推荐大模型算法实习生",
    "Shanghai ML PhD internship": "上海机器学习博士实习",
    "Strategy & Data Science internship (Shanghai)": "战略与数据科学实习（上海）",
    "Students & graduates in China": "中国区学生与毕业生招聘",
    "Students and graduates portal": "学生与毕业生招聘页面",
    "Talent portal home": "人才招聘首页",
    "Top Seed - LLM Applied Algorithm Intern": "Top Seed-大模型应用算法实习生",
}

INTERNSHIP_TYPE_ZH_MAP: dict[str, str] = {
    "Daily": "日常",
    "Fall/Winter/Spring": "秋/冬/春",
    "Summer": "暑期",
    "Summer / Daily": "暑期 / 日常",
    "Summer / Winter": "暑期 / 冬季",
    "Winter": "冬季",
}

LOCATION_ZH_MAP: dict[str, str] = {
    "Beijing": "北京",
    "Beijing / Hefei": "北京 / 合肥",
    "Beijing / Nanjing / Shenzhen": "北京 / 南京 / 深圳",
    "Beijing / Shanghai": "北京 / 上海",
    "Beijing / Shanghai / Changzhou": "北京 / 上海 / 常州",
    "Beijing / Shanghai / Chengdu": "北京 / 上海 / 成都",
    "Beijing / Shanghai / Chongqing": "北京 / 上海 / 重庆",
    "Beijing / Shanghai / Guangzhou": "北京 / 上海 / 广州",
    "Beijing / Shanghai / Nanjing": "北京 / 上海 / 南京",
    "Beijing / Shanghai / Shenzhen": "北京 / 上海 / 深圳",
    "Beijing / Shanghai / Shenzhen / Hangzhou": "北京 / 上海 / 深圳 / 杭州",
    "China": "中国",
    "China / Global": "中国 / 全球",
    "Global": "全球",
    "Global / China": "全球 / 中国",
    "Global / China filter": "全球 / 中国筛选",
    "Global / China-based roles if open": "全球 / 中国地区岗位（如开放）",
    "Greater China": "大中华区",
    "Guangzhou / Beijing / Shanghai": "广州 / 北京 / 上海",
    "Guangzhou / Shanghai": "广州 / 上海",
    "Guangzhou / Shanghai / Beijing": "广州 / 上海 / 北京",
    "Hangzhou": "杭州",
    "Hangzhou / Beijing / Shanghai": "杭州 / 北京 / 上海",
    "Hangzhou / Guangzhou": "杭州 / 广州",
    "Hong Kong": "中国香港",
    "Mainland China / Taiwan": "中国大陆 / 中国台湾",
    "Shanghai": "上海",
    "Shanghai / Beijing": "上海 / 北京",
    "Shanghai / Beijing / Hefei": "上海 / 北京 / 合肥",
    "Shanghai / Beijing / Shenzhen": "上海 / 北京 / 深圳",
    "Shanghai / Shenzhen": "上海 / 深圳",
    "Shanghai / Suzhou": "上海 / 苏州",
    "Shenzhen": "深圳",
    "Shenzhen / Beijing": "深圳 / 北京",
    "Shenzhen / Beijing / Shanghai": "深圳 / 北京 / 上海",
    "Shenzhen / Nanjing": "深圳 / 南京",
    "Shenzhen / Shanghai": "深圳 / 上海",
    "Shenzhen / Xi'an / Changsha": "深圳 / 西安 / 长沙",
    "Suzhou / Beijing / Shanghai": "苏州 / 北京 / 上海",
    "Suzhou / Shanghai / Beijing": "苏州 / 上海 / 北京",
    "Taipei": "台北",
    "Taiwan": "中国台湾",
}


def to_zh_company(company: str) -> str:
    return COMPANY_ZH_MAP.get(company, company)


def to_zh_focus(focus: str) -> str:
    return FOCUS_ZH_MAP.get(focus, focus)


def to_zh_internship_type(itype: str) -> str:
    return INTERNSHIP_TYPE_ZH_MAP.get(itype, itype)


def to_zh_location(location: str) -> str:
    return LOCATION_ZH_MAP.get(location, location)

# Only fill when an explicit deadline is visible on the official page.
DEADLINE_BY_URL: dict[str, str] = {
    "https://jobs.ashbyhq.com/meshy": "2026-07-30",
}


def get_deadline(url: str) -> str:
    return DEADLINE_BY_URL.get(url, "-")


def render_english() -> str:
    counts = count_by_category()
    lines: list[str] = []
    lines.append("# Campus2027")
    lines.append("")
    lines.append("Official LLM internship channels for Class of 2027 students (China focus).")
    lines.append("")
    lines.append(f"- Total entries: **{len(ENTRIES)}**")
    lines.append(f"- Categories: **{len(CATEGORIES)}**")
    lines.append(f"- Last verified: **{LAST_VERIFIED}**")
    lines.append("- Language: [English](./README.md) | [中文](./README_zh.md)")
    lines.append("")
    lines.append("## Category Overview")
    lines.append("")
    lines.append("| Category | Entries |")
    lines.append("| --- | ---: |")
    for key, name_en, _ in CATEGORIES:
        lines.append(f"| {name_en} | {counts.get(key, 0)} |")
    lines.append("")

    for key, name_en, _ in CATEGORIES:
        lines.append(f"## {name_en}")
        lines.append("")
        lines.append("| Company | Team / Focus | Internship Type | Location | Apply Link (Official) | Deadline | Last Verified |")
        lines.append("| --- | --- | --- | --- | --- | --- | --- |")
        for item in [x for x in ENTRIES if x["cat"] == key]:
            lines.append(
                "| "
                + " | ".join(
                    [
                        md_escape(item["company"]),
                        md_escape(item["focus"]),
                        md_escape(item["itype"]),
                        md_escape(item["location"]),
                        f"[Apply]({item['url']})",
                        get_deadline(item["url"]),
                        LAST_VERIFIED,
                    ]
                )
                + " |"
            )
        lines.append("")

    return "\n".join(lines) + "\n"


def render_chinese() -> str:
    counts = count_by_category()
    lines: list[str] = []
    lines.append("# Campus2027")
    lines.append("")
    lines.append("面向 2027 届同学的大模型实习官方投递入口（中国区优先）。")
    lines.append("")
    lines.append(f"- 总条目数: **{len(ENTRIES)}**")
    lines.append(f"- 分类数: **{len(CATEGORIES)}**")
    lines.append(f"- 最近核验: **{LAST_VERIFIED}**")
    lines.append("- 语言: [English](./README.md) | [中文](./README_zh.md)")
    lines.append("")
    lines.append("## 分类总览")
    lines.append("")
    lines.append("| 分类 | 条目数 |")
    lines.append("| --- | ---: |")
    for key, _, name_zh in CATEGORIES:
        lines.append(f"| {name_zh} | {counts.get(key, 0)} |")
    lines.append("")

    for key, _, name_zh in CATEGORIES:
        lines.append(f"## {name_zh}")
        lines.append("")
        lines.append("| 公司 | 团队/方向 | 实习类型 | 地点 | 官方投递链接 | 截止日期 | 最后核验 |")
        lines.append("| --- | --- | --- | --- | --- | --- | --- |")
        for item in [x for x in ENTRIES if x["cat"] == key]:
            lines.append(
                "| "
                + " | ".join(
                    [
                        md_escape(to_zh_company(item["company"])),
                        md_escape(to_zh_focus(item["focus"])),
                        md_escape(to_zh_internship_type(item["itype"])),
                        md_escape(to_zh_location(item["location"])),
                        f"[投递]({item['url']})",
                        get_deadline(item["url"]),
                        LAST_VERIFIED,
                    ]
                )
                + " |"
            )
        lines.append("")

    return "\n".join(lines) + "\n"


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    (root / "README.md").write_text(render_english(), encoding="utf-8")
    (root / "README_zh.md").write_text(render_chinese(), encoding="utf-8")
    print(f"Generated README.md and README_zh.md with {len(ENTRIES)} entries.")


if __name__ == "__main__":
    main()
