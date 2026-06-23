# `sidebar（侧边区域）`

## 语义职责

页面内的范围锁定、局部导航、辅助上下文或局部入口区，不是主结果区。

## 允许的 `block pattern（语义块模式）`

- `category_tree（分类树块）`
- `nav_menu_local（局部导航菜单块）`
- `facet_scope_panel（维度范围块）`
- `local_primary_action（局部主动作块）`

## 默认 / 可选组合

- 默认：`category_tree（分类树块）` 或 `nav_menu_local（局部导航菜单块）`
- 可选：`facet_scope_panel（维度范围块）`、`local_primary_action（局部主动作块）`

## 关键规则

- `local_primary_action（局部主动作块）` 默认作为 `sibling block（同级语义块）`
- 不要默认把局部新增入口并入 `category_tree（分类树块）`
- 若树节点自身带动作能力，应优先表达为 `category_tree（分类树块）` 的 `capability（能力）`，而不是树外入口

## 不建议放入的内容

- `record_table（记录表格块）`
- `pagination_footer（分页底部块）`
- 多个主次动作并存的完整动作集合
