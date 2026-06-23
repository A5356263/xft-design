# `DSIR（设计语义中间表示）` 内部标准

本 Skill 支持两种内部 DSIR 视角：

- `generic`：默认 richer semantic authoring 结果
- `genux-compile`：面向当前 GenUX compile 主线的更严格投影

## 作用

DSIR 是 Skill 的 machine-facing 内部语义结果，用于：
- 统一语义建模后的机器表达
- 约束内部一致性校验
- 服务下游机器消费准备
- 支撑 compile-facing projection 对齐

说明：
- DSIR 在当前 Skill 中默认不作为文件输出
- `design-spec.md` 才是默认外部产物

## generic internal dsir 最小结构

顶层至少包含：
- `project（项目）`
- `shared_context（共享上下文）`
- `pages（页面集合）`

每个页面至少表达：
- `page_id`
- `page_type`
- `page_goal`
- `target_actor`
- `primary_tasks`
- `layout_mode`
- `review_criteria`

每个 `section（区域）` 至少表达：
- `section_id`
- `section_role`
- `priority`
- `placement_preference`

每个 `block（语义块）` 至少表达：
- `block_id`
- `block_pattern`
- `semantic_payload.content_model_ref`
- `semantic_payload.instance_payload`
- `presentation_preference`

## genux-compile internal projection

如果目标是让当前 GenUX compile 主线直接消费内部 DSIR，必须改读：
- `references/profiles/genux-compile.md`
- `references/output-standards/genux-compile-dsir-output-standard.md`
- `references/core/vocab/genux-compile.md`

说明：
- `genux-compile` 不是更丰富的语义输出
- 它是更贴近当前 GenUX 自测样例与 protocol 的 compile-facing 收敛结果
- 它只存在于内部 projection 与校验层
