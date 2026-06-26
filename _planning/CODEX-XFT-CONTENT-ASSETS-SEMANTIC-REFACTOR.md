# XFT Content Assets 语义重整与完整 HTML 资产补强执行文档

> 适用仓库：`A5356263/xft-design`  
> 适用分支：`zhangfeng`  
> 适用 Skill（技能）：`.claude/skills/xft-design`  
> 执行对象：Codex（代码助手）/ AI Code（AI 代码执行工具）  
> 文档性质：正式执行文档，不是讨论稿  
> 本次范围：只处理 `content-assets` 内容资产语义重整与 HTML（超文本标记语言）完整性补强

---

## 1. 背景

当前 `xft-design` Skill（技能）已经完成以下能力：

1. 通过 `ROUTE_DECISION`（路由决策）判断页面范围、页面类型、页面配方。
2. 通过 `search_content_assets.py` 执行内容资产检索。
3. 通过 `CONTENT_ASSET_DECISION`（内容资产决策）确定实际读取的 HTML（超文本标记语言）资产。
4. 根据 `read_order`（读取顺序）读取命中资产并装配页面。
5. 真实页面验证已经证明结构链路可用。

当前仍需优化的问题不是检索架构，而是内容资产层：

1. `regions`（区域）、`modules`（模块）、`layouts`（布局）、`overlays`（覆盖层）、`states`（状态）边界不够清晰。
2. 部分区域资产仍像示例片段，不够像可维护的页面区域资产。
3. 部分模块资产承担了过多职责，需要明确业务模块边界。
4. 部分布局型资产被放在 `regions` 下，需要在数据表中标记为 `layout`（布局）。
5. 每个主资产都应具备完整 HTML 结构、稳定 class（类名）和可直接渲染能力。
6. CSS（层叠样式表）应集中维护，不应写进每个 HTML 文件。

---

## 2. 本次目标

本次目标是把当前“能跑”的内容资产库，升级成“可维护、可扩展、可直接套用”的内容资产系统。

完成后应满足：

1. 主资产 HTML 可直接插入页面。
2. 每个资产都有清晰的资产层级和职责边界。
3. 所有资产使用稳定 class，不依赖随机 class。
4. 所有资产使用设计系统 token（令牌）和集中 support CSS（支撑样式）。
5. `component-combos`（组件组合）和 `feedback`（反馈）本轮不处理。
6. 不改主检索架构。
7. 不回头修改 step11 / step12 / step13 / step15 文档。
8. 不破坏现有 4 个真实页面验证结果。

---

## 3. 执行范围

### 3.1 必须处理

```text
.claude/skills/xft-design/assets/content-assets/regions
.claude/skills/xft-design/assets/content-assets/modules
.claude/skills/xft-design/assets/content-assets/overlays
.claude/skills/xft-design/assets/content-assets/states
.claude/skills/xft-design/assets/content-assets/_support
.claude/skills/xft-design/data/content-assets/content-assets.csv
.claude/skills/xft-design/data/content-assets/recipe-asset-map.csv
.claude/skills/xft-design/data/content-assets/asset-keywords.csv
.claude/skills/xft-design/data/content-assets/asset-rules.csv
```

### 3.2 必须忽略

```text
.claude/skills/xft-design/assets/content-assets/component-combos
.claude/skills/xft-design/assets/content-assets/feedback
_planning/xft-content-asset-step11
_planning/xft-content-asset-step12
_planning/xft-content-asset-step13
_planning/xft-content-asset-step15
```

### 3.3 原则上不允许修改

```text
.claude/skills/xft-design/SKILL.md
.claude/skills/xft-design/scripts/search_content_assets.py
.claude/skills/xft-design/design-systems/tokens.css
.claude/skills/xft-design/design-systems/components.html
```

例外：如果验证发现 `support_css` 路径未被注入、路径映射错误或 CSV（表格数据）字段无法被现有脚本读取，允许做最小兼容修改，并必须在报告中说明原因。

---

## 4. 核心资产定义

### 4.1 Region（区域）

定义：

```text
Region（区域）= 页面中承担稳定位置和页面结构职责的一级内容区。
```

Region 负责回答：

```text
这个区域放在页面哪里？
它承载什么页面职责？
它和上下区域是什么关系？
```

典型 Region：

```text
页面头部区域
筛选区
表格操作区
表格区
分页区
表单底部操作区
详情摘要区
详情信息区
设置分组区
```

Region 必须是完整 HTML，不是空容器。

示例职责：

```text
筛选区 = label（标签）+ 控件 + 查询/重置操作
表格操作区 = 左侧标题/统计 + 右侧按钮组
表格区 = 表头 + 表体 + 行操作
分页区 = 总数 + 页码 + 每页条数
```

### 4.2 Module（模块）

定义：

```text
Module（模块）= 具备独立业务语义、可被多个页面复用的业务功能块。
```

Module 负责回答：

```text
这个资产本身是否是一个独立业务功能？
离开当前页面，它是否仍然有明确业务含义？
```

典型 Module：

```text
审批流模块
附件列表模块
操作记录模块
公式编辑器模块
表头设置模块
批量操作底栏
异步处理状态模块
```

Module 不按页面位置定义，而按业务能力定义。

### 4.3 Layout（布局）

定义：

```text
Layout（布局）= 跨区域的空间组织方式。
```

Layout 只处理跨区域结构，不处理具体业务内容。

典型 Layout：

```text
左侧锚点 + 右侧内容
左树 + 右表
标签页 + 内容区
主从分栏
左右详情布局
```

注意：

```text
筛选区内部 label 和控件排列，不独立成为 Layout。
操作区内部左右按钮排列，不独立成为 Layout。
审批流内部节点纵向排列，不独立成为 Layout。
```

这些属于 Region / Module 内部布局。

### 4.4 Overlay（覆盖层）

定义：

```text
Overlay（覆盖层）= 保留当前页面上下文的浮层交互载体。
```

典型 Overlay：

```text
Modal（对话框）
Drawer（抽屉）
ConfirmDialog（确认弹窗）
```

Overlay 必须挂载到 `OVERLAY_SLOT`，不得插入 `PAGE_CONTENT_SLOT`。

### 4.5 State（状态）

定义：

```text
State（状态）= 页面或区域在特定数据/流程状态下的展示。
```

典型 State：

```text
空状态
加载中
骨架屏
成功结果
失败结果
异常结果
处理中
```

State 可以作为完整页面内容，也可以作为 Region 内替代内容。

---

## 5. 资产分层规则

最终目标结构如下：

