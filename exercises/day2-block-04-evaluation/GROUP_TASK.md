# Exercise: audit an evaluation decision

**30 minutes in pairs · LLM Day 2 · room 13:45–14:15**

Act as the release reviewers for your own Mini-RAG: use measured evidence to decide which version, if either, deserves another test.

## Keep these slide takeaways beside you

Correctness, format and retrieval measure different things. Recall@k divides unique relevant IDs found by all relevant IDs; an empty relevant set is undefined. A judge is another fallible measurement. Previously inspected cases are retrospective.

## Before the room opens

Before class, cache/warm the judge and open the fixture notebook. Keep your own Block 2 export and source-derived labels ready after lunch. The concepts on slides 57–62 explain frozen tests, denominators and independent ratings; there is no additional setup slot. The room starts with a manual prediction before coding.

Use the [shared setup](../../README.md) and launch from the repository root:

```sh
uv run --locked --group prompting python start.py --block d2-4
```

## Your investigation

### 0–5 · Challenge a score

Agree what would make you prefer one configuration. On one fixture, calculate exact match, schema validity and Recall@2 by hand before running code. State every denominator; predict what k=3 can change. Fixtures are authored calibration cases, not evidence that a model performs well.

### 5–12 · Build and cross-check

Complete the single scoring TODO. Compare paired fixture configurations at k=2 and reconcile your manual case. Rescore at k=3 without regenerating answers. Explain why retrieval can change while saved-answer correctness and format remain fixed.

### 12–24 · Audit your actual assistant

Switch to your own Block 2 export, using original-document references and per-variant relevant IDs. Keep its evaluation-design label honest. Swap editor/checker at minute 15. One partner independently rates a chosen case from source evidence; then run the real model judge and compare its raw rating/schema. Record agreement, disagreement or unavailable/invalid judgment honestly.

### 24–27 · Make a release decision

Inspect one consequential failed or ambiguous case. Choose a configuration conditionally, or reject both. Name which metric supports the choice, one tradeoff, and a fresh held-out question that could reverse the decision. The checking partner challenges the claim using the original source.

### 27–30 · Save an auditable report

Export the per-case/aggregate report, manual check, k comparison, source-versus-judge evidence and decision. Save code; both partners must explain what the report cannot establish.

## Bring back

Manual score check, per-case and aggregate report, saved-answer k comparison, own-document human/judge comparison and a conditional release decision with a fresh test.

**Interpretation limit:** A few convenient records cannot certify an application. Exact match can reject a correct paraphrase; free-text answers may fail an irrelevant JSON contract. Choose metrics for the task and keep technical judge failures separate from agreement.

The editor changes/runs code; the checker predicts, checks sources and challenges the conclusion. Swap at minute 15. Ask for help through the trainer’s chat/room-visit route if blocked. A failed or unchanged real result is useful when explained; never invent measurements. Save Python and download findings: saving source alone does not retain widget inputs.
