import json
import os
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from validate import validate_repository  # noqa: E402


class RepositoryContractTests(unittest.TestCase):
    def test_repository_validator(self):
        self.assertEqual(validate_repository(), [])

    def test_validator_cli(self):
        result = subprocess.run(
            [sys.executable, "scripts/validate.py"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("OK — 1 skill", result.stdout)

    def test_activation_matrix_is_balanced(self):
        cases = json.loads((ROOT / "tests" / "activation-cases.json").read_text())
        positives = [case for case in cases if case["should_activate"]]
        negatives = [case for case in cases if not case["should_activate"]]
        self.assertEqual(len(positives), 10)
        self.assertEqual(len(negatives), 10)
        self.assertTrue(all(case.get("reason") for case in cases))

    def test_workflow_matrix_covers_all_paths_and_boundaries(self):
        cases = json.loads((ROOT / "tests" / "workflow-cases.json").read_text())
        paths = {case["expected_path"] for case in cases}
        references = {
            reference
            for case in cases
            for reference in case["required_references"]
        }
        self.assertEqual(paths, {"Quick", "Standard", "Governed"})
        self.assertEqual(
            references,
            {
                "adoption.md",
                "communication.md",
                "delivery.md",
                "discovery.md",
                "governance.md",
                "planning.md",
                "problem-solving.md",
                "retrospective.md",
            },
        )
        for case in cases:
            self.assertTrue(case["observable_invariants"])
            self.assertTrue(case["forbidden_actions"])

    def test_only_one_skill_entrypoint_exists(self):
        entries = sorted((ROOT / "skills").glob("*/SKILL.md"))
        self.assertEqual(entries, [ROOT / "skills" / "gap" / "SKILL.md"])

    def test_sample_fixture_is_green(self):
        fixture = ROOT / "tests" / "fixtures" / "sample-project"
        result = subprocess.run(
            [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
            cwd=fixture,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
