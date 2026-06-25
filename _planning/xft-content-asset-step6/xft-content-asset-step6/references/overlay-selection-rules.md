# 覆盖层选择规则

## Modal

适合短流程、少字段、需要用户集中处理的任务。

## Drawer

适合保留当前页面上下文的详情查看、复杂配置、较长表单。

## Confirm Modal

适合删除、撤销、作废、提交等高风险动作。

## Popconfirm

适合行内轻量确认，不能承载复杂说明。

## 禁止事项

- 不得把 overlay 写入 page-content-container。
- 不得用 Message 承载确认动作。
- 不得用 Popconfirm 处理批量高风险操作。
- 不得让 Drawer 替代短确认弹窗。
