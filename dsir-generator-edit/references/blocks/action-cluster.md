# `action_cluster（动作集合块）`

## 定义

用于表达一组面向当前页面或当前结果集的动作集合，并明确动作主次。

## 语义目标

- 承载页面主动作
- 承载批量动作
- 承载辅助动作

## 允许出现的区域

- `primary_content（主内容区）`
- 部分场景下可出现在 `shell_header（全局页头区）`

## 最小语义载荷

- `primary_action（主动作）`
- `secondary_actions（次级动作）`
- `utility_actions（辅助动作）`

## 使用的 `content model（内容模型）`

- `action_set（动作集合）`

## 能力范围

- `bulk_action_capable（批量动作能力）`
- `split_priority_actions（主次动作分层）`
- `overflow_actions（溢出动作）`
- `selection_dependent_actions（依赖选中状态的动作）`

## 呈现语义

常见的 `presentation_preference（呈现偏好）` 应表达为：
- `primary_group_alignment（主动作组对齐）`: `leading（左侧起始）`
- `utility_group_alignment（辅助动作组对齐）`: `trailing（右侧结束）`
- `group_separation（动作分组分离）`: `split_groups（主辅分组）`
- `primary_emphasis（主动作强调）`: `high（高）`
- `utility_emphasis（辅助动作强调）`: `low（低）`

当一个动作集合中左侧主要承载高频主动作、常规操作，右侧主要承载低频设置、字段设置、表头设置等内容时：
- 这属于 `presentation_preference（呈现偏好）` 的表达
- 不属于新的 `content model（内容模型）`
- 右侧内容通常仍落在 `secondary_actions（次级动作）` 或 `utility_actions（辅助动作）` 中

## 已确认变体

- 当前首批不单独定义固定变体

## 不应混入的内容

- 单个独立局部新增入口
- 结果表格
- 分页控制

## 常见搭配

- `filter_form（筛选表单块）`
- `record_table（记录表格块）`
