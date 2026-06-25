# XFT 内容资产 Step 9：检索与排序方法

## 本步定位

本步不是新增 HTML 资产，而是定义“如何根据需求找到资产”。

它把第 8 步统一数据转成可运行的检索管道：

```text
用户需求
→ 页面类型路由
→ 页面配方选择
→ 必选资产补齐
→ 可选资产检索
→ 规则过滤与排序
→ CONTENT_ASSET_DECISION
```

## 文件结构

```text
scripts/
  search_content_assets.py                 # 可运行检索原型

data/
  content-assets.csv                       # 第 8 步统一资产表
  page-type-router.csv                     # 页面类型路由
  recipe-rules.csv                         # 页面配方规则
  recipe-asset-map.csv                     # 配方与资产映射
  asset-rules.csv                          # 资产规则
  asset-keywords.csv                       # 关键词索引
  support-css-manifest.csv                 # CSS 支持文件清单
  search-config.json                       # 检索配置
  search-field-weights.csv                 # 检索字段权重
  asset-selection-thresholds.csv           # 选择阈值
  conflict-resolution-rules.csv            # 冲突处理规则

references/
  search-and-ranking-method.md             # 检索方法说明
  content-asset-decision-format.md         # 决策输出格式
  search-pipeline-test-cases.md            # 测试用例
  codex-integration-notes-step9.md         # 接入说明

examples/
  decision-table-page.json                 # 列表页决策示例
  decision-approval-detail.json            # 审批详情页决策示例
  decision-formula-settings.json           # 公式配置页决策示例
  search-input-examples.json               # 输入样例

_tests/
  run_search_smoke_tests.sh                # 冒烟测试
```

## 如何本地验证

```bash
cd xft-content-asset-step9
bash _tests/run_search_smoke_tests.sh
```

或直接执行：

```bash
python3 scripts/search_content_assets.py "生成员工花名册列表页，支持筛选和批量导出" --data-dir data --pretty
```

## 当前是否可以让 Agent 执行改项目？

还不建议。

原因：第 10 步会重写 `SKILL.md` 工作流。  
第 9 步只是“检索方法和脚本原型”。

## 你现在应该怎么放

```text
项目根目录/_planning/xft-content-asset-step9/
```

等第 10 步完成后，再让 Agent 按第 9 + 第 10 步一起改项目。
