#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""taxue-solar-polaroid 结构一致性检查（只读，不改文件）。

检查项：
1. SKILL.md frontmatter 含 name 与 description
2. SKILL.md 与 README.md 引用的 references/*.md 文件真实存在
3. README.md 引用的 assets/readme/*.svg 真实存在
4. templates/taxue-solar-polaroid.txt 存在
5. README.md 节气表行数与 references/seasonal-evidence-library.md 表格行数一致
   （介绍页与真源不得漂移；曾出现 README 凭印象改写节气表导致失真的问题）

用法：python3 scripts/consistency-check.py
退出码：0 = 全部一致；1 = 存在漂移。
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = (ROOT / "SKILL.md").read_text(encoding="utf-8")
README = (ROOT / "README.md").read_text(encoding="utf-8")

ERRORS = []


def check(ok: bool, msg: str):
    if not ok:
        ERRORS.append(msg)


def solar_table(text):
    """只提取以「| 节气 |」为表头的那张表的数据行。"""
    rows = []
    capture = False
    for line in text.splitlines():
        if line.startswith("| 节气 |"):
            capture = True
            continue
        if capture:
            if line.startswith("|"):
                if re.match(r"^\|[\s:\-|]+\|$", line):
                    continue
                rows.append(line)
            else:
                break
    return rows


def main():
    # 1. frontmatter
    fm = re.search(r"^---\n(.*?)\n---", SKILL, re.S)
    check(fm is not None, "SKILL.md 缺少 frontmatter")
    if fm:
        body = fm.group(1)
        check("name:" in body, "SKILL.md frontmatter 缺少 name")
        check("description:" in body, "SKILL.md frontmatter 缺少 description")

    # 2. SKILL.md / README.md 引用的 references 文件
    for text, who in ((SKILL, "SKILL.md"), (README, "README.md")):
        for ref in set(re.findall(r"references/([\w\-.]+\.md)", text)):
            check((ROOT / "references" / ref).exists(),
                  f"{who} 引用了不存在的 references/{ref}")

    # 3. README 引用的 assets / gallery 文件
    for asset in set(re.findall(r"\./(assets/readme/[\w\-.]+\.svg)", README)):
        check((ROOT / asset).exists(), f"README 引用了不存在的 {asset}")
    for img in set(re.findall(r"\./(gallery/[\w\-.]+\.(?:jpg|png|jpeg))\)", README)):
        check((ROOT / img).exists(), f"README 引用了不存在的 {img}")

    # 4. templates
    check((ROOT / "templates" / "taxue-solar-polaroid.txt").exists(),
          "templates/taxue-solar-polaroid.txt 缺失")

    # 5. README 节气表与真源一致性
    src = (ROOT / "references" / "seasonal-evidence-library.md").read_text(encoding="utf-8")
    src_rows = solar_table(src)
    readme_rows = solar_table(README)
    check(len(src_rows) == 24, f"seasonal-evidence-library.md 节气表异常（{len(src_rows)} 行）")
    check(len(readme_rows) == 24, f"README.md 节气表异常（{len(readme_rows)} 行）")
    if len(src_rows) == 24 and len(readme_rows) == 24:
        for i, (s, r) in enumerate(zip(src_rows, readme_rows)):
            s_cols = [c.strip() for c in s.split("|")[1:-1]]
            r_cols = [c.strip() for c in r.split("|")[1:-1]]
            if len(s_cols) >= 2 and len(r_cols) >= 2:
                check(s_cols[0] == r_cols[0],
                      f"README 节气表第 {i+1} 行名称漂移：{r_cols[0]} ≠ {s_cols[0]}")
                check(s_cols[1] == r_cols[1],
                      f"README 节气「{s_cols[0]}」的状态转折与真源不一致")
            else:
                check(False, f"节气表第 {i+1} 行解析失败：{s!r}")

    if ERRORS:
        print(f"❌ 发现 {len(ERRORS)} 处漂移：")
        for e in ERRORS:
            print(f"  - {e}")
        sys.exit(1)
    print("✅ 全部一致：frontmatter、引用文件、模板、节气表均与真源对齐")
    sys.exit(0)


if __name__ == "__main__":
    main()
