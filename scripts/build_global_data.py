#!/usr/bin/env python3
"""Build data/global.json and data/global.js from embedded reference dataset."""
import json
import os

# 50-year basic wind/snow pressure (kN/m²), reference values per national codes.
# Overseas values are engineering references; verify with local official maps for projects.

GLOBAL = {
    "us": {
        "nameZh": "美国", "nameEn": "United States",
        "code": "ASCE/SEI 7-16",
        "codeZh": "美国最低设计荷载规范 ASCE/SEI 7-16",
        "codeEn": "ASCE/SEI 7-16 Minimum Design Loads",
        "regions": {
            "东北部": {"纽约": [0.50, 0.30], "波士顿": [0.55, 0.35], "费城": [0.50, 0.30], "匹兹堡": [0.45, 0.35]},
            "五大湖": {"芝加哥": [0.50, 0.40], "底特律": [0.45, 0.40], "克利夫兰": [0.45, 0.40], "明尼阿波利斯": [0.45, 0.45]},
            "中大西洋": {"华盛顿": [0.50, 0.30], "巴尔的摩": [0.50, 0.30], "里士满": [0.45, 0.25]},
            "南部": {"亚特兰大": [0.50, 0.15], "达拉斯": [0.52, 0.20], "休斯顿": [0.60, 0.15], "新奥尔良": [0.65, 0.10]},
            "佛罗里达": {"迈阿密": [0.75, 0.10], "坦帕": [0.65, 0.10], "杰克逊维尔": [0.60, 0.10]},
            "西部": {"洛杉矶": [0.45, 0.12], "旧金山": [0.48, 0.15], "西雅图": [0.48, 0.22], "波特兰": [0.45, 0.20]},
            "山地": {"丹佛": [0.45, 0.35], "盐湖城": [0.42, 0.35], "凤凰城": [0.42, 0.08]},
            "阿拉斯加": {"安克雷奇": [0.53, 0.55], "费尔班克斯": [0.45, 0.60]},
            "夏威夷": {"檀香山": [0.68, 0.08]},
        },
    },
    "ca": {
        "nameZh": "加拿大", "nameEn": "Canada",
        "code": "NBC 2020", "codeZh": "加拿大国家建筑规范 NBC 2020", "codeEn": "National Building Code of Canada 2020",
        "regions": {
            "东部": {"多伦多": [0.50, 0.40], "渥太华": [0.45, 0.45], "蒙特利尔": [0.48, 0.50], "魁北克": [0.50, 0.55]},
            "西部": {"温哥华": [0.50, 0.30], "维多利亚": [0.48, 0.25], "卡尔加里": [0.49, 0.44], "埃德蒙顿": [0.52, 0.48]},
            "草原": {"温尼伯": [0.48, 0.50], "里贾纳": [0.50, 0.45], "萨斯卡通": [0.50, 0.48]},
            "大西洋": {"哈利法克斯": [0.55, 0.45], "圣约翰": [0.58, 0.50]},
        },
    },
    "mx": {
        "nameZh": "墨西哥", "nameEn": "Mexico",
        "code": "NTC-RCDF / CFE", "codeZh": "墨西哥建筑法规 NTC-RCDF", "codeEn": "NTC-RCDF Mexico Building Code",
        "regions": {
            "中部": {"墨西哥城": [0.44, 0.20], "瓜达拉哈拉": [0.42, 0.15], "普埃布拉": [0.42, 0.15]},
            "北部": {"蒙特雷": [0.47, 0.18], "蒂华纳": [0.45, 0.12], "奇瓦瓦": [0.45, 0.20]},
            "东部": {"坎昆": [0.72, 0.10], "韦拉克鲁斯": [0.60, 0.10], "梅里达": [0.55, 0.10]},
            "西部": {"马萨特兰": [0.55, 0.10], "蒂华纳": [0.45, 0.12]},
        },
    },
    "br": {
        "nameZh": "巴西", "nameEn": "Brazil",
        "code": "ABNT NBR 6123/8681", "codeZh": "巴西风荷载 NBR 6123 / 雪荷载 NBR 8681", "codeEn": "ABNT NBR 6123 Wind / NBR 8681 Snow",
        "regions": {
            "东南部": {"圣保罗": [0.45, 0.20], "里约热内卢": [0.55, 0.15], "贝洛奥里藏特": [0.42, 0.15], "库里蒂巴": [0.45, 0.15]},
            "南部": {"阿雷格里港": [0.48, 0.20], "弗洛里亚诺波利斯": [0.55, 0.15], "波尔图阿莱格里": [0.50, 0.18]},
            "东北部": {"萨尔瓦多": [0.52, 0.10], "累西腓": [0.55, 0.10], "福塔莱萨": [0.50, 0.10]},
            "北部": {"马瑙斯": [0.49, 0.12], "贝伦": [0.48, 0.10], "巴西利亚": [0.42, 0.12]},
        },
    },
    "ar": {
        "nameZh": "阿根廷", "nameEn": "Argentina",
        "code": "CIRSOC 102/103", "codeZh": "阿根廷 CIRSOC 102/103", "codeEn": "CIRSOC 102 Wind / 103 Snow",
        "regions": {
            "东部": {"布宜诺斯艾利斯": [0.48, 0.22], "罗萨里奥": [0.45, 0.18], "拉普拉塔": [0.48, 0.20]},
            "西部": {"门多萨": [0.43, 0.26], "科尔多瓦": [0.42, 0.18], "图库曼": [0.42, 0.15]},
            "南部": {"乌斯怀亚": [0.55, 0.35], "里奥加耶戈斯": [0.60, 0.40]},
            "北部": {"萨尔塔": [0.40, 0.15], "胡胡伊": [0.40, 0.12]},
        },
    },
    "cl": {
        "nameZh": "智利", "nameEn": "Chile",
        "code": "NCh 433/432", "codeZh": "智利 NCh 433/432", "codeEn": "NCh 433 Seismic / NCh 432 Loads",
        "regions": {
            "中部": {"圣地亚哥": [0.47, 0.21], "瓦尔帕莱索": [0.51, 0.23], "康塞普西翁": [0.52, 0.25]},
            "北部": {"安托法加斯塔": [0.56, 0.16], "阿里卡": [0.50, 0.12], "伊基克": [0.52, 0.14]},
            "南部": {"蓬塔阿雷纳斯": [0.65, 0.35], "蒙特港": [0.55, 0.30], "特木科": [0.50, 0.25]},
        },
    },
    "co": {
        "nameZh": "哥伦比亚", "nameEn": "Colombia",
        "code": "NSR-10 / NSC 101", "codeZh": "哥伦比亚 NSR-10", "codeEn": "NSR-10 Colombia Building Code",
        "regions": {
            "安第斯": {"波哥大": [0.46, 0.14], "麦德林": [0.45, 0.12], "卡利": [0.44, 0.12]},
            "加勒比": {"巴兰基亚": [0.55, 0.10], "卡塔赫纳": [0.58, 0.10], "圣玛尔塔": [0.60, 0.10]},
            "东部": {"比亚维森西奥": [0.44, 0.12]},
        },
    },
    "pe": {
        "nameZh": "秘鲁", "nameEn": "Peru",
        "code": "E.030 / E.020", "codeZh": "秘鲁 E.030 风荷载", "codeEn": "Peru E.030 Wind Loads",
        "regions": {
            "沿海": {"利马": [0.52, 0.10], "特鲁希略": [0.48, 0.10], "皮乌拉": [0.45, 0.10]},
            "山区": {"库斯科": [0.40, 0.15], "阿雷基帕": [0.42, 0.12]},
            "东部": {"伊基托斯": [0.45, 0.10]},
        },
    },
    "de": {
        "nameZh": "德国", "nameEn": "Germany",
        "code": "DIN EN 1991-1-3/4", "codeZh": "德国 DIN EN 1991-1-3/4", "codeEn": "DIN EN 1991-1-3 Snow / 1-4 Wind",
        "regions": {
            "北部": {"汉堡": [0.50, 0.25], "不来梅": [0.50, 0.25], "基尔": [0.52, 0.28]},
            "中部": {"柏林": [0.40, 0.30], "法兰克福": [0.42, 0.28], "汉诺威": [0.45, 0.30]},
            "南部": {"慕尼黑": [0.42, 0.45], "斯图加特": [0.42, 0.35], "纽伦堡": [0.42, 0.38]},
            "西部": {"科隆": [0.45, 0.28], "杜塞尔多夫": [0.45, 0.28], "多特蒙德": [0.45, 0.30]},
        },
    },
    "fr": {
        "nameZh": "法国", "nameEn": "France",
        "code": "NF EN 1991-1-3/4", "codeZh": "法国 NF EN 1991-1-3/4", "codeEn": "NF EN 1991-1-3 Snow / 1-4 Wind",
        "regions": {
            "巴黎盆地": {"巴黎": [0.40, 0.25], "奥尔良": [0.40, 0.25], "兰斯": [0.42, 0.28]},
            "地中海": {"马赛": [0.50, 0.12], "尼斯": [0.52, 0.12], "蒙彼利埃": [0.48, 0.15]},
            "大西洋": {"波尔多": [0.45, 0.18], "南特": [0.48, 0.20], "布雷斯特": [0.55, 0.20]},
            "阿尔卑斯": {"里昂": [0.42, 0.35], "格勒诺布尔": [0.42, 0.45], "斯特拉斯堡": [0.42, 0.35]},
        },
    },
    "gb": {
        "nameZh": "英国", "nameEn": "United Kingdom",
        "code": "BS EN 1991-1-3/4", "codeZh": "英国 BS EN 1991-1-3/4", "codeEn": "BS EN 1991-1-3 Snow / 1-4 Wind",
        "regions": {
            "英格兰": {"伦敦": [0.50, 0.20], "伯明翰": [0.45, 0.25], "曼彻斯特": [0.48, 0.28], "利物浦": [0.50, 0.25]},
            "苏格兰": {"爱丁堡": [0.55, 0.35], "格拉斯哥": [0.55, 0.35], "阿伯丁": [0.58, 0.38]},
            "威尔士": {"加的夫": [0.52, 0.25], "斯旺西": [0.55, 0.22]},
            "北爱尔兰": {"贝尔法斯特": [0.55, 0.28]},
        },
    },
    "it": {
        "nameZh": "意大利", "nameEn": "Italy",
        "code": "NTC 2018 / UNI EN 1991", "codeZh": "意大利 NTC 2018", "codeEn": "NTC 2018 Italy Building Code",
        "regions": {
            "北部": {"米兰": [0.42, 0.35], "都灵": [0.42, 0.40], "威尼斯": [0.45, 0.30]},
            "中部": {"罗马": [0.45, 0.20], "佛罗伦萨": [0.42, 0.22], "那不勒斯": [0.48, 0.15]},
            "南部": {"巴勒莫": [0.50, 0.12], "卡塔尼亚": [0.52, 0.12], "巴里": [0.48, 0.15]},
            "岛屿": {"卡利亚里": [0.52, 0.12]},
        },
    },
    "es": {
        "nameZh": "西班牙", "nameEn": "Spain",
        "code": "CTE DB-SE-AE", "codeZh": "西班牙 CTE DB-SE-AE", "codeEn": "CTE DB-SE-AE Spain Structural Code",
        "regions": {
            "中部": {"马德里": [0.40, 0.18], "萨拉曼卡": [0.40, 0.22], "萨拉戈萨": [0.42, 0.22]},
            "地中海": {"巴塞罗那": [0.45, 0.15], "瓦伦西亚": [0.48, 0.12], "马拉加": [0.50, 0.12]},
            "北部": {"毕尔巴鄂": [0.50, 0.25], "圣地亚哥": [0.52, 0.22], "桑坦德": [0.52, 0.25]},
            "群岛": {"拉斯帕尔马斯": [0.55, 0.10], "特内里费": [0.52, 0.10]},
        },
    },
    "nl": {
        "nameZh": "荷兰", "nameEn": "Netherlands",
        "code": "NEN EN 1991-1-3/4", "codeZh": "荷兰 NEN EN 1991", "codeEn": "NEN EN 1991-1-3/4",
        "regions": {
            "西部": {"阿姆斯特丹": [0.50, 0.25], "鹿特丹": [0.52, 0.25], "海牙": [0.52, 0.25]},
            "东部": {"格罗宁根": [0.48, 0.28], "阿纳姆": [0.45, 0.28]},
        },
    },
    "ch": {
        "nameZh": "瑞士", "nameEn": "Switzerland",
        "code": "SIA 261 / SN EN 1991", "codeZh": "瑞士 SIA 261", "codeEn": "SIA 261 Swiss Standard",
        "regions": {
            "高原": {"苏黎世": [0.42, 0.35], "伯尔尼": [0.42, 0.40], "巴塞尔": [0.42, 0.32]},
            "阿尔卑斯": {"日内瓦": [0.42, 0.35], "洛桑": [0.42, 0.35], "圣莫里茨": [0.45, 0.55]},
        },
    },
    "se": {
        "nameZh": "瑞典", "nameEn": "Sweden",
        "code": "BFS EN 1991", "codeZh": "瑞典 BFS EN 1991", "codeEn": "BFS EN 1991-1-3/4 Sweden",
        "regions": {
            "南部": {"斯德哥尔摩": [0.45, 0.40], "哥德堡": [0.48, 0.38], "马尔默": [0.48, 0.35]},
            "北部": {"吕勒奥": [0.50, 0.55], "于默奥": [0.48, 0.50]},
        },
    },
    "no": {
        "nameZh": "挪威", "nameEn": "Norway",
        "code": "NS EN 1991", "codeZh": "挪威 NS EN 1991", "codeEn": "NS EN 1991-1-3/4 Norway",
        "regions": {
            "南部": {"奥斯陆": [0.45, 0.45], "卑尔根": [0.55, 0.40], "斯塔万格": [0.52, 0.35]},
            "北部": {"特罗姆瑟": [0.55, 0.60], "博德": [0.55, 0.55]},
        },
    },
    "ru": {
        "nameZh": "俄罗斯", "nameEn": "Russia",
        "code": "СП 20.13330.2016", "codeZh": "俄罗斯 SP 20.13330", "codeEn": "SP 20.13330.2016 Russia Loads",
        "regions": {
            "中央": {"莫斯科": [0.50, 0.50], "下诺夫哥罗德": [0.48, 0.50], "沃罗涅日": [0.45, 0.45]},
            "西北": {"圣彼得堡": [0.55, 0.45], "摩尔曼斯克": [0.60, 0.55], "阿尔汉格尔斯克": [0.55, 0.55]},
            "西伯利亚": {"新西伯利亚": [0.48, 0.55], "克拉斯诺亚尔斯克": [0.45, 0.55], "伊尔库茨克": [0.42, 0.50]},
            "远东": {"海参崴": [0.58, 0.42], "哈巴罗夫斯克": [0.55, 0.48], "雅库茨克": [0.45, 0.65]},
            "南部": {"索契": [0.52, 0.20], "顿河畔罗斯托夫": [0.48, 0.30], "喀山": [0.48, 0.48]},
        },
    },
    "jp": {
        "nameZh": "日本", "nameEn": "Japan",
        "code": "AIJ Recommendations / BSL", "codeZh": "日本建筑学会 AIJ 风荷重 / 建筑基准法", "codeEn": "AIJ Wind Loads / Building Standards Law",
        "regions": {
            "关东": {"东京": [0.50, 0.25], "横滨": [0.52, 0.25], "千叶": [0.52, 0.22], "埼玉": [0.48, 0.25]},
            "关西": {"大阪": [0.50, 0.25], "京都": [0.48, 0.28], "神户": [0.52, 0.22]},
            "九州": {"福冈": [0.55, 0.20], "长崎": [0.58, 0.18], "鹿儿岛": [0.60, 0.15]},
            "东北": {"仙台": [0.52, 0.40], "盛冈": [0.48, 0.50], "青森": [0.55, 0.55]},
            "北海道": {"札幌": [0.48, 0.55], "函馆": [0.55, 0.50]},
            "冲绳": {"那霸": [0.70, 0.10], "石垣": [0.75, 0.08]},
        },
    },
    "kr": {
        "nameZh": "韩国", "nameEn": "South Korea",
        "code": "KDS 41 10 / 41 30", "codeZh": "韩国 KDS 41 10 风 / 41 30 雪", "codeEn": "KDS 41 10 Wind / 41 30 Snow",
        "regions": {
            "首都圈": {"首尔": [0.48, 0.28], "仁川": [0.52, 0.28], "水原": [0.48, 0.28]},
            "东南": {"釜山": [0.58, 0.22], "大邱": [0.48, 0.25], "蔚山": [0.58, 0.22]},
            "济州": {"济州岛": [0.68, 0.15], "西归浦": [0.65, 0.15]},
            "中部": {"大田": [0.45, 0.28], "光州": [0.48, 0.22]},
        },
    },
    "in": {
        "nameZh": "印度", "nameEn": "India",
        "code": "IS 875 Part 3/4", "codeZh": "印度 IS 875 第3/4部分", "codeEn": "IS 875 Part 3 Wind / Part 4 Snow",
        "regions": {
            "北部": {"新德里": [0.40, 0.25], "昌迪加尔": [0.42, 0.28], "勒克瑙": [0.42, 0.22]},
            "西部": {"孟买": [0.50, 0.15], "艾哈迈达巴德": [0.45, 0.12], "浦那": [0.45, 0.15]},
            "南部": {"班加罗尔": [0.42, 0.18], "钦奈": [0.52, 0.12], "海德拉巴": [0.45, 0.15], "科钦": [0.55, 0.10]},
            "东部": {"加尔各答": [0.48, 0.15], "布巴内斯瓦尔": [0.52, 0.12]},
            "喜马拉雅": {"西姆拉": [0.42, 0.45], "列城": [0.45, 0.55]},
        },
    },
    "sg": {
        "nameZh": "新加坡", "nameEn": "Singapore",
        "code": "SS CP 4 / SS EN 1991", "codeZh": "新加坡 SS CP 4", "codeEn": "SS CP 4 Singapore Wind Code",
        "regions": {"全境": {"新加坡": [0.62, 0.12], "裕廊": [0.60, 0.12]}},
    },
    "my": {
        "nameZh": "马来西亚", "nameEn": "Malaysia",
        "code": "MS 1553 / MS 1554", "codeZh": "马来西亚 MS 1553/1554", "codeEn": "MS 1553 Wind / MS 1554 Imposed",
        "regions": {
            "半岛": {"吉隆坡": [0.58, 0.12], "槟城": [0.55, 0.12], "新山": [0.55, 0.10], "关丹": [0.58, 0.10]},
            "东马": {"古晋": [0.65, 0.10], "亚庇": [0.62, 0.10], "哥打京那巴鲁": [0.60, 0.10]},
        },
    },
    "th": {
        "nameZh": "泰国", "nameEn": "Thailand",
        "code": "TIS 1030 / DPT 1301", "codeZh": "泰国 TIS 1030", "codeEn": "TIS 1030 Thailand Wind Loads",
        "regions": {
            "中部": {"曼谷": [0.52, 0.14], "大城": [0.50, 0.14], "呵叻": [0.48, 0.14]},
            "南部": {"普吉": [0.66, 0.10], "宋卡": [0.58, 0.10], "合艾": [0.55, 0.10]},
            "北部": {"清迈": [0.45, 0.14], "清莱": [0.42, 0.15]},
        },
    },
    "vn": {
        "nameZh": "越南", "nameEn": "Vietnam",
        "code": "TCVN 2737 / TCVN 9386", "codeZh": "越南 TCVN 2737", "codeEn": "TCVN 2737 Vietnam Loads",
        "regions": {
            "北部": {"河内": [0.46, 0.22], "海防": [0.55, 0.18], "下龙": [0.52, 0.18]},
            "中部": {"岘港": [0.58, 0.14], "顺化": [0.55, 0.14], "芽庄": [0.60, 0.12]},
            "南部": {"胡志明市": [0.56, 0.14], "芹苴": [0.52, 0.12], "头顿": [0.58, 0.12]},
        },
    },
    "ph": {
        "nameZh": "菲律宾", "nameEn": "Philippines",
        "code": "NSCP 2015", "codeZh": "菲律宾 NSCP 2015", "codeEn": "NSCP 2015 National Structural Code",
        "regions": {
            "吕宋": {"马尼拉": [0.64, 0.11], "碧瑶": [0.48, 0.15], "克拉克": [0.55, 0.12]},
            "米沙鄢": {"宿务": [0.68, 0.10], "伊洛伊洛": [0.62, 0.10]},
            "棉兰老": {"达沃": [0.65, 0.10], "三宝颜": [0.60, 0.10], "卡加延": [0.58, 0.10]},
        },
    },
    "id": {
        "nameZh": "印度尼西亚", "nameEn": "Indonesia",
        "code": "SNI 1726 / SNI 1727", "codeZh": "印度尼西亚 SNI 1726/1727", "codeEn": "SNI 1726 Wind / 1727 Earthquake",
        "regions": {
            "爪哇": {"雅加达": [0.60, 0.12], "泗水": [0.55, 0.12], "万隆": [0.48, 0.12], "日惹": [0.48, 0.12]},
            "苏门答腊": {"棉兰": [0.63, 0.11], "巴东": [0.55, 0.12], "巨港": [0.55, 0.10]},
            "加里曼丹": {"巴厘巴板": [0.52, 0.10], "坤甸": [0.55, 0.10]},
            "苏拉威西": {"望加锡": [0.58, 0.10], "万鸦老": [0.55, 0.10]},
            "巴厘岛": {"登巴萨": [0.58, 0.10]},
        },
    },
    "au": {
        "nameZh": "澳大利亚", "nameEn": "Australia",
        "code": "AS/NZS 1170.2/3", "codeZh": "澳大利亚 AS/NZS 1170.2/3", "codeEn": "AS/NZS 1170.2 Wind / 1170.3 Snow",
        "regions": {
            "东部": {"悉尼": [0.50, 0.20], "布里斯班": [0.48, 0.10], "黄金海岸": [0.52, 0.10]},
            "南部": {"墨尔本": [0.50, 0.20], "阿德莱德": [0.48, 0.15], "霍巴特": [0.55, 0.25]},
            "西部": {"珀斯": [0.48, 0.10], "弗里曼特尔": [0.52, 0.10]},
            "北部": {"达尔文": [0.70, 0.10], "凯恩斯": [0.65, 0.10], "汤斯维尔": [0.60, 0.10]},
            "内陆": {"堪培拉": [0.45, 0.15], "爱丽丝泉": [0.42, 0.08]},
        },
    },
    "nz": {
        "nameZh": "新西兰", "nameEn": "New Zealand",
        "code": "NZS 1170.2/3", "codeZh": "新西兰 NZS 1170.2/3", "codeEn": "NZS 1170.2 Wind / 1170.3 Snow",
        "regions": {
            "北岛": {"奥克兰": [0.52, 0.18], "惠灵顿": [0.58, 0.20], "汉密尔顿": [0.48, 0.18]},
            "南岛": {"基督城": [0.46, 0.25], "但尼丁": [0.52, 0.28], "皇后镇": [0.48, 0.35]},
        },
    },
    "ae": {
        "nameZh": "阿联酋", "nameEn": "UAE",
        "code": "UAE Building Code / BS", "codeZh": "阿联酋建筑规范", "codeEn": "UAE Building Code Wind Loads",
        "regions": {
            "沿海": {"迪拜": [0.54, 0.10], "阿布扎比": [0.52, 0.10], "沙迦": [0.54, 0.10], "富查伊拉": [0.58, 0.10]},
            "内陆": {"艾因": [0.48, 0.10]},
        },
    },
    "sa": {
        "nameZh": "沙特阿拉伯", "nameEn": "Saudi Arabia",
        "code": "SBC 301/304", "codeZh": "沙特 SBC 301/304", "codeEn": "SBC 301 Wind / 304 Snow",
        "regions": {
            "中部": {"利雅得": [0.46, 0.12], "布赖代": [0.45, 0.12]},
            "西部": {"吉达": [0.57, 0.10], "麦加": [0.55, 0.10], "延布": [0.55, 0.10]},
            "东部": {"达曼": [0.55, 0.10], "朱拜勒": [0.55, 0.10]},
        },
    },
    "eg": {
        "nameZh": "埃及", "nameEn": "Egypt",
        "code": "ECP 201-205", "codeZh": "埃及 ECP 201-205", "codeEn": "ECP 201-205 Egypt Loads",
        "regions": {
            "北部": {"开罗": [0.43, 0.16], "亚历山大": [0.51, 0.14], "塞得港": [0.55, 0.12]},
            "南部": {"阿斯旺": [0.45, 0.10], "卢克索": [0.45, 0.10]},
            "红海": {"赫尔格达": [0.52, 0.10]},
        },
    },
    "za": {
        "nameZh": "南非", "nameEn": "South Africa",
        "code": "SANS 10160-3", "codeZh": "南非 SANS 10160-3", "codeEn": "SANS 10160-3 Wind / Snow Loads",
        "regions": {
            "内陆": {"约翰内斯堡": [0.42, 0.24], "比勒陀利亚": [0.42, 0.22], "布隆方丹": [0.45, 0.22]},
            "沿海": {"开普敦": [0.54, 0.18], "德班": [0.55, 0.12], "伊丽莎白港": [0.52, 0.15]},
        },
    },
    "ng": {
        "nameZh": "尼日利亚", "nameEn": "Nigeria",
        "code": "NBC Nigeria", "codeZh": "尼日利亚国家建筑规范 NBC", "codeEn": "Nigeria National Building Code",
        "regions": {
            "南部": {"拉各斯": [0.61, 0.09], "哈科特港": [0.58, 0.09], "卡拉巴尔": [0.58, 0.09]},
            "中部": {"阿布贾": [0.45, 0.10], "卡诺": [0.42, 0.10]},
        },
    },
    "ke": {
        "nameZh": "肯尼亚", "nameEn": "Kenya",
        "code": "KS 06-100", "codeZh": "肯尼亚 KS 06-100", "codeEn": "KS 06-100 Kenya Building Code",
        "regions": {
            "中部": {"内罗毕": [0.45, 0.10], "纳库鲁": [0.42, 0.12]},
            "沿海": {"蒙巴萨": [0.58, 0.09], "马林迪": [0.55, 0.09]},
        },
    },
    "tr": {
        "nameZh": "土耳其", "nameEn": "Turkey",
        "code": "TS 4988 / TS EN 1991", "codeZh": "土耳其 TS 4988", "codeEn": "TS 4988 / TS EN 1991 Turkey",
        "regions": {
            "西部": {"伊斯坦布尔": [0.49, 0.22], "伊兹密尔": [0.52, 0.18], "布尔萨": [0.48, 0.22]},
            "中部": {"安卡拉": [0.42, 0.26], "开塞利": [0.42, 0.28]},
            "东部": {"埃尔祖鲁姆": [0.45, 0.45], "凡城": [0.48, 0.40]},
            "地中海": {"安塔利亚": [0.52, 0.15], "梅尔辛": [0.55, 0.14]},
        },
    },
    "pl": {
        "nameZh": "波兰", "nameEn": "Poland",
        "code": "PN-EN 1991-1-3/4", "codeZh": "波兰 PN-EN 1991", "codeEn": "PN-EN 1991-1-3/4 Poland",
        "regions": {
            "中部": {"华沙": [0.44, 0.33], "罗兹": [0.44, 0.32], "卢布林": [0.42, 0.35]},
            "北部": {"格但斯克": [0.50, 0.30], "什切青": [0.50, 0.30]},
            "南部": {"克拉科夫": [0.42, 0.38], "弗罗茨瓦夫": [0.44, 0.35]},
        },
    },
    "ua": {
        "nameZh": "乌克兰", "nameEn": "Ukraine",
        "code": "DBN V.1.2-2 / DSTU", "codeZh": "乌克兰 DBN V.1.2-2", "codeEn": "DBN V.1.2-2 Ukraine Loads",
        "regions": {
            "中部": {"基辅": [0.47, 0.36], "第聂伯": [0.45, 0.35], "哈尔科夫": [0.45, 0.38]},
            "西部": {"利沃夫": [0.42, 0.38], "敖德萨": [0.52, 0.22]},
            "东部": {"顿涅茨克": [0.45, 0.35]},
        },
    },
    "ir": {
        "nameZh": "伊朗", "nameEn": "Iran",
        "code": "Iranian Building Code / BHPA", "codeZh": "伊朗建筑规范", "codeEn": "Iranian Building Code Loads",
        "regions": {
            "北部": {"德黑兰": [0.44, 0.24], "马什哈德": [0.45, 0.28], "大不里士": [0.42, 0.30]},
            "南部": {"阿巴斯港": [0.53, 0.13], "布什尔": [0.52, 0.12], "设拉子": [0.45, 0.15]},
            "中部": {"伊斯法罕": [0.42, 0.20]},
        },
    },
    "il": {
        "nameZh": "以色列", "nameEn": "Israel",
        "code": "IS 1225 / IS 413", "codeZh": "以色列 IS 1225/413", "codeEn": "IS 1225 Wind / IS 413 Loads",
        "regions": {
            "地中海": {"特拉维夫": [0.48, 0.12], "海法": [0.52, 0.12], "耶路撒冷": [0.42, 0.15]},
            "南部": {"埃拉特": [0.50, 0.10], "贝尔谢巴": [0.45, 0.12]},
        },
    },
    "pk": {
        "nameZh": "巴基斯坦", "nameEn": "Pakistan",
        "code": "BCP SP 2007", "codeZh": "巴基斯坦 BCP SP 2007", "codeEn": "BCP SP 2007 Pakistan Building Code",
        "regions": {
            "北部": {"伊斯兰堡": [0.42, 0.25], "拉合尔": [0.42, 0.18], "白沙瓦": [0.42, 0.22]},
            "南部": {"卡拉奇": [0.52, 0.10], "奎达": [0.45, 0.18]},
        },
    },
    "bd": {
        "nameZh": "孟加拉国", "nameEn": "Bangladesh",
        "code": "BNBC 2020", "codeZh": "孟加拉国 BNBC 2020", "codeEn": "BNBC 2020 Bangladesh Code",
        "regions": {
            "中部": {"达卡": [0.52, 0.12], "吉大港": [0.58, 0.12], "库尔纳": [0.55, 0.12]},
        },
    },
    "kz": {
        "nameZh": "哈萨克斯坦", "nameEn": "Kazakhstan",
        "code": "SN RK / SP RK", "codeZh": "哈萨克斯坦 SN RK", "codeEn": "SN RK Kazakhstan Loads",
        "regions": {
            "南部": {"阿拉木图": [0.42, 0.45], "奇姆肯特": [0.42, 0.35]},
            "北部": {"阿斯塔纳": [0.45, 0.50], "卡拉干达": [0.45, 0.48]},
        },
    },
    "tw": {
        "nameZh": "中国台湾", "nameEn": "Taiwan",
        "code": "CNS 14497 / 建筑技术规则", "codeZh": "台湾 CNS 14497 风荷载", "codeEn": "CNS 14497 Taiwan Wind Loads",
        "regions": {
            "北部": {"台北": [0.75, 0.15], "桃园": [0.70, 0.15], "新竹": [0.68, 0.15]},
            "中部": {"台中": [0.70, 0.15], "彰化": [0.68, 0.15]},
            "南部": {"高雄": [0.80, 0.15], "台南": [0.75, 0.15], "屏东": [0.78, 0.12]},
            "东部": {"花莲": [0.72, 0.15], "台东": [0.75, 0.12]},
        },
    },
    "hk": {
        "nameZh": "中国香港", "nameEn": "Hong Kong",
        "code": "CoP HK Wind Code 2019", "codeZh": "香港风效应规范 CoP 2019", "codeEn": "Code of Practice for Wind Effects HK 2019",
        "regions": {"全境": {"香港": [0.80, 0.10], "九龙": [0.80, 0.10], "新界": [0.75, 0.10]}},
    },
    "mo": {
        "nameZh": "中国澳门", "nameEn": "Macau",
        "code": "Macau Wind Code", "codeZh": "澳门风荷载规范", "codeEn": "Macau Wind Load Code",
        "regions": {"全境": {"澳门": [0.75, 0.10]}},
    },
    "cr": {
        "nameZh": "哥斯达黎加", "nameEn": "Costa Rica",
        "code": "Seismic Code CR", "codeZh": "哥斯达黎加建筑抗震规范", "codeEn": "Costa Rica Building Seismic Code",
        "regions": {"中央谷地": {"圣何塞": [0.56, 0.11], "利蒙": [0.60, 0.10], "蓬塔雷纳斯": [0.58, 0.10]}},
    },
    "pa": {
        "nameZh": "巴拿马", "nameEn": "Panama",
        "code": "Panama Building Code", "codeZh": "巴拿马建筑规范", "codeEn": "Panama Building Code",
        "regions": {"运河区": {"巴拿马城": [0.64, 0.09], "科隆": [0.62, 0.09], "大卫": [0.55, 0.10]}},
    },
    "uy": {
        "nameZh": "乌拉圭", "nameEn": "Uruguay",
        "code": "UNIT 858", "codeZh": "乌拉圭 UNIT 858", "codeEn": "UNIT 858 Uruguay Loads",
        "regions": {"南部": {"蒙得维的亚": [0.51, 0.20], "萨尔托": [0.48, 0.18], "埃斯特角": [0.55, 0.18]}},
    },
    "ve": {
        "nameZh": "委内瑞拉", "nameEn": "Venezuela",
        "code": "COVENIN 1756", "codeZh": "委内瑞拉 COVENIN 1756", "codeEn": "COVENIN 1756 Venezuela",
        "regions": {
            "北部": {"加拉加斯": [0.58, 0.11], "马拉开波": [0.52, 0.12], "巴基西梅托": [0.48, 0.12]},
            "东部": {"玻利瓦尔城": [0.48, 0.10]},
        },
    },
    "ec": {
        "nameZh": "厄瓜多尔", "nameEn": "Ecuador",
        "code": "NEC-SE-MP", "codeZh": "厄瓜多尔 NEC-SE", "codeEn": "NEC-SE Ecuador Structural Code",
        "regions": {
            "沿海": {"瓜亚基尔": [0.52, 0.10], "曼塔": [0.55, 0.10]},
            "高原": {"基多": [0.42, 0.15], "昆卡": [0.40, 0.15]},
        },
    },
    "ma": {
        "nameZh": "摩洛哥", "nameEn": "Morocco",
        "code": "RPS 2011 / Eurocode", "codeZh": "摩洛哥 RPS 2011", "codeEn": "RPS 2011 Morocco Seismic/Wind",
        "regions": {
            "沿海": {"卡萨布兰卡": [0.52, 0.14], "拉巴特": [0.52, 0.14], "丹吉尔": [0.55, 0.14]},
            "内陆": {"马拉喀什": [0.45, 0.14], "非斯": [0.45, 0.16]},
        },
    },
    "qa": {
        "nameZh": "卡塔尔", "nameEn": "Qatar",
        "code": "QCS 2014", "codeZh": "卡塔尔 QCS 2014", "codeEn": "QCS 2014 Qatar Construction Specs",
        "regions": {"全境": {"多哈": [0.52, 0.10], "赖扬": [0.52, 0.10], "沃克拉": [0.52, 0.10]}},
    },
    "kw": {
        "nameZh": "科威特", "nameEn": "Kuwait",
        "code": "Kuwait Building Code", "codeZh": "科威特建筑规范", "codeEn": "Kuwait Building Code",
        "regions": {"全境": {"科威特城": [0.50, 0.10], "艾哈迈迪": [0.52, 0.10]}},
    },
    "fi": {
        "nameZh": "芬兰", "nameEn": "Finland",
        "code": "BY EN 1991", "codeZh": "芬兰 BY EN 1991", "codeEn": "BY EN 1991-1-3/4 Finland",
        "regions": {
            "南部": {"赫尔辛基": [0.48, 0.45], "图尔库": [0.50, 0.42], "坦佩雷": [0.45, 0.48]},
            "北部": {"奥卢": [0.48, 0.55], "罗瓦涅米": [0.45, 0.60]},
        },
    },
    "dk": {
        "nameZh": "丹麦", "nameEn": "Denmark",
        "code": "DS/EN 1991", "codeZh": "丹麦 DS/EN 1991", "codeEn": "DS/EN 1991-1-3/4 Denmark",
        "regions": {
            "西兰": {"哥本哈根": [0.50, 0.28], "奥胡斯": [0.50, 0.28]},
            "日德兰": {"奥尔堡": [0.52, 0.30], "埃斯比约": [0.55, 0.28]},
        },
    },
    "pt": {
        "nameZh": "葡萄牙", "nameEn": "Portugal",
        "code": "NP EN 1991", "codeZh": "葡萄牙 NP EN 1991", "codeEn": "NP EN 1991-1-3/4 Portugal",
        "regions": {
            "北部": {"波尔图": [0.50, 0.20], "布拉加": [0.48, 0.22]},
            "中部": {"里斯本": [0.55, 0.15], "科英布拉": [0.50, 0.18]},
            "南部": {"法鲁": [0.52, 0.12], "拉各斯": [0.55, 0.10]},
            "群岛": {"丰沙尔": [0.55, 0.12], "蓬塔德尔加达": [0.58, 0.15]},
        },
    },
    "gr": {
        "nameZh": "希腊", "nameEn": "Greece",
        "code": "EAK / EN 1991", "codeZh": "希腊 EAK / EN 1991", "codeEn": "EAK Greece / EN 1991 Loads",
        "regions": {
            "大陆": {"雅典": [0.48, 0.15], "塞萨洛尼基": [0.48, 0.18]},
            "岛屿": {"克里特": [0.52, 0.12], "罗德岛": [0.55, 0.12], "圣托里尼": [0.55, 0.10]},
        },
    },
    "cz": {
        "nameZh": "捷克", "nameEn": "Czech Republic",
        "code": "ČSN EN 1991", "codeZh": "捷克 ČSN EN 1991", "codeEn": "ČSN EN 1991-1-3/4 Czechia",
        "regions": {
            "波希米亚": {"布拉格": [0.42, 0.35], "比尔森": [0.42, 0.35]},
            "摩拉维亚": {"布尔诺": [0.42, 0.35], "俄斯特拉发": [0.45, 0.38]},
        },
    },
    "at": {
        "nameZh": "奥地利", "nameEn": "Austria",
        "code": "ÖNORM EN 1991", "codeZh": "奥地利 ÖNORM EN 1991", "codeEn": "ÖNORM EN 1991-1-3/4 Austria",
        "regions": {
            "东部": {"维也纳": [0.42, 0.35], "格拉茨": [0.42, 0.35]},
            "西部": {"因斯布鲁克": [0.42, 0.50], "萨尔茨堡": [0.42, 0.45]},
        },
    },
    "be": {
        "nameZh": "比利时", "nameEn": "Belgium",
        "code": "NBN EN 1991", "codeZh": "比利时 NBN EN 1991", "codeEn": "NBN EN 1991-1-3/4 Belgium",
        "regions": {
            "弗拉芒": {"布鲁塞尔": [0.45, 0.28], "安特卫普": [0.48, 0.28], "根特": [0.50, 0.28]},
            "瓦隆": {"列日": [0.45, 0.30], "那慕尔": [0.45, 0.30]},
        },
    },
    "ie": {
        "nameZh": "爱尔兰", "nameEn": "Ireland",
        "code": "I.S. EN 1991", "codeZh": "爱尔兰 I.S. EN 1991", "codeEn": "I.S. EN 1991-1-3/4 Ireland",
        "regions": {
            "东部": {"都柏林": [0.55, 0.22], "韦克斯福德": [0.55, 0.20]},
            "西部": {"戈尔韦": [0.58, 0.25], "香农": [0.55, 0.22]},
        },
    },
    "lk": {
        "nameZh": "斯里兰卡", "nameEn": "Sri Lanka",
        "code": "SLS 1304", "codeZh": "斯里兰卡 SLS 1304", "codeEn": "SLS 1304 Sri Lanka Loads",
        "regions": {
            "西部": {"科伦坡": [0.58, 0.10], "尼甘布": [0.58, 0.10]},
            "中部": {"康提": [0.48, 0.12], "努沃勒埃利耶": [0.45, 0.15]},
        },
    },
    "mm": {
        "nameZh": "缅甸", "nameEn": "Myanmar",
        "code": "Myanmar Building Code", "codeZh": "缅甸建筑规范", "codeEn": "Myanmar Building Code",
        "regions": {
            "南部": {"仰光": [0.58, 0.12], "毛淡棉": [0.55, 0.12]},
            "中部": {"曼德勒": [0.48, 0.14], "内比都": [0.48, 0.14]},
        },
    },
    "kh": {
        "nameZh": "柬埔寨", "nameEn": "Cambodia",
        "code": "Cambodia Building Code", "codeZh": "柬埔寨建筑规范", "codeEn": "Cambodia Building Code",
        "regions": {"全境": {"金边": [0.55, 0.12], "暹粒": [0.48, 0.12], "西哈努克": [0.58, 0.10]}},
    },
    "mn": {
        "nameZh": "蒙古", "nameEn": "Mongolia",
        "code": "MNS 6545", "codeZh": "蒙古 MNS 6545", "codeEn": "MNS 6545 Mongolia Loads",
        "regions": {
            "中部": {"乌兰巴托": [0.45, 0.50], "额尔登特": [0.45, 0.48]},
            "南部": {"达兰扎德嘎勒": [0.48, 0.35]},
        },
    },
    "fj": {
        "nameZh": "斐济", "nameEn": "Fiji",
        "code": "Fiji Building Code", "codeZh": "斐济建筑规范", "codeEn": "Fiji Building Code",
        "regions": {"群岛": {"苏瓦": [0.65, 0.10], "楠迪": [0.62, 0.10]}},
    },
    "gh": {
        "nameZh": "加纳", "nameEn": "Ghana",
        "code": "Ghana Building Code", "codeZh": "加纳建筑规范", "codeEn": "Ghana Building Code GS 1207",
        "regions": {
            "南部": {"阿克拉": [0.55, 0.09], "特马": [0.55, 0.09]},
            "北部": {"库马西": [0.48, 0.10]},
        },
    },
    "tz": {
        "nameZh": "坦桑尼亚", "nameEn": "Tanzania",
        "code": "Tanzania Building Code", "codeZh": "坦桑尼亚建筑规范", "codeEn": "Tanzania Building Regulations",
        "regions": {
            "沿海": {"达累斯萨拉姆": [0.58, 0.09], "桑给巴尔": [0.60, 0.09]},
            "内陆": {"多多马": [0.45, 0.10], "阿鲁沙": [0.42, 0.12]},
        },
    },
    "et": {
        "nameZh": "埃塞俄比亚", "nameEn": "Ethiopia",
        "code": "EBCS 1", "codeZh": "埃塞俄比亚 EBCS 1", "codeEn": "EBCS 1 Ethiopia Building Code",
        "regions": {
            "高原": {"亚的斯亚贝巴": [0.42, 0.15], "贡德尔": [0.40, 0.18]},
            "低地": {"德雷达瓦": [0.45, 0.10]},
        },
    },
    "bo": {
        "nameZh": "玻利维亚", "nameEn": "Bolivia",
        "code": "NB 22000", "codeZh": "玻利维亚 NB 22000", "codeEn": "NB 22000 Bolivia Code",
        "regions": {
            "高原": {"拉巴斯": [0.40, 0.15], "奥鲁罗": [0.40, 0.18], "波托西": [0.40, 0.18]},
            "低地": {"圣克鲁斯": [0.45, 0.10], "科恰班巴": [0.42, 0.12]},
        },
    },
    "py": {
        "nameZh": "巴拉圭", "nameEn": "Paraguay",
        "code": "Paraguay Building Code", "codeZh": "巴拉圭建筑规范", "codeEn": "Paraguay Building Code",
        "regions": {"全境": {"亚松森": [0.48, 0.12], "东方市": [0.45, 0.12]}},
    },
    "cu": {
        "nameZh": "古巴", "nameEn": "Cuba",
        "code": "NC Cuban Code", "codeZh": "古巴 NC 建筑规范", "codeEn": "NC Cuba Building Code",
        "regions": {
            "西部": {"哈瓦那": [0.65, 0.10], "比那尔德里奥": [0.62, 0.10]},
            "东部": {"圣地亚哥": [0.62, 0.10]},
        },
    },
    "jm": {
        "nameZh": "牙买加", "nameEn": "Jamaica",
        "code": "Jamaica Building Code", "codeZh": "牙买加建筑规范", "codeEn": "Jamaica Building Code",
        "regions": {"全境": {"金斯敦": [0.68, 0.10], "蒙特哥贝": [0.65, 0.10]}},
    },
    "is": {
        "nameZh": "冰岛", "nameEn": "Iceland",
        "code": "Icelandic Building Code", "codeZh": "冰岛建筑规范", "codeEn": "Icelandic Building Regulation",
        "regions": {"全境": {"雷克雅未克": [0.55, 0.40], "阿克雷里": [0.58, 0.45]}},
    },
    "ro": {
        "nameZh": "罗马尼亚", "nameEn": "Romania",
        "code": "SR EN 1991", "codeZh": "罗马尼亚 SR EN 1991", "codeEn": "SR EN 1991-1-3/4 Romania",
        "regions": {
            "南部": {"布加勒斯特": [0.45, 0.35], "康斯坦察": [0.52, 0.22]},
            "北部": {"克卢日": [0.42, 0.38], "雅西": [0.45, 0.38]},
        },
    },
    "hu": {
        "nameZh": "匈牙利", "nameEn": "Hungary",
        "code": "MSZ EN 1991", "codeZh": "匈牙利 MSZ EN 1991", "codeEn": "MSZ EN 1991-1-3/4 Hungary",
        "regions": {
            "全境": {"布达佩斯": [0.42, 0.35], "德布勒森": [0.42, 0.35], "佩奇": [0.42, 0.32]},
        },
    },
}


