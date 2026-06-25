# 可直接粘贴给 Codex / Agent 的执行提示词

你现在要改造 `xft-design` Skill（技能），不要自由发挥。

请先读取：

```text
_planning/xft-content-asset-step11/CODEX-XFT-CONTENT-ASSET-REFACTOR.md
```

然后严格按文档执行。

执行约束：

1. 不要一次性重构整个项目。
2. 不要修改 `tokens.css` 的 token（令牌）名称和值。
3. 不要改写 `assets/shells/` 的壳子结构。
4. 不要删除旧 `assets/page-blocks.html`，只把它降级为 fallback（兜底）。
5. 直接改写现有 `SKILL.md`，不要求备份旧文件。
6. 必须新增 `CONTENT_ASSET_DECISION` 工作流。
7. 必须接入 `scripts/search_content_assets.py`。
8. 必须跑 3 条检索测试。
9. 如果测试失败，不要继续扩展功能；先修复数据路径或脚本路径。
10. 完成后按文档第 10 节格式汇报。
11. 每完成一个任务，必须同步更新 `_planning/xft-content-asset-step11/EXECUTION-PROGRESS.md`。
