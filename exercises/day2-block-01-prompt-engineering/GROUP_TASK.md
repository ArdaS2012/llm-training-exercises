# Exercise: test a prompt revision

**30 minutes in pairs · LLM Day 2 · room 09:40–10:10**

Build and stress-test a research intake assistant: can a prompt protect missing facts and resist instructions hidden in a document?

## Keep these slide takeaways beside you

Examples teach a pattern, not new weights. System policy and document data have different roles. Valid JSON can still contain an invented fact; a plausible calculation still needs checking.

## Before the room opens

Before class, cache/warm the pinned model and open the starter. The five-minute plenary orientation shows the three documents, schema, message controls and source-verdict fields. The pair completes both small TODOs in the room; no comparison is pre-solved.

Use the [shared setup](../../README.md) and launch from the repository root:

```sh
uv run --locked --group prompting python start.py --block d2-1
```

## Your investigation

### 0–4 · Check the reasoning

Each partner calculates the pen question independently. Complete the reasoning-prompt TODO, run its two variants and compare the actual calculation with your own. Does an explanation establish correctness? Keep the arithmetic evidence.

### 4–10 · Make your first assistant

Choose a failure to watch: missing values or instructions inside document text. Predict which case will expose it. Complete the extraction-message TODO and run the zero-/few-shot baseline on all three supplied documents. Inspect raw output and the separate schema flags. Download this baseline before editing policy.

### 10–20 · Repair one thing

Change only system policy to target that failure. Keep model, decoding, examples and all three documents fixed; rerun. Swap editor/checker at minute 15. The new checker independently audits source words instead of trusting the first partner’s judgment.

### 20–27 · Put the revision on trial

Each partner presents one before/after case: quote the source, show the raw values and judge schema versus factual correctness separately. Count fully correct cases per variant. Keep regression or no improvement; choose which policy you would use conditionally, and design a fresh input that could disprove that choice.

### 27–30 · Save your evidence

Record the policy comparison, reasoning check, decision and limitation; download findings and save code. Both partners must explain why one output passed or failed.

## Bring back

Baseline and revised policies/exports, actual raw outputs, source-backed factual judgments separate from schema flags, checked arithmetic and a conditional policy decision.

**Interpretation limit:** These three inspected cases are development diagnostics. More cases and a fresh held-out test are needed before a reliability claim. Small-model failure is a finding, not an invitation to write an ideal answer in its place.

The editor changes/runs code; the checker predicts, checks sources and challenges the conclusion. Swap at minute 15. Ask for help through the trainer’s chat/room-visit route if blocked. A failed or unchanged real result is useful when explained; never invent measurements. Save Python and download findings: saving source alone does not retain widget inputs.
