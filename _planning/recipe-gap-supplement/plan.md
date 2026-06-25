# XFT Design Skill — 优化规划

## 背景

### 这个 Skill 是什么

`xft-design` 是一个企业后台页面原型生成 Skill。它通过固定的装配流水线（Route Decision → Content Asset Decision → 读取 HTML 积木 → 装配输出），生成 B 端管理后台原型页面。

**设计理念**：不让 AI 自由发挥页面结构，而是提供预制的区域/模块 HTML 积木块，AI 负责按 recipe 规则选择和装配。

### 借鉴来源

| 借鉴对象 | 借鉴了什么 |
|----------|-----------|
| `ui-ux-pro-max` | BM25 搜索引擎 + CSV 知识库 + 推理链路的思路（产品→风格→参数），转化为"需求→页面类型→页面配方→资产组合" |
| `ant-design-pro` | B 端页面结构知识，将其 `src/pages/` 的完整页面拆解为更细粒度的 region/module HTML 积木块 |

### 本次优化的问题来源

在完成 skill 搭建后，我们对两个参考 skill 和 xft-design 自身做了完整分析（见根目录 `skill-research-report.md`），并评估了借鉴效果。过程中发现三个问题：

#### 问题 1：部分资产类型 AI 不需要

当前 `assets/content-assets/` 下有 7 类资产：`regions`、`modules`、`component-combos`、`feedback`、`overlays`、`states`。但经过分析：

| 资产类别 | 是否需要 | 原因 |
|----------|---------|------|
| `regions` | **必须保留** | 区域排列规则（筛选栏左右分区、表格工具栏等）AI 容易写得不一致 |
| `modules` | **必须保留** | 业务模块（审批流、公式编辑器、文件预览等）结构复杂，AI 难写对 |
| `states` | **保留** | 空状态、加载态、结果态——结构简单但需要规范一致性 |
| `component-combos` | **移除** | 一个 input 配一个 label，AI 闭着眼就能写，给好 CSS 即可 |
| `feedback` | **移除** | Alert/Message/Notification，AI 不需要模板 |
| `overlays` | **移除** | Modal/Drawer/Popconfirm 的结构 AI 很熟，不需要模板 |

**结论**：regions 和 modules 是核心价值——它们解决了"AI 容易写错的结构和排列"。其他三类是多余的。

#### 问题 2：缺少对标 ant-design-pro 的高级 Recipe

ant-design-pro 提供了 10+ 种页面类型。对标后 xft-design 的 recipe 体系覆盖了大部分，但缺少：

1. **高级表单**（antd-pro `form/advanced-form`）：多 Card 分组 + 动态表单项
2. **多 Tab 详情**（antd-pro `profile/advanced`）：Tab 切换不同信息区
3. **表格 CRUD 闭环**：表格 + 弹窗编辑（增删改不跳页）

所需 region 积木块（`form-section.multi-section`、`tabs.basic`）已存在，只需补 recipe 规则。

### 核心原则

**AI 不需要 HTML 模板就能写的东西，不要给模板。AI 容易写错结构和排列的东西，用积木块约束。**

---

## 执行顺序

1. 先移除三类低价值资产的 CSV 检索入口
2. 再补充 4 个缺失 recipe
3. 先后顺序确保新 recipe 不会被配对上即将移除的资产

---

## Part 1：移除三类低价值资产

### 策略

**只删 CSV 检索入口，不删物理文件。**

| 操作 | 原因 |
|------|------|
| 从 `content-assets.csv` 删三类行 | 切掉检索入口，search_content_assets.py 搜不到 |
| 从 `asset-keywords.csv` 删对应行 | 关键词不再触发匹配 |
| 从 `recipe-asset-map.csv` 删引用 | 配方不再拉入 |
| `asset-rules.csv` 中的规则不动 | 规则是知识（如 `modal_vs_drawer`、`blocking_level`），AI 仍需参考 |
| HTML 文件不动 | 物理保留，随时可恢复 |
| `_support/*.css` 不动 | 同上 |

### 要移除的资产

component-combos（10 个）：`combo-input-field`、`combo-select-field`、`combo-date-picker`、`combo-checkbox-group`、`combo-radio-group`、`combo-switch-setting`、`combo-upload-field`、`combo-cascader`、`combo-tree-select`、`combo-input-number`、`combo-time-picker`、`combo-sidebar-contents`、`combo-button-placement/*`、`combo-display/*`

feedback（6 个）：`feedback-alert-basic`、`feedback-alert-warning`、`feedback-message-error`、`feedback-message-success`、`feedback-notification-basic`

overlays（5 个）：`OV_MODAL_FUNCTIONAL`、`OV_MODAL_CONFIRM`、`OV_DRAWER_BASIC`、`overlay.detail-drawer`、`overlay.popconfirm-basic`

### 必须保留的规则（asset-rules.csv）

| 规则 ID | 内容 | 保留原因 |
|---------|------|---------|
| `overlay_mount` | Modal/Drawer 必须挂到 OVERLAY_SLOT | 装配约束 |
| `modal_vs_drawer` | 短流程用 Modal，长表单用 Drawer | 选型指导 |
| `blocking_level` | Message 不阻断，Alert 弱阻断，Confirm Modal 强阻断 | 交互规范 |
| `empty_action` | 空状态必须给出原因或下一步 | UX 规范 |
| `loading_choice` | Skeleton vs Spin vs Progress | 性能/UX 规范 |

