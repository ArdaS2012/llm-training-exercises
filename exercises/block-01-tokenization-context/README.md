# Block 1 — Tokenization & Context

Use the predictions from Token Detective to compare English, German and code. Inspect
how text becomes token IDs, then calculate whether input and an answer reserve fit
within a teaching context limit.

**Prerequisites:** basic Python and the [shared environment setup](../../README.md).
Work with a partner; swap who edits and who predicts/checks midway through the exercise.
The planned pair-practice slot is 30 minutes.

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

## Your tasks

### 1. Record your hypothesis

Copy your breakout ranking and write one reason for each text before measuring:

```text
The model predicts the next token.
Das Modell sagt das nächste Token voraus.
next_token = model.predict(context)
```

These strings differ in length, and the code is a related example rather than a
translation. Your experiment should test a prediction about these examples, not
establish a universal ranking of languages.

### 2. Complete TODO 1 — Encode and count

Show the code for `inspect_text`. Replace its two `None` values to produce the token
ID sequence and its count. Keep the supplied function name and return line, then
run the cell with **Shift+Enter**.

The automatic check, comparison table and token inspector update. Inspect all three
texts, including the displayed pieces, raw bytes and full-sequence decoding. Count
sequence positions; repeated IDs still occupy positions. The whitespace-based count
is a simple comparison convention and is particularly limited for code.

### 3. Make one controlled edit

Predict what will change, then alter one word, leading space, newline, punctuation
mark or emoji in a text box. Record the original count, edited count and your
explanation. Check whether the full decoded sequence restores the edited text.

### 4. Complete TODO 2 — Calculate the context budget

Show the code for `context_budget` and replace its two `None` values. Calculate the
space remaining after accounting for input and reserved output, and whether the
request fits. An exact fit is allowed; retain a negative remainder to show overflow.

Test the supplied 3,000-token input, 2,000-token answer reserve and 4,000-token
limit. Revise one quantity to make the request fit and explain the tradeoff.
Also test an exact fit using the supplied 6,000 / 2,000 / 8,000 example.

### 5. Save and share your findings

- Compare your measurements with the original hypothesis.
- Explain one surprising split and one consequence for prompt design.
- Record your budget revision and its tradeoff.
- Save notebook code with **Ctrl+S** (Windows/Linux) or **Cmd+S** (macOS).
- Choose **Download my findings** before closing. Text-box observations are session
  values; they are preserved in the downloaded JSON, not the saved Python code.

Keep the JSON alongside your notebook. It contains your hypothesis, edited texts,
comparison, token IDs, budget, observations and TODO check status.

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

This practice follows continuous Day 1 slides **20–21** (Block 1 local slides **10–11**).
Budgeting builds on slides **18–19**; cost, performance and findings are discussed on
slides **22–24**. See the [presenter guide and speaking cues](https://github.com/ArdaS2012/EDV_Training/blob/main/docs/LLM_Training/llm_day1/01_tokenization_context.md#slide-11).

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
