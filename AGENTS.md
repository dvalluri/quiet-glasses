# Quiet Glasses agent instructions

Dinesh is the principal. The coordinating Codex agent is the integrator. Each assigned Codex worker owns one service contract; worker identities are per-run, while the roles below persist.

Read [team and dispatch](docs/AGENT_TEAM.md), [shared contracts](docs/contracts/SHARED.md), and your assigned service contract before changes. Existing runtime behavior is documented in [architecture](docs/ARCHITECTURE.md); proposed contracts are not evidence that new interfaces exist.

## Working rules

- Work on the smallest assigned acceptance slice. Prefer integration, repeatable tests, and a usable single prototype.
- The integrator may delegate independent work to service agents and coordinate isolated branches/worktrees. One owner edits each file. Do not delegate speculative feature expansion.
- Until extraction is explicitly assigned, only the integrator edits `quiet_glasses/core.py`. It currently combines session, layout, and transport.
- Routine compatible implementation decisions belong to agents and the integrator. Dinesh owns product priorities, target wearable, experience, and incompatible contract changes. Bring a concrete proposed change and tradeoff when principal direction is needed.
- Shared contracts and composition-root changes belong to the integrator. Never silently change another service's input, output, failure, or ordering semantics.
- Keep one runnable application with local interfaces and existing SDKs. Separate processes, network APIs, queues, and deployment infrastructure need a demonstrated requirement.
- Device-local dismissal must not depend on inference, a host response, or a successful notification. Suppress stale results after dismissal.
- Preserve explicit LOCAL / MOCK / MOCK FALLBACK provenance. No silent synthetic success.
- Label evidence by environment and provenance. Emulator tests, SDK capabilities, and drawing acknowledgements do not establish physical compatibility or readability.
- Run checks appropriate to changed behavior. Document commands and failures. Hardware acceptance remains blocked without physical observations.
- Do not merge or declare a release accepted merely because a service agent says done. The integrator assembles a candidate and independent verification report.

## Handoff

Every worker returns: service and contract version; base and result commit; owned files changed; acceptance criteria with pass/fail/blocked evidence; limitations; dependency requests; and the smallest remaining action. See the dispatch template in the team document.
