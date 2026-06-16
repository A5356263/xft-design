---
name: xft-design
version: "6.2"
description: Generate enterprise admin web prototypes with a stable shell-to-block XFT flow.
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
    entry: examples/
  outputs:
    primary: examples/
  design_system:
    requires: true
    sections:
      - color
      - typography
      - layout
      - components
---

# XFT Design Skill

你是一个企业后台页面原型生成 agent。不要自由拼页面。必须走固定生成链，先判定范围和壳子，再选择 block / overlay，再填业务内容，最后输出带版本号的单文件到 `examples/`。

## Stable Flow

生成顺序固定为：

Route Decision
→ Output ROUTE_DECISION
→ 按 Conditional Reads 读取 Phase 2 必要资产
→ Copy Shell as template（原文复制，不得重写）
→ 在 shell 第一个 <style> 前插入 tokens.css 原文
→ 保留 shell <style> 原文
→ 在 shell <style> 后插入 components.css 原文
→ 替换 Shell Slots（PAGE_CONTENT_SLOT / CONTENT_SLOT / OVERLAY_SLOT）
→ 替换 Shell Chrome 可见占位文案
→ 如确有必要，追加页面级新增 CSS（作为第四个 <style>，只能追加）
→ 输出 examples/{slug}-{YYYY-MM-DD}-v<N>.html
→ 如环境支持，运行 scripts/check_skill_output.py；否则按 Final Check 自检

硬规则：

- 不得跳过 Route Decision
- 不得先写业务主体再补 shell
- 不得在未选择 shell 和 page block 前生成主体内容
- 不得输出多个 HTML 文件
- 不得在 validator PASS，或无脚本环境下完成 Final Check 自检前，声称完成

## Route Decision Record

进入 Phase 2 之前，必须先输出 ROUTE_DECISION。
没有 ROUTE_DECISION，不得读取 shell / page-block / overlay / tokens / components 等资产文件。

ROUTE_DECISION 只记录结果，不输出推理过程。
ROUTE_DECISION 只输出在对话 / 执行日志中，不得写入任何 HTML 文件或资产文件。
最终 HTML 只保留 XFT_ROUTE，且 XFT_ROUTE 必须紧跟 <!DOCTYPE html>。

格式：

```
<!-- ROUTE_DECISION
scope: Full Page | Page Overlay | Component State
page_type: HomePage | TablePage | CreatePage | DetailPage | EditPage | SettingsPage | LoginPage | ErrorPage | BlankPage | None
shell: admin-side-shell | blank-shell
page_block: ListPageBlock | DetailPageBlock | FormPageBlock | SettingsPageBlock | None
overlay_type: Modal | Drawer | ConfirmDialog | None
output: examples/{slug}-{YYYY-MM-DD}-v<N>.html
-->
```

Route Decision 阶段选择的是资产名称，不读取资产内容。

允许：根据 SKILL.md 的路由规则选择 shell / page_block / overlay_type 名称。
不得：在 ROUTE_DECISION 输出前读取 shell / page-block / overlay / tokens / components 文件内容。

ROUTE_DECISION 必须与最终 HTML 中的 XFT_ROUTE 保持一致。
如果 Phase 2 发现 block 不存在、slot 不匹配或路由不成立，必须回退并重新输出 ROUTE_DECISION，不得静默发明结构。

## Conditional Reads and Execution Protocol

不要在生成前一次性读取全部文件。必须先完成 Route Decision，再按当前路由读取最少必要资产。

无文件系统时，只能依据本文件中的最小规则执行，不得假装已读取外部文件。

### Phase 1：Route Decision 前

只依赖本 SKILL.md。

在读取任何 asset / reference / examples 文件之前，必须先完成：

- scope 判断
- page_type 判断
- shell 判断
- page_block / overlay 判断
- output path 确认（按文件命名规则生成版本号文件名）

Route Decision 完成前，不得读取：

- `examples/`
- `examples/archive/`
- `references/checklist.md`
- 与当前路由无关的 shell / block / overlay / reference 文件

### Phase 2：Route Decision 后，生成 HTML 前

所有最终输出都必须读取：

- `design-systems/tokens.css`
- `components.css`

按路由条件读取最少必要资产：

- Full Page / 后台业务页 → `assets/shells/admin-side-shell.html`
- LoginPage / ErrorPage / BlankPage / Component State / 独立 Overlay → `assets/shells/blank-shell.html`
- TablePage / CreatePage / EditPage / DetailPage / SettingsPage → `assets/page-blocks.html`
- Page Overlay → `assets/overlays.html`
- HomePage（无 HomePageBlock）→ `references/layouts.md`
- 组件选择有分歧时 → `references/component-selection.md`
- token 或组件细节不确定时 → `design-systems/USAGE.md` 或 `design-systems/DESIGN.md`

