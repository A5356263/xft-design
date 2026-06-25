# XFT Design Agent Contract

本文件用于约束后续在本项目内工作的 Agent 行为，目标是：

- 最大限度减少 AI 自由推理带来的漂移
- 所有可工程化的能力，优先走“数据 + 检索 + 决策 + 装配 + 校验”链路
- 最终让 AI 主要负责两件事：
  - 读需求
  - 按既定工程逻辑生成 HTML

---

## 1. 总原则

### 1.1 检索优先，不靠自由脑补

凡是可以结构化、数据化、脚本化的能力，都必须优先进入正式检索链路。

禁止默认做法：

- 先看需求，再凭经验自由拼页面
- 不经过脚本，直接猜 page_type / recipe / asset
- 明明可以落数据表，却只在 `SKILL.md` 里写口头规则
- 为单个页面临时发明新的通用结构

允许的 AI 自由度只保留在：

- 业务文案填充
- 示例数据填充
- 页面级轻量前端胶水逻辑

不允许 AI 自由决定：

- 页面类型
- recipe
- 主体资产选择
- support CSS 选择
- shell 结构
- 基础组件交互协议

---

## 2. 当前正式工程链路

当前 `xft-design` 的正式生成链路是：

```text
需求
-> ROUTE_DECISION
-> search_content_assets.py
-> CONTENT_ASSET_DECISION
-> Conditional Reads
-> Shell Assembly
-> HTML Output
-> check_skill_output.py / final-check-protocol
```

对应文件位置：

- Skill 主规则：
  - `.claude/skills/xft-design/SKILL.md`
- 内容资产检索脚本：
  - `.claude/skills/xft-design/scripts/search_content_assets.py`
- 内容资产数据：
  - `.claude/skills/xft-design/data/content-assets/`
- shell：
  - `.claude/skills/xft-design/assets/shells/`
- design systems：
  - `.claude/skills/xft-design/design-systems/`
- 页面输出校验：
  - `.claude/skills/xft-design/scripts/check_skill_output.py`
- 输出目录：
  - `output/`

---

## 3. 当前正式检索逻辑

### 3.1 Route Decision

`ROUTE_DECISION` 是第一层决策，必须先于任何内容资产读取。

它负责决定：

- `scope`
  - `Full Page`
  - `Page Overlay`
  - `Component State`
- `page_type`
- `recipe_id`
- `shell`
- `overlay_type`

当前路由判定来源有两层：

1. 显式关键词规则
2. `data/content-assets/page-type-router.csv`

脚本位置：

- `.claude/skills/xft-design/scripts/search_content_assets.py`

说明：

- 这是“匹配式路由”，不是纯大模型自由分类
- 特别场景，如 `弹窗 / 对话框 / Modal / 浮层 / 弹窗编辑`，必须优先走 overlay 路由

---

### 3.2 Content Asset Decision

`CONTENT_ASSET_DECISION` 是第二层正式决策，负责：

- `page_type`
- `recipe_id`
- `required_assets`
- `optional_assets`
- `support_css`
- `unsupported`
- `read_order`

当前数据来源：

- `content-assets.csv`
- `asset-keywords.csv`
- `asset-rules.csv`
- `recipe-rules.csv`
- `recipe-asset-map.csv`
- `support-css-manifest.csv`

脚本逻辑特点：

1. 先选 page route
2. 再选 recipe
3. 再补 required assets
4. 再按关键词 / 规则 / page_type / recipe 过滤 optional assets
5. 最后生成 `read_order`

这层是正式工程检索层，必须作为主体页面生成的唯一资产来源。

---

### 3.3 Conditional Reads

当前项目严格要求按决策结果读取，不允许全量扫资产目录后自行决定。

允许读取的内容必须来自：

- `ROUTE_DECISION`
- `CONTENT_ASSET_DECISION`
- shell
- design systems
- support CSS
- `read_order`

不允许：

- 全量读取 `assets/content-assets/`
- 读未命中的 HTML 资产
- 读历史输出作为生成依据

---

### 3.4 Assembly

HTML 装配必须遵循固定顺序：

1. 复制 shell
2. 注入 `tokens.css`
3. 保留 shell 自身样式
4. 注入 `components.html` 样式
5. 注入 support CSS
6. 按 `read_order` 组装 HTML
7. 替换业务文案和示例数据
8. 输出单个 HTML

这意味着：

- shell 不是自由重写对象
- 页面主体资产不是自由拼装对象
- 页面结构必须来自 shell + 决策命中的资产

---

### 3.5 Final Check

当前正式校验链路：

1. 优先：
   - `.claude/skills/xft-design/scripts/check_skill_output.py`
2. 兜底：
   - `.claude/skills/xft-design/references/content-assets/final-check-protocol.md`

验收重点包括：

- `XFT_ROUTE`
- `CONTENT_ASSET_DECISION`
- slot 是否清干净
- `read_order` 路径是否真实存在
- 是否有禁止 class
- 是否有不允许的 inline style

