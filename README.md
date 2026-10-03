# LLM Training Exercises

Prepared Python exercises for the LLM course. Start with **Block 1 — Tokenization & Context**:
predict token boundaries, compare English/German/code, and calculate a context budget.
The notebook guides you through two small `# TODO` areas. Everything else is provided.

**You need:** a browser, an internet connection for the first setup, and `uv`.
No separate Python installation, API key, paid account, GPU, Docker, Conda or editor is required.
The exercise runs locally. It does not call an LLM or send your text to a model provider.

## Start here

### 1. Install uv once

uv manages Python and the exercise's dependencies for you. Use the command for your computer,
then **close and reopen your terminal** so it can find uv.

**Windows 10/11 — PowerShell** (open PowerShell from the Start menu):

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS / Linux — Terminal:**

```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
```

These are the [official uv installation commands](https://docs.astral.sh/uv/getting-started/installation/).
If your organization's policy blocks the installer, use its approved installation route
or the alternatives on that page. Administrator access is normally unnecessary.

### 2. Get your own exercise folder

If Git is already installed, run these commands in your terminal (same on all three systems):

```sh
git clone https://github.com/ArdaS2012/llm-training-exercises.git
cd llm-training-exercises
```

**No Git installed?** On the [repository page](https://github.com/ArdaS2012/llm-training-exercises),
choose **Code → Download ZIP**, extract it, and open a terminal in the extracted folder
(`llm-training-exercises-main`). On Windows, right-click the folder and choose **Open in Terminal**;
on macOS/Linux, open Terminal and `cd` to that folder. Work in the extracted folder, not inside the ZIP.

### 3. Open the exercise

```sh
uv run --locked python start.py
```

Use this same command every time. First launch downloads a compatible Python 3.12 if needed,
installs the locked dependencies in `.venv`, and caches the tokenizer's small vocabulary asset.
Wait until it says **Ready**. The marimo editor opens in your browser; if it does not,
open **http://127.0.0.1:2718**. Keep the terminal open while working.

Windows users can also double-click **start.cmd** after installing uv.
On macOS/Linux you can use **`sh start.sh`**. Both launchers work even when the folder path contains spaces.

## Before class: one setup check

Run this on the same computer and user account you will use in class, while online:

```sh
uv run --locked python start.py --check
```

**Setup check passed** means Python, dependencies and tokenizer are ready. Keep `.venv`
and `.tokenizer-cache` in place; afterward the exercise can run without internet:

```sh
uv run --offline --locked python start.py
```

Moving the folder to another computer does not move a usable Python environment.
Repeat setup on that computer. Optional documentation links need internet, but the exercise does not.

## What to do in Block 1

1. Record the ranking and reasons from your Token Detective group before measuring.
2. Show the code in **TODO 1** and replace two `None` values to encode text and count IDs.
3. Run the cell with **Shift+Enter**. The check, comparison table and token inspector update.
4. Change one word, space, newline or symbol in a text box. Predict first; record before/after counts.
5. Complete **TODO 2**: calculate remaining context space and whether the request fits.
6. Test an overflowing request, an exact fit, and one revised budget; explain the tradeoff.
7. Download your findings and save the notebook code. Bring one surprising result to the discussion.

Hints are folded below each TODO. A **waiting** message on first launch is expected;
the notebook is intentionally unfinished. Only edit the two marked TODO areas at first.
The setup and display cells are prepared. Basic Python is enough.

The tokenizer is **tiktoken / cl100k_base**, used as a concrete BPE example. It is not a universal
tokenizer or a claim about a current model's context limit. All budgets, role labels and cost
rates are labelled teaching examples. The optional request experiment demonstrates formatting
overhead using a toy format; use a real model's own chat template for production accounting.

## Save, stop and return

- Save your code with **Ctrl+S** on Windows/Linux or **Cmd+S** on macOS.
- Text-box observations are session values. Choose **Download my findings** before closing;
  the JSON contains your hypotheses, texts, measured counts/IDs, budget and explanations.
- Stop with **Ctrl+C** in the terminal. Restart with the same launch command.
- Keep your downloaded JSON with your notebook (downloads may initially go to the browser's Downloads folder).
- To preserve a checkpoint with Git, commit your notebook changes on your own local branch.
  No pushing is needed to complete the exercise.

To reset just the starter after saving your work elsewhere, clone/download a fresh folder.
That is simpler and safer than resetting your whole checkout.

## Troubleshooting

| What you see | What to try |
|---|---|
| `uv` is not recognized / command not found | Reopen the terminal after installing. Check `uv --version`. On Windows try a new PowerShell window. See the official installation page for PATH help. |
| Download or certificate failure on first launch | Check internet/proxy access and your organization's certificate setup. For a managed system trust store, try `uv --native-tls sync --locked`. If tokenizer download still fails, ask IT to allow `openaipublic.blob.core.windows.net`; tiktoken uses Python Requests and may need an approved `REQUESTS_CA_BUNDLE`. Do not disable certificate checks. |
| Browser did not open | Manually open `http://127.0.0.1:2718` on the same computer. Keep the terminal running. |
| Port 2718 already in use | Run `uv run --locked python start.py --port 2719`, then use `http://127.0.0.1:2719`. |
| Cannot find `start.py` | Open the terminal in the extracted/cloned exercise folder, where README.md and start.py are visible. |
| Red error after editing a TODO | Undo your last edit, check indentation and spelling, keep the function's return line, and rerun with Shift+Enter. |
| Check still says waiting | Replace **both** `None` values in that TODO, then run the cell. |
| Weird `\x..` in token pieces | A token can contain only part of a UTF-8 character. Inspect bytes and the full-sequence decode; this is expected. |
| Changes in text boxes are gone after restarting | Those are session inputs; save them with **Download my findings** before closing. Saved Python code remains in the notebook file. |
| Browser screen too crowded | Collapse code cells you are not editing. You only need the TODO code and the results. |

The supported classroom targets are current Windows 10/11, macOS (Intel/Apple Silicon),
and Linux on platforms with the locked dependencies' Python wheels. Unusual architectures,
old operating systems and managed devices may need a trainer-assisted setup. OS automation
checks are in `.github/workflows/check.yml`; their actual results are visible in GitHub Actions.

## Repository map

| Path | Purpose |
|---|---|
| `notebooks/01_tokenization_context.py` | Your editable marimo starter, with two TODO areas |
| `start.py`, `start.sh`, `start.cmd` | Cross-platform launchers and pre-class check |
| `pyproject.toml`, `uv.lock`, `.python-version` | Reproducible Python environment |
| `llm_exercises/` | Prepared display, tokenizer and feedback helpers |
| `tests/` | Checks for setup, feedback and the unfinished starter |

Only Block 1 is supplied so far. Other blocks can be added here without asking students
to install a separate environment for each exercise.

## For trainers and maintainers

The student repository contains the unfinished exercise and setup checks. Instructor
answers and completed-notebook checks are maintained separately on the trainer’s computer
and are excluded from Git. Run the public starter checks with:

```sh
uv run --locked python start.py --check
uv run --locked marimo check --strict notebooks/01_tokenization_context.py
uv run --locked python -m unittest discover -s tests -v
```

This repository is independent. Students clone it directly; no parent training repository is needed.
In the parent repository it is registered as the `llm-training-exercises` Git submodule.
Parent maintainers obtain it with `git submodule update --init llm-training-exercises`;
after exercise changes are committed here, update the parent submodule pointer.

Sources: [marimo project environments](https://docs.marimo.io/guides/package_management/projects/),
[uv + marimo](https://docs.astral.sh/uv/guides/integration/marimo/),
[tiktoken implementation](https://github.com/openai/tiktoken),
[SentencePiece](https://github.com/google/sentencepiece),
[Hugging Face chat templates](https://huggingface.co/docs/transformers/main/en/chat_templating).

Exercise code and documentation: MIT; see [LICENSE](LICENSE). Third-party packages retain their own licenses.
