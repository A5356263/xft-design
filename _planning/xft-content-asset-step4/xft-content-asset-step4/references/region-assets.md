# 第 4 步：XFT 区域资产说明

本步骤把素材中的页面结构和区域布局，转成 **可直接装配的区域级 HTML 片段**。

## 本步产出范围

- 已生成区域资产：29 条
- 已生成 HTML 片段：29 个
- 已生成公共区域 CSS：`assets/regions/_region-support.css`
- 已建立 91 张素材的覆盖映射：`_coverage/material-coverage-step4.csv`

## 区域资产分层

| 目录 | 内容 |
|---|---|
| `page-header/` | 页面标题、说明、返回、页面级操作 |
| `filter-bar/` | 基础筛选、高级筛选、紧凑搜索 |
| `table-toolbar/` | 表格标题、工具栏、列设置入口 |
| `table-region/` | 表格主体、选择汇总 |
| `pagination/` | 分页区域 |
| `form-region/` | 表单分组、底部操作 |
| `detail-region/` | 摘要区、详情信息、详情左右布局 |
| `settings-region/` | 设置页锚点布局、设置项分组 |
| `home-region/` | 首页指标区、首页内容网格 |
| `navigation-region/` | 步骤条、标签页、锚点 |
| `result-region/` | 结果页、异常页区域 |
| `split-layout/` | 主从分栏/父子结构 |
| `card-grid/` | 卡片列表/卡片表格 |

## 使用原则

1. 区域资产可以直接复制到页面配方的对应位置。
2. 业务字段、标题、表格列、具体文案允许替换。
3. 区域结构、class、对齐关系、按钮位置不允许自由改写。
4. 当前 HTML 片段依赖 `assets/regions/_region-support.css`。
5. 后续第 7 步会把这些区域资产与模块资产一起整理成最终装配包。

## 注意

本步没有处理：审批流、上传下载、异步处理、表头设置、反馈、弹窗、抽屉、组件 API 规则。它们已在覆盖表中登记，后续步骤继续转化。