---

## 4. 壳与基础交互的工程边界

当前项目已经确认：

### 4.1 shell 的职责

shell 负责：

- 页面整体布局
- 固定顶部
- 固定侧边
- 固定 context tabs
- 主内容滚动区
- overlay 根节点

当前主 shell：

- `.claude/skills/xft-design/assets/shells/admin-side-shell.html`

### 4.2 shell chrome 的归属

以下内容属于 shell chrome，不属于 content-assets：

- top-nav
- side-menu
- context-tabs

它们不参加 `CONTENT_ASSET_DECISION` 检索。

### 4.3 基础交互的归属

基础交互属于 skill 内建能力，由 runtime 提供：

- menu 展开 / 收起 / active
- tabs 切换
- overlay 开关
- collapse
- switch
- anchor
- dropdown / popover 基础开关

runtime 位置：

- `.claude/skills/xft-design/assets/runtime/basic-interactions.js`

原则：

- 基础交互不由 AI 临时发明
- 页面级联动胶水允许由 AI 按页面需求编写
- 复杂交互不属于 skill 范围

---

## 5. 当前 icon 层状态

当前 icon 层已经进入正式工程链路。

现状：

- 索引：
  - `.claude/skills/xft-design/data/icons.csv`
- 本地资源：
  - `.claude/skills/xft-design/assets/icons/`
- 检索脚本：
  - `.claude/skills/xft-design/scripts/search_icons.py`
- 流程入口：
  - `.claude/skills/xft-design/SKILL.md`

当前正式目标链路已经是：

```text
需求
-> ROUTE_DECISION
-> CONTENT_ASSET_DECISION
-> ICON_DECISION
-> Conditional Reads
-> HTML Assembly
```

说明：

- icon 不并入 `content-assets`
- icon 作为独立检索域存在
- 资源来源为本地 `assets/icons/`
- 选择来源为 `data/icons.csv`
- 后续新增 icon 能力也必须先补数据和脚本，再允许页面使用

---

## 6. 后续新增能力的统一落地标准

后续无论补什么能力，都必须优先判断它属于哪一类：

### A. 正式检索域

适用于：

- page_type / route
- recipe
- region / module / overlay / state
- support CSS
- icon
- 未来的图表模板、状态模板、导航模式等

必须具备：

1. 独立数据源
2. 独立或挂接到正式检索脚本
3. 结构化决策输出
4. 明确读取顺序
5. 明确校验方式

最小落地标准：

- `data/*.csv` 或等价结构化数据
- `scripts/*.py` 或挂接到现有正式脚本
- 决策记录字段
- 被 `SKILL.md` 正式纳入流程

### B. Skill 内建基础设施

适用于：

- shell
- tokens
- components
- runtime

特点：

- 不参与逐页检索
- 是固定底座
- 只能按规则升级，不允许页面级随意改写

### C. 页面级胶水逻辑

适用于：

- 点击菜单切换右侧局部内容
- 纯前端模拟上传状态
- 页面内部几个组件的简单联动

特点：

- 可以由 AI 按页面需求编写
- 但不沉淀为 skill 正式检索域
- 也不沉淀为 skill 通用 runtime，除非后续确认应升级为基础能力

---

## 7. 后续新增能力禁止走的路径

禁止新增以下模式：

### 7.1 只写在 SKILL.md 里，不落工程数据

如果某类能力会重复出现，就不能只写一段描述规则。

必须至少补齐：

- 数据
- 检索
- 决策输出

### 7.2 把所有东西都塞进 content-assets

`content-assets` 只负责页面内容资产。

以下不应强塞进去：

- shell chrome
- runtime
- icon 本地资源
- 页面级胶水逻辑

### 7.3 让 AI 自由决定通用能力实现

以下内容不应由 AI 临时自由决定：

- 通用布局协议
- 通用组件结构
- 基础交互协议
- 通用 icon 风格
- 页面主体资产选型

---

## 8. Agent 工作准则

后续 Agent 在本项目内工作时，应遵守：

1. 先判断该需求属于：
   - 正式检索域
   - 基础设施
   - 页面级胶水

2. 能走匹配就不走自由推理

3. 能走数据表就不只写说明

4. 能走脚本就不手工猜

5. 若当前工程链路还没有这类能力：
   - 先补正式检索机制
   - 再让页面生成使用

6. 如果暂时只能用特殊规则：
   - 必须明确标记为“过渡态”
   - 后续要收回到统一工程逻辑

---

## 9. 当前项目的目标状态

最终目标不是“AI 很会设计页面”，而是：

```text
AI 只读需求
-> 通过工程规则完成匹配
-> 只读取命中的结构化资源
-> 写出 HTML
```

也就是说：

- AI 的创造性主要体现在文案、示例数据和少量页面胶水
- 页面骨架、内容资产、图标、基础交互、壳结构，都尽量工程化

这是本项目后续所有补充工作的统一方向。
