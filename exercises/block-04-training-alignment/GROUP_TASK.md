# Exercise: test a learning update

**Exercise + breakout · LLM Day 1 Block 4 · 15 minutes in pairs**

Learning goal: Connect negative-log loss, gradient descent and a control experiment to evidence of learning.

## Before the room opens

Open the output-layer starter and identify fixed features versus trainable W/b. Inspect loss/update function signatures and the reset-to-baseline controls. No model loading is needed.

Use the [shared setup](../../README.md); model downloads and launch checks happen before the task. Start from the repository root with `uv run --locked python start.py --block 4`. Keep the starter open. Prerequisite TODOs discussed in plenary belong to setup; the task below is the room assignment.

## Your group task

1. Predict the ordering of loss for target probabilities 0.25 and 0.5. Complete both bounded TODOs and check one scalar parameter update by hand.

2. Run rate 0.5 for 40 updates. Record before/after target probability and loss. Repeat with rate 0 and the same update count, keeping everything else fixed.

3. Compare W/b changes across the two runs. Explain why lower training loss cannot establish factual accuracy, alignment or generalization; specify one additional evaluation you would need.

## Bring back

One checked loss/update calculation, measured baseline/zero-rate comparison and a stated evaluation limit.

Use the notebook’s prediction/observation fields. Save the Python source and download findings to retain browser inputs and measurements. Both partners should be able to explain the conclusion; swap editor/checker around halfway. If you finish early, state a competing explanation and a new controlled test that would distinguish it.

## Work within the timebox

2 minutes to predict and agree; 7 to implement and compare; 4 to diagnose and defend; 2 to record/export. Ask for help through the trainer’s chat/room-visit route if blocked. Return to plenary for review and the scheduled quiz. Honest unchanged or failed results count as evidence when they are explained; do not invent measurements.