```text
.claude/skills/xft-design/assets/content-assets/
  regions/
    page-header-region/
    filter-region/
    table-action-region/
    data-table-region/
    pagination-region/
    form-footer-region/
    detail-summary-region/
    detail-info-region/
    setting-section-region/

  modules/
    approval-flow/
    attachment-list/
    operation-log/
    formula-editor/
    batch-action-footer/
    table-column-settings/
    async-processing/

  layouts/
    anchor-layout/
    split-layout/
    tabs-layout/
    master-detail-layout/

  overlays/
    modal/
    drawer/

  states/
    empty/
    loading/
    result/
    exception/

  _support/
    region-support.css
    module-support.css
    layout-support.css
    overlay-support.css
    state-support.css
```

### 5.1 文件移动策略

为了降低风险，本次不强制大规模删除旧文件。

执行策略：

1. 先补齐新标准资产文件。
2. 在 `content-assets.csv` 中把新资产路径指向新目录。
3. 旧资产可保留，但不得继续被新 recipe（页面配方）优先命中。
4. 如果旧资产与新资产重复，旧资产在 `notes` 中标记为 `legacy`（旧版）。
5. 不删除旧文件，避免破坏历史验证页面。

---

## 6. CSS 策略

### 6.1 结论

```text
HTML 资产必须完整。
CSS 不写进每个 HTML 资产。
CSS 按资产类型集中维护在 _support 目录。
```

### 6.2 为什么不能只靠 token

Token（令牌）只负责值：

```text
颜色
字号
间距
圆角
阴影
```

CSS 负责结构：

```text
筛选区横向排列
操作区左右布局
表格工具栏左右分组
审批流纵向节点
抽屉右侧固定
弹窗居中
```

因此必须保留 support CSS。

### 6.3 禁止写法

禁止在 HTML 中写内联样式：

```html
<section style="display:flex; gap:16px;"></section>
```

禁止每个资产单独内嵌 `<style>`：

```html
<section class="xft-filter-region"></section>
<style>
.xft-filter-region { ... }
</style>
```

禁止写死颜色和尺寸：

```css
color: #333;
border-radius: 6px;
gap: 16px;
```

### 6.4 推荐写法

HTML：

```html
<section class="xft-region xft-filter-region" data-xft-asset="region.filter.basic"></section>
```

CSS：

```css
.xft-filter-region {
  display: flex;
  gap: var(--spacing-4);
  border-radius: var(--border-radius-large);
  background: var(--color-container-bg-neutral-bright);
}
```

---

## 7. 统一 HTML 资产规范

每个主资产外层必须具备：

```html
data-xft-asset="资产 ID"
data-xft-layer="region | module | layout | overlay | state"
data-xft-variant="basic | advanced | compact | selected | view | edit"
```

### 7.1 Region 外层格式

```html
<section
  class="xft-region xft-{name}-region"
  data-xft-asset="region.{name}.{variant}"
  data-xft-layer="region"
  data-xft-variant="{variant}"
>
  ...
</section>
```

### 7.2 Module 外层格式

```html
<section
  class="xft-module xft-module-card xft-{name}-module"
  data-xft-asset="module.{name}.{variant}"
  data-xft-layer="module"
  data-xft-variant="{variant}"
>
  ...
</section>
```

### 7.3 Layout 外层格式

```html
<section
  class="xft-layout xft-{name}-layout"
  data-xft-asset="layout.{name}.{variant}"
  data-xft-layer="layout"
  data-xft-variant="{variant}"
>
  ...
</section>
```

### 7.4 Overlay 外层格式

```html
<div
  class="xft-overlay-root"
  data-xft-asset="overlay.{name}.{variant}"
  data-xft-layer="overlay"
  data-xft-variant="{variant}"
>
  ...
</div>
```

### 7.5 State 外层格式

```html
<section
  class="xft-state xft-{name}-state"
  data-xft-asset="state.{name}.{variant}"
  data-xft-layer="state"
  data-xft-variant="{variant}"
>
  ...
</section>
```

---

## 8. Slot 机制规则

### 8.1 允许使用 Slot 的地方

Slot（插槽）只用于有限替换，不拆散结构骨架。

允许：

```text
FIELD_SLOT
ACTION_SLOT
TABLE_ROW_SLOT
SETTING_ITEM_SLOT
MODULE_SLOT
OVERLAY_SLOT
STATE_SLOT
```

### 8.2 禁止过度拆分

禁止把资产拆成：

```text
LABEL_SLOT
ICON_SLOT
BUTTON_TEXT_SLOT
BORDER_SLOT
COLOR_SLOT
```

### 8.3 推荐表达

资产中可以写注释说明可替换位置：

```html
<!-- SLOT: FIELD_SLOT，可替换筛选字段组；不得改变 filter-actions 位置 -->
```

不要让 HTML 变成无法直接渲染的空模板。

---

## 9. 必须新增或替换的完整资产文件

以下资产文件为本次必须写入的标准资产。Codex 必须按路径创建或替换。

### 9.1 `assets/content-assets/regions/filter-region/basic.html`

```html
<!-- asset: region.filter.basic | layer: region | variant: basic -->
<section
  class="xft-region xft-filter-region"
  data-xft-asset="region.filter.basic"
  data-xft-layer="region"
  data-xft-variant="basic"
>
  <div class="xft-filter-fields">
    <div class="form-field">
      <label class="field-label">人员姓名</label>
      <div class="form-control">请输入人员姓名</div>
    </div>

    <div class="form-field">
      <label class="field-label">所属组织</label>
      <div class="select-control">请选择组织</div>
    </div>

    <div class="form-field is-short">
      <label class="field-label">在职状态</label>
      <div class="select-control">请选择状态</div>
    </div>
  </div>

  <div class="xft-filter-actions">
    <button class="btn btn-primary" type="button">查询</button>
    <button class="btn btn-secondary" type="button">重置</button>
  </div>
</section>
```

### 9.2 `assets/content-assets/regions/filter-region/advanced.html`

```html
<!-- asset: region.filter.advanced | layer: region | variant: advanced -->
<section
  class="xft-region xft-filter-region is-advanced"
  data-xft-asset="region.filter.advanced"
  data-xft-layer="region"
  data-xft-variant="advanced"
>
  <div class="xft-filter-fields">
    <div class="form-field">
      <label class="field-label">关键词</label>
      <div class="form-control">请输入姓名、手机号或编号</div>
    </div>

    <div class="form-field">
      <label class="field-label">所属组织</label>
      <div class="select-control">请选择组织</div>
    </div>

    <div class="form-field is-short">
      <label class="field-label">人员状态</label>
      <div class="select-control">全部状态</div>
    </div>

    <div class="form-field is-short">
      <label class="field-label">角色类型</label>
      <div class="select-control">全部角色</div>
    </div>

    <div class="form-field is-wide">
      <label class="field-label">更新时间</label>
      <div class="form-control">开始日期 至 结束日期</div>
    </div>
  </div>

  <div class="xft-filter-actions">
    <button class="btn btn-primary" type="button">查询</button>
    <button class="btn btn-secondary" type="button">重置</button>
    <button class="btn btn-text" type="button">收起</button>
  </div>
</section>
```

