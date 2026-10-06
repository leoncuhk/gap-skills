# Communication artifacts

Choose the lightest medium that makes the important relationship easy to inspect.

## Select for the reader’s operation

Use concise Markdown for linear reasoning, short plans, ordinary reports, and a few findings. Text, diagrams, HTML and video are alternative forms, not a ladder of complexity: choose for the reader’s actual question. A static relationship needs only a small source-backed diagram; navigation, comparison or criterion-specific feedback can justify HTML. Use video only when motion, timing or a real procedure is essential and production/verification tools are already available; do not install a media stack to complete an ordinary explanation. Use one self-contained HTML artifact when the reader must compare several alternatives, inspect a diagram or map, explore dense evidence, tune parameters, review a long plan, or understand a UI/prototype spatially.

Do not turn a short answer into a web page.

## Exploration

For visual directions, architectures, or approaches, show genuinely different alternatives. Label the belief and tradeoff behind each. Keep exploration artifacts disposable and separate from production code; their durable output is the decision or criterion learned.

## Plans and architecture

Make the decision structure visible before implementation detail. Useful views include:

- dependency graph for tickets and gates;
- system/component flow for architecture;
- side-by-side alternative comparison;
- risk and evidence matrix;
- collapsible plan with volatile decisions first.

Every visual claim must trace to the same source-of-truth evidence as the text. A diagram is a view, not a second specification.

## Review, demo, and status

Lead with the working behavior or failure evidence, then the problem and chosen bet, the hardest reviewer questions, deviations, residual risk, and explicit non-scope. Group changes by intent rather than file list. Link to durable artifacts and diffs rather than copying them into a second authority.

For a substantive change, a compact before/after comparison can make the claim inspectable: the same input or observation, its source versions, and the actual failing/passing output. If no baseline was run, say so; a hypothetical example or pseudocode is not an execution receipt. Choose evidence for the claim: screenshots show visible state, execution checks show tested behavior, and neither alone proves user benefit. State what rollback reverses, any effects it cannot undo, and the affected users or consumers. Use this only where it helps the reader decide; a small edit needs no fixed report template or diagram.

Match the venue: short Markdown for chat/PR, self-contained HTML for long or interactive review. Accessibility, readable contrast, keyboard navigation, and printable fallback are part of correctness for an HTML artifact.

## Checkpoint review and returned feedback

When an existing gap checkpoint is the source of truth, the installed helper can show it without changing it:

```sh
python3 "$GAP/scripts/checkpoint.py" --root "$TASK" --state "$TASK/state.json" view
# Only when expanding evidence and returning per-criterion feedback helps:
python3 "$GAP/scripts/checkpoint.py" --root "$TASK" --state "$TASK/state.json" view --format html --output "$TASK/review.html"
python3 "$GAP/scripts/checkpoint.py" --root "$TASK" --state "$TASK/state.json" feedback --file gap-feedback.json
```

The default is text. Output files must be new, so a view cannot overwrite source evidence. HTML is an offline view with native disclosures and a local JSON export; it neither sends nor applies feedback. The observation fingerprint binds the contract, state and actual current files, including symlink target identity. Changed files make old feedback stale even when state.json is unchanged. Re-open current evidence and recheck the note; never remove the version binding to force it through. Intake validates IDs/version and returns review input, not approval or a changed criterion. Verify the feedback’s actual provenance and meaning, then continue within existing authorization.

Test the reader’s operation: find the questionable criterion, inspect its source/evidence, state the unresolved decision, modify/export/read back a note, and confirm stale feedback cannot be used as current. Browser checks establish interaction correctness; model reviews or attractive layouts do not establish human understanding, saved review time or business value.

### Source-bound delivery explanation (optional)

When hashes and receipt names do not explain the change, add `--brief brief.json` to **both** `view` and `feedback`. Render text and HTML from that same file. Keep it beside the existing task artifacts. Version 1 schema:

```text
{version: 1, summary,
 changes: [{criterion, title, impact, claim_type: "source_fact"|"inference"|"proposal",
            before: CITE, after: CITE, basis: [CITE]}],
 decisions: [{criterion, question, owner, deferral,
              options: [{id, label, consequence, tradeoff}, ...]}],
 limits: [text]}
CITE = {path, start, end, sha256, target}
```

Citations use canonical root-relative paths, actual full-file SHA-256 and resolved target, with 1-based inclusive spans up to 80 lines in a UTF-8 file up to 512000 bytes. Cite the meaningful exception/context, not a convenient fragment; the helper verifies identity and extracts actual text but cannot judge whether a span supports a claim. Each change names a known criterion and includes at least one basis citation. Distinguish source facts, inference and proposals. Every unresolved human criterion needs its question, decision owner, consequence of deferral, and at least two options with consequences and tradeoffs. This is information for a real decision, never an added approval ritual for settled choices.

The default text view keeps the change, impact, verification, pending decision and material limits, with exact source paths/spans. Add `--details` to the same `view` command (keep the same `--brief` and write a new output) for full original excerpts, computed line differences and a deduplicated receipt directory. Both text modes and HTML bind the same observation. HTML keeps details in the same document, folded by default; source/receipt links open their containing disclosures, focus and scroll to the target. Without JavaScript, manually expand the named native disclosures. Technical fingerprints remain secondary; no evidence or material exception may be deleted to reduce reading length. A changed citation makes the explanation explicitly stale and blocks feedback intake until rechecked, even if checkpoint state has not changed. The user must not treat old narrative paired with newly changed text as a reviewed conclusion. Missing sources fail closed. Source formatting, interaction correctness and information completeness are separate from actual human comprehension, which needs a real reader trial.
