# Workflow

## Default Operating Mode

- Work against bilingual `.docx` manuscripts
- Use PDF only as a reference source, not as the mutation target
- Review in small section-local chunks of `1-3` natural paragraphs
- Preserve the translator's style unless a change is necessary for meaning or consistency

## Calibration Sequence

1. Locate the section with `inspect_docx_bilingual.py`
2. Confirm whether the manuscript is arranged as English/Chinese pairs, English block + Chinese block, or mixed figure text
3. Calibrate the current chunk
4. Return `结论 + 必要修改`
5. Wait for the user to apply the Chinese revision
6. After confirmation, dry-run English deletion
7. Review candidate indices
8. Run real deletion only for the confirmed range

## Range Selection Rules

- Prefer explicit section boundaries:
  - current section heading
  - next section heading
- If headings are unreliable, use explicit paragraph indices from inspection output
- Never infer a wider deletion range than the confirmed scope

## Deletion Safety Rules

- Delete only paragraphs that contain Latin letters and no CJK characters by default
- Leave mixed Chinese/English paragraphs untouched
- Leave figure text, legend text, and mixed glossary lines untouched unless the user explicitly asks otherwise
- Always run dry-run before the real deletion
- Report candidate paragraph count and exact indices before deletion

## Common Failure Modes

- English heading deleted but paired Chinese heading left in a confusing position
- Mixed figure captions accidentally deleted because they contain English labels
- English block and Chinese block are no longer aligned after earlier manual edits
- The next section marker appears multiple times; choose by paragraph index, not by text alone, if ambiguity remains

## Response Format

Use this default structure:

- range identifier
- `校准结论：可保留 / 建议微调 / 建议修改`
- only the necessary changes
- brief reason limited to:
  - terminology inconsistency
  - technical mistranslation
  - obvious omission/addition
  - clear wording or formatting error
