# `category_tree（分类树块）`

## 定义

通过树形结构帮助用户切换局部范围、锁定内容区范围、在层级结构内定位内容。

## 语义目标

- 表达层级分类
- 表达范围锁定
- 表达树形局部导航

## 允许出现的区域

- `sidebar（侧边区域）`

## 最小语义载荷

- `tree_scope（树范围）`
- `node_kind（节点类型）`
- `selection_goal（选择目标）`

## 使用的 `content model（内容模型）`

- `hierarchical_options（层级选项）`

## 能力范围

- `hierarchical_scope_switching（层级范围切换）`
- `single_selectable（单选）`
- `multi_selectable（多选）`
- `expandable（可展开）`
- `node_context_awareness（节点上下文感知）`
- `node_action_capable（节点动作能力）`

## 已确认变体

- 当前首批不单独定义固定变体

## 不应混入的内容

- 树外独立新增入口
- 树外导入入口
- 树外帮助说明

## 常见搭配

- `local_primary_action（局部主动作块）`
- `context_note（说明块）`
