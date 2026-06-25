# Shell 识别输入说明

本次只分析桌面 Web 端系统首页。

文件说明：
- homepage-full.pic.jpg：系统首页完整截图
- global-header.pic.jpg：顶部全局导航截图
- common.css
- iconfont.css
- p__workbench.8226df7d.chunk.css
- reset.css
- styles.fd71c94d080b1e28e773.css
- umi.04e2b1ce.css
- wrappers.42c706bf.chunk.css

注意：
首页卡片、数据内容、业务模块不属于 Shell。本次只识别卡片外层所在的 Content Area 容器、布局边界、间距、滚动关系和区域结构，不分析卡片内部内容。不要分析卡片文案、数据、图标和业务含义。只记录卡片所在内容区的容器关系。

分析目标：
- 识别 Global Shell
- 识别 App Shell，如果不存在则说明不存在
- 识别 Page Header
- 识别 Content Area

限制：
- 不分析移动端
- 不重构页面
- 不新增导航
- 不根据通用 B 端经验推导未出现的结构
- 无法确认的信息标记为“需确认”