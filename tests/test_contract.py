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
        cases = json.loads((ROOT / "tests" / "cases" / "activation.json").read_text())
        positives = [case for case in cases if case["should_activate"]]
        negatives = [case for case in cases if not case["should_activate"]]
        self.assertEqual(len(positives), 10)
        self.assertEqual(len(negatives), 10)
        self.assertTrue(all(case.get("reason") for case in cases))

    def test_workflow_matrix_covers_all_paths_and_boundaries(self):
        cases = json.loads((ROOT / "tests" / "cases" / "workflows.json").read_text())
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

        standard = next(
            case for case in cases if case["id"] == "standard-ambiguous-feature"
        )
        self.assertEqual(standard["budget"], {"max_iterations": 5, "max_minutes": 30})
        for key in ("fixture", "hidden_evaluator", "reference_solution"):
            self.assertTrue((ROOT / standard[key]).exists())

    def test_only_one_skill_entrypoint_exists(self):
        entries = sorted((ROOT / "skills").glob("*/SKILL.md"))
        self.assertEqual(entries, [ROOT / "skills" / "gap" / "SKILL.md"])

    def test_baseline_fixtures_are_green(self):
        for fixture_name in ("quick-project", "standard-invitation"):
            with self.subTest(fixture=fixture_name):
                fixture = ROOT / "tests" / "fixtures" / fixture_name
                result = subprocess.run(
                    [
                        sys.executable,
                        "-m",
                        "unittest",
                        "discover",
                        "-s",
                        "tests",
                        "-v",
                    ],
                    cwd=fixture,
                    env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
                    text=True,
                    capture_output=True,
                    check=False,
                )
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_standard_mvp_evaluator_is_red_capable_and_known_good(self):
        evaluator = ROOT / "tests" / "evaluators" / "standard_invitation.py"
        baseline = ROOT / "tests" / "fixtures" / "standard-invitation"
        reference = ROOT / "tests" / "reference-solutions" / "standard-invitation"

        red = subprocess.run(
            [sys.executable, str(evaluator), str(baseline), "-v"],
            cwd=ROOT,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertNotEqual(red.returncode, 0, "baseline must fail the hidden evaluator")

        green = subprocess.run(
            [sys.executable, str(evaluator), str(reference), "-v"],
            cwd=ROOT,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(green.returncode, 0, green.stdout + green.stderr)


if __name__ == "__main__":
    unittest.main()
