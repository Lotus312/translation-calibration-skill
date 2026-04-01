# translation-calibration-skill

A Codex skill for conservative bilingual book-manuscript translation calibration.

It is designed for `.docx` workflows where English source text and Chinese translation appear together in the same manuscript. The skill focuses on small-range review, terminology consistency, mistranslation detection, and safe removal of confirmed English source paragraphs after the revised Chinese has already been applied.

## What it does

- Inspects bilingual `.docx` manuscripts by section marker or paragraph range
- Calibrates translation in small local chunks, usually `1-3` natural paragraphs at a time
- Prioritizes only necessary fixes:
  - terminology inconsistency
  - technical mistranslation
  - obvious omissions or additions
  - clear wording or format errors
- Deletes only English-only source paragraphs after explicit confirmation

## Repository structure

- `SKILL.md`: skill definition and operating rules
- `references/terminology-guidelines.md`: term consistency rules and preferred translations
- `references/workflow.md`: canonical calibration and deletion workflow
- `scripts/inspect_docx_bilingual.py`: inspect section-local bilingual paragraph layout without editing
- `scripts/delete_english_range_docx.py`: dry-run and delete confirmed English-only paragraphs from a `.docx`

## Typical workflow

1. Inspect the manuscript structure and confirm English/Chinese paragraph pairing.
2. Calibrate a small section and return `校准结论 + 必要修改`.
3. Apply the Chinese revisions in the working manuscript.
4. Run deletion in dry-run mode first.
5. Delete only the confirmed English-only paragraphs for that exact range.

## Notes

- This skill is optimized for bilingual book manuscripts, not general app or website localization.
- PDF can be used as a reference source, but `.docx` is the primary mutation target.
- Mixed Chinese/English figure labels are not deleted by default.