### 9.3 `assets/content-assets/regions/table-action-region/basic.html`

```html
<!-- asset: region.table-action.basic | layer: region | variant: basic -->
<section
  class="xft-region xft-table-action-region"
  data-xft-asset="region.table-action.basic"
  data-xft-layer="region"
  data-xft-variant="basic"
>
  <div class="xft-table-action-left">
    <div class="xft-region-title">成员列表</div>
    <div class="xft-region-meta">共 128 条数据</div>
  </div>

  <div class="xft-table-action-right">
    <button class="btn btn-secondary" type="button">导出</button>
    <button class="btn btn-secondary" type="button">批量导入</button>
    <button class="btn btn-primary" type="button">新增成员</button>
  </div>
</section>
```

### 9.4 `assets/content-assets/regions/data-table-region/basic.html`

```html
<!-- asset: region.data-table.basic | layer: region | variant: basic -->
<section
  class="xft-region xft-data-table-region"
  data-xft-asset="region.data-table.basic"
  data-xft-layer="region"
  data-xft-variant="basic"
>
  <div class="data-table-wrap">
    <table class="data-table">
      <thead>
        <tr>
          <th>成员姓名</th>
          <th>所属组织</th>
          <th>手机号</th>
          <th>在职状态</th>
          <th>最近更新</th>
          <th class="table-action-col">操作</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>陈语安</td>
          <td>华东销售一部</td>
          <td>138 0000 2048</td>
          <td><span class="status-tag status-success">在职</span></td>
          <td>2026-06-24 16:20</td>
          <td class="table-actions">
            <button class="btn btn-text" type="button">查看</button>
            <button class="btn btn-text" type="button">编辑</button>
          </td>
        </tr>
        <tr>
          <td>李明远</td>
          <td>总行运营管理部</td>
          <td>139 0000 1188</td>
          <td><span class="status-tag status-neutral">停用</span></td>
          <td>2026-06-23 11:08</td>
          <td class="table-actions">
            <button class="btn btn-text" type="button">查看</button>
            <button class="btn btn-text" type="button">启用</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</section>
```

### 9.5 `assets/content-assets/regions/data-table-region/with-selection.html`

```html
<!-- asset: region.data-table.with-selection | layer: region | variant: with-selection -->
<section
  class="xft-region xft-data-table-region"
  data-xft-asset="region.data-table.with-selection"
  data-xft-layer="region"
  data-xft-variant="with-selection"
>
  <div class="xft-selection-summary">
    <span>已选择 <strong>2</strong> 条数据</span>
    <button class="btn btn-text" type="button">清空选择</button>
  </div>

  <div class="data-table-wrap">
    <table class="data-table">
      <thead>
        <tr>
          <th class="table-check-col"><input type="checkbox" checked aria-label="全选" /></th>
          <th>成员姓名</th>
          <th>所属组织</th>
          <th>手机号</th>
          <th>在职状态</th>
          <th class="table-action-col">操作</th>
        </tr>
      </thead>
      <tbody>
        <tr class="is-selected">
          <td class="table-check-col"><input type="checkbox" checked aria-label="选择陈语安" /></td>
          <td>陈语安</td>
          <td>华东销售一部</td>
          <td>138 0000 2048</td>
          <td><span class="status-tag status-success">在职</span></td>
          <td class="table-actions"><button class="btn btn-text" type="button">查看</button></td>
        </tr>
      </tbody>
    </table>
  </div>
</section>
```

### 9.6 `assets/content-assets/regions/pagination-region/basic.html`

```html
<!-- asset: region.pagination.basic | layer: region | variant: basic -->
<nav
  class="xft-region xft-pagination-region"
  data-xft-asset="region.pagination.basic"
  data-xft-layer="region"
  data-xft-variant="basic"
  aria-label="分页"
>
  <div class="xft-pagination-total">共 128 条</div>
  <div class="xft-pagination-actions">
    <button class="btn btn-secondary" type="button">上一页</button>
    <button class="btn btn-primary" type="button">1</button>
    <button class="btn btn-secondary" type="button">2</button>
    <button class="btn btn-secondary" type="button">下一页</button>
    <div class="select-control is-page-size">10 条/页</div>
  </div>
</nav>
```

### 9.7 `assets/content-assets/regions/page-header-region/basic.html`

```html
<!-- asset: region.page-header.basic | layer: region | variant: basic -->
<header
  class="xft-region xft-page-header-region"
  data-xft-asset="region.page-header.basic"
  data-xft-layer="region"
  data-xft-variant="basic"
>
  <div class="xft-page-header-main">
    <h1 class="page-title">页面标题</h1>
    <p class="page-description">用于说明当前页面的业务对象、处理范围和关键规则。</p>
  </div>
</header>
```

### 9.8 `assets/content-assets/regions/page-header-region/with-actions.html`

```html
<!-- asset: region.page-header.with-actions | layer: region | variant: with-actions -->
<header
  class="xft-region xft-page-header-region has-actions"
  data-xft-asset="region.page-header.with-actions"
  data-xft-layer="region"
  data-xft-variant="with-actions"
>
  <div class="xft-page-header-main">
    <h1 class="page-title">成员管理</h1>
    <p class="page-description">集中维护成员基础信息、组织归属、状态和数据权限入口。</p>
  </div>
  <div class="xft-page-header-actions">
    <button class="btn btn-secondary" type="button">导出</button>
    <button class="btn btn-primary" type="button">新增成员</button>
  </div>
</header>
```

### 9.9 `assets/content-assets/regions/form-footer-region/sticky.html`

```html
<!-- asset: region.form-footer.sticky | layer: region | variant: sticky -->
<footer
  class="xft-region xft-form-footer-region is-sticky"
  data-xft-asset="region.form-footer.sticky"
  data-xft-layer="region"
  data-xft-variant="sticky"
>
  <div class="xft-form-footer-info">保存后将按当前配置立即生效，请确认影响范围。</div>
  <div class="xft-form-footer-actions">
    <button class="btn btn-secondary" type="button">取消</button>
    <button class="btn btn-secondary" type="button">暂存</button>
    <button class="btn btn-primary" type="button">提交</button>
  </div>
</footer>
```

### 9.10 `assets/content-assets/layouts/anchor-layout/settings.html`

