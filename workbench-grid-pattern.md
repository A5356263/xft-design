# 工作台首页卡片布局 / Workbench 3-Column Card Grid Layout

该布局用于 Web 端工作台首页 Content Area，不属于 Global Shell 或 App Shell，而属于首页内容区布局 Pattern。

## 布局规则

1. 首页内容区采用 3 等分栅格。
2. 卡片容器支持 3 种宽度：1/3、2/3、3/3。
3. 1/3 卡片占 1 个栅格位，可用于左侧主区域或右侧辅助列。
4. 2/3 卡片占 2 个栅格位，仅用于左侧主区域。
5. 3/3 卡片占满整行，仅在不区分左右区域的特殊场景使用，使用频率较低。
6. 右侧辅助列固定为 1/3 宽度，只能承载 1/3 卡片。
7. 左侧主区域为 2/3 宽度，可承载 1 个 2/3 卡片，或并排承载 2 个 1/3 卡片。
8. 卡片内部的文案、图标、数据和业务内容不属于布局规则；AI 只需识别卡片外壳、宽度跨度、排列方式和区域归属。

## 结构示意

```
workbench-grid（3 等分栅格）
├── row 1
│   ├── main_area   span-2 (占 2/3)
│   └── side_area   span-1 (占 1/3)
├── row 2
│   ├── main_area   span-1 (占 1/3)
│   ├── main_area   span-1 (占 1/3)
│   └── side_area   span-1 (占 1/3)
└── row 3
    └── full_width_area  span-3 (全宽)
```

## 生成约束

- 不得将该布局简化为普通双栏布局。
- 不得将该布局简化为等宽卡片列表。
- 不得在右侧辅助列生成 2/3 或 3/3 卡片。
- 不得随意改变卡片跨度。
- 如果无法判断卡片宽度，应标记为需确认，不得自行推导。

## 与 Shell 的关系

- 3 列栅格与 Shell 中的 `page-content-container`（白色圆角大容器）**平级**。
- **首页**（工作台首页 / 应用内首页）→ 使用 3 列栅格替代 `page-content-container`，插入 `micro-wrapper` 内。
- **非首页**（表格页、表单页、详情页等）→ 使用原有的 `page-content-container` 白色容器。

```
page-content
└── micro-wrapper
    ├── [HomePage]  home-grid (3列栅格)
    └── [非HomePage] page-content-container (白色圆角大容器)
```

## 响应式宽度

屏幕宽度记为 W。基础变量：左右边距 16px×2，卡片间距 16px，栅格内 2 个间距 16px×2。

### 场景一：工作台首页（无 Sidebar）

`content_width = clamp(1248px, W - 32px, 1580px)`

- W < 1280 → 1248px（横向溢出）
- 1280 ≤ W ≤ 1612 → W - 32px
- W > 1612 → 1580px

### 场景二：业务应用首页（有 188px Sidebar）

`content_width = clamp(1060px, W - 188px - 32px, 1580px)`

- W < 1280 → 1060px（横向溢出）
- 1280 ≤ W ≤ 1800 → W - 188px - 32px
- W > 1800 → 1580px

### 卡片宽度

- 1/3 = (content_width - 32px) / 3
- 2/3 = 1/3 × 2 + 16px
- 3/3 = content_width

### CSS 实现

两种场景共用 `margin: 0 var(--spacing-4)` 产生左右 16px 自然留白，裁切时由 `page-content` 的 `overflow: auto` 产生滚动条，留白不被压缩。场景二额外扣除 188px sidebar（通过 `work-area` 的 `flex: 1` 自动处理）。

### 生成约束

- 不得将卡片宽度写成固定像素值。
- 不得在最小断点以下压缩卡片，不得在最大断点以上拉伸卡片。
- 生成业务应用首页时，必须先扣除 188px sidebar，再计算栅格宽度。
- 不得将业务应用首页按工作台首页规则计算，不得将卡片跨入 Sidebar 区域。
- 若无法判断页面是否存在 sidebar，标记为需确认。
- 若无法确认屏幕宽度，使用 span-1/span-2/span-3 表达跨度，不推导像素值。

## 适用范围

- 工作台首页（场景一，无 Sidebar）
- 业务应用首页（场景二，有 188px Sidebar）
