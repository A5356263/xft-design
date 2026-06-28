"""Parse requirement text into stable intent tags and V0.1 signals."""

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


def _contains_any(text: str, tokens: tuple[str, ...]) -> bool:
    return any(token in text for token in tokens)


def _derive_signals(text: str, query_text: str, tags: set[str]) -> dict[str, bool]:
    base_filtering = "base_filtering" in tags or _contains_any(text, ("筛选", "查询", "搜索", "filter", "search", "query"))
    quick_positive = "quick_filtering" in tags or _contains_any(text, ("快捷筛选", "标签筛选", "quick filter", "saved view", "chip"))
    quick_negative = _contains_any(text, ("不要快捷筛选", "无快捷筛选", "不含快捷筛选", "without quick filter"))
    quick_filtering = quick_positive and not quick_negative
    advanced_filtering = "advanced_filtering" in tags or _contains_any(text, ("高级筛选", "更多筛选", "展开筛选", "advanced filter", "more filters"))
    primary_positive = "top_primary_action" in tags or _contains_any(text, ("新增", "创建", "新建", "发起", "create", "new"))
    primary_negative = _contains_any(text, ("不需要新增", "无需新增", "不要新增", "无新增按钮", "no create", "without primary action"))
    top_primary_action = primary_positive and not primary_negative
    top_secondary_actions = "top_secondary_actions" in tags or _contains_any(
        text, ("导出", "导入", "下载", "上传", "启用", "停用", "删除", "export", "import", "download", "upload")
    )
    top_utility_actions = "top_utility_actions" in tags or _contains_any(
        text, ("刷新", "列设置", "密度", "refresh", "column settings", "density")
    )

    return {
        "always": True,
        "base_filtering": base_filtering,
        "quick_filtering": quick_filtering,
        "advanced_filtering": advanced_filtering,
        "filtering": base_filtering or quick_filtering,
        "top_primary_action": top_primary_action,
        "top_secondary_actions": top_secondary_actions,
        "top_utility_actions": top_utility_actions,
        "top_actions": top_primary_action or top_secondary_actions or top_utility_actions,
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

    signals = _derive_signals(text, query_text, tags)
    title = _extract_title(query, page_spec)
    scene = "copy_permission" if signals["copy_flow"] and "tabular_data" in tags else "generic"

    if scene == "copy_permission":
        signals["base_filtering"] = True
        signals["filtering"] = True
        signals["top_primary_action"] = True
        signals["top_secondary_actions"] = True
        signals["top_utility_actions"] = True
        signals["top_actions"] = True

    return {
        "query": query.strip(),
        "title": title,
        "scene": scene,
        "tags": sorted(tags),
        "signals": signals,
        "evidence": evidence,
        "status": "ready",
    }
