# Exercise: tokens and context budget

**Exercise + breakout · LLM Day 1 Block 1 · 15 minutes in pairs**

Learning goal: Use token measurements and boundary tests to defend a context-budget decision.

## Before the room opens

Open the starter and inspect its two TODO interfaces, encoding identity and full-sequence decode. Keep the supplied English, German and code strings. Demonstrate where to record predictions without giving their ranking.

Use the [shared setup](../../README.md); model downloads and launch checks happen before the task. Start from the repository root with `uv run --locked python start.py --block 1`. Keep the starter open. Prerequisite TODOs discussed in plenary belong to setup; the task below is the room assignment.

## Your group task

1. Before measuring, rank the three supplied texts and justify one boundary prediction. Complete the encoding/count TODO and compare IDs, pieces and counts.

2. Choose one text and change only a leading space, punctuation mark or word. Preserve the baseline; explain the changed pieces/count, including a result with unchanged count if that occurs.

3. Complete the context-budget TODO. Test input 3000, reserve 2000, limit 4000; revise exactly one quantity to fit. Test 6000+2000 with limit 8000 and justify your boundary decision.

## Bring back

Three-text measurement table, one controlled-edit comparison, overflow and exact-fit checks, and a justified budget revision in the findings export.

Use the notebook’s prediction/observation fields. Save the Python source and download findings to retain browser inputs and measurements. Both partners should be able to explain the conclusion; swap editor/checker around halfway. If you finish early, state a competing explanation and a new controlled test that would distinguish it.

## Work within the timebox

2 minutes to predict and agree; 7 to implement and compare; 4 to diagnose and defend; 2 to record/export. Ask for help through the trainer’s chat/room-visit route if blocked. Return to plenary for review and the scheduled quiz. Honest unchanged or failed results count as evidence when they are explained; do not invent measurements.
