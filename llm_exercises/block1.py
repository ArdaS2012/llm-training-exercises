"""Prepared displays and training orchestration; BPE algorithms live in student TODOs."""

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENCODING_NAME = "cl100k_base"
EXAMPLES = {
    "English": "The model predicts the next token.",
    "German": "Das Modell sagt das nächste Token voraus.",
    "Code": "next_token = model.predict(context)",
}
BPE_CORPUS = {"map": 8, "maps": 4, "cap": 5, "can": 10, "ran": 3}
BPE_PROBES = ("maps", "rap")


def check_pairs(count_pairs):
    """Small behavioral checks, without a reference counting implementation."""
    cases = [
        ({"cat": ["c", "a", "t"], "car": ["c", "a", "r"]}, {"cat": 2, "car": 1},
         {("c", "a"): 3, ("a", "t"): 2, ("a", "r"): 1},
         "Check the cat cat car example above: include the pairs from every copy of each word."),
        ({"shhh": ["s", "h", "h", "h"]}, {"shhh": 3}, {("s", "h"): 3, ("h", "h"): 6},
         "In each shhh, check s–h, then h–h, then h–h. Its frequency tells you how many copies there are."),
        ({"cat": ["cat"], "a": ["a"], "": []}, {"cat": 2, "a": 1, "": 1}, {},
         "A word stored as one token has no neighbouring pair. Empty lists also contribute none."),
        ({"cats": ["ca", "t", "s"]}, {"cats": 2}, {("ca", "t"): 2, ("t", "s"): 2},
         "Use the pieces in splits: ca is already one token in this check. See the folded special cases."),
    ]
    try:
        from copy import deepcopy
        for splits, frequencies, expected, message in cases:
            before = deepcopy(splits)
            original_frequencies = frequencies.copy()
            result = count_pairs(splits, frequencies)
            if result is None:
                return False, "TODO 1 is waiting. Return a dictionary of pair frequencies."
            if not isinstance(result, dict) or result != expected:
                return False, message
            if splits != before or frequencies != original_frequencies:
                return False, "Counting must leave the supplied token lists and frequencies unchanged."
        return True, "TODO 1 passed: weighted counts, repeated neighbours and word boundaries."
    except Exception as exc:
        return False, f"TODO 1 needs another look: {type(exc).__name__}: {exc}"


def check_merge(merge_pair):
    """Check non-overlap, existing multi-character tokens and input preservation."""
    cases = [
        (["a", "b", "a", "b"], ("a", "b"), ["ab", "ab"]),
        (["a", "a", "a"], ("a", "a"), ["aa", "a"]),
        (["ab", "c", "ab", "c"], ("ab", "c"), ["abc", "abc"]),
        (["a", "b", "c"], ("a", "c"), ["a", "b", "c"]),
        (["x"], ("x", "y"), ["x"]),
        ([], ("x", "y"), []),
    ]
    try:
        for tokens, pair, expected in cases:
            original = tokens.copy()
            result = merge_pair(tokens, pair)
            if result is None:
                return False, "TODO 2 is waiting. Return a new list after one merge pass."
            if not isinstance(result, list) or result != expected:
                return False, "Merge matching neighbours left to right without reusing a token. Keep all other tokens."
            if tokens != original or result is tokens:
                return False, "Return a new list; keep the original list unchanged for comparison."
        return True, "TODO 2 passed: repeated matches, overlap, merged tokens and empty input."
    except Exception as exc:
        return False, f"TODO 2 needs another look: {type(exc).__name__}: {exc}"


def train_bpe(frequencies, count_pairs, merge_pair, rounds=3):
    """Supply the training loop, calling the learner's two algorithmic steps."""
    splits = {word: list(word) for word in frequencies}
    merges, trace = [], []
    for step in range(1, rounds + 1):
        counts = count_pairs(splits, frequencies)
        if not counts:
            break
        pair = min(counts, key=lambda item: (-counts[item], item))
        splits = {word: merge_pair(tokens, pair) for word, tokens in splits.items()}
        merges.append(pair)
        trace.append({
            "Round": step, "Chosen pair": list(pair), "Weighted occurrences": counts[pair],
            "All pair counts": [
                {"pair": list(key), "count": value}
                for key, value in sorted(counts.items(), key=lambda item: (-item[1], item[0]))
            ],
            "Splits after merge": {word: tokens.copy() for word, tokens in splits.items()},
            "Corpus token positions": sum(len(splits[word]) * freq for word, freq in frequencies.items()),
        })
    return {"frequencies": dict(frequencies), "merges": merges, "trace": trace, "splits": splits}


def apply_bpe(word, merges, merge_pair, alphabet):
    """Replay this toy's learned rules; reject characters absent from its alphabet."""
    if not set(word) <= set(alphabet):
        raise ValueError("Use only characters from the training alphabet in this toy.")
    tokens = list(word)
    for pair in merges:
        tokens = merge_pair(tokens, pair)
    return tokens


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
