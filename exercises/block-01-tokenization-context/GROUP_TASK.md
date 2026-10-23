# Exercise: Tokenizer design desk

**30 minutes in pairs · LLM Day 1 · rooms 09:35–10:05**

## Your investigation

Can a small change in training text change the rules used to encode new words? Work with the running notebook, inspect its results and make a decision together. One partner edits while the other checks the prediction and evidence; swap at minute 15.

## Keep these slide takeaways beside the task

From slides 13–20: vocabulary, BPE/SentencePiece, context and cost: **Frequent adjacent pieces become vocabulary entries. Encoding reuses learned rules. Every resulting token consumes context.**

These ideas tell you what to measure. Use the definitions and worked input/output examples next to each TODO whenever you need help. A successful check establishes a function contract; the comparisons below establish your understanding.

## Before rooms open

Complete the [shared setup](../../README.md), open `uv run --locked python start.py --block 1` from the student repository root and practise running/saving cells. Downloads and environment repair precede class. Live handoff: 09:30–09:35; leave the implementations and predictions for the room.

## Try it, inspect it, explain it

1. Predict the first merge from at least two corpus contributions. Build the weighted-count and merge functions, using the supplied small input/output examples. Trace one merge by hand before trusting the three-round display.

2. Keep the baseline, then change only `can` from 10 to 20. Predict before running. Inspect the changed merge order and the pieces of `maps` and unseen `rap`. Explain one choice using a count, and explain an unchanged probe if that is what you observe.

3. Choose one additional `can` frequency using the existing control. Try to make a different merge win, rather than turning controls at random. Record the frequency and the winning count. Restore the baseline before comparing the supplied real English/German/code tokenizer examples.

4. Use the prepared real-tokenizer counts and context budget to choose what to remove or shorten. Give a tradeoff. Explain why training this character-BPE toy does not measure a language model’s answer quality or latency.

## Your 30-minute route

0–4 min: inspect the corpus and predict. 4–14: implement and check the two steps. 14–24: compare frequency changes and unseen-word encoding, swapping editor/checker at minute 15. 24–30: inspect real token counts, decide on the budget and export evidence.

## Bring back

Initial prediction, baseline and changed-frequency traces, your extra frequency test, unseen-word explanation, and a context-budget recommendation with one limitation. Before changing another control, record the current setting and result in the notebook’s observation/conclusion field, or download that run. The export holds the current run and baseline, so retain intermediate evidence before replacing it. Save code separately: browser fields are retained through the findings download, not by saving Python.

Both partners should explain one result. If stuck, use the folded conceptual help or ask for a room visit. Explain honest unchanged/failed results. Stop optional exploration when six minutes remain and finish your explanation.

## Course handoff

Actual Day 1 slide **21**, followed by the existing plenary review and external quiz.
