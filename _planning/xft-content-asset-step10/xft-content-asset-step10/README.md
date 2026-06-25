# XFT 内容资产 Skill 工作流改造草案｜第 10 步

本包用于重写 `xft-design` 的 Skill（技能）工作流。

## 本步定位

这一步产出的是：

- 新版 `SKILL.md` 草案
- `ROUTE_DECISION`（路由决策）协议
- `CONTENT_ASSET_DECISION`（内容资产决策）协议
- 条件读取规则
- HTML（超文本标记语言）装配规则
- 最终校验规则
- 禁止行为清单

## 当前使用方式

请先放入：

```text
项目根目录/_planning/xft-content-asset-step10/
```

暂时不要让 Agent（智能体）执行替换。

原因：第 11 步还会输出 Codex（代码助手）可执行改造文档，统一说明哪些文件复制到 `.claude/skills/xft-design/`，哪些文件只作为参考。

## 核心变化

旧流程：

```text
需求 → 路由 → 壳子 → 页面块 → 填内容
```

新流程：

```text
需求结构化
→ ROUTE_DECISION（路由决策）
→ 页面配方选择
→ CONTENT_ASSET_DECISION（内容资产决策）
→ 条件读取命中资产
→ HTML 装配
→ 校验
```

## 本包文件

```text
SKILL.v7.content-asset-workflow.draft.md
references/skill-workflow-refactor.md
references/content-asset-decision-protocol.md
references/conditional-read-protocol.md
references/html-assembly-protocol.md
references/final-check-protocol.md
references/route-to-asset-decision-map.md
references/codex-notes-step10.md
data/skill-phase-checklist.csv
data/conditional-read-map.csv
data/disallowed-behaviors.csv
examples/ROUTE_DECISION.table-page.example.md
examples/CONTENT_ASSET_DECISION.table-page.example.json
examples/CONTENT_ASSET_DECISION.approval-detail.example.json
```
