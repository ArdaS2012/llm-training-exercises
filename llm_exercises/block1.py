"""Infrastructure supplied to students; the two TODOs live in the notebook."""

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENCODING_NAME = "cl100k_base"
EXAMPLES = {
    "English": "The model predicts the next token.",
    "German": "Das Modell sagt das nächste Token voraus.",
    "Code": "next_token = model.predict(context)",
}


def load_tokenizer():
    """Use a repo-local cache so pre-class setup also works offline later."""
    import tiktoken

    # Always use the exercise cache, including in the spawned marimo process.
    os.environ["TIKTOKEN_CACHE_DIR"] = str(ROOT / ".tokenizer-cache")
    return tiktoken.get_encoding(ENCODING_NAME)


def token_rows(tokenizer, ids):
    """Show byte fragments without implying every token is valid UTF-8 alone."""
    return [
        {
            "Position (from 0)": position,
            "Token ID": token_id,
            "Piece (repr; spaces visible)": repr(
                tokenizer.decode_single_token_bytes(token_id).decode(
                    "utf-8", errors="backslashreplace"
                )
            ),
            "Bytes (hex)": tokenizer.decode_single_token_bytes(token_id).hex(" "),
        }
        for position, token_id in enumerate(ids)
    ]


def check_inspect(inspect_text, tokenizer):
    """Check unseen examples, empty input, whitespace and Unicode; no grading API."""
    try:
        for text in ["", *EXAMPLES.values(), " hello  world\n", "🙂 café", "<|endoftext|>"]:
            result = inspect_text(text, tokenizer)
            if result is None or result == (None, None):
                return False, "TODO 1 is waiting for your two lines. Everything else is ready."
            ids, count = result
            if ids != tokenizer.encode_ordinary(text):
                return False, "The IDs differ. Use tokenizer.encode_ordinary(text) on the original text."
            if type(count) is not int or count != len(ids):
                return False, "Count sequence positions with len(ids), including repeated IDs."
            if tokenizer.decode(ids) != text:
                return False, "Full-sequence decoding should restore the original text."
        return True, "TODO 1 passed: empty text, all three examples, spaces and Unicode."
    except Exception as exc:
        return False, f"TODO 1 needs another look: {type(exc).__name__}: {exc}"


def check_budget(context_budget):
    """Boundary and overflow checks prevent a hard-coded answer from passing."""
    # Expected outcomes are feedback fixtures, not a reference implementation.
    cases = [
        (3000, 2000, 4000, -1000, False),
        (3000, 1000, 4000, 0, True),
        (6000, 2000, 8000, 0, True),
        (0, 0, 4000, 4000, True),
        (35, 10, 64, 19, True),
    ]
    try:
        for input_tokens, reserve, limit, expected, expected_fit in cases:
            result = context_budget(input_tokens, reserve, limit)
            if result is None or result == (None, None):
                return False, "TODO 2 is waiting for your two lines."
            remaining, fits = result
            if type(remaining) is not int or remaining != expected:
                return False, "Subtract input AND reserved output from the context limit. Keep a negative result."
            if type(fits) is not bool or fits != expected_fit:
                return False, "An exact fit is allowed: remaining == 0 must also fit."
        return True, "TODO 2 passed: overflow, exact fit, spare room and empty input."
    except Exception as exc:
        return False, f"TODO 2 needs another look: {type(exc).__name__}: {exc}"


def toy_request(system, history, document, question):
    """Explicit teaching serialization, NOT a real model's chat template."""
    values = [system, history, document, question]
    labels = ["system", "history", "document", "question"]
    contents_only = "\n".join(values)
    formatted = "\n".join(f"[{label}]\n{value}" for label, value in zip(labels, values))
    return contents_only, formatted + "\n[assistant]\n"
