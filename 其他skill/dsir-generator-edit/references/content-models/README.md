# `content model（内容模型）` 使用说明

`content model（内容模型）` 用于定义 `block（语义块）` 承载的信息结构原语。

它回答的问题是：
- 这里承载什么类型的信息
- 最少需要哪些信息角色
- 哪些信息项可选
- 哪些状态或角色需要被区分

它不回答的问题是：
- 用什么组件实现
- 具体文案是什么
- 具体参数怎么写
- 最终如何排版渲染

组织原则：
- `page family（页面族）` 不拥有 `content model（内容模型）`
- `section（区域）` 不拥有 `content model（内容模型）`
- `block（语义块）` 使用 `content model（内容模型）`
- `content model（内容模型）` 自身独立定义，供多个 `block（语义块）` 复用
