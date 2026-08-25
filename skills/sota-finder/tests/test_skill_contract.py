import json
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]


class SkillContractTests(unittest.TestCase):
    def test_required_skill_and_output_contract_are_present(self):
        skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(skill.startswith("---\nname: sota-finder\n"))
        self.assertNotIn("[TODO", skill)
        for name in ("brief-report.md", "full-report.html", "leaderboards.xlsx", "evidence.json"):
            self.assertIn(name, skill)
        self.assertIn("AMiner is optional", skill)
        self.assertIn("CNY 5", skill)
        self.assertIn("Main Leaderboard", skill)
        self.assertIn("Reference Results", skill)
        self.assertIn("Conflicts / Unavailable", skill)

    def test_prototype_is_self_contained_and_portable(self):
        text_files = [
            path
            for path in SKILL_ROOT.rglob("*")
            if path.is_file()
            and "tests" not in path.relative_to(SKILL_ROOT).parts
            and path.suffix in {".md", ".py", ".json", ".yaml", ".txt"}
        ]
        combined = "\n".join(path.read_text(encoding="utf-8") for path in text_files)
        self.assertNotIn("/Users/", combined)
        self.assertNotIn("leaderboard-builder", combined)
        self.assertNotIn("result-table-extraction", combined)
        self.assertNotIn("AMINER_API_KEY\"]", combined)
        self.assertTrue((SKILL_ROOT / "requirements.txt").exists())
        self.assertEqual((SKILL_ROOT / "requirements.txt").read_text(encoding="utf-8").strip(), "openpyxl>=3.1,<4")

    def test_schema_and_evals_are_machine_readable(self):
        schema = json.loads((SKILL_ROOT / "schemas" / "evidence.schema.json").read_text(encoding="utf-8"))
        self.assertEqual(schema["$id"], "urn:aminer-open-skill:sota-finder:evidence:v1")
        self.assertEqual(schema["properties"]["schema_version"]["const"], "sota-finder.evidence.v1")
        self.assertIn("claims", schema["required"])
        self.assertIn("sources", schema["required"])
        self.assertIn("conflicts", schema["required"])

        evals = json.loads((SKILL_ROOT / "evals" / "evals.json").read_text(encoding="utf-8"))
        self.assertEqual(evals["skill_name"], "sota-finder")
        self.assertGreaterEqual(len(evals["evals"]), 10)
        self.assertTrue(all(item.get("expectations") for item in evals["evals"]))

    def test_bilingual_and_progressive_disclosure_files_exist(self):
        required = [
            "SKILL.zh.md",
            "commands/sota-finder.md",
            "references/research-playbook.md",
            "references/data-contract.md",
            "references/output-contract.md",
            "scripts/build_outputs.py",
            "tests/fixtures/sample_research.json",
        ]
        for relative in required:
            self.assertTrue((SKILL_ROOT / relative).exists(), relative)


if __name__ == "__main__":
    unittest.main()
