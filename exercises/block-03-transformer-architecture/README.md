# Block 3 — Causal Masking & Sampling

Prepared for Day 1 **13:25–14:00** (35 minutes), continuous slide **58 — Apply masking and sampling in marimo**, followed by slide **59 — Compare the mask and the samples**. Supporting explanations: slide 50 (causal mask), 54 (logits), 55 (temperature), 56 (candidate filtering) and 57 (Visual Lab).

Use the [shared installation and troubleshooting guide](../../README.md). Launch from the student repository:

```sh
uv run --locked python start.py --block 3 --check
uv run --locked python start.py --block 3
```

After preparing that environment on this computer, use `uv run --offline --locked python start.py --block 3`. Wrappers forward the same arguments: `sh start.sh --block 3` or `start.cmd --block 3`. Block 1 remains the default.

## Goals and prerequisites

You should recognize Q/K/V, row-wise softmax and output logits from the earlier explanations. All tiny arrays, rendering and random draws are supplied; completing Practice 2 is not required. No LLM, GPU, API key or additional dataset is used. Python lists and list comprehensions are enough. Shapes and formulas are explained in the notebook.

## Tasks

1. **Predict (5 min):** sketch the allowed attention triangle. Predict how lower temperature and k=1 change sampling.
2. **TODO 1 (10 min):** return a new causal score matrix. Rows are receiving Queries; columns are source Keys. Preserve the diagonal/past, block the future before the prepared softmax. Inspect both heatmaps, row sums and zero future weights.
3. **TODOs 2–3 (10 min):** implement stable temperature softmax on a separate vocabulary vector, then keep and renormalize its top-k probabilities. Prepared draws use your result. Retain the original candidate order in the returned vector. Use a consistent index order for ties. The supplied inputs use positive T, 1 ≤ k ≤ vocabulary size and strictly positive input probabilities; invalid inputs beyond this domain are outside the task.
4. **Compare (5 min):** swap who edits. Compare T=0.5/2 and k=1/2 with the same seed/draw count; change just the seed or count and explain the effect. Finite fractions estimate probabilities. This holds toy logits fixed; it does not generate a sentence or update model parameters.
5. **Save/share (5 min):** save Python with Ctrl+S / Cmd+S; download both SVG heatmaps and `results-block3.json` with predictions, checks, probabilities, counts, settings and explanations. Browser fields are not preserved by saving Python. Share a row-B interpretation and one sampling comparison at slide 59.

Open the notebook cell code, edit only `# TODO` / `# END TODO` regions and run with Shift+Enter. The untouched starter shows friendly waiting messages. Masking and sampling tasks are independent. Hints and checks help with triangle orientation, normalization, numerical stability and k boundaries; they do not provide a completed implementation.

## Findings to explain

Which attention entries disappear, and why? Why do valid rows still sum to one? What changes when T changes? What does k=1 permit? Why do observed counts differ from theoretical probabilities? Explain how masking controls access to context while sampling selects a vocabulary candidate. Top-p remains the Visual Lab comparison, rather than an extra coding TODO.

## Help and sources

Undo if a cell turns red; check indentation, function names and return shapes. A score of zero is not blocked. Temperature scaling belongs before exponentiation. Top-k must renormalize retained mass, not move candidates into different positions. Keep the seed fixed to repeat a run, rather than resetting before every draw.

[Original Transformer](https://arxiv.org/abs/1706.03762) explains decoder masking. [Generation parameters](https://huggingface.co/docs/transformers/main/en/main_classes/text_generation) describes temperature and top-k. [marimo basics](https://docs.marimo.io/getting_started/) explains editing/running cells. Optional private trainer resource: [guide §16](https://github.com/ArdaS2012/EDV_Training/blob/main/docs/LLM_Training/llm_day1/03_transformer_architecture.md#slide-16). Students do not need access to it.
