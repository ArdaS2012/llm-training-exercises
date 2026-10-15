# Exercise: test a prompt revision

**Exercise + breakout · LLM Day 2 Block 1 · 15 minutes in pairs**

Learning goal: Test a prompt hypothesis against factual and formatting evidence while holding the model and cases fixed.

## Before the room opens

Preload the pinned model before class. In plenary, complete the independent reasoning-prompt TODO and inspect its checkable arithmetic comparison. Show the three extraction documents, schema, message interface and source-based verdict controls. Leave extraction message construction for rooms.

Use the [shared setup](../../README.md); model downloads and launch checks happen before the task. Start from the repository root with `uv run --locked --group prompting python start.py --block d2-1`. Keep the starter open. Prerequisite TODOs discussed in plenary belong to setup; the task below is the room assignment.

## Your group task

1. Predict missing-field behavior. Complete the extraction-message TODO and run the supplied zero-/few-shot comparison on all three documents. Inspect raw outputs and automatic schema flags.

2. Save the baseline. Change only the system policy to address one observed failure; rerun the same cases. Each partner checks a subset against original source words; compare the fully correct case count separately from schema validity.

3. Defend or reject the revision using one case-level comparison. Identify a remaining failure or limitation and propose a fresh test that could disprove your conclusion.

## Bring back

Baseline/revised policy, real raw outputs, source-backed judgments and a conditional decision in the findings export.

Use the notebook’s prediction/observation fields. Save the Python source and download findings to retain browser inputs and measurements. Both partners should be able to explain the conclusion; swap editor/checker around halfway. If you finish early, state a competing explanation and a new controlled test that would distinguish it.

## Work within the timebox

2 minutes to predict and agree; 7 to implement and compare; 4 to diagnose and defend; 2 to record/export. Ask for help through the trainer’s chat/room-visit route if blocked. Return to plenary for review and the scheduled quiz. Honest unchanged or failed results count as evidence when they are explained; do not invent measurements.