不得读取：

- `examples/archive/`
- 与当前路由无关的 shell / block / overlay
- `references/checklist.md`

Phase 2 是 Asset Assembly，只读取并装配 ROUTE_DECISION 已选中的资产，不重新判断或发明 page_type / shell / page_block。
如 Phase 2 发现 block 不存在、slot 不匹配或路由不成立，必须回退并重新输出 ROUTE_DECISION。

### Phase 3：最终验收

生成文件后，必须先运行：

```bash
python3 scripts/check_skill_output.py examples/<生成文件名>.html
```

只有在以下情况才读取 `references/checklist.md`：

- 用户要求人工复核
- 需要排查 Final Check / validator 未覆盖的问题

## Scope Routing

### Full Page

完整后台页面、首页、表格页、详情页、表单页、设置页、登录页、异常页、明确无导航页。

### Page Overlay

弹窗、抽屉、确认框。

### Component State

空状态、加载态、错误态、局部组件状态。

硬规则：

- 只涉及弹窗 / 抽屉 / 确认框的需求，不得扩写成完整页面
- 局部组件状态不得默认生成完整后台页面

## Page Type Routing

- 查询 / 筛选 / 列表 / 表格 / 批量操作 / 分页 → `TablePage`
- 新建 / 创建 / 提交 / 申请 / 发起流程 → `CreatePage`
- 查看 / 详情 / 审批详情 / 单据详情 → `DetailPage`
- 编辑 / 修改 / 维护 / 回填 → `EditPage`
- 系统配置 / 参数配置 / 权限配置 / 偏好设置 → `SettingsPage`
- 概览 / 指标 / 快捷入口 / 待办 / 趋势 → `HomePage`
- 登录 / 注册 / 找回密码 → `LoginPage`
- 403 / 404 / 500 / 异常 → `ErrorPage`
- 明确无导航页面 → `BlankPage`

## Shell Routing

- 后台业务 `Full Page` → `admin-side-shell`
- 登录页 / 异常页 / 明确无导航页 → `blank-shell`
- 独立 `Page Overlay` → `blank-shell`
- 后台页面内 `Page Overlay` → `admin-side-shell + OVERLAY_SLOT`
- `Component State` → `blank-shell`

## Page Blocks

`assets/page-blocks.html` 当前实际存在的 block 只有：

- `ListPageBlock`
- `DetailPageBlock`
- `FormPageBlock`
- `SettingsPageBlock`

路由规则：

- `TablePage` → `ListPageBlock`
- `CreatePage` → `FormPageBlock`
- `EditPage` → `FormPageBlock`
- `DetailPage` → `DetailPageBlock`
- `SettingsPage` → `SettingsPageBlock`
- `HomePage` → 不得发明 `HomePageBlock`；若无现成 block，使用 `references/layouts.md` 的首页结构要求生成，`page_block: None`

硬规则：

- page block 只能插入 `PAGE_CONTENT_SLOT` 或 `CONTENT_SLOT`
- page block 不得包含 `TopNav / SideNav / WebTabs / AppShell`

## Overlay Routing

- 短流程表单 / 信息补充 / 普通编辑 → `Modal`
- 右侧详情 / 复杂配置 / 保留列表上下文 → `Drawer`
- 删除 / 撤销 / 作废 / 提交 / 高风险确认 → `ConfirmDialog`

硬规则：

- overlay 必须挂到 `OVERLAY_SLOT`
- 页面内 overlay 必须挂载到顶层 `overlay-root`
- 不得把 overlay 写进 `page-content-container` 内

## Output Contract

- 最终 HTML 输出到 `examples/` 目录，文件名格式为 `{page-type-slug}-{YYYY-MM-DD}-v{N}.html`
- 最终 HTML 必须自包含
- 不得输出到 `/tmp`、`examples/archive/` 或 skill 包外部目录
- 最终 HTML 顶部必须保留 `XFT_ROUTE` 注释，位置应紧跟 `<!DOCTYPE html>` 之后
- 没有 `XFT_ROUTE`，不得输出最终 HTML

## 文件命名规则

格式：`{page-type-slug}-{YYYY-MM-DD}-v{N}.html`

`page_type` → slug 映射（来自 XFT_ROUTE）：

| page_type | slug |
|-----------|------|
| TablePage | table-page |
| CreatePage | create-page |
| DetailPage | detail-page |
| EditPage | edit-page |
| SettingsPage | settings-page |
| HomePage | home-page |
| LoginPage | login-page |
| ErrorPage | error-page |
| BlankPage | blank-page |
| None（Full Page） | page |

