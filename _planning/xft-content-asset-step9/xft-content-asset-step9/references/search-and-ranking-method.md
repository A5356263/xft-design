# XFT 内容资产检索与排序方法

## 目标

把用户需求转换成可执行的资产决策：

```text
需求
→ 页面类型路由
→ 页面配方选择
→ 必选资产补齐
→ 可选资产检索
→ 规则过滤/排序
→ CONTENT_ASSET_DECISION
```

核心原则：**AI 只判断选哪个资产，不现场发明布局。**

## 1. 页面类型路由

读取：`data/page-type-router.csv`

输入：用户需求。

输出：

- `page_type`
- `recipe_id`
- `scope`
- `shell`
- `page_block`

判断逻辑：

1. 用 `match_keywords` 做关键词召回。
2. 命中 `negative_keywords` 时强降权。
3. 多个命中时按 `priority` 排序。
4. 没有命中时回退 `TablePage + recipe.table.basic`。

## 2. 页面配方选择

读取：`data/recipe-rules.csv`

输入：用户需求 + `page_type` + 路由推荐 `recipe_id`。

输出：一个 `recipe`。

判断逻辑：

1. 只在当前 `page_type` 内检索。
2. 用 `recipe_name / keywords / required_regions / optional_modules` 做匹配。
3. 路由推荐的 `recipe_id` 有轻微优先级。
4. 配方负责决定默认区域顺序和必选资产。

## 3. 必选资产补齐

读取：`data/recipe-asset-map.csv`

输入：`recipe_id`。

输出：必选资产列表。

规则：

- 必选资产不依赖关键词分数。
- 配方里 required=true 的资产必须进入结果。
- 如果资产文件缺失，标记 `unsupported`，不得现场发明。

## 4. 可选资产检索

读取：`data/content-assets.csv`

输入：用户需求 + 当前 `page_type`。

输出：可选资产列表。

匹配字段：

- `asset_name`
- `keywords`
- `conditions`
- `validation`
- `notes`

规则：

- 可选资产必须有关键词或规则命中。
- 可选资产不能覆盖必选资产。
- 命中 `forbidden_when` 时强降权。
- 默认最多返回 8 个。

## 5. 规则过滤与排序

读取：`data/asset-rules.csv`

输入：用户需求 + page_type + 已选资产。

输出：命中的规则列表。

规则类型包括：

- 组合规则
- 禁用规则
- 插入位置规则
- 校验规则

规则只做约束，不直接生成 HTML。

## 6. 输出结构

最终必须输出：

```text
CONTENT_ASSET_DECISION
```

内容包括：

- 页面类型
- 页面配方
- 壳子
- 必选资产
- 可选资产
- CSS 支持文件
- 命中规则
- unsupported 缺口
- 硬校验

## 7. 禁止事项

- 不得跳过资产决策直接写 HTML。
- 不得一次读取全部资产 HTML。
- 不得自造区域布局类名。
- 不得把缺失资产临时编出来。
- 不得让可选资产破坏页面配方顺序。
