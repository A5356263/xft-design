#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SCRIPT="$ROOT/scripts/search_content_assets.py"
DATA="$ROOT/data"

python3 "$SCRIPT" "生成员工花名册列表页，支持姓名、组织、状态筛选，支持批量导出和查看详情" --data-dir "$DATA" --pretty >/tmp/xft-table-decision.json
python3 "$SCRIPT" "生成审批单详情页，需要展示基础信息、审批流、附件和操作记录" --data-dir "$DATA" --pretty >/tmp/xft-detail-decision.json
python3 "$SCRIPT" "生成公式配置页面，支持字段选择、公式编辑、智能助手和保存发布" --data-dir "$DATA" --pretty >/tmp/xft-settings-decision.json

python3 - <<'PY'
import json
cases = [
    ('/tmp/xft-table-decision.json', 'TablePage'),
    ('/tmp/xft-detail-decision.json', 'DetailPage'),
    ('/tmp/xft-settings-decision.json', 'SettingsPage'),
]
for path, expected in cases:
    data = json.load(open(path, encoding='utf-8'))
    assert data['decision_type'] == 'CONTENT_ASSET_DECISION'
    assert data['page_type'] == expected, (path, data['page_type'], expected)
    assert data['assets'], path
print('PASS: search smoke tests')
PY
