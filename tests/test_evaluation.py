"""Public plumbing checks: no solved scoring implementation."""
import json
import importlib.util
from pathlib import Path
from unittest.mock import patch
import unittest
import tempfile
from llm_exercises.evaluation import cases, parse_output, normalize, score_rows, aggregate, run_judge, load_rag, RUBRIC

class EvaluationPlumbing(unittest.TestCase):
    def test_starter_executes_without_inference(self):
        path=Path(__file__).resolve().parents[1]/"exercises/day2-block-04-evaluation/04_evaluation.py"
        spec=importlib.util.spec_from_file_location("evaluation_starter",path)
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        with patch("llm_exercises.evaluation.run_judge",side_effect=AssertionError("Unexpected inference")):
            _,definitions=module.app.run()
        self.assertEqual(definitions["scored"],[])
        self.assertIsNone(definitions["judge"])
        self.assertEqual(definitions["normalize"](' A  B '), 'a b')

    def test_paired_holdout(self):
        rows=cases()
        for split in ['dev','test']:
            groups=[{r['id'] for r in rows if r['configuration']==c and r['split']==split} for c in ['baseline','changed']]
            self.assertEqual(groups[0],groups[1])
        self.assertEqual(len(rows),12)
    def test_schema_rejects_nonobjects_and_duplicate_keys(self):
        for raw in ['8','null','{"answer":"8","sources":[],"extra":1}','{"answer":"8","answer":"9","sources":[]}','{"answer":NaN,"sources":[]}']:
            self.assertFalse(parse_output(raw)['schema_valid'])
        self.assertTrue(parse_output(json.dumps(dict(answer='8',sources=[])))['schema_valid'])
    def test_waiting_starter(self):
        result,message=score_rows(cases(),lambda *args:None,2)
        self.assertEqual(result,[])
        self.assertIn('TODO',message)
    def test_empty_aggregate(self):
        self.assertEqual(aggregate([]),[])
    def test_invalid_student_return_has_actionable_feedback(self):
        scored,message=score_rows(cases(),lambda *args:7,2)
        self.assertEqual(scored,[])
        self.assertIn('exact_match',message)
        def broken(*args):
            raise TypeError('check inputs')
        scored,message=score_rows(cases(),broken,2)
        self.assertEqual(scored,[])
        self.assertIn('TypeError',message)
    def test_declared_normalization(self):
        self.assertEqual(normalize(' A  and B '),'a and b')

    def test_judge_uses_the_recorded_rubric_and_strict_output_contract(self):
        for raw, expected in [
            ('{"score":2,"reason":"Supported."}', 2),
            ('{"score":0,"score":2,"reason":"Duplicated."}', None),
            ('{"score":2,"reason":"Supported.","extra":NaN}', None),
            ('{"score":2,"reason":"Supported.","extra":1}', None),
            ('{"score":true,"reason":"Supported."}', None),
            ('{"score":2,"reason":" "}', None),
        ]:
            with self.subTest(raw=raw), patch('llm_exercises.prompting.generate', return_value={'text':raw}) as generate:
                report = run_judge(cases()[0])
            sent = generate.call_args.args[0]
            self.assertIn(RUBRIC, sent[0]['content'])
            self.assertEqual(report['messages'], sent)
            self.assertEqual(report['rubric'], RUBRIC)
            self.assertEqual(report['rating'], expected)

    def test_import_does_not_promote_a_test_label_to_heldout_evidence(self):
        data = {'format':'edv-mini-rag-v1', 'documents':[{'text':'A synthetic passage.'}],
                'records':[{'question_number':1,'variant':'baseline','question':'A question?',
                            'chunks':[{'id':'doc:0-3'}], 'reranked':[{'id':'doc:0-3'}],
                            'generation':{'text':'A response.'}}]}
        labels = json.dumps({'1':{'split':'test','reference':'A reference.',
                                 'relevant_ids':{'baseline':['doc:0-3']}}})
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)/'export.json'; path.write_text(json.dumps(data))
            rows = load_rag(path, labels)
            self.assertEqual(rows[0]['evaluation_design'], 'retrospective')
            self.assertEqual(rows[0]['original_record'], data['records'][0])
            self.assertEqual(load_rag(path, labels, 'reserved_before_runs')[0]['evaluation_design'], 'reserved_before_runs')
            with self.assertRaises(ValueError):
                load_rag(path, labels, 'heldout_by_filename')

if __name__=='__main__':unittest.main()
