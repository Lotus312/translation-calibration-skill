# Terminology Guidelines

Use the manuscript's dominant term unless the current term is clearly wrong or creates a local inconsistency that would confuse readers.

## Decision Rules

- `robust`
  - For systems, architecture, engineering practice: prefer `健壮`
  - For model behavior or robustness as a technical property: keep `鲁棒` when the manuscript already uses it or the meaning is specifically robustness-oriented
- `pipeline`
  - Keep the manuscript-wide dominant usage
  - Do not change `数据管道` to `数据流水线` or vice versa unless the user decides to standardize the whole manuscript
- `agent`
  - For generative-AI orchestration contexts: prefer `智能体`
  - Do not switch between `智能体` and `代理` within the same chapter unless the source clearly distinguishes them
- `architecture`
  - Titles and technical discussion usually use `架构`
  - Use `架构设计` only when the sentence is clearly about the design activity rather than the architecture itself
- `AI系统` and `人工智能系统`
  - Keep the manuscript's dominant chapter-level usage
  - Titles may stay shorter (`AI系统`) even if prose occasionally uses `人工智能（AI）系统` on first mention

## Keep English Terms When Needed

Keep the English form, optionally with Chinese support, when the manuscript or domain expects it:

- `Transformer`
- `Actor-Critic`
- `RAG`
- `LangChain`
- `Kubernetes`
- `OAuth`
- model/framework/library names

## Calibration Priority

When choosing whether to change a term, use this order:

1. Clear technical correctness
2. In-chapter consistency
3. Whole-manuscript dominant usage
4. Style preference

If the issue is only stylistic and the current wording is technically correct, do not change it by default.
