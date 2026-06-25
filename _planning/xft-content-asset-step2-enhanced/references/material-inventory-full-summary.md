# 第 2 步增强版：素材包完整盘点

## 盘点口径

本次以用户重新上传的 `场景.zip` 为准，不再只依据 5 张汇总图。

- 压缩包成员总数：113
- 有效图片素材：91
- 系统文件 / 目录：22
- 覆盖状态：所有有效图片均已进入 `material-inventory-full.csv`

## 按素材类型统计

| 类型 | 数量 |
|---|---:|
| 典型页面 | 17 |
| 数据展示 | 15 |
| 数据录入 | 13 |
| 反馈 | 11 |
| 复杂场景 | 11 |
| 按钮规则 | 10 |
| 导航 | 10 |
| 复杂场景/公式编辑器 | 4 |

## 按资产层级统计

| 资产层级 | 数量 |
|---|---:|
| page_recipe | 17 |
| business_module | 15 |
| component_combo | 12 |
| display_component_combo | 8 |
| navigation_region | 7 |
| display_module | 6 |
| interaction_rule | 6 |
| state_asset | 5 |
| overlay_asset | 4 |
| component_combo_rule | 4 |
| feedback_rule_asset | 3 |
| shell_navigation_rule | 3 |
| form_region | 1 |

## 按优先级统计

| 优先级 | 数量 |
|---|---:|
| P1 | 46 |
| P0 | 37 |
| P2 | 8 |

## 直接 HTML 转化判断

| needs_direct_html | 数量 |
|---|---:|
| partial | 44 |
| yes | 41 |
| no | 6 |

## 这一步的性质

这一步是“完整素材盘点 + 资产转化路线判断”。

它已经可以作为后续步骤的素材索引使用，但还不是最终可装配资产。

- 可以交给后续 Agent 读取，作为素材清单。
- 不能直接拿来生成页面。
- 后续第 3～7 步会继续把素材转成页面配方、规则表、HTML 片段。

## 不漏素材的约束

后续每一步都必须以 `data/material-inventory-full.csv` 为来源清单。
任何新增资产、规则或 HTML 片段，都需要回填对应的 `material_id`。
如果某个素材暂不转化，也必须在后续文档中标记 `deferred`，不能静默忽略。
