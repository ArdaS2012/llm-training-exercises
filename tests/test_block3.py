"""Public infrastructure checks only; no completed student implementations."""
import ast
import importlib.util
import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import patch
from llm_exercises.block3 import check_mask, check_temperature, check_top_k, heatmap_svg

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / 'exercises/block-03-transformer-architecture/03_masking_sampling.py'


class Block3StarterChecks(unittest.TestCase):
    def test_waiting_and_malformed_feedback(self):
        for check in [check_mask, check_temperature, check_top_k]:
            self.assertIn('waiting', check(lambda *_: None)[1])
            self.assertFalse(check(lambda *_: 3)[0])

    def test_unfinished_notebook_executes(self):
        spec = importlib.util.spec_from_file_location('block3_starter', NOTEBOOK)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        _, definitions = module.app.run()
        self.assertFalse(definitions['mask_ok'])
        self.assertFalse(definitions['temperature_ok'])
        self.assertFalse(definitions['top_k_ok'])
        self.assertEqual(definitions['sample_rows'], [])

    def test_selection_preflight_skips_tokenizer(self):
        import start
        with patch.object(sys, 'argv', ['start.py', '--block', '3', '--check']), patch.object(start, 'load_tokenizer', side_effect=AssertionError('Block 3 must not load tokenizer')):
            self.assertEqual(start.main(), 0)

    def test_selection_launches_correct_notebook(self):
        import start
        with patch.object(sys, 'argv', ['start.py', '--block', '3', '--port', '2729']), patch.object(start.subprocess, 'call', return_value=0) as launch:
            self.assertEqual(start.main(), 0)
            command = launch.call_args.args[0]
            self.assertIn(str(NOTEBOOK), command)
            self.assertIn('2729', command)
            self.assertIn('127.0.0.1', command)

    def test_svg_has_axes_and_escapes_title(self):
        svg = heatmap_svg([[1, 0, 0]]*3, '<test>')
        self.assertIn('Query', svg)
        self.assertIn('Source / Key', svg)
        self.assertIn('&lt;test&gt;', svg)
