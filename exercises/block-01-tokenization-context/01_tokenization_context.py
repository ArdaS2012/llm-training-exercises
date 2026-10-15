import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="BPE Detective · Block 1")


@app.cell(hide_code=True)
def _():
    import json
    import sys
    from pathlib import Path

    import marimo as mo

    sys.path.insert(0, str(next(
        _parent for _parent in Path(__file__).resolve().parents
        if (_parent / "llm_exercises" / "block1.py").is_file()
    )))
    from llm_exercises.block1 import (
        BPE_CORPUS, BPE_PROBES, ENCODING_NAME, EXAMPLES,
        apply_bpe, check_merge, check_pairs, load_tokenizer,
        token_rows, train_bpe,
    )
    tokenizer = load_tokenizer()
    return (
        BPE_CORPUS, BPE_PROBES, ENCODING_NAME, EXAMPLES, apply_bpe,
        check_merge, check_pairs, json, mo, token_rows, tokenizer,
        train_bpe,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # BPE Detective: build a tiny tokenizer

    **Exercise + breakout · Block 1 · 15 minutes in pairs after guided setup.**
    Learn how training text determines BPE merges, then use the learned rules on
    a word the tokenizer has never seen. Basic Python loops, lists and dictionaries
    are enough. Setup, training control and result displays are supplied.

    **Your route:** predict → implement two short functions → inspect three merges →
    change one training frequency → explain the evidence. Swap editor/checker halfway.

    Show the code of a TODO cell using its code control. Replace its `None` placeholder
    with your implementation inside `# TODO` / `# END TODO`; keep the function name
    and return line. Run with **Shift+Enter**. Later displays update automatically.
    A **waiting** message is normal until you implement that function. The two checks
    are independent, so you can work on either TODO first.
    """)
    return


@app.cell(hide_code=True)
def _(BPE_CORPUS, mo):
    mo.vstack([
        mo.md("""
        ## 1. Understand the experiment and predict

        A **corpus** is training text. Here we store each distinct word with how
        often it occurs: frequency 8 means eight copies, not eight letters.
        **Tokens** start as individual characters. A **pair** is two adjacent
        current tokens inside one word; it may contain longer pieces after a merge.

        In each training round, the supplied loop asks your functions to count
        pairs and merge the most frequent one throughout the corpus. It then
        recounts using the new token lists. We stop after **three merges**. Ties
        use alphabetical tuple order so a repeat run is deterministic.

        This is a **character-based teaching version of BPE**: words are already
        separated, merges never cross words, and there is no whitespace handling,
        byte fallback or special-token format. It trains a tokenizer, not an LLM.
        """),
        mo.ui.table([
            {"Word": _word, "Frequency": _freq, "Starting tokens": list(_word)}
            for _word, _freq in BPE_CORPUS.items()
        ], selection=None),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    prediction = mo.ui.text_area(
        label="Before coding: predict the first merge and justify it with counts from at least two words",
        placeholder="Candidate pair: ...\nEvidence from the corpus: ...\nPrediction for the unseen word rap: ...",
        full_width=True, debounce=False,
    )
    prediction
    return (prediction,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## 2. TODO 1 — Count the pairs that BPE can merge

    Implement `count_pairs(splits, frequencies)` in about **5–8 lines**.

    - **Inputs:** `splits` maps each word to its *current* list of tokens;
      `frequencies` maps the same words to occurrence counts. For example,
      `{"mint": ["mi", "n", "t"]}` describes three tokens, with `"mi"` already merged.
    - **Return:** a dictionary whose keys are two-token tuples and whose values are
      total occurrence counts across the corpus. Include only pairs that occur.
    - Count every adjacent position within each word, weighted by that word's
      frequency. Repeated neighbours contribute at each position, including overlaps
      during **counting**. Leave both input dictionaries and their lists unchanged.
      Empty lists and single tokens contribute no pairs.

    The trainer supplies pair selection and all three training rounds. Your job is
    to supply accurate statistics; you do not need sorting or a training loop here.
    A passed check unlocks your initial frequency table.
    """)
    return


@app.function
def count_pairs(splits, frequencies):
    # TODO 1: build the dictionary described above (about 5–8 lines).
    counts = None
    # END TODO 1
    return counts


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"Optional concept check for TODO 1": mo.md(
        "Does your result describe neighbours in the current token list, or letters "
        "inside a token that was already merged? How many copies of each word does "
        "one dictionary entry represent?"
    )})
    return


@app.cell(hide_code=True)
def _(check_pairs, mo):
    pairs_ok, pairs_message = check_pairs(count_pairs)
    mo.callout(pairs_message, kind="success" if pairs_ok else "info")
    return (pairs_ok,)


