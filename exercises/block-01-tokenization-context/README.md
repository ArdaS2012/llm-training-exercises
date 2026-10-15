# Block 1 — Tokenization & Context

Record predictions in the combined exercise + breakout to compare English, German and code. Inspect
how text becomes token IDs, then calculate whether input and an answer reserve fit
within a teaching context limit.

**Prerequisites:** basic Python and the [shared environment setup](../../README.md).
Work with a partner; swap who edits and who predicts/checks midway through the exercise.
The group task is 15 minutes inside the agenda’s setup/practice/review allocation.

## Open this block

From the **repository root**, run:

```sh
uv run --locked python start.py
```

The launcher opens [01_tokenization_context.py](01_tokenization_context.py) in marimo.
Keep the terminal open. To launch the notebook directly from the root after the
setup check, you can also use:

```sh
uv run --locked marimo edit exercises/block-01-tokenization-context/01_tokenization_context.py
```

If your terminal is already in this block folder, return to the root with `cd ../..`.
The notebook's setup, examples and display cells are prepared. You only need to edit
the two marked `# TODO` areas first. A **waiting** message on opening is expected.

## Exercise + breakout

Follow the [15-minute group task](GROUP_TASK.md) after guided setup. It defines the required comparison, evidence and shared result. Keep the technical help below for the bounded TODOs.

## Optional extension — Count a formatted request

Open the optional request section and compare counting the current question alone
with counting instructions, history, documents and question together. Then inspect
the count with the supplied teaching role labels and separators included.

The labels are a **toy format**, not a real model's chat template. Separately encoded
components need not add exactly because boundaries affect tokenization. Use the
target model's actual template and accounting for real requests.

## What the experiment demonstrates

The selected tokenizer is **tiktoken / cl100k_base**, a concrete BPE example. The
vocabulary catalogue size differs from your sequence length and a context-window
limit. Token IDs identify entries; they are not embedding vectors or importance scores.
SentencePiece is a separate toolkit supporting BPE and Unigram; this exercise does
not train either a tokenizer or an LLM.

The context limits and cost rates are hypothetical teaching values. Reserving output
space does not mean actually generating or billing that amount. The following slide
debrief connects your counts to cost and performance. This notebook measures tokens,
not LLM latency or answer quality. Preserve useful evidence when shortening input.

## Help with this task

| What you see | What to try |
|---|---|
| Check says waiting | Replace both placeholders in that TODO and rerun it. |
| Red error after an edit | Undo the last change, check spelling and indentation, and keep the supplied return line. |
| A check fails | Read its feedback and open the folded hint. Explain each variable to your partner. |
| Weird `\x..` in a piece | One token may contain only part of a UTF-8 character. Inspect bytes and the full-sequence decode. |
| Too much code on screen | Collapse the prepared cells and keep the TODO code and results visible. |
| Notes disappeared after restart | Text-box values are session inputs. Download findings before closing. Saved notebook code remains on disk. |

For installation, connection or port problems, use the [general troubleshooting guide](../../README.md#troubleshooting).

## Course mapping and resources

Current handoff: LLM Day 1 slide 21, **Exercise: tokens and context budget**. The combined room task runs 10:00–10:15; setup/review are separate.

References: [tiktoken](https://github.com/openai/tiktoken),
[SentencePiece](https://github.com/google/sentencepiece),
[real chat templates](https://huggingface.co/docs/transformers/main/en/chat_templating).

[Back to all exercises](../README.md) · [Repository setup](../../README.md)

## Maintainer check

From the repository root, validate this notebook's structure with:

```sh
uv run --locked marimo check --strict exercises/block-01-tokenization-context/01_tokenization_context.py
```

Instructor solutions and completed-notebook checks are kept locally and excluded
from the student repository.

## Current teaching handoff

LLM Day 1, Block 1: actual slide **21 — Exercise: tokens and context budget** launches the combined exercise + breakout. Return to plenary at the agenda’s room end. The notebook and group task are self-contained; private trainer files are not required.
