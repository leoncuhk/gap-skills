# Independent repair verification — a8965bad4e2d788662f0aa930bd793a4ff7e4eb3

Reviewed repair diff from 12a9915 and reran the original independent reproducer against an archive of a8965ba. Both findings are resolved in the tested cases.

- P2: changing only consulted experience now changes observation_sha256; old feedback exits 2; check still identifies experience.md as stale. Both text and HTML surface experience path, declared scope/use, reason and stale files. Criterion evidence continues to distinguish recorded and current identities. Actual outputs are probe-results.json, feedback-after-experience.stdout.txt and probe-task/review-after.txt.
- P3: Boolean and float schema versions are rejected. Additional independent validation used the fresh current observation and rejected true, 1.0, "1", null, list and object versions, avoiding a false pass caused merely by stale observation. See independent-repair-controls.json.
- Valid and rejected feedback remain read-only. The source-change negative control remains correct. Original prior findings/results are preserved in review-round1.

Repository validation and 30 tests passed with actual stdout retained in this directory. No additional blocking issue found within the reviewed scope; no acceptance threshold was weakened. This is the first code repair follow-up, not a new solver context. Browser/render QA remains unavailable under the existing tool restriction; no workaround was attempted. Functional JS unit evidence is not browser evidence. Human effort or usability benefit remains unmeasured.
