# Component Selection Rules

本文件定义业务页面生成时的组件选择规则。生成页面时，必须先根据页面类型选择组件，再生成页面结构。

说明：
- `assets/shells/admin-side-shell.html` 提供完整页面基座和样式。
- `assets/page-blocks.html` 提供可复制的结构片段。
- `references/checklist.md` 提供最终验收门。
- 本文件负责决定“选什么”，不负责提供最终页面壳子。
- 本文件里的“组件”指页面框架组件与页面主体结构组件的选择关系，不等同于原子控件库。

本文件在完整生成链中的位置是：

```text
页面类型路由
→ 框架路由
→ 复制 shell seed
→ 先按 layouts 确定页面类型布局
→ 再按本文件选择页面主体结构片段
→ 最后进入 checklist 验收
```

## 选择原则

组件选择遵循以下优先级：

1. 先使用 `assets/shells/admin-side-shell.html` 或 `assets/shells/blank-shell.html` 提供页面基座。
2. 再选择页面框架组件。
3. 再选择页面类型组件。
4. 再选择内容组件。
5. 最后选择交互和反馈组件。

不得跳过页面框架直接生成业务内容。

不得跳过页面类型判断，直接从组件库随意拼装页面。

## 页面框架组件

所有后台业务页面默认使用以下组件组合：

| 组件 | 用途 | 必须性 |
|---|---|---|
| `AppShell` | 后台系统整体框架 | 必须 |
| `TopNav` | 顶部系统级导航 | 必须 |
| `MainFrame` | 顶部导航下方主工作区 | 必须 |
| `SideNav` | 左侧模块和页面导航 | 必须 |
| `WorkArea` | 右侧工作区 | 必须 |
| `WebTabs` | 页面打开多页签 | 必须 |
| `PageContent` | 当前业务页面内容区 | 必须 |

标准组合：

```html
<AppShell>
  <TopNav />
  <MainFrame>
    <SideNav />
    <WorkArea>
      <WebTabs />
      <PageContent />
    </WorkArea>
  </MainFrame>
</AppShell>
```

禁止省略 `WebTabs`。禁止将 `PageContent` 直接放到 `TopNav` 下方。

## TopNav 选择规则

### 何时使用

所有后台业务页面必须使用 `TopNav`。

### 用途

`TopNav` 用于系统级导航和全局能力。

### 应包含

- 系统名称
- 一级模块入口
- 全局搜索
- 消息
- 帮助
- 用户信息

### 不应包含

- 表格筛选条件
- 表单提交按钮
- 详情页编辑按钮
- 页面局部切换
- 页面级业务 Tab

## SideNav 选择规则

### 何时使用

后台业务页面默认使用 `SideNav`。

### 用途

`SideNav` 用于承载模块级、页面级导航。

### 必须规则

左侧导航仅有一级导航和二级导航，不存在三级导航。

一级导航必须展示：

```text
描边 icon + 导航文案
```

一级导航 icon 必须为线性描边样式，使用 `fill="none"` 和 `stroke="currentColor"` 的 SVG。

二级导航仅展示文案，不展示 icon：

```text
导航文案
```

正确结构（一级导航）：

```html
<div class="side-nav-item level-1 is-expanded">
  <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
    ...
  </svg>
  <span class="nav-label">业务管理</span>
  <svg class="nav-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
    <path d="M6 9l6 6 6-6"/>
  </svg>
</div>
```

正确结构（二级导航，仅文案）：

```html
<div class="side-nav-item level-2 is-active">
  <span class="nav-label">订单管理</span>
</div>
```

禁止结构（二级导航展示 icon）：

```html
<div class="side-nav-item level-2">
  <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
    ...
  </svg>
  <span class="nav-label">订单管理</span>
</div>
```

禁止结构（使用三级导航）：

```html
<div class="side-nav-item level-3">
  <span class="nav-label">报销单管理</span>
</div>
```

### 菜单层级选择

| 场景 | 推荐 |
|---|---|
| 只有模块和页面 | 一级（icon+文案）+ 二级（仅文案） |
| 菜单文案较长 | 固定宽度 + 省略号 |
| 菜单需要强调 | 使用推荐、NEW、AI 标签 |
| 当前页面 | 左侧导航对应项选中 |

左侧导航最多只有两级，不存在三级导航。

## WebTabs 选择规则

### 何时使用

所有后台业务页面必须使用 `WebTabs`。

### 用途

`WebTabs` 用于展示已打开页面，支持页面之间切换。

### 不适用

`WebTabs` 不用于：

- 表单分组
- 详情页分区
- 筛选条件切换
- 卡片内容切换
- 设置页分组切换

这些场景应使用内容区内的普通业务 Tab 或分组组件，但不能替代 `WebTabs`。

### 必须结构

多页签必须包含：

- 首页或固定页签
- 当前选中页签
- 其他打开页签
- 关闭图标
- 上一页按钮
- 下一页按钮
- 更多按钮

