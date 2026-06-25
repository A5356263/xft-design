# CONTENT_ASSET_DECISION 协议

## 作用

CONTENT_ASSET_DECISION（内容资产决策）用于把“用户需求”变成“可读取、可装配、可校验的资产清单”。

## 必填字段

| 字段 | 含义 |
|---|---|
| decision_type | 固定为 CONTENT_ASSET_DECISION |
| page_type | 页面类型 |
| recipe_id | 页面配方编号 |
| shell | 壳子 |
| selected_assets | 被选中的资产清单 |
| support_css | 需要注入的补充 CSS（层叠样式表） |
| unsupported | 暂不支持项 |
| validation_targets | 校验目标 |

## selected_assets 字段

| 字段 | 含义 |
|---|---|
| asset_id | 资产编号 |
| asset_type | 资产类型 |
| html_path | HTML（超文本标记语言）路径 |
| insert_slot | 插入插槽 |
| order | 装配顺序 |
| required | 是否必选 |
| reason | 选择原因 |

## 硬规则

- selected_assets 只能来自 `content-assets.csv`。
- html_path 必须存在。
- 同一 insert_slot 内按 order 升序装配。
- required 为 true 的资产不得缺失。
- 冲突资产必须按 `conflict-resolution-rules.csv` 处理。
