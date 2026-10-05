import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="Masking & Sampling · Block 3")


@app.cell(hide_code=True)
def _():
    import json
    import math
    import sys
    from pathlib import Path
    import marimo as mo

    sys.path.insert(0, str(next(p for p in Path(__file__).resolve().parents if (p / "llm_exercises").is_dir())))
    from llm_exercises.block3 import (
        Q, K, V, SCORES, LOGITS, CANDIDATES, row_softmax,
        check_mask, check_temperature, check_top_k, comparison, heatmap_svg,
    )

    return (
        CANDIDATES,
        K,
        LOGITS,
        Q,
        SCORES,
        V,
        check_mask,
        check_temperature,
        check_top_k,
        comparison,
        heatmap_svg,
        json,
        mo,
        row_softmax,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Masking & Sampling
    **Block 3 · Day 1 slide 58: Apply masking and sampling in marimo**

    Predict → complete three short TODOs → change one input → interpret → download.
    Work in pairs; swap the editor halfway through. This is a 35-minute exercise.
    Supplied toy arrays make this independent of your progress in the Block 2 notebook.
    No model, API key or additional data download is needed.

    Show a TODO cell's code, replace `None`, and run with **Shift+Enter**.
    Keep function names and return lines. Waiting messages are normal.
    All matrices/logits are illustrative, not trained-model measurements.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    prediction = mo.ui.text_area(label="Predict: which cells are blocked? What will lower T and k=1 do?", full_width=True, debounce=False)
    prediction
    return (prediction,)


@app.cell(hide_code=True)
def _(K, Q, SCORES, V, mo):
    mo.md(f"""
    ## 1. Add a causal mask (10 minutes after 5 minutes predicting)
    Supplied Q = {Q}, K = {K}, V = {V}. Each has shape 3 × 2.
    Scores S = QKᵀ / √2 have shape 3 × 3: `{SCORES}`.
    Rows receive context (Queries); columns provide it (Keys/Values).
    Complete `causal_scores`: return a **new nested list**, retaining S[i][j]
    for j ≤ i and replacing future entries with `-math.inf`.
    Python lists use `scores[i][j]`; `len(scores)` is the position count.
    Prepared row-wise softmax then produces A = softmax(S + M).
    M is 0 on allowed entries and −∞ elsewhere; exp(−∞)=0.
    Masking happens **before** softmax. Keep the diagonal to avoid empty rows.
    """)
    return


@app.function
def causal_scores(scores):
    # TODO 1: construct the masked score table (about 1–3 lines).
    masked = None
    # END TODO 1
    return masked


@app.cell(hide_code=True)
def _(SCORES, check_mask, heatmap_svg, mo, row_softmax):
    mask_ok, mask_message = check_mask(causal_scores)
    unmasked = [row_softmax(row) for row in SCORES]
    masked_weights = [row_softmax(row) for row in causal_scores(SCORES)] if mask_ok else None
    unmasked_svg = heatmap_svg(unmasked, "Unmasked attention")
    masked_svg = heatmap_svg(masked_weights, "Causal attention") if mask_ok else None
    mo.vstack([
        mo.callout(mask_message, kind="success" if mask_ok else "info"),
        mo.Html(unmasked_svg),
        mo.Html(masked_svg) if mask_ok else mo.md("Complete TODO 1 to reveal the causal heatmap."),
        mo.md(f"Row sums: {[sum(row) for row in masked_weights]} · future weights zero: {all(masked_weights[i][j] == 0 for i in range(3) for j in range(i+1, 3))}") if mask_ok else mo.md("Check the triangle orientation, diagonal and row sums."),
    ])
    return mask_ok, masked_svg, masked_weights, unmasked_svg


@app.cell(hide_code=True)
def _(CANDIDATES, LOGITS, mo):
    mo.md(rf"""
    ## 2. Temperature and top-k (10 minutes)
    Vocabulary candidates: {CANDIDATES}; logits z = {LOGITS}, shape (4,).
    These scores are separate from the attention matrix.

    For T > 0, $p_i(T)=\exp(z_i/T)/\sum_j\exp(z_j/T)$.
    z and T are dimensionless; p is a vocabulary probability vector summing to 1.
    Complete the three steps: scale each logit, exponentiate after subtracting
    the largest scaled value, then divide each weight by the sum of weights.
    Use `math.exp`, `max`, `sum` and list comprehensions. A shared shift preserves
    the distribution and prevents overflow (try logits shifted by +1000).
    At equal logits, candidates are equally likely. T=0 is excluded;
    greedy selection is a separate rule.
    """)
    return


@app.function
def temperature_probs(logits, temperature):
    # TODO 2: stable temperature softmax (about three lines).
    scaled = None
    weights = None
    probabilities = None
    # END TODO 2
    return probabilities


@app.cell(hide_code=True)
def _(check_temperature, mo):
    temperature_ok, temperature_message = check_temperature(temperature_probs)
    mo.callout(temperature_message, kind="success" if temperature_ok else "info")
    return (temperature_ok,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Keep the k largest probabilities, with a deterministic tie order.
    Return a list of the **same length**: discarded candidates get 0.
    Normalize the retained mass: $q_i=p_i\mathbf{1}[i\in K]/\sum_{j\in K}p_j$.
    K is the set of retained indices; here 1 ≤ k ≤ vocabulary size and p_i > 0.
    `sorted(range(len(probabilities)), key=probabilities.__getitem__, reverse=True)`
    orders indices by probability. Use a slice to select k and a membership check
    to build the full vector. The prepared random draw uses your q afterwards.
    Top-p was explored in the Visual Lab; today's coding implements top-k only.
    """)
    return


@app.function
def top_k_probs(probabilities, k):
    # TODO 3: select indices, retain weights, renormalize (about three lines).
    kept = None
    retained = None
    normalized = None
    # END TODO 3
    return normalized


@app.cell(hide_code=True)
def _(check_top_k, mo):
    top_k_ok, top_k_message = check_top_k(top_k_probs)
    mo.callout(top_k_message, kind="success" if top_k_ok else "info")
    return (top_k_ok,)


@app.cell(hide_code=True)
def _(mo):
    seed = mo.ui.number(start=0, stop=10000, value=42, step=1, label="Random seed")
    draws = mo.ui.number(start=10, stop=5000, value=200, step=10, label="Draws per fixed distribution")
    interpretation = mo.ui.text_area(label="Record: row B, temperature/top-k comparison, one controlled change, masking vs sampling", full_width=True, debounce=False)
    mo.vstack([mo.md("## 3. Compare and explain (5 minutes)\nCompare T=0.5/2 and k=1/2. Hold seed and sample count fixed, then change just the seed or draw count. Counts estimate probabilities; rare events need not appear. These are repeated fixed-prefix draws, not generated text. We reset the generator once per setting, never before each draw."), seed, draws, interpretation])
    return draws, interpretation, seed


@app.cell(hide_code=True)
def _(comparison, draws, mo, seed, temperature_ok, top_k_ok):
    sample_rows = comparison(temperature_probs, top_k_probs, int(seed.value), int(draws.value)) if temperature_ok and top_k_ok else []
    mo.ui.table(sample_rows, selection=None) if sample_rows else mo.md("Complete TODOs 2 and 3 to see sampling comparisons. TODO 1 is independent.")
    return (sample_rows,)


@app.cell(hide_code=True)
def _(
    draws,
    interpretation,
    json,
    mask_ok,
    masked_svg,
    masked_weights,
    mo,
    prediction,
    sample_rows,
    seed,
    temperature_ok,
    top_k_ok,
    unmasked_svg,
):
    _report = dict(prediction=prediction.value, interpretation=interpretation.value, seed=seed.value, draws=draws.value,
                   masked_weights=masked_weights, sampling=sample_rows,
                   checks=dict(mask=mask_ok, temperature=temperature_ok, top_k=top_k_ok))
    mo.vstack([
        mo.md("## 4. Save and share (5 minutes)\nSave code with Ctrl+S / Cmd+S. Browser text and widget values are not saved in Python: download findings before closing. Share both heatmaps, the table and your explanation at slide 59, **Compare the mask and the samples**."),
        mo.download(json.dumps(_report, indent=2).encode(), filename="results-block3.json", label="Download findings and comparison table"),
        mo.download(unmasked_svg.encode(), filename="unmasked-attention.svg", label="Save unmasked heatmap"),
        mo.download(masked_svg.encode(), filename="causal-attention.svg", label="Save causal heatmap") if masked_svg else mo.md("Causal heatmap download becomes available after TODO 1."),
        mo.accordion({"Hints and troubleshooting": mo.md("Mask: compare column index to row index; zero is a valid score, not a block. Temperature: scale before exponentiating and sum along the vocabulary. Top-k: retain original positions before normalizing. If a cell turns red, undo and check indentation/return values. k=1 should permit only one token. Sample fractions need not exactly equal probabilities.")}),
        mo.md("Sources: [Transformer decoder masking](https://arxiv.org/abs/1706.03762), [generation parameters](https://huggingface.co/docs/transformers/main/en/main_classes/text_generation), [marimo](https://docs.marimo.io/getting_started/). Trainer-only explanation: Day 1 guide §16, slides 50 and 54–59. Student instructions are in this notebook and its README."),
    ])
    return


if __name__ == "__main__":
    app.run()
