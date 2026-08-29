#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""taxue-solar-polaroid 提示词 lint（只读）。

对「生成的生图提示词」做静态检查，机检 SKILL.md【严格禁止】与交付标准中的高频漂移项：
固定主物、伪事实断言、装饰性几何、风格滥用、文案病、品牌污染、无判断模板结构、固定节日符号。

判定原则：SKILL.md 的原文是「不能**在没有判断的情况下**使用」，静态检查无法判断
有没有判断，所以每个命中都只是「候选违规」，附规则出处供人工复核；确有主题依据时
用 --allow 放行。

注意：本工具只用于 lint 提示词文本，不要对本仓库的 SKILL.md / template / references
运行——禁止清单本身含这些词。

用法：
    python3 scripts/prompt-lint.py 提示词.txt          # lint 一个或多个文件
    cat 提示词.txt | python3 scripts/prompt-lint.py    # lint stdin
    python3 scripts/prompt-lint.py --selftest          # 内置正反例自检
    python3 scripts/prompt-lint.py 提示词.txt --allow 荷叶   # 放行含指定子串的命中
退出码：0 = 干净；1 = 存在候选违规；2 = 自检失败（规则无正例覆盖）。
"""
import argparse
import re
import sys

# (正则, 规则出处)。新增规则必须同时在 DIRTY_FIXTURE 中加正例，否则 --selftest 失败。
RULES = [
    (r"荷叶|荷花|莲叶", "固定主物：处暑≠荷叶（SKILL.md 严格禁止）"),
    (r"嫩芽|新芽", "固定主物：立春≠嫩芽（SKILL.md 严格禁止）"),
    (r"喜鹊桥|鹊桥|玉兔|龙舟|嫦娥", "固定节日符号：节日不等于神话图腾（README 节日成图纪律）"),
    (r"今日|此地|今年最早", "伪事实断言：未提供地点/时间时不写可核验断言（SKILL.md 自然文案）"),
    (r"假日期|虚假日期", "伪事实：不虚构日期（SKILL.md 严格禁止）"),
    (r"红点|橙点|绿点|圆点|小方块|印章|几何标记", "装饰性几何标记：强调色只能来自主题证据（SKILL.md 交付标准）"),
    (r"泛黄|做旧|怀旧滤镜|复古滤镜|赛博|霓虹|噪点|颗粒感", "风格滥用：不用泛黄和颗粒冒充质感（SKILL.md 推演卡 F / 严格禁止）"),
    (r"古诗|诗词|典故|伪引用|名言|口号", "文案病：不默认生成古诗、典故、伪引用、口号（SKILL.md 自然文案）"),
    (r"假英文|微字|密集小字", "文案病：不为高级感添加假英文或密集微字（SKILL.md 严格禁止）"),
    (r"logo|水印|watermark", "品牌污染：不加 logo、水印（SKILL.md 严格禁止）"),
    (r"斜叶|右上植物影|双色横切|节气日期|宋体标题", "无判断模板结构：借用须有主题理由（SKILL.md 严格禁止）"),
]

CLEAN_FIXTURE = """为小红书创作一张 3:4 即时成像摄影，主题为“一场雨之后”。
创作命题：雨刚停，屋檐还在归还积攒的水。
窗口物证：残留物——窗台上一把收了一半的湿伞，伞沿悬着一滴水。
摄影逻辑：35mm 定焦近距，手持透视；现场光为阴天窗光单一来源；色彩由湿/干张力对推导，冷灰占大部分，伞面一点暖。
文字：相纸白边手写一行“伞沿还在滴水”。
约束：主体为物证而非摆拍人物；相纸为染料显影质感。"""

DIRTY_FIXTURE = """创作一张节气海报，主题立春：嫩芽破土，旁边配荷叶点缀。
今日此地，拍下今年最早的春雨。
角落加一个红点做强调，背景泛黄做旧，再来一点赛博霓虹光。
文案配一首古诗点题，加一句英文口号，底部铺密集微字和假英文。
右上植物影配斜叶越过窗口，画一座鹊桥和玉兔。
角落加个 logo 和水印，日期写成假日期。"""

ERRORS = []


def lint(text, allow=()):
    """返回 [(行号, 命中词, 规则出处)]；allow 为放行子串列表。"""
    hits = []
    for lineno, line in enumerate(text.splitlines(), 1):
        for pattern, rule in RULES:
            for m in re.finditer(pattern, line, re.IGNORECASE):
                if any(a.lower() in m.group(0).lower() for a in allow):
                    continue
                hits.append((lineno, m.group(0), rule))
    return hits


def selftest():
    """干净样例必须零命中；脏样例必须让每条规则至少命中一次（规则无正例=测试失败）。"""
    global ERRORS
    clean_hits = lint(CLEAN_FIXTURE)
    if clean_hits:
        ERRORS.append(f"干净样例出现 {len(clean_hits)} 个误报：{clean_hits[:3]}")
    dirty_hits = lint(DIRTY_FIXTURE)
    hit_rules = {rule for _, _, rule in dirty_hits}
    for _, rule in RULES:
        if rule not in hit_rules:
            ERRORS.append(f"规则「{rule}」在脏样例中无正例覆盖，请在 DIRTY_FIXTURE 中补一个命中")
    if ERRORS:
        print("❌ lint 自检失败：")
        for e in ERRORS:
            print(f"  - {e}")
        return 2
    print(f"✅ lint 自检通过：干净样例零误报，{len(RULES)} 条规则全部有正例覆盖")
    return 0


def main():
    parser = argparse.ArgumentParser(description="生成提示词的禁词 lint")
    parser.add_argument("files", nargs="*", help="待检查的提示词文本文件；缺省读 stdin")
    parser.add_argument("--allow", action="append", default=[],
                        help="放行含指定子串的命中，可多次给出")
    parser.add_argument("--selftest", action="store_true", help="运行内置正反例自检")
    args = parser.parse_args()

    if args.selftest:
        sys.exit(selftest())

    if args.files:
        text = "\n".join(open(f, encoding="utf-8").read() for f in args.files)
        label = ", ".join(args.files)
    else:
        text = sys.stdin.read()
        label = "stdin"

    hits = lint(text, allow=args.allow)
    if hits:
        print(f"❌ {label}：{len(hits)} 个候选违规（供人工复核，确有主题依据可 --allow 放行）：")
        for lineno, word, rule in hits:
            print(f"  L{lineno} 「{word}」—— {rule}")
        sys.exit(1)
    print(f"✅ {label}：无候选违规（{len(RULES)} 条规则）")
    sys.exit(0)


if __name__ == "__main__":
    main()
