"""Split one requirement into V0 pages."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
ROUTES_PATH = ROOT / "data" / "retrieval" / "page-routes.csv"


def _load_routes() -> list[dict[str, str]]:
    with ROUTES_PATH.open("r", encoding="utf-8-sig", newline="") as file:
        rows = list(csv.DictReader(file))
    rows.sort(key=lambda row: int(row.get("priority", "999")))
    return rows


def decompose_pages(intent: dict[str, Any]) -> list[dict[str, Any]]:
    signals = intent.get("signals", {})
    tags = set(intent.get("tags", []))
    routes = _load_routes()

    pages: list[dict[str, Any]] = []
    primary_added = False

    for route in routes:
        signal_name = route.get("source_signal", "")
        route_kind = route.get("route_kind", "")
        matches = signal_name in tags or bool(signals.get(signal_name, False))

        if route_kind == "primary":
            if primary_added or not matches:
                continue
            pages.append(
                {
                    "id": route.get("page_id", ""),
                    "page_type": route.get("page_type", ""),
                    "role": route.get("role", "primary"),
                    "depends_on": [],
                    "route_id": route.get("route_id", ""),
                    "use_page_template": True,
                }
            )
            primary_added = True
            continue

        if route_kind == "secondary" and matches and primary_added:
            depends = route.get("depends_on", "")
            pages.append(
                {
                    "id": route.get("page_id", ""),
                    "page_type": route.get("page_type", ""),
                    "role": route.get("role", "secondary"),
                    "depends_on": [depends] if depends else [],
                    "route_id": route.get("route_id", ""),
                    "use_page_template": True,
                }
            )

    if not primary_added and (signals.get("filtering") or signals.get("top_actions") or signals.get("copy_flow")):
        pages.append(
            {
                "id": "shell-content",
                "page_type": "table",
                "role": "primary",
                "depends_on": [],
                "route_id": "direct.table-shell",
                "use_page_template": False,
            }
        )

    return pages
