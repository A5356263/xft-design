# XFT 内容资产系统改造：Codex 执行文档

> 用途：把第 3～10 步产出的内容资产、检索数据、检索脚本、Skill（技能）工作流，正式接入 `xft-design` 项目。
>
> 执行对象：Codex（代码助手）/ Agent（智能体）。
>
> 重要原则：不要自由重构项目；只按本文档接入内容资产系统。

---

## 0. 执行前提

请确认项目根目录下已经放好这些 planning（规划）目录：

```text
_planning/
  xft-content-asset-step1/
  xft-content-asset-step2-enhanced/
  xft-content-asset-step3/
  xft-content-asset-step4/
  xft-content-asset-step5/
  xft-content-asset-step6/
  xft-content-asset-step7/
  xft-content-asset-step8/
  xft-content-asset-step9/
  xft-content-asset-step10/
```

如果缺任意目录，先停止，不要改 `.claude/skills/xft-design/`。

---

## 1. 总目标

把当前 `xft-design` 从：

```text
需求 → 路由 → 壳子 → 页面块 → AI 自由填内容
```

改成：

```text
需求结构化
→ ROUTE_DECISION（路由决策）
→ 页面配方选择
→ 内容资产检索
→ CONTENT_ASSET_DECISION（内容资产决策）
→ 条件读取命中资产
→ HTML（超文本标记语言）装配
→ 最终校验
```

核心变化：

```text
不让 AI 现场想布局
只让 AI 选择资产、填业务内容、做装配
```

---

## 2. 目标目录结构

在 `.claude/skills/xft-design/` 下新增以下结构：

```text
.claude/skills/xft-design/
  assets/
    content-assets/
      regions/
      modules/
      feedback/
      states/
      overlays/
      component-combos/
      _support/
  data/
    content-assets/
  references/
    content-assets/
  examples/
    content-decisions/
  scripts/
    search_content_assets.py
```

说明：

- 原有 `assets/shells/` 保留。
- 原有 `assets/page-blocks.html` 暂时保留，但降级为 fallback（兜底）参考，不再作为主生成方式。
- 新增资产全部放在 `assets/content-assets/`，避免和现有壳子、旧页面块混在一起。

---

## 3. 文件复制任务

### 3.1 区域资产

从：

```text
_planning/xft-content-asset-step4/assets/regions/
```

复制到：

```text
.claude/skills/xft-design/assets/content-assets/regions/
```

将：

```text
_planning/xft-content-asset-step4/assets/regions/_region-support.css
```

复制到：

```text
.claude/skills/xft-design/assets/content-assets/_support/region-support.css
```

---

### 3.2 模块资产

从：

```text
_planning/xft-content-asset-step5/assets/modules/
```

复制到：

```text
.claude/skills/xft-design/assets/content-assets/modules/
```

将：

```text
_planning/xft-content-asset-step5/assets/modules/_module-support.css
```

复制到：

```text
.claude/skills/xft-design/assets/content-assets/_support/module-support.css
```

---

### 3.3 状态、反馈、覆盖层资产

复制：

```text
_planning/xft-content-asset-step6/assets/feedback/
→ .claude/skills/xft-design/assets/content-assets/feedback/

_planning/xft-content-asset-step6/assets/states/
→ .claude/skills/xft-design/assets/content-assets/states/

_planning/xft-content-asset-step6/assets/overlays/
→ .claude/skills/xft-design/assets/content-assets/overlays/
```

将：

```text
_planning/xft-content-asset-step6/assets/feedback/_feedback-support.css
```

复制到：

```text
.claude/skills/xft-design/assets/content-assets/_support/feedback-support.css
```

---

### 3.4 组件组合资产

从：

```text
_planning/xft-content-asset-step7/assets/component-combos/
```

复制到：

```text
.claude/skills/xft-design/assets/content-assets/component-combos/
```

将：

```text
_planning/xft-content-asset-step7/assets/component-combos/_component-combo-support.css
```

复制到：

```text
.claude/skills/xft-design/assets/content-assets/_support/component-combo-support.css
```

---

### 3.5 统一检索数据

从：

```text
_planning/xft-content-asset-step8/data/
```

复制到：

```text
.claude/skills/xft-design/data/content-assets/
```

必须包含：

```text
content-assets.csv
asset-keywords.csv
asset-rules.csv
recipe-rules.csv
page-type-router.csv
recipe-asset-map.csv
asset-source-map.csv
support-css-manifest.csv
package-stats.json
```

---

### 3.6 检索脚本

从：

```text
_planning/xft-content-asset-step9/scripts/search_content_assets.py
```

复制到：

```text
.claude/skills/xft-design/scripts/search_content_assets.py
```

从：

```text
_planning/xft-content-asset-step9/_tests/run_search_smoke_tests.sh
```

复制到：

```text
.claude/skills/xft-design/scripts/run_search_smoke_tests.sh
```

复制后执行：

```bash
chmod +x .claude/skills/xft-design/scripts/run_search_smoke_tests.sh
```

---

### 3.7 工作流参考文档

从：

```text
_planning/xft-content-asset-step10/references/
```

复制到：

```text
.claude/skills/xft-design/references/content-assets/
```

从：

```text
_planning/xft-content-asset-step10/examples/
```

复制到：

```text
.claude/skills/xft-design/examples/content-decisions/
```

---

## 4. SKILL.md 改造任务

### 4.1 直接改写现有文件

本次执行不要求备份旧 `SKILL.md`。

要求：

