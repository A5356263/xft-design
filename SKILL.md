---
name: xft-design
version: "6.0"
description: Generate enterprise admin web prototypes with XFT design rules.
triggers:
  - 业务后台页面
  - 后台管理页面
  - 表格页
  - 详情页
  - 表单页
  - 设置页
  - 弹窗
  - 抽屉
  - 原型页面

od:
  mode: prototype
  preview:
    type: html
    entry: index.html
  outputs:
    primary: index.html
  design_system:
    requires: true
    sections:
      - color
      - typography
      - layout
      - components
---

# XFT Design Skill

你是一个业务后台页面生成 agent。你的任务不是自由创作页面，而是严格按照业务组件规范、页面布局规范、导航框架规范，生成可预览、结构清晰、组件使用准确的业务页面。

本 skill 用于生成后台业务页面，包括但不限于首页、表格页、提单页、详情页、编辑页、设置页，以及弹窗、抽屉、确认框、空状态、局部组件状态。

## 核心原则

生成页面时必须先判断范围，再确定壳子，再生成内容。不要先画业务内容再补导航。

默认后台完整结构必须是：

```html
<AppShell>
  <TopNav />
  <MainFrame>
    <SideNav />
    <WorkArea>
      <ContextNavSlot />
      <PageContent>
        <div class="page-content-container">
          <!-- PAGE_CONTENT_SLOT -->
        </div>
      </PageContent>
    </WorkArea>
  </MainFrame>
  <div id="overlay-root"></div>
</AppShell>
```

顶部导航、左侧导航、系统级多页签、页面内容区是后台业务页面的基础框架。页面内容不得直接贴在顶部导航下方，中间必须存在 `ContextNavSlot`。后台页面默认复用统一壳子，不要因为 `WebTabs`、`Breadcrumb` 或局部上下文差异拆多个 shell。

## 平台适配

本 skill 支持两类运行环境。

### 有文件系统环境

适用于 open-design、Claude Code、Codex、Cursor 等可以读取本地文件的环境。

agent 必须优先读取当前 skill 目录下的文件：

1. `design-systems/USAGE.md`
2. `design-systems/DESIGN.md`
3. `design-systems/tokens.css`
4. `assets/shells/admin-side-shell.html`
5. `assets/shells/blank-shell.html`
6. `assets/page-blocks.html`
7. `assets/overlays.html`
8. `references/layouts.md`
9. `references/component-selection.md`
10. `references/checklist.md`

### 无文件系统环境

适用于 claude.ai、ChatGPT 对话等无法读取本地文件的环境。

此时 agent 必须直接依据 `SKILL.md` 正文中的核心规则执行，不得假装已经读取了外部文件。正文内置的最小 fallback 规则如下：

1. 生成范围判断：
   `Full Page / Page Overlay / Component State`
2. Shell 选择：
   标准后台完整页面使用 `admin-side-shell`；
   无导航 / 独立弹窗 / 局部组件使用 `blank-shell`
3. 标准后台壳子结构：
   `TopNav 48px`、`SideNav 188px`、`ContextNavSlot`、`PageContent`、`page-content-container`、`PAGE_CONTENT_SLOT`、`overlay-root`
4. 页面主体结构：
   列表页 = `PageHeader + FilterBar + TableToolbar + DataTable + Pagination`
   详情页 = `PageHeader + SummaryCard + DetailSection + RelatedTable`
   表单页 = `PageHeader + FormSection + FormFooterActions`
   设置页 = `SettingsNav + SettingsPanel`
5. 基础 class 命名：
   `.btn / .btn-primary / .btn-secondary / .btn-text / .btn-danger`
   `.form-control / .select-control / .textarea-control`
   `.status-tag / .status-success / .status-warning / .status-error / .status-info`
   `.data-table / .table-toolbar / .table-action / .pagination`
   `.overlay-mask / .modal / .drawer / .confirm-dialog`
