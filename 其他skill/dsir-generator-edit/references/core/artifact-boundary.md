# artifact-boundary

## 边界

- `design plan`：上游输入，可不完整，可混合需求、草图、上下文与约束
- `design-spec.md`：human-facing 结构化设计说明，用于评审、解释与讨论
- `DSIR`：machine-facing 结构化设计语义，用于内部机器消费、校验与投影
- `Proto Spec`：下游 compile 产物，不是本 Skill 输出

## 原则

- `design-spec.md` 不应被 machine-prep 结构淹没
- `design-spec.md` 不按 `generic / genux-compile` 分版本
- `DSIR` 可以有 profile，但 profile 只能改变内部投影，不得回写 core
- `genux-compile` 只是一种 compile-facing projection，不是 Skill 本体
- 当前 Skill 默认不输出 `dsir.json` 文件