```html
<!-- asset: layout.anchor.settings | layer: layout | variant: settings -->
<section
  class="xft-layout xft-anchor-layout"
  data-xft-asset="layout.anchor.settings"
  data-xft-layer="layout"
  data-xft-variant="settings"
>
  <aside class="xft-anchor-sidebar">
    <button class="xft-anchor-item is-active" type="button">基础规则</button>
    <button class="xft-anchor-item" type="button">生效范围</button>
    <button class="xft-anchor-item" type="button">修改影响</button>
    <button class="xft-anchor-item" type="button">最近变更</button>
  </aside>
  <div class="xft-anchor-content">
    <section class="xft-setting-section" id="basic-rule">
      <div class="xft-section-header">
        <h2 class="xft-section-title">基础规则</h2>
        <p class="xft-section-desc">控制当前参数是否启用以及默认处理方式。</p>
      </div>
      <div class="xft-setting-item">
        <div>
          <div class="xft-setting-title">启用自动校验</div>
          <div class="xft-setting-desc">提交前自动校验字段完整性和业务规则。</div>
        </div>
        <button class="switch is-on" type="button" aria-label="启用自动校验"></button>
      </div>
    </section>
    <section class="xft-setting-section" id="effective-scope">
      <div class="xft-section-header">
        <h2 class="xft-section-title">生效范围</h2>
        <p class="xft-section-desc">定义配置对哪些组织、角色或业务对象生效。</p>
      </div>
      <div class="xft-scope-list"><span class="tag">总行</span><span class="tag">华东区域</span><span class="tag">公司金融条线</span></div>
    </section>
    <section class="xft-setting-section" id="change-impact">
      <div class="xft-section-header">
        <h2 class="xft-section-title">修改影响</h2>
        <p class="xft-section-desc">修改后将影响新增单据校验，不回溯已完成流程。</p>
      </div>
      <div class="alert alert-warning">建议在业务低峰期调整，并提前通知相关管理员。</div>
    </section>
    <section class="xft-setting-section" id="recent-change">
      <div class="xft-section-header">
        <h2 class="xft-section-title">最近变更</h2>
        <p class="xft-section-desc">记录最近一次配置调整人、时间和变更内容。</p>
      </div>
      <div class="xft-change-record">张三 · 2026-06-24 16:20 · 调整自动校验范围</div>
    </section>
  </div>
</section>
```

### 9.11 `assets/content-assets/modules/approval-flow/basic.html`

```html
<!-- asset: module.approval-flow.basic | layer: module | variant: basic -->
<section
  class="xft-module xft-module-card xft-approval-flow-module"
  data-xft-asset="module.approval-flow.basic"
  data-xft-layer="module"
  data-xft-variant="basic"
>
  <header class="xft-module-header">
    <div>
      <h2 class="xft-module-title">审批流程</h2>
      <p class="xft-module-desc">展示当前单据的审批节点、处理人和处理状态。</p>
    </div>
    <button class="btn btn-secondary" type="button">查看流转记录</button>
  </header>
  <div class="xft-module-body">
    <div class="xft-approval-flow">
      <div class="xft-approval-step is-done"><div class="xft-approval-node">✓</div><div class="xft-approval-content"><div class="xft-approval-title">提交申请 <span class="status-tag status-success">已提交</span></div><div class="xft-approval-desc">申请人提交业务单据，进入审批流程。</div><div class="xft-approval-meta">陈语安 · 2026-06-24 09:30</div></div></div>
      <div class="xft-approval-step is-current"><div class="xft-approval-node">2</div><div class="xft-approval-content"><div class="xft-approval-title">部门负责人审批 <span class="status-tag status-info">处理中</span></div><div class="xft-approval-desc">当前节点需要确认业务信息是否完整。</div><div class="xft-approval-meta">李明远 · 待处理</div></div></div>
      <div class="xft-approval-step"><div class="xft-approval-node">3</div><div class="xft-approval-content"><div class="xft-approval-title">财务复核 <span class="status-tag status-neutral">未开始</span></div><div class="xft-approval-desc">前置节点通过后自动进入。</div></div></div>
    </div>
  </div>
</section>
```

### 9.12 `assets/content-assets/modules/attachment-list/view.html`

```html
<!-- asset: module.attachment-list.view | layer: module | variant: view -->
<section
  class="xft-module xft-module-card xft-attachment-list-module"
  data-xft-asset="module.attachment-list.view"
  data-xft-layer="module"
  data-xft-variant="view"
>
  <header class="xft-module-header">
    <div>
      <h2 class="xft-module-title">审批附件</h2>
      <p class="xft-module-desc">查看本次审批关联的附件材料，支持预览和下载。</p>
    </div>
  </header>
  <div class="xft-module-body">
    <div class="xft-file-list">
      <div class="xft-file-item"><div class="xft-file-main"><div class="xft-file-name">费用明细清单.xlsx</div><div class="xft-file-meta">248 KB · 上传于 2026-06-24 09:28</div></div><div class="xft-file-actions"><button class="btn btn-text" type="button">预览</button><button class="btn btn-text" type="button">下载</button></div></div>
      <div class="xft-file-item"><div class="xft-file-main"><div class="xft-file-name">审批说明.pdf</div><div class="xft-file-meta">1.2 MB · 上传于 2026-06-24 09:29</div></div><div class="xft-file-actions"><button class="btn btn-text" type="button">预览</button><button class="btn btn-text" type="button">下载</button></div></div>
    </div>
  </div>
</section>
```

### 9.13 `assets/content-assets/modules/operation-log/basic.html`

```html
<!-- asset: module.operation-log.basic | layer: module | variant: basic -->
<section
  class="xft-module xft-module-card xft-operation-log-module"
  data-xft-asset="module.operation-log.basic"
  data-xft-layer="module"
  data-xft-variant="basic"
>
  <header class="xft-module-header">
    <div>
      <h2 class="xft-module-title">操作记录</h2>
      <p class="xft-module-desc">记录关键操作人、操作时间和处理结果。</p>
    </div>
  </header>
  <div class="xft-module-body">
    <div class="xft-operation-log">
      <div class="xft-operation-log-item"><div class="xft-log-time">2026-06-24 16:20</div><div class="xft-log-content">张三调整成员所属组织</div><div class="xft-log-result">已完成</div></div>
      <div class="xft-operation-log-item"><div class="xft-log-time">2026-06-23 11:08</div><div class="xft-log-content">李四停用成员账号</div><div class="xft-log-result">已生效</div></div>
      <div class="xft-operation-log-item"><div class="xft-log-time">2026-06-22 18:42</div><div class="xft-log-content">王五导出成员列表</div><div class="xft-log-result">已记录</div></div>
    </div>
  </div>
</section>
```

### 9.14 `assets/content-assets/modules/batch-action-footer/selected.html`