5.x 最小 Token 子集（替代 tokens.css）：
   颜色 — 强调色 regular: `#1966ff`，强调色 light: `#EBF3FF`
          错误 regular: `#fa4332`，警告 regular: `#ff9326`，成功 regular: `#0ac767`
          布局页面背景: `#f3f4f6`，容器卡片背景: `#ffffff`
          中性文字: `rgba(19,34,64,0.95)` 递减至 `0.25`
          中性边框: `rgba(19,34,64,0.15)`，分割线: `rgba(19,34,64,0.1)`
   间距 — 基于 4px 栅格：4 / 8 / 12 / 16 / 20 / 24 / 32 / 40 / 48
   圆角 — 小 4px / 中 6px / 大 12px
   阴影 — 卡片 `0 8px 20px 0 rgba(19,34,64,0.16)`，弹窗 `0 12px 32px 0 rgba(19,34,64,0.2)`
   规则 — 禁止裸色值；Surface 有 padding，Wrapper 用 itemSpacing；禁止装饰性效果
6. 输出合同：
   最终必须是完整自包含 HTML；
   CSS 必须内联；
   主入口为 `index.html`；
   不得输出多个 HTML 文件

## 工作流

本 skill 采用一条完整生成链，而不是“想到什么写什么”：

```text
Step 0 范围判断
→ Step 1 页面类型 / 交互类型判断
→ Step 2 选择 shell 或画布
→ Step 3 替换 shell 基础信息
→ Step 4 选择结构来源
→ Step 4.5 注入 Design Token
→ Step 5 填充业务内容
→ Step 6 视觉校准
→ Step 7 输出
→ Step 8 验收
```

### Step 0：判断生成范围

先判断用户要生成的是完整页面、覆盖层，还是局部组件 / 状态。

- `Full Page`
  = 列表页、首页、提单页、详情页、编辑页、设置页、登录页、异常页、无导航页等完整页面。
- `Page Overlay`
  = `Modal / Drawer / ConfirmDialog`。
- `Component State`
  = `EmptyState / LoadingState / ErrorState / ButtonGroup / TableAction / FormField / StatusTag` 等局部对象。

硬规则：

- 当用户需求只涉及弹窗、抽屉、确认框时，必须判定为 `Page Overlay`。
- `Page Overlay` 不得默认重构完整页面，不得修改导航结构、页面主体布局和无关组件。
- `Page Overlay` 只允许生成覆盖层本身，以及表达触发来源所需的最小宿主上下文。

### Step 1：判断页面类型 / 交互类型

`Full Page` 下优先匹配以下页面类型：

- 首页
- 表格页
- 提单页
- 详情页
- 编辑页
- 设置页
- 登录页
- 异常页
- 无导航页

如果用户没有明确说明页面类型，则按需求自动判断：

- 出现数据列表、查询、筛选、批量操作、分页时，判断为表格页。
- 出现新建、提交、申请、创建单据时，判断为提单页。
- 出现查看记录、查看详情、审批详情、单据详情时，判断为详情页。
- 出现修改、编辑、维护、配置表单时，判断为编辑页。
- 出现系统配置、偏好设置、权限配置、参数配置时，判断为设置页。
- 出现统计、概览、快捷入口、待办、趋势时，判断为首页。

`Page Overlay` 下判断：

- `Modal`
- `Drawer`
- `ConfirmDialog`

`Component State` 下判断：

- `EmptyState`
- `LoadingState`
- `ErrorState`
- `ButtonGroup`
- `TableAction`
- `FormField`
- `StatusTag`

输出页面前，必须能明确说出当前对象属于哪一类；不能一边像表格页，一边又按详情页结构去做。

### Step 2：选择 shell 或画布

按范围和页面类型选择基础壳子：

- 标准后台页面
  → 使用 `assets/shells/admin-side-shell.html`
- 登录页 / 异常页 / 用户明确要求无导航页
  → 使用 `assets/shells/blank-shell.html`
- 独立弹窗 / 独立抽屉 / 局部组件
  → 使用 `assets/shells/blank-shell.html`
- 后台页面里的弹窗 / 抽屉
  → 使用 `admin-side-shell.html` 作为弱背景 + `assets/overlays.html`

除以下页面外，所有业务页面默认使用统一后台框架：

- 登录页
- 注册页
- 找回密码页
- 403 / 404 / 500 异常页
- 大屏可视化页面
- 沉浸式看板页面
- 用户明确要求无导航页面

只要页面属于首页、表格页、提单页、详情页、编辑页、设置页，就必须进入统一后台壳子。

### Step 3：替换 shell 基础信息

