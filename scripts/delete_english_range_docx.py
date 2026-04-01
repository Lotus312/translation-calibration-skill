#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}


def para_text(para: ET.Element) -> str:
    return "".join(t.text or "" for t in para.findall(".//w:t", NS)).strip()


def has_cjk(text: str) -> bool:
    return any("\u4e00" <= ch <= "\u9fff" for ch in text)


def has_latin(text: str) -> bool:
    return any(("A" <= ch <= "Z") or ("a" <= ch <= "z") for ch in text)


def is_english_only(text: str) -> bool:
    return bool(text) and has_latin(text) and not has_cjk(text)


def find_index(texts: list[str], marker: str, start_at: int = 0) -> int:
    for idx in range(start_at, len(texts)):
        if texts[idx] == marker:
            return idx
    raise ValueError(f"marker not found: {marker}")


def load_doc(path: Path) -> tuple[ET.ElementTree, ET.Element, list[ET.Element], list[str]]:
    with zipfile.ZipFile(path, "r") as zf:
        xml = zf.read("word/document.xml")
    root = ET.fromstring(xml)
    body = root.find("w:body", NS)
    if body is None:
        raise ValueError("word/document.xml missing body")
    paras = body.findall("w:p", NS)
    texts = [para_text(p) for p in paras]
    return ET.ElementTree(root), body, paras, texts


def build_visible_entries(paras: list[ET.Element], texts: list[str]) -> list[dict[str, object]]:
    entries = []
    visible_index = 0
    for raw_index, text in enumerate(texts):
        if not text:
            continue
        visible_index += 1
        entries.append(
            {
                "visible_index": visible_index,
                "raw_index": raw_index,
                "text": text,
            }
        )
    return entries


def write_doc(src: Path, root: ET.Element, out_path: Path) -> None:
    xml_bytes = ET.tostring(root, encoding="utf-8", xml_declaration=True)
    tmp_path = out_path.with_suffix(".tmp.docx")
    with zipfile.ZipFile(src, "r") as zin, zipfile.ZipFile(tmp_path, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = xml_bytes if item.filename == "word/document.xml" else zin.read(item.filename)
            zout.writestr(item, data)
    tmp_path.replace(out_path)


def main() -> int:
    parser = argparse.ArgumentParser(description="Delete English-only DOCX paragraphs in a confirmed range.")
    parser.add_argument("docx", type=Path)
    parser.add_argument("--section-text", help="Exact paragraph text for the current section heading")
    parser.add_argument("--next-section-text", help="Exact paragraph text for the next section heading")
    parser.add_argument("--start-index", type=int, help="1-based start paragraph index")
    parser.add_argument("--end-index", type=int, help="1-based end paragraph index")
    parser.add_argument("--dry-run", action="store_true", help="Show candidate indices only")
    parser.add_argument("--backup", action="store_true", help="Write a .bak copy before editing")
    args = parser.parse_args()

    tree, body, paras, texts = load_doc(args.docx)
    entries = build_visible_entries(paras, texts)
    visible_texts = [entry["text"] for entry in entries]

    if args.section_text:
        start_visible_idx = find_index(visible_texts, args.section_text)
        if args.next_section_text:
            end_visible_idx = (
                find_index(visible_texts, args.next_section_text, start_visible_idx + 1) - 1
            )
        else:
            raise ValueError("--next-section-text is required when using --section-text")
    else:
        if args.start_index is None or args.end_index is None:
            parser.error("use --section-text/--next-section-text or both --start-index and --end-index")
        start_visible_idx = max(0, args.start_index - 1)
        end_visible_idx = min(len(entries) - 1, args.end_index - 1)

    candidates: list[tuple[int, str]] = []
    for entry in entries[start_visible_idx : end_visible_idx + 1]:
        text = entry["text"]
        if is_english_only(text):
            candidates.append((int(entry["visible_index"]), int(entry["raw_index"]), text))

    print(f"docx: {args.docx}")
    print(f"range: {start_visible_idx + 1}-{end_visible_idx + 1}")
    print(f"candidate_count: {len(candidates)}")
    print("candidate_indices:", [visible_idx for visible_idx, _, _ in candidates])
    for visible_idx, _, text in candidates:
        print(f"{visible_idx:04d}: {text}")

    if args.dry_run:
        return 0

    if args.backup:
        backup_path = args.docx.with_suffix(args.docx.suffix + ".bak")
        shutil.copy2(args.docx, backup_path)
        print(f"backup: {backup_path}")

    for _, raw_idx, _ in reversed(candidates):
        body.remove(paras[raw_idx])

    write_doc(args.docx, tree.getroot(), args.docx)
    return 0


if __name__ == "__main__":
    sys.exit(main())
