# 后续转化批次建议

## 批次原则

不是按文件夹机械转，而是按“页面生成闭环”转。

## Batch 1：页面配方与主路径资产

目标：先闭环列表页、详情页、表单页、设置页、首页。

包含：
- 典型页面 17 张
- 表格 Table、描述列表 Descriptions、表单 Form
- Header / Toolbar / Footer / Body 按钮位置规则

产出：
- page-recipes
- regions
- asset-rules

## Batch 2：高频内容区模块

目标：补齐 B 端内容区核心模块。

包含：
- 审批流
- 上传 / 上传下载
- 筛选项配置
- 表头设置
- 异步处理
- 拖拽排序
- 附件 / 文件预览

产出：
- modules
- component-combos
- states

## Batch 3：反馈、状态、覆盖层

目标：让生成页面具备操作闭环。

包含：
- Modal / Drawer / Popconfirm
- Alert / Message / Notification
- Progress / Skeleton / Spin / Result / Empty

产出：
- overlays
- states
- feedback-rules

## Batch 4：导航与补充组件组合

目标：补齐页面内导航和基础控件规则。

包含：
- Tabs / Steps / Anchor / Pagination / Dropdown / ReturnButton
- Input / Select / Checkbox / Radio / DatePicker 等
- Tag / Badge / Tooltip / Popover 等展示组件

产出：
- navigation regions
- component-combos
- rules

## Batch 5：复杂专题

目标：处理复杂资产的专项设计。

包含：
- 公式编辑器 4 张
- 图片裁剪
- 全屏
- Tour
- Carousel 等低频场景

产出：
- complex modules
- deferred rules
