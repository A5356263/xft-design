# 页面配方选择规则

## 选择顺序

页面配方选择必须按以下顺序执行：

```text
1. 先判断 scope
2. 再判断 page_type
3. 再匹配 recipe_id
4. 再决定 required_regions
5. 再决定 optional_modules
```

## 优先级规则

### 审批优先

只要需求包含审批、流程、流转、待办审批、审批详情，优先选择：

```text
recipe.workflow.detail
```

不要退化成普通详情页。

### 复杂配置优先

只要需求包含字段配置、表头设置、筛选项配置、公式编辑，优先选择：

```text
recipe.complex.config
```

不要退化成普通设置页。

### 分步优先于普通表单

需求包含分步、步骤、多阶段、流程化提交时，选择：

```text
recipe.form.step
```

不要选择普通表单。

### 父子关系优先于普通表格

需求包含组织树、分类树、左树右表、主从数据时，选择：

```text
recipe.table.parent-child
```

不要选择基础表格。

### 汇总/报表区别

- 以查询明细为主，附带少量指标：`recipe.table.summary`
- 以统计分析、导出、条件查询为主：`recipe.table.report`

## 禁止事项

- 不得直接基于整页截图生成整页 HTML。
- 不得跳过页面配方直接选择区域资产。
- 不得在没有 CONTENT_ASSET_DECISION 的情况下生成内容区。
- 不得把未命中的低频复杂场景硬编成自定义布局。
- 缺少资产时，应回退到最接近的通用资产，并记录 fallback。

## 输出格式建议

后续 SKILL.md 中应新增：

```html
<!-- CONTENT_ASSET_DECISION
page_recipe: recipe.table.basic
required_regions: region.page-header.basic, region.filter-bar.basic, region.table-toolbar.basic, region.data-table.basic, region.pagination.basic
optional_modules: module.batch-action-footer, overlay.detail-drawer
fallback: none
-->
```
