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

    **Exercise + breakout · Block 1 · 30 minutes in pairs after guided setup.**
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
def _(mo):
    mo.md("""
    ## Tokenizer design desk

    **30 minutes in pairs · rooms 09:35–10:05.** Can a small change in training text change the rules used to encode new words?

    **From the preceding slides:** Frequent adjacent pieces become vocabulary entries. Encoding reuses learned rules. Every resulting token consumes context.

    1. Predict the first merge from at least two corpus contributions. Build the weighted-count and merge functions, using the supplied small input/output examples. Trace one merge by hand before trusting the three-round display.

    2. Keep the baseline, then change only `can` from 10 to 20. Predict before running. Inspect the changed merge order and the pieces of `maps` and unseen `rap`. Explain one choice using a count, and explain an unchanged probe if that is what you observe.

    3. Choose one additional `can` frequency using the existing control. Try to make a different merge win, rather than turning controls at random. Record the frequency and the winning count. Restore the baseline before comparing the supplied real English/German/code tokenizer examples.

    4. Use the prepared real-tokenizer counts and context budget to choose what to remove or shorten. Give a tradeoff. Explain why training this character-BPE toy does not measure a language model’s answer quality or latency.

    **Your route:** 0–4 min: inspect the corpus and predict. 4–14: implement and check the two steps. 14–24: compare frequency changes and unseen-word encoding, swapping editor/checker at minute 15. 24–30: inspect real token counts, decide on the budget and export evidence.

    **Bring back:** Initial prediction, baseline and changed-frequency traces, your extra frequency test, unseen-word explanation, and a context-budget recommendation with one limitation. Record each setting/result before changing a control. Download intermediate runs if you need to keep their tables; the final export contains the current run and baseline. Save code and download findings. Full task: `GROUP_TASK.md`.
    """)
    return


@app.cell(hide_code=True)
def _(BPE_CORPUS, mo):
    mo.vstack([
        mo.md("""
        ## 1. Understand the experiment and predict

        **The training text is already supplied.** A collection of training text
        is called a **corpus**. Below you can see every word in our tiny corpus,
        including repeated copies. You do not need to find or load another dataset.

        The table stores the same text more compactly: a row with `map` and 8
        means that `map` appears eight times. The last column shows the pieces
        we currently use to write that word. Each piece is a **token**. Initially,
        each letter is its own token. A **pair** is two tokens next to each other.

        In each training round, the supplied loop asks your functions to count
        pairs and merge the most frequent one throughout the corpus. It then
        recounts using the new token lists. We stop after **three merges**. Ties
        use alphabetical tuple order so a repeat run is deterministic.

        This is a **character-based teaching version of BPE**: words are already
        separated, merges never cross words, and there is no whitespace handling,
        byte fallback or special-token format. It trains a tokenizer, not an LLM.
        """),
        mo.md("**Our complete training text (repeated words included):**\n\n" +
              "\n\n".join("`" + " ".join([_word] * _freq) + "`"
                            for _word, _freq in BPE_CORPUS.items())),
        mo.ui.table([
            {"Word": _word, "How many copies?": _freq, "Current tokens (at the start)": list(_word)}
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
    ## 2. TODO 1 — Count which pieces appear next to each other

    BPE needs to know which neighbouring pieces occur most often. Your function
    supplies these counts. First, follow this small example, separate from the
    main training text above.

    **Imagine this is all our training text:**

    ```text
    cat cat car
    ```

    Look at each copy separately:

    | Word in the text | Its current pieces | Which pieces are next to each other? |
    |---|---|---|
    | First cat | `c`, `a`, `t` | `c` then `a`; `a` then `t` |
    | Second cat | `c`, `a`, `t` | `c` then `a`; `a` then `t` |
    | The car | `c`, `a`, `r` | `c` then `a`; `a` then `r` |

    In **each copy** of `cat`, `c` is followed by `a`, and `a` is followed by `t`.
    There are two copies, so each of these pairs occurs twice. The one copy of
    `car` adds another `c` followed by `a`, plus one `a` followed by `r`.

    | Neighbours | From the two copies of cat | From the one copy of car | Total |
    |---|---|---|---|
    | `c` then `a` | 2 | 1 | 3 |
    | `a` then `t` | 2 | 0 | 2 |
    | `a` then `r` | 0 | 1 | 1 |

    **How does your function receive that training text?** Python stores the
    same information in two dictionaries:

    ```python
    frequencies = {"cat": 2, "car": 1}  # How many copies of each word?
    splits = {                         # Each word's current pieces
        "cat": ["c", "a", "t"],
        "car": ["c", "a", "r"],
    }
    ```

    **For this small example, your function would return:**

    ```python
    {("c", "a"): 3, ("a", "t"): 2, ("a", "r"): 1}
    ```

    `("c", "a")` names a pair; `3` says how often it occurs across all word copies.
    This is what **weighted pair counting** means: a word that occurs twice
    contributes its pairs twice.

    **Now implement `count_pairs(splits, frequencies)` in the next cell.** Use the
    dictionaries passed into the function. The supplied code calls it with the
    main corpus and with separate small examples that check your work. Each call
    supplies all the words and frequencies you need for that call.

    Return a dictionary of neighbouring-token pairs and their total counts. Keep
    the input dictionaries and lists unchanged. Count inside each word; no pair
    crosses from the end of one word to the beginning of another.

    The supplied training loop uses your counts to choose a merge. A passed check
    unlocks your initial pair table. You only implement counting in this TODO.
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
    mo.accordion({"After the cat example: two special cases to handle": mo.md("""
        **A piece may contain several letters.** After a merge, `cat` might be
        represented as `["ca", "t"]`. There are two tokens, with one neighbouring
        pair: `("ca", "t")`. If it is `["cat"]`, there is just one token and no pair.
        An empty list also has no pair. Use the current list in `splits` each time.

        **Check every neighbouring position.** In `["s", "h", "h", "h"]` (`shhh`),
        the neighbours are `s–h`, `h–h`, `h–h`. The middle letters can belong to
        two candidate pairs while you count. Applying a merge happens in TODO 2.
        """)})
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

    **Small example:** given `["c", "a", "t"]` and the selected pair `("c", "a")`,
    return `["ca", "t"]`. The letters stay the same; two neighbouring pieces
    have become one piece.
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

        **Time guide:** 4 minutes predict, 10 build/check, 10 experiment, 6 explain/export.
        If blocked, use the folded concept checks or ask for a trainer room visit.
        An unchanged probe result is valid evidence; explain why rather than inventing
        a change. Use your chosen frequency test to challenge a prediction; stop exploring when six minutes remain so you can explain and export.
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
