# genux-compile profile

用于内部生成当前 GenUX 编译主线最容易直接消费的 DSIR projection。

本 profile 只追加 `DSIR contract`、词表、payload 形式与 compile boundary 约束，不改变 Skill 的通用语义内核，也不改变 `design-spec.md`。

## 目标

在保持设计语义边界正确的前提下，生成更贴近当前 GenUX 自测样例的 compile-facing 内部 DSIR：

- 顶层使用 `metadata / project / shared_context / pages`
- `project` 优先表达 `project_id / shell_model`
- `shared_context` 优先表达 `project_scope / normalized_from`，`component_preset` 仅作为可选上下文字段
- page / section / block 词表对齐当前 `packages/protocol/src/types/dsir.ts`
- block 的 `semantic_payload` 优先收敛为：
  - `page_id`
  - `region_id`
  - `module_refs`
- `compile_hints` 优先保持轻量，仅表达 compile-facing 来源与最小语义提示

## 必须遵守的边界

- 不输出 `Proto Spec`
- 不输出组件树
- 不输出 `preset / manifest / renderer` 私有实现
- 不把 workflow runtime、plugin system、patch rule 带进 Skill
- 不改变 `design-spec.md` 的 human-facing 表达

## 词表映射原则

若 richer semantic model 使用了通用词表，投影到 `genux-compile` 时必须先映射到当前 GenUX canonical vocab。

### page family -> page_type
- `list-management` -> `directory`
- `detail-overview` -> `detail`
- `dashboard-analysis` -> `dashboard`

### section_role 约束
输出只允许当前 GenUX protocol 已定义的 section role：
- `hero`
- `navigation`
- `summary`
- `filters`
- `content`
- `detail`
- `review`
- `actions`

### block_pattern 约束
输出只允许当前 GenUX protocol 已定义的 block pattern。
优先使用已在真实 compile 中 resolved 的集合：
- `section-navigation`
- `metric-group`
- `record-table`
- `record-collection`
- `descriptive-items`
- `action-cluster`

## 投影收敛规则

对于 richer semantic model 中暂未在当前 GenUX compile-facing contract 中稳定出现的语义块：
- 优先压缩到最接近的已支持 block pattern
- 若无法稳定映射，则保留在 `design-spec.md`，不要强行写入 compile-facing internal DSIR
- 不要为了保留全部上游语义而破坏当前 compile contract

## design-spec 边界

`genux-compile` 只约束内部 DSIR 的 compile-facing projection。
不要把 `design-spec.md` 一起改写成 machine-prep 结构。
`design-spec.md` 仍应遵守 `references/output-standards/design-spec-output-standard.md`。

## 输出说明

- `genux-compile` 只影响内部 DSIR 推导与 compile-facing 校验
- 不输出 `dsir.json` 文件
