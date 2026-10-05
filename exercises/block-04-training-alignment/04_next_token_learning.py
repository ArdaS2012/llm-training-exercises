import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="Next-Token Loss & Learning · Block 4")


@app.cell(hide_code=True)
def _():
    import json
    import math
    import sys
    from pathlib import Path
    import marimo as mo

    sys.path.insert(0, str(next(p for p in Path(__file__).resolve().parents if (p / "llm_exercises").is_dir())))
    from llm_exercises.block4 import (
        PREFIXES, VOCABULARY, FEATURES, TARGETS, check_loss, check_update, train, loss_plot,
    )
    return FEATURES, PREFIXES, TARGETS, VOCABULARY, check_loss, check_update, json, loss_plot, mo, train


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Next-Token Loss & Learning
    **Block 4 · Day 1 slide 73: Watch a tiny model learn in marimo**

    Predict → complete two short TODOs → run → change one setting → explain → download.
    Work in pairs for 20 minutes; swap editors before the second TODO.
    Show a TODO cell's code, replace `None`, and run with **Shift+Enter**.
    Waiting messages are normal. Keep function names and return lines.
    This trains a tiny output layer on local toy data, with fixed features;
    it does not train a Transformer or implement instruction tuning/RLHF/DPO.
    No model download, API key, GPU or earlier notebook is needed.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    prediction = mo.ui.text_area(label="Predict (2 minutes): which target probability has greater loss, 0.25 or 0.5? What should zero learning rate do?", full_width=True, debounce=False)
    prediction
    return (prediction,)


@app.cell(hide_code=True)
def _(FEATURES, PREFIXES, TARGETS, VOCABULARY, mo):
    mo.vstack([
        mo.md(r"""
        ## 1. Calculate a target-token loss (5 minutes)
        Vocabulary has four illustrative whole-word tokens. Rows are independent toy
        contexts; the identity feature table is supplied, not learned embeddings.
        H has shape 3 × 3, W has shape 3 × 4 and b has shape (4,).
        z = HW + b gives 3 × 4 logits; supplied row softmax gives probabilities P.
        Initial W and b are zero, so each candidate starts at probability 0.25.

        For one target, $\ell=-\log p_y$; mean loss is $\mathcal L=\frac1N\sum_i\ell_i$.
        p_y is the correct token's probability, not a token ID; log is natural logarithm.
        Loss is a scalar in nats per target. Complete `target_loss` for 0 < p ≤ 1
        using `math.log`. Keep the supplied boundary check. Zero probability has
        infinite loss; this task reports it explicitly rather than clipping silently.
        """),
        mo.ui.table([{'Prefix': s, 'Target token': VOCABULARY[t], 'Target index': t, 'Fixed features': FEATURES[i]}
                     for i, (s, t) in enumerate(zip(PREFIXES, TARGETS))], selection=None),
    ])
    return


@app.function
def target_loss(probability):
    import math
    if not 0 < probability <= 1:
        raise ValueError("Target probability must be in (0, 1].")
    # TODO 1: return the negative natural log (one line).
    loss = None
    # END TODO 1
    return loss


