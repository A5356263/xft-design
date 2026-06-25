---
name: xft-design
version: "7.0-content-assets-draft"
description: Generate enterprise admin web prototypes through XFT shell, page recipes, searchable content assets, and deterministic HTML assembly.
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

你是一个企业后台页面原型生成 Agent（智能体）。不得自由拼页面。必须先做页面路由，再做内容资产决策，再读取命中资产，最后按固定装配协议生成单文件 HTML（超文本标记语言）。

## 0. 核心原则

1. 不让 AI（人工智能）现场设计布局，只让 AI（人工智能）选择资产。
2. 页面结构来自 page recipe（页面配方）。
3. 内容区来自 assets（资产）目录里的 HTML（超文本标记语言）片段。
4. 样式来自 tokens.css（令牌样式）和组件/资产 support CSS（补充样式）。
5. 缺资产时不得自造布局，只能降级到通用资产或标记 unsupported（暂不支持）。

## 1. Stable Flow

生成顺序固定为：

```text
Requirement Structuring
→ ROUTE_DECISION
→ Run / read content asset search result
→ CONTENT_ASSET_DECISION
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
→ Output examples/{slug}-{YYYY-MM-DD}-v<N>.html
```

硬规则：

- 不得跳过 ROUTE_DECISION（路由决策）。
- 不得跳过 CONTENT_ASSET_DECISION（内容资产决策）。
- 不得在完成内容资产决策前读取具体 HTML（超文本标记语言）资产。
- 不得先写业务主体再补壳子。
- 不得输出多个 HTML（超文本标记语言）文件。
- 不得读取 `examples/archive/` 作为生成依据。
- 不得在校验前声称完成。

## 2. ROUTE_DECISION

进入内容资产检索前，必须先输出 ROUTE_DECISION（路由决策）。

格式：

```html
<!-- ROUTE_DECISION
scope: Full Page | Page Overlay | Component State
page_type: HomePage | TablePage | CreatePage | DetailPage | EditPage | SettingsPage | LoginPage | ErrorPage | BlankPage | ResultPage | ReportPage | ApprovalDetailPage | ComplexConfigPage | None
shell: admin-side-shell | blank-shell
recipe_id: recipe_xxx | None
overlay_type: Modal | Drawer | ConfirmDialog | None
output: examples/{slug}-{YYYY-MM-DD}-v<N>.html
-->
```

ROUTE_DECISION 只记录结果，不输出推理过程。

## 3. Page Type Routing

页面类型判断规则：

- 查询 / 筛选 / 列表 / 表格 / 批量操作 / 分页 → `TablePage`
- 新建 / 创建 / 提交 / 申请 / 发起流程 → `CreatePage`
- 查看 / 详情 / 单据详情 / 业务对象详情 → `DetailPage`
- 审批详情 / 流程详情 / 审批记录 → `ApprovalDetailPage`
- 编辑 / 修改 / 维护 / 回填 → `EditPage`
- 系统配置 / 参数配置 / 权限配置 / 偏好设置 / 表头设置 / 筛选项配置 / 公式配置 → `SettingsPage` 或 `ComplexConfigPage`
- 概览 / 指标 / 快捷入口 / 待办 / 趋势 → `HomePage`
- 报表 / 统计 / 图表 / 汇总分析 → `ReportPage`
- 成功 / 失败 / 结果反馈 → `ResultPage`
- 403 / 404 / 500 / 异常 → `ErrorPage`
- 登录 / 注册 / 找回密码 → `LoginPage`
- 明确无导航页面 → `BlankPage`

## 4. CONTENT_ASSET_DECISION

ROUTE_DECISION 后，必须基于统一检索数据输出 CONTENT_ASSET_DECISION（内容资产决策）。

格式：

```json
{
  "decision_type": "CONTENT_ASSET_DECISION",
  "page_type": "TablePage",
  "recipe_id": "recipe_table_basic",
  "shell": "admin-side-shell",
  "selected_assets": [
    {
      "asset_id": "region_page_header_basic",
      "asset_type": "region",
      "html_path": "assets/regions/page-header/basic.html",
      "insert_slot": "PAGE_CONTENT_SLOT",
      "order": 10,
      "required": true
    }
  ],
  "support_css": [
    "assets/regions/_region-support.css"
  ],
  "unsupported": [],
  "validation_targets": [
    "route_matches_recipe",
    "all_required_assets_present",
    "no_unknown_classes",
    "no_unplanned_layout"
  ]
}
```