```html
<!-- asset: module.batch-action-footer.selected | layer: module | variant: selected -->
<section
  class="xft-module xft-batch-action-footer"
  data-xft-asset="module.batch-action-footer.selected"
  data-xft-layer="module"
  data-xft-variant="selected"
>
  <div class="xft-batch-summary">
    <span>已选择 <strong>2</strong> 名成员</span>
    <button class="btn btn-text" type="button">清空选择</button>
  </div>
  <div class="xft-batch-actions">
    <button class="btn btn-secondary" type="button">批量导出</button>
    <button class="btn btn-secondary" type="button">批量启用</button>
    <button class="btn btn-danger" type="button">批量停用</button>
  </div>
</section>
```

### 9.15 `assets/content-assets/overlays/modal/member-edit.html`

```html
<!-- asset: overlay.modal.member-edit | layer: overlay | variant: member-edit -->
<div
  class="xft-overlay-root"
  data-xft-asset="overlay.modal.member-edit"
  data-xft-layer="overlay"
  data-xft-variant="member-edit"
>
  <div class="xft-overlay-mask"></div>
  <div class="xft-overlay-center">
    <section class="xft-modal-panel" role="dialog" aria-modal="true" aria-label="编辑成员信息">
      <header class="xft-modal-header">
        <div><h2 class="xft-overlay-title">编辑成员信息</h2><p class="xft-overlay-description">修改成员基础信息、组织归属和在职状态。</p></div>
        <button class="btn btn-text" type="button">关闭</button>
      </header>
      <div class="xft-modal-body">
        <div class="form-grid">
          <div class="form-field"><label class="field-label">成员姓名</label><input class="input" value="陈语安" aria-label="成员姓名" /></div>
          <div class="form-field"><label class="field-label">手机号</label><input class="input" value="138 0000 2048" aria-label="手机号" /></div>
          <div class="form-field"><label class="field-label">所属部门</label><div class="select-control">华东销售一部</div></div>
          <div class="form-field"><label class="field-label">在职状态</label><div class="select-control">在职</div></div>
        </div>
      </div>
      <footer class="xft-modal-footer"><button class="btn btn-secondary" type="button">取消</button><button class="btn btn-primary" type="button">保存</button></footer>
    </section>
  </div>
</div>
```

### 9.16 `assets/content-assets/overlays/drawer/detail.html`

```html
<!-- asset: overlay.drawer.detail | layer: overlay | variant: detail -->
<div
  class="xft-overlay-root"
  data-xft-asset="overlay.drawer.detail"
  data-xft-layer="overlay"
  data-xft-variant="detail"
>
  <div class="xft-overlay-mask"></div>
  <aside class="xft-drawer-panel" role="dialog" aria-modal="true" aria-label="成员详情">
    <header class="xft-drawer-header">
      <div><h2 class="xft-overlay-title">成员详情</h2><p class="xft-overlay-description">在保留列表上下文的前提下查看成员关键信息。</p></div>
      <button class="btn btn-text" type="button">关闭</button>
    </header>
    <div class="xft-drawer-body">
      <section class="xft-module xft-module-card">
        <header class="xft-module-header"><div><h3 class="xft-module-title">基础信息</h3><p class="xft-module-desc">成员基础资料、组织归属和最近更新时间。</p></div><span class="status-tag status-success">在职</span></header>
        <div class="xft-module-body">
          <div class="descriptions-grid">
            <div class="description-cell"><div class="description-label">成员姓名</div><div class="description-value">陈语安</div></div>
            <div class="description-cell"><div class="description-label">所属部门</div><div class="description-value">华东销售一部</div></div>
            <div class="description-cell"><div class="description-label">成员编号</div><div class="description-value">EMP-10284</div></div>
            <div class="description-cell"><div class="description-label">手机号</div><div class="description-value">138 0000 2048</div></div>
            <div class="description-cell"><div class="description-label">入职日期</div><div class="description-value">2024-03-18</div></div>
            <div class="description-cell"><div class="description-label">最近更新</div><div class="description-value">2026-06-24 16:20</div></div>
          </div>
        </div>
      </section>
    </div>
    <footer class="xft-drawer-footer"><button class="btn btn-secondary" type="button">关闭</button><button class="btn btn-primary" type="button">编辑成员</button></footer>
  </aside>
</div>
```

### 9.17 `assets/content-assets/states/empty/table.html`

```html
<!-- asset: state.empty.table | layer: state | variant: table -->
<section
  class="xft-state xft-empty-state"
  data-xft-asset="state.empty.table"
  data-xft-layer="state"
  data-xft-variant="table"
>
  <div class="xft-state-icon">∅</div>
  <h2 class="xft-state-title">暂无符合条件的数据</h2>
  <p class="xft-state-desc">可以调整筛选条件后重新查询，或新增一条业务数据。</p>
  <div class="xft-state-actions">
    <button class="btn btn-secondary" type="button">重置筛选</button>
    <button class="btn btn-primary" type="button">新增数据</button>
  </div>
</section>
```

---

## 10. 必须新增或补强的 support CSS

### 10.1 `assets/content-assets/_support/region-support.css`

在现有文件基础上追加以下内容。不得删除已有规则。

