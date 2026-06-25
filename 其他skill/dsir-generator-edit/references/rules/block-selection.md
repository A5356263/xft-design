# `block selection（语义块选择）` 规则

## 基本原则

`block pattern（语义块模式）` 是页面内可复用的语义实现单元，不是组件名，不是视觉样式名。

## 选择顺序

按下面顺序判断：
1. `page goal（页面目标）`
2. `section role（区域职责）`
3. `content model（内容模型）`
4. `interaction hints（交互提示）`

## 首批常用 `block pattern（语义块模式）`

- `filter_form（筛选表单块）`
- `action_cluster（动作集合块）`
- `local_primary_action（局部主动作块）`
- `record_table（记录表格块）`
- `pagination_footer（分页底部块）`
- `view_switcher（视图切换块）`
- `metric_group（指标组块）`
- `category_tree（分类树块）`

## 动作类判断

- 一组动作，内部存在主次关系：`action_cluster（动作集合块）`
- 一个局部范围内只有一个独立且显著的主动作入口：`local_primary_action（局部主动作块）`

不要因为最终渲染成一个按钮，就把它降成组件级问题。
