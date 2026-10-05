# Exercises

Choose a block, open its README and follow its task instructions. Install the shared
environment once using the [repository setup guide](../README.md).

| Block | Exercise instructions | Status |
|---|---|---|
| 1 — Tokenization & Context | [Block 1 README](block-01-tokenization-context/README.md) | Prepared starter available |
| 2 — Tiny Attention Head | [Block 2 README](block-02-self-attention/README.md) | Prepared starter available |
| 3 — Causal Masking & Sampling | [Block 3 README](block-03-transformer-architecture/README.md) | Prepared starter available |
| 4 — Next-Token Loss & Learning | [Block 4 README](block-04-training-alignment/README.md) | Prepared starter available |
| Day 2 · 1 — Prompt Engineering | [Day 2 Block 1 README](day2-block-01-prompt-engineering/README.md) | Prepared starter; real local model calls |

Day 1 Blocks 1–4 and Day 2 Block 1 are supplied. Future blocks belong in separate folders with
their own README and notebooks. Each block README describes its learning goals,
launch command, tasks, expected participant outputs and task-specific help.

## Day 2 Block 2 — Mini-RAG

[Mini-RAG instructions](day2-block-02-rag/README.md) — two TODOs, own documents, real Chroma/embedding/reranker/generator, source judgments and JSON handoff. Prepare with `uv sync --locked --group rag`; select `uv run --locked --group rag python start.py --block d2-2`. Day 1 default is preserved.
