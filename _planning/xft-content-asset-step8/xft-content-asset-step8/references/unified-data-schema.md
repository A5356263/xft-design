# 统一检索数据表说明

本步骤将第 3～7 步的页面配方、区域资产、模块资产、反馈/状态/覆盖层资产、组件组合资产整合为统一检索数据。

## 核心表

- `data/content-assets.csv`：统一资产索引。后续检索脚本的主表。
- `data/asset-keywords.csv`：关键词倒排表。用于提升中文关键词召回稳定性。
- `data/asset-rules.csv`：资产规则与校验规则。用于过滤、排序、装配前校验。
- `data/recipe-rules.csv`：页面配方表。用于先选页面结构，再选内容资产。
- `data/page-type-router.csv`：页面类型路由。用于从需求判断页面类型与配方。
- `data/recipe-asset-map.csv`：页面配方与候选资产的关系。
- `data/asset-source-map.csv`：资产来源与目标路径映射。后续交给 Codex 复制资产时使用。

## content-assets.csv 字段

| 字段 | 说明 |
|---|---|
| asset_id | 唯一资产编号 |
| asset_layer | 资产层级：region/module/feedback/state/overlay/component_combo |
| asset_type | 资产类型 |
| asset_name | 资产名称 |
| page_type | 适用页面类型 |
| keywords | 召回关键词 |
| conditions | 使用条件 |
| forbidden_when | 禁用条件 |
| variant | 变体 |
| html_path | 装配时读取的 HTML 片段路径 |
| css_path | 该资产依赖的补充 CSS 路径 |
| slots | 插槽 |
| priority / priority_rank | 优先级 |
| validation | 装配校验规则 |
| source_materials | 来源素材编号 |
| source_step | 来源步骤 |

## 重要原则

1. 先选页面配方，再选资产。
2. `content-assets.csv` 只负责资产索引，不直接替代 HTML 资产。
3. 命中资产后，必须读取 `html_path` 对应片段，不允许 AI 重新写同类布局。
4. 多资产冲突时，先看页面配方 required，再看 `priority_rank`，最后看规则过滤。
