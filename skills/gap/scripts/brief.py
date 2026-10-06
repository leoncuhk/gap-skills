"""Optional source-bound explanation data; no business-truth or approval oracle."""
import difflib
import re
from pathlib import Path


def _text(value, label):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f'brief needs nonempty {label}')
    return value


def load_brief(root, path, criteria, read, snapshot, file_path):
    raw = read(file_path(root, path))
    if not isinstance(raw, dict) or type(raw.get('version')) is not int or raw['version'] != 1:
        raise ValueError('unsupported brief version')
    if set(raw) != {'version', 'summary', 'changes', 'decisions', 'limits'}:
        raise ValueError('brief fields must be version, summary, changes, decisions, limits')
    _text(raw['summary'], 'summary')
    if not isinstance(raw['changes'], list) or not raw['changes']:
        raise ValueError('brief needs at least one source-backed change')
    if not isinstance(raw['decisions'], list) or not isinstance(raw['limits'], list):
        raise ValueError('brief decisions and limits must be lists')
    for limit in raw['limits']:
        _text(limit, 'limit')
    known = {c['id']: c for c in criteria}
    files = snapshot(root, [path])
    sources, stale, seen = [], [], {}

    def citation(ref):
        if not isinstance(ref, dict) or set(ref) != {'path', 'start', 'end', 'sha256', 'target'}:
            raise ValueError('citation needs path, start, end, sha256, target')
        for key in ('path', 'sha256', 'target'):
            _text(ref[key], key)
        if not re.fullmatch('[0-9a-f]{64}', ref['sha256']):
            raise ValueError('citation needs a full SHA-256')
        start, end = ref['start'], ref['end']
        if type(start) is not int or type(end) is not int or start < 1 or end < start or end - start >= 80:
            raise ValueError('citation needs a bounded 1-based span of at most 80 lines')
        identity = (ref['path'], start, end, ref['sha256'], ref['target'])
        if identity in seen:
            return seen[identity]
        if str(Path(ref['path'])) != ref['path']:
            raise ValueError('citation path must be canonical root-relative')
        actual = snapshot(root, [ref['path']])
        current = actual[ref['path']]
        source = file_path(root, ref['path'])
        if source.stat().st_size > 512000:
            raise ValueError('citation source exceeds 512000 bytes; use an authorized bounded export')
        lines = source.read_text(encoding='utf-8').splitlines()
        is_stale = current != {'sha256': ref['sha256'], 'target': ref['target']}
        if end > len(lines) and not is_stale:
            raise ValueError('citation span exceeds source lines')
        if is_stale:
            stale.append(ref['path'])
        item = {**ref, 'anchor': f'source-{len(sources)}', 'stale': is_stale,
                'text': '\n'.join(lines[start-1:end]), 'current': current}
        sources.append(item)
        seen[identity] = item
        files.update(actual)
        return item

    changes = []
    for item in raw['changes']:
        if not isinstance(item, dict) or set(item) != {'criterion', 'title', 'impact', 'claim_type', 'before', 'after', 'basis'}:
            raise ValueError('invalid brief change fields')
        if item['criterion'] not in known:
            raise ValueError('brief change names an unknown criterion')
        for key in ('title', 'impact'):
            _text(item[key], key)
        if item['claim_type'] not in ('source_fact', 'inference', 'proposal'):
            raise ValueError('change claim_type must distinguish fact, inference or proposal')
        if not isinstance(item['basis'], list) or not item['basis']:
            raise ValueError('change needs cited basis')
        before, after = citation(item['before']), citation(item['after'])
        basis = [citation(ref) for ref in item['basis']]
        diff = '\n'.join(difflib.unified_diff(before['text'].splitlines(), after['text'].splitlines(),
                      fromfile=f"{before['path']}:{before['start']}",
                      tofile=f"{after['path']}:{after['start']}", lineterm=''))
        changes.append({**item, 'before': before, 'after': after, 'basis': basis, 'diff': diff})
    decisions, decision_ids = [], set()
    for item in raw['decisions']:
        if not isinstance(item, dict) or set(item) != {'criterion', 'question', 'owner', 'deferral', 'options'}:
            raise ValueError('invalid brief decision fields')
        criterion = item['criterion']
        if criterion not in known or known[criterion]['kind'] != 'human' or criterion in decision_ids:
            raise ValueError('decision must name a unique human criterion')
        decision_ids.add(criterion)
        for key in ('question', 'owner', 'deferral'):
            _text(item[key], key)
        if not isinstance(item['options'], list) or len(item['options']) < 2:
            raise ValueError('human decision needs at least two meaningful options')
        option_ids = set()
        for option in item['options']:
            if not isinstance(option, dict) or set(option) != {'id', 'label', 'consequence', 'tradeoff'}:
                raise ValueError('invalid decision option fields')
            for key in option:
                _text(option[key], key)
            if option['id'] in option_ids:
                raise ValueError('duplicate decision option id')
            option_ids.add(option['id'])
        decisions.append(item)
    required = {c['id'] for c in criteria if c['kind'] == 'human' and c['status'] != 'pass'}
    if required - decision_ids:
        raise ValueError('brief omits an unresolved human decision: ' + ', '.join(sorted(required-decision_ids)))
    return {**raw, 'changes': changes, 'decisions': decisions, 'sources': sources,
            'stale_sources': sorted(set(stale)), 'path': path}, files


