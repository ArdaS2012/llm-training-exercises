# Block 2 — Build a Tiny Attention Head

Day 1 **11:25–12:00**, 35 minutes in pairs. Continuous slide **38 — Build a tiny attention head in marimo** launches the practice; slides **39 — Trace one row from score to output** and **40 — What did your change actually change?** support sharing. Slides 31–36 explain the equations and heatmap.

Use the [shared setup and troubleshooting](../../README.md), then run from this repository:

```sh
uv run --locked python start.py --block 2 --check
uv run --locked python start.py --block 2
```

After setup on this computer: `uv run --offline --locked python start.py --block 2`. Wrappers support `sh start.sh --block 2` and `start.cmd --block 2`. Block 1 remains the default. No new packages, models, API keys or asset downloads are needed.

## Goals and prerequisites

Know what Q, K and V represent from the slide explanation; basic Python lists/loops are enough. Three supplied 3 × 2 toy matrices illustrate the arithmetic, not learned sentence relationships. Implement scaled scores, stable row-softmax and weighted Values. Read Query/source axes, check row sums, and distinguish changes in matching (Q/K) from changes in payload (V). This is one unrestricted attention head: no causal mask, learned projections, positional-encoding implementation, residuals, training or multi-head combination. Those explanations belong to the slides and later blocks.

## Pair tasks

1. **Predict and inspect, 4 min:** keep your Attention Detective hypothesis; identify n, d_k, d_v and the heatmap axes. Predict the preferred sources for Query A.
2. **TODO 1, 7 min:** calculate the Query–Key dot products divided by √d_k, returning a new nested list. Inputs have matching feature widths; output shape is Query count × Key count.
3. **TODO 2, 8 min:** return stable row probabilities. Subtract a row maximum before exponentiating and normalize each row separately. Row totals should be approximately one, including equal-score and single-source cases.
4. **TODO 3, 6 min:** swap editors; mix Value vectors using each weight row. Output shape is Query count × d_v; Value feature count can differ from source count. Inspect scores, weights, outputs and the baseline heatmap.
5. **Controlled change, 7 min:** predict, select Q/K/V, a position and coordinate, then add a nonzero delta. Change only one coordinate. Compare with the preserved baseline; reset delta to zero before trying another intervention. Explain one output row and what changed/stayed fixed. Q and K changes affect matching differently; a V-only intervention isolates payload mixing.
6. **Save/share, 3 min:** save Python, download both SVG heatmaps and `results-block2.json` (matrices, settings, predictions, checks and interpretation). Browser fields are session values: saving Python does not preserve them. Bring one heatmap-cell interpretation and one causal explanation of your input change to slides 39–40.

Reveal code at a TODO, replace `None`, keep the function name and return structure, and run **Shift+Enter**. Prepared cells are hidden; TODO functions remain visible. Later unfinished tasks do not hide earlier completed results. All arrays are finite, nonempty, rectangular lists with compatible dimensions. Invalid/empty input handling is outside these short tasks.

## Checks and help

Wait messages are normal until you complete a step. A shape failure usually means confusing sequence positions with features. Scores need all Query–Key pairs; softmax needs a separate normalization per row; mixing sums across source positions for each Value coordinate. A high attention weight is not a direct importance score or a complete explanation of a model. The tiny head neither trains language relationships nor measures model quality.

Hints and boundary feedback are in the notebook. Undo if a cell turns red; check indentation and return values. Restart/port/network help is in the shared README.

[Original Transformer, §3.2](https://arxiv.org/abs/1706.03762) defines scaled dot-product attention. [marimo basics](https://docs.marimo.io/getting_started/) explains editing and running cells. Optional private trainer resource: [guide §12](https://github.com/ArdaS2012/EDV_Training/blob/main/docs/LLM_Training/llm_day1/02_self_attention.md#slide-12); students do not need access to it.
