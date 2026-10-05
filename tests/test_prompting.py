"""Public shape/starter checks. No completed student prompt implementation."""
import importlib.util
import unittest
from pathlib import Path
from unittest.mock import patch
from llm_exercises.prompting import validate_output, check_template

NOTEBOOK = Path(__file__).resolve().parents[1] / 'exercises/day2-block-01-prompt-engineering/01_prompt_engineering.py'

class PromptingStarterChecks(unittest.TestCase):
    def test_format_boundaries(self):
        self.assertTrue(validate_output('{"study":"sample","participants":0,"weeks":null}')['schema_valid'])
        for raw in ['{}', '[]', '{"study":"","participants":1,"weeks":null}',
                    '{"study":"sample","participants":true,"weeks":null}',
                    '{"study":"sample","participants":-1,"weeks":null}',
                    '{"study":"sample","participants":1,"weeks":null,"extra":0}']:
            self.assertFalse(validate_output(raw)['schema_valid'])
        for raw in ['```json\n{}\n```', '{"study":"a","study":"b"}', '{"weeks":NaN}']:
            self.assertFalse(validate_output(raw)['json_valid'])

    def test_waiting_feedback(self):
        self.assertIn('waiting', check_template(lambda *_: None)[1])
        self.assertFalse(check_template(lambda *_: 'wrong type')[0])

    def test_untouched_starter_never_calls_model(self):
        spec = importlib.util.spec_from_file_location('prompt_starter', NOTEBOOK)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with patch('llm_exercises.prompting.generate', side_effect=AssertionError('Starter must wait for run button')):
            _, definitions = module.app.run()
        self.assertFalse(definitions['template_ok'])
        self.assertIsNone(definitions['build_messages']('source', False, 'policy'))
        self.assertIsNone(definitions['reasoning_prompt']('question', False))

    def test_selection_is_day_qualified(self):
        import start, sys
        with patch.object(sys, 'argv', ['start.py','--block','d2-1','--offline-models']), patch('llm_exercises.prompting.load_model') as load, patch('llm_exercises.prompting.generate', return_value={'output_tokens':1,'seconds':0.1}), patch.object(start.subprocess, 'call', return_value=0) as launch:
            self.assertEqual(start.main(), 0)
            load.assert_called_once_with(online=False)
            self.assertIn(str(NOTEBOOK), launch.call_args.args[0])
