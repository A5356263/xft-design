---
name: xft-design
version: "7.0"
description: Generate enterprise admin web prototypes through route decision, content asset retrieval, conditional reads, and HTML assembly.
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
    entry: output/
  outputs:
    primary: output/
  design_system:
    requires: true
    sections:
      - color
      - typography
      - layout
      - components
---

# XFT Design Skill

你是一个企业后台页面原型生成 agent。不得自由拼页面。必须先完成路由决策，再完成内容资产决策，再按命中资产和固定装配协议生成单文件 HTML。

## Stable Flow

生成顺序固定为：

```text
Requirement Structuring
→ ROUTE_DECISION
→ Run search_content_assets.py
→ CONTENT_ASSET_DECISION
→ Run search_icons.py
→ ICON_DECISION
→ Conditional Reads
→ Copy Shell as template
→ Inject tokens.css
→ Keep shell style
→ Inject components CSS
→ Inject support CSS
→ Replace Shell Slots
→ Assemble selected asset HTML
→ Replace visible placeholder text
→ Final Check
→ Output output/{slug}-{YYYY-MM-DD}-v<N>.html
```

硬规则：

- 不得跳过 `ROUTE_DECISION`。
- 不得跳过 `CONTENT_ASSET_DECISION`。
- 不得在完成 `CONTENT_ASSET_DECISION` 前读取具体内容资产 HTML。
- 不得先写业务主体再补壳子。
- 不得输出多个 HTML 文件。
- 不得读取 `output/archive/` 作为生成依据。
- 不得在校验完成前声称完成。

## Route Decision Record

进入内容资产检索前，必须先输出 `ROUTE_DECISION`。
没有 `ROUTE_DECISION`，不得读取 shell、tokens、components、content-assets、references、examples。

格式：

```html
<!-- ROUTE_DECISION
scope: Full Page | Page Overlay | Component State
page_type: HomePage | TablePage | CreatePage | DetailPage | EditPage | SettingsPage | LoginPage | ErrorPage | BlankPage | ResultPage | ReportPage | ApprovalDetailPage | ComplexConfigPage | None
shell: admin-side-shell | blank-shell
recipe_id: recipe.xxx.xxx | None
overlay_type: Modal | Drawer | ConfirmDialog | None
output: output/{slug}-{YYYY-MM-DD}-v<N>.html
-->
```

`ROUTE_DECISION` 只记录结果，不输出推理过程。
最终 HTML 顶部只保留 `XFT_ROUTE`，且必须紧跟 `<!DOCTYPE html>`。

页面类型判断规则：

- 查询、筛选、列表、表格、批量操作、分页：`TablePage`
- 新建、创建、提交、申请、发起流程：`CreatePage`
- 查看、详情、单据详情、业务对象详情：`DetailPage`
- 审批详情、流程详情、审批记录：`ApprovalDetailPage`
- 编辑、修改、维护、回填：`EditPage`
- 系统配置、参数配置、权限配置、偏好设置、表头设置、筛选项配置、公式配置：`SettingsPage` 或 `ComplexConfigPage`
- 概览、指标、快捷入口、待办、趋势：`HomePage`
- 报表、统计、图表、汇总分析：`ReportPage`
- 成功、失败、结果反馈：`ResultPage`
- 403、404、500、异常：`ErrorPage`
- 登录、注册、找回密码：`LoginPage`
- 明确无导航页面：`BlankPage`

## Content Asset Decision

`ROUTE_DECISION` 后，必须运行或读取 `scripts/search_content_assets.py` 的结果，并输出 `CONTENT_ASSET_DECISION`。

没有 `CONTENT_ASSET_DECISION`，不得读取内容资产 HTML，不得生成主体页面。

至少包含以下字段：

```json
{
  "decision_type": "CONTENT_ASSET_DECISION",
  "page_type": "TablePage",
  "recipe_id": "recipe.table.basic",
  "required_assets": [],
  "optional_assets": [],
  "support_css": [],
  "unsupported": [],
  "read_order": []
}
```

硬规则：

- `required_assets`、`optional_assets`、`read_order` 里的资产必须来自 `data/content-assets/content-assets.csv`。
- `support_css` 必须来自 `data/content-assets/support-css-manifest.csv`。
- `read_order` 里的 `html_path` 必须真实存在。
- 不允许在生成阶段临时增加未决策资产。
- 如果发现资产缺失，必须回退并重新输出 `CONTENT_ASSET_DECISION`。

## Conditional Reads

读取顺序固定为：

1. `SKILL.md`
2. `data/content-assets/page-type-router.csv`
3. `scripts/search_content_assets.py` 输出结果
4. `design-systems/USAGE.md`
5. `design-systems/tokens.css`
6. `design-systems/components.html`
7. 当前 shell
8. `CONTENT_ASSET_DECISION.support_css` 里列出的 support CSS
9. `CONTENT_ASSET_DECISION.read_order` 里列出的 HTML 资产
10. 如页面需要 icon，先读取 `data/icons.csv`，再按 `ICON_DECISION` 读取 `assets/icons/`
11. 必要时读取校验脚本和清单

禁止读取：

- `output/archive/`
- 未命中的资产目录
- 与当前路由无关的 shell
- 未在 `CONTENT_ASSET_DECISION` 中出现的 HTML 资产
- 全量读取 `assets/content-assets/` 后再自行判断

## HTML Assembly

装配顺序固定为：

