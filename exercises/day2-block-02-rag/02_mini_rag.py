import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="Mini-RAG · Day 2 Block 2")


@app.cell(hide_code=True)
def _():
    import json
    import sys
    from pathlib import Path
    import marimo as mo
    sys.path.insert(0, str(next(p for p in Path(__file__).resolve().parents if (p / 'llm_exercises').is_dir())))
    from llm_exercises.rag import read_documents, chunk_documents, retrieve, rerank, validate_selection, validate_context, answer, EMBED_MODEL, EMBED_REVISION, RERANK_MODEL, RERANK_REVISION
    return EMBED_MODEL, EMBED_REVISION, RERANK_MODEL, RERANK_REVISION, answer, chunk_documents, json, mo, read_documents, rerank, retrieve, validate_context, validate_selection


@app.cell(hide_code=True)
def _(EMBED_MODEL, RERANK_MODEL, mo):
    mo.md(f"""
    # Build a Mini-RAG over your own documents
    **Day 2 Block 2 · launch slide 32, findings slide 33. Work in pairs: 45 minutes.**

    You will ingest your own permitted text → split chunks → embed → search Chroma →
    rerank → select evidence → generate → check sources. Two short TODOs are yours;
    model/database plumbing is supplied. Predict before measuring. The generator is
    a small real model and may invent an answer or citation: keep that failure.

    **Preparation:** README preflight first. CPU only; no API key. Embeddings:
    `{EMBED_MODEL}`; reranker: `{RERANK_MODEL}`. These English models need short
    English texts for this exercise. Work with 2–4 non-confidential `.txt`/`.md` files
    you created or have permission to use, ideally 100–250 words each. No PDF parsing.
    All inference stays on your computer. Downloads/results contain document text.
    Show TODO code, replace `None`, then run **Shift+Enter**. Save with Ctrl+S / Cmd+S.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    folder = mo.ui.text(value="documents", label="Folder of your UTF-8 .txt/.md files (absolute path is safest)", full_width=True)
    questions = mo.ui.array([mo.ui.text(label=f"Question {i}: {'answer absent from ALL documents' if i == 3 else 'answer supported by your documents'}", full_width=True) for i in [1, 2, 3]])
    prediction = mo.ui.text_area(label="Predict: which source should answer Q1/Q2? Why is Q3 absent? What might smaller chunks lose?", full_width=True, debounce=False)
    changed_size = mo.ui.dropdown(options={"40 words":40,"120 words":120}, value="40 words", label="Changed chunk size; baseline is 80 words. Both use overlap 20.")
    mo.vstack([mo.md('## 1. Prepare and predict (8 min)\nCreate the documents folder, add your own short files, and write two answerable questions plus one absent-answer question. Do not put the answers into the question. Name expected source passages in your prediction.'), folder, questions, prediction, changed_size])
    return changed_size, folder, prediction, questions


@app.cell(hide_code=True)
def _(folder, mo, read_documents):
    documents = []
    document_issue = ""
    try:
        documents = read_documents(folder.value)
    except Exception as _exc:
        document_issue = str(_exc)
    mo.vstack([mo.callout(document_issue, kind='info') if document_issue else mo.callout('Documents read locally. Check these are your permitted texts.', kind='success'),
               mo.ui.table(documents, selection=None) if documents else mo.md('Add your documents; there is no hidden default corpus.')])
    return documents, document_issue


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## 2. Select the reranked evidence (7 min)
    `rows` is a list of candidate dictionaries with `id`, `text`, `source`, `cosine`
    and `rerank_logit`. The supplied reranker scores every candidate. TODO 1 must
    order by `rerank_logit` (higher first) and return the first `keep` records,
    or all records when fewer are available. Keep IDs/text unchanged; do not use
    cosine for this second-stage ordering. About 2 lines of Python.
    """)
    return


