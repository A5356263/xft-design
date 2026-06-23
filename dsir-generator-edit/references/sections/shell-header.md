# `shell_header（全局页头区）`

## 语义职责

全局环境识别与系统级工具入口，不直接承载页面内业务执行。

## 允许的 `block pattern（语义块模式）`

- `branding_bar（标识块）`
- `project_switcher（项目切换块）`
- `global_search（全局搜索块）`
- `utility_actions（系统工具块）`
- `user_profile（用户入口块）`
- `primary_nav_horizontal（水平主导航块）`

## 默认 / 可选组合

- 默认：`branding_bar + global_search + utility_actions + user_profile`
- 可选：`project_switcher`、`primary_nav_horizontal`

## 不建议放入的内容

- 页面内筛选
- 记录结果展示
- 局部业务主动作
