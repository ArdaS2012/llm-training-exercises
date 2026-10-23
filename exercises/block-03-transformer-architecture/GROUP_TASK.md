# Exercise: Decoder controls bench

**30 minutes in pairs · LLM Day 1 · rooms 13:35–14:05**

## Your investigation

Can you stop future information leaking in while explaining why repeated token draws differ? Work with the running notebook, inspect its results and make a decision together. One partner edits while the other checks the prediction and evidence; swap at minute 15.

## Keep these slide takeaways beside the task

From slides 50–58: causal visibility, logits, temperature and top-k/top-p: **Causal masks restrict source positions before softmax. Temperature reshapes probabilities. Top-k limits vocabulary candidates.**

These ideas tell you what to measure. Use the definitions and worked input/output examples next to each TODO whenever you need help. A successful check establishes a function contract; the comparisons below establish your understanding.

## Before rooms open

Complete the [shared setup](../../README.md), open `uv run --locked python start.py --block 3` from the student repository root and practise running/saving cells. Downloads and environment repair precede class. Live handoff: 13:30–13:35; leave the implementations and predictions for the room.

## Try it, inspect it, explain it

1. Predict which source positions row B may use. Complete the causal-mask function. Verify future weights are zero, diagonal/past are eligible and rows sum to one. Explain why replacing a blocked score by zero would still permit a contribution.

2. Complete temperature softmax and top-k using their notebook explanations and independent checks. Compare T=0.5 and T=2 with k=2, seed 42 and 200 draws fixed. Read both probabilities and counts, rather than judging one sampled token.

3. At fixed T compare k=1 and k=2. Swap roles. Predict what changing only the seed will affect, then test it. Restore seed 42, increase only the draw count from 200 to 1000, and record one frequency/probability discrepancy.

4. Choose a supplied setting for repeatable fixed-prefix selection and one for more varied selection. Justify each from the retained candidates and measured distribution. Explain why neither setting guarantees truth, and why these independent draws do not simulate a whole generated conversation.

## Your 30-minute route

0–4 min: predict visibility and label the two spaces. 4–14: implement the three bounded functions using their worked contracts. 14–24: inspect the heatmap and controlled T/k comparisons, swapping roles at minute 15. 24–30: challenge the sampling claim with seed/draw changes, decide and export.

## Bring back

Masked heatmap, fixed-logit T/k table, k=1 boundary, seed/draw comparison and two justified decoding choices with a limitation. Before changing another control, record the current setting and result in the notebook’s observation/conclusion field, or download that run. The export holds the current run and baseline, so retain intermediate evidence before replacing it. Save code separately: browser fields are retained through the findings download, not by saving Python.

Both partners should explain one result. If stuck, use the folded conceptual help or ask for a room visit. Explain honest unchanged/failed results. Stop optional exploration when six minutes remain and finish your explanation.

## Course handoff

Actual Day 1 slide **60**, followed by the existing plenary review and external quiz.
