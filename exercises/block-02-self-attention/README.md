# Block 2 — Build a Tiny Attention Head

Day 1 practice allocation **11:10–11:40**; room task **11:20–11:35** after guided setup. Current launch: slide **39 — Exercise: trace and perturb attention**.

Use the [shared setup and troubleshooting](../../README.md), then run from this repository:

```sh
uv run --locked python start.py --block 2 --check
uv run --locked python start.py --block 2
```

After setup on this computer: `uv run --offline --locked python start.py --block 2`. Wrappers support `sh start.sh --block 2` and `start.cmd --block 2`. Block 1 remains the default. No new packages, models, API keys or asset downloads are needed.

## Goals and prerequisites

Know what Q, K and V represent from the slide explanation; basic Python lists/loops are enough. Three supplied 3 × 2 toy matrices illustrate the arithmetic, not learned sentence relationships. Implement scaled scores, stable row-softmax and weighted Values. Read Query/source axes, check row sums, and distinguish changes in matching (Q/K) from changes in payload (V). This is one unrestricted attention head: no causal mask, learned projections, positional-encoding implementation, residuals, training or multi-head combination. Those explanations belong to the slides and later blocks.

## Exercise + breakout

Follow the [15-minute group task](GROUP_TASK.md) after guided setup. It defines the required comparison, evidence and shared result. Keep the technical help below for the bounded TODOs.

## Checks and help

Wait messages are normal until you complete a step. A shape failure usually means confusing sequence positions with features. Scores need all Query–Key pairs; softmax needs a separate normalization per row; mixing sums across source positions for each Value coordinate. A high attention weight is not a direct importance score or a complete explanation of a model. The tiny head neither trains language relationships nor measures model quality.

Hints and boundary feedback are in the notebook. Undo if a cell turns red; check indentation and return values. Restart/port/network help is in the shared README.

[Original Transformer, §3.2](https://arxiv.org/abs/1706.03762) defines scaled dot-product attention. [marimo basics](https://docs.marimo.io/getting_started/) explains editing and running cells. Optional private trainer resource: [guide §12](https://github.com/ArdaS2012/EDV_Training/blob/main/docs/LLM_Training/llm_day1/02_self_attention.md#slide-12); students do not need access to it.

## Current teaching handoff

LLM Day 1, Block 2: actual slide **39 — Exercise: trace and perturb attention** launches the combined exercise + breakout. Return to plenary at the agenda’s room end. The notebook and group task are self-contained; private trainer files are not required.
