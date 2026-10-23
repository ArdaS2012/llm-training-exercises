# Day 2 Block 4 — A small evaluation setup


## Exercise + breakout

Follow the [30-minute investigation](GROUP_TASK.md) immediately after the concept explanation.

Compare exact match, output-schema validity and Recall@k. Keep a paired test set, inspect a real model judge against source evidence, and export a justified configuration choice. One TODO is about 3–5 lines; a 30-minute investigation immediately after the concepts. Day 2 launch slide 64.

Use [shared setup](../../README.md). From the repository root:

```sh
uv sync --locked
uv run --locked python start.py --block d2-4 --check
uv run --locked python start.py --block d2-4
```

These commands need no model download for automatic scoring. For the actual CPU judge, reuse the optional prompting group and cache:

```sh
uv sync --locked --group prompting
uv run --locked --group prompting python start.py --block d2-1 --check
uv run --locked --group prompting python start.py --block d2-4
```

The judge uses the pinned model from Day 2 prompting, no API key. Its rating may be wrong or invalid JSON. Base d2-4 preflight does not verify model availability. After model preflight, use `uv run --offline --locked --group prompting python start.py --block d2-1 --offline-models --check` to check the cache on this computer. Then launch d2-4 with the same cached environment. Windows/macOS/Linux use the existing wrappers and selector; actual remote CI results are not claimed.

1. Predict a tradeoff before inspecting scores. Fixtures contain two dev and four test questions with authored paired outputs; they are not measured model results.
2. Implement only the marked scoring region: normalize answer/reference, calculate set-based recall for first k IDs, return the documented dictionary. No relevant IDs means undefined recall (`None`). Duplicate IDs count once. Use Shift+Enter and save code with Ctrl+S/Cmd+S.
3. Compare the authored test fixtures, keeping N and recall-eligible M visible. Changing k only rescores saved rankings; it does not regenerate answers.
4. Choose **Own Mini-RAG export**, enter the local Block 2 JSON path and ground truth JSON. Inspect original documents and the full chunks list. For each question use `split` (`dev` or `test`), a string `reference`, and `relevant_ids` mapping each variant to exact chunk-ID lists. Different chunk sizes need different relevance labels. Label at least one comparison case as test. Choose **Reserved before both runs** only if those questions were reserved before Block 2 generation, both configurations were frozen and no tuning used their answers. Otherwise keep **retrospective diagnostics**; a test label alone is not held-out evidence. Plan fresh questions for the next test. Q3 is absent only if ALL documents lack the answer; reference UNKNOWN, relevant IDs empty. Never use generated answers as references. Failed calls remain in the denominator.
5. Independently rate a case 0/1/2 from source evidence, then run the judge. Inspect its raw response. Record a source-backed disagreement, or honestly record agreement and inspect another case/schema failure. Invalid judge JSON is a failure, not agreement.
6. Download `evaluation-day2-block4.json` to preserve widget values, scores, imported records, judge evidence and choice. Saving Python alone preserves code. Keep document-containing reports local; check before sharing.

The report needs per-case scores, aggregate task/retrieval scores, one judge/human comparison with source evidence, an explicit evaluation-design label, a justified choice, sample limits and a next held-out test. Strict exact match can reject paraphrases; schema validity does not check factual support. Free-text RAG outputs usually fail the fixture’s JSON contract; discuss whether your application needs that contract.

Troubleshooting: complete the TODO before scoring; list/set intersection counts evidence, not repeated occurrences. Use original per-variant IDs for import. JSON labels must contain every question number. Missing exports permit a fixture fallback but leave your own-record transfer pending. Model errors leave explicit failures; do not substitute a made-up rating. Restart with the same selector after saving. [MMLU](https://arxiv.org/abs/2009.03300) and [LLM-as-judge](https://arxiv.org/abs/2306.05685) explain benchmark/judge scope.

## Current teaching handoff

LLM Day 2, Block 4: actual slide **64 — Exercise: audit an evaluation decision** launches the combined exercise + breakout. Return to plenary at the agenda’s room end. The notebook and group task are self-contained; private trainer files are not required.

## Why this is hands-on

Act as the release reviewers for your own Mini-RAG: use measured evidence to decide which version, if either, deserves another test. Both partners change or inspect actual runnable behavior, challenge a prediction with source evidence, and make a decision. The [investigation](GROUP_TASK.md) keeps the slide takeaways beside the task and gives a topic-specific 30-minute route; extra time is for understanding and diagnosis, not more boilerplate code.