scope 为 `Page Overlay` 时，用 `overlay_type` 替代 `page_type` 作为 slug：

| overlay_type | slug |
|---|---|
| Modal | modal |
| Drawer | drawer |
| ConfirmDialog | confirm-dialog |

版本号 N：扫描 `examples/` 目录，找出当天同 slug 文件中最大版本号，+1 后作为本次版本号；不存在则从 v1 开始。

示例：
- 今天第一次生成表格页 → `examples/table-page-2026-06-16-v1.html`
- 今天第二次生成表格页 → `examples/table-page-2026-06-16-v2.html`
- 今天第一次生成提单页 → `examples/create-page-2026-06-16-v1.html`
- 今天第一次生成抽屉 → `examples/drawer-2026-06-16-v1.html`

`examples/archive/` 仅保存历史示例，不参与生成。
生成时不得读取、复制、引用 `examples/archive/` 下的任何文件。
不得从 archive 示例中继承 HTML 结构、CSS、业务字段、token、inline style 或页面布局。

## XFT_ROUTE

最终 HTML 顶部必须包含：

```html
<!-- XFT_ROUTE
scope: Full Page | Page Overlay | Component State
page_type: HomePage | TablePage | CreatePage | DetailPage | EditPage | SettingsPage | LoginPage | ErrorPage | BlankPage | None
overlay_type: Modal | Drawer | ConfirmDialog | None
shell: admin-side-shell | blank-shell
page_block: ListPageBlock | DetailPageBlock | FormPageBlock | SettingsPageBlock | None
token_source: design-systems/tokens.css
content_slot: PAGE_CONTENT_SLOT | CONTENT_SLOT | None
overlay_slot: OVERLAY_SLOT | None
-->
```

注意：

- `HomePageBlock` 当前不存在，`HomePage` 默认 `page_block: None`
- `SettingsPageBlock` 存在，可直接使用
- 只要 `XFT_ROUTE` 中合法记录了 slot 名，就不算 slot 残留

## Copy-as-template Execution Protocol

读取 shell 后，必须以 shell 文件的 HTML 原文作为 base string 进行字符串级操作。

不得根据记忆重写 shell HTML 或 CSS。
不得合并、整理、优化、改写 shell style。
不得修改 shell DOM、class、padding、margin、transition、shadow、radius、导航结构、micro-wrapper 或 page-content-container。

最终 HTML 的 style 块顺序必须是：

1. 第一个 `<style>`：`design-systems/tokens.css` 原文
2. 第二个 `<style>`：shell 原有 `<style>` 原文，一字不改
3. 第三个 `<style>`：`components.css` 原文
4. 第四个 `<style>`：页面级新增 CSS，仅允许追加

不得修改前三个 `<style>` 的内容。

允许且仅允许以下操作：

1. 在 shell 第一个 `<style>` 前插入 tokens.css 内容
2. 保留 shell 原有 `<style>` 块原文不变
3. 在 shell 原有 `<style>` 之后插入 components.css 内容
4. 将 `<!-- PAGE_CONTENT_SLOT -->` 或 `<!-- CONTENT_SLOT -->` 替换为选定 page block 内容
5. 将 `<!-- OVERLAY_SLOT -->` 替换为选定 overlay 内容；没有 overlay 时保持空 overlay root
6. 在第四个 `<style>` 中追加页面级新增 CSS
7. 替换 shell chrome 中的可见占位文案（见下节）

除此之外，shell 原文必须保持不变。

## Shell Chrome Text Replacement

Copy Shell 不等于所有文字都不替换。

必须保留（不得修改）：

- shell DOM 层级
- shell class
- shell CSS
- TopNav / SideNav / WebTabs / micro-wrapper / page-content-container 结构
- padding / margin / transition / shadow / radius 等样式值

必须替换 shell 中的可见占位文案：

- 产品名称（`产品名称`）
- 企业名称（`演示企业名称`）
- TopNav 当前模块文案
- SideNav 菜单文案与当前选中项
- WebTabs 中的 `页面标签`
- WebTabs 中的 `当前页面`
- checker 封锁的其他 shell 占位文案

示例：

- `页面标签` → 替换为当前页面所属模块或上级页签
- `当前页面` → 替换为当前生成页面名称
- `产品名称` / `演示企业名称` → 根据业务语境替换；无明确业务时使用中性占位名称
- SideNav 菜单项 → 替换为与当前页面匹配的后台菜单，并设置正确的选中态

不得借此机会修改 shell DOM 结构、class、CSS、layout、spacing、transition、shadow 或 radius。

## PageBlock and Overlay Usage

page block / overlay 片段必须以资产原文为基础。

不得重写：

- page block DOM 结构
- overlay DOM 结构
- class
- CSS
- section 顺序
- overlay 根结构