def dedupe_cities(data: dict) -> dict:
    """Last entry wins for duplicate city keys within a region."""
    return data


def count_stats(global_data: dict) -> tuple[int, int, int]:
    countries = len(global_data)
    regions = sum(len(c["regions"]) for c in global_data.values())
    cities = sum(
        len(cities)
        for c in global_data.values()
        for cities in c["regions"].values()
    )
    return countries, regions, cities


def to_js(global_data: dict) -> str:
    lines = [
        "// Global wind/snow load reference data (50-year baseline, kN/m²)",
        "// Verify with local official code maps for formal engineering.",
        "const GLOBAL_DATA = {",
    ]
    for code, country in sorted(global_data.items(), key=lambda x: x[1]["nameZh"]):
        lines.append(f'    "{code}": {{')
        lines.append(f'        standard: {{ zh: {json.dumps(country["codeZh"], ensure_ascii=False)}, en: {json.dumps(country["codeEn"], ensure_ascii=False)} }},')
        lines.append(f'        code: {json.dumps(country["code"], ensure_ascii=False)},')
        lines.append(f'        name: {{ zh: {json.dumps(country["nameZh"], ensure_ascii=False)}, en: {json.dumps(country["nameEn"], ensure_ascii=False)} }},')
        lines.append('        regions: {')
        for region, cities in country["regions"].items():
            lines.append(f'            {json.dumps(region, ensure_ascii=False)}: {{')
            for city, vals in sorted(cities.items()):
                lines.append(f'                {json.dumps(city, ensure_ascii=False)}: [{vals[0]},{vals[1]}],')
            lines.append('            },')
        lines.append('        },')
        lines.append('    },')
    lines.append('};')
    return '\n'.join(lines)


def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out_json = os.path.join(root, 'data', 'global.json')
    out_js = os.path.join(root, 'data', 'global.js')

    with open(out_json, 'w', encoding='utf-8') as f:
        json.dump(GLOBAL, f, ensure_ascii=False, indent=2)

    with open(out_js, 'w', encoding='utf-8') as f:
        f.write(to_js(GLOBAL))

    c, r, n = count_stats(GLOBAL)
    print(f'Wrote {out_json}')
    print(f'Wrote {out_js}')
    print(f'Stats: {c} countries, {r} regions, {n} cities')


if __name__ == '__main__':
    main()
