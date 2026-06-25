# xft-content-asset-step4

第 4 步产物：区域资产包。

## 包含

- `assets/regions/`：可直接装配的区域 HTML 片段
- `assets/regions/_region-support.css`：区域资产需要的补充 CSS
- `data/region-assets.csv`：区域资产清单，可用于后续检索
- `data/region-material-map.csv`：素材与区域资产映射
- `_coverage/material-coverage-step4.csv`：91 张素材的本步覆盖状态
- `references/region-assets.md`：区域资产说明
- `references/region-composition-rules.md`：区域组合规则

## 当前使用方式

先放入 `_planning/xft-content-asset-step4/`，不要直接覆盖现有 skill。

等第 5、6、7 步完成后，再由 Codex 根据总改造文档统一合并到 `.claude/skills/xft-design/`。
