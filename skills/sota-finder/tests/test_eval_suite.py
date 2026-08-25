import json
import unittest
from collections import Counter
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
EVALS_PATH = SKILL_ROOT / "evals" / "evals.json"
PLAN_PATH = SKILL_ROOT / "evals" / "evaluation-plan.md"

EXPECTED_CATEGORIES = {
    "routing-input",
    "scope-comparability",
    "evidence-integrity",
    "discovery-coverage",
    "robustness-aminer",
    "artifact-delivery",
}
EXPECTED_MODES = {"live_web", "offline_fixture", "behavioral", "aminer_optional"}
REQUIRED_CASE_FIELDS = {
    "id",
    "name",
    "category",
    "mode",
    "difficulty",
    "prompt",
    "expected_output",
    "files",
    "expectations",
    "failure_conditions",
    "tags",
}


class EvalSuiteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(EVALS_PATH.read_text(encoding="utf-8"))
        cls.cases = cls.data["evals"]

    def test_suite_has_exactly_30_unique_sequential_cases(self):
        ids = [case["id"] for case in self.cases]
        self.assertEqual(self.data["case_count"], 30)
        self.assertEqual(len(self.cases), 30)
        self.assertEqual(sorted(ids), list(range(1, 31)))
        self.assertEqual(len(ids), len(set(ids)))

    def test_declared_categories_modes_and_must_pass_ids_are_consistent(self):
        categories = Counter(case["category"] for case in self.cases)
        modes = Counter(case["mode"] for case in self.cases)
        case_ids = {case["id"] for case in self.cases}
        tagged_must_pass = {
            case["id"] for case in self.cases if "must-pass" in case["tags"]
        }

        self.assertEqual(set(self.data["categories"]), EXPECTED_CATEGORIES)
        self.assertEqual(set(categories), EXPECTED_CATEGORIES)
        self.assertTrue(all(count >= 4 for count in categories.values()))
        self.assertEqual(set(self.data["modes"]), EXPECTED_MODES)
        self.assertEqual(set(modes), EXPECTED_MODES)
        self.assertTrue(set(self.data["must_pass_ids"]).issubset(case_ids))
        self.assertEqual(set(self.data["must_pass_ids"]), tagged_must_pass)

    def test_every_case_has_an_actionable_rubric(self):
        allowed_difficulty = {"basic", "intermediate", "adversarial"}
        for case in self.cases:
            with self.subTest(case_id=case["id"]):
                self.assertTrue(REQUIRED_CASE_FIELDS.issubset(case))
                self.assertIn(case["category"], EXPECTED_CATEGORIES)
                self.assertIn(case["mode"], EXPECTED_MODES)
                self.assertIn(case["difficulty"], allowed_difficulty)
                self.assertGreaterEqual(len(case["prompt"].strip()), 20)
                self.assertGreaterEqual(len(case["expected_output"].strip()), 20)
                self.assertGreaterEqual(len(case["expectations"]), 4)
                self.assertGreaterEqual(len(case["failure_conditions"]), 2)
                self.assertEqual(len(case["expectations"]), len(set(case["expectations"])))
                self.assertEqual(
                    len(case["failure_conditions"]),
                    len(set(case["failure_conditions"])),
                )
                self.assertTrue(case["tags"])

    def test_all_fixture_references_are_local_existing_and_parseable(self):
        referenced = set()
        for case in self.cases:
            for relative in case["files"]:
                with self.subTest(case_id=case["id"], file=relative):
                    path = (SKILL_ROOT / relative).resolve()
                    self.assertTrue(path.is_relative_to(SKILL_ROOT.resolve()))
                    self.assertTrue(path.is_file())
                    self.assertTrue(relative.startswith("evals/fixtures/"))
                    referenced.add(path)
                    if path.suffix == ".json":
                        json.loads(path.read_text(encoding="utf-8"))

        fixture_dir = SKILL_ROOT / "evals" / "fixtures"
        available = {path.resolve() for path in fixture_dir.iterdir() if path.is_file()}
        self.assertEqual(referenced, available)
        self.assertGreaterEqual(len(referenced), 4)

    def test_suite_covers_key_product_contracts(self):
        tags = {tag for case in self.cases for tag in case["tags"]}
        prompts = "\n".join(case["prompt"] for case in self.cases)
        category_modes = {(case["category"], case["mode"]) for case in self.cases}

        self.assertRegex(prompts, r"[\u4e00-\u9fff]")
        self.assertRegex(prompts, r"[A-Za-z]")
        self.assertTrue(
            {
                "official-source",
                "no-official-benchmark",
                "closed-source",
                "split",
                "metric-direction",
                "aggregator",
                "conflict",
                "source-registry",
                "latest",
                "multilingual",
                "aminer-optional",
                "cost-guardrail",
                "overwrite",
                "html",
                "localization",
                "machine-contract",
            }.issubset(tags)
        )
        self.assertIn(("routing-input", "live_web"), category_modes)
        self.assertIn(("scope-comparability", "offline_fixture"), category_modes)
        self.assertIn(("robustness-aminer", "aminer_optional"), category_modes)
        self.assertIn(("artifact-delivery", "offline_fixture"), category_modes)

    def test_evaluation_plan_documents_execution_and_scoring(self):
        text = PLAN_PATH.read_text(encoding="utf-8")
        for marker in (
            "30 cases",
            "offline_fixture",
            "behavioral",
            "live_web",
            "aminer_optional",
            "Must-pass status",
            "Live-web drift policy",
            "suite-level hard failures",
            "tests/test_eval_suite.py",
        ):
            self.assertIn(marker, text)
        for case in self.cases:
            self.assertIn(f"| {case['id']:02d} |", text)


if __name__ == "__main__":
    unittest.main()
