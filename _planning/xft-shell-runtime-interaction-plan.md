# XFT Shell Runtime Interaction Plan

## 背景

当前 `xft-design` 已完成内容资产驱动改造，但 shell 与组件交互层存在以下问题：

1. `admin-side-shell.html` 的壳职责和业务 chrome 边界不够清晰。
2. 左侧菜单、顶部导航、上下文页签虽然存在结构和样式，但基础交互尚未产品化。
3. 如果没有统一 runtime，后续页面交互很容易退化成 AI 临时写 JS。

本计划用于约束下一阶段 shell 与基础交互能力建设，不涉及重做内容资产体系，不涉及修改 step11/step12 的既有结论。

## 总目标

把 `xft-design` 从“静态壳 + 静态组件示意”升级为：

- 稳定的后台壳布局系统
- 稳定的壳级 chrome
- 稳定的基础交互 runtime
- AI 只做声明式接入，不自由发明交互逻辑

## 已确认决议

1. `admin-side-shell.html` 保留为完整壳资源。
2. `top-nav`、`side-menu`、`context-tabs` 属于壳级 chrome，不进入 `content-assets` 检索体系。
3. shell 布局目标固定为：
   - `top-nav` 固定在顶部
   - `side-nav` 固定在左侧
   - `context-tabs` 固定在右侧内容区顶部
   - `page-content` 为唯一主滚动区
   - `overlay-root` 为独立覆盖层容器
4. 基础交互统一由 runtime 提供，AI 不允许自由写组件交互 JS。
5. AI 只能通过既定 HTML 结构、class、`data-*`、`aria-*`、默认状态声明来接入交互。
6. 复杂交互默认不纳入基础 runtime。

## 基础交互白名单

### 必须支持

1. Menu
   - 菜单分组展开 / 收起
   - 当前项 active
   - group title 选中态
   - 二级菜单显隐
   - hover / active CSS 状态

2. Tabs
   - tab 切换
   - active 状态切换
   - close 按钮基础反馈
   - hover / active CSS 状态

3. Overlay
   - modal 打开 / 关闭
   - drawer 打开 / 关闭
   - confirm dialog 打开 / 关闭
   - close 按钮关闭
   - 是否允许 mask 关闭可配置

4. Collapse
   - 展开 / 收起
   - `aria-expanded`
   - panel 显隐

5. Switch
   - checked / unchecked
   - `aria-checked`
   - active 样式切换

6. Anchor
   - 当前项高亮
   - 点击定位

7. Dropdown / Popover
   - 基础开 / 关
   - 点击外部关闭
   - trigger active 状态

### 说明

- `hover` 主要由 CSS 承担。
- `click / toggle / open / close / active / expanded` 主要由 runtime 承担。
- 允许后续补充更多基础交互，但必须先沉到 runtime，再允许页面使用。

## 白名单覆盖性评估

### 结论

当前白名单可以覆盖“绝大多数组件的基础交互”，但不能覆盖“所有组件的全部交互”。

### 可以被基础 runtime 覆盖的类型

- 导航切换型：menu、tabs、anchor、segmented
- 开关型：switch、collapse、dropdown、popover
- 显隐型：modal、drawer、confirm、tooltip、message、notification
- 选择型的轻状态切换：checkbox、radio、select 的展示态切换

### 只需要 CSS 或几乎不需要 runtime 的类型

- button
- typography
- divider
- space
- tag
- card
- page header
- descriptions
- statistic
- result
- empty
- skeleton

### 不应承诺由基础 runtime 完整覆盖的类型

- autocomplete
- cascader
- datepicker / timepicker
- upload
- tree / tree-select
- transfer
- slider
- color picker
- carousel
- calendar
- tour
- table 的复杂排序 / 过滤 / 列拖拽
- 复杂表单校验
- 异步搜索
- 拖拽排序
- 树懒加载
- 虚拟滚动

### 因此建议的正式口径

不要对外表述为：

- “runtime 能覆盖所有组件交互”

而要表述为：

- “runtime 覆盖所有通用基础交互，不覆盖复杂业务交互和高复杂度控件逻辑”

## Skill 与页面胶水边界

### Skill 负责

1. shell 布局
2. 壳级 chrome
3. 组件 HTML 结构约定
4. token 与基础 CSS
5. 基础交互 runtime
6. 通用状态表达规则

### AI 按页面需求负责

1. 页面级联动胶水逻辑
2. 纯前端模拟交互
3. 组件之间的局部联动

典型示例：

- 点击左侧菜单切换右侧内容
- 点击某个局部操作切换详情 panel
- 切换 tab 后联动局部内容显隐
- 上传区模拟选择文件后展示列表、进度和状态

这些能力不沉到 skill 通用 runtime，由 AI 在页面生成时根据需求编写轻量前端逻辑即可。

### Skill 不负责

1. 页面级联动胶水的通用框架
2. 复杂组件完整 API
3. 真实上传能力
4. 后端接口联动
5. 拖拽、虚拟滚动、复杂校验、复杂状态机

### 上传能力正式边界

上传相关页面仅支持：

- 纯前端模拟交互
- 展示文件名、进度、成功失败状态
- 局部删除、重试等前端表现

不支持：

- 真实本地文件上传到服务端
- 与系统文件能力打通
- 复杂上传管理逻辑

## 交互接入规则

页面和壳只能使用以下方式接入交互：

1. 既定 class
2. 既定 `data-*`
3. 既定 `aria-*`
4. 既定 `hidden`
5. 既定状态 class，例如：
   - `is-active`
   - `is-selected`
   - `contract`

禁止：

1. 页面级自由内联脚本
2. 组件级临时自定义事件系统
3. 与 runtime 平行的第二套交互协议

补充说明：

- runtime 只承接基础组件交互
- 页面联动胶水不进入 runtime
- AI 如需实现页面联动，应写局部、轻量、纯前端的逻辑，不得把页面胶水反向抽象成新的 skill 基础设施

## 下一阶段执行顺序

1. 固化 shell 布局协议
   - 修正 `top-nav`、`side-nav`、`context-tabs` 固定关系
   - 修正 `page-content` 独立滚动

2. 完善 runtime 第一版
   - menu
   - tabs
   - overlay
   - collapse
   - switch
   - anchor
   - dropdown / popover

3. 更新 skill 规则
   - 明确 AI 不允许自由写交互 JS
   - 明确只允许声明式接入

4. 做页面级验证
   - 生成真实页面
   - 检查交互是否按协议工作

## 验收标准

1. `admin-side-shell` 成为稳定壳，不再依赖内容区滚动驱动整体布局。
2. `side-menu` 支持展开 / 收起 / hover / active。
3. `context-tabs` 支持 active 切换。
4. overlay / collapse / switch / anchor / dropdown-popover 至少支持基础开关能力。
5. AI 生成页面时不再需要临时写组件交互 JS。
6. 交互全部通过统一 runtime 接管。
7. `SKILL.md` 中有明确的交互边界说明。

## 当前边界

本计划只覆盖：

- shell
- 壳级 chrome
- 基础 runtime
- skill 交互规则

本计划不覆盖：

- 复杂业务交互
- 后端接口驱动行为
- 高复杂度输入控件的完整能力模拟
