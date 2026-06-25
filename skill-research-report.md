# Skill 研究报告：ui-ux-pro-max vs shadcn/ui vs ant-design-pro

> 2026-06-23，基于 `ui-ux-pro-max-skill-main`（v2.5.0）、`ui`（shadcn/ui v4.11.0）和 `ant-design-pro`（v6）源码分析。

---

## 一、一句话定位

| Skill | 一句话 |
|-------|--------|
| ui-ux-pro-max | 设计知识检索系统：根据产品类型查表匹配风格/配色/字体/动效，输出设计参数 |
| shadcn/ui | 组件使用规范引擎：通过 CLI 获取组件 + 规则文件约束代码写法，保障 API 正确性 |
| ant-design-pro | **B 端页面脚手架**：提供 10+ 种企业级页面类型的完整代码模板，自带两个 skill（antd 组件查询 + pro 框架升级） |

---

## 二、文件规模对比

| | ui-ux-pro-max | shadcn/ui |
|---|---|---|
| 仓库总文件数 | ~330 | ~9000+（monorepo） |
| Skill 核心文件 | 3 个 Python + 31 个 CSV + 1 个 SKILL.md | 1 个 SKILL.md + 5 个 rules/*.md + 8 个辅助 .md |
| 真正的知识量 | CSV 约 6,500 行结构化数据 | Markdown 约 35 条规则（每条含正确/错误代码对照） |
| 为什么文件多 | 多平台分发系统：cli/ 打包器 + templates/ 适配器 + .claude/ 本地入口 | monorepo：apps/ 文档站 + packages/ CLI 工具 + skills/ 技能定义 |

---

## 三、知识存储方式和粒度

### ui-ux-pro-max：CSV 结构化数据库

**为什么用 CSV：** 纯文本表格，带列名。Excel 能编辑、Python 能解析、Git 能 diff、人眼能直接读。AI 和脚本都能按"列"提取结构化信息（如"产品类型→推荐颜色"），而纯自然语言文本做不到。

**数据分布在 4 层：**

| 层级 | 文件 | 一行 = 什么 | 粒度 |
|------|------|-----------|------|
| 产品映射 | `products.csv`（161行） | 一种产品类型的推荐风格/落地页模式/配色重点 | 宏观方向，一句话级别 |
| 推理调度 | `ui-reasoning.csv`（161行） | 产品类别→风格优先级+配色情绪+反模式 | 调度指令（决定"去哪张表找什么"） |
| 设计参数 | `styles.csv`（84行）+ `colors.csv`（160行）+ `typography.csv`（73行） | 风格20+列/CSS代码/检查清单；16个语义色 Hex 值；字体+Google Fonts URL+CSS Import | 精确到 `#2563EB`、`150-300ms`、可直接粘贴的代码 |
| 实现规则 | `ux-guidelines.csv`（98行）+ `stacks/*.csv`（17个×~50行） | 单一 UX 问题 Do/Don't + 好代码/坏代码；技术栈最佳实践 | 代码级对比 |

### shadcn/ui：Markdown 规则文件 + 远程组件库

**知识分散在三个地方，只有规则在本地：**

| 位置 | 内容 | 谁维护 |
|------|------|--------|
| `skills/shadcn/rules/*.md`（本地） | ~35 条组件使用规则，每条=一句话禁令+错误代码+正确代码 | shadcn 团队 |
| npm: `shadcn` 包（远程，运行时 npx 拉） | CLI 逻辑（add/search/docs/info 等命令） | shadcn 团队 |
| `ui.shadcn.com/r/`（远程注册表） | 每个组件的源码、示例、文档 | shadcn 团队 + 社区 |

**规则的格式就是代码级正误对照：**

```tsx
// ❌ 错误
<SelectContent>
  <SelectItem value="apple">Apple</SelectItem>
</SelectContent>

// ✓ 正确
<SelectContent>
  <SelectGroup>
    <SelectItem value="apple">Apple</SelectItem>
  </SelectGroup>
</SelectContent>
```

---

## 四、工作流程对比

### ui-ux-pro-max：4 步查表匹配管道

```
用户需求: "做一个员工花名册管理页面"
    │
    ▼
Step 1: AI 提取关键词 → "employee roster management tool"
    │
    ▼
Step 2: 跑 python search.py "..." --design-system
    │
    ├─ ① 搜 products.csv → 确定产品类别: "Productivity Tool"
    ├─ ② 查 ui-reasoning.csv → 得到调度指令:
    │     style_priority = ["Flat Design", "Micro-interactions"]
    │     color_mood = "Clear hierarchy + Functional colors"
    │     pattern = "Interactive Demo + Feature-Rich"  ← 只是个 3 词标签
    │     注: color_mood 和 typography_mood 不参与搜索，仅展示
    ├─ ③ 并行搜索 5 表（styles/colors/landing/typography/product）
    │     其中 styles 的查询词被 style_priority 增强
    ├─ ④ 关键词打分精选最佳行
    └─ ⑤ 拼装输出：pattern + style + colors + typography + effects + anti_patterns
    │
    ▼
Step 3: 补充搜索 --domain ux / --domain chart / --stack react
    │
    ▼
Step 4: AI 综合所有结果 → 写代码
```

**关键发现：中间完全是确定性查表，不是 AI 推理。** BM25 是数学公式打分，reasoning 是预填的 switch-case 映射表（人类设计师提前写好"Productivity Tool → Flat Design"），AI 只在两端起作用（关键词提取、代码生成）。

### shadcn/ui：CLI + 规则约束管道

```
用户需求: "做一个员工花名册管理页面"
    │
    ▼
① 获取项目上下文
    npx shadcn@latest info --json
    → 别名、Tailwind 版本、底层库类型、图标库、已安装组件列表
    │
    ▼
② AI 查固定选型表（SKILL.md 内置）→ 确定需要哪些组件
    │ 数据展示 → Table, Card, Badge
    │ 表单输入 → Input, Select, Combobox
    │ 覆盖层 → Dialog, Sheet, Drawer
    │ ...
    ▼
③ 检查已安装 vs 缺失 → npx shadcn@latest search 查找 → npx shadcn add 安装
    │
    ▼
④ 查组件文档和示例
    npx shadcn@latest docs button dialog table
    → 返回文档 URL 和示例 URL → AI fetch 阅读
    │
    ▼
⑤ AI 写代码 ← 实时对照 rules/*.md 约束
    ├── styling.md: className 只用于布局，不许覆盖颜色
    ├── composition.md: SelectItem 必须在 SelectGroup 内
    ├── forms.md: 表单必须用 FieldGroup + Field
    └── icons.md: Button 内图标必须加 data-icon
    │
    ▼
⑥ 交付前检查：组件组合是否正确、导入路径是否匹配别名
```

**关键发现：CLI 负责"拿来"（获取组件、配置、文档），Skill 负责"用对"（规范代码写法）。** AI 在这里参与了更多决策——自己读规则、自己对照检查，而不是等一个脚本输出结果。

---

## 五、"推理"的本质

| | ui-ux-pro-max | shadcn/ui |
|---|---|---|
| 什么是"推理" | 人类预填的 161 条"产品→风格"映射，运行时字符串匹配查表 | AI 读规则文件后自己做判断 |
| 脚本/AI 分工 | Python 做匹配打分，AI 做关键词提取和代码生成 | CLI 做组件获取，AI 做组件选择和代码合规 |
| 能否叫"推理" | 不能。是确定性查表，0 个环节是 AI "想"出来的 | 部分能。组件选型和不犯错是 AI 判断的 |

---

## 六、对 B 端产品的适配评估

### ui-ux-pro-max：弱

- landing.csv 的 34 个模式全部是营销落地页（Hero + Features + CTA 等）
- **零个**数据表格模式、详情页模式、审批流模式、仪表盘布局模式
- "员工花名册"会被匹配到 "Feature-Rich Showcase"（一个营销页模式），完全不对
- 配色和字体推荐仍然可用，但页面结构指导完全缺失

### shadcn/ui：中

- 组件注册表包含 B 端必备组件：Table、Form 体系（FieldGroup/InputGroup）、Sheet/Drawer、Command、Chart、Sidebar
- 但**没有页面结构/区域布局的指导**——管"组件怎么用对"，不管"页面怎么搭"
- 数据表格的工具栏布局、详情页的信息架构、审批流的步骤编排，仍然靠 AI 经验

### 两者的共同空白

**B 端真正需要但两个 skill 都没给的：**

```
页面类型层   →  数据表格页 / 表单页 / 详情页 / 仪表盘 / 审批流 / 权限配置
区域布局层   →  工具栏区 / 筛选区 / 表格区 / 分页区 的排列和间距规则
组件组合层   →  "搜索框 + 筛选按钮 + 批量操作栏" 的元组组合关系
微观排版层   →  标签对齐方式、列数分布、行内操作按钮位置
```

ui-ux-pro-max 只到"整个产品的风格"层面，shadcn 只到"单个组件的 API"层面，两者之间的**页面结构和区域布局层是空白**。

---

## 七、核心差异总结

| 维度 | ui-ux-pro-max | shadcn/ui |
|------|--------------|-----------|
| **性质** | 设计知识检索系统 | 组件使用规范引擎 |
| **知识形式** | CSV 数据库（6500 行） | Markdown 规则（35 条）+ 远程组件库 |
| **知识归属** | 全部自持（离线可用） | 分散三地（在线依赖） |
| **检索/匹配方式** | Python BM25 搜索引擎 | CLI 工具 + AI 判断 |
| **决策粒度** | 产品级："这个产品用什么风格/配色/字体" | 组件级："这个组件怎么组合使用" |
| **输出形式** | 设计参数（Hex 值、字体名、动效时长） | 代码约束（不许手写样式、必须用语义色） |
| **AI 参与程度** | 低：入口提取关键词 + 出口写代码 | 中：读规则→做判断→自我检查 |
| **对 B 端覆盖** | 弱：34 种营销页模式 | 中：有 B 端组件但无页面结构 |
| **更新机制** | 改 CSV 提交 Git | 改规则文件提交 Git + 远程组件独立发版 |
| **多平台支持** | 19 个 AI 编码平台（通过模板系统） | Claude Code 专用（通过 CLI + MCP） | Claude Code（2 个 skill） |
| **适用场景** | "不知道该做成什么风格" | "知道要做什么但怕把 shadcn 用错" | "做 B 端项目但不想从零写页面" |

---

## 八、ant-design-pro 专项分析：填补 B 端页面结构空白

### 定位

ant-design-pro **不是一个 skill，而是一个 B 端项目模板**。它自带两个 skill，但它们的职责不同：

| Skill | 性质 | 做什么 |
|-------|------|--------|
| `/antd` | 组件 API 工具（类似 shadcn 的 CLI） | 查 antd 组件的 props/demo/token/migrate/lint——永远不靠记忆写 API |
| `/pro-upgrade` | 框架迁移工具 | 自动对比最新模板 → diff → 合并框架文件 → 保留业务代码 |

**真正的"知识"不在 skill 文件里，而在 `src/pages/` 的页面模板里。**

### 页面类型完整度

ant-design-pro 的 `config/routes.ts` 定义了完整的 B 端路由树，对应 `src/pages/` 下的实现：

```
src/pages/
├── dashboard/                 ← 仪表盘（3种）
│   ├── analysis/              → 分析仪表盘（指标卡片 + 图表网格 + 趋势）
│   ├── monitor/               → 监控仪表盘（实时数据 + 状态指示）
│   └── workplace/             → 工作台（待办 + 快捷入口 + 动态）
│
├── form/                      ← 表单页（3种）
│   ├── basic-form/            → 基础表单（单列布局，简单数据项）
│   ├── step-form/             → 分步表单（步骤指示器 + 分布验证）
│   └── advanced-form/         → 高级表单（多分组 + 动态表单项 + 复杂验证）
│
├── list/                      ← 列表/表格页（4种）
│   ├── table-list/            → 数据表格（ProTable + 批量操作 + CRUD 抽屉）
│   ├── basic-list/            → 基础列表
│   ├── card-list/             → 卡片列表
│   └── search/                → 搜索列表（含 articles/projects/applications）
│
├── profile/                   ← 详情页（2种）
│   ├── basic/                 → 基础详情（Descriptions + 信息分组）
│   └── advanced/              → 高级详情（多 Tab + 表格嵌套 + 步骤时间线）
│
├── result/                    ← 结果页（2种）
│   ├── success/               → 操作成功（反馈卡片 + 下一步引导）
│   └── fail/                  → 操作失败（错误信息 + 重试入口）
│
├── exception/                 ← 异常页（3种）
│   ├── 403/                   → 无权限
│   ├── 404/                   → 页面不存在
│   └── 500/                   → 服务器错误
│
├── account/                   ← 账户管理（2种）
│   ├── center/                → 个人中心
│   └── settings/              → 个人设置
│
└── user/                      ← 登录/注册（3种）
    ├── login/                 → 登录
    ├── register/              → 注册
    └── register-result/       → 注册结果
```

**这就是 B 端页面结构知识。** 每个目录不是一个配置项，而是一个**可运行的完整页面**，包含 index.tsx + service.ts + 子组件 + 样式。

### 页面实现粒度的实际案例

以 **table-list（数据表格页）** 为例，它的结构是：

```
table-list/
├── index.tsx              ← 主页面（ProTable 配置 + 行选择 + 批量操作）
├── components/
│   ├── CreateForm.tsx     ← 新建抽屉表单
│   └── UpdateForm.tsx     ← 编辑抽屉表单
└── index.test.tsx         ← 带测试
```

`index.tsx` 里包含的 B 端表格页面完整逻辑：

```
工具栏区域   → ProTable 内置：新建按钮 + 批量删除 + 搜索输入框
表格区域     → ProColumns 定义：列排序/筛选/渲染/链接跳转
行操作       → 编辑按钮（打开 UpdateForm 抽屉）+ 删除按钮
批量操作     → 多选后底部 FooterToolbar 浮现
详情抽屉     → ProDescriptions 展示选中行完整信息
状态管理     → @tanstack/react-query 处理增删改的缓存失效
```

**这是"组件组合关系"的具体实践：** Table + Toolbar + Drawer + Form + FooterToolbar 的完整编排。

以 **advanced-form（高级表单页）** 为例：

```
区域布局     → ProForm + Card 分组：主体信息 / 企业信息 / 发票信息
列数分布     → 单列 vs 双列字段按内容长度自适应
表单控件     → Input / Select / DatePicker / Radio / Upload 等10+种
联动逻辑     → ProFormDependency 实现字段间关联
动态表单     → ProFormList 支持增删行
```

### skill 与模板的关系

```
/antd skill                         /pro-upgrade skill
    │                                    │
    │ "查 antd 组件的正确 API"            │ "保持框架代码与上游同步"
    │                                    │
    ▼                                    ▼
与 shadcn 的 CLI 同类型              ant-design-pro 独有
——保障实现正确性                      ——保障项目可升级
    │                                    │
    └──────────┬────────────────────────┘
               │
               ▼
    都服务于同一个模板的页面代码
            src/pages/
    （B 端页面结构和区域布局的真正知识所在）
```

### 跟前面两个 skill 的本质对比

| | ui-ux-pro-max | shadcn/ui | ant-design-pro |
|---|---|---|---|
| **知识形态** | CSV 数据行 | Markdown 规则 | **完整页面代码** |
| **覆盖层级** | 产品级风格决策 | 组件级 API 正确性 | **页面级结构 + 区域布局 + 组件组合** |
| **B 端覆盖** | 弱（34种营销页） | 中（有组件无页面） | **强（10+种页面类型）** |
| **可执行性** | 输出建议文本 | 约束代码写法 | **可直接运行的工程代码** |
| **对 AI 的价值** | 告诉 AI 用什么颜色 | 告诉 AI 组件怎么组合 | **给 AI 看一个完整页面长什么样** |

### 三者的完整拼图

```
ui-ux-pro-max                 shadcn/ui                    ant-design-pro
    │                            │                              │
    │ "做成什么样"                │ "怎么写对"                    │ "页面怎么搭"
    │                            │                              │
    ▼                            ▼                              ▼
设计决策层                    实现规范层                      页面结构层
  ├─ 风格选择                   ├─ 组件 API 正确性              ├─ 表格页模板
  ├─ 配色方案                   ├─ 组合嵌套规则                 ├─ 表单页模板
  ├─ 字体配对                   ├─ 样式约束                    ├─ 详情页模板
  └─ 动效参数                   └─ 图标使用规范                 ├─ 仪表盘模板
                                                               ├─ 异常页模板
                                                               └─ 结果页模板
    │                            │                              │
    └────────────┬───────────────┴──────────────┬──────────────┘
                 │                              │
                 ▼                              ▼
       之前报告说的"共同盲区"              被 ant-design-pro 填上了
```

### ant-design-pro 的局限

1. **技术栈绑定**：只适用于 antd + Umi 技术栈。不用 antd 的项目无法复用。
2. **页面模板是代码，不是知识**：AI 需要读代码理解模式，而不是查表获取结构化建议。知识提取依赖 AI 的理解能力。
3. **没有搜索/匹配机制**：ui-ux-pro-max 有 BM25 搜索引擎，shadcn 有 CLI 搜索注册表，antd-pro 全靠 AI 自己读文件找合适的页面模板。
4. **页面的"为什么"缺失**：模板写好了怎么做，但没解释为什么这样做——为什么工具栏在左侧、搜索框在右侧、批量操作在底部浮现。

---

## 九、三者的关系总结

```
ui-ux-pro-max            shadcn/ui               ant-design-pro
    │                       │                        │
    │ "做成什么样"           │ "怎么写对"              │ "页面怎么搭"
    │                       │                        │
    ▼                       ▼                        ▼
设计决策层              实现规范层                页面结构层
  ├─ 风格选择              ├─ 组件 API               ├─ 表格页完整模板
  ├─ 配色方案              ├─ 组合规则               ├─ 表单页完整模板
  ├─ 字体配对              └─ 样式约束               ├─ 详情页完整模板
  └─ 动效参数                                        ├─ 仪表盘完整模板
                                                     ├─ 异常/结果页模板
                                                     └─ 登录/账户模板
    │                       │                        │
    └───────────┬───────────┴───────────┬────────────┘
                │                       │
                ▼                       ▼
       ui-ux-pro-max +                ant-design-pro
       shadcn 共同的盲区              填补了这个盲区
```

三者拼接后，**"设计决策 → 实现规范 → 页面结构"** 的链路闭合。

---

## 十、附录：CSV 数据实录（摘选）

CSV 就是带列名的纯文本表格——用逗号分隔列、换行分隔行，拿 Excel 能编辑、拿 Python 能解析、拿 git 能 diff、拿眼睛能直接读。

`src/ui-ux-pro-max/data/` 下各文件的核心内容摘录：

```
products.csv (161行):     E-commerce Luxury → Liquid Glass + Glassmorphism / Premium colors
                          Financial Dashboard → Dark Mode (OLED) + Data-Dense
                          Healthcare App → Neumorphism + Accessible & Ethical

ui-reasoning.csv (161行): B2B Service → Trust & Authority+Minimalism / "must_have: case-studies, roi-messaging"
                          Fintech → Minimalism+Accessible & Ethical / "must_have: security-first"
                          Productivity Tool → Flat Design+Micro-interactions / "if_collaboration→add-real-time-cursors"

styles.csv (84行×21列):   Minimalism & Swiss Style: 关键词=grid-based/functional, 主色=#000+#FFF,
                          动效=Subtle hover 200-250ms, 性能=Excellent, 无障碍=WCAG AAA,
                          CSS关键词=display:grid/gap:2rem, 设计变量=--spacing:2rem/--shadow:none

colors.csv (160行×16色):  SaaS: Primary #2563EB, Accent #EA580C, Background #F8FAFC
                          CRM: Primary #2563EB, Accent #059669, Notes="Professional blue+deal green"

typography.csv (73行):    Minimal Swiss: Inter/Inter → @import url('https://fonts.googleapis.com/...')

landing.csv (34行):       Hero+Features+CTA: 1.Hero→2.Value prop→3.Features(3-5)→4.CTA→5.Footer
                          (注：全部34个均为营销页模式，0个B端数据表格/详情页模式)

ux-guidelines.csv (98行): Table Handling: Do="overflow-x-auto wrapper", Don't="table overflows viewport"
                          Bulk Actions: Do="Checkbox column+Action bar", Don't="single row actions only"

stacks/react.csv (53行):  Use keys properly: Do=key={item.id}, Don't=key={index}, Severity=High
                          Memoize: Do=useMemo(() => expensive(), [deps]), Don't=recalculate every render

charts.csv (25行):        Trend→Line Chart, <1000pts:SVG ≥1000:Canvas → Chart.js/Recharts, 无障碍AA
                          Compare→Bar Chart, <20:vertical 20-50:horizontal >50:table → 无障碍AAA
```

核心结构化数据合计约 **6,500 行**，均为 AI 和脚本可直接按列读取的结构化数据。

