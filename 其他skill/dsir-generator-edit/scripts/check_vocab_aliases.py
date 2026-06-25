import json
import sys
from pathlib import Path

GENUX_PAGE_TYPES = {"workspace_shell", "dashboard", "directory", "form", "detail", "reference_lab"}
GENUX_SECTION_ROLES = {"hero", "navigation", "summary", "filters", "content", "detail", "review", "actions"}
GENUX_BLOCK_PATTERNS = {
    "page-shell", "shell-side", "shell-main", "section-navigation", "card-group",
    "summary-panel", "metric-group", "action-cluster", "text-stack", "hero-panel",
    "descriptive-items", "record-collection", "record-table", "record-summary", "empty-placeholder"
}
GENERIC_ALIASES = {
    "list-management": "directory",
    "detail-overview": "detail",
    "dashboard-analysis": "dashboard",
    "shell_header": "hero",
    "route_nav_bar": "navigation",
    "shell_navigation": "navigation",
    "sidebar": "navigation",
    "primary_content": "content",
    "category_tree": "section-navigation",
    "filter_form": "descriptive-items",
    "local_primary_action": "action-cluster",
    "view_switcher": "action-cluster",
    "pagination_footer": "record-table",
    "record_table": "record-table",
    "metric_group": "metric-group",
    "action_cluster": "action-cluster",
}

path = Path(sys.argv[1])
data = json.loads(path.read_text(encoding='utf-8'))
violations = []
for page in data.get('pages', []):
    pt = page.get('page_type')
    if pt in GENERIC_ALIASES:
        violations.append(f"page_type still uses generic alias: {pt} -> {GENERIC_ALIASES[pt]}")
    for section in page.get('sections', []):
        sr = section.get('section_role')
        if sr in GENERIC_ALIASES:
            violations.append(f"section_role still uses generic alias: {sr} -> {GENERIC_ALIASES[sr]}")
        for block in section.get('blocks', []):
            bp = block.get('block_pattern')
            if bp in GENERIC_ALIASES:
                violations.append(f"block_pattern still uses generic alias: {bp} -> {GENERIC_ALIASES[bp]}")

if violations:
    raise AssertionError("; ".join(violations))
print("VOCAB_OK")
