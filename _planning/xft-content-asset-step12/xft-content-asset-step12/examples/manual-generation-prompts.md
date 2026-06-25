# 手工生成验证用 Prompt

用于第 12 步人工验收页面效果。

## 1. 列表页

```text
用 xft-design 生成员工花名册列表页，包含按组织、岗位、状态筛选，支持批量导出、列设置、查看详情。必须先输出 CONTENT_ASSET_DECISION。
```

## 2. 审批详情页

```text
用 xft-design 生成审批详情页，包含基础信息、审批流、附件、操作记录、当前状态和返回操作。必须先输出 CONTENT_ASSET_DECISION。
```

## 3. 表单页

```text
用 xft-design 生成新建申请表单页，包含基础信息、业务信息、附件上传和底部提交操作。必须先输出 CONTENT_ASSET_DECISION。
```

## 4. 设置页

```text
用 xft-design 生成参数设置页，左侧为设置分组，右侧为设置项，包含启用状态和配置操作。必须先输出 CONTENT_ASSET_DECISION。
```

## 5. 弹窗

```text
用 xft-design 生成成员编辑弹窗，包含基础字段、手机号、角色选择、确认和取消。只生成弹窗，不要扩写完整后台页面。
```
