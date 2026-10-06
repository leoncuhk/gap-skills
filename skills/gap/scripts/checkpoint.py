#!/usr/bin/env python3
"""Optional local evidence checkpoint. No job execution, authorization or truth oracle."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import tempfile

KINDS = {'artifact', 'check', 'external', 'human', 'review'}


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def file_path(root, name):
    path = (root / name).resolve()
    if not path.is_relative_to(root) or not path.is_file():
        raise ValueError(f'missing file or outside root: {name}')
    return path


def snapshot(root, names):
    result = {}
    for name in names:
        path = file_path(root, name)
        key = str(path.relative_to(root))
        result[key] = hashlib.sha256(path.read_bytes()).hexdigest()
    return result


def changed(root, files):
    stale = []
    for name, expected in files.items():
        try:
            actual = snapshot(root, [name])[name]
        except (ValueError, OSError):
            actual = None
        if actual != expected:
            stale.append(name)
    return stale


def contract_valid(contract):
    if not isinstance(contract, dict):
        raise ValueError('contract must be an object')
    for key in ('purpose', 'source'):
        if not isinstance(contract.get(key), str) or not contract[key].strip():
            raise ValueError(f'contract needs {key}')
    for key in ('semantics', 'inputs'):
        value = contract.get(key)
        if not isinstance(value, list) or any(not isinstance(x, str) or not x.strip() for x in value):
            raise ValueError(f'{key} must be a list of nonempty strings')
    criteria = contract.get('criteria')
    if not isinstance(criteria, list) or not criteria:
        raise ValueError('contract needs criteria')
    ids = set()
    for item in criteria:
        if not isinstance(item, dict) or item.get('kind') not in KINDS:
            raise ValueError('invalid criterion kind')
        for key in ('id', 'claim'):
            if not isinstance(item.get(key), str) or not item[key].strip():
                raise ValueError(f'criterion needs {key}')
        if item['id'] in ids:
            raise ValueError('duplicate criterion id')
        ids.add(item['id'])


def save(path, state):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    # Atomic replacement protects a checkpoint from interrupted writes.
    fd, name = tempfile.mkstemp(prefix='.gap-', dir=path.parent)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as stream:
            json.dump(state, stream, indent=2, ensure_ascii=False)
            stream.write('\n')
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def load_state(path):
    state = read(path)
    if state.get('version') != 1:
        raise ValueError('unsupported checkpoint version')
    contract_valid(state['contract'])
    if digest(state['contract']) != state['revisions'][-1]['contract_sha256']:
        raise ValueError('contract edited outside revise; restore it and use revise to preserve history')
    return state


def nonreview_digest(state):
    return digest([r for r in state['receipts'] if r['kind'] != 'review'])


def inspect(state, root):
    contract = state['contract']
    current = digest(contract)
    basis_changes = changed(root, state['revisions'][-1]['inputs'])
    items = []
    for criterion in contract['criteria']:
        receipts = [r for r in state['receipts'] if r['criterion'] == criterion['id']]
        record = receipts[-1] if receipts else None
        status, reasons = 'missing', []
        if record:
            if record['contract_sha256'] != current or record.get('revision') != len(state['revisions']):
                reasons.append('contract changed')
            reasons.extend('basis changed; revise after inspection: ' + p for p in basis_changes)
            reasons.extend('file changed or missing: ' + p for p in changed(root, record['files']))
            if record['kind'] != criterion['kind']:
                reasons.append('evidence kind mismatch')
            if criterion.get('independent') and not record.get('independent'):
                reasons.append('required independent review absent')
            if criterion['kind'] == 'review' and record.get('covers') != nonreview_digest(state):
                reasons.append('evidence changed after review')
            status = 'stale' if reasons else record['result']
        items.append({'id': criterion['id'], 'claim': criterion['claim'], 'kind': criterion['kind'],
                      'status': status, 'reasons': reasons, 'by': record.get('by') if record else None})
    artifacts = [i for i in items if i['kind'] == 'artifact']
    reviews = [i for i in items if i['kind'] == 'review']
    all_pass = all(i['status'] == 'pass' for i in items)
    independent = bool(reviews) and all(
        i['status'] == 'pass' and next(r for r in reversed(state['receipts']) if r['criterion'] == i['id']).get('independent')
        for i in reviews)
    return {
        'purpose': contract['purpose'], 'run': state['run'],
        'artifact_ready': all(i['status'] == 'pass' for i in artifacts) if artifacts else None,
        'all_criteria_evidenced': all_pass,
        'independent_acceptance': 'recorded; identity and judgment require verification' if independent and all_pass else 'not established',
        'waiting_for_human': [i['id'] for i in items if i['kind'] == 'human' and i['status'] != 'pass'],
        'criteria': items,
        'experience_uses': [{**x, 'stale_files': changed(root, x['files'])} for x in state['experience_uses']],
        'next': 'Inspect receipts and semantic fit before claiming completion.' if all_pass else 'Inspect missing/stale actual artifacts; recheck affected criteria before resuming. Do not blindly rerun.',
        'limits': 'Hashes prove file continuity, not truth, external delivery, authorization or independent reviewer identity.'}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', required=True, type=Path, help='actual task directory; all evidence stays inside it')
    parser.add_argument('--state', required=True, type=Path, help='existing project checkpoint location')
    commands = parser.add_subparsers(dest='command', required=True)
    init = commands.add_parser('init')
    init.add_argument('--contract', required=True, type=Path)
    revise = commands.add_parser('revise')
    revise.add_argument('--contract', required=True, type=Path)
    revise.add_argument('--reason', required=True)
    revise.add_argument('--authority', required=True, help='user decision or corrected factual source; not agent preference')
    record = commands.add_parser('record', help='capture an ACTUAL receipt after observing/running the check')
    record.add_argument('--criterion', required=True)
    record.add_argument('--kind', required=True, choices=sorted(KINDS))
    record.add_argument('--result', required=True, choices=['pass', 'fail'])
    record.add_argument('--by', required=True, help='actual actor/context; declared, not authenticated')
    record.add_argument('--receipt', required=True, help='local check log, action receipt, decision or review report')
    record.add_argument('--file', action='append', default=[], help='output/source checked; repeat as needed')
    record.add_argument('--independent', action='store_true', help='review came from a separate context; declaration only')
    record.add_argument('--note', required=True, help='what was actually observed and its limits')
    end = commands.add_parser('end')
    end.add_argument('--reason', required=True)
    use = commands.add_parser('use', help='record an experience consulted, without promoting it')
    use.add_argument('--file', required=True)
    use.add_argument('--status', choices=['candidate', 'validated'], required=True)
    use.add_argument('--decision', choices=['trial', 'apply', 'reject'], required=True)
    use.add_argument('--reason', required=True, help='applicability, evidence, and expected effect in this task')
    commands.add_parser('check')
    args = parser.parse_args(argv)
    root = args.root.resolve()
    try:
        if not root.is_dir():
            raise ValueError('root must be an existing task directory')
        state_path = args.state.resolve()
        if not state_path.is_relative_to(root):
            raise ValueError('state must be inside task root')
        if args.command == 'init':
            if state_path.exists():
                raise ValueError('checkpoint exists; inspect/check it instead of overwriting')
            contract = read(args.contract)
            contract_valid(contract)
            snapshot(root, contract['inputs'])
            state = {'version': 1, 'contract': contract, 'revisions': [
                {'contract': contract, 'contract_sha256': digest(contract), 'authority': contract['source'], 'reason': 'initial', 'inputs': snapshot(root, contract['inputs'])}],
                'receipts': [], 'experience_uses': [], 'run': {'status': 'active'}}
        else:
            state = load_state(state_path)
        if args.command == 'revise':
            contract = read(args.contract)
            contract_valid(contract)
            snapshot(root, contract['inputs'])
            if digest(contract) == digest(state['contract']) and not changed(root, state['revisions'][-1]['inputs']):
                raise ValueError('no contract change; inspect files or record new evidence instead')
            state['contract'] = contract
            state['revisions'].append({'contract': contract, 'contract_sha256': digest(contract),
                                       'authority': args.authority, 'reason': args.reason, 'inputs': snapshot(root, contract['inputs'])})
            state['run'] = {'status': 'active'}
        elif args.command == 'record':
            if changed(root, state['revisions'][-1]['inputs']):
                raise ValueError('basis changed; inspect it and revise with reason/authority before recording')
            criterion = next((c for c in state['contract']['criteria'] if c['id'] == args.criterion), None)
            if not criterion or criterion['kind'] != args.kind:
                raise ValueError('unknown criterion or evidence kind mismatch')
            if args.kind == 'artifact' and not args.file:
                raise ValueError('artifact evidence requires --file for actual output')
            if args.independent and args.kind != 'review':
                raise ValueError('--independent applies only to actual review receipts')
            files = snapshot(root, state['contract']['inputs'] + [args.receipt] + args.file)
            if str(state_path.relative_to(root)) in files:
                raise ValueError('checkpoint cannot be its own evidence')
            receipt = {'criterion': args.criterion, 'kind': args.kind, 'result': args.result,
                       'by': args.by, 'note': args.note, 'independent': args.independent,
                       'contract_sha256': digest(state['contract']), 'revision': len(state['revisions']), 'files': files}
            if args.kind == 'review':
                for prior in state['receipts']:
                    if prior['kind'] != 'review':
                        receipt['files'].update(prior['files'])
                receipt['covers'] = nonreview_digest(state)
            state['receipts'].append(receipt)
        elif args.command == 'end':
            state['run'] = {'status': 'ended', 'reason': args.reason}
        elif args.command == 'use':
            if args.status == 'candidate' and args.decision == 'apply':
                raise ValueError('candidate experience may be trialed or rejected, not applied as validated')
            state['experience_uses'].append({'path': args.file, 'declared_status': args.status,
                                            'decision': args.decision, 'reason': args.reason,
                                            'files': snapshot(root, [args.file])})
        if args.command != 'check':
            save(state_path, state)
        result = inspect(state, root)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0 if args.command != 'check' or result['all_criteria_evidenced'] else 1
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(json.dumps({'error': str(exc)}, ensure_ascii=False))
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
