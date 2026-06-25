# 最终验收清单

## 目录验收

- [ ] `.claude/skills/xft-design/assets/content-assets/regions/` 存在
- [ ] `.claude/skills/xft-design/assets/content-assets/modules/` 存在
- [ ] `.claude/skills/xft-design/assets/content-assets/feedback/` 存在
- [ ] `.claude/skills/xft-design/assets/content-assets/states/` 存在
- [ ] `.claude/skills/xft-design/assets/content-assets/overlays/` 存在
- [ ] `.claude/skills/xft-design/assets/content-assets/component-combos/` 存在
- [ ] `.claude/skills/xft-design/data/content-assets/content-assets.csv` 存在
- [ ] `.claude/skills/xft-design/scripts/search_content_assets.py` 存在

## 工作流验收

- [ ] `SKILL.md` 版本为 `7.0`
- [ ] `SKILL.md` 包含 `CONTENT_ASSET_DECISION`
- [ ] `SKILL.md` 明确禁止无资产决策直接生成页面
- [ ] `SKILL.md` 明确条件读取规则
- [ ] `SKILL.md` 明确 HTML（超文本标记语言）装配顺序

## 检索验收

执行：

```bash
cd .claude/skills/xft-design
python3 scripts/search_content_assets.py "生成员工花名册列表页，支持筛选、批量导出和详情查看" --data-dir data/content-assets --pretty
python3 scripts/search_content_assets.py "生成审批详情页，包含审批流、基础信息和操作记录" --data-dir data/content-assets --pretty
python3 scripts/search_content_assets.py "生成公式编辑器配置页，包含公式编辑和智能辅助" --data-dir data/content-assets --pretty
```

- [ ] 三条命令均返回 JSON（数据格式）
- [ ] 返回结果包含 `page_type`
- [ ] 返回结果包含 `recipe_id`
- [ ] 返回结果包含 `read_order`
- [ ] `read_order` 中的路径真实存在

## 生成验收

- [ ] 最终 HTML 顶部包含 `XFT_ROUTE`
- [ ] 最终 HTML 包含 `CONTENT_ASSET_DECISION` 或对应决策记录
- [ ] 最终 HTML 没有残留 `PAGE_CONTENT_SLOT`
- [ ] 最终 HTML 没有残留 `CONTENT_SLOT`
- [ ] 最终 HTML 没有随机布局 class（类名）
- [ ] 最终 HTML 没有裸色值大面积新增