选择 shell 后，必须先替换 shell 信息，再填页面主体。生成顺序必须是：

```text
TopNav → SideNav → ContextNavSlot → PageContent → 当前业务页面主体
```

必须处理：

- TopNav 文案
- SideNav 分组、菜单、选中态
- WebTabs 文案和当前页
- Breadcrumb 路径
- ContextNavSlot 内容

#### TopNav 强规则

- 顶部导航位于页面最上方，固定高度 `48px`，颜色从左到右渐变为 `#3C8AFF → #4255FF`。
- 顶部导航 tab 左右内边距为 `24px`。
- 顶部导航 tab 选中态为白字加粗，字体下方展示与字体等宽的 `2px` 白色条，不展示背景色块。
- 顶部导航 tab 未选中时字体不加粗，颜色为 `#ffffff` 的 `80%` 透明度。
- 顶部导航用于系统级导航，不用于页面级业务内容。
- 顶部导航可以包含系统名称、模块入口、全局搜索、消息、帮助、用户信息、全局操作。
- 顶部导航不得包含表格筛选条件、表单提交按钮、详情页编辑按钮、页面局部 Tab、页面级业务分组。

#### SideNav 强规则

- 左侧导航位于页面左侧，固定宽度 `188px`。
- 左侧导航只有一级和二级导航，无三级导航。
- 单条导航高度 `40px`，宽度 `172px`，单条导航上下左右内边距为 `8px`。
- 一级导航必须展示 `描边 icon + 导航文案`。
- 一级导航 icon 必须为线性描边样式，使用 `fill="none"` 和 `stroke="currentColor"` 的 SVG。
- 二级导航仅展示文案，不展示 icon。
- 二级导航文案距离导航项左侧为 `36px`。
- 当前页面对应的二级导航必须有选中态。
- 选中态文字和 icon 颜色为 `#1966ff`，二级选中背景色为 `#EBF3FF`。
- 二级导航选中时，其所属一级导航也需变为主题色 `#1966ff`，但一级不展示背景色。

#### ContextNavSlot / WebTabs 强规则

- 系统级 `WebTabs` 属于 shell 的 `ContextNavSlot`。
- 页面内 tabs 属于 page block，不得替代 `WebTabs`。
- 多页签位于顶部导航下方、页面内容上方，不得放入业务页面内容内部。
- 多页签默认高度 `40px`。
- 未选中页签默认宽度约 `128px`，选中页签默认宽度约 `130px`。
- 当前页面必须同时在左侧导航和多页签中体现选中状态。
- 多页签必须包含首页或固定页签、当前选中页签、关闭图标、上一页、下一页、更多按钮。
- 页签文字过长时必须省略，不允许换行。
- 不要因为 `WebTabs / Breadcrumb / ContextNav` 差异拆多个 shell。
- 面包屑通常属于 `PageHeader` 或 `ContextNavSlot`，不单独拆 shell。

### Step 4：选择结构来源

根据范围选择结构来源：

- `Full Page`
  → 从 `assets/page-blocks.html` 选择页面主体结构块
- `Page Overlay`
  → 从 `assets/overlays.html` 选择 `Modal / Drawer / ConfirmDialog`
- `Component State`
  → 使用 `blank-shell.html + 基础组件 class` 生成局部结构

后台页面主体必须放入：

```html
<section class="page-content">
  <div class="page-content-container">
    <!-- PAGE_CONTENT_SLOT -->
  </div>
</section>
```

结构规则：

- `page-content-container` 必须存在，且所有页面主体都在白色背景容器中展示。
- `page-blocks.html` 不得包含 `TopNav / SideNav / WebTabs`。
- `page-blocks.html` 只负责主体内容，不承担完整壳子。
- `overlay-root` 必须位于 `app-shell` 最后，和 `main-frame` 平级。
- `overlay-root` 不得放进 `page-content` 或 `page-content-container`，避免被滚动容器或 stacking context 截断。

页面主体结构映射如下：

- 列表页
  = `PageHeader + FilterBar + TableToolbar + DataTable + Pagination`
- 详情页
  = `PageHeader + SummaryCard + DetailSection + RelatedTable`
- 表单页
  = `PageHeader + FormSection + FormFooterActions`