### 状态规则

当前页面在 `WebTabs` 中必须高亮。

页签文字过长时必须省略。

页签过多时必须使用更多菜单，不允许换行。

## PageContent 选择规则

### 何时使用

所有业务页面主体必须放入 `PageContent`。

### 用途

`PageContent` 是当前业务页面的唯一主体容器。页面内容区必须有一个大背景容器 `#ffffff`（白色），所有页面内容（页面标题、筛选区、表格、表单、详情等）必须在此白色容器中展示，不允许有任何内容裸露在白色容器之外。

### 禁止

禁止在 `PageContent` 内重复生成：

- `TopNav`
- `SideNav`
- `WebTabs`

禁止页面内容裸露在白色背景容器之外。

## 页面类型组件选择

### 首页

首页用于业务概览。

推荐组件：

| 组件 | 用途 |
|---|---|
| `PageHeader` | 首页标题和说明 |
| `OverviewCards` | 核心指标 |
| `QuickAccess` | 快捷入口 |
| `TodoList` | 待办事项 |
| `ChartPanel` | 趋势或分布 |
| `RecentList` | 最近访问或最近记录 |

首页禁用：

- 不要默认生成大表格作为唯一内容。
- 不要省略快捷入口。
- 不要把首页做成纯欢迎页。

### 表格页

表格页用于数据查询和管理。

推荐组件：

| 组件 | 用途 |
|---|---|
| `PageHeader` | 页面标题、说明、主操作 |
| `FilterBar` | 查询条件 |
| `TableToolbar` | 批量操作、导出、列设置 |
| `DataTable` | 数据表格 |
| `Pagination` | 分页 |
| `EmptyState` | 空数据状态 |

表格类型选择：

| 场景 | 推荐组件 |
|---|---|
| 普通只读列表 | `DataTable` |
| 单元格编辑 | `DataTable editable="cell"` |
| 整行编辑 | `DataTable editable="row"` |
| 批量录入 | `EditableGrid` |
| 父子层级数据 | `NestedTable` 或 `DataTable expandable` |
| 大数据量 | `DataTable virtual` |

表格页禁用：

- 禁止用普通卡片堆叠替代 DataTable，除非用户明确要求卡片列表。
- 禁止把查询条件放进 TopNav。
- 禁止省略分页，除非数据明确少于一页。
- 禁止没有主操作或工具栏的管理页。

### 提单页

提单页用于创建新单据、提交申请、发起流程。

推荐组件：

| 组件 | 用途 |
|---|---|
| `PageHeader` | 页面标题、说明 |
| `FormPage` | 表单页面容器 |
| `FormSection` | 表单分组 |
| `FormField` | 表单字段 |
| `AttachmentArea` | 附件上传 |
| `ActionBar` | 提交、取消、暂存 |

表单布局选择：

| 场景 | 推荐 |
|---|---|
| 字段少于等于 8 个 | 基础表单 |
| 字段较少且字段短 | 左右表单 |
| 字段较多或存在语义分组 | 分组表单 |
| 存在明确流程步骤 | 分步表单 |
| 轻量新建，字段少于等于 5 个 | Modal 表单 |
| 需要保留列表上下文 | Drawer 表单 |
| 字段超过 8 个 | 独立提单页 |

提单页禁用：

- 禁止字段超过 10 个仍使用无分组单列表单。
- 禁止提交按钮离开表单上下文。
- 禁止在 Modal 中放复杂长表单。
- 禁止缺少取消或返回操作。

### 详情页

详情页用于展示只读信息。

推荐组件：

| 组件 | 用途 |
|---|---|
| `PageHeader` | 标题、状态、操作 |
| `StatusSummary` | 状态摘要 |
| `DetailLayout` | 详情布局 |
| `DescriptionList` | 字段描述 |
| `RelatedTable` | 关联数据 |
| `Timeline` | 操作记录或流程记录 |
| `ActionBar` | 编辑、返回、审批等操作 |

详情布局选择：

| 场景 | 推荐 |
|---|---|
| 字段少于等于 8 个 | 单列详情 |
| 字段 9 到 20 个 | 双列详情 |
| 字段较多且有语义分组 | 分组详情 |
| 包含关联数据 | 详情 + 关联表格 |
| 包含流程记录 | 详情 + 时间线 |
| 内容较少且从列表打开 | Drawer 详情 |
| 内容复杂 | 独立详情页 |

详情页禁用：

- 禁止默认让所有字段可编辑。
- 禁止没有状态信息。
- 禁止关联数据直接散落，不使用表格或分组。
- 禁止详情页没有返回或主要操作。

### 编辑页

编辑页用于修改已有数据。

推荐组件：

| 组件 | 用途 |
|---|---|
| `PageHeader` | 页面标题、说明 |
| `FormPage` | 编辑表单容器 |
| `FormSection` | 表单分组 |
| `FormField` | 字段 |
| `ActionBar` | 保存、取消 |