1. 直接在 `.claude/skills/xft-design/SKILL.md` 上改写。
2. 不保留 `references/legacy/` 目录作为本次改造目标。
3. 旧 `SKILL.md` 内容只作为当前项目现状参考，不作为交付产物保留要求。

### 4.2 用新工作流草案替换主流程

将：

```text
_planning/xft-content-asset-step10/SKILL.v7.content-asset-workflow.draft.md
```

作为新 `SKILL.md` 的主体。

注意：

1. 保留原 `SKILL.md` 顶部 YAML（配置块）中的 `name`、`triggers`、`od` 基础信息。
2. 将 `version` 更新为 `7.0`。
3. 描述改为：

```text
Generate enterprise admin web prototypes through route decision, content asset retrieval, conditional reads, and HTML assembly.
```

4. 正文必须包含以下章节：

```text
Stable Flow
Route Decision Record
Content Asset Decision
Conditional Reads
HTML Assembly
Output Contract
Final Check
Disallowed Behaviors
Fallback Rules
```

### 4.4 执行进度记录

执行过程中必须持续更新：

```text
_planning/xft-content-asset-step11/EXECUTION-PROGRESS.md
```

最少记录：

1. 当前任务编号 / 名称
2. 当前总完成度
3. 本任务已完成的具体事项
4. 当前阻塞或风险
5. 下一步动作

### 4.3 主流程必须使用 CONTENT_ASSET_DECISION

新 `SKILL.md` 必须明确：

```text
没有 CONTENT_ASSET_DECISION，不得读取内容资产 HTML，不得生成主体页面。
```

`CONTENT_ASSET_DECISION` 至少包含：

```json
{
  "page_type": "TablePage",
  "recipe_id": "table-basic",
  "required_assets": [],
  "optional_assets": [],
  "support_css": [],
  "unsupported": [],
  "read_order": []
}
```

---

## 5. 检索脚本接入规则

### 5.1 推荐命令

在 skill 目录内测试：

```bash
cd .claude/skills/xft-design
python3 scripts/search_content_assets.py "生成员工花名册列表页，支持筛选、批量导出和详情查看" --data-dir data/content-assets --pretty
```

预期：

- 返回 `page_type`。
- 返回 `recipe_id`。
- 返回 `required_assets`。
- 返回 `read_order`。
- 不应返回空资产。

### 5.2 不允许的做法

禁止：

```text
AI 直接读所有 assets/content-assets 文件
AI 不经过脚本直接猜资产
AI 在没有命中资产时自造布局
AI 修改 tokens.css 中的 token 名称
AI 改 shell 的结构来适配内容区
```

---

## 6. CSS（层叠样式表）接入规则

页面生成时 CSS 顺序必须保持：

```text
第 1 个 style：tokens.css 原文
第 2 个 style：shell 原有 style
第 3 个 style：components.html 中组件 CSS
第 4 个 style：命中资产所需 support CSS
第 5 个 style：页面级最小补充 CSS，可选
```

禁止：

- 把 support CSS 合并进 tokens.css。
- 在 HTML 片段里写大量 inline style（行内样式）。
- 用新的随机 class（类名）覆盖现有视觉体系。

---

## 7. 校验任务

### 7.1 检索测试

执行：

```bash
cd .claude/skills/xft-design
python3 scripts/search_content_assets.py "生成员工花名册列表页，支持筛选、批量导出和详情查看" --data-dir data/content-assets --pretty
python3 scripts/search_content_assets.py "生成审批详情页，包含审批流、基础信息和操作记录" --data-dir data/content-assets --pretty
python3 scripts/search_content_assets.py "生成公式编辑器配置页，包含公式编辑和智能辅助" --data-dir data/content-assets --pretty
```

通过标准：

- 3 条命令均返回合法 JSON（数据格式）。
- 至少包含一个页面配方。
- 至少返回 3 个资产路径。
- `unsupported` 可以存在，但不能替代核心资产。

### 7.2 产物校验

如果原项目已有：

```text
scripts/check_skill_output.py
```

需要扩展它，至少校验：

```text
XFT_ROUTE 是否存在
CONTENT_ASSET_DECISION 是否存在
support_css 是否真实存在
read_order 中的 html_path 是否真实存在
最终 HTML 是否包含 PAGE_CONTENT_SLOT / CONTENT_SLOT 未替换残留
最终 HTML 是否出现禁止 class 前缀 custom/new/random
```

如果暂时不扩展脚本，必须在 `references/content-assets/final-check-protocol.md` 中手工校验。

---

## 8. 验收标准

本次改造完成后，应满足：

| 验收项 | 标准 |
|---|---|
| 目录完整 | `assets/content-assets/`、`data/content-assets/`、`scripts/search_content_assets.py` 存在 |
| 检索可运行 | 3 条测试需求能返回资产决策 |
| 工作流已替换 | `SKILL.md` 包含 `CONTENT_ASSET_DECISION` |
| 旧能力未破坏 | shell、tokens、components 仍按原顺序注入 |
| 禁止自由布局 | 文档明确禁止未命中资产时自造布局 |
| 素材可追踪 | `asset-source-map.csv` 保留素材来源 |

---

## 9. 推荐提交信息

```text
feat(skill): add content asset retrieval and assembly workflow
```

---

## 10. 执行完成后反馈给用户

完成后只汇报：

```text
已完成内容资产系统接入：
1. 新增 assets/content-assets
2. 新增 data/content-assets
3. 新增 search_content_assets.py
4. 重写 SKILL.md 为 v7 工作流
5. 检索测试通过/未通过
6. 如未通过，列出具体错误文件和错误原因
```

不要汇报大段过程，不要描述无关实现细节。
