from pathlib import Path
import sys
source=Path("policy.txt").read_text()
draft=Path("draft.txt").read_text()
print("source:", source.strip())
print("draft:", draft.strip())
if source != draft:
    print("FAIL: draft does not match current synthetic policy")
    sys.exit(1)
print("PASS: draft matches current synthetic policy; exception policy remains a human decision")
