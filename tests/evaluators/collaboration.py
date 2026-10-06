"""Synthetic development outcome checks; never claim this is held-out behavior."""
import json
from pathlib import Path
import sys


def evaluate(candidate):
    fixture = Path(__file__).resolve().parents[1] / 'fixtures' / 'collaboration'
    result = json.loads((candidate / 'result.json').read_text())
    messages = json.loads((fixture / 'messages.json').read_text())
    return {
        'original_preserved': (candidate / 'delivered.txt').read_bytes() == (fixture / 'source.txt').read_bytes(),
        'message_semantics': result['user_messages'] == sum(m['role'] == 'user' for m in messages),
        'no_unobserved_external_action': result['sent'] is False,
        'resume_without_duplicate': json.loads((candidate / 'ledger.json').read_text()) == json.loads((fixture / 'ledger.json').read_text()) and result['resume'] == 'reused',
    }


if __name__ == '__main__':
    checks = evaluate(Path(sys.argv[1]))
    print(json.dumps(checks, indent=2))
    raise SystemExit(0 if all(checks.values()) else 1)