@app.cell(hide_code=True)
def _(check_loss, mo):
    loss_ok, loss_message = check_loss(target_loss)
    mo.vstack([
        mo.callout(loss_message, kind="success" if loss_ok else "info"),
        mo.ui.table([{'Target probability': p, 'Loss (nats)': target_loss(p)} for p in [0.25, 0.5, 1.0]], selection=None) if loss_ok else mo.md("Complete TODO 1 to see your loss calculations."),
    ])
    return (loss_ok,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. Apply a parameter update (5 minutes)
    Swap editors. Gradient descent is $\theta_{k+1}=\theta_k-\eta g_k$.
    θ is one trainable number, η is the learning rate, and g is its loss derivative.
    Complete `update_parameter` with one scalar operation. The supplied loop calls
    your function for every W and b coordinate; you do not implement matrix plumbing.
    For softmax cross-entropy, $\partial\ell/\partial z_j=p_j-\mathbf1[j=y]$.
    Thus the target gets a negative logit derivative when its probability is below 1.
    The loop computes G=(P−one-hot targets)/3, grad_W=HᵀG and grad_b=sum_rows(G).
    It evaluates loss at step 0 and after each update. Ordinary inference uses W,b
    without this update. More updates or a larger learning rate need not improve
    every example or generalization. Today's data are training examples only.
    """)
    return


@app.function
def update_parameter(parameter, gradient, learning_rate):
    # TODO 2: take one descent step (one line).
    updated = None
    # END TODO 2
    return updated


@app.cell(hide_code=True)
def _(check_update, mo):
    update_ok, update_message = check_update(update_parameter)
    mo.callout(update_message, kind="success" if update_ok else "info")
    return (update_ok,)


@app.cell(hide_code=True)
def _(mo):
    learning_rate = mo.ui.number(start=0, stop=100, value=0.5, step=0.1, label="Learning rate η")
    update_count = mo.ui.number(start=0, stop=200, value=40, step=1, label="Number of updates")
    interpretation = mo.ui.text_area(label="Record: baseline vs changed rate/steps, target probability/loss, which parameters changed, one limit", full_width=True, debounce=False)
    mo.vstack([mo.md("## 3. Run a controlled comparison (5 minutes)\nEach run starts from the same zero W,b. The baseline is η=0.5 and 40 updates; change only one setting. Try η=0 or zero updates, then restore. A very large η can cause overshoot; check the measured curve rather than assuming monotonicity. Explain the probability/loss relationship, and why this does not establish quality on unseen contexts."), learning_rate, update_count, interpretation])
    return interpretation, learning_rate, update_count


@app.cell(hide_code=True)
def _(learning_rate, loss_ok, loss_plot, mo, train, update_count, update_ok):
    baseline = train(target_loss, update_parameter) if loss_ok and update_ok else None
    run_result = train(target_loss, update_parameter, float(learning_rate.value), int(update_count.value)) if loss_ok and update_ok else None
    plot_svg = loss_plot(run_result['history']) if run_result and run_result['history'] else None
    mo.vstack([
        mo.md("Complete both TODOs to run the prepared training loop.") if not run_result else mo.md(f"**Baseline mean loss:** {baseline['history'][0]['Mean loss']:.4f} → {baseline['history'][-1]['Mean loss']:.4f}. **Selected run:** {run_result['history'][0]['Mean loss']:.4f} → {run_result['history'][-1]['Mean loss']:.4f}."),
        mo.callout(run_result['error'], kind="warn") if run_result and 'error' in run_result else mo.md("The selected result is from your completed functions; it is not a full language model."),
        mo.ui.table(run_result['rows'], selection=None) if run_result and 'rows' in run_result else mo.md("Target comparison table waits for a valid run."),
        mo.Html(plot_svg) if plot_svg else mo.md("The labelled loss plot waits for a valid run."),
    ])
    return baseline, plot_svg, run_result


@app.cell(hide_code=True)
def _(baseline, interpretation, json, learning_rate, loss_ok, mo, plot_svg, prediction, run_result, update_count, update_ok):
    _report = dict(prediction=prediction.value, interpretation=interpretation.value,
                   rate=learning_rate.value, steps=update_count.value,
                   checks=dict(loss=loss_ok, update=update_ok), baseline=baseline, selected=run_result)
    mo.vstack([
        mo.md("## 4. Save and share (3 minutes)\nSave code with Ctrl+S / Cmd+S. Download findings because widget inputs are not saved in Python. Share one target calculation, the baseline/controlled curve and an explanation at slide 74, **What changed when the loss fell?** The export includes measured probabilities, W,b and both runs, plus your notes; it does not export function source."),
        mo.download(json.dumps(_report, indent=2).encode(), filename="results-block4.json", label="Download findings and measured runs"),
        mo.download(plot_svg.encode(), filename="training-loss.svg", label="Save loss plot") if plot_svg else mo.md("Plot download becomes available after both TODOs."),
        mo.accordion({"Hints and troubleshooting": mo.md("Loss: identify the target's probability, use a natural log and consider its sign. Update: move opposite the derivative and scale by the learning rate. Zero rate should preserve all parameters. If a cell turns red, undo and check indentation/return values. The loop, softmax and gradients are supplied in llm_exercises/block4.py. Read them after finishing if useful; neither TODO is solved there. A falling training curve says nothing yet about held-out data.")}),
        mo.md("Sources: [autoregressive pretraining](https://arxiv.org/abs/2005.14165), [cross-entropy definition](https://docs.pytorch.org/docs/stable/generated/torch.nn.CrossEntropyLoss.html), [marimo](https://docs.marimo.io/getting_started/). Student instructions are self-contained here and in this block's README. Trainer mapping: Day 1 slides 65–67 and 73–74."),
    ])
    return


if __name__ == "__main__":
    app.run()
