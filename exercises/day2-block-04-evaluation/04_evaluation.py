import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="Evaluation · Day 2 Block 4")


@app.cell(hide_code=True)
def _():
    import json
    import sys
    from pathlib import Path
    import marimo as mo
    sys.path.insert(0, str(next(p for p in Path(__file__).resolve().parents if (p / 'llm_exercises').is_dir())))
    from llm_exercises.evaluation import cases, normalize, load_rag, score_rows, aggregate, run_judge, RUBRIC

    return RUBRIC, aggregate, cases, json, load_rag, mo, run_judge, score_rows


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Your 30-minute investigation

    **Act as the release reviewers for your own Mini-RAG: use measured evidence to decide which version, if either, deserves another test.**

    ### Remember from the slides
    Correctness, format and retrieval measure different things. Recall@k divides unique relevant IDs found by all relevant IDs; an empty relevant set is undefined. A judge is another fallible measurement. Previously inspected cases are retrospective.

    **0–5 · Challenge a score**
    Agree what would make you prefer one configuration. On one fixture, calculate exact match, schema validity and Recall@2 by hand before running code. State every denominator; predict what k=3 can change. Fixtures are authored calibration cases, not evidence that a model performs well.

    **5–12 · Build and cross-check**
    Complete the single scoring TODO. Compare paired fixture configurations at k=2 and reconcile your manual case. Rescore at k=3 without regenerating answers. Explain why retrieval can change while saved-answer correctness and format remain fixed.

    **12–24 · Audit your actual assistant**
    Switch to your own Block 2 export, using original-document references and per-variant relevant IDs. Keep its evaluation-design label honest. Swap editor/checker at minute 15. One partner independently rates a chosen case from source evidence; then run the real model judge and compare its raw rating/schema. Record agreement, disagreement or unavailable/invalid judgment honestly.

    **24–27 · Make a release decision**
    Inspect one consequential failed or ambiguous case. Choose a configuration conditionally, or reject both. Name which metric supports the choice, one tradeoff, and a fresh held-out question that could reverse the decision. The checking partner challenges the claim using the original source.

    **27–30 · Save an auditable report**
    Export the per-case/aggregate report, manual check, k comparison, source-versus-judge evidence and decision. Save code; both partners must explain what the report cannot establish.

    **Bring back:** Manual score check, per-case and aggregate report, saved-answer k comparison, own-document human/judge comparison and a conditional release decision with a fresh test.

    **Limit:** A few convenient records cannot certify an application. Exact match can reject a correct paraphrase; free-text answers may fail an irrelevant JSON contract. Choose metrics for the task and keep technical judge failures separate from agreement.

    Swap editor/checker at minute 15; keep this task open. Full preparation/help: this block’s `GROUP_TASK.md`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # Measure, inspect, decide
    **Day 2 Block 4 · launch slide 64 · 30-minute investigation immediately after the concepts.**
    Predict → implement one small scoring TODO → compare paired cases → inspect a
    real judge → check against source evidence → export findings. The supplied paired
    fixtures are authored examples, not measured model outputs. Use your Block 2
    export as well: labels must come from original documents, not generated answers.
    Saving Python does not save widget values: download the report before leaving.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mode = mo.ui.dropdown(options=['Teaching fixtures','Own Mini-RAG export'], value='Teaching fixtures', label='Dataset')
    design = mo.ui.dropdown(options={'Already inspected: retrospective diagnostics':'retrospective',
        'Reserved before both runs; no tuning on test questions':'reserved_before_runs'},
        value='Already inspected: retrospective diagnostics', label='Own-record evaluation design')
    path = mo.ui.text(label='Local path to results-day2-block2.json', full_width=True)
    labels = mo.ui.text_area(label='Ground truth JSON: question number → split, reference, relevant_ids by variant', full_width=True, debounce=False, value='{"1":{"split":"dev","reference":"REPLACE","relevant_ids":{"baseline":[],"changed":[]}},"2":{"split":"test","reference":"REPLACE","relevant_ids":{"baseline":[],"changed":[]}},"3":{"split":"test","reference":"UNKNOWN","relevant_ids":{"baseline":[],"changed":[]}}}')
    k = mo.ui.slider(1, 3, value=2, label='Recall@k (reranked candidate list)')
    prediction = mo.ui.text_area(label='Predict a metric tradeoff and freeze a hypothesis before test results.', full_width=True)
    mo.vstack([mode,design,path,labels,k,prediction,mo.md('**Before rooms open:** prepare the own-document reference and ALL relevant chunks separately for each chunk configuration. Empty relevant_ids means no answer exists; check the entire corpus. A test label does not make previously inspected questions held out. Claim held-out evidence only when questions 2/3 were reserved before both Block 2 runs, configurations were frozen, and no tuning used those answers. Otherwise keep retrospective diagnostics and propose fresh questions. Fixtures simulate two dev and four test cases with authored outputs. Changing k rescores saved rankings; it does not rerun generation.')])
    return design, k, labels, mode, path, prediction


