# 第 6 步：状态 / 反馈 / 覆盖层资产说明

本步把素材中的反馈类内容转成可装配资产。资产分为三类：

1. feedback：Message、Alert、Notification，表达操作反馈或提示。
2. state：Empty、Loading、Progress、Result，替换页面或区域内容状态。
3. overlay：Modal、Drawer、Popconfirm，承载临时流程或确认。

## 使用边界

- Message：轻量、短文案、非阻断。
- Alert：页面内说明、限制、弱提醒。
- Notification：异步完成或可稍后处理提醒。
- Empty：内容为空且需要说明原因或下一步。
- Skeleton：首屏或卡片加载。
- Spin：短时局部等待。
- Progress：可量化任务进度。
- Modal：短流程表单、简单编辑、确认。
- Drawer：右侧详情、复杂配置、保留上下文。
- Popconfirm：行内轻量危险操作。
