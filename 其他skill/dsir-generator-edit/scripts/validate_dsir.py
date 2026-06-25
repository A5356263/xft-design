import json, sys
from pathlib import Path

ALLOWED_PAGE_TYPES = {"list-management", "detail-overview", "dashboard-analysis"}
ALLOWED_SECTION_ROLES = {"shell_header", "route_nav_bar", "shell_navigation", "sidebar", "primary_content"}
ALLOWED_BLOCK_PATTERNS = {"category_tree", "filter_form", "action_cluster", "local_primary_action", "record_table", "pagination_footer", "view_switcher", "metric_group"}
ALLOWED_CONTENT_MODELS = {"hierarchical_options", "query_conditions", "action_set", "single_primary_action", "record_collection", "pagination_context", "view_options", "scalar_metrics"}

path = Path(sys.argv[1])
data = json.loads(path.read_text(encoding="utf-8"))
for page in data.get("pages", []):
    assert page.get("page_type") in ALLOWED_PAGE_TYPES, f"unknown page_type: {page.get('page_type')}"
    for section in page.get("sections", []):
        assert section.get("section_role") in ALLOWED_SECTION_ROLES, f"unknown section_role: {section.get('section_role')}"
        for block in section.get("blocks", []):
            assert block.get("block_pattern") in ALLOWED_BLOCK_PATTERNS, f"unknown block_pattern: {block.get('block_pattern')}"
            cm = block.get("semantic_payload", {}).get("content_model_ref")
            assert cm in ALLOWED_CONTENT_MODELS, f"unknown content_model_ref: {cm}"
print("VALID")