def text_brief(brief, details=False):
    lines = ['## 交付说明（AI整理，原文可追查）']
    if brief['stale_sources']:
        lines.append('说明已过期，请先重新核查：' + ', '.join(brief['stale_sources']))
    lines += [brief['summary'], '']
    for item in brief['changes']:
        lines += [f"### {item['title']} [{item['claim_type']}]", '影响：' + item['impact']]
        for label in ('before', 'after'):
            ref = item[label]
            lines += [f"{label}: {ref['path']}:{ref['start']}-{ref['end']} [{ref['anchor']}]"]
        lines += ['依据：' + ', '.join(f"{r['path']}:{r['start']}-{r['end']} [{r['anchor']}]" for r in item['basis'])]
        if details:
            lines += ['实际行差异：', item['diff'] or '引用行无差异；不能据此声称内容发生变化。']
    for item in brief['decisions']:
        lines += [f"### 待决定：{item['question']}", '负责人：' + item['owner'], '暂不决定：' + item['deferral']]
        for option in item['options']:
            lines += [f"- {option['id']} · {option['label']}：{option['consequence']}；代价/取舍：{option['tradeoff']}"]
    lines += ['限制：' + x for x in brief['limits']]
    if details:
        lines += ['', '## 原文目录（同一引用只保留一次）']
        for ref in brief['sources']:
            lines += [f"[{ref['anchor']}] {ref['path']}:{ref['start']}-{ref['end']}",
                      ref['text'], f"Recorded: {ref['target']} {ref['sha256']} | Current: {ref['current']}"]
    return lines


def html_brief(brief):
    from html import escape as e
    def link(ref):
        return f'<a data-evidence-target href="#{ref["anchor"]}">{e(ref["path"])}:{ref["start"]}-{ref["end"]}</a>'
    warning = ('<p role="alert"><strong>说明已过期，请先重新核查：</strong>' + e(', '.join(brief['stale_sources'])) + '</p>') if brief['stale_sources'] else ''
    parts = ['<section><h2>交付说明（AI整理，原文可追查）</h2>' + warning + '<p>' + e(brief['summary']) + '</p>']
    for item in brief['changes']:
        labels = {'source_fact':'来源事实', 'inference':'推断', 'proposal':'建议'}
        parts += [f'<article><h3>{e(item["title"])} · {labels[item["claim_type"]]}</h3><p>影响：{e(item["impact"])}</p>']
        parts += ['<p>之前：' + link(item['before']) + ' · 现在：' + link(item['after']) + '</p>']
        parts += ['<p>依据：' + ' · '.join(link(r) for r in item['basis']) + '</p>',
                  '<details><summary>查看实际行差异</summary><pre>' + e(item['diff'] or '引用行无差异；不能据此声称内容发生变化。') + '</pre></details></article>']
    for item in brief['decisions']:
        parts += [f'<article><h3>待决定：{e(item["question"])}</h3><p>负责人：{e(item["owner"])}</p><p>暂不决定：{e(item["deferral"])}</p><ul>']
        for option in item['options']:
            parts += [f'<li><strong>{e(option["id"])} · {e(option["label"])}</strong>：{e(option["consequence"])}<br>代价/取舍：{e(option["tradeoff"])}</li>']
        parts += [f'</ul><p>在判据 {e(item["criterion"])} 的反馈中写明选择或问题；不会自动批准或执行。</p></article>']
    parts += ['<ul>' + ''.join('<li>'+e(x)+'</li>' for x in brief['limits']) + '</ul></section>',
              '<section><details id="source-index"><summary>原文目录（引用点击后展开定位）</summary>']
    for ref in brief['sources']:
        numbered = '\n'.join(f'{ref["start"]+i}: {line}' for i,line in enumerate(ref['text'].splitlines()))
        parts += [f'<details id="{ref["anchor"]}"><summary>{e(ref["path"])}:{ref["start"]}-{ref["end"]}' + ('（来源已变）' if ref['stale'] else '') + f'</summary><pre>{e(numbered)}</pre><p>记录SHA：<code>{e(ref["sha256"])}</code></p></details>']
    parts += ['</details><noscript>无JavaScript时，请手动展开原文目录和对应引用。</noscript></section>']
    return ''.join(parts)