不得为了"统一风格""优化写法""减少冗余"而重写 page-blocks / overlays 的结构和 class。

## Component Contract

生成时优先使用 `assets/page-blocks.html` 与 `assets/overlays.html` 中已存在的 canonical class：

- `.btn / .btn-primary / .btn-secondary / .btn-text / .btn-danger`
- `.form-field / .field-label / .form-control / .select-control / .textarea-control`
- `.page-header / .page-header-main / .page-title / .page-description / .page-header-actions`
- `.filter-bar / .filter-actions`
- `.page-card / .table-toolbar / .table-toolbar-left / .table-toolbar-right / .data-table`
- `.status-tag / .status-success / .status-warning / .status-error / .status-info / .status-neutral`
- `.pagination / .pagination-actions / .page-btn`
- `.summary-card / .summary-item / .detail-section`
- `.settings-layout / .settings-anchor / .settings-anchor-item / .settings-section / .setting-item`
- `.overlay-mask / .overlay-mask-right / .overlay-header / .overlay-body / .overlay-footer / .modal / .drawer / .confirm-dialog`

不要再发明第二套按钮、状态标签、表单控件 class。旧 class 仅在兼容历史资产时可作为 alias，不应成为新生成页面的默认选择。

## Token And Self-contained Rules

- 最终 HTML 必须自包含
- 不得保留 `<link rel="stylesheet">`
- 不得保留 `../components.css`
- `tokens.css` 必须作为第一个 `<style>` 块注入
- `components.css` 的有效样式必须内联到最终 HTML
- 页面级新增 CSS 必须继续使用 token 变量

组件层禁止：

- 裸色值
- `rgba()` 直接写在 HTML 元素的 `style=""`
- 裸字号
- 裸间距
- 裸圆角
- 裸阴影

说明：

- `tokens.css` 内的裸值合法
- shell 基础 CSS 内若仍存在 `rgba()`，只可作为人工复核项，不自动视为 P0 失败

## Admin Full Page Hard Rules

后台业务页必须满足：

- `AppShell`
- `TopNav`
- `MainFrame`
- `SideNav`
- `WorkArea`
- `WebTabs`
- `PageContent`
- `micro-wrapper`
- `page-content-container`

标准结构：

```html
<section class="page-content">
  <div class="micro-wrapper">
    <div class="page-content-container">
      <!-- PAGE_CONTENT_SLOT -->
    </div>
  </div>
</section>
```

说明：

- `micro-wrapper` 默认保留
- `micro-wrapper` 是透明布局层，不属于 page block
- page block 必须插入 `page-content-container` 内
- 不得把 page block 插到 `micro-wrapper` 外层

禁止：

- `PageContent` 直接贴在 `TopNav` 下方
- 把 `WebTabs` 放进 `page-content-container`
- 在 page block 中重复生成 `TopNav / SideNav / WebTabs`
- 把页面内部 tab 当成 `WebTabs`

## Content Fill Rules

填充业务内容时，不允许：

- 复制 `examples/` 中的业务字段、示例数据、品牌信息、流程
- 用无语义 `div` 堆叠伪装真实组件
- 让导航文案、左侧选中态、多页签当前页互相不一致

## Final Check

最终输出必须满足以下验收标准。

如运行环境支持，必须运行：

```bash
python3 scripts/check_skill_output.py examples/<生成文件名>.html
```

validator FAIL 时，必须根据报错修正后重新运行 validator；不得默认读取 `references/checklist.md`。

如运行环境不支持脚本执行，必须按以下条目自检：

- XFT_ROUTE 存在且紧跟 `<!DOCTYPE html>`
- 最终 HTML 不得包含 ROUTE_DECISION；只保留 XFT_ROUTE
- 文件位于 `examples/` 根目录，命名符合 `{slug}-{YYYY-MM-DD}-v<N>.html`
- 不得输出到 `examples/archive/`
- 无外链 CSS，无 `../components.css`
- 第一个 `<style>` 为 tokens.css 原文
- 前三个 `<style>` 必须存在且顺序固定；第四个 `<style>` 仅在需要页面级补充样式时追加
- 无 slot 残留（PAGE_CONTENT_SLOT / CONTENT_SLOT / OVERLAY_SLOT）
- 无 shell 占位文案残留（页面标签 / 当前页面 等）
- 无 inline style 属性
- Full Page 结构完整（AppShell / TopNav / SideNav / WebTabs / page-content-container）
- 如有 overlay，必须正确挂在 `overlay-root` 内；无 overlay 时不得强行生成 `data-overlay`

只有在以下情况才读取 `references/checklist.md`：

- 用户要求人工复核
- 需要排查 Final Check / validator 未覆盖的问题
