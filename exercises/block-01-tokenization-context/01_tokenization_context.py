import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="Token Detective · Block 1")


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
        ENCODING_NAME, EXAMPLES, check_budget, check_inspect,
        load_tokenizer, token_rows, toy_request,
    )

    tokenizer = load_tokenizer()
    return (
        ENCODING_NAME,
        EXAMPLES,
        check_budget,
        check_inspect,
        json,
        mo,
        token_rows,
        tokenizer,
        toy_request,
    )


@app.cell(hide_code=True)
def _(ENCODING_NAME, mo, tokenizer):
    mo.md(f"""
    # Token Detective
    **Block 1 · Tokenization & Context**

    You already predicted how English, German and code might split into tokens.
    Now test your prediction, inspect the actual pieces, and leave room for an answer.

    **Your route:** record a prediction → complete TODO 1 → change one thing →
    complete TODO 2 → save your findings. Work with a partner and swap who edits.

    Everything around the **two `# TODO` areas** is prepared. No account, API key,
    GPU or model download is needed. Your text stays in this local notebook.

    **Using marimo:** scroll to a TODO, show its code using the cell's code control,
    replace the two `None` placeholders, then run that cell with **Shift+Enter**.
    Dependent results update automatically. Edit only those placeholders first;
    keep the supplied function names and `return` lines. You can undo an edit.
    A waiting message is expected before you complete the TODOs.

    **Tokenizer:** `{ENCODING_NAME}` from tiktoken. Vocabulary entries (including
    special-token slots): **{tokenizer.n_vocab:,}**. This is a catalogue size,
    not the number of tokens in your text and not a context-window limit.
    We encode ordinary text: literal special-token-looking strings stay text.
    This BPE encoding is a specific example; SentencePiece is a different toolkit
    supporting BPE and Unigram. We do not train a tokenizer or an LLM here.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    prediction = mo.ui.text_area(
        label="Before measuring: your ranking and one reason per text",
        debounce=False,
        placeholder="Fewest → most: ...\nEnglish: ...\nGerman: ...\nCode: ...",
        full_width=True,
    )
    mo.vstack([mo.md("## 1. Keep your Token Detective hypothesis"), prediction])
    return (prediction,)


@app.cell(hide_code=True)
def _(EXAMPLES, mo):
    english = mo.ui.text_area(value=EXAMPLES["English"], label="English", full_width=True)
    german = mo.ui.text_area(value=EXAMPLES["German"], label="German", full_width=True)
    code = mo.ui.text_area(value=EXAMPLES["Code"], label="Code (a related example, not a translation)", full_width=True)
    mo.vstack([english, german, code])
    return code, english, german


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## 2. TODO 1 — Encode and count

    Complete the next cell's **two lines** inside `inspect_text`.
    `tokenizer.encode_ordinary(text)` produces a list of vocabulary IDs.
    `len(a_list)` counts the positions in a list.

    Do not strip spaces, split into words, or count unique IDs. A repeated ID
    still uses another sequence position. Return both the IDs and their count.
    Once the check passes, the comparison table and token inspector become available.
    """)
    return


@app.function
def inspect_text(text, tokenizer):
    # TODO 1: replace only these two None values (about two lines).
    token_ids = None
    token_count = None
    # END TODO 1
    return token_ids, token_count


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"Hint for TODO 1": mo.md("First produce the sequence of IDs. Then count its positions. Which supplied method produces a list, and which Python operation counts a list's entries?")})
    return


@app.cell(hide_code=True)
def _(check_inspect, mo, tokenizer):
    inspect_ok, inspect_message = check_inspect(inspect_text, tokenizer)
    mo.callout(inspect_message, kind="success" if inspect_ok else "info")
    return (inspect_ok,)


@app.cell(hide_code=True)
def _(code, english, german, inspect_ok, mo, tokenizer):
    texts = {"English": english.value, "German": german.value, "Code": code.value}
    comparison = []
    if inspect_ok:
        for _label, _text in texts.items():
            _ids, _count = inspect_text(_text, tokenizer)
            comparison.append({
                "Text": _label,
                "Original": _text,
                "Whitespace-separated items": len(_text.split()),
                "Tokens": _count,
                "Unique IDs (not token count)": len(set(_ids)),
                "Full decode matches": tokenizer.decode(_ids) == _text,
            })
    mo.vstack([
        mo.md("### Your comparison\nWhitespace splitting is only a simple word-count convention; it is especially limited for code."),
        mo.ui.table(comparison, selection=None) if inspect_ok else mo.md("Complete TODO 1 to see your measurements."),
    ])
    return comparison, texts


@app.cell(hide_code=True)
def _(mo):
    selected_text = mo.ui.dropdown(options=["English", "German", "Code"], value="German", label="Inspect which text?")
    selected_text
    return (selected_text,)


