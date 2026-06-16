# XFT 设计系统

> 分类：企业级 & 专业
> 面向企业后台业务应用的维度化 Token 命名设计系统。清晰、克制、信息密度高。

## 1. 视觉主题与氛围

企业级后台业务设计系统，适用于管理后台、工作台、表单页、数据表格等信息密集型页面。清晰优先，结构层次优先于装饰表达。

- **视觉风格：** 清晰、专业、以信息为导向
- **色彩立场：** 强调色 + 语义色（错误/警告/成功/信息）+ 中性布局色
- **设计意图：** 每个视觉决策都应服务于内容可读性和任务效率

## 2. 色彩

### Token 命名

Color token 遵循固定的维度顺序：`type-object-attribute-intention-prominence-state`。

| 维度 | 取值 |
|------|------|
| object | `layout`（页面级背景，不透明）/ `container`（卡片、面板，允许半透明） |
| attribute | `bg` / `border` / `text` / `divider` |
| intention | `accent` / `error` / `warning` / `success` / `info` / `neutral` |
| prominence | `regular` / `light` / `subtle`（语义组）— `bright` / `lightgray` / `gray` / `inverse`（中性组） |
| state | `hover` / `active` |

### Intention 与 Prominence 分组

**语义组**（intention = accent/error/warning/success/info）：
- `regular` — 强对比，主操作按钮、状态文字
- `light` — 浅色背景色、弱强调边框
- `subtle` — 大面积背景区分（仅 accent）

**中性组**（intention = neutral）：
- `bright` — 默认白色表面（不透明）
- `lightgray` — 微对比容器背景（半透明）
- `gray` — 布局/容器背景，或浅色表面上的文字（搭配数字 10-50）
- `inverse` — 深色反转区域，或深色表面上的文字（搭配数字 20-50）

### 关键色值

- 强调色 regular: `#1966ff`
- 布局页面背景: `#f3f4f6`
- 容器卡片背景: `#ffffff`
- 中性文字: `rgba(19, 34, 64, 0.95)`（gray50）递减至 `0.25`（gray10）
- 中性边框: `rgba(19, 34, 64, 0.15)`
- 中性分割线: `rgba(19, 34, 64, 0.1)`

中性背景、边框、文字色大量使用半透明叠加。这使得元素在嵌套表面中保持稳定对比度，无需为不同背景色配置多套 token。

## 3. 字体排版

**字号阶梯：** 12 / 14 / 16 / 18 / 20 / 24 / 32

**object 分类：**
- `heading` — 标题，index 1-7（1 最大）
- `body` — 正文，默认 14px
- `paragraph` — 长文阅读
- `auxiliary` — 辅助文字、标签、元数据

**字重：** 400（常规）、600（加粗）
**行高：** 1.37（紧凑）、1.6（常规）、1.75（宽松）

**字体族：** 系统原生优先 — `-apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", Arial, sans-serif`。

## 4. 间距

基于 4px 栅格。Scale：0 / 4 / 8 / 12 / 16 / 20 / 24 / 32 / 40 / 48 / 64 / 80 / 160。

### Surface 与 Wrapper

- **Surface（视觉承载层）** — 至少具备一种视觉边界的容器：背景色 / 边框 / 阴影。Surface 拥有 `padding`。
- **Wrapper（纯布局层）** — 仅用于排列分组的容器，本身不产生可见的区块边界。Wrapper 使用 `itemSpacing` 控制间距，默认 `padding: 0`。

**规则：** 同一个视觉边界只由一层承担 padding。内层 Wrapper 通过 `itemSpacing` 控制排列，不叠加 padding。

### 分隔手段优先级

区块需要区分时，从弱到强选择：
1. 标题 + 间距（同一 Surface 内）
2. Divider 分割线（同一 Surface 内章节划分）
3. 新 Surface — 至少选用一项：对比背景色 / 边框 / 阴影

## 5. 圆角

| Token | 值 | 用途 |
|-------|-----|------|
| `small` | 4px | 标签、小按钮、复选框 |
| `regular` | 6px | 输入框、按钮、选择器、下拉菜单 |
| `large` | 12px | 卡片、弹窗、Banner |

## 6. 阴影

两个维度：`size`（大小）× `direction`（方向）。

**Size：** `small`（toast、tooltip）→ `regular`（下拉菜单、浮层）→ `large`（弹窗、对话框）→ `special1/2/3`（特定业务语义：浮动主按钮、吸底操作区、工作台核心卡片）。

**Direction：** `top` / `right` / `bottom` / `left`。

## 7. 布局与组合

后台业务页面默认结构：

```
页面 (layout-bg-neutral-gray)
├── 主 Surface (container-bg-neutral-bright + border-neutral + shadow-regular-bottom)
│   ├── 页面标题 (heading-regular-3)
│   ├── 章节 (spacing-6 分隔)
│   │   ├── 章节标题 (heading-regular-5)
│   │   └── 内容 (spacing-4 itemSpacing)
│   └── 章节 ...
```

桌面端推荐默认值：
- 页面内边距：`spacing-7`(32) 或 `spacing-8`(40)
- 卡片/Surface 内边距：`spacing-6`(24)
- 章节间距：`spacing-6`(24)；章节标题与内容：`spacing-3`(12)
- 字段列表 itemSpacing：`spacing-4`(16)
- Label 与控件：`spacing-2`(8)

## 8. 反模式

- 禁止给无视觉边界的容器设置 `padding >= 16`。将 padding 上移到最近的 Surface，或改为 `itemSpacing`。
- 禁止连续两层 Surface 都具有较大 padding，造成"无边界留白叠加"。
- 禁止使用 token 体系之外的配色。
- 禁止所有文字使用同一字号和字重，导致层级扁平。
- 禁止添加装饰性效果（大面积渐变、厚重阴影、超大圆角、玻璃拟态）。本系统刻意保持克制。