编辑页选择规则：

| 场景 | 推荐 |
|---|---|
| 字段少于等于 8 个 | 基础编辑表单 |
| 字段超过 10 个 | 分组编辑表单 |
| 存在步骤 | 分步编辑表单 |
| 从详情页局部编辑 | Drawer 编辑 |
| 少量字段快速编辑 | Modal 编辑 |

编辑页禁用：

- 禁止与提单页完全相同但没有回填状态。
- 禁止没有保存和取消。
- 禁止把编辑操作放到 TopNav。

### 设置页

设置页用于系统配置、业务参数、偏好设置。

推荐组件：

| 组件 | 用途 |
|---|---|
| `PageHeader` | 设置页标题 |
| `SettingsLayout` | 设置页布局 |
| `SettingsAnchor` | 左侧设置锚点 |
| `SettingsSection` | 设置分组 |
| `SettingItem` | 设置项 |
| `Switch` | 开关 |
| `RadioGroup` | 单选配置 |
| `Select` | 下拉配置 |
| `Button` | 配置操作 |

设置页布局选择：

| 场景 | 推荐 |
|---|---|
| 设置分组少于 3 个 | 单列设置分组 |
| 设置分组多于等于 3 个 | 左侧锚点 + 右侧设置分组 |
| 设置项需要说明 | SettingItem 标题 + 描述 + 控件 |
| 设置项立即生效 | Switch / Select / Radio |
| 设置项需二次配置 | Button 打开 Drawer 或独立配置页 |

设置页禁用：

- 禁止默认使用 DataTable 作为设置页主体。
- 禁止只展示控件而没有说明。
- 禁止设置项没有分组。
- 禁止把设置分组做成 WebTabs。

## 业务 Tab 与 WebTabs 的区别

| 类型 | 位置 | 用途 |
|---|---|---|
| `WebTabs` | 顶部导航下方、页面内容上方 | 已打开页面切换 |
| `ContentTabs` | PageContent 内部 | 当前页面内部内容分区 |
| `Segmented` | PageContent 内部 | 小范围视图切换 |
| `Steps` | PageContent 内部 | 流程步骤 |

禁止用 `ContentTabs`、`Segmented`、`Steps` 替代 `WebTabs`。

禁止用 `WebTabs` 做页面内部内容分区。

## 图标选择规则

一级导航中的 icon 必须为描边风格。二级导航不展示 icon。

推荐 SVG 属性：

```html
<svg
  class="nav-icon"
  viewBox="0 0 24 24"
  fill="none"
  stroke="currentColor"
  stroke-width="1.8"
  stroke-linecap="round"
  stroke-linejoin="round"
>
</svg>
```

禁止：

- 使用 emoji 作为导航 icon。
- 使用实心图标作为一级导航 icon。
- 二级导航展示 icon。
- icon 与文字垂直不对齐。
- 当前导航选中后 icon 颜色不变化。

## 按钮选择规则

按钮应按操作重要性选择：

| 场景 | 推荐 |
|---|---|
| 页面主操作 | Primary Button |
| 次要操作 | Default Button |
| 危险操作 | Danger Button |
| 表格行操作 | Link Button |
| 批量操作 | Default Button 或 Primary Button |

页面主操作通常位于 `PageHeader` 右侧或 `ActionBar` 中。

表单提交操作必须在表单上下文中，不应放到顶部导航。

## 筛选区选择规则

筛选区只用于表格页和部分数据分析页。

字段少于等于 4 个时，单行展示。

字段超过 4 个时，支持展开收起。

筛选区操作必须包含查询和重置。

复杂筛选可提供更多筛选或高级筛选。

## 表单字段选择规则

表单字段必须包含 label。

必填字段必须有明显标识。

字段需要说明时，使用帮助文案。

字段需要分组时，使用 `FormSection`。

禁止大量字段无分组平铺。

## 验收说明

本文件只负责“选什么”，不再单独维护 P0 gate 列表。

最终验收统一以 `references/checklist.md` 为准：

- 页面类型和组件选择是否匹配
- 表格页 / 表单页 / 详情页 / 设置页是否用对主体结构
- `WebTabs`、`PageContent`、左侧导航层级是否正确

## Overlay 相关组件选择规则

### Modal

适用于：

- 短流程表单；
- 信息补充；
- 普通编辑。

不适用于复杂长表单或需要保留大量列表上下文的场景。

### Drawer

适用于：

- 右侧详情；
- 复杂配置；
- 与列表强关联的查看 / 编辑。

适合需要保留宿主列表或详情上下文的场景。

### ConfirmDialog

适用于：

- 删除；
- 撤销；
- 作废；
- 提交等高风险二次确认。

危险操作优先使用 `btn-danger + ConfirmDialog`，不要只给普通主按钮。
