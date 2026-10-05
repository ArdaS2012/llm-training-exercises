# Day 2 Block 2 — Mini-RAG over your own documents

Build a traceable retrieval-and-generation pipeline in pairs (45 minutes).
Prerequisites: basic Python lists/dictionaries, Day 1 context/inference and Day 2
prompting. Read the [shared setup](../../README.md) first. Two TODOs select
reranked records and compose labelled context; all other plumbing is supplied.

## Prepare and launch

From the student repository, on a supported Windows/macOS/Linux machine:

```sh
uv sync --locked --group rag
uv run --locked --group rag python start.py --block d2-2 --check
uv run --locked --group rag python start.py --block d2-2
```

`bash start.sh --block d2-2` / `start.cmd --block d2-2` select the same dependency group.
The editor uses http://127.0.0.1:2718; use `--port 2722` if busy. Save code with
Ctrl+S / Cmd+S, rerun a TODO with Shift+Enter, and stop the terminal with Ctrl+C.
After online preflight, use this on that same computer:

```sh
uv run --offline --locked --group rag python start.py --block d2-2 --offline-models --check
uv run --offline --locked --group rag python start.py --block d2-2 --offline-models
```

`uv --offline` controls package access; `--offline-models` controls model access.
The notebook always uses cached model files. Missing assets require online preflight.
Models are local CPU-only, with no paid account, API key, GPU or remote inference:

| Role | Model / exact revision | Assumptions |
|---|---|---|
| Embeddings | [all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2), `1110a243fdf4706b3f48f1d95db1a4f5529b4d41` | 384 dimensions, mask-aware mean pooling, unit normalization, truncation at 256 model tokens |
| Reranker | [ms-marco-TinyBERT-L2-v2](https://huggingface.co/cross-encoder/ms-marco-TinyBERT-L2-v2), `81d1926f67cb8eee2c2be17ca9f793c7c3bd20cc` | Query/passage pair, 512-token cap, raw logits; higher ranks first |
| Generator | [SmolLM2-135M-Instruct](https://huggingface.co/HuggingFaceTB/SmolLM2-135M-Instruct), `12fd25f77366fa6b3b4b768ec3050bf629380bac` | Same generator as prompting, CPU greedy decoding, 96 new tokens |

All three model cards declare Apache-2.0 (checked 2026-10-05). Environment:
Transformers 4.57.1, PyTorch 2.8.0 CPU, Chroma 1.5.9, marimo 0.25.1.
First setup downloads assets from Hugging Face and locked packages; reserve at
least 2 GB disk for libraries and caches. See the verification record for measured
cache sizes and latency. Linux x86-64 is tested locally. The three-OS CI matrix
is configured, not evidence of completed Windows/macOS runs; this PyTorch pin
may lack Intel macOS wheels. Verify the actual classroom computers in advance.

## Your documents and data flow

Create an ignored `documents/` folder inside this repository. Add **your own**
2–4 short permitted English UTF-8 `.txt`/`.md` texts, ideally 100–250 words each.
Examples: a project description, your own lab procedure or an event plan.
Use material you wrote or may reuse, with no confidential/personal information.
Each file must be at most 20,000 bytes; at most eight immediate files are read.
No recursive folders, PDF, Word, OCR or automatic web fetching. Enter the folder
path in the notebook; an absolute path avoids launch-directory ambiguity.

Text, embeddings and queries stay local. Chroma is **in memory**, with explicit
embeddings and telemetry disabled; temporary collections are deleted after search.
No Chroma account/server or default embedding download is used. Rebuild from files
after restart. Model caches stay in ignored `.cache/`. Results include full text,
question, prompt and answer, so inspect them before sharing. Deleting source files
does not delete a previously downloaded results file.

Public sample documents in `samples/` are a technical fallback, explicitly labelled
fictional. Using only samples does not fulfill the own-document activity.

## Tasks, timing and findings

1. **Prepare/predict (8 min):** inspect your documents; write two answerable
   questions and one whose answer is absent from all documents. Predict supporting
   passages and the effect of smaller chunks.
2. **TODO 1 (7 min):** order candidate dictionaries by descending reranker score;
   retain `keep` records (or all when fewer exist). Preserve text and metadata.
3. **TODO 2 (7 min):** return a single context string containing every passage
   unchanged with its exact `[chunk ID]` label. Test independently of TODO 1.
4. **Measure (13 min):** press Run for three questions × two chunk settings.
   Baseline: 80 whitespace words; changed: 40 or 120; both overlap 20. Hold
   model/questions, five candidates and two selected passages fixed. Inspect cosine
   order before reranking, raw logits after reranking and actual generated answers.
5. **Judge (8 min):** record supported/unsupported/uncertain per answer. Verify
   each citation exists AND supports its claim. Check the absent question across
   original files. Explain one retrieval change and one failure/limitation.
6. **Save/share (2 min):** save Python and download `results-day2-block2.json`.
   Provide three baseline question/answer/source records plus the controlled
   comparison and absent-answer finding. Retain the export for Block 4.

The export format `edv-mini-rag-v1` includes document hashes/text, question IDs,
chunk settings/boundaries, vector/rerank results, selected context, real generator
metadata/outputs and manual judgments. It is a JSON handoff for future evaluation;
Block 4's importer is not yet authored. Saving Python alone loses browser values.
Export before editing settings; edits invalidate reactive run results and judgments
must be reassessed for a new run. No gain is guaranteed. This tiny generator can
invent facts/citations or fail to abstain: keep its raw output and explain the error.

## Help and mapping

Friendly waiting messages are normal before TODO completion/documents. Keep TODO
function names and return types. If context overflows, shorten documents or select
fewer/shorter passages in an explicitly recorded follow-up experiment. Model token
counts differ from word counts. A top score is not an answerability threshold;
reranking cannot see passages omitted from vector candidates. Repeat setup preflight
for missing caches; shared README covers proxy/PATH/port problems. Restart from the
same selection command; saved code persists, downloaded observations are separate.

Actual trainer slides: **21–30** concepts; **31** planned Visual Lab;
**32 — Hands-on Mini-RAG starts now** launches this notebook;
**33 — Locate the failure before changing the pipeline** reviews findings.
Students need no private presenter files. Sources: [RAG](https://arxiv.org/abs/2005.11401),
[Chroma collections](https://docs.trychroma.com/docs/collections/add-data),
[FAISS](https://github.com/facebookresearch/faiss/wiki/Getting-started).
