import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="Tiny Attention Head · Block 2")


@app.cell(hide_code=True)
def _():
    import json
    import sys
    from pathlib import Path
    import marimo as mo
    sys.path.insert(0, str(next(p for p in Path(__file__).resolve().parents if (p / "llm_exercises").is_dir())))
    from llm_exercises.block2 import Q, K, V, changed_inputs, check_scores, check_softmax, check_values, pipeline, matrix_rows, heatmap_svg

    return (
        K,
        Q,
        V,
        changed_inputs,
        check_scores,
        check_softmax,
        check_values,
        heatmap_svg,
        json,
        matrix_rows,
        mo,
        pipeline,
    )


@app.cell(hide_code=True)
def _(K, Q, V, mo):
    mo.md(rf"""
    # Build a tiny attention head
    **Block 2 · Day 1 slide 38 · 35 minutes in pairs**

    Predict → complete three short TODOs → inspect → change one input → explain.
    All setup, toy matrices, checks and rendering are prepared. Show TODO code,
    replace `None` and run with **Shift+Enter**. Preserve function names/return lines.
    Waiting feedback is normal. Swap who edits after the weight calculation.
    No model, API key, GPU, trained sentence relationships or extra download is used.

    Q = {Q}, K = {K}, V = {V}; each has shape 3 × 2.
    n=3 positions A/B/C, d_k=2 matching features, d_v=2 Value features.
    Q rows receive context, K/V rows supply it. These are dimensionless toy values.
    $S=QK^\top/\sqrt{{d_k}},\quad A=\mathrm{{softmax}}_{{\mathrm{{row}}}}(S),\quad O=AV$.
    S/A have shape n × n; O has shape n × d_v.
    This is unrestricted attention; causal masking comes in Block 3.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    prediction = mo.ui.text_area(label="Predict the strongest sources for Query A; state what the axes mean", full_width=True, debounce=False)
    mo.vstack([mo.md("## 1. Predict and inspect (4 minutes)\nKeep your Attention Detective hypothesis, but do not treat these arrays as measurements of the sentence."), prediction])
    return (prediction,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. TODO 1 — Scaled scores (7 minutes)
    For every Query q_i and Key k_j, compute their dot product, then divide by √d_k.
    A dot product multiplies corresponding coordinates and adds the products.
    `zip(q, k)` pairs coordinates; `sum` adds; `math.sqrt` takes a square root.
    Return a new nested list, one row per Query, one column per Key.
    Use feature width `len(q[0])`, not the number of positions.
    A single row of Q and two rows of K should return shape 1 × 2.
    """)
    return


@app.function
def scaled_scores(q, k):
    import math
    # TODO 1: pair each Query with every Key, then scale (about two lines).
    scores = None
    # END TODO 1
    return scores


@app.cell(hide_code=True)
def _(check_scores, mo):
    scores_ok, scores_message = check_scores(scaled_scores)
    mo.callout(scores_message, kind="success" if scores_ok else "info")
    return (scores_ok,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. TODO 2 — Stable row softmax (8 minutes)
    $A_{ij}=\exp(S_{ij}-m_i)/\sum_l\exp(S_{il}-m_i)$, where m_i=max_j S_ij.
    The common row shift cancels in the ratio; it prevents exp(1000) overflowing.
    Each row is a separate source distribution for one Query; sum along columns.
    Loop over the supplied rows, use `math.exp` after subtracting `max(row)`,
    divide by the sum of that row's exponential weights, and append the new row.
    Return the same table shape. Equal scores produce equal weights.
    An illustrative row [0,0] has weights [0.5,0.5]; one source always has weight 1.
    """)
    return


@app.function
def row_probabilities(scores):
    import math
    # TODO 2: calculate and append probabilities for each row (about four lines).
    probabilities = None
    # END TODO 2
    return probabilities


@app.cell(hide_code=True)
def _(check_softmax, mo):
    weights_ok, weights_message = check_softmax(row_probabilities)
    mo.callout(weights_message, kind="success" if weights_ok else "info")
    return (weights_ok,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. TODO 3 — Weighted Values (6 minutes)
    $O_{ir}=\sum_j A_{ij}V_{jr}$: j indexes sources; r indexes Value coordinates.
    For each Query row, compute one weighted sum for each of d_v Value features.
    `len(v[0])` counts Value features; `len(v)` counts source positions.
    Return shape Query count × d_v; d_v need not equal d_k or source count.
    Example: weights [0.25,0.75] and Values [[0,2],[4,0]] mix to [3,0.5].
    Convex mixing is a calculation, not a guarantee of meaningful language features.
    """)
    return


@app.function
def mix_values(weights, v):
    # TODO 3: sum across sources for each Value coordinate (about 1–3 lines).
    outputs = None
    # END TODO 3
    return outputs


@app.cell(hide_code=True)
def _(check_values, mo):
    values_ok, values_message = check_values(mix_values)
    mo.callout(values_message, kind="success" if values_ok else "info")
    return (values_ok,)


