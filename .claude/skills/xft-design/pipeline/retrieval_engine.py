"""Resolve design-system, shell, runtime, icon, and template registry inputs."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "retrieval"


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def retrieve_context(
    *,
    query: str,
    page_spec_path: str | None,
    intent: dict[str, Any],
    pages: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "query": query,
        "page_spec_path": page_spec_path,
        "intent_tags": intent.get("tags", []),
        "signals": intent.get("signals", {}),
        "pages": pages,
        "design_system_paths": {
            "usage": str(ROOT / "design-systems" / "USAGE.md"),
            "tokens": str(ROOT / "design-systems" / "tokens.css"),
            "components": str(ROOT / "design-systems" / "components.html"),
        },
        "registry_paths": {
            "page_routes": str(DATA_DIR / "page-routes.csv"),
            "region_routes": str(DATA_DIR / "region-routes.csv"),
            "overlay_routes": str(DATA_DIR / "overlay-routes.csv"),
            "template_registry": str(DATA_DIR / "template-registry.csv"),
            "rewrite_slots": str(DATA_DIR / "rewrite-slots.csv"),
            "shell_registry": str(DATA_DIR / "shell-registry.csv"),
            "runtime_registry": str(DATA_DIR / "runtime-registry.csv"),
            "icon_registry": str(DATA_DIR / "icon-registry.csv"),
        },
        "registries": {
            "region_routes": _read_csv(DATA_DIR / "region-routes.csv"),
            "overlay_routes": _read_csv(DATA_DIR / "overlay-routes.csv"),
            "template_registry": _read_csv(DATA_DIR / "template-registry.csv"),
            "rewrite_slots": _read_csv(DATA_DIR / "rewrite-slots.csv"),
            "shell_registry": _read_csv(DATA_DIR / "shell-registry.csv"),
            "runtime_registry": _read_csv(DATA_DIR / "runtime-registry.csv"),
            "icon_registry": _read_csv(DATA_DIR / "icon-registry.csv"),
        },
        "status": "ready",
        "notes": [
            "Use registered templates first.",
            "Use shells as host containers only.",
            "Use runtime.basic only for V0.",
            "Use local registered icons only.",
        ],
    }
