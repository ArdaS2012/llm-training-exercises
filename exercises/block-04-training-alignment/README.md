# Block 4 — Next-Token Loss & Learning

Practice for Day 1, 14:45–15:05 (20 minutes, pairs). You will calculate a target's
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

1. **Predict (2 min):** compare loss at target probabilities 0.25 and 0.5; predict zero-rate learning.
2. **TODO 1 (5 min):** implement a single-target negative natural-log loss. Keep supplied validation.
3. **TODO 2 (5 min):** swap editors and implement one scalar gradient-descent update. A provided loop applies it to all weights/biases.
4. **Compare (5 min):** run the baseline, then change only rate or steps. Each run resets to the same parameters. Inspect the labelled loss plot, target table and zero-update case.
5. **Record (3 min):** explain what changed and why, save code, download JSON findings and the SVG plot.

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

**Verified course mapping:** continuous Day 1 slide 73, “Watch a tiny model learn in
marimo”, launches this exercise; slide 74, “What changed when the loss fell?”, reviews
it. Slides 65–67 teach targets, loss and parameter updates. These titles/numbers are
trainer references; students do not need access to the private presentation/guide.

References: [GPT-3 pretraining](https://arxiv.org/abs/2005.14165),
[cross-entropy](https://docs.pytorch.org/docs/stable/generated/torch.nn.CrossEntropyLoss.html).
