"""Public starter/setup checks; completed student implementations stay ignored."""
import importlib.util
import sys
import unittest
from pathlib import Path
from unittest.mock import patch
from llm_exercises.block4 import check_loss, check_update, loss_plot, softmax

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / 'exercises/block-04-training-alignment/04_next_token_learning.py'


class Block4StarterChecks(unittest.TestCase):
    def test_waiting_and_invalid_return_feedback(self):
        for check in [check_loss, check_update]:
            self.assertIn('waiting', check(lambda *_: None)[1])
            self.assertFalse(check(lambda *_: 'invalid')[0])

    def test_unfinished_notebook_executes(self):
        spec = importlib.util.spec_from_file_location('block4_starter', NOTEBOOK)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        _, definitions = module.app.run()
        self.assertFalse(definitions['loss_ok'])
        self.assertFalse(definitions['update_ok'])
        self.assertIsNone(definitions['run_result'])
        self.assertIsNone(definitions['plot_svg'])

    def test_preflight_and_selection_skip_tokenizer(self):
        import start
        with patch.object(sys, 'argv', ['start.py', '--block', '4', '--check']), patch.object(start, 'load_tokenizer', side_effect=AssertionError('No tokenizer in Block 4')):
            self.assertEqual(start.main(), 0)
        with patch.object(sys, 'argv', ['start.py', '--block', '4', '--port', '2729']), patch.object(start.subprocess, 'call', return_value=0) as launch:
            self.assertEqual(start.main(), 0)
            command = launch.call_args.args[0]
            self.assertIn(str(NOTEBOOK), command)
            self.assertIn('127.0.0.1', command)
            self.assertIn('2729', command)

    def test_supplied_softmax_stability(self):
        self.assertEqual(softmax([1000]*4), [0.25]*4)

    def test_plot_labels_and_escaping(self):
        svg = loss_plot([{'Step': 0, 'Mean loss': 2}, {'Step': 10, 'Mean loss': 1}], '<test>')
        self.assertIn('&lt;test&gt;', svg)
        self.assertIn('nats / target', svg)
        self.assertIn('Update step', svg)
