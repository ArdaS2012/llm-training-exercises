# Block 3 — Causal Masking & Sampling

Current handoff: LLM Day 1 slide 60, **Exercise: masking versus sampling**. The combined room task runs 13:35–14:05; setup/review are separate.

Use the [shared installation and troubleshooting guide](../../README.md). Launch from the student repository:

```sh
uv run --locked python start.py --block 3 --check
uv run --locked python start.py --block 3
```

After preparing that environment on this computer, use `uv run --offline --locked python start.py --block 3`. Wrappers forward the same arguments: `sh start.sh --block 3` or `start.cmd --block 3`. Block 1 remains the default.

## Goals and prerequisites

You should recognize Q/K/V, row-wise softmax and output logits from the earlier explanations. All tiny arrays, rendering and random draws are supplied; completing Practice 2 is not required. No LLM, GPU, API key or additional dataset is used. Python lists and list comprehensions are enough. Shapes and formulas are explained in the notebook.

## Exercise + breakout

Follow the [30-minute investigation](GROUP_TASK.md) after guided setup. It defines the required comparison, evidence and shared result. Keep the technical help below for the bounded TODOs.

## Findings to explain

Which attention entries disappear, and why? Why do valid rows still sum to one? What changes when T changes? What does k=1 permit? Why do observed counts differ from theoretical probabilities? Explain how masking controls access to context while sampling selects a vocabulary candidate. Top-p remains the Visual Lab comparison, rather than an extra coding TODO.

## Help and sources

Undo if a cell turns red; check indentation, function names and return shapes. A score of zero is not blocked. Temperature scaling belongs before exponentiation. Top-k must renormalize retained mass, not move candidates into different positions. Keep the seed fixed to repeat a run, rather than resetting before every draw.

[Original Transformer](https://arxiv.org/abs/1706.03762) explains decoder masking. [Generation parameters](https://huggingface.co/docs/transformers/main/en/main_classes/text_generation) describes temperature and top-k. [marimo basics](https://docs.marimo.io/getting_started/) explains editing/running cells. Optional private trainer resource: [guide §16](https://github.com/ArdaS2012/EDV_Training/blob/main/docs/LLM_Training/llm_day1/03_transformer_architecture.md#slide-16). Students do not need access to it.

## Current teaching handoff

LLM Day 1, Block 3: actual slide **60 — Exercise: masking versus sampling** launches the combined exercise + breakout. Return to plenary at the agenda’s room end. The notebook and group task are self-contained; private trainer files are not required.

## Investigation and slide takeaways

The [30-minute task](GROUP_TASK.md) keeps the relevant slide takeaways beside the investigation, explains the controls and required evidence, and gives you time to try an additional prediction. Can you stop future information leaking in while explaining why repeated token draws differ?
