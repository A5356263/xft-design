"""Select page, region, overlay, shell, runtime, and icon assets for V0."""

from __future__ import annotations

from typing import Any


PAGE_TEMPLATE_MAP = {
    "table": "page.table",
    "detail": "page.detail",
    "form": "page.form",
}


def _index_by(rows: list[dict[str, str]], key: str) -> dict[str, dict[str, str]]:
    return {row[key]: row for row in rows if row.get(key)}


def _select_regions(page_type: str, signals: dict[str, Any], routes: list[dict[str, str]]) -> list[dict[str, str]]:
    selected: list[dict[str, str]] = []
    for row in sorted(routes, key=lambda item: int(item.get("priority", "999"))):
        if row.get("applies_to_page_type") not in {page_type, "any"}:
            continue
        signal_name = row.get("source_signal", "")
        if signal_name != "always" and not signals.get(signal_name, False):
            continue
        selected.append(row)
    return selected


def _select_overlays(signals: dict[str, Any], routes: list[dict[str, str]], page_id: str) -> list[dict[str, str]]:
    overlays: list[dict[str, str]] = []
    for row in sorted(routes, key=lambda item: int(item.get("priority", "999"))):
        signal_name = row.get("source_signal", "")
        if not signals.get(signal_name, False):
            continue
        if row.get("target_page_id") != page_id:
            continue
        overlays.append(row)
    return overlays


def _select_shell(page_type: str, shell_rows: list[dict[str, str]]) -> dict[str, str]:
    for row in shell_rows:
        supported = set((row.get("supported_page_types") or "").split("|"))
        if page_type in supported:
            return row
    return shell_rows[0]


def _select_runtime(runtime_rows: list[dict[str, str]]) -> dict[str, str]:
    return runtime_rows[0]


def _select_icons(scene: str, page_type: str, icon_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    wanted = ["search", "filter"]
    if page_type == "table":
        wanted.extend(["plus", "copy", "edit", "delete"])
    if scene == "copy_permission":
        wanted.extend(["check-circle", "close", "info-circle"])
    found = {row.get("semantic_name"): row for row in icon_rows}
    return [found[name] for name in wanted if name in found]


def select_templates(schema: dict[str, Any], retrieval_context: dict[str, Any]) -> dict[str, Any]:
    registries = retrieval_context.get("registries", {})
    template_index = _index_by(registries.get("template_registry", []), "template_id")
    shell_rows = registries.get("shell_registry", [])
    runtime_rows = registries.get("runtime_registry", [])
    region_routes = registries.get("region_routes", [])
    overlay_routes = registries.get("overlay_routes", [])
    icon_rows = registries.get("icon_registry", [])
    rewrite_slots = registries.get("rewrite_slots", [])

    pages: list[dict[str, Any]] = []
    unsupported = list(schema.get("unsupported", []))

    for page in schema.get("pages", []):
        page_type = page.get("page_type", "form")
        template_id = PAGE_TEMPLATE_MAP.get(page_type, "")
        page_template = template_index.get(template_id)
        if not page_template:
            unsupported.append({"page_id": page.get("id", ""), "reason": f"missing_template:{template_id}"})
            continue

        selected_regions = _select_regions(page_type, schema.get("signals", {}), region_routes)
        selected_overlays = _select_overlays(schema.get("signals", {}), overlay_routes, page.get("id", ""))

        page_record = {
            "page_id": page.get("id"),
            "page_type": page_type,
            "role": page.get("role", "primary"),
            "depends_on": page.get("depends_on", []),
            "shell": _select_shell(page_type, shell_rows),
            "runtime": _select_runtime(runtime_rows),
            "page_template": page_template,
            "regions": [
                {
                    **region,
                    "template": template_index.get(region.get("template_id", ""), {}),
                }
                for region in selected_regions
            ],
            "overlays": [
                {
                    **overlay,
                    "template": template_index.get(overlay.get("template_id", ""), {}),
                }
                for overlay in selected_overlays
            ],
            "icons": _select_icons(schema.get("scene", "generic"), page_type, icon_rows),
            "rewrite_slots": [
                row
                for row in rewrite_slots
                if row.get("template_id")
                in {
                    page_template.get("template_id", ""),
                    *[region.get("template_id", "") for region in selected_regions],
                    *[overlay.get("template_id", "") for overlay in selected_overlays],
                }
            ],
        }
        pages.append(page_record)

    return {
        "pages": pages,
        "unsupported": unsupported,
        "index_shell": next(
            (row for row in shell_rows if row.get("shell_id") == "shell.blank"),
            shell_rows[0] if shell_rows else {},
        ),
        "status": "ready",
    }
