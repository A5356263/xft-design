# XFT 内容资产模型 v1

> 目标：把设计素材图、页面样本、组件规范转成可检索、可装配、可校验的 Skill 资产，而不是让 AI 自由阅读规范后现场写布局。

## 1. 核心原则

### 1.1 资产不是设计说明

最终 Skill 不应让 AI 根据设计说明自由发挥，而应让 AI：

```text
需求 → 页面类型 → 页面配方 → 内容资产 → 变体 → HTML 装配 → 校验
```

### 1.2 资产必须可直接使用

凡是进入 `assets/` 的内容，必须是可复制、可插入、可校验的 HTML 片段。

不允许把图片、长篇规范、解释性文本当作最终资产。

### 1.3 结构固定，内容可填

固定：

- 区域顺序
- 模块位置
- 对齐关系
- 插槽结构
- class 名
- token 使用方式

可填：

- 业务字段名
- 表格列名
- 示例数据
- 按钮文案
- 说明文案

---

## 2. 资产分层

```text
page-recipes       页面配方
regions            区域资产
modules            业务模块资产
component-combos   组件组合资产
states             状态资产
overlays           覆盖层资产
rules              规则数据，放在 data/*.csv
```

### 2.1 Page Recipe（页面配方）

定义一个页面默认由哪些区域和模块组成。

例：TablePageRecipe

```text
PageHeader
→ FilterBar
→ TableToolbar
→ DataTable
→ Pagination
→ optional: BatchActionFooter
→ optional: DetailDrawer
```

特点：

- 不直接写完整页面 HTML
- 负责决定默认组合顺序
- 是页面装配的骨架

### 2.2 Region（区域资产）

页面中稳定出现的大区域。

例：

- PageHeader
- FilterBar
- TableToolbar
- DataTableRegion
- PaginationRegion
- FormSection
- DetailSummary
- SettingsGroup

特点：

- 可直接插入页面
- 有固定 class 和插槽
- 是第一优先级资产

### 2.3 Module（业务模块资产）

带业务语义的复合模块。

例：

- ApprovalFlow
- AttachmentList
- OperationLog
- RelatedTable
- AsyncProgress
- HeaderColumnSetting
- FormulaEditor

特点：

- 通常依赖特定页面或区域
- 需要更明确的使用条件
- 可作为详情页、表单页、设置页的扩展模块

### 2.4 Component Combo（组件组合资产）

多个基础组件形成的固定组合。

例：

- SearchInputWithButton
- LabelControlPair
- StatusTagGroup
- PrimarySecondaryButtonGroup
- InlineActionGroup
- CheckboxTreeSelector

特点：

- 颗粒度比 region 小
- 主要服务 region/module 内部插槽
- 防止 AI 临时组合组件

### 2.5 State（状态资产）

页面或局部区域的状态表达。

例：

- EmptyState
- LoadingState
- ErrorState
- NoPermissionState
- SuccessResult
- FailResult
- SkeletonState

特点：

- 可替换页面主体或局部区域
- 必须有触发条件
- 必须避免与正常内容同时冲突显示

### 2.6 Overlay（覆盖层资产）

悬浮在页面上的交互容器。

例：

- ModalForm
- DrawerDetail
- DrawerConfig
- ConfirmDialog
- PopoverInfo

特点：

- 必须挂载到 overlay slot
- 不允许写进普通内容流
- 必须有触发源和关闭动作

---

## 3. 资产文件结构

建议放在 skill 根目录：

```text
.claude/skills/xft-design/
├── assets/
│   ├── page-recipes/
│   ├── regions/
│   ├── modules/
│   ├── component-combos/
│   ├── states/
│   └── overlays/
├── data/
│   ├── content-assets.csv
│   ├── recipe-rules.csv
│   ├── asset-rules.csv
│   └── asset-keywords.csv
├── references/
│   └── content-asset-model.md
└── scripts/
    ├── search_assets.py
    └── check_asset_output.py
```

---

## 4. 每个资产必须包含的信息

### 4.1 必填字段

