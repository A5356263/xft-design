#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verify XFT content asset integration after Step 11 execution.

This script checks:
- required directories
- required data files
- SKILL.md workflow markers
- search script availability
- validation test cases
- read_order path existence when returned by the search script
"""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List


REQUIRED_DIRS = [
    "assets/content-assets/regions",
    "assets/content-assets/modules",
    "assets/content-assets/feedback",
    "assets/content-assets/states",
    "assets/content-assets/overlays",
    "assets/content-assets/component-combos",
]

REQUIRED_DATA = [
    "data/content-assets/content-assets.csv",
    "data/content-assets/asset-keywords.csv",
    "data/content-assets/asset-rules.csv",
    "data/content-assets/recipe-rules.csv",
    "data/content-assets/recipe-asset-map.csv",
    "data/content-assets/page-type-router.csv",
]

REQUIRED_SKILL_MARKERS = [
    "ROUTE_DECISION",
    "CONTENT_ASSET_DECISION",
    "content asset",
]


def check_path(base: Path, rel: str) -> Dict[str, Any]:
    p = base / rel
    return {"path": rel, "exists": p.exists(), "is_dir": p.is_dir(), "is_file": p.is_file()}


def read_cases(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def run_search(skill_dir: Path, query: str) -> Dict[str, Any]:
    script = skill_dir / "scripts/search_content_assets.py"
    data_dir = skill_dir / "data/content-assets"
    cmd = [sys.executable, str(script), query, "--data-dir", str(data_dir), "--pretty"]
    try:
        proc = subprocess.run(cmd, cwd=str(skill_dir), text=True, capture_output=True, timeout=20)
    except Exception as exc:
        return {"ok": False, "error": f"exception: {exc}"}
    if proc.returncode != 0:
        return {"ok": False, "error": proc.stderr.strip() or proc.stdout.strip()}
    try:
        data = json.loads(proc.stdout)
    except json.JSONDecodeError:
        return {"ok": False, "error": "search output is not valid JSON", "stdout": proc.stdout[:2000]}
    return {"ok": True, "data": data}


def collect_read_order(data: Any) -> List[str]:
    if not isinstance(data, dict):
        return []
    candidates = []
    for key in ["read_order", "required_assets", "assets"]:
        val = data.get(key)
        if isinstance(val, list):
            candidates.extend(val)
    paths = []
    for item in candidates:
        if isinstance(item, str):
            paths.append(item)
        elif isinstance(item, dict):
            for k in ["html_path", "path", "asset_path"]:
                if item.get(k):
                    paths.append(str(item[k]))
                    break
    # Some implementations nest decision
    decision = data.get("CONTENT_ASSET_DECISION") or data.get("content_asset_decision")
    if isinstance(decision, dict):
        paths.extend(collect_read_order(decision))
    return list(dict.fromkeys(paths))


def path_exists_for_read_order(skill_dir: Path, rel: str) -> bool:
    rel = rel.strip()
    if not rel:
        return False
    candidates = [skill_dir / rel]
    if rel.startswith("assets/"):
        candidates.append(skill_dir / rel.replace("assets/", "assets/content-assets/", 1))
    if rel.startswith("content-assets/"):
        candidates.append(skill_dir / "assets" / rel)
    return any(p.exists() for p in candidates)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skill-dir", required=True)
    parser.add_argument("--test-cases", required=True)
    parser.add_argument("--report", required=True)
    args = parser.parse_args()

    skill_dir = Path(args.skill_dir).resolve()
    test_cases = Path(args.test_cases).resolve()
    report_path = Path(args.report).resolve()
    report_path.parent.mkdir(parents=True, exist_ok=True)

    report: Dict[str, Any] = {
        "skill_dir": str(skill_dir),
        "status": "unknown",
        "checks": {},
        "test_results": [],
        "blocking_issues": [],
        "non_blocking_issues": [],
    }

    if not skill_dir.exists():
        report["status"] = "fail"
        report["blocking_issues"].append(f"skill dir not found: {skill_dir}")
        report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 1

    dir_checks = [check_path(skill_dir, rel) for rel in REQUIRED_DIRS]
    data_checks = [check_path(skill_dir, rel) for rel in REQUIRED_DATA]
    report["checks"]["required_dirs"] = dir_checks
    report["checks"]["required_data"] = data_checks

    for item in dir_checks + data_checks:
        if not item["exists"]:
            report["blocking_issues"].append(f"missing: {item['path']}")

    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        report["blocking_issues"].append("missing: SKILL.md")
        skill_text = ""
    else:
        skill_text = skill_md.read_text(encoding="utf-8", errors="ignore")
    marker_results = {m: (m in skill_text) for m in REQUIRED_SKILL_MARKERS}
    report["checks"]["skill_markers"] = marker_results
    for marker, ok in marker_results.items():
        if not ok:
            report["blocking_issues"].append(f"SKILL.md missing marker: {marker}")

    search_script = skill_dir / "scripts/search_content_assets.py"
    if not search_script.exists():
        report["blocking_issues"].append("missing: scripts/search_content_assets.py")

    if test_cases.exists() and search_script.exists():
        for case in read_cases(test_cases):
            result = run_search(skill_dir, case["user_query"])
            entry: Dict[str, Any] = {
                "case_id": case.get("case_id"),
                "case_name": case.get("case_name"),
                "ok": result.get("ok", False),
            }
            if result.get("ok"):
                data = result["data"]
                entry["page_type"] = data.get("page_type") or data.get("route", {}).get("page_type")
                entry["recipe_id"] = data.get("recipe_id") or data.get("recipe", {}).get("recipe_id")
                read_order = collect_read_order(data)
                entry["read_order_count"] = len(read_order)
                missing_paths = [p for p in read_order if not path_exists_for_read_order(skill_dir, p)]
                entry["missing_read_order_paths"] = missing_paths
                if missing_paths:
                    entry["ok"] = False
                    report["blocking_issues"].append(f"{case.get('case_id')} read_order missing paths: {missing_paths}")
                if not entry.get("page_type"):
                    entry["ok"] = False
                    report["blocking_issues"].append(f"{case.get('case_id')} missing page_type")
                if not entry.get("recipe_id"):
                    # Not all overlay/component-state routes may have a recipe; keep non-blocking for None cases.
                    if case.get("expected_page_type") not in ("None", ""):
                        entry["ok"] = False
                        report["blocking_issues"].append(f"{case.get('case_id')} missing recipe_id")
                    else:
                        report["non_blocking_issues"].append(f"{case.get('case_id')} has no recipe_id; confirm overlay route is expected")
            else:
                entry["error"] = result.get("error")
                report["blocking_issues"].append(f"{case.get('case_id')} search failed: {result.get('error')}")
            report["test_results"].append(entry)
    else:
        if not test_cases.exists():
            report["blocking_issues"].append(f"test cases not found: {test_cases}")

    report["status"] = "pass" if not report["blocking_issues"] else "fail"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
