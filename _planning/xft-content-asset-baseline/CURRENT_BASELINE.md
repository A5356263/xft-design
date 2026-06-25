# CURRENT_BASELINE

## Status

当前 `xft-design` 的内容资产改造成果已冻结为可用基线。

本基线明确约束：

- 不再修改 `step11`
- 不再修改 `step12`
- 不再修改 `step13`
- 不再修改 `step15`

本文件仅记录当前可用能力和后续方向，不引入新的实现变更。

## Current Capability

当前 Skill 已具备以下稳定能力：

- 已完成内容资产驱动工作流接入
- `SKILL.md` 已切换到 `ROUTE_DECISION -> CONTENT_ASSET_DECISION -> asset reads -> assembly` 主流程
- 检索脚本可输出稳定的 `CONTENT_ASSET_DECISION`
- 内容资产目录、数据表、支持 CSS、校验脚本已接通
- `Page Overlay` / `Modal` 路由已生效
- TablePage optional asset 命中规则已收紧

## Validated Baseline

当前基线满足以下验收结论：

- 4 个验证页面全部 `PASS`
- `unsupported` 为空
- 弹窗编辑已走 `Page Overlay + Modal`
- 列表页默认态不再静态展开批量底栏和详情抽屉

对应验证页面如下：

- [employee-roster-validation-2026-06-25-v2.html](e:/AI设计/xft-design/output/employee-roster-validation-2026-06-25-v2.html:1)
- [approval-detail-validation-2026-06-25-v2.html](e:/AI设计/xft-design/output/approval-detail-validation-2026-06-25-v2.html:1)
- [settings-config-validation-2026-06-25-v2.html](e:/AI设计/xft-design/output/settings-config-validation-2026-06-25-v2.html:1)
- [member-edit-modal-validation-2026-06-25-v2.html](e:/AI设计/xft-design/output/member-edit-modal-validation-2026-06-25-v2.html:1)

对应最新验证报告：

- [xft-real-page-validation-step15-2026-06-25.json](e:/AI设计/xft-design/output/xft-real-page-validation-step15-2026-06-25.json:1)

## Baseline Behavior

### 1. 员工花名册列表页

- 默认态只展示列表核心区域
- 不默认展开批量操作底栏
- 不默认展开详情抽屉
- 筛选、工具栏、表格、分页语义稳定

### 2. 审批详情页

- 审批流、基础信息、操作记录、关联明细已可稳定组合
- 附件区默认走“预览 / 下载 / 查看”语义
- 不再默认使用上传 / 补传语义

### 3. 参数配置设置页

- 左侧锚点与右侧分组已一一对应
- 已补充“生效范围 / 修改影响 / 最近变更”
- 页面已具备设置中心的基本内容密度

### 4. 成员编辑弹窗

- 路由为 `scope: Page Overlay`
- `overlay_type: Modal`
- `page_type: None`
- Modal 下方已有真实成员列表上下文
- 关键字段已表现为可编辑控件

## Known P2 Issues

以下问题当前不阻塞基线冻结，但仍属于已知 `P2`：

- 当前没有单独产出“批量操作态”的独立列表样例页
- 当前没有单独产出“详情抽屉态”的独立列表样例页
- Modal 中的下拉字段当前使用原生 `<select class="input">`，可编辑语义已成立，但视觉还不是更强的 XFT 组件态
- 部分验证页面仍偏“能力样例页”，离高保真业务产品页还有继续微调空间

## Optional Next Steps

后续如果继续优化，建议按以下方向推进：

1. 补状态样例
   - 单独补“列表批量态”
   - 单独补“列表详情抽屉态”

2. 提升组件真实感
   - 为 Modal 内选择字段补更接近 XFT 的选择控件表达
   - 优化少量示例数据与文案的产品真实感

3. 扩展验证覆盖
   - 增加更多页面类型
   - 增加更多 overlay / drawer / result / settings 变体

4. 进入下一阶段前的原则
   - 以当前基线为冻结起点
   - 新优化尽量以新增样例、补状态、补规则为主
   - 避免回头改写 `step11`、`step12`、`step13`、`step15` 的既有逻辑

## Freeze Note

从当前时点开始，`xft-design` 内容资产改造成果以本基线为准。  
后续新增工作应被视为“基线之上的增量优化”，而不是重新定义本轮改造结果。
