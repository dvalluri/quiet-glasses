# Quiet Glasses: principal and agent team

Status: proposed service boundaries v0.1, prepared 2026-11-08. This change defines contracts and dispatch instructions; it does not refactor runtime code or establish new hardware results.

## Authority

Dinesh is the principal: product purpose, priorities, target wearable, user experience, acceptance of demonstrated usability, and incompatible interface changes.

The coordinating Codex agent is the integrator: translates the chosen milestone into bounded assignments, resolves dependencies, owns shared contracts and wiring, reviews work, and assembles one runnable candidate. Routine compatible changes proceed within the assigned scope. Verification reports evidence independently; it cannot waive a failed criterion.

Service agents own implementation choices inside their contract. They do not invent product requirements, change peers' interfaces, or declare their own physical compatibility. Roles persist in the repository; Codex workers are launched for specific tasks, not continuously running background services.

## Ownership and contracts

| Service / Codex role | Input → output | Exclusive responsibility | Contract |
| --- | --- | --- | --- |
| Session | User action + text task → lifecycle, display commands, status | One active request, ordering, cancellation, deadlines | [Session](contracts/SESSION.md) |
| Content | Explicit content request → literal text or inference task | Source identity, mode validation, output constraints | [Content](contracts/CONTENT.md) |
| Inference | Prompt → asynchronous content chunks | Local-model integration, completion, provider provenance | [Inference](contracts/INFERENCE.md) |
| Transport | Complete message bytes → complete replies or transport error | Connection, SDK deployment, framing, bounded delivery | [Transport](contracts/TRANSPORT.md) |
| Display | Versioned display commands + local input → pixels and events | Layout, blank state, rendering, local dismissal, stale suppression | [Display](contracts/DISPLAY.md) |
| Verification | Candidate + acceptance profile → evidence report | Independent integration checks and claim limits | [Verification](contracts/VERIFICATION.md) |

These are independently owned logical services in one application. Start with direct calls and the current device protocol. The existing external AI server remains behind Inference. The agents build and maintain the components; they are not needed for runtime operation.

## Current mapping and file ownership

| Existing location | Current behavior | Owner before extraction | Proposed location after extraction |
| --- | --- | --- | --- |
| `quiet_glasses/core.py` | HUD, layout, emulator transport | Integrator only | `session.py`, `rendering.py`, `transports/emulator.py` |
| `quiet_glasses/providers.py` | Mock/local providers and selection | Inference | Same |
| `quiet_glasses/device/main.lua` | Halo Lua rendering and input | Display | Same |
| `quiet_glasses/cli.py`, `launch`, packaging | Application wiring and startup | Integrator | Same |
| No content module | Generic question passed to provider | Content proposes; no runtime edits yet | `quiet_glasses/content/` |
| Existing tests and verification script | Unit/contract tests and desktop demo | Assign individual files before edits | Owner unit tests; Verification integration tests |

The integrator mechanically extracts shared code before parallel implementation touches it. Extraction must preserve the existing imports through a compatibility shim or update all internal consumers together. Display owns layout policy after extraction; Transport cannot truncate content to satisfy delivery limits. Existing test files also require one assigned editor each.

## Evidence baseline

At source revision `83a86b2fa5b91891fd1c6b8486e28f82fd3ee80a`, repository documentation records 23 tests passing on November 6, a historical real Ollama desktop demonstration, and emulator-only Halo transport. These checks were not rerun to produce these contracts.

The latest conversation records a Quest 3S browser passthrough demonstration: classify as quest-browser / user-reported, not native Quest evidence. No Quest implementation or reproducible Quest procedure was found in this repository during this review. Physical Halo transport, optics, and button behavior remain unverified.

## First dispatch

Current milestone: one repeatable wearable text interaction. Working target is the already-owned Quest 3S, following the latest project discussion; Halo implementation remains parked. Native Quest rendering is a proposed path, not an established dependency. Transport and Display first identify the smallest reproducible path from the reported browser demo and report any required platform decision with evidence. Do not build two backends concurrently.

1. Integrator: preserve the emulator baseline and perform a behavior-preserving extraction only when implementation starts.
2. Content: supply one short public ASCII fixture and one bounded question; reader, translation, and guide modes stay disabled.
3. Inference: document the existing provider boundary and supply deterministic mock behavior; do not add models.
4. Transport + Display: reproduce the selected wearable path, then static text and local dismissal. First establish the adapter seam; a Quest browser is a separate backend, not Halo Lua running on Quest.
5. Verification: prepare the acceptance profile and reproduce software checks when the environment supports them; record hardware-dependent checks as blocked.
6. Integrator: assemble one candidate; after static text succeeds, attach the existing streamed provider and repeat the same interaction.

Provisional acceptance profile v0.1 (engineering targets, not measured results or principal-approved usability thresholds): blank startup; explicit activation; one readable short text; local dismissal while host/provider is stalled; late updates cannot redisplay; ten repeated cycles with results recorded. Target application-observed input → blank is at most 250 ms, to be measured rather than assumed. Record physical gesture → callback delay separately. Human observation is required for readability. A browser-panel pass must be named as such; native spatial or Halo compatibility requires its own evidence.

## Assignment and report template

```text
Assignment: <service role, contract v0.1, bounded task>
Base revision / branch:
Allowed files:
Dependencies / frozen inputs:
Required outputs:
Acceptance commands or manual steps:
Out of scope:
Report: result commit; changed files; pass/fail/blocked criteria;
        environment + provenance; evidence paths; limitations;
        dependency requests; smallest next action.
```

The integrator consolidates this into the weekly status: demonstrated functionality, actual wearable observations, blockers, and one next milestone. No new evidence means no claimed progress.
