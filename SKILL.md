---
name: translation-calibration
description: Calibrate bilingual book-manuscript translations in `.docx` files with PDF or source-text reference support. Use when Codex needs to inspect paragraph-paired English/Chinese manuscripts, review translations in small section-local chunks, enforce terminology consistency, detect mistranslation/omission/format issues, and delete only the confirmed English source paragraphs after the user says the revised Chinese has already been applied.
---

# Translation Calibration

## Overview

Calibrate bilingual book manuscripts conservatively. Keep fluent Chinese style intact unless meaning, terminology, consistency, or clear wording/format errors require a change.

Delete English source text only after the user explicitly confirms the revised Chinese has been applied to the working manuscript.

## Workflow

1. Inspect the manuscript structure first. Use `scripts/inspect_docx_bilingual.py` to locate the requested section and confirm English/Chinese paragraph pairing before making suggestions.
2. Work in small chunks by default: `1-3` natural paragraphs within the current section. Keep titles, figure captions, lists, and prose as separate units when possible.
3. Return calibration feedback in this default format:
   - section or paragraph range
   - `校准结论：可保留 / 建议微调 / 建议修改`
   - only the necessary edits
   - a short reason limited to meaning, terminology, consistency, omission/addition, or clear wording/format errors
4. Prioritize only these issue classes unless the user asks for stylistic rewriting:
   - terminology inconsistency
   - technical mistranslation
   - obvious omission or over-translation
   - clear wording, punctuation, or formatting errors
5. Prefer the manuscript's dominant terminology unless it is clearly wrong. Use [references/terminology-guidelines.md](references/terminology-guidelines.md) when terminology decisions matter.
6. Keep bilingual technical terms when needed for clarity or consistency with the manuscript, especially for model families, algorithms, protocols, and framework names.
7. After the user confirms the Chinese revision has been applied, run `scripts/delete_english_range_docx.py` in dry-run mode first. Confirm the candidate paragraph indices, then run the real deletion.

## Deletion Rules

- Never delete Chinese paragraphs.
- Never delete beyond the confirmed section or paragraph range.
- Anchor deletion by explicit section markers or by explicit paragraph indices.
- Do not delete mixed Chinese/English paragraphs by default.
- Treat figure captions, section headings, and mixed glossary lines separately from ordinary prose.

## Scripts

- `scripts/inspect_docx_bilingual.py`
  - Inspect a `.docx` and report paragraph indices plus nearby previews around a section marker or index range.
  - Use this before calibration and before deletion.
- `scripts/delete_english_range_docx.py`
  - Delete English-only paragraphs from a confirmed range in a `.docx`.
  - Supports section-text boundaries or explicit index ranges.
  - Requires a dry run first.

## References

- [references/terminology-guidelines.md](references/terminology-guidelines.md): dominant-term policy and bilingual technical-term rules
- [references/workflow.md](references/workflow.md): canonical calibration workflow, chunking, and deletion safety rules

## Command Patterns

```bash
# Inspect a section by heading text
python3 scripts/inspect_docx_bilingual.py manuscript.docx \
  --section-text "1.2.2 AI基础设施的深远影响：赋能各行业智能化解决方案"

# Inspect an explicit paragraph range
python3 scripts/inspect_docx_bilingual.py manuscript.docx --start-index 320 --end-index 340

# Dry-run deletion for a confirmed section
python3 scripts/delete_english_range_docx.py manuscript.docx \
  --section-text "1.2.2 AI基础设施的深远影响：赋能各行业智能化解决方案" \
  --next-section-text "1.2.3 AI系统架构的核心组件" \
  --dry-run

# Delete confirmed English-only paragraphs after dry-run review
python3 scripts/delete_english_range_docx.py manuscript.docx \
  --section-text "1.2.2 AI基础设施的深远影响：赋能各行业智能化解决方案" \
  --next-section-text "1.2.3 AI系统架构的核心组件"
```
