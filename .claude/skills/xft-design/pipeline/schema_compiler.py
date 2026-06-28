"""Compile a V0 schema contract from pages and retrieval context."""

from __future__ import annotations

from typing import Any


VALID_PAGE_TYPES = {"form", "table", "detail"}


def compile_schema(
    *,
    query: str,
    intent: dict[str, Any],
    pages: list[dict[str, Any]],
    retrieval_context: dict[str, Any],
) -> dict[str, Any]:
    normalized_pages = []
    unsupported: list[dict[str, str]] = []

    for page in pages:
        page_type = page.get("page_type", "form")
        if page_type not in VALID_PAGE_TYPES:
            unsupported.append(
                {
                    "page_id": str(page.get("id", "")),
                    "reason": f"unsupported_page_type:{page_type}",
                }
            )
            continue
        normalized_pages.append({**page, "page_type": page_type})

    return {
        "version": "0.1.0",
        "query": query.strip(),
        "title": intent.get("title", query.strip()),
        "scene": intent.get("scene", "generic"),
        "intent_tags": intent.get("tags", []),
        "signals": intent.get("signals", {}),
        "pages": normalized_pages,
        "unsupported": unsupported,
        "retrieval_context": {
            "design_system_paths": retrieval_context.get("design_system_paths", {}),
            "registry_paths": retrieval_context.get("registry_paths", {}),
        },
        "status": "ready",
    }
