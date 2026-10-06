"""Actual file-bound adoption, stale evidence and scoped validation controls."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

MODULE = Path(__file__).resolve().parents[1] / 'skills/gap/scripts/experience.py'
SPEC = importlib.util.spec_from_file_location('experience', MODULE)
experience = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(experience)


class ExperienceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.data = {
            'version': 1, 'id': 'receipt-propagation', 'status': 'validated',
            'sources': [{'task_id': 'incident', 'failure': 'Caller swallowed a failing check.',
                         'receipt': self.ref('failure.log', 'observed incident failure')}],
            'scope': {'applies_to': ['local CLI exit propagation'], 'excludes': ['remote CI policy']},
            'correction': {'action': 'Propagate check return code.',
                           'expected_result': 'Bad case fails in caller.', 'check': 'Run bad and good controls.'},
            'validations': [self.validation('regression'), self.validation('forward')]}
        self.scope = {'task_id': 'new-task', 'experience_id': self.data['id'],
                      'matched_scope': self.data['scope']['applies_to'][:],
                      'excluded_conditions_checked': self.data['scope']['excludes'][:],
                      'basis': [self.ref('task.txt', 'A local CLI caller check task.')],
                      'reason': 'This caller is local; it does not alter remote CI.'}
        self.write()

    def ref(self, path, text=None):
        file = self.root / path
        if text is not None:
            file.write_text(text, encoding='utf-8')
        return {'path': path, 'target': str(file.resolve().relative_to(self.root)),
                'sha256': hashlib.sha256(file.read_bytes()).hexdigest()}

    def validation(self, task):
        return {'task_id': task, 'kind': task, 'scope': ['local CLI exit propagation'],
                'before': self.ref(task + '-before.log', task + ': bad case exits zero'),
                'after': self.ref(task + '-after.log', task + ': bad exits 1; good exits 0'),
                'before_result': 'fail', 'after_result': 'pass', 'observed': 'Caller now preserves failure.',
                'review': {'by': 'separate context', 'independent': True,
                           'receipt': self.ref(task + '-review.md', task + ': scope and evidence reviewed')}}

    def write(self):
        (self.root / 'experience.json').write_text(json.dumps(self.data), encoding='utf-8')
        (self.root / 'scope.json').write_text(json.dumps(self.scope), encoding='utf-8')

    def assess(self, status='validated', decision='apply', scope='scope.json'):
        return experience.assess_experience(self.root, 'experience.json', status, decision, scope)

    def finish(self, record, outcome='pass', name='result.json', **changes):
        body = {'use_id': record['id'], 'task_id': record['task_id'], 'experience_id': record['experience_id'],
                'outcome': outcome, 'observed': 'Bad and good cases observed through caller.',
                'cost': 'unknown', 'user_intervention': 'unknown',
                'checks': [self.ref(name + '.log', name + ': task actually checked ' + outcome)]}
        body.update(changes)
        (self.root / name).write_text(json.dumps(body), encoding='utf-8')
        return experience.finish_experience(self.root, record, name, outcome)

    def test_validated_adoption_waits_for_actual_result(self):
        record = self.assess()
        self.assertEqual('unverified', record['result_status'])
        self.assertEqual('evidence_recorded', record['validation_status'])
        self.assertIn('forward-after.log', record['files'])
        self.assertIn('task.txt', record['files'])
        finished = self.finish(record)
        self.assertEqual('recorded', finished['result_status'])
        self.assertEqual('unverified', record['result_status'])
        self.assertEqual('pass', finished['results'][0]['outcome'])
        self.assertIn('semantic review', record['limits'])

    def test_legacy_trial_and_reject_remain_compatible(self):
        self.ref('legacy.md', 'Candidate: preserve exit codes.')
        for decision in ('trial', 'reject'):
            record = experience.assess_experience(self.root, 'legacy.md', 'candidate', decision)
            self.assertEqual('legacy', record['format'])
        for status, decision in [('validated', 'apply'), ('candidate', 'apply'), ('validated', 'trial')]:
            with self.assertRaises(ValueError):
                experience.assess_experience(self.root, 'legacy.md', status, decision)

    def test_version_must_be_integer_not_boolean_or_float(self):
        for version in (True, 1.0, '1', None, 2):
            self.data['version'] = version
            self.write()
            with self.assertRaises(ValueError):
                self.assess()

    def test_candidate_cannot_promote_via_cli_label(self):
        self.data.update(status='candidate', validations=[])
        self.write()
        self.assertEqual('candidate', self.assess('candidate', 'trial')['validation_status'])
        for status in ('candidate', 'validated'):
            with self.assertRaises(ValueError):
                self.assess(status, 'apply')

    def test_validated_needs_two_distinct_tasks_and_forward_check(self):
        original = copy.deepcopy(self.data)
        variants = [[], self.data['validations'][:1],
                    [self.data['validations'][0], copy.deepcopy(self.data['validations'][0])]]
        for validations in variants:
            self.data = copy.deepcopy(original)
            self.data['validations'] = validations
            self.write()
            with self.assertRaises(ValueError):
                self.assess()
        self.data = original
        self.data['validations'][1]['kind'] = 'regression'
        self.write()
        with self.assertRaises(ValueError):
            self.assess()

    def test_relabelled_identical_receipts_are_not_independent(self):
        self.data['validations'][1]['after'] = self.ref(
            'copied.log', (self.root / 'regression-after.log').read_text())
        self.write()
        with self.assertRaisesRegex(ValueError, 'reused validation'):
            self.assess()

    def test_source_or_before_bytes_cannot_be_relabelled_as_success(self):
        original = copy.deepcopy(self.data)
        for source in ('failure.log', 'regression-before.log'):
            self.data = copy.deepcopy(original)
            self.data['validations'][0]['after'] = self.ref(
                'false-success.log', (self.root / source).read_text())
            self.write()
            with self.assertRaises(ValueError):
                self.assess()

    def test_source_task_cannot_double_as_validation(self):
        self.data['validations'][0]['task_id'] = 'incident'
        self.write()
        with self.assertRaisesRegex(ValueError, 'separate task'):
            self.assess()

    def test_missing_limits_or_unsupported_generalization_rejected(self):
        original = copy.deepcopy(self.data)
        for mutation in ('limits', 'scope', 'check', 'review'):
            self.data = copy.deepcopy(original)
            if mutation == 'limits':
                self.data['scope']['excludes'] = []
            elif mutation == 'scope':
                self.data['scope']['applies_to'].append('all automation')
            elif mutation == 'check':
                self.data['correction']['check'] = ''
            else:
                self.data['validations'][0]['review']['independent'] = False
            self.write()
            with self.assertRaises(ValueError):
                self.assess()

    def test_task_scope_requires_match_exclusions_and_actual_basis(self):
        original = copy.deepcopy(self.scope)
        for key, value in [('matched_scope', ['other domain']), ('excluded_conditions_checked', []),
                           ('basis', []), ('experience_id', 'different')]:
            self.scope = copy.deepcopy(original)
            self.scope[key] = value
            self.write()
            with self.assertRaises(ValueError):
                self.assess()
        with self.assertRaises(ValueError):
            self.assess(scope=None)

    def test_changed_underlying_validation_blocks_fresh_experience_file(self):
        self.ref('forward-after.log', 'changed later')
        with self.assertRaisesRegex(ValueError, 'stale experience'):
            self.assess()

    def test_reject_can_retain_stale_reference_for_audit(self):
        self.ref('forward-after.log', 'changed later')
        self.assertEqual('not_required', self.assess(decision='reject')['result_status'])

    def test_source_and_scope_changes_block_result(self):
        for name in ('failure.log', 'task.txt', 'scope.json', 'experience.json'):
            original = (self.root / name).read_bytes()
            record = self.assess()
            (self.root / name).write_bytes(original + b' ')
            with self.assertRaisesRegex(ValueError, 'stale experience adoption'):
                self.finish(record)
            (self.root / name).write_bytes(original)

    def test_same_bytes_symlink_retarget_is_stale(self):
        self.ref('same.log', (self.root / 'failure.log').read_text())
        (self.root / 'alias.log').symlink_to('failure.log')
        self.data['sources'][0]['receipt'] = self.ref('alias.log')
        self.write()
        record = self.assess()
        (self.root / 'alias.log').unlink()
        (self.root / 'alias.log').symlink_to('same.log')
        with self.assertRaises(ValueError):
            self.assess()
        with self.assertRaises(ValueError):
            self.finish(record)

    def test_paths_cannot_escape_root(self):
        for path in ('../outside.json', '/etc/passwd', './experience.json'):
            with self.assertRaises(ValueError):
                experience.assess_experience(self.root, path, 'candidate', 'trial')
        (self.root / 'escape').symlink_to('/etc/passwd')
        with self.assertRaises(ValueError):
            experience.assess_experience(self.root, 'escape', 'candidate', 'trial')
        self.data['sources'][0]['receipt']['target'] = '../outside'
        self.write()
        with self.assertRaises(ValueError):
            self.assess()

    def test_each_task_and_use_requires_its_own_result(self):
        first = self.assess()
        self.scope['task_id'] = 'second-task'
        self.write()
        second = self.assess()
        with self.assertRaisesRegex(ValueError, 'use_id mismatch'):
            self.finish(second, use_id=first['id'])
        with self.assertRaisesRegex(ValueError, 'task_id mismatch'):
            self.finish(second, task_id=first['task_id'])
        self.assertEqual('recorded', self.finish(second)['result_status'])
        self.assertEqual('unverified', first['result_status'])

    def test_unknown_stays_unverified_and_fail_history_survives_retry(self):
        record = self.assess()
        self.assertEqual('unverified', self.finish(record, 'unknown')['result_status'])
        failed = self.finish(record, 'fail', 'failed.json')
        passed = self.finish(failed, 'pass', 'passed.json')
        self.assertEqual(['fail', 'pass'], [r['outcome'] for r in passed['results']])

    def test_result_needs_new_checks_and_reported_outcome(self):
        record = self.assess()
        for changes in ({'checks': []}, {'checks': [self.data['validations'][0]['after']]},
                        {'observed': ''}, {'user_intervention': ''}):
            with self.assertRaises(ValueError):
                self.finish(record, **changes)
        self.finish(record)
        with self.assertRaises(ValueError):
            experience.finish_experience(self.root, record, 'result.json', 'fail')

    def test_reject_has_no_adoption_result(self):
        with self.assertRaises(ValueError):
            self.finish(self.assess(decision='reject'))


if __name__ == '__main__':
    unittest.main()
