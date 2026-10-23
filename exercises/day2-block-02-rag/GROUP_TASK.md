# Exercise: diagnose your Mini-RAG

**30 minutes in pairs · LLM Day 2 · room 11:15–11:45**

Turn your own permitted documents into a research assistant, then trace one answer back through the pipeline to find what helped or failed.

## Keep these slide takeaways beside you

Chunks must keep supporting facts together. Cosine similarity ranks candidates, not truth. Reranking only reorders retrieved candidates. A citation must exist AND support the claim.

## Before the room opens

Before class, cache/warm models, check permissions and mechanically load 2–4 short own English documents. The five-minute plenary orientation shows the full source-to-answer trace and reference-label controls. Source questions, labels and both small TODOs are pair work, before any run.

Use the [shared setup](../../README.md) and launch from the repository root:

```sh
uv run --locked --group rag python start.py --block d2-2
```

## Your investigation

### 0–6 · Set a source contract

Choose two questions your own texts can answer and one whose answer is absent from ALL texts. Quote reference words now; mark the relevant chunk IDs separately for each configuration. Freeze both configurations and reserve Q2/Q3 before either run. Predict which fact a smaller/larger chunk might lose. If you inspect these cases while improving the system, call the later evaluation retrospective.

### 6–12 · Wire the evidence

Complete evidence selection and labeled-context TODOs. Inspect the feedback on your own code. Explain to your partner why a score alone is insufficient: the generator needs both the unchanged passage and its source ID.

### 12–22 · Run your experiment

Run baseline 80-word chunks and one changed chunk size for the same three questions. Hold models, questions, overlap (20 words), candidate limit (5) and passage limit (2) fixed. Swap editor/checker at minute 15. While calls run, use source texts to check the reference labels; do not tune to reserved answers.

### 22–27 · Follow the broken link

Pick one surprising result. Walk original source → chunk boundary → vector candidates → reranked/selected context → raw answer. Point to the first stage that lost or distorted support. Check the absent question across the whole corpus. Recommend the next fix and say what measurement would test it.

### 27–30 · Hand off to evaluation

Download all six question/answer/source records and your findings for Block 4. Save your source-derived labels locally. Both partners explain the traced case and one limit.

## Bring back

Own-document question/reference records, paired rankings/selected context/raw answers, source checks, a failure-stage diagnosis and one justified next fix; export retained for evaluation.

**Interpretation limit:** Two retained 80-word chunks supply up to 160 word occurrences; two 40-word chunks up to 80. Fixed overlap also changes its proportion. This tests a whole chunk setting, not boundary placement alone. Fewer chunks can produce fewer candidates/passages. Do not claim every change isolates a single mechanism.

The editor changes/runs code; the checker predicts, checks sources and challenges the conclusion. Swap at minute 15. Ask for help through the trainer’s chat/room-visit route if blocked. A failed or unchanged real result is useful when explained; never invent measurements. Save Python and download findings: saving source alone does not retain widget inputs.

**Before measuring:** the notebook displays both complete chunk inventories without any model call. Open the baseline and changed inventories, copy each supporting ID and original-source reference into **Freeze your source references**, then run. Your downloaded export preserves these source notes for Block 4.
