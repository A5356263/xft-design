# `capability（能力）` 与 `variant（变体）` 判断规则

## `capability（能力）`

满足以下条件时，优先归为 `capability（能力）`：
- 不改变语义块本质
- 不改变主要结构
- 不改变主要交互模型
- 只是说明该块支持什么

例子：
- `category_tree（分类树块）` 支持 `multi_selectable（可多选）`
- `record_table（记录表格块）` 支持 `row_selectable（可选行）`
- `filter_form（筛选表单块）` 支持 `collapsible（可折叠）`

## `variant（变体）`

满足以下条件时，才考虑归为 `variant（变体）`：
- 改变主要结构
- 改变主要交互模型
- 改变主要使用方式

## 默认规则

- 先写 `capability（能力）`
- 只有充分证据时才升为 `variant（变体）`
- 不要因为布局变化、新增相邻块、视觉权重变化就定义新变体
