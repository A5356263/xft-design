# 第 12 步：验证与补齐说明

## 目标

验证第 11 步执行后，`xft-design` 是否真正从“指南驱动”变成“内容资产检索与装配驱动”。

## 验证顺序

```text
目录存在性
→ 数据表存在性
→ 检索脚本可运行
→ CONTENT_ASSET_DECISION 可输出
→ read_order 路径真实存在
→ 生成 HTML 是否使用资产片段
→ 是否存在自由拼布局
→ 缺口登记
```

## 必须通过的硬标准

1. `SKILL.md` 必须包含 `CONTENT_ASSET_DECISION`。
2. `.claude/skills/xft-design/assets/content-assets/` 必须存在六类资产目录。
3. `.claude/skills/xft-design/data/content-assets/content-assets.csv` 必须存在。
4. `.claude/skills/xft-design/scripts/search_content_assets.py` 必须可运行。
5. 至少 8 条测试需求能返回 JSON 决策。
6. 返回结果中的 `read_order` 路径必须真实存在。
7. 生成页面时不得跳过资产决策。
8. 不得改 `tokens.css`。
9. 不得改 shell 主结构。
10. 不得把旧 `page-blocks.html` 继续作为主路径。

## 问题处理原则

### 轻微问题

例如关键词命中不准、资产优先级不合适。
处理：改 `asset-keywords.csv`、`asset-rules.csv` 或排序权重。

### 中等问题

例如页面配方选对了，但缺少模块。
处理：补 `recipe-asset-map.csv` 或新增模块资产。

### 严重问题

例如没有 `CONTENT_ASSET_DECISION` 就开始生成 HTML。
处理：停止扩展，回退 Skill 工作流修改，先修 SKILL.md。

### 架构问题

例如 Agent 仍然自由写大量新 class。
处理：强化禁止规则和校验脚本，不要继续堆更多模板。

## 验收输出

Agent 完成后必须给出：

```text
1. 目录检查结果
2. 数据表检查结果
3. 检索测试结果
4. read_order 路径检查结果
5. 生成页面样例路径
6. 发现的问题列表
7. 是否满足验收标准
```
