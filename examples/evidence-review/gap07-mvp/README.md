# Inspectable synthetic delivery snapshot

Open the [HTML review](review.html), read the [compact text](review.txt), or inspect the [full text evidence](review-details.txt). All three bind the same observation.

Check the correction from 21 to 17 and which requests changed or stayed the same. Follow source links to original excerpts and actual line differences, then inspect Mei's two shipping choices, cost, arrival timing and consequence of deferral. With JavaScript disabled, expand the native source disclosures manually. Feedback is local review input; it neither authorizes nor performs shipping. Browser interaction and human comprehension remain unverified.

These are retained 0.7.0 presentation snapshots, including their original Chinese narrative and labels, not examples of the current English UI. They were rendered after the four solver runs without changing the original brief, checkpoint or business output. See [provenance.json](provenance.json) for source and renderer identities. The unabridged original views and task state remain in the local ignored `tests/results/2026-10-06-gap07-evidence.tar.gz`; that bundle is not distributed through GitHub. Do not substitute a display snapshot for the task's source of truth.

If you have the original bundle, extract into a new directory and use the helper against `runs/dev/enhanced`: `view --brief deliverables/brief.json`; add `--details` for full text. Summary and details must share the observation; if they differ, recheck. `check` exits 1 while Mei's decision remains pending. For a reproducible example from a public checkout alone, use the [repository demo builder](../README.md); it exercises stale evidence and feedback, not the original four-arm experiment.
