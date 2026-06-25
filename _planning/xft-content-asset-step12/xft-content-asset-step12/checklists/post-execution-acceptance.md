# 执行后验收清单

## 1. 文件结构

- [ ] `.claude/skills/xft-design/assets/content-assets/regions/` 存在
- [ ] `.claude/skills/xft-design/assets/content-assets/modules/` 存在
- [ ] `.claude/skills/xft-design/assets/content-assets/feedback/` 存在
- [ ] `.claude/skills/xft-design/assets/content-assets/states/` 存在
- [ ] `.claude/skills/xft-design/assets/content-assets/overlays/` 存在
- [ ] `.claude/skills/xft-design/assets/content-assets/component-combos/` 存在
- [ ] `.claude/skills/xft-design/assets/content-assets/_support/` 存在

## 2. 数据与脚本

- [ ] `.claude/skills/xft-design/data/content-assets/content-assets.csv` 存在
- [ ] `.claude/skills/xft-design/data/content-assets/asset-rules.csv` 存在
- [ ] `.claude/skills/xft-design/data/content-assets/asset-keywords.csv` 存在
- [ ] `.claude/skills/xft-design/data/content-assets/recipe-rules.csv` 存在
- [ ] `.claude/skills/xft-design/scripts/search_content_assets.py` 存在

## 3. Skill 工作流

- [ ] `SKILL.md` 已备份旧版本
- [ ] `SKILL.md` 包含 `ROUTE_DECISION`
- [ ] `SKILL.md` 包含 `CONTENT_ASSET_DECISION`
- [ ] `SKILL.md` 明确禁止无资产决策直接生成页面
- [ ] `SKILL.md` 明确不允许自由新建布局 class
- [ ] `SKILL.md` 明确旧 `page-blocks.html` 只是 fallback

## 4. 检索测试

- [ ] 8 条测试用例均能返回 JSON
- [ ] JSON 包含 `page_type`
- [ ] JSON 包含 `recipe_id`
- [ ] JSON 包含 `read_order`
- [ ] `read_order` 中所有路径真实存在
- [ ] 没有出现空资产决策

## 5. 生成测试

- [ ] 列表页使用区域资产，不是自由写布局
- [ ] 详情页使用审批流/操作记录模块资产
- [ ] 表单页使用表单分组和底部操作资产
- [ ] 设置页使用设置布局和设置项资产
- [ ] 弹窗需求没有扩写成完整页面
- [ ] 空状态没有替代整个页面结构

## 6. 安全边界

- [ ] 未修改 `tokens.css`
- [ ] 未重写 shell 主结构
- [ ] 未删除旧资产
- [ ] 未引入外部依赖
- [ ] 未把图片素材直接放进 skill 让 AI 阅读
