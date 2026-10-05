"""Public setup/starter checks; no student implementation or solved fixture."""
import tempfile
import unittest
from pathlib import Path
from llm_exercises.rag import read_documents, chunk_documents, validate_selection, validate_context


class RagSetupTests(unittest.TestCase):
    def test_ingestion_and_metadata(self):
        with tempfile.TemporaryDirectory() as folder:
            Path(folder,'own.txt').write_text('My own short test document.',encoding='utf-8')
            Path(folder,'ignored.csv').write_text('ignored')
            docs=read_documents(folder)
            self.assertEqual(len(docs),1)
            self.assertEqual(docs[0]['source'],'own.txt')
            self.assertEqual(len(docs[0]['sha256']),64)
    def test_empty_and_oversize(self):
        with tempfile.TemporaryDirectory() as folder:
            with self.assertRaises(ValueError):read_documents(folder)
            Path(folder,'big.md').write_text('x'*20001)
            with self.assertRaises(ValueError):read_documents(folder)
    def test_chunk_edges(self):
        doc=dict(source='own',text=' '.join(map(str,range(180))),sha256='test')
        chunks=chunk_documents([doc],80,20)
        self.assertEqual([(r['start'],r['end']) for r in chunks],[(0,80),(60,140),(120,180)])
        self.assertEqual(chunk_documents([dict(doc,text='')]),[])
        for size,overlap in [(0,0),(5,5),(5,-1)]:
            with self.assertRaises(ValueError):chunk_documents([doc],size,overlap)
    def test_waiting_feedback(self):
        self.assertFalse(validate_selection([],None,2)[0])
        self.assertFalse(validate_context([],None)[0])
    def test_starter_is_unfinished(self):
        text=(Path(__file__).resolve().parents[1]/'exercises/day2-block-02-rag/02_mini_rag.py').read_text()
        self.assertIn('selected = None',text)
        self.assertIn('context = None',text)
        self.assertNotIn('instructor/',text)

if __name__=='__main__':unittest.main()

class RagStarterExecutionTests(unittest.TestCase):
    def test_untouched_starter_waits_without_models(self):
        import importlib.util
        from unittest.mock import patch
        path=Path(__file__).resolve().parents[1]/'exercises/day2-block-02-rag/02_mini_rag.py'
        spec=importlib.util.spec_from_file_location('rag_starter',path)
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        with patch('llm_exercises.rag.answer',side_effect=AssertionError('No automatic model call')):
            _,definitions=module.app.run()
        self.assertFalse(definitions['selection_ready'])
        self.assertFalse(definitions['context_ready'])
        self.assertEqual(definitions['records'],[])
    def test_selection_launches_day2_rag(self):
        from unittest.mock import patch
        import sys,start
        with patch.object(sys,'argv',['start.py','--block','d2-2','--offline-models']), patch('llm_exercises.rag.preflight',return_value={'ready':True}) as preflight, patch.object(start.subprocess,'call',return_value=0) as launch:
            self.assertEqual(start.main(),0)
        preflight.assert_called_once_with(online=False)
        self.assertIn('day2-block-02-rag',launch.call_args.args[0][4])
