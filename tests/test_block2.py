"""Public setup/starter checks; completed attention calculations remain local."""
import importlib.util
import sys
import unittest
from pathlib import Path
from unittest.mock import patch
from llm_exercises.block2 import Q, K, V, changed_inputs, check_scores, check_softmax, check_values

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / 'exercises/block-02-self-attention/02_self_attention.py'


class Block2StarterChecks(unittest.TestCase):
    def test_unfinished_notebook_executes_without_cell_errors(self):
        spec = importlib.util.spec_from_file_location('block2_starter', NOTEBOOK)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        _, definitions = module.app.run()
        self.assertFalse(definitions['scores_ok'])
        self.assertFalse(definitions['weights_ok'])
        self.assertFalse(definitions['values_ok'])
        self.assertEqual(definitions['baseline'], {'scores': None, 'weights': None, 'outputs': None})

    def test_waiting_and_malformed_feedback(self):
        for check in [check_scores, check_softmax, check_values]:
            self.assertIn('waiting', check(lambda *_: None)[1])
            self.assertFalse(check(lambda *_: 3)[0])

    def test_controlled_change_preserves_baseline_and_other_entries(self):
        sources = {'Q': Q, 'K': K, 'V': V}
        for target in sources:
            changed = dict(zip(sources, changed_inputs(target, 1, 0, 0.5)))
            for name in sources:
                for i in range(3):
                    for j in range(2):
                        difference = changed[name][i][j] - sources[name][i][j]
                        self.assertEqual(difference, 0.5 if (name, i, j) == (target, 1, 0) else 0)
            self.assertEqual(changed_inputs(target, 1, 0, 0), (Q,K,V))

    def test_selection_check_and_launch_skip_tokenizer(self):
        import start
        with patch.object(start, 'load_tokenizer', side_effect=AssertionError('No Block 2 tokenizer')), patch.object(start.subprocess, 'call', return_value=0) as launch:
            with patch.object(sys, 'argv', ['start.py', '--block', '2', '--check']):
                self.assertEqual(start.main(), 0)
                launch.assert_not_called()
            with patch.object(sys, 'argv', ['start.py', '--block', '2', '--port', '2731']):
                self.assertEqual(start.main(), 0)
                self.assertIn(str(NOTEBOOK), launch.call_args.args[0])
                self.assertIn('2731', launch.call_args.args[0])
