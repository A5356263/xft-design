# `view_switcher（视图切换块）`

## 定义

用于在同一业务域下，对同类记录集合做状态、口径或子视图切换。

## 语义目标

- 切换记录集合视图
- 在不离开当前页面的前提下做视图分流

## 允许出现的区域

- `primary_content（主内容区）`
- 少量场景下可在 `route_nav_bar（路径任务导航区）`

## 最小语义载荷

- `view_options（视图选项）`
- `switch_goal（切换目标）`
- `shared_record_scope（共享记录范围）`

## 使用的 `content model（内容模型）`

- `view_options（视图选项）`

## 能力范围

- `status_switching（状态切换）`
- `subscope_switching（子范围切换）`
- `counts_with_views（视图计数）`

## 已确认变体

- 当前首批不单独定义固定变体

## 不应混入的内容

- 全局页签导航
- 记录表格主体

## 常见搭配

- `filter_form（筛选表单块）`
- `record_table（记录表格块）`
