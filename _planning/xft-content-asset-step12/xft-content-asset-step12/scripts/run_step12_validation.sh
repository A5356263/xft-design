#!/usr/bin/env bash
set -euo pipefail

ROOT="$(pwd)"
SKILL_DIR="$ROOT/.claude/skills/xft-design"
PLANNING_DIR="$ROOT/_planning/xft-content-asset-step12"

python3 "$PLANNING_DIR/scripts/verify_xft_content_asset_integration.py" \
  --skill-dir "$SKILL_DIR" \
  --test-cases "$PLANNING_DIR/data/validation-test-cases.csv" \
  --report "$PLANNING_DIR/_reports/validation-report.generated.json"
