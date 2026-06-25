# Ant Design Pro 资产形态对齐说明

## 借鉴边界

本项目不复制 ant-design-pro 的 React、Umi、ProComponents 代码。

只借鉴它的 B 端页面资产形态：

```text
页面类型 → 区域结构 → 模块组合 → 操作闭环
```

## 对齐关系

| Ant Design Pro 页面类型 | XFT 页面配方 |
|---|---|
| table-list | recipe.table.basic |
| basic-list / card-list | recipe.table.card |
| advanced-form | recipe.form.basic.vertical / recipe.form.step |
| profile/basic | recipe.detail.basic.vertical |
| profile/advanced | recipe.detail.table.horizontal / recipe.workflow.detail |
| dashboard/workplace | recipe.home.basic |
| result/success / result/fail | recipe.result.success / recipe.result.fail |
| exception/403 / 404 / 500 | recipe.exception.basic |

## 转化原则

- Ant Design Pro 的完整页面只作为结构样本，不作为最终代码。
- 最终输出必须使用 XFT 的 HTML 片段、class、token。
- 页面结构必须落到 page-recipes 和 recipe-asset-map。
- 区域和模块需要后续生成独立 HTML 资产。

## 对 XFT 的意义

Ant Design Pro 补的是页面结构层，而不是视觉层。

本项目已有 token 和组件基础，下一步应补：

```text
区域资产
模块资产
组件组合资产
状态资产
覆盖层资产
```
