# 条件读取协议

## 目标

减少 AI（人工智能）一次性读取太多资料导致混乱。

## 读取顺序

1. `SKILL.md`
2. `data/page-type-router.csv`
3. `scripts/search_content_assets.py` 输出结果
4. `design-systems/USAGE.md`
5. `design-systems/tokens.css`
6. `design-systems/components.html`
7. 当前 shell（壳子）
8. 命中的 support CSS（补充样式）
9. 命中的 HTML（超文本标记语言）资产

## 禁止读取

| 类型 | 说明 |
|---|---|
| archive（归档）示例 | 不得继承历史布局 |
| 未命中资产 | 不得偷看后再拼 |
| 无关 shell | 避免混入其他壳子结构 |
| 全量 assets | 避免模型自由选择 |
