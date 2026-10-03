"""Public checks for setup and the intentionally unfinished student starter."""

import ast
import importlib.util
import unittest
from unittest.mock import patch

from llm_exercises.block1 import ROOT, check_budget, check_inspect, load_tokenizer

NOTEBOOK = ROOT / "exercises" / "block-01-tokenization-context" / "01_tokenization_context.py"


def student_function(name):
    tree = ast.parse(NOTEBOOK.read_text(encoding="utf-8"))
    node = next(n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == name)
    node.decorator_list = []
    namespace = {}
    exec(compile(ast.fix_missing_locations(ast.Module(body=[node], type_ignores=[])), str(NOTEBOOK), "exec"), namespace)
    return namespace[name]


class StudentStarterChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tokenizer = load_tokenizer()

    def test_starter_has_friendly_waiting_feedback(self):
        ok, message = check_inspect(student_function("inspect_text"), self.tokenizer)
        self.assertFalse(ok)
        self.assertIn("waiting", message)
        ok, message = check_budget(student_function("context_budget"))
        self.assertFalse(ok)
        self.assertIn("waiting", message)

    def test_feedback_handles_invalid_return_values(self):
        self.assertFalse(check_inspect(lambda *_: 3, self.tokenizer)[0])
        self.assertFalse(check_budget(lambda *_: 3)[0])

    def test_tokenizer_reloads_from_cache_without_network(self):
        import tiktoken.registry

        with patch.dict(tiktoken.registry.ENCODINGS, clear=True):
            with patch("requests.get", side_effect=AssertionError("Unexpected download")):
                fresh = load_tokenizer()
                self.assertEqual(fresh.name, self.tokenizer.name)

    def test_unfinished_notebook_executes_without_cell_errors(self):
        spec = importlib.util.spec_from_file_location("starter_smoke", NOTEBOOK)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        module.app.run()


if __name__ == "__main__":
    unittest.main()
