"""One launcher for Windows, macOS and Linux. Run: uv run python start.py."""

import argparse
import subprocess
import sys
from pathlib import Path

from llm_exercises.block1 import ENCODING_NAME, EXAMPLES, load_tokenizer


def main():
    parser = argparse.ArgumentParser(description="Open a prepared marimo exercise.")
    parser.add_argument("--block", choices=["1", "2", "3", "4", "d2-1", "d2-2"], default="1", help="Exercise block (default: 1).")
    parser.add_argument("--check", action="store_true", help="Verify selected exercise setup without opening a browser.")
    parser.add_argument("--port", type=int, default=2718, help="Local notebook port (default: 2718).")
    parser.add_argument("--offline-models", action="store_true", help="Use cached Day 2 model files only; prohibit model downloads.")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    try:
        import marimo
        if args.block == "1":
            print("Preparing the tokenizer. First use needs internet; later runs use the local cache.", flush=True)
            tokenizer = load_tokenizer()
            for label, text in EXAMPLES.items():
                ids = tokenizer.encode_ordinary(text)
                assert tokenizer.decode(ids) == text
                print(f"  {label}: {len(ids)} tokens", flush=True)
            print(f"Ready: Python {sys.version.split()[0]}, tokenizer {ENCODING_NAME}. No API key needed.", flush=True)
        elif args.block == "2":
            from llm_exercises.block2 import Q, K, V, changed_inputs
            assert all(len(matrix) == 3 for matrix in (Q, K, V))
            assert changed_inputs("Q", 0, 0, 0) == (Q, K, V)
            print(f"Ready: Block 2, Python {sys.version.split()[0]}, marimo {marimo.__version__}. Local toy data; no assets or API key needed.")
        elif args.block == "3":
            from llm_exercises.block3 import SCORES, LOGITS, row_softmax
            assert len(SCORES) == 3 and len(LOGITS) == 4
            assert abs(sum(row_softmax(SCORES[0])) - 1) < 1e-9
            print(f"Ready: Block 3, Python {sys.version.split()[0]}, marimo {marimo.__version__}. Local toy data; no assets or API key needed.")
        elif args.block == "d2-2":
            from llm_exercises.rag import preflight
            report = preflight(online=not args.offline_models)
            print(f"Ready: Mini-RAG on local CPU; {report}")
        elif args.block == "d2-1":
            from llm_exercises.prompting import load_model, generate, MODEL, CACHE
            load_model(online=not args.offline_models)
            sample = generate([{"role": "user", "content": "Say hello."}], max_tokens=8)
            assert sample['output_tokens'] > 0
            print(f"Ready: {MODEL}, CPU greedy inference; cache {CACHE}; measured smoke call {sample['seconds']} s.")
        else:
            from llm_exercises.block4 import FEATURES, TARGETS, VOCABULARY, softmax
            assert len(FEATURES) == len(TARGETS) == 3 and len(VOCABULARY) == 4
            assert softmax([0.0]*4) == [0.25]*4
            print(f"Ready: Block 4, Python {sys.version.split()[0]}, marimo {marimo.__version__}. Local toy data; no assets or API key needed.")
    except Exception as exc:
        print(f"Setup could not finish: {exc}\nFor d2-1 use --group prompting; for d2-2 first run uv sync --locked --group rag. Connect to the internet for first model preflight and retry. On a managed network, see README.md → Troubleshooting.", file=sys.stderr)
        return 1
    if args.check:
        print("Setup check passed. You can now work offline on this computer.")
        return 0
    notebooks = {"d2-2": "day2-block-02-rag/02_mini_rag.py", "d2-1": "day2-block-01-prompt-engineering/01_prompt_engineering.py", "2": "block-02-self-attention/02_self_attention.py", "1": "block-01-tokenization-context/01_tokenization_context.py", "3": "block-03-transformer-architecture/03_masking_sampling.py", "4": "block-04-training-alignment/04_next_token_learning.py"}
    print(f"Opening the editor at http://127.0.0.1:{args.port}. Keep this terminal open; Ctrl+C stops it.", flush=True)
    try:
        return subprocess.call(
            [sys.executable, "-m", "marimo", "edit", str(root / "exercises" / notebooks[args.block]),
             "--host", "127.0.0.1", "--port", str(args.port),
             "--no-token", "--no-sandbox", "--skip-update-check"], cwd=root
        )
    except KeyboardInterrupt:
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