@app.cell(hide_code=True)
def _(inspect_ok, mo, selected_text, texts, token_rows, tokenizer):
    _items = [mo.md("### Token IDs and pieces")]
    if inspect_ok:
        _text = texts[selected_text.value]
        _ids, _count = inspect_text(_text, tokenizer)
        _items.extend([
            mo.md(f"**Token IDs:** `{_ids}`\n\n**Full-sequence decode (repr):** `{tokenizer.decode(_ids)!r}`"),
            mo.ui.table(token_rows(tokenizer, _ids), selection=None),
        ])
    _items.append(mo.md("""
    `repr` makes spaces and newlines visible. `\\x..` means that an individual
    piece contains bytes that do not form a complete UTF-8 character on their own.
    **Decode the whole sequence** before judging whether text was restored correctly.
    IDs identify vocabulary entries; they are not embedding vectors or importance scores.
    """))
    mo.vstack(_items)
    return


@app.cell(hide_code=True)
def _(mo):
    observation = mo.ui.text_area(label="Your controlled edit: prediction, change, observed count and explanation", full_width=True, debounce=False)
    mo.vstack([
        mo.md("""
        ## 3. Change one thing
        Predict first. In one text box above, change **one** word, leading space,
        newline, punctuation mark or emoji. Watch the table and inspector update.
        Try `hello` versus ` hello`, or add `🙂`. Record the before/after counts.
        Changing the text is an experiment; it does not retrain the tokenizer.
        These three examples alone cannot establish a universal ranking of languages.
        """),
        observation,
    ])
    return (observation,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## 4. TODO 2 — Leave room for the answer

    A request fits this teaching window when **input + reserved output ≤ limit**.
    Complete the next cell's two lines:

    - `remaining`: limit minus input minus reserved output. Keep negative values:
      they tell you how many tokens overflow.
    - `fits`: a Boolean (`True` or `False`). An exact fit is allowed.

    The supplied 3,000 input tokens already include instructions, history, documents
    and formatting. The limits here are **hypothetical teaching values**, not a
    claim about a model using cl100k_base. Real services can impose additional
    input or output limits.
    """)
    return


@app.function
def context_budget(input_tokens, reserved_output, context_limit):
    # TODO 2: replace only these two None values (about two lines).
    remaining = None
    fits = None
    # END TODO 2
    return remaining, fits


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"Hint for TODO 2": mo.md("Start with the available capacity. Which two quantities use that capacity? Think separately about spare space, overflow, and an exact fit.")})
    return


@app.cell(hide_code=True)
def _(check_budget, mo):
    budget_ok, budget_message = check_budget(context_budget)
    mo.callout(budget_message, kind="success" if budget_ok else "info")
    return (budget_ok,)


@app.cell(hide_code=True)
def _(mo):
    input_count = mo.ui.number(start=0, stop=100000, step=1, value=3000, label="Input tokens (including all overhead)")
    output_reserve = mo.ui.number(start=0, stop=100000, step=1, value=2000, label="Reserved output tokens")
    context_limit = mo.ui.number(start=1, stop=100000, step=1, value=4000, label="Teaching context limit")
    mo.vstack([input_count, output_reserve, context_limit])
    return context_limit, input_count, output_reserve


@app.cell(hide_code=True)
def _(budget_ok, context_limit, input_count, mo, output_reserve):
    budget_result = None
    if budget_ok:
        _remaining, _fits = context_budget(input_count.value, output_reserve.value, context_limit.value)
        budget_result = {"remaining": _remaining, "fits": _fits}
        _message = f"Fits. {_remaining:,} tokens remain after reserving the answer." if _fits else f"Does not fit: {-_remaining:,} tokens overflow."
        mo.output.replace(mo.callout(_message, kind="success" if _fits else "warn"))
    else:
        mo.output.replace(mo.md("Complete TODO 2 to test your budget."))
    return (budget_result,)


@app.cell(hide_code=True)
def _(mo):
    budget_reason = mo.ui.text_area(label="Make the slide example fit: what did you change, and what is the tradeoff?", full_width=True, debounce=False)
    mo.vstack([
        mo.md("For **3,000 + 2,000 with a limit of 4,000**, predict the overflow. Then change one number to make it fit. If you reduce input, preserve needed evidence. If you reduce the output reserve, the answer may have less room. Finally test **6,000 + 2,000 with a limit of 8,000**: does an exact fit pass?"),
        budget_reason,
    ])
    return (budget_reason,)


@app.cell(hide_code=True)
def _(mo):
    system_text = mo.ui.text_area(value="Answer using the supplied document.", label="Instructions", full_width=True)
    history_text = mo.ui.text_area(value="User: What does a tokenizer do?\nAssistant: It represents text as IDs.", label="History", full_width=True)
    document_text = mo.ui.text_area(value="Vocabulary size counts catalogue entries. Context length counts sequence positions.", label="Document", full_width=True)
    question_text = mo.ui.text_area(value="Are vocabulary size and context length the same?", label="Current question", full_width=True)
    mo.accordion({"Optional: count a complete teaching request": mo.vstack([
        mo.md("These literal `[system]` / `[assistant]` labels are a **toy format**, not a real model's chat template. We count the complete serialized string, including separators, to show why counting only the question misses input. Use the target model's actual template and token accounting in production."),
        system_text, history_text, document_text, question_text,
    ])})
    return document_text, history_text, question_text, system_text


@app.cell(hide_code=True)
def _(
    budget_ok,
    context_limit,
    document_text,
    history_text,
    mo,
    output_reserve,
    question_text,
    system_text,
    tokenizer,
    toy_request,
):
    _contents, _request = toy_request(system_text.value, history_text.value, document_text.value, question_text.value)
    _plain_count = len(tokenizer.encode_ordinary(_contents))
    _request_count = len(tokenizer.encode_ordinary(_request))
    _question_count = len(tokenizer.encode_ordinary(question_text.value))
    _rows = [
        {"Counted text": "Question alone", "Tokens": _question_count},
        {"Counted text": "All contents joined with newlines", "Tokens": _plain_count},
        {"Counted text": "Complete teaching format", "Tokens": _request_count},
    ]
    _items = [mo.md("### Formatting experiment\nCounts are measured on complete strings; separate counts need not add exactly because boundaries can change tokenization."), mo.ui.table(_rows, selection=None), mo.md(f"**Formatting delta:** {_request_count - _plain_count} tokens in this example.")]
    if budget_ok:
        _remaining, _fits = context_budget(_request_count, output_reserve.value, context_limit.value)
        _items.append(mo.md(f"Using this measured complete request: fits = **{_fits}**, remaining = **{_remaining}**. This is separate from the supplied 3,000-token slide exercise above."))
    mo.accordion({"Optional experiment results": mo.vstack(_items)})
    return


@app.cell(hide_code=True)
def _(mo):
    takeaway = mo.ui.text_area(label="One surprising split and one practical consequence for prompt design", full_width=True, debounce=False)
    mo.vstack([
        mo.md("""
        ## 5. Bring your findings back

        - Compare the measured English/German/code counts with your original ranking.
        - Explain a space, punctuation or byte-fragment result using the inspector.
        - Explain the overflow and your revised context budget.

        **Cost:** at invented rates of €2 per million input tokens and €8 per
        million output tokens, 6,000 input + **500 actually generated** output cost
        `(6000 / 1_000_000) * 2 + (500 / 1_000_000) * 8 = €0.016`.
        Reserving 2,000 output tokens does not mean generating or billing 2,000.
        Real bills use the service's usage categories and rates.

        **Performance:** more input generally means more processing and stored
        context; longer answers need more generation steps. This tokenizer exercise
        does not measure LLM latency or answer quality. Remove unnecessary repetition
        while preserving useful evidence. Fitting alone does not guarantee correctness.
        """),
        takeaway,
    ])
    return (takeaway,)


@app.cell(hide_code=True)
def _(
    ENCODING_NAME,
    budget_ok,
    budget_reason,
    budget_result,
    comparison,
    context_limit,
    input_count,
    inspect_ok,
    json,
    mo,
    observation,
    output_reserve,
    prediction,
    takeaway,
    texts,
    tokenizer,
):
    _report = {
        "tokenizer": ENCODING_NAME,
        "hypothesis": prediction.value,
        "texts": texts,
        "comparison": comparison,
        "token_ids": {label: inspect_text(text, tokenizer)[0] for label, text in texts.items()} if inspect_ok else {},
        "controlled_edit": observation.value,
        "budget_inputs": {"input": input_count.value, "reserved_output": output_reserve.value, "limit": context_limit.value},
        "budget": budget_result,
        "budget_revision_and_tradeoff": budget_reason.value,
        "takeaway": takeaway.value,
        "checks_passed": {"inspect": inspect_ok, "budget": budget_ok},
    }
    mo.vstack([
        mo.md("### Save your work\nSave notebook code with **Ctrl+S** (Windows/Linux) or **Cmd+S** (macOS). Text-box observations are session values: **download your findings before closing**. Keep this JSON alongside your notebook; it records whether TODO checks passed. Nothing is uploaded."),
        mo.download(data=json.dumps(_report, ensure_ascii=False, indent=2).encode("utf-8"), filename="results-block1.json", label="Download my findings"),
        mo.md("""
        ### If you get stuck
        Open a hint, then check the `return` line and indentation. If a cell turns red,
        undo your last edit and rerun it. Ask your partner to explain what each variable
        means. Restarting the notebook does not erase saved code, but download typed
        observations first. The README has setup help and restart instructions.

        ### Where this fits
        Continuous Day 1 slides **20–21**: predict / measure. Slides **22–24**:
        cost, performance and sharing. These are Block 1 local slides **10–14**.
        [Presenter guide and speaking cues](https://github.com/ArdaS2012/EDV_Training/blob/main/docs/LLM_Training/llm_day1/01_tokenization_context.md#slide-11).

        Learn more: [tiktoken](https://github.com/openai/tiktoken),
        [SentencePiece](https://github.com/google/sentencepiece),
        [real chat templates](https://huggingface.co/docs/transformers/main/en/chat_templating),
        [marimo basics](https://docs.marimo.io/getting_started/).
        """),
    ])
    return


if __name__ == "__main__":
    app.run()
