# 第 12 步：执行后验证与补齐包

本包用于 Codex / Agent 完成第 11 步项目改造后，对 `xft-design` Skill 进行验收、回归测试、缺口登记和补齐。

## 使用位置

放到：

```text
项目根目录/_planning/xft-content-asset-step12/
```

## 使用时机

只有在第 11 步已经由 Codex / Agent 执行完成后使用。
如果还没有执行第 11 步，本包只作为后续验收工具备用。

## 核心文件

```text
scripts/verify_xft_content_asset_integration.py   自动验收脚本
scripts/run_step12_validation.sh                  一键验收命令
data/validation-test-cases.csv                    验收用例
checklists/post-execution-acceptance.md           人工验收清单
references/step12-validation-and-gap-fill.md      验证与补齐说明
references/issue-classification.md                问题分类与处理策略
prompts/agent-validation-prompt.md                给 Agent 的验证提示词
prompts/agent-gap-fix-prompt.md                   给 Agent 的补齐修复提示词
_reports/gap-backlog-template.csv                 缺口登记模板
```

## 下一步操作

1. 先让 Codex 执行第 11 步改造。
2. 执行完成后，把本包放到 `_planning/xft-content-asset-step12/`。
3. 给 Agent 读取 `prompts/agent-validation-prompt.md`。
4. Agent 运行 `scripts/run_step12_validation.sh`。
5. 把报告、报错、生成页面效果发回给人工复核。