| 字段 | 说明 |
|---|---|
| asset_id | 资产唯一 ID |
| asset_name | 资产名称 |
| asset_type | page_recipe / region / module / component_combo / state / overlay |
| page_type | TablePage / DetailPage / FormPage / SettingsPage / DashboardPage / ResultPage / ExceptionPage / Any |
| keywords | 命中关键词 |
| intent | 使用意图 |
| conditions | 使用条件 |
| forbidden_when | 禁用条件 |
| variant | 变体名称 |
| html_path | HTML 片段路径 |
| slots | 可填插槽 |
| required_with | 依赖资产 |
| forbidden_with | 冲突资产 |
| priority | 优先级 |
| validation | 校验规则 |

### 4.2 资产 ID 命名

```text
{type}.{domain}.{name}.{variant}
```

例：

```text
region.table.filter-bar.basic
region.table.filter-bar.advanced-expand
module.detail.approval-flow.vertical
state.common.empty.simple
overlay.form.modal.basic
```

---

## 5. 页面类型建议

第一版页面类型：

| page_type | 说明 |
|---|---|
| TablePage | 查询、筛选、表格、分页、批量操作 |
| DetailPage | 查看对象详情、状态、关联信息、操作记录 |
| FormPage | 新建、编辑、提交、申请 |
| SettingsPage | 参数配置、权限配置、偏好设置 |
| DashboardPage | 指标、趋势、待办、快捷入口 |
| ResultPage | 成功、失败、处理中结果 |
| ExceptionPage | 403、404、500、无权限 |
| BlankPage | 无导航或独立页面 |

---

## 6. 页面配方初版

### 6.1 TablePageRecipe

```text
PageHeader
→ FilterBar
→ TableToolbar
→ DataTableRegion
→ PaginationRegion
→ optional: BatchActionFooter
→ optional: DrawerDetail
```

### 6.2 DetailPageRecipe

```text
PageHeaderWithActions
→ DetailSummary
→ DetailInfoSection
→ optional: ApprovalFlow
→ optional: RelatedTable
→ optional: AttachmentList
→ optional: OperationLog
```

### 6.3 FormPageRecipe

```text
PageHeader
→ FormSectionGroup
→ optional: DynamicDetailTable
→ optional: AttachmentUpload
→ FormFooterActions
```

### 6.4 SettingsPageRecipe

```text
SettingsLayout
→ SettingsAnchor
→ SettingsGroup
→ SettingItemList
→ optional: DrawerConfig
```

### 6.5 DashboardPageRecipe

```text
PageHeader
→ MetricCardGroup
→ ChartGrid
→ TaskOrShortcutPanel
→ optional: ActivityFeed
```

### 6.6 ResultPageRecipe

```text
ResultStatus
→ ResultDescription
→ ResultActions
→ optional: ResultExtraInfo
```

### 6.7 ExceptionPageRecipe

```text
ExceptionIllustration
→ ExceptionTitle
→ ExceptionDescription
→ ExceptionActions
```

---

## 7. 装配规则

### 7.1 必须先决策再生成

生成 HTML 前必须输出：

```text
CONTENT_ASSET_DECISION
```

内容包括：

```text
page_recipe
selected_regions
selected_modules
selected_states
selected_overlays
variants
unsupported_items
```

### 7.2 只读取命中资产

不得一次性读取所有 assets。

### 7.3 不允许自造布局结构

禁止：

- 自造 class
- 自造容器层级
- 自造区域顺序
- 自造 overlay 挂载位置

### 7.4 缺资产时的处理

只能：

```text
1. 使用最接近的通用资产
2. 标记 unsupported
3. 请求后续补充资产
```

不得现场硬编复杂布局。

---

## 8. 校验方向

校验脚本至少检查：

- 是否有 XFT_ROUTE
- 是否有 CONTENT_ASSET_DECISION
- 是否只使用登记过的 asset_id
- 是否引用存在的 html_path
- 是否使用未登记 class
- overlay 是否挂载在 overlay slot
- page_recipe 必选区域是否齐全
- forbidden_with 是否冲突
- required_with 是否缺失

---

## 9. 当前阶段结论

第一步只完成资产模型。下一步应进入素材盘点：

```text
图片素材 → 逐张归类 → 标记可转资产类型 → 输出素材盘点表
```