---

## Part 2：补充 Recipe

### 1. 新增 `recipe.form.advanced`（CreatePage）

**对标**：ant-design-pro `form/advanced-form`

**背景**：当前 `recipe.form.basic` 只能处理单 Section 简单表单，无法表达多分组 + 动态表单项场景。

**region_order**：
```
page-header > form-summary-card > multi-section-form > dynamic-form-list > form-footer-actions
```

**required_regions**：`page-header;form-summary-card;multi-section-form;form-footer-actions`

**optional_modules**：`dynamic-form-list;attachment-upload;confirm-modal;form-help`

**forbidden_patterns**：不得把所有分组铺平不区分层级；不得缺少分组标题

**关键词**：高级表单、多分组、动态字段、明细录入、成员管理、发票信息

**priority**：85

---

### 2. 新增 `recipe.detail.tabs`（DetailPage）

**对标**：ant-design-pro `profile/advanced`

**背景**：当前 detail recipe 只有 section-stack 和 two-column-layout，缺少 Tab 切换多信息区的表达。

**region_order**：
```
page-header > detail-summary > tabs > tab-panel-basic > tab-panel-detail > tab-panel-log
```

**required_regions**：`page-header;detail-summary;tabs;tab-panel-basic`

**optional_modules**：`tab-panel-detail;tab-panel-log;related-table;attachment-list;operation-log`

**forbidden_patterns**：不得把所有内容平铺不分组；不得让 Tab 承担流程步骤

**关键词**：多标签详情、Tab 详情、复杂详情、分 tab 查看

**priority**：85

---

### 3. 新增 `recipe.detail.table-tabs`（DetailPage）

**对标**：ant-design-pro `profile/advanced` 中 Tab 嵌套表格的场景

**背景**：详情页中某些 Tab 包含关联表格，需要在 Tab 内嵌入 table 区域。

**region_order**：
```
page-header > detail-summary > tabs > tab-panel-basic > tab-panel-table > tab-panel-log
```

**required_regions**：`page-header;detail-summary;tabs;tab-panel-basic;tab-panel-table`

**optional_modules**：`related-table;attachment-list;operation-log;tab-panel-log`

**关键词**：表格详情、关联表详情、多 Tab 表格

**priority**：80

---

### 4. 新增 `recipe.table.crud`（TablePage）

**对标**：B 端高频变体——表格 + 页面内弹窗编辑闭环

**背景**：当前 recipe.table.basic 的 optional_modules 分散在基础配方中，缺少显式表达"增删改查一站式"的 recipe。

**region_order**：
```
page-header > filter-bar > table-toolbar > data-table > pagination
```

**required_regions**：`page-header;filter-bar;table-toolbar;data-table;pagination`

**optional_modules**：`modal-functional;drawer-basic;detail-drawer;confirm-modal;batch-action-footer;empty-state;table-column-settings`

**forbidden_patterns**：不得把新增/编辑做成独立页面跳转

**关键词**：CRUD、弹窗编辑、页面内闭环、行内操作

**priority**：90

---

## 不变更内容

- 不新增 region/module HTML 文件（所需积木已存在）
- 不新增 support CSS
- 不删除任何物理文件（HTML/CSS 保留，只切 CSV 入口）
- 不修改 `asset-rules.csv` 中的规则
- 不修改 `search_content_assets.py`
- 不修改 SKILL.md 装配流程
- 登录页、个人中心暂不纳入

---

## 涉及文件

### Part 1 — 移除

| 文件 | 操作 |
|------|------|
| `data/content-assets/content-assets.csv` | 删除 component-combos/feedback/overlays 的行 |
| `data/content-assets/asset-keywords.csv` | 删除关联 keywords 行 |
| `data/content-assets/recipe-asset-map.csv` | 删除关联映射行 |

### Part 2 — 补充

| 文件 | 操作 |
|------|------|
| `data/content-assets/recipe-rules.csv` | 新增 4 行 recipe |
| `data/content-assets/recipe-asset-map.csv` | 新增对应资产映射（form-summary-card / tabs / tab-panel-* / multi-section-form / dynamic-form-list 等已存在于 content-assets.csv） |
| `references/layouts.md` | 补充新 recipe 的布局说明 |

---

## 验证方式

### Part 1 验证

1. 运行 `python scripts/search_content_assets.py "弹窗编辑"` → CONTENT_ASSET_DECISION 中不出现 `combo-`、`feedback-`、`OV_` 前缀资产
2. 运行 `python scripts/search_content_assets.py "批量操作表格页"` → 仍能正常命中 `recipe.table.basic`，required_assets 无缺失

### Part 2 验证

1. `python scripts/search_content_assets.py "高级表单多分组动态字段"` → 命中 `recipe.form.advanced`
2. `python scripts/search_content_assets.py "多Tab详情查看"` → 命中 `recipe.detail.tabs`
3. `python scripts/search_content_assets.py "弹窗编辑列表增删改查"` → 命中 `recipe.table.crud`
4. 所有 recipe 的 `required_assets` 中 `html_path` 指向的文件真实存在
