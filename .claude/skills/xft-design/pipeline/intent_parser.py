"""Parse requirement text into stable intent tags and V0 signals."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
INTENT_TAGS_PATH = ROOT / "data" / "retrieval" / "intent-tags.csv"
DEFAULT_TAGS = ("high_density",)


def _load_tag_rows() -> list[dict[str, str]]:
    with INTENT_TAGS_PATH.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def _has_any(text: str, keywords: str) -> bool:
    return any(token.strip() and token.strip().lower() in text for token in keywords.split("|"))


def _extract_title(query: str, page_spec: str) -> str:
    for line in page_spec.splitlines():
        stripped = line.strip().lstrip("#").strip()
        if stripped:
            return stripped
    return query.strip()


def _derive_signals(text: str, query_text: str) -> dict[str, bool]:
    return {
        "always": True,
        "filtering": any(token in text for token in ("筛选", "查询", "搜索", "filter", "search", "query")),
        "footer_actions": any(token in text for token in ("确认", "取消", "提交", "底部按钮", "footer")),
        "copy_flow": any(token in text for token in ("复制", "copy", "duplicate")),
        "result_feedback": any(token in text for token in ("结果弹窗", "结果反馈", "success", "error", "失败", "成功")),
        "independent_detail": any(token in text for token in ("独立详情页", "详情页", "查看页", "detail page", "detail-page"))
        and not any(token in query_text for token in ("结果弹窗", "result modal")),
    }


def parse_intent(query: str, page_spec: str = "") -> dict[str, Any]:
    query_text = query.lower()
    text = f"{query}\n{page_spec}".lower()
    tags = set(DEFAULT_TAGS)
    evidence: list[str] = []

    for row in _load_tag_rows():
        tag_id = row.get("tag_id", "").strip()
        keywords = row.get("keywords", "")
        if tag_id and _has_any(text, keywords):
            tags.add(tag_id)
            evidence.append(f"matched:{tag_id}")

    signals = _derive_signals(text, query_text)
    title = _extract_title(query, page_spec)
    scene = "copy_permission" if signals["copy_flow"] and "tabular_data" in tags else "generic"

    if scene == "copy_permission":
        signals["filtering"] = True
        signals["footer_actions"] = True

    return {
        "query": query.strip(),
        "title": title,
        "scene": scene,
        "tags": sorted(tags),
        "signals": signals,
        "evidence": evidence,
        "status": "ready",
    }
