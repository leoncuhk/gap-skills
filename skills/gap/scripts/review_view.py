"""Offline views of one observed checkpoint; no independent state or approvals."""
from html import escape
import json


def render_text(data):
    lines = [f"# {data['purpose']}", f"Source: {data['source']}",
             f"Contract revision: {data['revision']} | Observation: {data['observation_sha256']}",
             f"Run: {data['run']['status']} | Artifact ready: {data['artifact_ready']}",
             f"Independent acceptance: {data['independent_acceptance']}",
             'Human judgment pending: ' + (', '.join(data['waiting_for_human']) or 'none recorded'), '']
    for item in data['criteria']:
        lines += [f"## {item['id']} — {item['status']} ({item['kind']})", item['claim']]
        lines += ['- ' + reason for reason in item['reasons']]
        lines += [f"- Evidence: {file['path']} | recorded: {file['target']} {file['sha256']} | current: {file['current']}" for file in item['evidence']]
        if item['note']:
            lines += ['Observed: ' + item['note']]
    lines += ['', 'Feedback must quote the observation and criterion ID. It does not authorize actions.', data['limits']]
    return '\n'.join(lines) + '\n'


def render_html(data):
    cards = []
    for index, item in enumerate(data['criteria']):
        evidence = ''.join(f"<li><code>{escape(f['path'])}</code><br>Recorded target: <code>{escape(f['target'])}</code><br>Recorded SHA-256: <code>{escape(f['sha256'])}</code><br>Current: <code>{escape(json.dumps(f['current'], ensure_ascii=False))}</code></li>" for f in item['evidence']) or '<li>No recorded evidence.</li>'
        reasons = ''.join(f'<li>{escape(r)}</li>' for r in item['reasons'])
        cards.append(f'''<section class="criterion" data-status="{escape(item['status'])}" id="criterion-{index}">
<h2>{escape(item['id'])} <span class="status">{escape(item['status'])}</span></h2>
<p>{escape(item['claim'])}</p><p class="sub">Kind: {escape(item['kind'])} · By: {escape(item['by'] or 'not recorded')}</p>
<ul>{reasons}</ul><details><summary>Inspect evidence for {escape(item['id'])}</summary>
<p>{escape(item['note'])}</p><ul>{evidence}</ul></details>
<label for="decision-{index}">Feedback for {escape(item['id'])}</label>
<select id="decision-{index}"><option value="">No feedback</option value="question">Question</option><option value="correction">Correction</option><option value="agree">Agree with this evidence</option></select>
<label for="note-{index}">Reason / correction for {escape(item['id'])}</label><textarea id="note-{index}" rows="2"></textarea></section>''')
    payload = json.dumps({'version': 1, 'observation_sha256': data['observation_sha256'],
                          'ids': [i['id'] for i in data['criteria']]}, ensure_ascii=False).replace('<', '\\u003c')
    return '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Gap evidence review</title><style>
