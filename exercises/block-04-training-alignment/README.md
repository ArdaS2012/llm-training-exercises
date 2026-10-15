# Block 4 — Next-Token Loss & Learning


## Exercise + breakout

Follow the [15-minute group task](GROUP_TASK.md) after guided setup.

Practice for Day 1, 14:45–15:05 (guided setup, then 15-minute exercise + breakout). You will calculate a target's
cross-entropy penalty, apply a parameter update, run a supplied tiny output-layer
training loop, and explain how loss and target probability change.

Use the [shared setup guide](../../README.md) first. Basic Python arithmetic/functions
are enough; no prior completed notebook, API, model download, GPU or new dependency.

```sh
uv run --locked python start.py --block 4 --check
uv run --locked python start.py --block 4
```

After online environment setup on this computer:

```sh
uv run --offline --locked python start.py --block 4
```

The correct notebook is [04_next_token_learning.py](04_next_token_learning.py).
If a browser does not open, visit http://127.0.0.1:2718. Both shared wrappers forward
`--block 4`, `--check` and `--port`; use `--port 2720` for a port conflict.

Follow the [15-minute group task](GROUP_TASK.md) after guided setup.

Show code with the cell's code control and rerun with Shift+Enter. Unfinished TODOs
show waiting messages. Submit/share one probability-to-loss calculation, the two
run settings, measured before/after evidence, and one limitation. Browser text/widget
values are preserved by the JSON download, not by saving the Python notebook alone.

The four-token vocabulary and three independent context features are **toy data**.
Only output weights W (3×4) and bias b (4,) learn; fixed H (3×3) is not a Transformer.
The loop supplies softmax and averaged gradients; your functions supply loss and
updates. This illustrates pretraining mechanics. Instruction tuning and preference
optimization are conceptual topics, not extra coding tasks. Lower training loss does
not prove generalization, truthfulness or alignment. A large learning rate can overshoot.

Waiting output: finish the TODO, preserving the return. Red cell: undo, check indentation
and scalar values. Logarithms require 0 < p ≤ 1; the supplied validation rejects invalid
inputs. No clipping is needed for the moderate default logits. If an aggressive rate
underflows a target probability, reduce it; full training libraries use log-softmax.
Read the formulas and conceptual hints in the notebook before requesting help.

Current handoff: LLM Day 1 slide 76, **Exercise: test a learning update**. The combined room task runs 14:50–15:05; setup/review are separate.

References: [GPT-3 pretraining](https://arxiv.org/abs/2005.14165),
[cross-entropy](https://docs.pytorch.org/docs/stable/generated/torch.nn.CrossEntropyLoss.html).

## Current teaching handoff

LLM Day 1, Block 4: actual slide **76 — Exercise: test a learning update** launches the combined exercise + breakout. Return to plenary at the agenda’s room end. The notebook and group task are self-contained; private trainer files are not required.
