# LLM Training Exercises

Prepared marimo exercises for the LLM course, using one shared Python environment.
This README covers repository access, installation, starting/stopping marimo and
general troubleshooting. Learning goals and task instructions belong in each
[exercise folder’s README](exercises/README.md).

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

## Choose an exercise

See the [exercise index](exercises/README.md), then read the README in the selected
block folder. Each folder contains its own notebook, tasks and task-specific help.

| Available block | Instructions |
|---|---|
| 1 — Tokenization & Context | [Block 1 README](exercises/block-01-tokenization-context/README.md) |

Only Block 1 is currently supplied. The launcher opens that block by default.
Future blocks will use separate folders and the same shared environment.

## Save, stop and return

- Save your code with **Ctrl+S** on Windows/Linux or **Cmd+S** on macOS.
- Save session inputs using the block’s documented findings export before closing.
  Browser input values are not automatically saved into the notebook code.
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

For coding feedback, notebook outputs and saving observations, see your block’s README.

The supported classroom targets are current Windows 10/11, macOS (Intel/Apple Silicon),
and Linux on platforms with the locked dependencies' Python wheels. Unusual architectures,
old operating systems and managed devices may need a trainer-assisted setup. OS automation
checks are in `.github/workflows/check.yml`; their actual results are visible in GitHub Actions.

## Repository map

| Path | Purpose |
|---|---|
| [exercises/](exercises/README.md) | Exercise index; one folder and README per block |
| `start.py`, `start.sh`, `start.cmd` | Cross-platform launchers and pre-class check |
| `pyproject.toml`, `uv.lock`, `.python-version` | Reproducible Python environment |
| `llm_exercises/` | Prepared display, tokenizer and feedback helpers |
| `tests/` | Checks for setup, feedback and the unfinished starter |

## For trainers and maintainers

The student repository contains the unfinished exercise and setup checks. Instructor
answers and completed-notebook checks are maintained separately on the trainer’s computer
and are excluded from Git. Run the public starter checks with:

```sh
uv run --locked python start.py --check
uv run --locked python -m unittest discover -s tests -v
```

This repository is independent. Students clone it directly; no parent training repository is needed.
In the parent repository it is registered as the `llm-training-exercises` Git submodule.
Parent maintainers obtain it with `git submodule update --init llm-training-exercises`;
after exercise changes are committed here, update the parent submodule pointer.

Add future blocks as `exercises/block-XX-topic/`, with a README and notebook. Keep shared
setup here and the learning goals, TODO walkthrough, result requirements and specialized
troubleshooting in that block’s README. Update the exercise index and path references.

Sources: [marimo project environments](https://docs.marimo.io/guides/package_management/projects/),
[uv + marimo](https://docs.astral.sh/uv/guides/integration/marimo/).

Exercise code and documentation: MIT; see [LICENSE](LICENSE). Third-party packages retain their own licenses.
