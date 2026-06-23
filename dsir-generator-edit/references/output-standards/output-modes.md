# 输出模式

## 默认模式
未设置 `output_mode` 时，按默认流程输出：
- `design-spec.md`
- 可选说明文件，如 `review-summary.md`
- 不输出 `dsir.json`

要求：
- 保持完整流程不变：需求解析、语义建模、内部 DSIR 推导、profile 选择、DSIR 校验全部照常执行
- 禁止创建、更新、覆盖任何 `dsir.json` 文件
- `review-summary.md` 若输出，需说明 DSIR 已在内部完成推导但未输出为文件

## design-spec-only
若显式设置 `output_mode=design-spec-only`：
- 行为与默认模式等价
- 仅作为显式说明，不引入新的输出分支

## 边界
- 输出层默认只面向 `design-spec.md`
- `generic / genux-compile` 的差异只存在于内部 DSIR projection 与校验目标
- `design-spec.md` 不因 profile 改写为不同版本
- 不改变 `semantic-model`
- 不改变内部 DSIR 推导与校验逻辑
