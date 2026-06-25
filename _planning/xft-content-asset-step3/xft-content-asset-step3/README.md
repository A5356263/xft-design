# XFT Content Asset Step 3：页面配方定义

本包是第 3 步产物：把素材中的典型页面与 B 端页面结构，转成可检索、可装配的页面配方。

## 文件说明

- `data/page-recipes.csv`：页面配方主表。定义每类页面的默认区域顺序、必选区域、可选模块、禁用组合。
- `data/recipe-asset-map.csv`：页面配方与后续资产的映射表。用于后续生成 region/module/component-combo 资产。
- `data/page-type-router.csv`：页面类型路由表。用于从用户需求判断 page_type 与 recipe_id。
- `references/page-recipes.md`：页面配方说明，给人和 Agent 阅读。
- `references/recipe-selection-rules.md`：页面配方选择规则，后续会进入 SKILL.md。
- `references/ant-design-pro-asset-alignment.md`：说明哪些配方借鉴了 ant-design-pro 的页面资产形态，但不复制其代码。

## 当前阶段怎么用

当前包请先放入 `_planning/xft-content-asset-step3/`，不要直接覆盖 `.claude/skills/xft-design/`。

本包还不是最终可执行改造包。后续第 4~8 步会继续补：区域资产、模块资产、HTML 片段、检索数据表。
