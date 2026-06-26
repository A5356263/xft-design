# XFT Field资产化 + Schema数据驱动生成（执行规范）

---

# 1. Field（字段资产化）

## 1.1 目标

将字段从“HTML写死结构”升级为“可组合资产单元”。

---

## 1.2 Field定义

Field = 最小UI单元资产

不包含布局，仅包含语义与表现规则。

---

## 1.3 Field标准结构

{
  type: string,          # field.text / field.select / field.multi / field.date
  label: string,         # 展示名称
  required: boolean,      # 是否必填
  span: 1 | 2,           # 占列能力
  props: object          # 控件属性
}

---

## 1.4 Field类型库

- field.text
- field.select
- field.multiSelect
- field.textarea
- field.date
- field.switch

---

## 1.5 Field渲染规则

- Field不控制布局
- Field不包含HTML结构
- Field只描述语义 + 类型
- Layout（布局）由Region控制

---

## 1.6 Field输出规范

Field必须可以被映射为：

<div class="form-field span-{n}">
  <label>{label}</label>
  <div class="control">{render}</div>
</div>

---

# 2. Schema（数据驱动生成）

## 2.1 目标

用结构化数据驱动页面生成，而不是模板选择。

---

## 2.2 Schema定义

Schema = 页面生成的唯一输入源

---

## 2.3 Schema结构

{
  pageType: "form",
  region: "form-region",
  mode: "basic | horizontal | multi",
  fields: [
    {
      type: "field.text",
      label: "姓名",
      required: true,
      span: 1
    }
  ],
  actions: [
    {
      type: "button.primary",
      label: "提交"
    }
  ]
}

---

## 2.4 Schema驱动流程

1. 输入Schema
2. 选择Region（表单区域）
3. 选择Mode（布局模式）
4. Field映射Field Asset
5. Render HTML

---

## 2.5 Schema约束规则

- 不允许直接写HTML
- 不允许直接选择模板文件
- 只能选择Asset + 参数
- Layout必须由mode控制
- Field必须来自Field库

---

## 2.6 生成链路

Schema
  → Region（结构）
  → Mode（布局）
  → Field Assets（字段）
  → Render Engine（渲染器）

---

# 3. 核心原则

- Field = 数据单元，不是布局单元
- Schema = 唯一真相源
- HTML = 最终输出，不是输入
- Region = 容器
- Mode = 布局策略

---

# 4. 成功标志

- 无模板选择逻辑
- 无HTML驱动生成
- 无嵌套slot结构
- 所有UI来自Schema
