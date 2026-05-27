#!/usr/bin/env python3
"""Parse GB 50009-2012 Appendix E.5 table from readthedocs markdown export."""
import json
import re
import sys

PROVINCES = {
    "北京", "天津", "河北", "山西", "内蒙古", "辽宁", "吉林", "黑龙江",
    "上海", "江苏", "浙江", "安徽", "福建", "江西", "山东", "河南",
    "湖北", "湖南", "广东", "广西", "海南", "重庆", "四川", "贵州",
    "云南", "西藏", "陕西", "甘肃", "青海", "宁夏", "新疆", "台湾", "香港", "澳门",
}

NUM = re.compile(r"^-?\d+\.?\d*$")
ZONE = re.compile(r"^[ⅠⅡⅢ]$")


def is_data_token(s: str) -> bool:
    return bool(NUM.match(s)) or s == "-" or bool(ZONE.match(s))


def parse_table(path: str) -> dict:
    with open(path, encoding="utf-8") as f:
        lines = [ln.strip() for ln in f.readlines() if ln.strip()]

    start = next(i for i, ln in enumerate(lines) if ln == "表E.5 全国各城市的雪压、风压和基本气温")
    i = start + 1
    while i < len(lines) and lines[i] != "北京":
        i += 1

    data: dict[str, dict[str, list[float]]] = {}
    current_prov = None

    while i < len(lines):
        ln = lines[i]
        if ln.startswith("注：") or ln.startswith("##"):
            break

        if ln in PROVINCES:
            current_prov = ln
            i += 1
            continue

        if current_prov is None:
            i += 1
            continue

        city = ln.rstrip("市")
        i += 1
        block = []
        while i < len(lines) and len(block) < 10:
            if lines[i] in PROVINCES:
                break
            if not is_data_token(lines[i]):
                break
            block.append(lines[i])
            i += 1

        if len(block) < 7:
            continue

        w50, s50 = block[2], block[5]
        if w50 == "-" or s50 == "-":
            continue

        data.setdefault(current_prov, {})[city] = [
            round(float(w50), 2),
            round(float(s50), 2),
        ]

    return data


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else None
    if not src:
        print("Usage: parse_gb50009.py <E.html.txt>", file=sys.stderr)
        sys.exit(1)

    data = parse_table(src)
    total = sum(len(v) for v in data.values())
    print(f"Parsed {total} cities in {len(data)} provinces", file=sys.stderr)

    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out_json = os.path.join(root, "data", "cities.json")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Wrote {out_json}", file=sys.stderr)


if __name__ == "__main__":
    main()
