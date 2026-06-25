# xft-content-asset-step2-enhanced

这是第 2 步增强版产物：基于 `场景.zip` 的完整素材包盘点。

## 文件说明

- `data/material-inventory-full.csv`
  - 91 张有效图片的完整清单
  - 每张图都有素材编号、来源路径、资产层级、是否转 HTML、是否转规则、优先级、建议目标路径

- `data/material-category-summary.csv`
  - 按素材类型、资产层级、优先级统计

- `references/material-inventory-full-summary.md`
  - 本次盘点摘要

- `references/conversion-batches-full.md`
  - 后续分批转化建议

- `_source_manifest/zip-member-manifest.csv`
  - 原始 zip 成员清单，用来防止遗漏

## 使用方式

现在可以放入 Codex 工作区 `_planning/xft-content-asset-step2-enhanced/`。

这一步仍然不要直接让 Agent 改项目。
如果要给 Agent 看，也只让它阅读，不要执行文件迁移。
