"""Build an actual synthetic stale-evidence review, with real local check receipts."""
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
HELPER = ROOT / 'skills/gap/scripts/checkpoint.py'
target = Path(sys.argv[1]).resolve()
target.mkdir(parents=True, exist_ok=False)
(target/'policy.txt').write_text('Synthetic policy: cancellation window = 14 days.\n')
(target/'draft.txt').write_text('Synthetic policy: cancellation window = 14 days.\n')
check = subprocess.run([sys.executable, '-c', "from pathlib import Path; assert Path('policy.txt').read_bytes()==Path('draft.txt').read_bytes(); print('PASS: synthetic draft matches source at time of check')"], cwd=target, text=True, capture_output=True)
assert check.returncode == 0
(target/'verification.txt').write_text(check.stdout)
contract = {'purpose': 'Review the current cancellation explanation and identify the remaining human decision',
            'source': 'Synthetic demo request; never real customer policy',
            'semantics': ['Use current source, preserve original draft for comparison', 'No external publishing authorized'],
            'inputs': ['policy.txt'], 'criteria': [
                {'id': 'current-explanation', 'claim': 'Draft matches the current policy', 'kind': 'artifact'},
                {'id': 'exception-policy', 'claim': 'Owner decides whether an exception route is appropriate', 'kind': 'human'}]}
(target/'contract.json').write_text(json.dumps(contract, indent=2))
base = [sys.executable, str(HELPER), '--root', str(target), '--state', str(target/'state.json')]
def run(*args):
    result = subprocess.run(base+list(args), text=True, capture_output=True)
    if result.returncode: raise RuntimeError(result.stdout+result.stderr)
    return result
run('init', '--contract', str(target/'contract.json'))
run('record', '--criterion', 'current-explanation', '--kind', 'artifact', '--result', 'pass', '--by', 'synthetic-local-check', '--receipt', 'verification.txt', '--file', 'draft.txt', '--note', 'Actual byte comparison passed before the source changed.')
run('end', '--reason', 'Earlier process stopped; source subsequently updated.')
(target/'policy.txt').write_text('Synthetic policy: cancellation window = 21 calendar days.\n')
run('view', '--format', 'html', '--output', str(target/'review.html'))
run('view', '--format', 'text', '--output', str(target/'review.txt'))
print(target/'review.html')
