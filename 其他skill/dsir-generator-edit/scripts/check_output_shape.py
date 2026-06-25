import json, sys
from pathlib import Path

path = Path(sys.argv[1])
data = json.loads(path.read_text(encoding="utf-8"))
assert isinstance(data.get("pages"), list), "missing pages"
for page in data["pages"]:
    for field in ["page_id", "page_type", "page_goal", "target_actor", "primary_tasks", "layout_mode", "review_criteria"]:
        assert field in page, f"missing page field: {field}"
    for section in page.get("sections", []):
        for field in ["section_id", "section_role", "priority", "placement_preference"]:
            assert field in section, f"missing section field: {field}"
        for block in section.get("blocks", []):
            assert "block_id" in block and "block_pattern" in block, "missing block identity"
            sp = block.get("semantic_payload", {})
            assert "content_model_ref" in sp, "missing semantic_payload.content_model_ref"
            assert "instance_payload" in sp, "missing semantic_payload.instance_payload"
            assert "presentation_preference" in block, "missing presentation_preference"
print("OK")
