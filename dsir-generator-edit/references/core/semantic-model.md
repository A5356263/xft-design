# semantic-model

本文件定义 `dsir-generator` 的内部唯一语义骨架。

它用于承接不完整的 `design plan / requirement / context`，先完成设计语义补全，再分别投影为：
- `design-spec.md`：human-facing 结构化设计说明
- `dsir.json`：machine-facing 结构化设计语义

## 边界

本模型不是：
- `Proto Spec`
- 组件树
- 组件库私有实现
- `preset / manifest / renderer` 私有配置
- 运行时状态机或动作图

本模型只表达设计语义，不表达最终执行形态。

## 核心对象

### InputContext
承接上游输入，并保留其不完整性。
建议字段：
- `source_type`
- `requirement_summary`
- `known_scope`
- `known_constraints`
- `known_entities`
- `known_tasks`
- `open_questions`
- `reference_inputs`

### DesignIntent
表达整体设计目标与任务意图。
建议字段：
- `artifact_scope`
- `target_actor`
- `primary_goals`
- `primary_tasks`
- `success_criteria`
- `density_preference`
- `presentation_tone`
- `interaction_level`

### PageIntent
表达页面级语义对象。
建议字段：
- `page_key`
- `page_family`
- `page_goal`
- `task_focus`
- `importance`
- `page_relation_hints`
- `review_focus`

### SectionIntent
表达区域职责。
建议字段：
- `section_key`
- `section_role`
- `section_goal`
- `priority`
- `placement_preference`
- `relationship_to`
- `content_kind`

### BlockIntent
表达可复用语义块。
建议字段：
- `block_key`
- `block_pattern`
- `block_goal`
- `content_model_ref`
- `capabilities`
- `state_hints`
- `interaction_hints`
- `presentation_preference`
- `compile_hints`

### ContentIntent
表达块承载的信息结构。
建议字段：
- `content_model_ref`
- `data_shape`
- `must_have_fields`
- `optional_fields`
- `placeholder_strategy`
- `emphasis`
- `content_priority`

### DecisionLog
记录补全过程中的关键判断。
建议字段：
- `assumption`
- `rationale`
- `ambiguity`
- `fallback_choice`
- `unresolved_items`

## 对象关系

最小关系：
- `InputContext -> DesignIntent`
- `DesignIntent -> PageIntent`
- `PageIntent -> SectionIntent`
- `SectionIntent -> BlockIntent`
- `BlockIntent -> ContentIntent`
- `DecisionLog` 贯穿整个补全过程

## 投影规则

- `design-spec.md`：面向人，强调页面目标、区域职责、语义块说明、设计判断、待确认项
- `dsir.json`：面向机器，强调 page / section / block / content / hints 的结构化表达

## 一句话

本 Skill 不是直接从不完整输入拼 `design-spec` 或拼 `dsir`，而是先补全成统一的设计语义模型，再分别生成两种结构化结果。
