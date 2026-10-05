# Day 2 Block 1 — Prompt Engineering

Compare zero-shot and few-shot extraction, system policy, a checkable reasoning
example and JSON output checks. Two short TODOs build prompts; model loading,
generation, widgets and format checks are supplied. Work in pairs for 35 minutes.
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

## Tasks and evidence

1. **Predict (3 min):** describe expected missing-field behavior and why JSON can
   still be factually wrong.
2. **TODO 1 (8 min):** return system/user messages; optionally insert the supplied
   example user/assistant pair. Preserve the current document and system policy.
   Run six calls: three documents × two variants.
3. **Inspect (7 min):** compare the raw answers against every document. Record
   correct / incorrect / uncertain with source words; count fully correct cases
   out of three per variant. Inspect automatic schema flags separately. Save a
   baseline export, then change only the policy and rerun. Record one failed case.
4. **TODO 2 (8 min):** return a reasoning instruction, optionally including the
   supplied worked demonstration. Predict the new arithmetic task on paper, run
   both variants, and check steps and final count.
5. **Compare/share (8 min):** explain the controlled change, case-level factual
   judgments, schema validity and one limitation. Finish any missing observations.
6. **Save (1 min):** save Python and download `results-day2-block1.json`. The export
   contains actual prompts, raw outputs, format flags, timings/token counts and your
   notes. Browser widget values are not preserved by saving Python alone.

The comparison table provides automatic JSON/schema flags; you assess task
correctness against the source. No factual score is silently inferred from fluency.
Few-shot can help, do nothing or make output worse. This tiny model may fail every
case; document that honestly. A rationale is generated text, not a truth certificate.
The supplied helper uses ordinary greedy decoding, without constrained JSON decoding
or automatic repair. Counts refer to this small fixed diagnostic set, not a benchmark.

## Help and course mapping

Show TODO code and run with Shift+Enter. Do not edit the supplied setup. Waiting
messages are expected before implementation. If the model cache is missing, run
the preflight online. Proxy/certificate or PATH problems use the shared guide.
If code turns red, undo and check indentation and return values. Each reasoning
run is independent of the extraction TODO. A response stopped at 96 tokens may be
truncated; record it as a failure. Buttons bound model calls; no automatic paid calls.
A fixed greedy configuration improves comparability but is not a cross-hardware
bit-for-bit promise. The download includes all inputs: inspect it before sharing.

Actual trainer map: Day 2 slides **9–14** teach the concepts, **15–16** are the
breakout/debrief, **17 — Hands-on prompting starts now** launches this notebook,
**18 — What changed in the measured answers?** reviews findings. Students need no
private trainer files. Sources: [few-shot paper](https://arxiv.org/abs/2005.14165),
[Chain-of-Thought paper](https://arxiv.org/abs/2201.11903),
[chat templates](https://huggingface.co/docs/transformers/v4.57.1/en/chat_templating),
[JSON Schema](https://json-schema.org/understanding-json-schema/reference/object).
