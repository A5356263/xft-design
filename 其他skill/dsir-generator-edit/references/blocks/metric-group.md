# `metric_group（指标组块）`

## 定义

用于在列表主执行区上方或附近，表达与当前结果集相关的概览指标。

## 语义目标

- 提供总体概览
- 辅助理解当前记录集合状态
- 为后续筛选或处理提供上下文

## 允许出现的区域

- `primary_content（主内容区）`
- 少量场景下可在 `sidebar（侧边区域）`

## 最小语义载荷

- `metric_scope（指标范围）`
- `metric_items（指标项）`
- `comparison_basis（比较基准）`

## 使用的 `content model（内容模型）`

- `scalar_metrics（单值指标集合）`

## 能力范围

- `summary_metrics（摘要指标）`
- `status_breakdown（状态拆分）`
- `comparative_metrics（对比指标）`
- `clickable_metrics（可点击指标入口）`

## 已确认变体

- 当前首批不单独定义固定变体

## 不应混入的内容

- 详细分析图表
- 主结果表格
- 分页控制

## 常见搭配

- `filter_form（筛选表单块）`
- `record_table（记录表格块）`
