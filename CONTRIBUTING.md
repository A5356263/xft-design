# Maintaining xft-design

本文件给维护者看，不参与页面生成。
除非用户明确要求维护或修改 skill，否则不得读取。

## 问题归因

| 现象 | 修改位置 |
|---|---|
| 路由判断错 | SKILL.md → Routing Rules |
| 跳过 Route Decision | SKILL.md → Stable Flow / Route Decision Record |
| shell 漂移 / 结构被重写 | SKILL.md → Copy-as-template Execution Protocol，或 shell 资产本身 |
| shell 占位文案残留 | SKILL.md → Shell Chrome Text Replacement |
| class 对不上 | assets/page-blocks.html / assets/overlays.html / components.css |
| token 不一致 | design-systems/tokens.css / components.css |
| validator 误报 / 漏报 | scripts/check_skill_output.py |
| 历史示例污染 | 移入 examples/archive/，确认 SKILL.md Archive 段禁止读取 |
| 页面结构类型不够 | assets/page-blocks.html 或 references/layouts.md |
