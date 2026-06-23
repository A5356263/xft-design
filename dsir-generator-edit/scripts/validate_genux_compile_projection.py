import json
import sys
from pathlib import Path

PAGE_TYPES = {"workspace_shell", "dashboard", "directory", "form", "detail", "reference_lab"}
LAYOUT_MODES = {"single_column", "two_column", "three_column", "shell_main"}
DENSITIES = {"comfortable", "compact", "dense"}
SECTION_ROLES = {"hero", "navigation", "summary", "filters", "content", "detail", "review", "actions"}
BLOCK_PATTERNS = {
    "page-shell", "shell-side", "shell-main", "section-navigation", "card-group",
    "summary-panel", "metric-group", "action-cluster", "text-stack", "hero-panel",
    "descriptive-items", "record-collection", "record-table", "record-summary", "empty-placeholder"
}

path = Path(sys.argv[1])
data = json.loads(path.read_text(encoding='utf-8'))

assert set(data.keys()) >= {"metadata", "project", "shared_context", "pages"}, "missing top-level fields for genux-compile"
metadata = data["metadata"]
for key in ["spec_id", "schema_version", "project_id", "generated_from"]:
    assert key in metadata, f"missing metadata.{key}"
project = data["project"]
for key in ["project_id", "shell_model"]:
    assert key in project, f"missing project.{key}"
shared = data["shared_context"]
for key in ["project_scope", "normalized_from"]:
    assert key in shared, f"missing shared_context.{key}"
if "component_preset" in shared:
    assert isinstance(shared['component_preset'], str) and shared['component_preset'], 'component_preset must be non-empty string when provided'
for page in data["pages"]:
    assert page.get("page_type") in PAGE_TYPES, f"invalid page_type: {page.get('page_type')}"
    assert page.get("layout_mode") in LAYOUT_MODES, f"invalid layout_mode: {page.get('layout_mode')}"
    assert page.get("density") in DENSITIES, f"invalid density: {page.get('density')}"
    for key in ["page_id", "page_goal", "target_actor", "primary_tasks", "review_criteria"]:
        assert key in page, f"missing page field: {key}"
    for section in page.get("sections", []):
        assert section.get("section_role") in SECTION_ROLES, f"invalid section_role: {section.get('section_role')}"
        for key in ["section_id", "priority", "content_kind", "placement_preference"]:
            assert key in section, f"missing section field: {key}"
        for block in section.get("blocks", []):
            assert block.get("block_pattern") in BLOCK_PATTERNS, f"invalid block_pattern: {block.get('block_pattern')}"
            sp = block.get("semantic_payload")
            assert isinstance(sp, dict), "semantic_payload must be object"
            assert set(sp.keys()) <= {"page_id", "region_id", "module_refs"}, "semantic_payload must be compile-facing payload"
            for key in ["page_id", "region_id", "module_refs"]:
                assert key in sp, f"missing semantic_payload.{key}"
            assert isinstance(sp["module_refs"], list) and sp["module_refs"], "module_refs must be non-empty list"
            if "compile_hints" in block:
                hints = block["compile_hints"]
                assert isinstance(hints, dict), "compile_hints must be object"
                assert hints.get("source") == "dsir-native", "compile_hints.source must be dsir-native"
            forbidden = ["content_model_ref", "instance_payload", "capabilities", "state_hints", "interaction_hints", "presentation_preference"]
            for fk in forbidden:
                assert fk not in block, f"{fk} should not appear in genux-compile block"
print("GENUX_COMPILE_VALID")
