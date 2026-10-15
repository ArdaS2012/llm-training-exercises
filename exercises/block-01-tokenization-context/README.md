# Block 1 — BPE Detective: build a tiny tokenizer

Learn the mechanism behind tokenization: count neighbouring token pairs, merge a selected pair, and inspect three rounds of BPE training. Change one training frequency and compare the learned rules on the same words, including a word absent from training.

**Prerequisites:** basic Python loops, lists, dictionaries and tuples; the [shared setup](../../README.md). No API key, GPU or LLM is required. First setup caches the small tiktoken asset for the prepared comparison section.

## Open the exercise

From the **repository root**, run:

```sh
uv run --locked python start.py --block 1
```

The default launcher without `--block` also opens Block 1. Keep the terminal open. The editable starter is [01_tokenization_context.py](01_tokenization_context.py).

## What you do

Follow the [15-minute pair task](GROUP_TASK.md). Guided setup happens before rooms open. Alternate editor/checker roles.

The notebook contains two marked functions:

| Task | Supplied input | Your output | Purpose |
|---|---|---|---|
| TODO 1: `count_pairs` | Word → current tokens; word → frequency | Dictionary: two-token tuple → weighted occurrence count | Decide which neighbouring pieces are frequent in the training corpus |
| TODO 2: `merge_pair` | One token list and the selected pair | New list after one non-overlapping merge pass | Construct the next tokenization without losing text or changing the original |

Each task explains its boundary rules in the notebook. Implement about 5–8 and 8–12 lines respectively inside the marked regions; keep the function names and return lines. Show the cell's code, edit, then run with **Shift+Enter**. Later displays update automatically. A waiting message is expected in the untouched starter. Each TODO has independent feedback and a folded conceptual prompt; neither needs the other to pass.

The supplied code selects pairs, resolves ties alphabetically, runs three rounds, displays traces and applies learned rules to probe words. Your implementation does the counting and merging. Record a prediction before revealing outputs. Change only `can`'s frequency from 10 to 20, preserve the baseline and explain a changed choice using counts. Compare the same probe words across both runs; raw corpus totals are not directly comparable when the corpus size changes.

## Transfer and limitations

Open the prepared real-tokenizer/context section after the BPE experiment. It includes English/German/code measurements with **tiktoken / cl100k_base** and a context decision. There is no arithmetic TODO: use the prepared result to choose a tradeoff.

The toy starts with characters, separates words in advance and omits whitespace processing, byte fallback and special tokens. New probe words must use the training alphabet. It trains a tokenizer, not an LLM. The fixed real encoding is separate from your learned toy rules. Vocabulary size, sequence length and context capacity are different quantities. SentencePiece is a toolkit supporting BPE and Unigram; this exercise does not implement Unigram.

Context values are hypothetical. Reserving output does not mean generating or billing that amount; fitting does not guarantee answer quality. The notebook measures neither LLM speed nor quality.

## Save and share

Save code with **Ctrl+S** / **Cmd+S**, and **download findings before closing**. Browser fields are session inputs. The JSON records predictions, both traces, the current frequency setting, probe pieces/counts, explanations, real-tokenizer measurements and check status. Share one explanation both partners can defend.

## Help

| What you see | What to try |
|---|---|
| Waiting | Replace that function's `None` with your implementation and rerun. |
| Pair-count check fails | Re-read the rules for word frequency, current token boundaries and repeated neighbours. |
| Merge check fails | Re-read the rules for non-overlap, the final position and preserving input. |
| Red cell error | Check indentation and the return line; undo the last edit if needed. |
| Same probe result in both runs | This is valid. Compare which learned rules that word actually uses. |
| Weird `\x..` in a real token | A byte fragment need not form a UTF-8 character by itself. Inspect full-sequence decoding. |

For connection, port or installation problems use [shared troubleshooting](../../README.md#troubleshooting).

## Course mapping and sources

LLM Day 1 slide **21 — Exercise: learn and test BPE merges** launches the 10:00–10:15 room task; slide 24 debriefs the evidence. Setup and plenary review are separate.

Background for after the exercise: [Hugging Face BPE lesson](https://huggingface.co/learn/llm-course/en/chapter6/5), [tiktoken](https://github.com/openai/tiktoken), [SentencePiece](https://github.com/google/sentencepiece).

[All exercises](../README.md) · [Repository setup](../../README.md)

## Maintainer check

```sh
uv run --locked marimo check --strict exercises/block-01-tokenization-context/01_tokenization_context.py
```

Instructor implementations, reference traces and completed-notebook checks stay local in the ignored `instructor/` folder.
