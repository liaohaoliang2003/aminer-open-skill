import copy
import importlib.util
import json
import sys
import tempfile
import unittest
from unittest import mock
from pathlib import Path

from openpyxl import load_workbook

SKILL_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = SKILL_ROOT / "scripts" / "build_outputs.py"
SPEC = importlib.util.spec_from_file_location("sota_finder_build_outputs", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)
FIXTURE = SKILL_ROOT / "tests" / "fixtures" / "sample_research.json"


class BuildOutputsTests(unittest.TestCase):
    def raw_fixture(self):
        return json.loads(FIXTURE.read_text(encoding="utf-8"))

    def test_normalization_is_stable_and_respects_direction_and_ties(self):
        first = MODULE.normalize_bundle(self.raw_fixture())
        second = MODULE.normalize_bundle(self.raw_fixture())
        self.assertEqual(
            [(claim["claim_id"], claim["scope_id"], claim["rank"]) for claim in first["claims"]],
            [(claim["claim_id"], claim["scope_id"], claim["rank"]) for claim in second["claims"]],
        )
        quality = next(scope for scope in first["scopes"] if scope["name"] == "Standard quality track")
        quality_main = [claim for claim in first["claims"] if claim["scope_id"] == quality["scope_id"] and claim["section"] == "main"]
        self.assertEqual([claim["rank"] for claim in quality_main], [1, 1])
        self.assertTrue(all(claim["sota"] for claim in quality_main))

        latency = next(scope for scope in first["scopes"] if scope["name"] == "Standard latency track")
        latency_main = [claim for claim in first["claims"] if claim["scope_id"] == latency["scope_id"] and claim["section"] == "main"]
        self.assertEqual([claim["method"] for claim in latency_main], ["Method B", "Method A"])
        self.assertEqual([claim["rank"] for claim in latency_main], [1, 2])

        reference = [claim for claim in first["claims"] if claim["section"] == "reference"]
        self.assertTrue(reference)
        self.assertTrue(all(claim["rank"] is None and not claim["sota"] for claim in reference))
        method_a = next(claim for claim in first["claims"] if claim["method"] == "Method A" and claim["scope_id"] == quality["scope_id"])
        self.assertTrue(method_a["evidence_locators"][0]["source_id"].startswith("src-"))
        self.assertNotIn("source_key", method_a["evidence_locators"][0])

    def test_builds_exact_four_artifacts_and_multiscope_workbook(self):
        data = MODULE.normalize_bundle(self.raw_fixture())
        with tempfile.TemporaryDirectory() as tmp:
            output = MODULE.build_artifacts(data, output_root=Path(tmp))
            self.assertEqual({path.name for path in output.iterdir()}, set(MODULE.DEFAULT_ARTIFACTS))
            evidence = json.loads((output / "evidence.json").read_text(encoding="utf-8"))
            self.assertEqual(evidence["schema_version"], MODULE.SCHEMA_VERSION)
            self.assertEqual(len(evidence["scopes"]), 2)
            self.assertTrue(all(claim["claim_id"].startswith("clm-") for claim in evidence["claims"]))

            workbook = load_workbook(output / "leaderboards.xlsx", read_only=False, data_only=True)
            self.assertEqual(workbook.sheetnames[0], "Index")
            self.assertIn("Standard quality track", workbook.sheetnames)
            self.assertIn("Standard latency track", workbook.sheetnames)
            quality = workbook["Standard quality track"]
            headers = [cell.value for cell in quality[1]]
            self.assertIn("Claim ID", headers)
            self.assertIn("Evidence Source IDs", headers)
            self.assertEqual(quality.freeze_panes, "A2")

            html_text = (output / "full-report.html").read_text(encoding="utf-8")
            self.assertNotIn("cdn.", html_text.lower())
            self.assertIn("Method A", html_text)
            self.assertIn("claim ID", html_text)

    def test_existing_bundle_is_not_overwritten(self):
        data = MODULE.normalize_bundle(self.raw_fixture())
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            first = MODULE.build_artifacts(data, output_root=root)
            sentinel = (first / "evidence.json").read_text(encoding="utf-8")
            second = MODULE.build_artifacts(data, output_root=root)
            self.assertNotEqual(first, second)
            self.assertEqual(second.name, f"{first.name}-2")
            self.assertEqual((first / "evidence.json").read_text(encoding="utf-8"), sentinel)

    def test_explicit_empty_output_directory_is_reused_without_overwrite(self):
        data = MODULE.normalize_bundle(self.raw_fixture())
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "custom-run"
            target.mkdir()
            (target / "keep.txt").write_text("preserve", encoding="utf-8")
            output = MODULE.build_artifacts(data, output_dir=target)
            self.assertEqual(output, target)
            self.assertEqual((target / "keep.txt").read_text(encoding="utf-8"), "preserve")
            self.assertTrue(all((target / name).exists() for name in MODULE.DEFAULT_ARTIFACTS))

    def test_artifact_failure_leaves_no_partial_bundle(self):
        data = MODULE.normalize_bundle(self.raw_fixture())
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with mock.patch.object(MODULE, "render_workbook", side_effect=RuntimeError("synthetic failure")):
                with self.assertRaisesRegex(RuntimeError, "synthetic failure"):
                    MODULE.build_artifacts(data, output_root=root)
            target = root / data["research_run"]["topic_slug"]
            self.assertFalse(target.exists())
            self.assertFalse(any(root.glob(".sota-finder-*")))

    def test_invalid_calendar_date_is_rejected(self):
        raw = self.raw_fixture()
        raw["research_run"]["evidence_checked_through"] = "2026-02-31"
        with self.assertRaisesRegex(MODULE.ContractError, "valid calendar date"):
            MODULE.normalize_bundle(raw)

    def test_main_claim_requires_authoritative_evidence(self):
        raw = self.raw_fixture()
        raw["claims"][0]["evidence_source_keys"] = ["aggregator"]
        with self.assertRaisesRegex(MODULE.ContractError, "requires official, primary, or author evidence"):
            MODULE.normalize_bundle(raw)

    def test_unknown_cross_reference_is_rejected(self):
        raw = self.raw_fixture()
        raw["claims"][0]["evidence_source_keys"] = ["missing-source"]
        with self.assertRaisesRegex(MODULE.ContractError, "Unknown source reference"):
            MODULE.normalize_bundle(raw)

    def test_chinese_visible_reports_keep_machine_ids(self):
        raw = self.raw_fixture()
        raw["research_run"]["language"] = "zh-CN"
        data = MODULE.normalize_bundle(raw)
        with tempfile.TemporaryDirectory() as tmp:
            output = MODULE.build_artifacts(data, output_root=Path(tmp))
            self.assertRegex(output.name, r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
            brief = (output / "brief-report.md").read_text(encoding="utf-8")
            self.assertIn("主排行榜", brief)
            evidence = json.loads((output / "evidence.json").read_text(encoding="utf-8"))
            self.assertTrue(evidence["claims"][0]["claim_id"].startswith("clm-"))


if __name__ == "__main__":
    unittest.main()
