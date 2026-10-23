# Day 2 Block 1 — Prompt Engineering

Compare zero-shot and few-shot extraction, system policy, a checkable reasoning
example and JSON output checks. Two short TODOs build prompts; model loading,
generation, widgets and format checks are supplied. Work in pairs in breakout rooms for the 30-minute investigation after the brief orientation.
Prerequisites: Day 1 inference/context and basic Python lists/dictionaries.
Read the [shared setup guide](../../README.md) first.

## Prepare and launch

From your exercise repository, on Windows/macOS/Linux:

```sh
uv sync --locked --group prompting
uv run --locked --group prompting python start.py --block d2-1 --check
uv run --locked --group prompting python start.py --block d2-1
```

Select **d2-1**, not Day 1's default Block 1. Wrappers also accept `--block d2-1`.
The local editor opens at http://127.0.0.1:2718; leave the terminal running. Use
`--port 2720` for a conflict. Save code with Ctrl+S / Cmd+S; stop with Ctrl+C.
After successful online setup, verify the cached route on that same computer:

```sh
uv run --offline --locked --group prompting python start.py --block d2-1 --offline-models --check
uv run --offline --locked --group prompting python start.py --block d2-1 --offline-models
```

The notebook always loads cached files only. `uv --offline` controls package
resolution; `--offline-models` separately prevents model downloads in preflight.

Model: [HuggingFaceTB/SmolLM2-135M-Instruct](https://huggingface.co/HuggingFaceTB/SmolLM2-135M-Instruct),
revision `12fd25f77366fa6b3b4b768ec3050bf629380bac`, Apache-2.0 per its model card.
CPU inference uses Transformers 4.57.1 / PyTorch 2.8.0 and greedy decoding, with
96 new tokens per call. Observed model cache: about **260 MiB**; the Linux CPU
PyTorch wheel download is about **175 MiB**, plus other dependencies. Allow disk
space for installed libraries and caches. First setup needs Hugging Face and
package-index access; no API key, paid account or GPU. Linux x86-64 was verified
locally. CI is configured for Linux, Windows and macOS runners; those CI runs have
not been executed locally. Intel macOS and other architectures are unverified;
this pinned PyTorch release may have no compatible wheel. Use an approved supported
machine rather than promising every platform works. Prompt data stay on the
local CPU; preflight requests model assets from Hugging Face. Use the supplied
public toy texts, not confidential material.

## Exercise + breakout

Follow the [30-minute investigation](GROUP_TASK.md) after the brief orientation. It defines the required comparison, evidence and shared result. Keep the technical help below for the bounded TODOs.

## Help and course mapping

Show TODO code and run with Shift+Enter. Do not edit the supplied setup. Waiting
messages are expected before implementation. If the model cache is missing, run
the preflight online. Proxy/certificate or PATH problems use the shared guide.
If code turns red, undo and check indentation and return values. Each reasoning
run is independent of the extraction TODO. A response stopped at 96 tokens may be
truncated; record it as a failure. Buttons bound model calls; no automatic paid calls.
A fixed greedy configuration improves comparability but is not a cross-hardware
bit-for-bit promise. The download includes all inputs: inspect it before sharing.

Current handoff: LLM Day 2 slide 17, **Exercise: test a prompt revision**. The combined room task runs 09:40–10:10; setup/review are separate.

## Current teaching handoff

LLM Day 2, Block 1: actual slide **17 — Exercise: test a prompt revision** launches the combined exercise + breakout. Return to plenary at the agenda’s room end. The notebook and group task are self-contained; private trainer files are not required.

## Why this is hands-on

Build and stress-test a research intake assistant: can a prompt protect missing facts and resist instructions hidden in a document? Both partners change or inspect actual runnable behavior, challenge a prediction with source evidence, and make a decision. The [investigation](GROUP_TASK.md) keeps the slide takeaways beside the task and gives a topic-specific 30-minute route; extra time is for understanding and diagnosis, not more boilerplate code.
