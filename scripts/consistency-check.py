#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""taxue-solar-polaroid 结构一致性检查（只读，不改文件）。

检查项：
1. SKILL.md frontmatter 含 name/description，且 name 与目录名一致
2. SKILL.md 与 README.md 引用的 references/*.md 文件真实存在
3. README.md 引用的 assets 与 gallery 图片真实存在
   （同时覆盖 markdown `](path)`、HTML `<img src>` 与 `<a href>` 三种形式）
4. templates/taxue-solar-polaroid.txt 存在，且包含全部结构区块与关键锚点
5. seasonal-evidence-library.md 节气表自洽（24 行）；README 若仍有节气表则同步对比
6. --against <真源目录>：逐字节对比 SKILL.md / references/*.md / templates/*.txt，
   守护「真源 ↔ 仓库」同步（历史上曾因手工双维护导致发布版落后真源）

用法：
    python3 scripts/consistency-check.py
    python3 scripts/consistency-check.py --against ~/.agents/skills/taxue-solar-polaroid
退出码：0 = 全部一致；1 = 存在漂移。
"""
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# template 必须包含的结构区块与关键锚点；措辞可改，区块名与语义锚点不可丢
TEMPLATE_ANCHORS = [
    "【工作总则】", "【创作推演卡】", "【形式路由】",
    "【自然文案规则】", "【提示词编译顺序】", "【输出格式】", "【严格禁止】",
    "【本次创作输入】", "踏雪寻仙", "3:4",
]
# 前缀型锚点：template 区块名带说明后缀（如「【多张组图：解释矩阵，而非固定模板】」）
TEMPLATE_PREFIX_ANCHORS = ["【多张组图"]

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


def referenced_images(text):
    """提取文本中引用的 assets/ 与 gallery/ 图片相对路径，覆盖 markdown 与 HTML。"""
    paths = set()
    for prefix in ("assets/readme", "gallery"):
        for m in re.finditer(r"(?:\.?/|\()" + prefix + r"/[\w./\-]+\.(?:jpg|jpeg|png|svg)", text):
            paths.add(m.group(0).lstrip("( "))
    return paths


def compare_against(target: Path):
    """逐字节对比仓库文本真源与外部真源树，报告漂移。"""
    for rel in ["SKILL.md"] + \
               sorted(f"references/{p.name}" for p in (ROOT / "references").glob("*.md")) + \
               sorted(f"templates/{p.name}" for p in (ROOT / "templates").glob("*.txt")):
        here = ROOT / rel
        there = target / rel
        if not there.exists():
            check(False, f"[--against] 真源缺少 {rel}（仓库有、真源无）")
        elif not here.exists():
            check(False, f"[--against] 仓库缺少 {rel}（真源有、仓库无）")
        elif here.read_text(encoding="utf-8") != there.read_text(encoding="utf-8"):
            check(False, f"[--against] {rel} 与真源内容漂移，需重新同步")


def main():
    parser = argparse.ArgumentParser(description="结构一致性检查")
    parser.add_argument("--against", type=Path, default=None,
                        help="外部真源目录（如 ~/.agents/skills/taxue-solar-polaroid），逐文件对比")
    args = parser.parse_args()

    skll_path = ROOT / "SKILL.md"
    SKILL = skll_path.read_text(encoding="utf-8")
    README = (ROOT / "README.md").read_text(encoding="utf-8")

    # 1. frontmatter
    fm = re.search(r"^---\n(.*?)\n---", SKILL, re.S)
    check(fm is not None, "SKILL.md 缺少 frontmatter")
    if fm:
        body = fm.group(1)
        name = re.search(r"name:\s*([^\n]+)", body)
        check("description:" in body, "SKILL.md frontmatter 缺少 description")
        if name:
            check(name.group(1).strip() == ROOT.name,
                  f"frontmatter name「{name.group(1).strip()}」与目录名「{ROOT.name}」不一致")

    # 2. SKILL.md / README.md 引用的 references 文件
    for text, who in ((SKILL, "SKILL.md"), (README, "README.md")):
        for ref in set(re.findall(r"references/([\w\-.]+\.md)", text)):
            check((ROOT / "references" / ref).exists(),
                  f"{who} 引用了不存在的 references/{ref}")

    # 3. README 引用的 assets / gallery 图片
    for img in referenced_images(README):
        check((ROOT / img).exists(), f"README 引用了不存在的 {img}")

    # 4. templates：存在 + 结构区块锚点
    tpl_path = ROOT / "templates" / "taxue-solar-polaroid.txt"
    check(tpl_path.exists(), "templates/taxue-solar-polaroid.txt 缺失")
    if tpl_path.exists():
        tpl = tpl_path.read_text(encoding="utf-8")
        for anchor in TEMPLATE_ANCHORS:
            check(anchor in tpl, f"template 缺少结构锚点「{anchor}」，区块骨架漂移")
        for anchor in TEMPLATE_PREFIX_ANCHORS:
            check(anchor in tpl, f"template 缺少结构锚点「{anchor}…」，区块骨架漂移")

    # 5. 节气表：真源必查 24 行；README 有表时才对比（介绍页已不再展示节气表）
    src = (ROOT / "references" / "seasonal-evidence-library.md").read_text(encoding="utf-8")
    src_rows = solar_table(src)
    check(len(src_rows) == 24, f"seasonal-evidence-library.md 节气表异常（{len(src_rows)} 行）")
    readme_rows = solar_table(README)
    if readme_rows:
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

    # 6. 真源树对比
    if args.against:
        compare_against(args.against)

    if ERRORS:
        print(f"❌ 发现 {len(ERRORS)} 处漂移：")
        for e in ERRORS:
            print(f"  - {e}")
        sys.exit(1)
    scope = "（含真源对比）" if args.against else ""
    print(f"✅ 全部一致：frontmatter、引用文件、模板锚点、节气表{scope}均对齐")
    sys.exit(0)


if __name__ == "__main__":
    main()