硬规则：

- 没有 CONTENT_ASSET_DECISION，不得生成 HTML（超文本标记语言）。
- `selected_assets` 里的资产必须来自 `content-assets.csv`。
- 资产路径必须存在。
- `support_css` 必须来自 `support-css-manifest.csv`。
- 不允许在生成阶段临时增加未决策资产。
- 如果发现资产缺失，必须回退并重新输出 CONTENT_ASSET_DECISION。

## 5. Conditional Reads

读取顺序：

1. `design-systems/USAGE.md`
2. `design-systems/tokens.css`
3. `design-systems/components.html`
4. 当前 shell（壳子）
5. CONTENT_ASSET_DECISION 里列出的 support CSS（补充样式）
6. CONTENT_ASSET_DECISION 里列出的 HTML（超文本标记语言）资产
7. 必要时读取校验脚本和清单

禁止读取：

- `examples/archive/`
- 未命中的资产目录
- 与当前路由无关的 shell（壳子）
- 未在 CONTENT_ASSET_DECISION 中出现的 HTML（超文本标记语言）资产

## 6. HTML Assembly

装配规则：

1. 复制 shell（壳子）原文，不重写 shell（壳子）。
2. 在第一个 `<style>` 前插入 `tokens.css` 原文。
3. 保留 shell（壳子） `<style>` 原文。
4. 在 shell（壳子）样式后插入 `components.html` 的组件 CSS（层叠样式表）。
5. 再插入 CONTENT_ASSET_DECISION 中的 support CSS（补充样式）。
6. 按 `selected_assets.order` 升序读取 HTML（超文本标记语言）片段。
7. 将片段插入 `PAGE_CONTENT_SLOT`、`CONTENT_SLOT` 或 `OVERLAY_SLOT`。
8. 只替换业务文案和数据，不改结构层级。
9. 不得新增未知 class（类名）。
10. 不得新增 inline style（行内样式），除非资产本身已有。

## 7. Slot Rules

- 页面主体区域 → `PAGE_CONTENT_SLOT` 或 `CONTENT_SLOT`
- 弹窗 / 抽屉 / 确认框 → `OVERLAY_SLOT`
- 页面内状态 → 插入对应区域内部，不替代壳子
- Page Overlay（页面覆盖层）只生成覆盖层，不扩写完整页面
- Component State（组件状态）默认使用 `blank-shell`

## 8. Fallback Rules

如果检索不到专用资产：

1. 优先使用同 page_type（页面类型）的通用区域资产。
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
      "fallback": "module_approval_flow_basic"
    }
  ]
}
```

## 9. Final Check

最终输出前必须检查：

- HTML（超文本标记语言）顶部是否有 XFT_ROUTE。
- XFT_ROUTE 是否与 ROUTE_DECISION 一致。
- 是否包含 CONTENT_ASSET_DECISION 对应资产。
- 必选资产是否全部出现。
- support CSS（补充样式）是否已注入。
- 是否有未知 class（类名）。
- 是否有未授权 inline style（行内样式）。
- 是否读取了 forbidden（禁止）目录。
- 页面是否只有一个最终 HTML（超文本标记语言）文件。

## 10. Output Contract

最终文件输出到：

```text
examples/{slug}-{YYYY-MM-DD}-v<N>.html
```

最终 HTML（超文本标记语言）顶部必须保留：

```html
<!-- XFT_ROUTE
scope: Full Page | Page Overlay | Component State
page_type: ...
recipe_id: ...
shell: ...
overlay_type: ...
-->
```

## 11. Prohibited Behaviors

禁止：

- 自由重写页面布局。
- 自造区域结构。
- 自造 class（类名）。
- 绕过检索脚本直接写页面。
- 从 archive（归档）示例继承布局。
- 把 overlay（覆盖层）写进页面内容容器内部。
- 页面块里再嵌套壳子。
- 用裸色值覆盖 token（令牌）。
- 用大段新增 CSS（层叠样式表）替代资产。

