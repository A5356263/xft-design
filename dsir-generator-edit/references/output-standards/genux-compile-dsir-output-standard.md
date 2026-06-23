# GenUX compile-facing DSIR 输出标准

本文件定义 `genux-compile` profile 下的 `dsir.json` 目标形态。

## 顶层结构

必须包含：
- `metadata`
- `project`
- `shared_context`
- `pages`

## metadata

最小字段：
- `spec_id`
- `schema_version`
- `project_id`
- `generated_from`

可选字段：
- `created_at`

## project

最小字段：
- `project_id`
- `shell_model`

## shared_context

优先字段：
- `project_scope`
- `normalized_from`
- `component_preset`

## page

必须对齐当前 GenUX protocol：
- `page_id`
- `page_type`
- `page_goal`
- `target_actor`
- `primary_tasks`
- `layout_mode`
- `density`
- `review_criteria`

可选字段：
- `presentation_preference`

## section

必须包含：
- `section_id`
- `section_role`
- `priority`
- `content_kind`
- `placement_preference`

可选字段：
- `relationship_to`
- `blocks`

## block

必须包含：
- `block_id`
- `block_pattern`
- `semantic_payload`

在 `genux-compile` profile 下，`semantic_payload` 优先收敛为：
- `page_id`
- `region_id`
- `module_refs`

`compile_hints` 应保持轻量，优先使用：
- `{"source": "dsir-native"}`

## compile-facing 约束

- 不写 `content_model_ref`
- 不写 `instance_payload`
- 不写 richer semantic object 明细
- 不写组件库私有 props
- 不写 renderer 私有字段

这些 richer 语义应保留在：
- `design-spec.md`
- 通用 semantic model
- 可选 generic DSIR
