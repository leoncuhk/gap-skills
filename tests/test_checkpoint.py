"""Exercise shipped CLI with real files; no model or external calls."""
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HELPER = ROOT / 'skills/gap/scripts/checkpoint.py'


class CheckpointTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='gap-checkpoint-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.state = self.root / 'state.json'
        self.contract = {'purpose': 'Deliver original and actual message count', 'source': 'request.txt',
                         'semantics': ['preserve source bytes', 'events are not messages'],
                         'inputs': ['source.txt'], 'criteria': [
                             {'id': 'output', 'claim': 'original bytes preserved', 'kind': 'artifact'},
                             {'id': 'tests', 'claim': 'semantic checks pass', 'kind': 'check'}]}
        self.write('source.txt', 'original')
        self.write('output.txt', 'original')
        self.write('receipt.txt', 'Actual local comparison: matching original bytes.')
        self.write('contract.json', self.contract)
        self.cli('init', '--contract', str(self.root / 'contract.json'))

    def write(self, path, value):
        (self.root / path).write_text(json.dumps(value) if isinstance(value, (dict, list)) else value)

    def cli(self, *args, expected=0, helper=HELPER):
        result = subprocess.run([sys.executable, str(helper), '--root', str(self.root),
                                 '--state', str(self.state), *args], capture_output=True, text=True)
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        return json.loads(result.stdout)

    def record(self, criterion='output', kind='artifact', result='pass', **kw):
        return self.cli('record', '--criterion', criterion, '--kind', kind, '--result', result,
                        '--by', 'test-context', '--receipt', 'receipt.txt', '--file', 'output.txt',
                        '--note', 'Synthetic local observation', **kw)

    def test_run_ended_is_not_artifact_or_acceptance(self):
        result = self.cli('end', '--reason', 'interrupted')
        self.assertEqual(result['run']['status'], 'ended')
        self.assertFalse(result['artifact_ready'])
        self.assertFalse(result['all_criteria_evidenced'])
        self.assertEqual(result['independent_acceptance'], 'not established')
        self.cli('check', expected=1)

    def test_actual_files_checked_without_rerunning_or_overwriting(self):
        self.record()
        self.record('tests', 'check')
        before = {p.name: p.read_bytes() for p in self.root.iterdir()}
        self.assertTrue(self.cli('check')['all_criteria_evidenced'])
        self.assertEqual(before, {p.name: p.read_bytes() for p in self.root.iterdir()})
        self.write('output.txt', 'processed substitute')
        result = self.cli('check', expected=1)
        self.assertFalse(result['artifact_ready'])
        self.assertEqual(result['criteria'][0]['status'], 'stale')
        self.cli('init', '--contract', str(self.root / 'contract.json'), expected=2)

    def test_changed_basis_requires_inspection_and_revision(self):
        self.record()
        self.write('source.txt', 'new user message semantics')
        self.record(expected=2)
        self.cli('revise', '--contract', str(self.root / 'contract.json'),
                 '--authority', 'corrected source', '--reason', 'inspected new meaning')
        self.assertEqual(self.cli('check', expected=1)['criteria'][0]['status'], 'stale')
        self.assertEqual(len(json.loads(self.state.read_text())['revisions']), 2)

    def test_goal_revision_retains_old_promise_invalidates_evidence(self):
        self.record()
        self.contract['purpose'] = 'New user-authorized goal'
        self.write('contract.json', self.contract)
        self.cli('revise', '--contract', str(self.root / 'contract.json'),
                 '--authority', 'user turn 2', '--reason', 'changed intended output')
        stored = json.loads(self.state.read_text())
        self.assertEqual(stored['revisions'][0]['contract']['purpose'], 'Deliver original and actual message count')
        self.assertEqual(self.cli('check', expected=1)['criteria'][0]['status'], 'stale')
        stored['contract']['purpose'] = 'silent lowering'
        self.write('state.json', stored)
        self.cli('check', expected=2)

    def test_list_cannot_satisfy_external_receipt_kind_or_human_decision(self):
        self.contract['criteria'] += [{'id': 'send', 'claim': 'actual send receipt', 'kind': 'external'},
                                     {'id': 'decision', 'claim': 'human value choice', 'kind': 'human'}]
        self.write('contract.json', self.contract)
        self.cli('revise', '--contract', str(self.root / 'contract.json'), '--authority', 'user', '--reason', 'new scope')
        self.record('send', 'artifact', expected=2)
        result = self.record()
        self.assertTrue(result['artifact_ready'])
        self.assertFalse(result['all_criteria_evidenced'])
        self.assertEqual(result['waiting_for_human'], ['decision'])

    def test_latest_failure_supersedes_pass_and_missing_receipt_is_stale(self):
        self.record()
        self.record('tests', 'check')
        self.record('tests', 'check', 'fail')
        self.assertEqual(self.cli('check', expected=1)['criteria'][1]['status'], 'fail')
        (self.root / 'receipt.txt').unlink()
        self.assertEqual(self.cli('check', expected=1)['criteria'][0]['status'], 'stale')

    def test_review_is_declared_and_invalidated_by_later_evidence(self):
        self.contract['criteria'].append({'id': 'review', 'claim': 'fresh independent review', 'kind': 'review'})
        self.write('contract.json', self.contract)
        self.cli('revise', '--contract', str(self.root / 'contract.json'), '--authority', 'user', '--reason', 'require review')
        self.record()
        self.record('tests', 'check')
        self.cli('record', '--criterion', 'review', '--kind', 'review', '--result', 'pass', '--by', 'fresh-context',
                 '--receipt', 'receipt.txt', '--note', 'Review of current output', '--independent')
        self.assertIn('identity', self.cli('check')['independent_acceptance'])
        self.record('tests', 'check', 'fail')
        result = self.cli('check', expected=1)
        self.assertEqual(result['criteria'][2]['status'], 'stale')
        self.assertEqual(result['independent_acceptance'], 'not established')

    def test_candidate_experience_is_not_promoted_and_use_is_traceable(self):
        self.write('experience.txt', 'candidate: source counts may differ from events')
        self.cli('use', '--file', 'experience.txt', '--status', 'candidate', '--decision', 'apply', '--reason', 'shortcut', expected=2)
        result = self.cli('use', '--file', 'experience.txt', '--status', 'candidate', '--decision', 'trial', '--reason', 'compare current data')
        self.assertEqual(result['experience_uses'][0]['decision'], 'trial')
        self.write('experience.txt', 'changed conclusion')
        result = self.cli('check', expected=1)
        self.assertEqual(result['experience_uses'][0]['stale_files'], ['experience.txt'])

    def test_evidence_cannot_escape_root_or_reference_itself(self):
        (self.root / 'escape').symlink_to(HELPER)
        for name in ['escape', '../outside', 'state.json']:
            self.cli('record', '--criterion', 'output', '--kind', 'artifact', '--result', 'pass', '--by', 'context',
                     '--receipt', 'receipt.txt', '--file', name, '--note', 'bad path', expected=2)

    def test_repointed_source_symlink_invalidates_even_equal_content(self):
        self.write('alternate.txt', 'original')
        alias = self.root / 'alias.txt'
        alias.symlink_to(self.root / 'source.txt')
        self.contract['inputs'] = ['alias.txt']
        self.write('contract.json', self.contract)
        self.cli('revise', '--contract', str(self.root / 'contract.json'), '--authority', 'user', '--reason', 'source alias')
        self.record()
        self.record('tests', 'check')
        self.cli('check')
        alias.unlink()
        alias.symlink_to(self.root / 'alternate.txt')
        result = self.cli('check', expected=1)
        self.assertEqual(result['criteria'][0]['status'], 'stale')
        self.record(expected=2)

    def test_revised_review_does_not_require_retired_artifacts(self):
        self.record()
        self.contract['criteria'] = [{'id': 'new', 'claim': 'new output', 'kind': 'artifact'},
                                     {'id': 'review', 'claim': 'current independent review', 'kind': 'review', 'independent': True}]
        self.write('contract.json', self.contract)
        self.cli('revise', '--contract', str(self.root / 'contract.json'), '--authority', 'user turn 2', '--reason', 'new deliverable')
        (self.root / 'output.txt').unlink()
        self.write('new.txt', 'new requested output')
        self.cli('record', '--criterion', 'new', '--kind', 'artifact', '--result', 'pass', '--by', 'context',
                 '--receipt', 'receipt.txt', '--file', 'new.txt', '--note', 'new output inspected')
        self.cli('record', '--criterion', 'review', '--kind', 'review', '--result', 'pass', '--by', 'self',
                 '--receipt', 'receipt.txt', '--note', 'self-review')
        self.cli('check', expected=1)
        self.cli('record', '--criterion', 'review', '--kind', 'review', '--result', 'pass', '--by', 'fresh-context',
                 '--receipt', 'receipt.txt', '--note', 'separate review', '--independent')
        self.assertTrue(self.cli('check')['all_criteria_evidenced'])

    def test_installed_folder_is_self_contained(self):
        installed = self.root / 'installed-gap'
        shutil.copytree(ROOT / 'skills/gap', installed)
        self.assertFalse(self.cli('check', expected=1, helper=installed / 'scripts/checkpoint.py')['all_criteria_evidenced'])

    def test_development_scenarios_red_and_known_green(self):
        evaluator = ROOT / 'tests/evaluators/collaboration.py'
        for directory, expected in [('fixtures', 1), ('reference-solutions', 0)]:
            result = subprocess.run([sys.executable, str(evaluator), str(ROOT / 'tests' / directory / 'collaboration')],
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, expected, result.stderr)
            checks = json.loads(result.stdout)
            self.assertEqual(set(checks.values()), {expected == 0})


if __name__ == '__main__':
    unittest.main()
