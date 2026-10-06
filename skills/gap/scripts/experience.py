"""Bounded experience evidence. File continuity is not semantic validation."""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import re
import uuid


def _text(value, label):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f'{label} must be nonempty text')
    return value


def _strings(value, label):
    if not isinstance(value, list) or not value:
        raise ValueError(f'{label} must be a nonempty list')
    for item in value:
        _text(item, label)
    if len(set(value)) != len(value):
        raise ValueError(f'{label} contains duplicates')
    return value


def _object(value, label):
    if not isinstance(value, dict):
        raise ValueError(f'{label} must be an object')
    return value


def _name(value):
    _text(value, 'path')
    path = Path(value)
    if path.is_absolute() or '..' in path.parts or str(path) != value or value == '.':
        raise ValueError('evidence path must be canonical root-relative without ..')
    return path


def _snapshot(root, name):
    root = Path(root).resolve()
    path = (root / _name(name)).resolve()
    if not path.is_relative_to(root) or not path.is_file():
        raise ValueError(f'missing file or outside root: {name}')
    return {'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'target': str(path.relative_to(root))}


def _load(root, name):
    _snapshot(root, name)
    return json.loads((Path(root).resolve() / name).read_text(encoding='utf-8'))


def _bind(root, ref, files, require_fresh=True):
    _object(ref, 'evidence reference')
    name = str(_name(ref.get('path')))
    target = str(_name(ref.get('target')))
    sha = ref.get('sha256')
    if not isinstance(sha, str) or not re.fullmatch('[0-9a-f]{64}', sha):
        raise ValueError('evidence reference needs sha256')
    expected = {'sha256': sha, 'target': target}
    # Resolve even rejected evidence: paths outside the task are never inspected.
    actual = _snapshot(root, name)
    if require_fresh and actual != expected:
        raise ValueError(f'stale experience evidence: {name}')
    if name in files and files[name] != expected:
        raise ValueError(f'conflicting evidence reference: {name}')
    files[name] = expected
    return target


def _refs(root, refs, files, fresh=True):
    if not isinstance(refs, list) or not refs:
        raise ValueError('evidence references must be a nonempty list')
    return [_bind(root, ref, files, fresh) for ref in refs]


def _experience(root, data, files, fresh):
    _object(data, 'experience')
    if (type(data.get('version')) is not int or data['version'] != 1
            or data.get('status') not in ('candidate', 'validated')):
        raise ValueError('experience needs version 1 and candidate/validated status')
    _text(data.get('id'), 'experience id')
    scope = _object(data.get('scope'), 'scope')
    _strings(scope.get('applies_to'), 'scope.applies_to')
    _strings(scope.get('excludes'), 'scope.excludes')
    if set(scope['applies_to']) & set(scope['excludes']):
        raise ValueError('scope conditions cannot also be exclusions')
    correction = _object(data.get('correction'), 'correction')
    for key in ('action', 'expected_result', 'check'):
        _text(correction.get(key), f'correction.{key}')
    sources = data.get('sources')
    if not isinstance(sources, list) or not sources:
        raise ValueError('experience needs concrete failure sources')
    source_tasks = set()
    source_targets, source_hashes = set(), set()
    for source in sources:
        _object(source, 'source')
        source_tasks.add(_text(source.get('task_id'), 'source task_id'))
        _text(source.get('failure'), 'source failure')
        source_targets.add(_bind(root, source.get('receipt'), files, fresh))
        source_hashes.add(source['receipt']['sha256'])
    validations = data.get('validations', [])
    if not isinstance(validations, list):
        raise ValueError('validations must be a list')
    validation_tasks, validation_targets, validation_hashes = set(), set(), set()
    forward = False
    for validation in validations:
        _object(validation, 'validation')
        task = _text(validation.get('task_id'), 'validation task_id')
        if task in validation_tasks:
            raise ValueError('validation tasks must be distinct')
        validation_tasks.add(task)
        if validation.get('kind') not in ('regression', 'forward'):
            raise ValueError('validation kind must be regression or forward')
        forward = forward or validation['kind'] == 'forward'
        if task in source_tasks:
            raise ValueError('validation needs a separate task from failure sources')
        if set(_strings(validation.get('scope'), 'validation scope')) != set(scope['applies_to']):
            raise ValueError('validation scope must match the bounded experience scope')
        if validation.get('before_result') != 'fail' or validation.get('after_result') != 'pass':
            raise ValueError('validation needs fail-before and pass-after results')
        _text(validation.get('observed'), 'validation observed')
        before = _bind(root, validation.get('before'), files, fresh)
        after = _bind(root, validation.get('after'), files, fresh)
        if (before == after or after in source_targets
                or validation['before']['sha256'] == validation['after']['sha256']
                or validation['after']['sha256'] in source_hashes):
            raise ValueError('validation must use distinct before/after evidence')
        after_hash = validation['after']['sha256']
        if after in validation_targets or after_hash in validation_hashes:
            raise ValueError('reused validation receipt cannot count as an independent task')
        validation_targets.add(after)
        validation_hashes.add(after_hash)
        review = _object(validation.get('review'), 'validation review')
        _text(review.get('by'), 'review by')
        if review.get('independent') is not True:
            raise ValueError('validation needs a declared independent semantic review')
        review_target = _bind(root, review.get('receipt'), files, fresh)
        if review_target in {before, after} | source_targets:
            raise ValueError('semantic review needs its own receipt')
    if data['status'] == 'validated' and (len(validation_tasks) < 2 or not forward):
        raise ValueError('validated label requires two independent validation tasks including forward evidence')
    return data


def assess_experience(root, path, declared_status, decision, scope_file=None):
    """Capture bounded adoption; caller binds checkpoint/task revision separately."""
    if declared_status not in ('candidate', 'validated') or decision not in ('trial', 'apply', 'reject'):
        raise ValueError('invalid experience status or decision')
    files = {path: _snapshot(root, path)}
    raw = (Path(root).resolve() / path).read_text(encoding='utf-8')
    structured = Path(path).suffix.lower() == '.json' or raw.lstrip().startswith('{')
    data = _experience(root, json.loads(raw), files, decision != 'reject') if structured else None
    if data and data['status'] != declared_status:
        raise ValueError('declared status does not match experience status')
    if not data and declared_status != 'candidate':
        raise ValueError('legacy Markdown is candidate evidence only')
    if decision == 'apply' and (not data or data['status'] != 'validated'):
        raise ValueError('candidate experience may be trialed or rejected, not applied as validated')
    experience_id = data['id'] if data else path
    scope = None
    if data and decision != 'reject' and scope_file is None:
        raise ValueError('trial/apply requires task scope evidence')
    if scope_file is not None:
        files[scope_file] = _snapshot(root, scope_file)
        scope = _object(_load(root, scope_file), 'task scope')
        _text(scope.get('task_id'), 'scope task_id')
        _text(scope.get('reason'), 'scope reason')
        if scope.get('experience_id') != experience_id:
            raise ValueError('scope experience_id mismatch')
        matches = _strings(scope.get('matched_scope'), 'matched_scope')
        excluded = scope.get('excluded_conditions_checked')
        if data:
            if set(matches) != set(data['scope']['applies_to']):
                raise ValueError('task scope must match all experience conditions')
            if set(_strings(excluded, 'excluded_conditions_checked')) != set(data['scope']['excludes']):
                raise ValueError('task scope must check every exclusion')
        _refs(root, scope.get('basis'), files)
    return {'id': uuid.uuid4().hex, 'path': path, 'declared_status': declared_status,
            'decision': decision, 'format': 'structured' if data else 'legacy',
            'experience_id': experience_id, 'task_id': scope['task_id'] if scope else None,
            'scope_file': scope_file, 'scope': scope,
            'validation_status': 'evidence_recorded' if data and data['status'] == 'validated' else 'candidate',
            'result_status': 'not_required' if decision == 'reject' else 'unverified',
            'files': files,
            'limits': 'Integrity and freshness only; independent review identity, scope fit and causal improvement require semantic review.'}


def finish_experience(root, use_record, receipt_path, outcome):
    """Return a new adoption record with a same-use actual result receipt."""
    if use_record.get('decision') not in ('trial', 'apply'):
        raise ValueError('only trial/apply has a use result')
    if outcome not in ('pass', 'fail', 'unknown'):
        raise ValueError('outcome must be pass, fail or unknown')
    record = copy.deepcopy(use_record)
    for name, expected in record['files'].items():
        if _snapshot(root, name) != expected:
            raise ValueError(f'stale experience adoption: {name}')
    if receipt_path in record['files']:
        raise ValueError('result receipt must be new evidence for this use')
    fingerprint = _snapshot(root, receipt_path)
    if fingerprint['target'] in {x['target'] for x in record['files'].values()}:
        raise ValueError('result receipt cannot alias existing adoption evidence')
    receipt = _object(_load(root, receipt_path), 'use result')
    for key, expected in (('use_id', record['id']), ('task_id', record['task_id']),
                          ('experience_id', record['experience_id']), ('outcome', outcome)):
        if receipt.get(key) != expected:
            raise ValueError(f'use result {key} mismatch')
    for key in ('observed', 'cost', 'user_intervention'):
        _text(receipt.get(key), f'use result {key} (use unknown if not measured)')
    prior_targets = {x['target'] for x in record['files'].values()}
    prior_hashes = {x['sha256'] for x in record['files'].values()}
    checks = _refs(root, receipt.get('checks'), record['files'])
    if any(ref['target'] in prior_targets or ref['sha256'] in prior_hashes for ref in receipt['checks']):
        raise ValueError('use result needs new task checks, not reused adoption evidence')
    if fingerprint['target'] in checks:
        raise ValueError('result receipt cannot be its own check evidence')
    record['files'][receipt_path] = fingerprint
    record['result'] = {'receipt': receipt_path, 'outcome': outcome, 'observed': receipt['observed'],
                        'cost': receipt['cost'], 'user_intervention': receipt['user_intervention']}
    record.setdefault('results', []).append(copy.deepcopy(record['result']))
    record['result_status'] = 'unverified' if outcome == 'unknown' else 'recorded'
    return record
