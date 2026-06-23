# `local_primary_action（局部主动作块）`

## 定义

用于表达一个局部范围内唯一且最突出的主动作入口。

## 语义目标

- 在局部范围内提供明确主动作
- 强调当前区域或容器的首要入口
- 避免把单个显著动作错误并入完整动作集合

## 允许出现的区域

- `sidebar（侧边区域）`
- `primary_content（主内容区）`
- 其他存在明确局部作用域的 `section（区域）` 或容器上下文

## 最小语义载荷

- `action_label（动作名称）`
- `action_goal（动作目标）`
- `action_scope（动作作用范围）`

## 使用的 `content model（内容模型）`

- `single_primary_action（单一主动作）`

## 能力范围

- `prominent_entry（显著入口）`
- `context_bound（绑定局部上下文）`
- `selection_independent（不依赖列表选中）`
- `single_primary_action（单一主动作）`

## 已确认变体

- 当前首批不单独定义固定变体

## 不应混入的内容

- 多个主次动作并存的集合
- 记录表格内部行操作
- 只因最终渲染成一个按钮就被降为组件级表达

## 常见搭配

- `category_tree（分类树块）`
- `nav_menu_local（局部导航菜单块）`
- `record_table（记录表格块）` 的外层局部容器
- `metric_group（指标组块）` 的外层局部容器