@app.cell(hide_code=True)
def _(BPE_CORPUS, mo, pairs_ok):
    _rows = []
    if pairs_ok:
        _counts = count_pairs({word: list(word) for word in BPE_CORPUS}, BPE_CORPUS)
        _rows = [{"Pair": list(pair), "Weighted occurrences": count}
                 for pair, count in sorted(_counts.items(), key=lambda item: (-item[1], item[0]))]
    mo.vstack([
        mo.md("### Initial pair frequencies — compare with your prediction"),
        mo.ui.table(_rows, selection=None) if pairs_ok else mo.md("Waiting for TODO 1. TODO 2 can be completed independently."),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## 3. TODO 2 — Apply one selected merge

    Implement `merge_pair(tokens, pair)` in about **8–12 lines**.

    - **Inputs:** one word's current token list and a tuple identifying the two
      tokens selected by the trainer. Tokens are strings, including longer pieces.
    - **Return:** a **new list** after one left-to-right pass. Replace each occurrence
      of that adjacent pair with the two strings joined together; keep other tokens
      in their original order. Leave the input list unchanged.
    - One original token can take part in at most one merge during this pass.
      For example, merging `("x", "x")` in `["x", "x", "x"]` must produce a
      two-token result and preserve all three characters when joined back together.
      Counting overlapping candidates and applying non-overlapping merges are different.
      Empty, one-token and no-match inputs still return a new list.

    This function applies **one given rule**; it does not select a pair or train
    new rules. The supplied loop handles that. Use whole token strings, not a
    replacement on the reconstructed word: token boundaries matter.
    """)
    return


@app.function
def merge_pair(tokens, pair):
    # TODO 2: create a new token list for one merge pass (about 8–12 lines).
    merged = None
    # END TODO 2
    return merged


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"Optional concept check for TODO 2": mo.md(
        "After consuming a matching pair, which original tokens are still available? "
        "After a non-match, which token must be preserved? Check what happens at the last position."
    )})
    return


@app.cell(hide_code=True)
def _(check_merge, mo):
    merge_ok, merge_message = check_merge(merge_pair)
    mo.callout(merge_message, kind="success" if merge_ok else "info")
    return (merge_ok,)


@app.cell(hide_code=True)
def _(BPE_CORPUS, merge_ok, mo, pairs_ok, train_bpe):
    baseline = None
    if pairs_ok and merge_ok:
        baseline = train_bpe(BPE_CORPUS, count_pairs, merge_pair)
    mo.vstack([
        mo.md("### Your three-round training trace\nExplain why the winning pair can change after a merge. Open each row to inspect all counts and splits."),
        mo.ui.table(baseline["trace"], selection=None) if baseline else mo.md("Waiting for both TODOs. Each has its own feedback above."),
    ])
    return (baseline,)


@app.cell(hide_code=True)
def _(mo):
    changed_frequency = mo.ui.number(
        start=1, stop=30, step=1, value=10,
        label="Frequency of can (baseline 10; change to 20 after predicting)",
    )
    experiment_notes = mo.ui.text_area(
        label="Before changing: predict the effect. After changing: record a changed merge and its evidence",
        full_width=True, debounce=False,
    )
    mo.vstack([
        mo.md("""
        ## 4. Controlled experiment: change the training data

        Keep the baseline above. Predict what changes if **only `can` occurs 20 times**
        instead of 10, then change the control below. Both runs use the same alphabet,
        two functions and three-merge budget. Inspect the merge order and final splits
        of **`maps`**. Identify one count that explains a changed choice.

        Now predict the split of **`rap`**, a word absent from both training corpora,
        under each set of learned rules. Does a new word need a whole-word entry?
        Record your prediction before opening the encoding results below.
        """), changed_frequency, experiment_notes,
    ])
    return changed_frequency, experiment_notes


@app.cell(hide_code=True)
def _(BPE_CORPUS, BPE_PROBES, apply_bpe, baseline, changed_frequency, mo, train_bpe):
    variant = None
    probe_rows = []
    if baseline:
        _frequencies = {**BPE_CORPUS, "can": changed_frequency.value}
        variant = train_bpe(_frequencies, count_pairs, merge_pair)
        _alphabet = set("".join(BPE_CORPUS))
        for _word in BPE_PROBES:
            _before = apply_bpe(_word, baseline["merges"], merge_pair, _alphabet)
            _after = apply_bpe(_word, variant["merges"], merge_pair, _alphabet)
            probe_rows.append({"Word": _word, "Baseline pieces": _before,
                               "Changed-corpus pieces": _after,
                               "Baseline count": len(_before), "Changed-corpus count": len(_after),
                               "Text restored in both": "".join(_before) == "".join(_after) == _word})
    mo.vstack([
        mo.md("### Changed-corpus training trace"),
        mo.ui.table(variant["trace"], selection=None) if variant else mo.md("Waiting for both TODOs."),
        mo.accordion({"Reveal encoding results after recording your prediction": mo.vstack([
            mo.md("Encoding replays learned rules in order. It does not recount pairs or update the vocabulary for this word."),
            mo.ui.table(probe_rows, selection=None) if probe_rows else mo.md("Waiting for both TODOs."),
        ])}),
        mo.md("Compare splits on the **same probe words**. The corpora contain different numbers of words, so their raw training-token totals alone are not a fair compression comparison."),
    ])
    return probe_rows, variant


@app.cell(hide_code=True)
def _(ENCODING_NAME, EXAMPLES, mo, token_rows, tokenizer):
    real_rows = []
    for _label, _text in EXAMPLES.items():
        _ids = tokenizer.encode_ordinary(_text)
        real_rows.append({"Text": _label, "Original": _text, "Tokens": len(_ids),
                          "IDs": _ids, "Full decode matches": tokenizer.decode(_ids) == _text})
    mo.accordion({"Prepared transfer check: a real tokenizer and a context decision": mo.vstack([
        mo.md(f"""
        ### 5. Connect the toy to a real tokenizer

        No additional coding is required. This table uses **tiktoken / `{ENCODING_NAME}`**,
        a fixed byte-level BPE encoding with **{tokenizer.n_vocab:,}** vocabulary slots
        including special-token slots. It is independent of your toy training runs.
        Its IDs identify vocabulary entries; they are not embedding vectors.
        Compare English, German and code: tokens need not be whole words. One token
        may contain an incomplete UTF-8 character; the complete sequence restores text.
        SentencePiece is a separate toolkit supporting BPE and Unigram.
        """),
        mo.ui.table(real_rows, selection=None),
        mo.md("German example: token bytes and visible pieces. `repr` exposes spaces; `\\x..` exposes partial UTF-8 bytes."),
        mo.ui.table(token_rows(tokenizer, tokenizer.encode_ordinary(EXAMPLES["German"])), selection=None),
        mo.md("""
        **Prepared context calculation:** input 3,000 + answer reserve 2,000 against
        a teaching limit of 4,000 leaves **−1,000** tokens. Choose one quantity to
        change and explain the tradeoff. Input includes instructions, history,
        documents and formatting. An exact fit is allowed. These limits are hypothetical.

        Why might a tokenizer that produces fewer tokens help with a context budget?
        Does fitting guarantee a useful answer? Keep useful evidence when shortening.
        A reserved answer is not an actually generated or billed answer. Cost depends
        on the service's input/output usage rates; this notebook measures neither LLM
        latency nor answer quality.
        """),
    ])})
    return (real_rows,)


@app.cell(hide_code=True)
def _(mo):
    conclusion = mo.ui.text_area(
        label="Shared conclusion: training vs encoding; one supported finding, one limitation, and your context decision",
        full_width=True, debounce=False,
    )
    mo.vstack([
        mo.md("""
        ## 6. Bring back evidence you can both explain

        - Your first-pair prediction and the three-round baseline trace.
        - The controlled comparison at `can = 20`, with one changed merge explained
          by its frequency and the pieces for the same probe words.
        - Why applying learned rules to `rap` is different from training on `rap`.
          State a limitation of this toy and a justified context-budget decision
          from the prepared transfer check.

        **Time guide:** 2 minutes predict, 7 implement, 4 compare/explain, 2 record/export.
        If blocked, use the folded concept checks or ask for a trainer room visit.
        An unchanged probe result is valid evidence; explain why rather than inventing
        a change. Optional extension: predict one further merge before running it.
        """), conclusion,
    ])
    return (conclusion,)


@app.cell(hide_code=True)
def _(
    ENCODING_NAME, baseline, changed_frequency, conclusion, experiment_notes,
    json, merge_ok, mo, pairs_ok, prediction, probe_rows, real_rows, variant,
):
    _report = {
        "exercise": "BPE Detective", "prediction": prediction.value,
        "baseline": baseline, "changed_can_frequency": changed_frequency.value,
        "variant": variant, "probe_comparison": probe_rows,
        "experiment_notes": experiment_notes.value, "conclusion": conclusion.value,
        "real_tokenizer": ENCODING_NAME, "real_measurements": real_rows,
        "checks_passed": {"pairs": pairs_ok, "merge": merge_ok},
    }
    mo.vstack([
        mo.md("### Save code and findings\nSave code with **Ctrl+S** (Windows/Linux) or **Cmd+S** (macOS). Browser fields are session inputs: download findings before closing. The JSON includes both traces, your frequency setting, measurements and written explanations. It stays on your computer."),
        mo.download(data=json.dumps(_report, ensure_ascii=False, indent=2).encode("utf-8"), filename="results-block1.json", label="Download my findings"),
        mo.md("The task sheet is `GROUP_TASK.md` in this block folder. Learn more after the exercise: [BPE background](https://huggingface.co/learn/llm-course/en/chapter6/5), [tiktoken](https://github.com/openai/tiktoken), [SentencePiece](https://github.com/google/sentencepiece)."),
    ])
    return


if __name__ == "__main__":
    app.run()
