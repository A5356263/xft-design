# `route_nav_bar（路径任务导航区）`

## 语义职责

任务上下文追踪与切换，用于帮助用户理解当前所处页面、任务路径或活跃页签。

## 允许的 `block pattern（语义块模式）`

- `tab_navigation（页签导航块）`
- `breadcrumb_navigation（面包屑导航块）`
- `context_switcher（上下文切换块）`

## 默认 / 可选组合

- 默认：`tab_navigation（页签导航块）` 或 `breadcrumb_navigation（面包屑导航块）`
- 可选：`context_switcher（上下文切换块）`

## 不建议放入的内容

- 记录筛选
- 主动作入口
- 记录表格