```css
/* Step16: semantic region assets */
.xft-region { width: 100%; box-sizing: border-box; }
.xft-page-header-region { display: flex; align-items: flex-start; justify-content: space-between; gap: var(--spacing-4); margin-bottom: var(--spacing-4); }
.xft-page-header-main { min-width: 0; }
.xft-page-header-actions { display: inline-flex; align-items: center; justify-content: flex-end; gap: var(--spacing-2); flex: 0 0 auto; }
.xft-filter-region { display: flex; align-items: flex-end; justify-content: space-between; gap: var(--spacing-4); padding: var(--spacing-4); margin-bottom: var(--spacing-4); border: 1px solid var(--color-divider-neutral); border-radius: var(--border-radius-large); background: var(--color-container-bg-neutral-bright); }
.xft-filter-region.is-advanced { align-items: flex-start; }
.xft-filter-fields { display: flex; flex-wrap: wrap; align-items: flex-end; gap: var(--spacing-4); flex: 1 1 auto; min-width: 0; }
.xft-filter-fields .form-field { min-width: 180px; flex: 1 1 180px; }
.xft-filter-fields .form-field.is-short { flex: 0 0 160px; }
.xft-filter-fields .form-field.is-wide { flex: 2 1 280px; }
.xft-filter-actions { display: inline-flex; align-items: center; justify-content: flex-end; gap: var(--spacing-2); flex: 0 0 auto; }
.xft-table-action-region { min-height: 56px; display: flex; align-items: center; justify-content: space-between; gap: var(--spacing-4); padding: var(--spacing-4) var(--spacing-6); border-bottom: 1px solid var(--color-divider-neutral); background: var(--color-container-bg-neutral-bright); }
.xft-table-action-left, .xft-table-action-right { display: inline-flex; align-items: center; gap: var(--spacing-2); min-width: 0; }
.xft-table-action-right { justify-content: flex-end; flex: 0 0 auto; }
.xft-region-title { color: var(--color-text-neutral-gray50); font-weight: var(--font-weight-bold); }
.xft-region-meta { color: var(--color-text-neutral-gray30); font-size: var(--font-size-small); }
.xft-data-table-region { background: var(--color-container-bg-neutral-bright); }
.xft-selection-summary { display: flex; align-items: center; justify-content: space-between; gap: var(--spacing-3); padding: var(--spacing-3) var(--spacing-6); border-bottom: 1px solid var(--color-divider-neutral); background: var(--color-bg-accent-subtle); }
.table-check-col { width: 48px; text-align: center; }
.data-table tr.is-selected { background: var(--color-bg-accent-subtle); }
.xft-pagination-region { min-height: 56px; display: flex; align-items: center; justify-content: space-between; gap: var(--spacing-4); padding: var(--spacing-4) var(--spacing-6); background: var(--color-container-bg-neutral-bright); }
.xft-pagination-total { color: var(--color-text-neutral-gray30); font-size: var(--font-size-small); }
.xft-pagination-actions { display: inline-flex; align-items: center; justify-content: flex-end; gap: var(--spacing-2); }
.select-control.is-page-size { min-width: 96px; }
.xft-form-footer-region { display: flex; align-items: center; justify-content: space-between; gap: var(--spacing-4); padding: var(--spacing-4) var(--spacing-6); border-top: 1px solid var(--color-divider-neutral); background: var(--color-container-bg-neutral-bright); }
.xft-form-footer-region.is-sticky { position: sticky; bottom: 0; z-index: 2; }
.xft-form-footer-info { color: var(--color-text-neutral-gray30); font-size: var(--font-size-small); }
.xft-form-footer-actions { display: inline-flex; align-items: center; gap: var(--spacing-2); }
```

### 10.2 `assets/content-assets/_support/module-support.css`

在现有文件基础上追加以下内容。不得删除已有规则。

```css
/* Step16: semantic module assets */
.xft-module { box-sizing: border-box; }
.xft-module-card { border: 1px solid var(--color-divider-neutral); border-radius: var(--border-radius-large); background: var(--color-container-bg-neutral-bright); overflow: hidden; }
.xft-module-card + .xft-module-card { margin-top: var(--spacing-4); }
.xft-module-header { min-height: 56px; display: flex; align-items: center; justify-content: space-between; gap: var(--spacing-3); padding: var(--spacing-4) var(--spacing-6); border-bottom: 1px solid var(--color-divider-neutral); }
.xft-module-title { margin: 0; color: var(--color-text-neutral-gray50); font-size: var(--font-size-regular); font-weight: var(--font-weight-bold); }
.xft-module-desc { margin: var(--spacing-1) 0 0; color: var(--color-text-neutral-gray30); font-size: var(--font-size-small); }
.xft-module-body { padding: var(--spacing-6); }
.xft-approval-flow { display: flex; flex-direction: column; gap: var(--spacing-4); }
.xft-approval-step { position: relative; display: grid; grid-template-columns: 28px minmax(0, 1fr); gap: var(--spacing-3); }
.xft-approval-step::before { content: ""; position: absolute; left: 13px; top: 28px; bottom: -16px; width: 1px; background: var(--color-divider-neutral); }
.xft-approval-step:last-child::before { display: none; }
.xft-approval-node { width: 28px; height: 28px; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; background: var(--color-container-bg-neutral-gray); color: var(--color-text-neutral-gray40); font-size: var(--font-size-small); font-weight: var(--font-weight-bold); }
.xft-approval-step.is-done .xft-approval-node { background: var(--color-bg-success-light); color: var(--color-text-success-regular); }
.xft-approval-step.is-current .xft-approval-node { background: var(--color-bg-accent-regular); color: var(--color-text-neutral-inverse50); }
.xft-approval-content { min-width: 0; }
.xft-approval-title { display: flex; align-items: center; gap: var(--spacing-2); color: var(--color-text-neutral-gray50); font-weight: var(--font-weight-bold); }
.xft-approval-desc, .xft-approval-meta { margin-top: var(--spacing-1); color: var(--color-text-neutral-gray30); font-size: var(--font-size-small); }
.xft-file-list { display: flex; flex-direction: column; gap: var(--spacing-2); }
.xft-file-item { min-height: 48px; display: flex; align-items: center; justify-content: space-between; gap: var(--spacing-3); padding: var(--spacing-3) var(--spacing-4); border: 1px solid var(--color-divider-neutral); border-radius: var(--border-radius-regular); background: var(--color-container-bg-neutral-bright); }
.xft-file-main { min-width: 0; }
.xft-file-name { color: var(--color-text-neutral-gray50); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.xft-file-meta { margin-top: var(--spacing-1); color: var(--color-text-neutral-gray30); font-size: var(--font-size-small); }
.xft-file-actions { display: inline-flex; align-items: center; gap: var(--spacing-2); flex: 0 0 auto; }
.xft-operation-log { display: flex; flex-direction: column; gap: var(--spacing-3); }
.xft-operation-log-item { display: grid; grid-template-columns: 160px minmax(0, 1fr) 100px; gap: var(--spacing-3); color: var(--color-text-neutral-gray40); font-size: var(--font-size-small); }
.xft-log-content { color: var(--color-text-neutral-gray50); }
.xft-log-result { text-align: right; color: var(--color-text-success-regular); }
.xft-batch-action-footer { min-height: 56px; display: flex; align-items: center; justify-content: space-between; gap: var(--spacing-4); padding: var(--spacing-3) var(--spacing-6); border: 1px solid var(--color-border-accent-regular); border-radius: var(--border-radius-large); background: var(--color-bg-accent-subtle); }
.xft-batch-summary, .xft-batch-actions { display: inline-flex; align-items: center; gap: var(--spacing-2); }
```

### 10.3 `assets/content-assets/_support/layout-support.css`

如不存在则新建。

