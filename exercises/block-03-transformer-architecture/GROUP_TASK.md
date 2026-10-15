# Exercise: masking versus sampling

**Exercise + breakout · LLM Day 1 Block 3 · 15 minutes in pairs**

Learning goal: Separate control of context visibility from control of vocabulary-token selection.

## Before the room opens

Open the independent toy arrays. Complete the temperature-softmax prerequisite with trainer guidance and inspect the supplied comparison table; leave causal masking and top-k selection for rooms. Confirm positive temperatures and stable candidate order.

Use the [shared setup](../../README.md); model downloads and launch checks happen before the task. Start from the repository root with `uv run --locked python start.py --block 3`. Keep the starter open. Prerequisite TODOs discussed in plenary belong to setup; the task below is the room assignment.

## Your group task

1. Predict row B visibility. Complete the causal-mask TODO; verify future weights are zero, diagonal/past remain eligible and valid rows sum to one.

2. Complete top-k selection. Compare T=0.5 and T=2 at the same k=2, seed and draw count; then compare k=1 and k=2 at fixed T. Interpret probabilities separately from sampled frequencies.

3. Change only the draw count from 200 to 1000. Explain a remaining discrepancy between frequencies and probabilities and why masking cannot replace candidate filtering.

## Bring back

Masked heatmap, temperature/top-k comparison, k=1 check and a finite-sample explanation in the findings export.

Use the notebook’s prediction/observation fields. Save the Python source and download findings to retain browser inputs and measurements. Both partners should be able to explain the conclusion; swap editor/checker around halfway. If you finish early, state a competing explanation and a new controlled test that would distinguish it.

## Work within the timebox

2 minutes to predict and agree; 7 to implement and compare; 4 to diagnose and defend; 2 to record/export. Ask for help through the trainer’s chat/room-visit route if blocked. Return to plenary for review and the scheduled quiz. Honest unchanged or failed results count as evidence when they are explained; do not invent measurements.
