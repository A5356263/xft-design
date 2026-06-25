# 检索接入说明

第 8 步只生成统一数据表，还不改项目。

后续第 9 步会基于这些表设计检索与排序逻辑，建议流程：

```text
用户需求
→ page-type-router.csv 判断 page_type / recipe_id
→ recipe-rules.csv 确定默认区域顺序
→ recipe-asset-map.csv 得到必选/可选资产候选
→ content-assets.csv + asset-keywords.csv 做关键词召回
→ asset-rules.csv 做规则过滤与校验
→ 输出 CONTENT_ASSET_DECISION
→ 按 html_path 读取资产片段装配
```

## 不允许

- 不允许只读规则后让 AI 自己重写布局。
- 不允许跳过页面配方直接拼资产。
- 不允许命中不到资产时现场创造新布局。
- 不允许把 overlay 插入内容区，应使用 OVERLAY_SLOT。

## 缺资产处理

缺资产时只能选择：

1. 使用同页面类型的通用资产；
2. 标记 unsupported；
3. 在后续资产补齐清单中新增需求。