```css
/* XFT content layout support CSS */
.xft-layout { width: 100%; box-sizing: border-box; }
.xft-anchor-layout { display: grid; grid-template-columns: 220px minmax(0, 1fr); gap: var(--spacing-6); align-items: start; }
.xft-anchor-sidebar { position: sticky; top: var(--spacing-4); display: flex; flex-direction: column; gap: var(--spacing-1); padding: var(--spacing-2); border: 1px solid var(--color-divider-neutral); border-radius: var(--border-radius-large); background: var(--color-container-bg-neutral-bright); }
.xft-anchor-item { min-height: 36px; display: flex; align-items: center; padding: 0 var(--spacing-3); border: 0; border-radius: var(--border-radius-regular); background: transparent; color: var(--color-text-neutral-gray40); text-align: left; cursor: pointer; }
.xft-anchor-item.is-active { background: var(--color-bg-accent-subtle); color: var(--color-text-accent-regular); font-weight: var(--font-weight-bold); }
.xft-anchor-content { display: flex; flex-direction: column; gap: var(--spacing-4); min-width: 0; }
.xft-setting-section { padding: var(--spacing-6); border: 1px solid var(--color-divider-neutral); border-radius: var(--border-radius-large); background: var(--color-container-bg-neutral-bright); }
.xft-section-header { margin-bottom: var(--spacing-4); }
.xft-section-title { margin: 0; color: var(--color-text-neutral-gray50); font-size: var(--font-size-heading-4); font-weight: var(--font-weight-bold); }
.xft-section-desc { margin: var(--spacing-1) 0 0; color: var(--color-text-neutral-gray30); font-size: var(--font-size-small); }
.xft-setting-item { min-height: 56px; display: flex; align-items: center; justify-content: space-between; gap: var(--spacing-4); padding: var(--spacing-3) 0; }
.xft-setting-title { color: var(--color-text-neutral-gray50); font-weight: var(--font-weight-bold); }
.xft-setting-desc { margin-top: var(--spacing-1); color: var(--color-text-neutral-gray30); font-size: var(--font-size-small); }
.xft-scope-list { display: flex; flex-wrap: wrap; gap: var(--spacing-2); }
.xft-change-record { color: var(--color-text-neutral-gray40); font-size: var(--font-size-small); }
```

### 10.4 `assets/content-assets/_support/overlay-support.css`

如不存在则新建。若已有同类规则，则合并，不重复定义。

```css
/* XFT content overlay support CSS */
.xft-overlay-root { position: fixed; inset: 0; z-index: 1000; pointer-events: auto; }
.xft-overlay-mask { position: absolute; inset: 0; background: var(--color-bg-mask); }
.xft-overlay-center { position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; padding: var(--spacing-6); }
.xft-modal-panel { width: min(640px, 100%); max-height: calc(100vh - 96px); display: flex; flex-direction: column; border-radius: var(--border-radius-large); background: var(--color-container-bg-neutral-bright); box-shadow: var(--shadow-large-bottom); overflow: hidden; }
.xft-modal-header, .xft-drawer-header { min-height: 56px; display: flex; align-items: center; justify-content: space-between; gap: var(--spacing-3); padding: var(--spacing-4) var(--spacing-6); border-bottom: 1px solid var(--color-divider-neutral); }
.xft-modal-body, .xft-drawer-body { padding: var(--spacing-6); overflow: auto; }
.xft-modal-footer, .xft-drawer-footer { min-height: 56px; display: flex; align-items: center; justify-content: flex-end; gap: var(--spacing-2); padding: var(--spacing-4) var(--spacing-6); border-top: 1px solid var(--color-divider-neutral); }
.xft-overlay-title { margin: 0; color: var(--color-text-neutral-gray50); font-size: var(--font-size-heading-4); font-weight: var(--font-weight-bold); }
.xft-overlay-description { margin: var(--spacing-1) 0 0; color: var(--color-text-neutral-gray30); font-size: var(--font-size-small); }
.xft-drawer-panel { position: absolute; top: 0; right: 0; width: min(560px, 100%); height: 100%; display: flex; flex-direction: column; background: var(--color-container-bg-neutral-bright); box-shadow: var(--shadow-large-left); }
```

### 10.5 `assets/content-assets/_support/state-support.css`

如不存在则新建。

```css
/* XFT content state support CSS */
.xft-state { box-sizing: border-box; }
.xft-empty-state { min-height: 280px; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: var(--spacing-3); padding: var(--spacing-8); border: 1px solid var(--color-divider-neutral); border-radius: var(--border-radius-large); background: var(--color-container-bg-neutral-bright); text-align: center; }
.xft-state-icon { width: 48px; height: 48px; display: inline-flex; align-items: center; justify-content: center; border-radius: 50%; background: var(--color-container-bg-neutral-gray); color: var(--color-text-neutral-gray30); font-size: var(--font-size-heading-3); }
.xft-state-title { margin: 0; color: var(--color-text-neutral-gray50); font-size: var(--font-size-heading-4); font-weight: var(--font-weight-bold); }
.xft-state-desc { margin: 0; color: var(--color-text-neutral-gray30); font-size: var(--font-size-small); }
.xft-state-actions { display: inline-flex; align-items: center; gap: var(--spacing-2); margin-top: var(--spacing-2); }
```

---

## 11. 数据表更新要求

### 11.1 `content-assets.csv`

必须新增或更新以下资产记录。字段顺序以现有 CSV 为准，不得破坏原有列。

```text
region.filter.basic
region.filter.advanced
region.table-action.basic
region.data-table.basic
region.data-table.with-selection
region.pagination.basic
region.page-header.basic
region.page-header.with-actions
region.form-footer.sticky
layout.anchor.settings
module.approval-flow.basic
module.attachment-list.view
module.operation-log.basic
module.batch-action-footer.selected
overlay.modal.member-edit
overlay.drawer.detail
state.empty.table
```

每条资产必须填写：

```text
asset_id
asset_layer
asset_type
asset_name
page_type
keywords
conditions
forbidden_when
variant
html_path
css_path
slots
priority
priority_rank
validation
notes
```

### 11.2 `asset_layer` 取值

```text
region
module
layout
overlay
state
```

不得使用：

```text
display_module
business_module
form_region
```

这些可以保留在 `asset_type`，但不应作为 `asset_layer`。

### 11.3 `css_path`

按资产类型声明：

```text
region  -> assets/content-assets/_support/region-support.css
module  -> assets/content-assets/_support/module-support.css
layout  -> assets/content-assets/_support/layout-support.css
overlay -> assets/content-assets/_support/overlay-support.css
state   -> assets/content-assets/_support/state-support.css
```

### 11.4 `recipe-asset-map.csv`

基础表格页应优先使用新标准资产：

```text
recipe.table.basic
1 region.page-header.basic
2 region.filter.basic
3 region.table-action.basic
4 region.data-table.basic
5 region.pagination.basic
```

批量态和详情抽屉只作为可选：

```text
module.batch-action-footer.selected required=false
region.data-table.with-selection required=false
overlay.drawer.detail required=false
```

设置页如需要锚点布局，应使用：

