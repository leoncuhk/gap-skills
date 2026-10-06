# Evidence review examples

Current entry: [gap07 HTML](gap07-mvp/review.html), [compact text](gap07-mvp/review.txt), [full evidence text](gap07-mvp/review-details.txt), and [provenance](gap07-mvp/README.md). These are synthetic snapshots, not live task state or real user approval.

`build_demo.py` remains a repository-only generator for a smaller stale-receipt mechanism demonstration. Run it with a new output directory; it does not rebuild the current gap07 delivery example.

## Historical examples and recovery

The old `mvp/` (0.6) and `usage-acceptance-2026-10-06/` (0.6.1) directories were moved out of the active examples after all 40 files matched commit `f62ba401eedaad65ed80afece8ebf1ab00f262ed` byte-for-byte. The [manifest](../../tests/results/2026-10-06-legacy-examples-manifest.json) records every hash and the local ignored archive hash. Every archived file was extracted to a new directory and verified before removal. Prior failures, original receipts, historical reports and all pre-existing evidence bundles remain retained.

To inspect the historical examples from Git, run from this repository (the destination is new):

```sh
restore_dir=$(mktemp -d /tmp/gap-history.XXXXXX)
git archive f62ba401eedaad65ed80afece8ebf1ab00f262ed | tar -x -C "$restore_dir"
```

The complete frozen tree includes its matching helper. Alternatively, extract the local ignored `tests/results/2026-10-06-legacy-examples-evidence.tar.gz` into a new directory for just the original two example directories. That bundle's SHA-256 is `5c69c15ac74ed9f89ac21ef8202dbc76188db7977d6ccfed871c1270b0641886`.

Historical paths such as `mvp/review.html`, `mvp/review.txt`, `mvp/qa-receipt.json`, and `usage-acceptance-2026-10-06/{acceptance.json,DELIVERY.md,result.json,execution.jsonl}` refer to this restored tree. Retained checkpoint JSON contains original roots and fingerprints: it is historical evidence, not a live checkpoint for the cleaned HEAD. Do not rewrite those identities to manufacture a current pass. For executable archive replays follow each original report's bundle instructions; Git alone does not contain the ignored agent-run bundles.
