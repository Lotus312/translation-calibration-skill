# Terminology Guidelines

Use the manuscript's dominant term unless the current term is clearly wrong or creates a local inconsistency that would confuse readers.

## Core Policy

- Prefer correctness over stylistic preference.
- Prefer manuscript-wide consistency over isolated local preference.
- Prefer chapter-level consistency when a manuscript intentionally varies terminology by context.
- Do not normalize terminology aggressively unless the user explicitly asks for a full standardization pass.

## Title-Level vs Body-Level Terms

- Titles, headings, and navigation labels often need shorter, more stable terminology.
- Body text may use fuller definitions on first mention and shorter forms afterward.
- Do not force heading terminology onto prose or prose terminology onto headings unless inconsistency becomes confusing.

## Domain-Term Decisions

When deciding whether to change a term, use this order:

1. Clear technical correctness
2. In-section consistency
3. In-chapter consistency
4. Whole-manuscript dominant usage
5. House style or personal preference

## Keep Source-Language Terms When Needed

Keep the source-language form, optionally with target-language support, when the manuscript or domain expects it:

- model families
- algorithm names
- protocols and standards
- framework and library names
- product names
- established abbreviations

Examples:

- `Transformer`
- `Actor-Critic`
- `RAG`
- `OAuth`
- `Kubernetes`
- model/framework/library names

## Example Patterns

These are examples, not mandatory global mappings:

- `robust`
  - Systems or engineering practice may prefer a more general translation such as `健壮`
  - Model behavior or robustness as a technical property may prefer a more specialized translation such as `鲁棒`
- `pipeline`
  - Keep the manuscript-wide dominant usage unless the user decides to standardize terminology globally
- `agent`
  - Choose the term that best fits the domain and keep it stable within the same section or chapter
- `architecture`
  - Distinguish between the thing itself and the act of designing it if the target language makes that distinction useful

If the issue is only stylistic and the current wording is technically correct, do not change it by default.