```text
layout.anchor.settings
```

审批详情页附件展示应优先使用：

```text
module.attachment-list.view
```

不得默认使用上传模块。

---

## 12. 执行步骤

### Step 1：建立备份

创建目录：

```text
.claude/skills/xft-design/_backup/step16-content-assets
```

备份：

```text
assets/content-assets
data/content-assets/content-assets.csv
data/content-assets/recipe-asset-map.csv
data/content-assets/asset-keywords.csv
data/content-assets/asset-rules.csv
```

### Step 2：创建新目录

创建第 5 节列出的新目录。

### Step 3：写入第 9 节中的完整 HTML 资产

必须逐个创建或替换，不得只写占位内容。

### Step 4：补齐 support CSS

按第 10 节追加或创建 CSS。

### Step 5：更新数据表

更新：

```text
data/content-assets/content-assets.csv
data/content-assets/recipe-asset-map.csv
data/content-assets/asset-keywords.csv
data/content-assets/asset-rules.csv
```

原则：

1. 新资产优先级高于旧资产。
2. 旧资产保留但不优先命中。
3. `region.settings-layout.anchor` 这类布局型资产在数据表中标为 `asset_layer=layout`。
4. `module-upload-file-basic` 不得作为审批详情附件查看的默认资产。
5. 附件查看语义使用 `module.attachment-list.view`。
6. 弹窗编辑语义优先使用 `overlay.modal.member-edit`。

### Step 6：验证搜索输出

运行：

```bash
python .claude/skills/xft-design/scripts/search_content_assets.py "员工花名册列表页，支持筛选、导出、新增成员、查看详情" --pretty
python .claude/skills/xft-design/scripts/search_content_assets.py "审批详情页，包含基础信息、审批流、审批附件、操作记录" --pretty
python .claude/skills/xft-design/scripts/search_content_assets.py "参数配置设置页，包含左侧锚点、生效范围、修改影响、最近变更" --pretty
python .claude/skills/xft-design/scripts/search_content_assets.py "弹窗编辑成员信息" --pretty
```

检查：

1. 表格页默认命中 `region.filter.basic`、`region.table-action.basic`、`region.data-table.basic`、`region.pagination.basic`。
2. 审批详情页命中 `module.approval-flow.basic`、`module.attachment-list.view`、`module.operation-log.basic`。
3. 设置页命中 `layout.anchor.settings`。
4. 弹窗编辑命中 `overlay.modal.member-edit` 或保持 `Page Overlay + Modal` 语义。
5. `unsupported` 为空。
6. `read_order` 路径都真实存在。

### Step 7：重新生成真实页面验证

重新生成以下 4 个页面：

```text
employee-roster-validation-2026-06-25-v3.html
approval-detail-validation-2026-06-25-v3.html
settings-config-validation-2026-06-25-v3.html
member-edit-modal-validation-2026-06-25-v3.html
```

每个页面必须包含：

```text
XFT_ROUTE
CONTENT_ASSET_DECISION
```

### Step 8：运行结构校验

运行现有校验脚本：

```bash
python .claude/skills/xft-design/scripts/check_skill_output.py .claude/skills/xft-design/examples/employee-roster-validation-2026-06-25-v3.html
python .claude/skills/xft-design/scripts/check_skill_output.py .claude/skills/xft-design/examples/approval-detail-validation-2026-06-25-v3.html
python .claude/skills/xft-design/scripts/check_skill_output.py .claude/skills/xft-design/examples/settings-config-validation-2026-06-25-v3.html
python .claude/skills/xft-design/scripts/check_skill_output.py .claude/skills/xft-design/examples/member-edit-modal-validation-2026-06-25-v3.html
```

---

## 13. 验收标准

### 13.1 结构验收

必须满足：

```text
4 个页面全部 PASS
所有页面保留 XFT_ROUTE
所有页面保留 CONTENT_ASSET_DECISION
unsupported 为空
read_order 路径真实存在
support_css 路径真实存在
```

### 13.2 资产验收

必须满足：

```text
每个新增资产 HTML 可直接渲染
每个新增资产有 data-xft-asset
每个新增资产有 data-xft-layer
每个新增资产有 data-xft-variant
没有内联 style
没有资产内联 <style>
没有随机 class
默认内容不是“字段名称”“内容占位”
```

### 13.3 CSS 验收

必须满足：

```text
CSS 集中在 _support 文件
不新增每资产 CSS 文件
不写死颜色
不写死字号
不写死圆角
不写死阴影
全部使用已有 token
```

### 13.4 语义验收

必须满足：

```text
筛选区像真实筛选区
操作区像真实按钮组区域
表格区像真实数据表格
分页区像真实分页区域
审批附件是查看/预览/下载语义，不是上传语义
弹窗编辑是 Overlay，不是完整页面
设置页锚点和内容一一对应
```

### 13.5 回归验收

不得破坏：

```text
SKILL.md v7 流程
ROUTE_DECISION
CONTENT_ASSET_DECISION
search_content_assets.py 主流程
已有 shell
tokens.css
components.html
```

---

## 14. 输出报告要求

执行完成后，必须输出：

```text
.claude/skills/xft-design/reports/step16-content-assets-refactor-report.md
```

报告必须包含：

```text
1. 本次新增文件
2. 本次修改文件
3. 新增资产清单
4. 旧资产兼容处理说明
5. region / module / layout / overlay / state 分类结果
6. 新增或修改的 support CSS
7. 搜索脚本验证结果
8. 4 个真实页面验证结果
9. 剩余问题
10. 是否建议进入下一阶段
```

---

## 15. 风险控制

### 15.1 不要一次性删除旧资产

旧资产先保留，避免破坏历史路径。

### 15.2 不要重构检索架构

本次只调数据表和资产文件，不改主架构。

### 15.3 不要把 Combo 独立拉进主检索

`combo` 本轮忽略。主检索层仍以：

```text
region
module
layout
overlay
state
```

为主。

### 15.4 不要过度 Slot 化

资产必须可直接渲染，不允许变成空模板。

### 15.5 不要用 CSS 替代 token

CSS 使用 token，不写死视觉值。

---

## 16. 完成定义

当以下条件全部满足，本轮完成：

```text
1. 第 9 节资产全部落地。
2. 第 10 节 support CSS 全部补齐。
3. content-assets.csv 和 recipe-asset-map.csv 已同步。
4. 搜索脚本能正确返回新资产。
5. 4 个真实页面 v3 全部 PASS。
6. unsupported 为空。
7. 页面视觉没有明显退化。
8. 输出 step16-content-assets-refactor-report.md。
```

完成后，本项目内容资产系统进入：

```text
可用基线版 → 可维护资产系统版
```
