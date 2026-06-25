# Step 7 组件组合规则

## 定位

本步处理按钮规则、数据录入控件、展示型组件组合。目标不是复刻单组件 API，而是沉淀 AI 可直接装配的“组件组合片段”。

## 核心规则

1. 控件不得裸放，必须进入字段组：label + control + help/error。
2. 按钮不得自由排布，必须进入 Header / Toolbar / Body / Footer 四类操作区。
3. 同一操作组只能有一个主按钮。
4. Switch 表示即时生效；需要提交确认时使用 Checkbox / Radio / Form Footer。
5. Tooltip 只放短说明；Popover 可放轻量内容；复杂配置升级 Drawer。
6. 展示组件不承载关键业务提交。

## 后续进入正式 skill 时

- `assets/component-combos/_component-combo-support.css` 需要作为组件组合补充样式插入。
- `data/component-combo-assets.csv` 参与内容资产检索。
- `data/component-combo-rules.csv` 参与规则过滤和校验。
