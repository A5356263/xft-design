# `filter_form（筛选表单块）`

## 定义

用于表达对 `record collection（记录集合）` 的筛选条件集合。

## 语义目标

- 缩小结果范围
- 支持条件检索
- 提供查询与重置入口

## 允许出现的区域

- `primary_content（主内容区）`

## 最小语义载荷

- `filter_fields（筛选字段）`
- `query_scope（查询范围）`
- `submit_actions（提交动作）`

## 使用的 `content model（内容模型）`

- `query_conditions（查询条件集合）`

## 能力范围

- `inline_layout（行内布局）`
- `stacked_layout（堆叠布局）`
- `collapsible（可折叠）`
- `advanced_filters（高级筛选）`
- `saved_filter_capable（可保存筛选）`

## 已确认变体

- 当前首批不单独定义固定变体

## 不应混入的内容

- 结果表格
- 批量操作集合
- 分页控制

## 常见搭配

- `action_cluster（动作集合块）`
- `record_table（记录表格块）`
