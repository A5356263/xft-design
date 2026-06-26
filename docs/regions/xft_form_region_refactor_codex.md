# XFT Form Region 统一重构执行文档（Codex版）

## 目标
将 form-region 从多模板结构重构为单 Form + mode 驱动系统。

## 当前问题
- 多HTML模板：basic-section / horizontal / multi-section / summary-card / footer-actions
- 布局逻辑分散
- footer 独立导致结构断裂
- summary-card 属于 readonly region，不应归属 form

## 重构方案

### 1. 单入口结构
仅保留：
/assets/content-assets/regions/form-region/base.html

### 2. mode 控制布局
- basic
- horizontal
- multi
- summary(readonly)

通过 data-mode 控制

### 3. 删除文件
- basic-section.html
- horizontal.html
- multi-section.html
- summary-card.html
- footer-actions.html

### 4. 结构规范
Form = Region（区域）
Layout = mode
Field = typed schema

### 5. footer 规则
必须合并入 Form 内部 ActionZone

### 6. summary 迁移
summary-card → summary-region

## 验收标准
- 单 form-region 文件
- 无多模板结构
- mode 正常生效
- skill 测试全 PASS
