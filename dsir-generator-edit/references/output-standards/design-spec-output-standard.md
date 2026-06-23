# design-spec 输出标准

`design-spec.md` 必须是 human-facing、结构化、可评审的设计说明。

## 推荐结构

1. 页面语义摘要
2. 主任务
3. 区域与语义块
4. 内容模型
5. 关键状态与交互提示
6. 设计判断与待确认项

## 必须遵守

- 不输出 `page_shell_specs / region_specs / module_specs / state_specs / interaction_specs` 这类 machine-prep 分段
- 不伪装成 compile 输入
- 可以结构化，但要让人一眼看懂页面目标、区域职责和关键判断
- `design-spec.md` 不区分 `generic / genux-compile` 版本
- 不因内部 DSIR projection 差异而改写成人机混合稿
- 默认只输出本文件，不附带 `dsir.json`

## 允许表达

- 关键假设
- 待确认项
- 低风险保守补全

## 不应表达

- 组件树
- renderer 节点
- preset / manifest 私有实现
- 仅为 compile 服务的 payload 细节
