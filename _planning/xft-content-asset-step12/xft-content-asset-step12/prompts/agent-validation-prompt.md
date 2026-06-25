# 给 Codex / Agent 的验证提示词

请执行第 12 步验收，不要继续改造功能。

先读取：

```text
_planning/xft-content-asset-step12/references/step12-validation-and-gap-fill.md
_planning/xft-content-asset-step12/checklists/post-execution-acceptance.md
```

然后执行：

```bash
bash _planning/xft-content-asset-step12/scripts/run_step12_validation.sh
```

要求：

1. 只做验收和问题记录。
2. 不要修改 `tokens.css`。
3. 不要修改 shell 主结构。
4. 不要新增无来源资产。
5. 如果验证失败，先输出失败原因和修复建议，不要继续扩展功能。
6. 最终按以下格式汇报：

```text
验证结论：通过 / 不通过
阻断问题：
非阻断问题：
通过的测试用例：
失败的测试用例：
需要人工确认的问题：
下一步建议：
```