@app.cell
def _():
    def select_evidence(rows, keep):
        # TODO 1: order candidate records by rerank_logit, then keep the requested count.
        selected = None
        # END TODO 1
        return selected
    return (select_evidence,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## 3. Build traceable context (7 min)
    TODO 2 receives selected records and returns ONE string. Include each passage
    unchanged and prefix it with its exact ID inside square brackets: `[chunk ID]`.
    Separate passages with newlines. About 1–3 lines. This labels evidence for the
    generator; it does not ensure that the model cites the right source.
    This task is independent: you can test it before completing TODO 1.
    """)
    return


@app.cell
def _():
    def build_context(selected):
        # TODO 2: combine every [id] label with its unchanged passage text.
        context = None
        # END TODO 2
        return context
    return (build_context,)


@app.cell(hide_code=True)
def _(build_context, mo, select_evidence, validate_context, validate_selection):
    _probe = [dict(id='shape-check:0-1', text='A shape-check passage.', rerank_logit=0.0, cosine=0.0, source='shape-check')]
    selection_ready = False
    context_ready = False
    try:
        selection_ready, _selection_message = validate_selection(_probe, select_evidence(_probe, 2), 2)
    except Exception as _exc:
        _selection_message = f'TODO 1: {_exc}'
    try:
        context_ready, _context_message = validate_context(_probe, build_context(_probe))
    except Exception as _exc:
        _context_message = f'TODO 2: {_exc}'
    mo.vstack([mo.callout(_selection_message, kind='success' if selection_ready else 'info'),
               mo.callout(_context_message, kind='success' if context_ready else 'info')])
    return context_ready, selection_ready


@app.cell(hide_code=True)
def _(mo):
    run_rag = mo.ui.run_button(label="Run baseline + changed chunks for all three questions (6 real answers)")
    mo.vstack([mo.md('## 4. Run and compare (13 min)\nUse the same documents, questions, models, overlap, candidate count (5) and selected count (2). Only chunk size changes: 80 → your selection. Inspect vector order AND reranker order. Model calls run only on this button and may take a minute. After any edit, press Run again to obtain new measured results.'), run_rag])
    return (run_rag,)


@app.cell(hide_code=True)
def _(answer, build_context, changed_size, chunk_documents, context_ready, documents, mo, questions, rerank, retrieve, run_rag, select_evidence, selection_ready, validate_context, validate_selection):
    records = []
    run_issue = ''
    if run_rag.value:
        if not documents or not all(q.strip() for q in questions.value):
            run_issue = 'Provide your documents and all three questions first.'
        elif not selection_ready or not context_ready:
            run_issue = 'Complete both TODOs before generating; both tasks remain independently editable.'
        else:
            for _variant, _size in [('baseline',80),('changed',changed_size.value)]:
                _chunks = chunk_documents(documents, _size, 20)
                for _i, _question in enumerate(questions.value):
                    try:
                        _retrieved = retrieve(_chunks, _question, candidates=5)
                        _ranked = rerank(_question, _retrieved)
                        _selected = select_evidence(_ranked, 2)
                        _ok, _message = validate_selection(_ranked, _selected, 2)
                        if not _ok:
                            raise ValueError(_message)
                        _context = build_context(_selected)
                        _ok, _message = validate_context(_selected, _context)
                        if not _ok:
                            raise ValueError(_message)
                        _generated = answer(_question, _context)
                        records.append(dict(variant=_variant, question_number=_i+1, question=_question,
                                            intended_absent=(_i==2), chunk_size_words=_size, overlap_words=20,
                                            candidates=5, keep=2, chunk_count=len(_chunks), chunks=_chunks,
                                            vector_ranking=_retrieved, reranked=_ranked, selected=_selected,
                                            context=_context, generation=_generated))
                    except Exception as _exc:
                        records.append(dict(variant=_variant,question_number=_i+1,question=_question,error=str(_exc)))
    mo.callout(run_issue, kind='info') if run_issue else mo.md('Results appear below after a run.' if not records else 'Read the measured records below. Scores and text are raw; failed answers are never replaced.')
    return (records,)


@app.cell(hide_code=True)
def _(mo, records):
    mo.vstack([mo.accordion({f"{r['variant']} / Q{r['question_number']}": mo.vstack([
        mo.md(f"**Question:** {r['question']}\n\n**Raw answer:** {r.get('generation',{}).get('text',r.get('error',''))}"),
        mo.md('Vector ranking: cosine high first; reranker: raw logits high first. The scales are different.'),
        mo.ui.table(r.get('vector_ranking',[]), selection=None),
        mo.ui.table(r.get('reranked',[]), selection=None),
        mo.md('**Selected evidence**'),mo.ui.table(r.get('selected',[]), selection=None)]) for r in records}),
        mo.md('No result yet: complete the TODOs and use Run.') if not records else mo.md('Compare source IDs, boundaries, rankings and answers between the two chunk settings.')])
    return


@app.cell(hide_code=True)
def _(mo):
    judgments = mo.ui.array([mo.ui.text_area(label=f"{v} / Q{i}: supported / unsupported / uncertain? Does each citation exist and support its claim? Quote source words. For Q3 verify absence across ALL original documents.", full_width=True, debounce=False) for v in ['baseline','changed'] for i in [1,2,3]])
    findings = mo.ui.text_area(label="Explain one retrieval change, one generation failure (or limitation), and what you would fix next. Did the absent-answer request abstain or invent?", full_width=True, debounce=False)
    mo.vstack([mo.md('## 5. Check and explain (8 min)\nA high cosine is not evidence that the answer exists. Reranking cannot recover a chunk absent from the candidates. Check Q3 in the original documents, not just top results. Keep failed outputs and explain retrieval versus generation failure.'),judgments,findings])
    return findings, judgments


@app.cell(hide_code=True)
def _(EMBED_MODEL, EMBED_REVISION, RERANK_MODEL, RERANK_REVISION, changed_size, documents, findings, json, judgments, mo, prediction, questions, records):
    _export = dict(format='edv-mini-rag-v1', embedding_model=EMBED_MODEL,embedding_revision=EMBED_REVISION,
                   rerank_model=RERANK_MODEL,rerank_revision=RERANK_REVISION,documents=documents,
                   questions=questions.value,prediction=prediction.value,changed_chunk_words=changed_size.value,
                   records=[dict(r,manual_judgment=j) for r,j in zip(records,judgments.value)], findings=findings.value)
    mo.vstack([mo.md('## 6. Save and hand off (2 min)\nSave Python, then download results to preserve widget values. Share three baseline question/answer/source records, the absent-answer finding and the controlled comparison. The export keeps both configurations and full source text for Block 4 evaluation. Inspect it before sharing; store it locally. Return to slide 33.'),
        mo.download(json.dumps(_export,indent=2).encode(),filename='results-day2-block2.json',label='Download questions, sources, rankings, raw answers and findings'),
        mo.accordion({'Hints and recovery':mo.md('Ordering and limiting a list are separate operations. Keep whole dictionaries, not just scores. Build one string, not a list. Python word counts differ from model tokens; shorten a text if context overflows. Missing model files: repeat online preflight. A failed call leaves an error record; it is not a measured answer. Export after reviewing the current run: changing settings clears reactive results. Smaller chunks need not improve relevance. Restart the launcher after saving; download preserves observations separately.')}),
        mo.md('Sources: [RAG paper](https://arxiv.org/abs/2005.11401), [Chroma](https://docs.trychroma.com/docs/collections/add-data), [embedding card](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2), [cross-encoder](https://huggingface.co/cross-encoder/ms-marco-TinyBERT-L2-v2).')])
    return


if __name__ == '__main__':
    app.run()
