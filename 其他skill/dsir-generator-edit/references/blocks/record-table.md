# `record_table（记录表格块）`

## 定义

用于承载 `record collection（记录集合）` 的主结果展示。

## 语义目标

- 展示记录集合
- 支持快速扫描
- 支持单条或批量后续处理

## 允许出现的区域

- `primary_content（主内容区）`

## 最小语义载荷

- `record_scope（记录范围）`
- `columns（列语义）`
- `row_identity（行标识）`

## 使用的 `content model（内容模型）`

- `record_collection（记录集合）`

## 能力范围

- `row_selectable（可选行）`
- `multi_row_selectable（可多选行）`
- `row_actions（行级动作）`
- `empty_state_capable（空状态能力）`
- `wide_table_capable（宽表能力）`
- `grouped_records（分组记录）`

## 已确认变体

- 当前首批不单独定义固定变体

## 不应混入的内容

- 筛选字段定义
- 主动作集合
- 分页控制

## 常见搭配

- `filter_form（筛选表单块）`
- `action_cluster（动作集合块）`
- `pagination_footer（分页底部块）`
