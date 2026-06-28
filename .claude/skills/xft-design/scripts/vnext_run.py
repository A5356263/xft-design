#!/usr/bin/env python3
"""Run the V0 prototype pipeline for xft-design."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pipeline import (
    assemble_html_plan,
    compile_schema,
    decompose_pages,
    parse_intent,
    retrieve_context,
    select_templates,
)


def read_optional_text(path: str | None) -> str:
    if not path:
        return ""
    file_path = Path(path)
    if not file_path.exists():
        return ""
    for encoding in ("utf-8", "utf-8-sig", "gb18030", "gbk"):
        try:
            return file_path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    return file_path.read_text(encoding="utf-8", errors="ignore")


def run(query: str, page_spec_path: str | None = None) -> dict[str, object]:
    page_spec = read_optional_text(page_spec_path)
    intent = parse_intent(query, page_spec)
    pages = decompose_pages(intent)
    retrieval_context = retrieve_context(
        query=query,
        page_spec_path=page_spec_path,
        intent=intent,
        pages=pages,
    )
    schema = compile_schema(
        query=query,
        intent=intent,
        pages=pages,
        retrieval_context=retrieval_context,
    )
    templates = select_templates(schema, retrieval_context)
    assembly_plan = assemble_html_plan(schema=schema, bundle=templates)
    return {
        "intent": intent,
        "pages": pages,
        "retrieval_context": retrieval_context,
        "schema": schema,
        "templates": templates,
        "assembly_plan": assembly_plan,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the xft-design V0 prototype generator.")
    parser.add_argument("query", help="Requirement text")
    parser.add_argument("--page-spec", help="Optional path to page_spec.md")
    args = parser.parse_args()
    print(json.dumps(run(args.query, args.page_spec), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
