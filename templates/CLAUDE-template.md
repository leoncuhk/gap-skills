# Project: <name>

## Stack
<language, framework, package manager — one line each>

## Commands
- verify: `<test cmd>` — also wired as a PostToolUse hook; the hook is authoritative
- build: `<cmd>`
- run: `<cmd>`

## Conventions
<2–5 lines: naming, structure, style — judgment calls only.
Any rule that MUST hold belongs in a hook, not here.>

## Boundaries
- Surgical changes: every changed line traces to the request.
- Simplicity first: no speculative abstractions, no unrequested features.
- State assumptions before implementing; if interpretations diverge, present them — don't pick silently.

## State
- Task working memory: TERRA.md ledgers (terra), deleted after merge.
- Durable decisions: docs/adr/ — graduate hard-to-reverse whys there.
