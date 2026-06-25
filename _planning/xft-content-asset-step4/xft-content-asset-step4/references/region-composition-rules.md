# 区域组合规则

## 列表页

默认顺序：

```text
page-header
→ filter-bar
→ page-card(table-toolbar + data-table + pagination)
```

规则：

- 筛选区和表格工具栏必须分离。
- 查询/重置放筛选区，不放表格工具栏。
- 新建、导出、列设置放表格工具栏。
- 分页在表格下方。
- 批量操作依赖多选状态，不要塞进行内操作。

## 表单页

默认顺序：

```text
page-header
→ step-indicator（可选）
→ form-section
→ form-footer-actions
```

规则：

- 表单字段多时按 section 分组。
- 底部操作区承载提交/取消。
- 分步表单使用步骤条，不使用标签页替代。

## 详情页

默认顺序：

```text
page-header.with-back
→ detail-summary
→ detail-info-section
→ optional modules
```

规则：

- 摘要区优先暴露状态、负责人、时间、编号。
- 只读详情不用表单控件。
- 内容较长时用右侧锚点或左右布局。

## 设置页

默认顺序：

```text
page-header
→ settings-layout.anchor
→ setting-section
```

规则：

- 设置项左侧是标题和说明，右侧是状态或操作。
- 设置页不要默认改成数据表格。
- 配置项多时使用左侧锚点。

## 首页/报表页

默认顺序：

```text
page-header
→ metric-grid / report-summary-bar
→ dashboard-grid / table-region
```

规则：

- 指标卡片用于概览，不承载复杂操作。
- 报表页可使用筛选区 + 汇总区 + 表格区。
