"""Public checks for setup and the intentionally unfinished student starter."""

import ast
import importlib.util
import unittest
from unittest.mock import patch

from llm_exercises.block1 import ROOT, check_merge, check_pairs, load_tokenizer, train_bpe, apply_bpe

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
        ok, message = check_pairs(student_function("count_pairs"))
        self.assertFalse(ok)
        self.assertIn("waiting", message)
        ok, message = check_merge(student_function("merge_pair"))
        self.assertFalse(ok)
        self.assertIn("waiting", message)

    def test_feedback_handles_invalid_return_values(self):
        self.assertFalse(check_pairs(lambda *_: 3)[0])
        self.assertFalse(check_merge(lambda *_: 3)[0])

    def test_feedback_rejects_unweighted_or_empty_results(self):
        self.assertFalse(check_pairs(lambda *_: {})[0])
        self.assertFalse(check_merge(lambda tokens, pair: tokens)[0])

    def test_training_supplies_recounting_and_deterministic_tie_order(self):
        # Stubs exercise orchestration only; neither implements a student TODO.
        calls = []
        def supplied_counts(splits, frequencies):
            calls.append(splits)
            return {("z", "x"): 2, ("a", "b"): 2} if len(calls) == 1 else {}
        result = train_bpe({"z": 1}, supplied_counts, lambda tokens, pair: tokens.copy())
        self.assertEqual(result["merges"], [("a", "b")])
        self.assertEqual(len(calls), 2)

    def test_encoding_uses_rules_without_training_or_accepting_unknown_symbols(self):
        seen = []
        def supplied_merge(tokens, pair):
            seen.append(pair)
            return tokens.copy()
        rules = [("a", "b"), ("b", "c")]
        self.assertEqual(apply_bpe("abc", rules, supplied_merge, "abc"), list("abc"))
        self.assertEqual(seen, rules)
        with self.assertRaises(ValueError):
            apply_bpe("d", rules, supplied_merge, "abc")

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
