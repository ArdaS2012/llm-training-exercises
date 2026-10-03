"""One launcher for Windows, macOS and Linux. Run: uv run python start.py."""

import argparse
import subprocess
import sys
from pathlib import Path

from llm_exercises.block1 import ENCODING_NAME, EXAMPLES, load_tokenizer


def main():
    parser = argparse.ArgumentParser(description="Open the prepared Block 1 marimo exercise.")
    parser.add_argument("--check", action="store_true", help="Prepare tokenizer and verify setup without opening a browser.")
    parser.add_argument("--port", type=int, default=2718, help="Local notebook port (default: 2718).")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    try:
        print("Preparing the tokenizer. First use needs internet; later runs use the local cache.", flush=True)
        tokenizer = load_tokenizer()
        for label, text in EXAMPLES.items():
            ids = tokenizer.encode_ordinary(text)
            assert tokenizer.decode(ids) == text
            print(f"  {label}: {len(ids)} tokens", flush=True)
        print(f"Ready: Python {sys.version.split()[0]}, tokenizer {ENCODING_NAME}. No API key needed.", flush=True)
    except Exception as exc:
        print(f"Setup could not finish: {exc}\nConnect to the internet and retry. On a managed network, see README.md → Troubleshooting.", file=sys.stderr)
        return 1
    if args.check:
        print("Setup check passed. You can now work offline on this computer.")
        return 0
    print(f"Opening the editor at http://127.0.0.1:{args.port}. Keep this terminal open; Ctrl+C stops it.", flush=True)
    try:
        return subprocess.call(
            [sys.executable, "-m", "marimo", "edit", str(root / "notebooks" / "01_tokenization_context.py"),
             "--host", "127.0.0.1", "--port", str(args.port),
             "--no-token", "--no-sandbox", "--skip-update-check"], cwd=root
        )
    except KeyboardInterrupt:
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
