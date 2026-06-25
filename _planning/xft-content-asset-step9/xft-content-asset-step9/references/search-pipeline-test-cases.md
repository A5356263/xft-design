# 检索管道测试用例

## 用例 1：基础列表页

输入：

```text
生成员工花名册列表页，支持姓名、组织、状态筛选，支持批量导出和查看详情
```

期望：

- page_type = TablePage
- recipe = recipe.table.basic
- 必须包含 page-header、filter-bar、table-toolbar、data-table、pagination
- 可选命中 batch-action-footer、detail-drawer

## 用例 2：审批详情页

输入：

```text
生成审批单详情页，需要展示基础信息、审批流、附件和操作记录
```

期望：

- page_type = DetailPage
- recipe 优先详情/审批相关配方
- 必须包含 detail-summary、detail-info-section
- 可选命中 approval-flow、upload/file、operation-log

## 用例 3：复杂配置页

输入：

```text
生成公式配置页面，支持字段选择、公式编辑、智能助手和保存发布
```

期望：

- page_type = SettingsPage 或 ConfigPage
- 命中 settings-layout
- 可选命中 formula-editor、formula-helper
- 提交类按钮位于底部或配置区右侧固定操作区

## 用例 4：分步表单

输入：

```text
生成新建申请表单，需要分三步填写基础信息、业务信息和确认提交
```

期望：

- page_type = CreatePage
- recipe = recipe.form.step
- 命中 steps、form-section、form-footer-actions

## 用例 5：异步导入

输入：

```text
生成批量导入任务页面，上传文件后展示异步处理进度和结果
```

期望：

- page_type = TablePage 或 CreatePage
- 命中 upload-file、async-processing、progress/result
- 不允许只给 Message 全局提示作为唯一反馈
