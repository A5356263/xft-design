# authoring-sequence

## 固定顺序

1. 判断目标 profile
2. 判断 `output_mode`
3. 收敛输入事实
4. 形成内部 `semantic-model`
5. 判断页面、区域、语义块与内容模型
6. 记录关键假设与未决项
7. 生成人读 `design-spec.md`
8. 生成目标 profile 的内部 DSIR 结果
9. 运行对应校验与回归
10. 输出 `design-spec.md` 与允许的说明文件

## 关键要求

- 永远先形成 `semantic-model`，再投影 human-facing 与 machine-facing 内部结果
- `design-spec.md` 保持 human-facing，不写成 compile 准备稿
- `design-spec.md` 不区分 profile
- `genux-compile` 只约束内部 DSIR projection 与 validator
- 默认不输出 `dsir.json`
