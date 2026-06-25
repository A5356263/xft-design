# generic profile

用于默认内部 DSIR projection。

约束：
- 保留 richer semantic payload
- 允许使用本 Skill 的 page family / section / block / content model 词表
- 目标是让下游代码智能体或其他设计语义消费者理解设计意图
- 不要求对齐 GenUX 当前 compile-facing contract
- 不改变 `design-spec.md` 的表达

适用场景：
- 独立使用本 Skill
- 需要更丰富的 design semantic authoring 结果
- 下游不直接使用当前 GenUX 编译主线

输出说明：
- generic profile 只影响内部 DSIR 推导与校验
- 不输出 generic `dsir.json` 文件