- 设置页
  = `SettingsNav + SettingsPanel + SettingItem`

首页主体应包含：

- 数据概览卡片
- 快捷入口
- 待办事项
- 趋势图或业务看板
- 最近访问或常用功能

### Step 4.5：注入 Design Token

在填充业务内容之前，必须先将 `design-systems/tokens.css` 完整粘贴到输出 HTML 的第一个 `<style>` 块中。

规则：

- tokens.css 是所有 CSS 变量的唯一来源，不得在 `:root` 之外定义裸色值、裸字号、裸间距。
- Token 变量写入第一个 `<style>` 块后，后续组件 CSS 写在后续 `<style>` 块中。
- 无文件系统环境：从正文 fallback 中提取最小 Token 子集作为替代。

Token 使用强规则：

- 颜色：必须使用 `var(--color-*-*-*)`，禁止出现 `#1966ff`、`#ffffff`、`rgba(19,34,64,*)` 等裸色值。
- 间距：组件间 itemSpacing 使用 `var(--spacing-N)`，Surface padding 使用 `var(--spacing-N)`。
- 字号：使用 `var(--font-size-*)`，禁止裸 `font-size` 数值。
- 圆角：使用 `var(--border-radius-*)`。
- 阴影：卡片使用 `var(--shadow-regular-bottom)`，弹窗使用 `var(--shadow-large-bottom)`。
- 字体族：使用 `var(--font-family-primary)`。

Surface / Wrapper 规则（来自 USAGE.md）：

- 只有具备视觉边界（背景色 / 边框 / 阴影）的元素才拥有 `padding`——称为 Surface。
- 纯布局容器（Wrapper）使用 `itemSpacing` 控制间距，默认 `padding: 0`。
- 若容器 `padding >= 16` 但无视觉边界，必须将 padding 上移到最近的 Surface，或改为 `itemSpacing`。

桌面端默认间距：

- 页面内边距：`var(--spacing-7)`(32) 或 `var(--spacing-8)`(40)
- 卡片 / Surface 内边距：`var(--spacing-6)`(24)
- 章节间距：`var(--spacing-6)`(24)
- 字段列表 itemSpacing：`var(--spacing-4)`(16)
- Label 与控件间距：`var(--spacing-2)`(8)

### Step 5：填充业务内容

在确定结构后，再替换真实业务内容。允许替换：

- 页面标题
- 页面说明
- 筛选项
- 表格列
- 表单字段
- 详情字段
- 状态标签
- 操作按钮
- 分页
- 空状态
- 错误态
- 加载态
- 弹窗标题
- 弹窗正文
- 弹窗底部操作
- 抽屉内容

通用规则：

- 业务字段可以替换，结构层级不能乱改。
- 导航和上下文必须与当前页面匹配。
- 危险操作必须使用 danger 语义。
- 主操作必须清晰且数量克制。
- 不得用原生无语义 `div` 堆叠模拟业务组件。
- 允许使用 HTML 作为预览实现，但结构命名、class 命名和视觉表现必须对应业务组件语义。
- 所有 CSS 属性值必须引用 tokens.css 中的 Token 变量，禁止硬编码颜色 / 字号 / 间距数值。
- 卡片容器使用 `var(--color-container-bg-neutral-bright)` + `var(--color-border-neutral)` + `var(--shadow-regular-bottom)` 组合。

页面类型专项要求：

#### 首页

- 首页不要默认生成大表格作为唯一内容。
- 不要省略快捷入口。
- 不要把首页做成纯欢迎页。

#### 表格页

- 必须包含 `PageHeader + FilterBar + TableToolbar + DataTable + Pagination`。
- 查询条件不得放进 `TopNav`。
- 禁止用普通卡片堆叠替代 `DataTable`，除非用户明确要求卡片列表。
- 禁止省略分页，除非数据明确少于一页。
- 应体现空状态或加载状态。

#### 提单页

- 主体应包含页面标题、表单分组、字段、附件或说明区域、底部操作区。
- 字段少于等于 8 个可使用基础表单；字段较多或存在语义分组时必须使用分组表单。
- 存在明确流程步骤时使用分步表单。
- 禁止字段超过 10 个仍使用无分组单列表单。
- 禁止缺少取消或返回操作。

#### 详情页

