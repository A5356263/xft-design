# 问题分类与处理策略

## A 类：路径/放置问题

表现：文件不存在、脚本找不到 CSV、read_order 路径无效。

优先处理：是。

处理方式：
- 对照 `_planning/xft-content-asset-step11/references/file-placement-map.md`。
- 不要修改资产内容，只修路径和复制位置。

## B 类：检索命中问题

表现：页面类型选错、模块漏选、低相关资产排在前面。

处理方式：
- 优先改关键词表。
- 其次改规则表。
- 最后才改脚本权重。

## C 类：装配问题

表现：HTML 片段插错位置、overlay 放进内容区、状态资产替换了整页。

处理方式：
- 查 `CONTENT_ASSET_DECISION.read_order`。
- 检查 `slot` 和 `insert_after` 规则。
- 修装配协议，不要让 AI 自由判断位置。

## D 类：视觉/样式问题

表现：间距不对、样式缺失、class 不生效。

处理方式：
- 先确认 support CSS 是否被引入。
- 不要改 token。
- 不要改 shell。
- 必要时补 `_support.css`。

## E 类：架构偏离问题

表现：Agent 跳过检索、直接写页面、随机生成 class。

处理方式：
- 这是阻断问题。
- 先修 SKILL.md 工作流和禁止事项。
- 暂停新增资产。
