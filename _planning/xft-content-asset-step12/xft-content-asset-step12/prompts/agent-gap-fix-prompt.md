# 给 Codex / Agent 的补齐修复提示词

你现在只处理第 12 步验收发现的问题，不要扩大改造范围。

请读取：

```text
_planning/xft-content-asset-step12/_reports/gap-backlog-template.csv
_planning/xft-content-asset-step12/references/issue-classification.md
```

修复规则：

1. A 类路径问题：只修复制位置或路径拼接。
2. B 类检索问题：优先改关键词/规则数据，不要先改脚本。
3. C 类装配问题：修 slot / read_order / 装配协议。
4. D 类样式问题：优先确认 support CSS 是否引入。
5. E 类架构偏离：停止其他修复，先修 SKILL.md 工作流。

禁止：

- 禁止重写 shell。
- 禁止改 token。
- 禁止删除旧资产。
- 禁止自由新增无来源模板。
- 禁止把图片素材直接放进 skill 让 AI 自己读。
