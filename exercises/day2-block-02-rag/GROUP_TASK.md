# Exercise: diagnose your Mini-RAG

**Exercise + breakout · LLM Day 2 Block 2 · 15 minutes in pairs**

Learning goal: Build a small own-document RAG and locate the stage responsible for a result.

## Before the room opens

Preload models, ingest 2–4 permitted short English documents and formulate two supported questions plus one absent-answer question. Reserve fresh evaluation questions before running either configuration. In plenary complete the context-labeling prerequisite and locate original source text; leave evidence selection for rooms.

Use the [shared setup](../../README.md); model downloads and launch checks happen before the task. Start from the repository root with `uv run --locked --group rag python start.py --block d2-2`. Keep the starter open. Prerequisite TODOs discussed in plenary belong to setup; the task below is the room assignment.

## Your group task

1. Predict source IDs and a chunk-size effect. Complete the reranked evidence-selection TODO; run the supplied baseline plus changed-chunk comparison for all three questions. Keep models, questions, overlap (20 words), candidate limit (5) and selected-passage limit (2) fixed.

2. For one supported question, compare top retrieved/reranked passages and actual generated answers. Quote original words and identify whether a failure starts in retrieval or generation.

3. Check the absent-answer question against all documents. Record abstention, invention or uncertainty honestly. Recommend one next fix from evidence and export the records for evaluation.

## Bring back

Three paired question/answer/source records, original-source checks, one diagnosed failure/limitation and a justified next fix.

The passage limit is fixed, but the amount of text is not: two 80-word chunks can supply up to 160 word occurrences; two 40-word chunks up to 80. Fewer candidates or passages are returned when fewer chunks are available. Keeping overlap at 20 words also changes its share of a chunk. Interpret the whole chunk-setting change; this comparison does not isolate boundary placement from context length or repeated evidence.

Use the notebook’s prediction/observation fields. Save the Python source and download findings to retain browser inputs and measurements. Both partners should be able to explain the conclusion; swap editor/checker around halfway. If you finish early, state a competing explanation and a new controlled test that would distinguish it.

## Work within the timebox

2 minutes to predict and agree; 7 to implement and compare; 4 to diagnose and defend; 2 to record/export. Ask for help through the trainer’s chat/room-visit route if blocked. Return to plenary for review and the scheduled quiz. Honest unchanged or failed results count as evidence when they are explained; do not invent measurements.
