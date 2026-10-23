# Exercise: Learning-update investigation

**30 minutes in pairs · LLM Day 1 · rooms 14:50–15:20**

## Your investigation

What evidence would convince you that parameters learned something rather than merely ran again? Work with the running notebook, inspect its results and make a decision together. One partner edits while the other checks the prediction and evidence; swap at minute 15.

## Keep these slide takeaways beside the task

From slides 67–70 and 73–75: loss, updates, training stages and inference: **Target loss is −log(p). Gradient descent changes parameters. Inference reads existing weights; a lower training loss needs evaluation.**

These ideas tell you what to measure. Use the definitions and worked input/output examples next to each TODO whenever you need help. A successful check establishes a function contract; the comparisons below establish your understanding.

## Before rooms open

Complete the [shared setup](../../README.md), open `uv run --locked python start.py --block 4` from the student repository root and practise running/saving cells. Downloads and environment repair precede class. Live handoff: 14:45–14:50; leave the implementations and predictions for the room.

## Try it, inspect it, explain it

1. Predict which target probability, 0.25 or 0.5, receives greater loss. Implement target loss and the update function. Check one scalar update by hand; name the parameter, gradient and learning rate.

2. Run η=0.5 for 40 updates. Record before/after target probability, mean loss and one W/b entry. Repeat from the same initial state at η=0 with the same update count. Inspect both curves and parameter tables.

3. Swap editor/checker. Choose either learning rate or update count to change, write a hypothesis and keep everything else fixed. Try to improve the measured loss with a bounded number of updates. Record the chosen setting and compare with the baseline; an unchanged or worse result is useful evidence.

4. Defend a setting for this supplied training task using both probabilities and parameter changes. Separate evidence of fitting these examples from evidence of generalization, factual accuracy or alignment. Propose one unseen-context evaluation before claiming a better assistant.

## Your 30-minute route

0–4 min: predict loss/control outcomes. 4–14: implement, check a scalar update and run the baseline. 14–24: compare the zero-rate control and one chosen intervention, swapping roles at minute 15. 24–30: inspect parameters, defend a limited conclusion and export.

## Bring back

Checked loss/update calculation, baseline/zero-rate curves and parameters, one self-chosen intervention and a qualified learning claim with a next evaluation. Before changing another control, record the current setting and result in the notebook’s observation/conclusion field, or download that run. The export holds the current run and baseline, so retain intermediate evidence before replacing it. Save code separately: browser fields are retained through the findings download, not by saving Python.

Both partners should explain one result. If stuck, use the folded conceptual help or ask for a room visit. Explain honest unchanged/failed results. Stop optional exploration when six minutes remain and finish your explanation.

## Course handoff

Actual Day 1 slide **76**, followed by the existing plenary review and external quiz.
