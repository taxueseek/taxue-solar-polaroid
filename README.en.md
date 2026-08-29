<p align="center">
  <a href="README.md">简体中文</a> · English
</p>

<p align="center">
  <img src="./assets/readme/hero.jpg" width="100%" alt="Taxue Solar Polaroid: give it a theme, and it derives the scene and the picture. Right: finished images for Lichun and Yuanxiao.">
</p>

<p align="center">
  <a href="#gallery">Gallery</a> ·
  <a href="#philosophy">Philosophy</a> ·
  <a href="#four-modes">Modes</a> ·
  <a href="#how-it-works">How it works</a> ·
  <a href="#get-started">Get started</a>
</p>

# Taxue Solar Polaroid

A prompt skill for the 24 solar terms and festivals: turn a solar term, a seasonal phrase, or a place-bound memory into an original editorial visual with real evidence, natural Chinese copy, and its own spatial logic.

## Gallery

Two sets of finished images. From afar they read as one paper-archive series; up close, every window and every line of copy is its own. Click a name for the full-size image.

### Solar terms

Eight images, from Lichun to Daxue.

<p align="center">

![Solar-term wall: Lichun, Yushui, Guyu, Xiazhi, Chushu, Bailu, Dongzhi, Daxue](./assets/readme/solar-wall.jpg)

</p>

<p align="center">
<a href="./gallery/lichun-hybrid-no-mark.jpg">Lichun</a> ·
<a href="./gallery/yushui-hybrid.jpg">Yushui</a> ·
<a href="./gallery/guyu-hybrid.jpg">Guyu</a> ·
<a href="./gallery/xiazhi-hybrid.jpg">Xiazhi</a> ·
<a href="./gallery/chushu-hybrid.jpg">Chushu</a> ·
<a href="./gallery/bailu-hybrid.jpg">Bailu</a> ·
<a href="./gallery/dongzhi-hybrid.jpg">Dongzhi</a> ·
<a href="./gallery/daxue-hybrid-no-mark.jpg">Daxue</a>
</p>

### Festivals

Six images: Spring Festival, Lantern Festival, Dragon Boat, Qixi, Mid-Autumn, Chongyang. No magpie bridges, moon rabbits or dragon boats — the visible evidence is, in order: ashes on red paper, warm lantern paper, soaked bamboo leaves, two stars and one line, moonlight in an empty cup, an unfinished stone stair.

<p align="center">

![Festival wall: Chunjie, Yuanxiao, Duanwu, Qixi, Zhongqiu, Chongyang](./assets/readme/festival-wall.jpg)

</p>

<p align="center">
<a href="./gallery/chunjie-hybrid.jpg">Spring Festival</a> ·
<a href="./gallery/yuanxiao-hybrid.jpg">Lantern Festival</a> ·
<a href="./gallery/duanwu-hybrid.jpg">Dragon Boat</a> ·
<a href="./gallery/qixi-hybrid.jpg">Qixi</a> ·
<a href="./gallery/zhongqiu-hybrid.jpg">Mid-Autumn</a> ·
<a href="./gallery/chongyang-hybrid.jpg">Chongyang</a> ·
<a href="./gallery/README.md">All originals</a>
</p>

## Philosophy

「Lichun」 does not mean a sprout. 「Chushu」 does not mean a lotus leaf. 「Qixi」 does not mean the Cowherd and the Weaver Girl. Every theme, in a different place, with different materials and different memories, should grow into a different picture.

This skill first builds a **creative inference card**, then chooses medium, form, space and copy:

- **Theme core**　one sentence on "what is changing, and how"
- **Evidence**　the user's place, materials and memory come first; otherwise marked as creative interpretation
- **Tension pair**　wet/dry, near/far, gathering/scattering, still/moving — drives color and space
- **Core form**　derived from direction, process, connection or rupture; never a plant by default
- **Spatial rule**　grid, folded pages, negative space, layering, archive sheets — never a centered card by default
- **Medium**　paper, photography, silkscreen, fabric, glass — never fake aging as texture
- **Copy voice**　observation, record, whisper, index — every line traceable to visible evidence

**Truthfulness discipline:** when the user gives no place or date, no 「today」, 「here」 or 「earliest this year」; no classical poems, allusions or solar-term slogans; no invented weather or phenology.

**Versus prompt libraries:** a prompt library picks the closest of ten thousand; this is seven inference variables that grow one prompt out of your theme. Same input, different place or memory — different picture.

## Four modes

- **Hybrid** (default)　only a theme is given: open inference decides the content, the paper-archive structure provides series identity.
- **Open**　no template wanted, concept poster wanted: pure open inference, free of the paper frame.
- **Fixed framework**　archive pages and series feel wanted: paper and reading hierarchy locked, theme still variable.
- **Photography (evidence polaroid)**　people, street shots, lens feel wanted: camera and space, no paper archive; the polaroid window pins down theme evidence, not a remake of viral celebrity selfies.

As many images as you ask for. Multi-image sets first get an **interpretation matrix**: each image changes at least two of theme angle, evidence, core form, spatial rule, medium, copy voice — recoloring or mirroring one card is forbidden.

## Phenology clues

`references/seasonal-evidence-library.md` lists common change directions for each solar term, as creative candidates only. One state shift and one piece of visible evidence per term. The user's place, time and materials always come first.

## How it works

<p align="center">
  <img src="./assets/readme/workflow.svg" width="100%" alt="From theme to prompt: build the inference card, choose a visual route, compile the prompt, deliver and iterate">
</p>

1. **Build the creative inference card**　theme core, evidence, tension pair, core form, spatial rule, medium, copy voice — in that order.
2. **Choose a visual route**　hybrid by default; open, fixed framework or photography on request.
3. **Compile the prompt**　fixed order: purpose & count → proposition → evidence → visual verb → space & medium → color & light → text → constraints.
4. **Deliver & iterate**　inference, visual plan, paste-ready prompt, in-image text, truthfulness notes; next round changes one variable only.

## Get started

```bash
npx skills add taxueseek/taxue-solar-polaroid
```

Then just say:

- 「立春」 (Lichun)　「元宵」 (Lantern Festival)　「春去秋来」 (spring goes, autumn comes)
- 「用纸本档案的感觉做一张谷雨海报」 (a Guyu poster with a paper-archive feel)
- 「立夏，四张，一组杂志内页」 (Lixia, four images, magazine pages)
- 「雨后的傍晚，落地窗，拍立得感觉」 (after the rain, at dusk, floor-to-ceiling window, polaroid feel)

The skill reads Chinese best — copy these lines as-is.

## File structure

```text
taxue-solar-polaroid/
├── README.md
├── README.en.md
├── SKILL.md
├── gallery/              # 8 solar terms, 6 festivals
├── references/           # inference, dual-layer routing, phenology, evidence polaroid
├── templates/
├── assets/readme/        # 5:2 hero, walls, workflow
└── scripts/              # read-only consistency check + prompt lint
```

## Privacy

This skill collects nothing. It does one thing: compile a theme into a prompt. Your places, dates, materials and memories appear only in the conversation — never leave your machine, never stored.

## License

MIT
