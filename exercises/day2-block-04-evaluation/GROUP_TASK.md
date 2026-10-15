# Exercise: audit an evaluation decision

**Exercise + breakout · LLM Day 2 Block 4 · 15 minutes in pairs**

Learning goal: Distinguish retrieval success, answer correctness and judge reliability in a defensible evaluation.

## Before the room opens

Load the paired teaching fixtures and prepare the pair’s original Mini-RAG export and per-variant ground-truth IDs. Preflight the real judge. Explain dev/test versus retrospective diagnostics and denominators; leave the scoring TODO for rooms.

Use the [shared setup](../../README.md); model downloads and launch checks happen before the task. Start from the repository root with `uv run --locked --group prompting python start.py --block d2-4`. Keep the starter open. Prerequisite TODOs discussed in plenary belong to setup; the task below is the room assignment.

## Your group task

1. Predict a tradeoff and implement the scoring TODO. Compare the fixture configurations at k=2; report exact match, schema validity, recall and their denominators. Verify one case manually.

2. Rescore at k=3 without regenerating answers. Explain which metric can change and why. Load the prepared own Mini-RAG records and label the evaluation design honestly.

3. Rate one case independently from source evidence, then run the actual judge. Record disagreement, agreement or schema failure; choose a configuration conditionally and specify a fresh held-out test.

## Bring back

Per-case/aggregate report, manual score check, k comparison, real judge/source comparison and a justified decision.

Use the notebook’s prediction/observation fields. Save the Python source and download findings to retain browser inputs and measurements. Both partners should be able to explain the conclusion; swap editor/checker around halfway. If you finish early, state a competing explanation and a new controlled test that would distinguish it.

## Work within the timebox

2 minutes to predict and agree; 7 to implement and compare; 4 to diagnose and defend; 2 to record/export. Ask for help through the trainer’s chat/room-visit route if blocked. Return to plenary for review and the scheduled quiz. Honest unchanged or failed results count as evidence when they are explained; do not invent measurements.
