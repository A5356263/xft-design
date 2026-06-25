# Step 9 接入说明

## 当前状态

本包是“检索与排序方法包”。它已经包含：

- 可运行的检索原型：`scripts/search_content_assets.py`
- 统一资产数据：`data/*.csv`
- 检索字段权重和冲突规则
- CONTENT_ASSET_DECISION 输出格式说明

## 现在是否让 Agent 执行？

暂时不要。

原因：第 10 步还要重写 `SKILL.md` 工作流。  
如果现在让 Agent 接入，会出现“有脚本但主工作流还不会调用”的半成品状态。

## 当前你应该怎么做

下载本包后放到：

```text
项目根目录/_planning/xft-content-asset-step9/
```

## 第 10 步之后再执行什么

第 10 步完成后，再让 Agent 依据第 9 + 第 10 步文档执行：

1. 将 `data/*.csv` 放入 `.claude/skills/xft-design/data/`。
2. 将 `scripts/search_content_assets.py` 放入 `.claude/skills/xft-design/scripts/`。
3. 改写 `SKILL.md`，加入 CONTENT_ASSET_DECISION 流程。
4. 校验脚本输出和 SKILL 工作流一致。
