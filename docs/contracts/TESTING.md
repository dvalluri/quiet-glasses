# Testing — agreement v0.1

Tries the assembled app and records what actually worked, what failed, and which hardware claims still lack evidence.

Assigned Codex agent: Testing. Reports evidence to the coordinating agent and Dinesh.

## Boundary

Input: Candidate(commit, contract_version, dependency versions, environment, commands) and AcceptanceProfile(criteria, expected outcomes).
Output: VerificationReport with pass/fail/blocked for every criterion, evidence references, limitations, and release recommendation.

Own integration checks, `scripts/verify_demo.py`, verification documentation and proposed evidence manifests. Each service owns its assigned unit tests. Existing shared tests require explicit per-file assignment.

## Evidence contract

Use two independent fields:

| Field | Values |
| --- | --- |
| Environment | mock, emulator, desktop-real-model, quest-browser, quest-native, halo-physical |
| Provenance | current-run, historical-artifact, user-reported, planned |

Also record separate backend (mock/headless, emulator, desktop, quest-browser, quest-native, halo-physical) and provider_mode (none, MOCK, LOCAL, MOCK FALLBACK) fields so a wearable mock run cannot appear to prove wearable real-model inference. Record commit, observation date, command/manual steps, versions, expected/actual outcomes, artifact reference, and limits. A source inspection is a code claim, not an executed test. SDK documentation is a dependency capability, not application evidence. A planned test has no observed outcome.

## Obligations

- Reproduce relevant checks on the candidate when the environment supports them; report unavailable prerequisites as blocked.
- Keep software-only, real-model and physical observations distinct. A passing mock cannot satisfy a real-model criterion.
- Missing physical evidence blocks wearable acceptance even if every emulator test passes.
- Test cancellation, stale suppression and failures, not just the happy path.
- Preserve existing public fixture artifacts and record failure cases alongside success. Do not capture private conversations by default.
- A recommendation does not merge or publish a release. Integrator assembles the candidate; principal accepts product usability and public compatibility scope.

## First dispatch and acceptance

Prepare/reproduce the documented software baseline, then independently check blank → static text → local dismissal → rejected stale output. Physical criteria remain blocked until a named backend is actually tested.

Using the provisional acceptance profile v0.1, for the chosen wearable record ten cycles, readability, application-input-to-clear timing, physical gesture recognition separately, host/provider stall and notification/link failure behavior. If static text passes, repeat with the existing real streamed provider. A browser-only result remains a browser result.

Weekly handoff: completed demonstrated behavior; new wearable observations; blockers; one smallest next milestone. If no new evidence exists, say so without promoting planned behavior.
