# Exercise: trace and perturb attention

**Exercise + breakout · LLM Day 1 Block 2 · 15 minutes in pairs**

Learning goal: Distinguish the matching function controlled by Q/K from the payload controlled by V.

## Before the room opens

Open the supplied Q/K/V arrays and explain receiver/source axes and feature dimensions. Complete the stable row-softmax prerequisite with trainer guidance before opening rooms; leave scaled scores and Value mixing for the group task.

Use the [shared setup](../../README.md); model downloads and launch checks happen before the task. Start from the repository root with `uv run --locked python start.py --block 2`. Keep the starter open. Prerequisite TODOs discussed in plenary belong to setup; the task below is the room assignment.

## Your group task

1. Predict the strongest source for Query A. Complete the score and Value-mixing TODOs; check shapes and approximately-one row sums. Trace one output coordinate numerically.

2. Keep a baseline. Add +1 to Q row A, feature 0; record which rows of scores, weights and outputs change. Reset delta to zero.

3. Add +1 to V row A, feature 0 with Q/K fixed. Compare with the Query intervention and explain the changed output using the relevant attention weight.

## Bring back

Baseline and two interventions, one worked output coordinate, invariant checks and a mechanism explanation in the findings export.

Use the notebook’s prediction/observation fields. Save the Python source and download findings to retain browser inputs and measurements. Both partners should be able to explain the conclusion; swap editor/checker around halfway. If you finish early, state a competing explanation and a new controlled test that would distinguish it.

## Work within the timebox

2 minutes to predict and agree; 7 to implement and compare; 4 to diagnose and defend; 2 to record/export. Ask for help through the trainer’s chat/room-visit route if blocked. Return to plenary for review and the scheduled quiz. Honest unchanged or failed results count as evidence when they are explained; do not invent measurements.
