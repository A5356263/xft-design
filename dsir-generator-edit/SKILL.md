---
name: dsir-generator
description: 根据不完整的 design plan、需求描述和设计上下文，先补全内部设计语义模型，再输出 human-facing design-spec.md。Skill 内部始终完成 DSIR 推导与校验，但不输出 dsir.json 文件；如需对齐不同机器消费目标，仅在内部区分 generic 与 genux-compile 两种 DSIR projection，不改变 design-spec.md 的人读表达。
---

# DSIR 生成技能

## 职责

本技能负责把不完整输入收敛为统一的设计语义模型，并从该模型投影出：
- `design-spec.md`
- 目标 profile 的内部 DSIR 结果（仅内部推导与校验，不落盘为文件）

本技能负责：
- 收敛上游设计信息
- 形成内部 `semantic-model`
- 选择页面、区域、语义块与内容模型
- 记录关键假设与未决项
- 生成人读 `design-spec.md`
- 生成目标 profile 的内部 DSIR 结果
- 对内部 DSIR 运行对应校验与回归
- 仅输出 `design-spec.md` 与允许的说明文件

本技能不负责：
- 输出 `dsir.json` 文件
- 直接生成 `Proto Spec`
- 直接输出组件树
- 直接定义 `preset / manifest / renderer` 私有实现
- 直接吸收 workflow runtime、plugin system、patch rule 等系统层信息

## 中轴定义

开始前先读：
- `references/core/semantic-model.md`
- `references/core/artifact-boundary.md`
- `references/core/authoring-sequence.md`
- `references/output-standards/output-modes.md`

要求：
- 先形成内部 `semantic-model`
- 再投影出 `design-spec.md` 与内部 DSIR 结果
- `design-spec.md` 始终保持 human-facing
- `design-spec.md` 不区分 `generic / genux-compile`
- `generic / genux-compile` 只约束内部 DSIR projection 与校验目标
- 默认不输出任何 `dsir.json` 文件

## profile 选择

profile 只服务于内部 DSIR 推导与校验，不改变 `design-spec.md` 的表达、结构和真相层级。

### 1. generic（默认内部 profile）
用于 richer semantic authoring 的内部 DSIR 结果。
适合：
- 独立使用本 Skill
- 下游不是当前 GenUX 编译主线
- 需要更丰富的内部语义层表达

读取：
- `references/profiles/generic.md`
- `references/output-standards/design-spec-output-standard.md`
- `references/output-standards/dsir-output-standard.md`

### 2. genux-compile（内部 projection profile）
用于让当前 GenUX compile 主线更容易直接接住内部 DSIR 结果。
适合：
- 当前目标是对齐 GenUX 自测项目的 compile-facing DSIR
- 需要对齐 `metadata / project / shared_context / pages` 顶层结构
- 需要对齐 `packages/protocol/src/types/dsir.ts` 的词表与最小字段
- 需要对齐当前 compile-facing payload 形式：`page_id / region_id / module_refs`

读取：
- `references/profiles/genux-compile.md`
- `references/output-standards/design-spec-output-standard.md`
- `references/output-standards/genux-compile-dsir-output-standard.md`
- `references/core/vocab/genux-compile.md`

## output_mode

### 默认
未设置 `output_mode` 时：
- 输出 `design-spec.md`
- 可输出 `review-summary.md`
- 始终不输出 `dsir.json`
- 内部仍完整执行 DSIR 推导、profile 选择、校验与回归

### design-spec-only（兼容别名）
若显式设置 `output_mode=design-spec-only`：
- 行为与默认模式等价
- 继续完整执行内部 DSIR 推导
- 继续按目标 profile 对内部 DSIR 进行校验
- 禁止创建、更新、覆盖任何 `dsir.json` 文件
- 仅输出：
  - `design-spec.md`
  - 允许的说明文件，如 `review-summary.md`
- 若输出 `review-summary.md`，必须写入：
  - `DSIR 已在内部完成推导，但根据当前输出策略未输出为文件。`

## 固定步骤

1. 判断目标 profile
2. 判断 `output_mode`（若未设置，按默认处理）
3. 收敛输入事实
4. 形成内部 `semantic-model`
5. 读取必要语义知识文件
6. 生成 `design-spec.md`
7. 生成目标 profile 的内部 DSIR 结果
8. 运行对应校验与回归
9. 仅输出 `design-spec.md` 与允许的说明文件

## 输出与校验

### design-spec
输出后运行：
- `python scripts/validate_design_spec_structure.py <design-spec.md>`

### generic internal dsir
始终执行内部校验：
- `python scripts/check_output_shape.py <internal-generic-dsir>`
- `python scripts/validate_dsir.py <internal-generic-dsir>`

要求：
- generic 结果只用于内部语义验证与机器消费准备
- 不写出 `dsir.json` 文件

### genux-compile internal dsir
始终执行内部校验：
- `python scripts/check_vocab_aliases.py <internal-genux-compile-dsir>`
- `python scripts/validate_genux_compile_projection.py <internal-genux-compile-dsir>`

要求：
- genux-compile 结果只用于内部 compile-facing 对齐与验证
- 不写出 `dsir.json` 文件

### regression
必要时运行：
- `python scripts/regression/run_regression.py`

## 文件路由

### 核心控制与中轴
- `references/core/semantic-model.md`
- `references/core/artifact-boundary.md`
- `references/core/authoring-sequence.md`
- `references/output-standards/output-modes.md`

### 页面大语义
- `references/page-families/list-management.md`

### 区域规则
- `references/sections/shell-header.md`
- `references/sections/route-nav-bar.md`
- `references/sections/shell-navigation.md`
- `references/sections/sidebar.md`
- `references/sections/primary-content.md`

### 语义块
- `references/blocks/category-tree.md`
- `references/blocks/filter-form.md`
- `references/blocks/action-cluster.md`
- `references/blocks/local-primary-action.md`
- `references/blocks/record-table.md`
- `references/blocks/pagination-footer.md`
- `references/blocks/view-switcher.md`
- `references/blocks/metric-group.md`

### 内容模型
- `references/content-models/README.md`
- `references/content-models/hierarchical-options.md`
- `references/content-models/query-conditions.md`
- `references/content-models/action-set.md`
- `references/content-models/single-primary-action.md`
- `references/content-models/record-collection.md`
- `references/content-models/pagination-context.md`
- `references/content-models/view-options.md`
- `references/content-models/scalar-metrics.md`
- `references/content-models/presentation-boundary.md`

### 判断规则
- `references/rules/block-selection.md`
- `references/rules/capability-vs-variant.md`

### 输出标准
- `references/output-standards/output-modes.md`
- `references/output-standards/design-spec-output-standard.md`
- `references/output-standards/dsir-output-standard.md`
- `references/output-standards/genux-compile-dsir-output-standard.md`
- `assets/templates/design-spec_minimal_template.md`
- `assets/templates/dsir_minimal_template.json`
- `assets/templates/genux_compile_dsir_template.json`
- `assets/templates/review_summary_template.md`