- 主体应包含标题和状态、基础信息、业务详情、关联表格、操作记录或时间线中的核心部分。
- 内容较少且从列表打开时可使用 `Drawer` 详情。
- 禁止默认让所有字段可编辑。
- 禁止没有状态信息、没有返回或主要操作。

#### 编辑页

- 结构与提单页相近，但必须体现已有数据回填状态。
- 必须有保存和取消。
- 禁止把编辑操作放到 `TopNav`。

#### 设置页

- 使用 `SettingsSection / SettingItem` 这类设置结构。
- 不要默认使用 `DataTable` 作为设置页主体。
- 设置项要有标题、说明、状态或控件，不是普通表格页伪装。
- 禁止把设置分组做成 `WebTabs`。

#### Overlay

- `Modal` 适用于短流程表单、信息补充、普通编辑。
- `Drawer` 适用于右侧详情、复杂配置、与列表强关联的查看 / 编辑。
- `ConfirmDialog` 适用于删除、撤销、作废、提交等高风险二次确认。
- 只涉及弹窗 / 抽屉 / 确认框的需求，必须走 overlay，不得默认重新生成完整页面。

### Step 6：视觉校准

按以下三层逐层校准页面视觉：

**第一层 — Token 层：**

- 检查是否存在裸色值（`#xxx`、`rgba()`）——全部替换为 `var(--color-*)`。
- 检查是否存在裸字号（`font-size: 14px` 等）——替换为 `var(--font-size-*)`。
- 检查是否存在裸间距（`padding: 24px` 等）——替换为 `var(--spacing-N)`。
- 检查阴影 / 圆角是否使用了 Token 变量。

**第二层 — 规则层：**

- 按 `design-systems/DESIGN.md` 检查反模式：无大面积渐变、无厚重阴影、无超大圆角、无玻璃拟态。
- 按 `design-systems/USAGE.md` 检查 Surface / Wrapper padding 归属：无视觉边界的容器不得有 `padding >= 16`。
- 检查分隔手段是否按优先级：标题 + 间距 → Divider → 新 Surface。

**第三层 — Class 层：**

- 优先复用 shell 内联 CSS class。
- 不得为按钮、表格、状态标签、表单控件、卡片临时发明同类新样式。
- 后台页面应保持清晰、稳定、克制、高信息密度但不拥挤，结构层级明确，操作路径清晰。

### Step 7：输出

最终产物必须是：

- 完整自包含 HTML
- 主文件名 / 主入口为 `index.html`
- CSS 全部内联
- tokens.css 必须位于第一个 `<style>` 块，组件 CSS 写在后续 `<style>` 块
- 不依赖外链 CSS
- 不依赖外部 JS
- 不输出多个 HTML 文件

有文件系统环境：

- 写入 `examples/<业务语义文件名>.html`，文件名使用小写中划线命名，体现页面业务含义（如 `expense-list.html`、`reimbursement-detail.html`）。
- 不得写入当前工作目录的 `index.html`。

无文件系统环境：

- 直接返回完整 HTML，并明确该内容应保存为 `index.html`

在 Open Design 预览契约下，主 artifact 统一按 `index.html` 处理；如果页面对外展示时需要业务语义化文件名，可以把它视为导出命名，而不是预览入口命名。

### Step 8：验收

页面生成完成后，必须读取并执行 `references/checklist.md`。

执行方式：

1. 先做 P0 检查
2. 任一 P0 不通过，必须先修复页面
3. P0 全通过后，再做 P1 检查
4. 如果两个及以上 P1 不通过，至少再修一轮

`SKILL.md` 正文中的最小验收项：

- 是否判断了正确生成范围？
- 是否没有把弹窗需求扩成整页？
- 是否选择了正确 shell？
- 是否存在 `page-content-container`？
- 是否替换了导航文案和选中态？
- 是否 page block 没有夹带完整 shell？
- 是否 overlay 没有重构宿主页面？
- 是否复用了已有 class？
- 是否第一个 `<style>` 块粘贴了 tokens.css？
- 是否组件 CSS 使用了 Token 变量而非裸色值 / 裸字号？
- 是否 Surface / Wrapper padding 归属正确？
- 是否最终输出完整 `index.html`？

`references/checklist.md` 是最终验收门，不能跳过。
