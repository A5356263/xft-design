# `primary_content（主内容区）`

## 语义职责

页面主业务执行区，用于完成筛选、查看、切换和处理记录集合。

## 允许的 `block pattern（语义块模式）`

- `metric_group（指标组块）`
- `filter_form（筛选表单块）`
- `action_cluster（动作集合块）`
- `local_primary_action（局部主动作块）`
- `view_switcher（视图切换块）`
- `record_table（记录表格块）`
- `pagination_footer（分页底部块）`

## 默认 / 可选组合

- 默认：`filter_form（筛选表单块） + action_cluster（动作集合块） + record_table（记录表格块） + pagination_footer（分页底部块）`
- 可选：`metric_group（指标组块）`、`view_switcher（视图切换块）`、`local_primary_action（局部主动作块）`

## 关键规则

- `record_table（记录表格块）` 是标准 `list-management（列表管理页）` 的核心块
- `view_switcher（视图切换块）` 只在其仍服务于同类记录集合切换时使用
- 当某个局部容器内只有一个独立且显著的主操作入口时，可使用 `local_primary_action（局部主动作块）`

## 不建议放入的内容

- 全局导航类 `block（语义块）`
- 仅用于壳层身份识别的内容
