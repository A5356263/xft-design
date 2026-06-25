# Skill 工作流改造说明

## 改造目标

把原来的“壳子 + 页面块 + AI 填内容”改成“壳子 + 页面配方 + 内容资产检索 + HTML 装配”。

## 新旧差异

| 项目 | 旧流程 | 新流程 |
|---|---|---|
| 页面主体 | page-blocks.html 大块 | page recipe（页面配方）+ 多个内容资产 |
| 内容生成 | AI（人工智能）根据指南写 | AI（人工智能）按检索结果装配 |
| 关键决策 | ROUTE_DECISION | ROUTE_DECISION + CONTENT_ASSET_DECISION |
| 资产读取 | 按页面类型读大文件 | 只读命中资产 |
| 风险 | 页面结构漂移 | 资产缺失时可控降级 |

## 主流程

```text
1. 需求结构化
2. 输出 ROUTE_DECISION（路由决策）
3. 调用或参考 search_content_assets.py（内容资产检索脚本）
4. 输出 CONTENT_ASSET_DECISION（内容资产决策）
5. 条件读取 shell、token、components、support CSS、HTML 资产
6. 按 order 装配
7. 替换业务字段和文案
8. 校验
9. 输出最终 HTML
```

## 重要结论

`SKILL.md` 应成为流程控制文件，不再承载大量具体设计规则。具体规则进入：

- `data/*.csv`
- `assets/**/*.html`
- `references/*.md`
- `scripts/*.py`