@app.cell(hide_code=True)
def _(mo):
    target = mo.ui.dropdown(options=["Q", "K", "V"], value="Q", label="Change which matrix?")
    changed_row = mo.ui.dropdown(options={"A": 0, "B": 1, "C": 2}, value="A", label="Position row")
    changed_column = mo.ui.dropdown(options={"Feature 0": 0, "Feature 1": 1}, value="Feature 0", label="Feature coordinate")
    delta = mo.ui.number(start=-3, stop=3, step=0.5, value=0, label="Add to one coordinate (0 = baseline)")
    change_prediction = mo.ui.text_area(label="Before changing: which scores, weights or outputs will change, and why?", full_width=True, debounce=False)
    observation = mo.ui.text_area(label="After changing: compare baseline/results; explain one output row and one limitation", full_width=True, debounce=False)
    mo.vstack([mo.md("## 5. Controlled change (7 minutes)\nPredict first; change just one coordinate. Baseline Q/K/V remain preserved. First change Q, then reset delta to 0 before trying K or V. A Value-only change isolates payload mixing. The fixed heatmap scale is 0–1; greater blue intensity means greater weight, not word importance."), change_prediction, target, changed_row, changed_column, delta, observation])
    return (
        change_prediction,
        changed_column,
        changed_row,
        delta,
        observation,
        target,
    )


@app.cell(hide_code=True)
def _(
    K,
    Q,
    V,
    changed_column,
    changed_inputs,
    changed_row,
    delta,
    heatmap_svg,
    matrix_rows,
    mo,
    pipeline,
    scores_ok,
    target,
    values_ok,
    weights_ok,
):
    baseline = pipeline(scaled_scores, row_probabilities, mix_values, Q, K, V, (scores_ok, weights_ok, values_ok))
    changed_q, changed_k, changed_v = changed_inputs(target.value, changed_row.value, changed_column.value, delta.value)
    experiment = pipeline(scaled_scores, row_probabilities, mix_values, changed_q, changed_k, changed_v, (scores_ok, weights_ok, values_ok))
    baseline_svg = heatmap_svg(baseline['weights'], "Baseline attention") if baseline['weights'] is not None else None
    experiment_svg = heatmap_svg(experiment['weights'], "Changed-input attention") if experiment['weights'] is not None else None
    _items = [mo.md(f"Changed Q={changed_q}, K={changed_k}, V={changed_v}")]
    for _label, _result, _svg in [('Baseline', baseline, baseline_svg), ('Changed input', experiment, experiment_svg)]:
        _items.append(mo.md(f"### {_label}"))
        for _stage, _matrix in _result.items():
            _items.append(mo.md(f"**{_stage}**"))
            _items.append(mo.ui.table(matrix_rows(_matrix), selection=None) if _matrix is not None else mo.md("Waiting for the required TODOs."))
        if _svg:
            _items.extend([mo.Html(_svg), mo.md(f"Row sums: {[sum(row) for row in _result['weights']]}")])
    mo.vstack(_items)
    return baseline, baseline_svg, experiment, experiment_svg


@app.cell(hide_code=True)
def _(
    baseline,
    baseline_svg,
    change_prediction,
    changed_column,
    changed_row,
    delta,
    experiment,
    experiment_svg,
    json,
    mo,
    observation,
    prediction,
    scores_ok,
    target,
    values_ok,
    weights_ok,
):
    _report = dict(prediction=prediction.value, change_prediction=change_prediction.value, observation=observation.value,
                   change=dict(matrix=target.value, row=changed_row.value, column=changed_column.value, delta=delta.value),
                   baseline=baseline, experiment=experiment, checks=dict(scores=scores_ok, weights=weights_ok, values=values_ok))
    _items = [mo.md("## 6. Save and share (3 minutes)\nSave Python with Ctrl+S / Cmd+S. Download findings before closing: saving code does not retain browser fields/widget values. Bring both heatmaps, scores/weights/outputs, your predictions and one explanation to slides 39–40. These toy weights do not establish linguistic relationships or explain a full model."),
              mo.download(json.dumps(_report, indent=2).encode(), filename="results-block2.json", label="Download my attention findings")]
    if baseline_svg:
        _items.extend([mo.download(baseline_svg.encode(), filename="attention-baseline.svg", label="Save baseline heatmap"), mo.download(experiment_svg.encode(), filename="attention-changed.svg", label="Save changed heatmap")])
    _items.extend([mo.accordion({"Hints": mo.md("Scores: think Query rows × Key rows. Softmax: normalize each row after exponentiating. Values: sum over source j while keeping output feature r. If a cell turns red, undo and inspect indentation and return shapes. Checks use different sizes to catch accidental hard-coding.")}), mo.md("Sources: [Attention Is All You Need, §3.2](https://arxiv.org/abs/1706.03762), [marimo basics](https://docs.marimo.io/getting_started/). The student README supplies all task instructions; trainer-only guide §12 maps to Day 1 slide 38.")])
    mo.vstack(_items)
    return


if __name__ == "__main__":
    app.run()
