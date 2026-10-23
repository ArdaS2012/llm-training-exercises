# Exercise: Attention circuit investigation

**30 minutes in pairs · LLM Day 1 · rooms 11:05–11:35**

## Your investigation

Which change reroutes information, and which changes only the information being carried? Work with the running notebook, inspect its results and make a decision together. One partner edits while the other checks the prediction and evidence; swap at minute 15.

## Keep these slide takeaways beside the task

From slides 31–37: Q/K/V, scaling, row softmax and weighted Values: **Q/K determine matching scores. Row softmax gives source weights. O = AV mixes the Value payloads.**

These ideas tell you what to measure. Use the definitions and worked input/output examples next to each TODO whenever you need help. A successful check establishes a function contract; the comparisons below establish your understanding.

## Before rooms open

Complete the [shared setup](../../README.md), open `uv run --locked python start.py --block 2` from the student repository root and practise running/saving cells. Downloads and environment repair precede class. Live handoff: 11:00–11:05; leave the implementations and predictions for the room.

## Try it, inspect it, explain it

1. Predict Query A’s strongest source. Complete the three small functions using the notebook’s shapes and worked softmax example. Check row sums and manually trace one output coordinate. Heatmap rows receive information; columns supply it.

2. Keep the baseline. Add +1 to Q row A, feature 0. Record which rows of scores, weights and outputs change, with numerical evidence. Reset delta to zero before the next run.

3. Add +1 to V row A, feature 0 with Q/K fixed. Compare both heatmaps and output tables. Use the relevant source weight to explain one output difference. Swap editor/checker and let the checker operate the next test.

4. Choose a single K coordinate, write a prediction, then test it. Look for either an affected receiver or a receiver that stays fixed. Use its dot product to explain the result. Decide which matrix you would change to alter routing versus payload, and state why this tiny head cannot explain a complete trained model.

## Your 30-minute route

0–4 min: predict and label the axes. 4–14: implement, use feedback and trace one output. 14–24: run Q/V interventions and swap roles at minute 15. 24–30: test your own Key prediction, defend the mechanism and export.

## Bring back

Baseline and Q/V comparisons, one worked weighted sum, a predicted/measured Key edit, invariant checks and a mechanism explanation with a limit. Before changing another control, record the current setting and result in the notebook’s observation/conclusion field, or download that run. The export holds the current run and baseline, so retain intermediate evidence before replacing it. Save code separately: browser fields are retained through the findings download, not by saving Python.

Both partners should explain one result. If stuck, use the folded conceptual help or ask for a room visit. Explain honest unchanged/failed results. Stop optional exploration when six minutes remain and finish your explanation.

## Course handoff

Actual Day 1 slide **39**, followed by the existing plenary review and external quiz.
