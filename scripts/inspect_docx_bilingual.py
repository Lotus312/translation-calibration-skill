#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}


def load_paragraphs(docx_path: Path) -> list[str]:
    with zipfile.ZipFile(docx_path) as zf:
        xml = zf.read("word/document.xml")
    root = ET.fromstring(xml)
    paragraphs = []
    for para in root.findall(".//w:p", NS):
        text = "".join(t.text or "" for t in para.findall(".//w:t", NS)).strip()
        if text:
            paragraphs.append(text)
    return paragraphs


def find_index(paragraphs: list[str], marker: str, start_at: int = 0) -> int:
    for idx in range(start_at, len(paragraphs)):
        if paragraphs[idx] == marker:
            return idx
    raise ValueError(f"marker not found: {marker}")


def build_preview(paragraphs: list[str], start: int, end: int) -> list[dict[str, str]]:
    preview = []
    for idx in range(start, end + 1):
        preview.append({"index": idx + 1, "text": paragraphs[idx]})
    return preview


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect bilingual DOCX paragraph ranges.")
    parser.add_argument("docx", type=Path)
    parser.add_argument("--section-text", help="Exact paragraph text of the current section heading")
    parser.add_argument("--next-section-text", help="Exact paragraph text of the next section heading")
    parser.add_argument("--start-index", type=int, help="1-based start paragraph index")
    parser.add_argument("--end-index", type=int, help="1-based end paragraph index")
    parser.add_argument("--context", type=int, default=6, help="Preview paragraphs before/after target when using section text")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of plain text")
    args = parser.parse_args()

    paragraphs = load_paragraphs(args.docx)

    if args.section_text:
        start_idx = find_index(paragraphs, args.section_text)
        if args.next_section_text:
            end_idx = find_index(paragraphs, args.next_section_text, start_idx + 1) - 1
        else:
            end_idx = min(len(paragraphs) - 1, start_idx + args.context)
        preview_start = max(0, start_idx - args.context)
        preview_end = min(len(paragraphs) - 1, end_idx + args.context)
    else:
        if args.start_index is None or args.end_index is None:
            parser.error("use --section-text or both --start-index and --end-index")
        start_idx = max(0, args.start_index - 1)
        end_idx = min(len(paragraphs) - 1, args.end_index - 1)
        preview_start = start_idx
        preview_end = end_idx

    data = {
        "docx": str(args.docx),
        "range_start": start_idx + 1,
        "range_end": end_idx + 1,
        "preview_start": preview_start + 1,
        "preview_end": preview_end + 1,
        "paragraphs": build_preview(paragraphs, preview_start, preview_end),
    }

    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print(f"docx: {data['docx']}")
        print(f"range: {data['range_start']}-{data['range_end']}")
        print(f"preview: {data['preview_start']}-{data['preview_end']}")
        for item in data["paragraphs"]:
            print(f"{item['index']:04d}: {item['text']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
