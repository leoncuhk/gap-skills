#!/usr/bin/env python3
"""Optional local evidence checkpoint. No job execution, authorization or truth oracle."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import tempfile
import uuid

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
        declared = Path(name)
        if declared.is_absolute() or '..' in declared.parts:
            raise ValueError(f'evidence path must be root-relative without ..: {name}')
        path = file_path(root, name)
        # Keep the alias AND target: a repointed symlink is a changed source,
        # even when both targets happen to contain the same bytes.
        result[str(declared)] = {'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                                 'target': str(path.relative_to(root))}
    return result


def changed(root, files):
    if not isinstance(files, dict):
        raise ValueError('file fingerprints must be an object')
    stale = []
    for name, expected in files.items():
        try:
            actual = snapshot(root, [name])[str(Path(name))]
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
    if not isinstance(state, dict):
        raise ValueError('checkpoint must be an object')
    if type(state.get('version')) is not int or state['version'] != 1:
        raise ValueError('unsupported checkpoint version')
    contract_valid(state['contract'])
    revisions = state.get('revisions')
    if not isinstance(revisions, list) or not revisions or any(not isinstance(r, dict) for r in revisions):
        raise ValueError('checkpoint needs a nonempty revision history of objects')
    if not isinstance(revisions[-1].get('inputs'), dict):
        raise ValueError('revision inputs must be a file fingerprint object')
    for key in ('receipts', 'experience_uses'):
        items = state.get(key)
        if not isinstance(items, list) or any(not isinstance(item, dict) for item in items):
            raise ValueError(f'{key} must be a list of objects')
    run = state.get('run')
    if not isinstance(run, dict) or run.get('status') not in ('active', 'ended'):
        raise ValueError('run must have an active or ended status')
    if digest(state['contract']) != state['revisions'][-1]['contract_sha256']:
        raise ValueError('contract edited outside revise; restore it and use revise to preserve history')
    return state


def nonreview_digest(state):
    return digest([r for r in state['receipts'] if r['kind'] != 'review'])


def experience_status(entry, state, root):
    stale = changed(root, entry['files'])
    basis_stale = changed(root, state['revisions'][-1]['inputs'])
    revision_stale = entry.get('revision') is not None and entry['revision'] != len(state['revisions'])
    return {**entry, 'stale_files': stale, 'stale_basis': basis_stale, 'stale_contract': revision_stale,
            'current_result_status': 'stale' if stale or basis_stale or revision_stale else entry.get('result_status', 'unverified')}


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
        'task_id': state.get('task_id', digest(state['revisions'][0]['contract'])),
        'artifact_ready': all(i['status'] == 'pass' for i in artifacts) if artifacts else None,
        'all_criteria_evidenced': all_pass,
        'independent_acceptance': 'recorded; identity and judgment require verification' if independent and all_pass else 'not established',
        'waiting_for_human': [i['id'] for i in items if i['kind'] == 'human' and i['status'] != 'pass'],
        'criteria': items,
        'experience_uses': [experience_status(x, state, root) for x in state['experience_uses']],
        'next': 'Inspect receipts and semantic fit before claiming completion.' if all_pass else 'Inspect missing/stale actual artifacts; recheck affected criteria before resuming. Do not blindly rerun.',
        'limits': 'Hashes prove file continuity, not truth, external delivery, authorization or independent reviewer identity.'}



def review_data(state, root, brief_path=None):
    data = inspect(state, root)
    names = set(state['contract']['inputs'])
    for experience in state['experience_uses']:
        names.update(experience['files'])
    for item in data['criteria']:
        receipt = next((r for r in reversed(state['receipts']) if r['criterion'] == item['id']), None)
        item['note'] = receipt.get('note', '') if receipt else ''
        item['evidence'] = []
        for path, fingerprint in (receipt['files'].items() if receipt else []):
            names.add(path)
            info = fingerprint if isinstance(fingerprint, dict) else {'sha256': fingerprint, 'target': path}
            item['evidence'].append({'path': path, **info})
    observed = {}
    for name in sorted(names):
        try:
            observed.update(snapshot(root, [name]))
        except (OSError, ValueError):
            observed[name] = None
    if brief_path is not None:
        from brief import load_brief
        data['brief'], brief_files = load_brief(root, brief_path, data['criteria'], read, snapshot, file_path)
        observed.update(brief_files)
    for item in data['criteria']:
        for evidence in item['evidence']:
            evidence['current'] = observed.get(evidence['path'])
    data.update(source=state['contract']['source'], revision=len(state['revisions']),
                observation_sha256=digest({'state': state, 'current_files': observed,
                                           'selected_brief': str(Path(brief_path)) if brief_path is not None else None}))
    return data


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
    use.add_argument('--scope', help='root-relative current-task scope JSON for structured adoption')
    use_result = commands.add_parser('use-result', help='bind an observed result to one recorded experience use')
    use_result.add_argument('--use-id', required=True)
    use_result.add_argument('--receipt', required=True)
    use_result.add_argument('--outcome', choices=['pass', 'fail', 'unknown'], required=True)
    commands.add_parser('check')
    view = commands.add_parser('view', help='read-only text or offline HTML review of current evidence')
    view.add_argument('--details', action='store_true', help='include full source and receipt appendix in text; HTML details remain expandable')
    view.add_argument('--format', choices=['text', 'html'], default='text')
    view.add_argument('--output', type=Path, help='new file inside root; never overwrite existing evidence')
    feedback = commands.add_parser('feedback', help='validate returned feedback without applying or approving it')
    feedback.add_argument('--file', required=True, help='root-relative exported JSON')
    view.add_argument('--brief', help='root-relative source-bound delivery explanation JSON')
    feedback.add_argument('--brief', help='same delivery explanation used for the reviewed view')
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
            state = {'version': 1, 'task_id': uuid.uuid4().hex, 'contract': contract, 'revisions': [
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
            if any(info['target'] == str(state_path.relative_to(root)) for info in files.values()):
                raise ValueError('checkpoint cannot be its own evidence')
            receipt = {'criterion': args.criterion, 'kind': args.kind, 'result': args.result,
                       'by': args.by, 'note': args.note, 'independent': args.independent,
                       'contract_sha256': digest(state['contract']), 'revision': len(state['revisions']), 'files': files}
            if args.kind == 'review':
                # Bind only latest evidence for criteria in the current revision.
                # Retired artifacts remain history, not fresh review dependencies.
                current_ids = {c['id'] for c in state['contract']['criteria'] if c['kind'] != 'review'}
                latest = {r['criterion']: r for r in state['receipts']
                          if r['criterion'] in current_ids and r.get('revision') == len(state['revisions'])}
                for prior in latest.values():
                    receipt['files'].update(prior['files'])
                receipt['covers'] = nonreview_digest(state)
            state['receipts'].append(receipt)
        elif args.command == 'end':
            state['run'] = {'status': 'ended', 'reason': args.reason}
        elif args.command in ('use', 'use-result'):
            from experience import assess_experience, finish_experience
            if changed(root, state['revisions'][-1]['inputs']):
                raise ValueError('basis changed; inspect and revise before experience adoption/result')
            if args.command == 'use':
                entry = assess_experience(root, args.file, args.status, args.decision, args.scope)
                task_id = state.get('task_id', digest(state['revisions'][0]['contract']))
                if entry['task_id'] is not None and entry['task_id'] != task_id:
                    raise ValueError('experience scope task_id does not match this checkpoint')
                entry.update(task_id=task_id, reason=args.reason, revision=len(state['revisions']),
                             contract_sha256=digest(state['contract']))
            else:
                entry = next((x for x in state['experience_uses'] if x.get('id') == args.use_id), None)
                if entry is None:
                    raise ValueError('unknown experience use id')
                if entry.get('revision') != len(state['revisions']) or entry.get('contract_sha256') != digest(state['contract']):
                    raise ValueError('experience use belongs to an older contract revision; reassess applicability')
                entry = finish_experience(root, entry, args.receipt, args.outcome)
            if any(info['target'] == str(state_path.relative_to(root)) for info in entry['files'].values()):
                raise ValueError('checkpoint cannot be its own experience evidence')
            if args.command == 'use':
                state['experience_uses'].append(entry)
            else:
                state['experience_uses'] = [entry if x.get('id') == args.use_id else x for x in state['experience_uses']]
        if args.command in ('view', 'feedback'):
            from review_view import render_html, render_text, validate_feedback
            data = review_data(state, root, args.brief)
            if args.command == 'feedback':
                print(json.dumps(validate_feedback(read(file_path(root, args.file)), data), indent=2, ensure_ascii=False))
                return 0
            rendered = render_html(data) if args.format == 'html' else render_text(data, details=args.details)
            if args.output:
                output = args.output.resolve()
                if not output.is_relative_to(root):
                    raise ValueError('view output must be inside task root')
                with output.open('x', encoding='utf-8') as stream:
                    stream.write(rendered)
                print(json.dumps({'output': str(output), 'observation_sha256': data['observation_sha256']}))
            else:
                print(rendered)
            return 0
        result = inspect(state, root)
        rendered = json.dumps(result, indent=2, ensure_ascii=False)
        if args.command != 'check':
            save(state_path, state)
        print(rendered)
        return 0 if args.command != 'check' or result['all_criteria_evidenced'] else 1
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(json.dumps({'error': str(exc)}, ensure_ascii=False))
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