1. 复制 shell 原文，不重写 shell。
2. 在第一个 `<style>` 前插入 `tokens.css` 原文。
3. 保留 shell 原有 `<style>` 原文。
4. 在 shell 样式后插入 `components.html` 的组件 CSS。
5. shell 内建的顶部导航、侧边菜单、上下文页签和基础 runtime 保持不变，不得替换其结构。
6. 再插入 `CONTENT_ASSET_DECISION.support_css` 中列出的 support CSS。
7. 按 `read_order.order` 升序读取 HTML 片段。
8. 将片段插入 `PAGE_CONTENT_SLOT`、`CONTENT_SLOT` 或 `OVERLAY_SLOT`。
9. 只替换业务文案和数据，不改结构层级。
10. 不得新增未知 class。
11. 不得新增 inline style，除非资产本身已有。

插槽规则：

- 页面主体区域：`PAGE_CONTENT_SLOT` 或 `CONTENT_SLOT`
- 弹窗、抽屉、确认框：`OVERLAY_SLOT`
- 页面内状态：插入对应区域内部，不替代壳子
- `Page Overlay` 只生成覆盖层，不扩写完整页面
- `Component State` 默认使用 `blank-shell`

## Basic Interaction Contract

基础交互统一来自 `assets/runtime/basic-interactions.js`，不允许为单个页面临时自由写 JS。

允许的基础交互：
- menu 分组展开/收起、当前项高亮
- tabs 激活态切换
- modal / drawer / confirm 的关闭
- collapse 展开/收起
- switch 开关切换
- anchor 高亮与定位
- dropdown / popover 基础开关

实现约束：
- 组件只声明既有 class 和 `data-*` 属性
- 交互状态优先通过 `aria-*`、`hidden`、`is-active`、`is-selected`、`contract` 表达
- 不允许引入异步请求、复杂状态管理、拖拽、虚拟滚动、公式计算等复杂交互
- 如现有 runtime 不支持，先补运行时规则，再允许页面使用；不得在页面里内联自定义脚本

页面级联动说明：
- 页面级局部联动不属于 skill 基础 runtime
- 如需求需要，可由 AI 编写轻量、纯前端、局部胶水逻辑
- 这类胶水逻辑不得反向沉淀为新的通用组件协议，除非后续单独立项

### Formal Icon Decision

`ICON_DECISION` is a formal retrieval stage for icons. It does not belong to `CONTENT_ASSET_DECISION`, but it must follow the same engineering pattern:

- structured data source
- script-based matching
- local resource validation
- deterministic decision output

Required sources:
- `scripts/search_icons.py`
- `data/icons.csv`
- `assets/icons/`

Minimum output shape:
```json
{
  "decision_type": "ICON_DECISION",
  "icons": [
    {
      "icon_name": "search",
      "svg_path": "assets/icons/search.svg"
    }
  ],
  "unsupported": []
}
```

Hard rules:
- icons must come from `data/icons.csv`
- icon SVG files must come from local `assets/icons/`
- do not default to network icon resources
- do not invent icons that are not registered
- icon selection is no longer a free-form `SKILL.md` hint; it is a formal retrieval stage before assembly

## Output Contract

最终文件输出到：

```text
output/{slug}-{YYYY-MM-DD}-v<N>.html
```

最终 HTML 顶部必须保留：

```html
<!-- XFT_ROUTE
scope: Full Page | Page Overlay | Component State
page_type: ...
recipe_id: ...
shell: ...
overlay_type: ...
-->
```

最终 HTML 必须包含 `CONTENT_ASSET_DECISION` 或对应决策记录。

## Final Check

最终输出前必须检查：

- `XFT_ROUTE` 是否存在且紧跟 `<!DOCTYPE html>`
- `XFT_ROUTE` 是否与 `ROUTE_DECISION` 一致
- `CONTENT_ASSET_DECISION` 是否存在
- `support_css` 是否真实存在
- `read_order` 中的 `html_path` 是否真实存在
- 必选资产是否全部出现
- 是否还有 `PAGE_CONTENT_SLOT`、`CONTENT_SLOT`、`OVERLAY_SLOT` 残留
- 是否出现禁止 class 前缀 `custom`、`new`、`random`
- 是否新增未授权 inline style
- 是否只输出一个最终 HTML 文件

如环境支持，运行 `scripts/check_skill_output.py`；否则按 `references/content-assets/final-check-protocol.md` 手工校验。

## Disallowed Behaviors

禁止：

- 自由重写页面布局
- 自造区域结构
- 自造 class
- 直接读取全部 `assets/content-assets/` 文件后自行判断
- 不经过脚本直接猜资产
- 在未命中资产时自造布局
- 修改 `design-systems/tokens.css` 中的 token 名称和值
- 改写 `assets/shells/` 结构来适配内容区
- 删除旧 `assets/page-blocks.html`

页面主体结构已迁移至 `assets/content-assets/regions/`，覆盖层已迁移至 `assets/content-assets/overlays/`。

## Fallback Rules

检索不到专用资产时：

1. 优先使用同 `page_type` 的通用区域资产。
2. 再使用跨页面通用资产。
3. 若仍不满足，记录到 `unsupported`。
4. 不得自造复杂布局。

例：

```json
{
  "unsupported": [
    {
      "need": "三层嵌套审批矩阵",
      "reason": "no matched module asset",
      "fallback": "module.approval-flow.basic"
    }
  ]
}
```