:root{font:16px/1.55 system-ui,sans-serif;color:#172b3a;background:#f2f5f7}body{max-width:1000px;margin:auto;padding:24px}h1{font-size:2rem;line-height:1.2}h2{font-size:1.15rem}section,header,aside{background:white;border:1px solid #b9cbd5;border-radius:10px;padding:20px;margin:16px 0}code{overflow-wrap:anywhere;font-size:.86em}.sub{color:#435c6a}.status{font-size:.85rem;border:1px solid #657f8d;border-radius:5px;padding:3px 8px;margin-left:8px}.criterion[data-status="stale"],.criterion[data-status="fail"]{border-left:6px solid #ae3c28}label{display:block;margin-top:12px}textarea,select{font:inherit;box-sizing:border-box;width:100%;padding:8px;border:1px solid #718694;border-radius:5px}button{font:inherit;padding:9px 15px;background:#174c65;color:white;border:0;border-radius:6px;margin:8px 8px 8px 0}summary,button{cursor:pointer}button:focus-visible,summary:focus-visible,textarea:focus-visible,select:focus-visible{outline:3px solid #cc6900;outline-offset:3px}#output{min-height:180px}svg{max-width:100%;height:auto}input[type=checkbox]{width:18px;height:18px;vertical-align:middle}li{margin:8px 0} @media(max-width:520px){body{padding:12px}header,section,aside{padding:14px}h1{font-size:1.5rem}}@media print{button,.controls,label,select,textarea{display:none}.criterion[hidden]{display:block}details{display:block}body{padding:0}section{break-inside:avoid}}
</style><header><p class="sub">GAP · observed evidence, not an approval</p><h1>''' + escape(data['purpose']) + '''</h1><p>Source: ''' + escape(data['source']) + '''</p><p>Contract revision: ''' + str(data['revision']) + '''</p><p>Observation: <code>''' + escape(data['observation_sha256']) + '''</code></p>
<p><strong>Run:</strong> ''' + escape(data['run']['status']) + ''' · <strong>Artifact ready:</strong> ''' + str(data['artifact_ready']) + '''</p><p><strong>Independent acceptance:</strong> ''' + escape(data['independent_acceptance']) + '''</p><p><strong>Human judgment pending:</strong> ''' + escape(', '.join(data['waiting_for_human']) or 'none recorded') + '''</p>
<details><summary>How to read this evidence</summary><svg viewBox="0 0 720 95" role="img" aria-label="Declared sources support criteria; receipts are checked against current files. A receipt is not authorization."><g fill="#e6eff4" stroke="#174c65"><rect x="5" y="15" width="195" height="55" rx="8"/><rect x="265" y="15" width="195" height="55" rx="8"/><rect x="525" y="15" width="190" height="55" rx="8"/></g><g fill="#172b3a" font-family="system-ui" font-size="17"><text x="30" y="49">Declared sources</text><text x="288" y="49">Task criteria</text><text x="551" y="49">Actual receipts</text><text x="217" y="49">→</text><text x="478" y="49">←</text></g></svg><p>Inspect each criterion’s evidence paths, target identities and current status. This schematic explains the declared relationship; it does not prove causal or business truth.</p></details></header>
<div class="controls"><label><input id="problems" type="checkbox"> Show only unresolved criteria</label></div>''' + ''.join(cards) + '''
<aside><h2>Return review feedback</h2><p>This exports local feedback only. It does not send, publish, approve or change the task. The agent must recheck the observed version before using it.</p><button id="prepare">Prepare feedback JSON</button><button id="download">Download prepared JSON</button><p id="message" role="status" aria-live="polite"></p><label for="output">Export preview / copy manually if download is unavailable</label><textarea id="output" readonly></textarea><noscript>Use the text view and return the observation ID, criterion ID and your note; interactive export needs JavaScript.</noscript></aside><footer>''' + escape(data['limits']) + '''</footer>
<script type="application/json" id="binding">''' + payload + '''</script><script>
'use strict';
const binding=JSON.parse(document.getElementById('binding').textContent);
const message=document.getElementById('message'), output=document.getElementById('output');
function prepare(){
 output.value='';
 const feedback=[];
 for(let i=0;i<binding.ids.length;i++){
  const decision=document.getElementById('decision-'+i).value;
  const note=document.getElementById('note-'+i).value.trim();
  if(!decision && !note)continue;
  if(!decision || !note){message.textContent='Choose a decision and provide a reason for each edited criterion.';return null;}
  feedback.push({criterion:binding.ids[i],decision,note});
 }
 if(!feedback.length){message.textContent='Add feedback to at least one criterion.';return null;}
 const text=JSON.stringify({version:1,observation_sha256:binding.observation_sha256,feedback},null,2);
 output.value=text;message.textContent='Prepared locally. Includes all edited criteria, even when filtered. Nothing has been applied.';return text;
}
binding.ids.forEach((id,i)=>['decision-','note-'].forEach(prefix=>document.getElementById(prefix+i).addEventListener('input',()=>{output.value='';message.textContent='Feedback changed; prepare again before returning it.';})));
document.getElementById('problems').addEventListener('change',event=>document.querySelectorAll('.criterion').forEach(el=>el.hidden=event.target.checked && el.dataset.status==='pass'));
document.getElementById('prepare').addEventListener('click',prepare);
document.getElementById('download').addEventListener('click',()=>{
 const text=prepare();if(!text)return;
 let url;
 try{url=URL.createObjectURL(new Blob([text],{type:'application/json'}));const a=document.createElement('a');a.href=url;a.download='gap-feedback.json';a.click();message.textContent='Download requested. The same JSON remains in the preview; verify your saved file.';}
 catch(error){message.textContent='Download unavailable. Copy the complete JSON from the preview.';}
 finally{if(url)setTimeout(()=>URL.revokeObjectURL(url),1000);}
});
</script></html>'''


def validate_feedback(payload, data):
    if not isinstance(payload, dict) or set(payload) != {'version', 'observation_sha256', 'feedback'} or payload['version'] != 1:
        raise ValueError('invalid feedback envelope')
    if payload['observation_sha256'] != data['observation_sha256']:
        raise ValueError('stale feedback: re-open current evidence and recheck the proposed decision')
    known = {c['id'] for c in data['criteria']}
    seen = set()
    if not isinstance(payload['feedback'], list) or not payload['feedback']:
        raise ValueError('feedback must contain at least one entry')
    for item in payload['feedback']:
        if not isinstance(item, dict) or set(item) != {'criterion', 'decision', 'note'}:
            raise ValueError('invalid feedback entry')
        if not isinstance(item['criterion'], str) or item['criterion'] not in known or item['criterion'] in seen:
            raise ValueError('unknown or duplicate feedback criterion')
        if item['decision'] not in ('question', 'correction', 'agree') or not isinstance(item['note'], str) or not item['note'].strip() or len(item['note']) > 5000:
            raise ValueError('invalid feedback decision or note')
        seen.add(item['criterion'])
    return {'feedback': payload['feedback'], 'observation_sha256': data['observation_sha256'],
            'applied': False, 'authorization': False,
            'next': 'Treat notes as review input. Verify provenance and meaning; continue only within existing authorization.'}