@app.cell(hide_code=True)
def _(cases, design, labels, load_rag, mo, mode, path):
    rows = []
    data_issue = ''
    try:
        rows = cases() if mode.value == 'Teaching fixtures' else load_rag(path.value,labels.value,design.value)
    except Exception as _exc:
        data_issue = str(_exc)
    mo.callout(data_issue,kind='warn') if data_issue else mo.ui.table(rows,selection=None)
    return (rows,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## One scoring TODO
    Inputs are answer/reference strings, ordered retrieved IDs, relevant IDs and k.
    Return `{"exact_match": bool, "recall": float or None}`. Use the supplied
    `normalize` policy on both strings. Recall is the fraction of unique relevant
    IDs found in the first k results. Repeated IDs count once. No relevant IDs →
    recall is `None`, not 1. About 3–5 lines; change only the marked region.
    """)
    return


@app.function
def score_case(answer, reference, ranked_ids, relevant_ids, k):
    # TODO: normalized exact match and set-based Recall@k.
    result = None
    # END TODO
    return result


@app.cell(hide_code=True)
def _(aggregate, k, mo, rows, score_rows):
    scored, score_issue = score_rows(rows,score_case,k.value)
    summary = aggregate(scored)
    mo.vstack([mo.callout(score_issue,kind='info') if score_issue else mo.md('## Paired comparison '),
        mo.ui.table(summary,selection=None),mo.ui.table(scored,selection=None),
        mo.md('Inspect a case where correctness and schema differ. Then switch to your own export and keep failures. Test results describe these cases only; do not tune repeatedly on them. Free-text Mini-RAG output usually fails this JSON contract; decide whether the application actually needs JSON. Exact match can reject a correct paraphrase.')])
    return scored, summary


@app.cell(hide_code=True)
def _(RUBRIC, mo, rows):
    judge_case = mo.ui.dropdown(options={f"{r['configuration']} / {r['id']}":i for i,r in enumerate(rows)}, label='Case to judge')
    judge_run = mo.ui.run_button(label='Run actual local judge (optional model group required)')
    human_score = mo.ui.dropdown(options={'0 wrong/unsupported':0,'1 partly correct':1,'2 correct/complete/supported':2},value='0 wrong/unsupported',label='Your independent source-based rating')
    disagreement = mo.ui.text_area(label='Quote source evidence. Where does the judge disagree or fail its schema? What would you fix?',full_width=True)
    mo.vstack([mo.md('## Judge and human calibration \nRate independently before pressing Run. The small local model can produce a wrong rating or invalid JSON. Keep its raw output; a missing rating is a judge failure, not agreement.'),mo.md(RUBRIC),judge_case,human_score,judge_run,disagreement])
    return disagreement, human_score, judge_case, judge_run


@app.cell(hide_code=True)
def _(judge_case, judge_run, mo, rows, run_judge):
    judge = None
    if judge_run.value and judge_case.value is not None:
        try:
            judge = run_judge(rows[judge_case.value])
        except Exception as _exc:
            judge = dict(issue=f'Judge unavailable: {_exc}. Use README model preflight; automatic metrics still work.')
    mo.accordion({'Raw judge evidence':mo.md(f'```json\n{__import__("json").dumps(judge,indent=2)}\n```')}) if judge else mo.md('Judge has not run. No generated score is supplied by the fixtures.')
    return (judge,)


@app.cell(hide_code=True)
def _(mo):
    decision = mo.ui.text_area(label='Configuration choice, metric tradeoff, sample limitation, next held-out test.',full_width=True)
    mo.vstack([mo.md('## Decide and save \nExport per-case/aggregate scores, your own-document records, judge evidence and the reason for your choice. If no numeric disagreement occurred, record agreement honestly and inspect a judge schema failure or another case. Return to the plenary findings review on slide 65.'),decision])
    return (decision,)


@app.cell(hide_code=True)
def _(
    decision,
    disagreement,
    human_score,
    json,
    judge,
    k,
    mo,
    prediction,
    scored,
    summary,
):
    report = dict(format='edv-evaluation-v1',normalization='casefold + whitespace collapse',k=k.value,
                  prediction=prediction.value,scored=scored,summary=summary,judge=judge,
                  human_rating=human_score.value,disagreement=disagreement.value,decision=decision.value)
    mo.download(json.dumps(report,indent=2).encode(),filename='evaluation-day2-block4.json',label='Download evaluation report')
    return


if __name__ == "__main__":
    app.run()
