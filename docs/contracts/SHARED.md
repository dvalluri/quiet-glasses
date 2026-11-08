# Shared service contracts v0.1

Status: target contracts. Existing implementations and wire semantics remain authoritative for current behavior until an adapter or extraction is implemented and tested. No HTTP service deployment is implied.

## Common rules

- Session is the sole owner of increasing request generations `g` and display snapshot sequence `s`. Reserve generation 0 for the initial clear/no-request state; activations allocate positive generations and snapshots use positive sequences. Providers do not invent IDs.
- At most one request may produce display writes and one display snapshot may await acknowledgement. Any abandoned cleanup task is quarantined and cannot write, even if it ignores cancellation. Display receives complete snapshots, not token deltas. Cancelled work cannot acquire a new generation.
- Lifecycle commands are serialized. Local dismissal is a priority event: clear first, then best-effort notification and cancellation; no wait for inference.
- Producer work ends once with completed, cancelled, or failed status, independently of display visibility. Completion may leave its answer visible until dismissal; later dismissal changes visibility without emitting a second producer outcome. Only still-running work is cancelled on dismissal. Failures attempt clear. A broken link means blankness is unknown until locally observed.
- Transport `send` acceptance is not device processing. `DRAWN` is completion of drawing calls, not proof of optical visibility. Dismissal is not secure erasure.
- Current defaults: activation/draw acknowledgement 1 second; total answer 60 seconds; local HTTP connect 2 seconds and read 30 seconds. Proposed provider cleanup budget: 1 second. These are software deadlines, not measured physical performance.
- Cleanup timeout reports failure without blocking local clear or accepting stale output. A provider that ignores cancellation must be isolated from future display writes.
- No automatic text replay after reconnect. Current v1 has no connection epoch; a new host session cannot assume its reset generation counter is safe against a still-running device. Until a verified reset/handshake exists, reject recovery rather than reuse uncertain state.
- No implicit prompt/answer persistence or telemetry. Evidence uses public fixtures and explicit capture. Preserve provider mode in every UI and report.

## Target domain records

These are semantic records, not newly implemented Python classes or a new wire protocol.

```text
ContentRequest(mode, user_input, source_ref?, target_language?)
  → TextTask(kind=literal|inference, text, source_ref?, constraints)
  | ContentError(code, detail)

TextProvider.stream(prompt: str) → AsyncIterator[str]

DisplayFrame(generation, sequence, complete_text)
DisplayEvent(kind=ready|active|drawn|dismissed, generation?, sequence?)
TransportFailure(kind=startup|disconnected|timeout|delivery|runtime, detail)

VerificationReport(candidate_commit, contract_version, environment,
  checks[{criterion, outcome=pass|fail|blocked, evidence}], limitations)
```

Session associates tasks and errors with its request generation; an untagged late result from another task is never applied to the current request.

## Compatibility and changes

Preserve the existing Halo ASCII protocol through the first extraction. Propose changes with consumer impact, migration, and a contract test. Integrator coordinates compatible amendments; principal decides incompatible product or cross-service changes. Services return an explicit unsupported error for unavailable capabilities; no silent substitution of Q&A for translation or synthetic output for real inference.
