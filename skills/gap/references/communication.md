# Communication artifacts

Choose the lightest medium that makes the important relationship easy to inspect.

## Markdown or HTML

Use concise Markdown for linear reasoning, short plans, ordinary reports, and a few findings. Use one self-contained HTML artifact when the reader must compare several alternatives, inspect a diagram or map, explore dense evidence, tune parameters, review a long plan, or understand a UI/prototype spatially.

HTML earns its cost only when interaction or layout materially improves understanding. Do not turn a short answer into a web page.

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

Match the venue: short Markdown for chat/PR, self-contained HTML for long or interactive review. Accessibility, readable contrast, keyboard navigation, and printable fallback are part of correctness for an HTML artifact.
