# Display service v0.1

Owner: Display Codex agent.

## Boundary

Inputs: activation, complete text snapshots, clear, and device-local input.
Outputs: framebuffer/render operations and ready/active/drawn/dismissed events.

Own `quiet_glasses/device/`, proposed `quiet_glasses/rendering.py`, a selected Quest display adapter if assigned, and their unit tests. Integrator extracts the existing host layout first.

## Current Halo ASCII v1

| Input | Required semantics / reply |
| --- | --- |
| Startup | Clear and register callbacks before READY |
| A\|g | Activate strictly newer generation, blank, reset sequence; ACTIVE\|g |
| T\|g\|s\|text | Draw only matching active generation and increasing sequence; DRAWN\|g\|s |
| D\|g | For g at least current generation, clear/deactivate; DISMISSED\|g |
| Local button | Clear/deactivate before best-effort DISMISSED notification |

Current limits: printable ASCII, host layout 28 columns × six lines, Lua text limit 174 bytes. Existing normalization loses unsupported characters; this is not multilingual support. Unparseable generation/sequence and stale commands are ignored; v1 is not a strict grammar validator. Current parsing can accept trailing activation/clear fields and clips excess lines. A stricter grammar or new ERROR wire response requires a contract change.

## Obligations

- Start blank and remain blank until explicit activation.
- Local dismissal clears without inference, host availability, notification delivery, or host acknowledgement.
- A dismissed generation cannot be reactivated/redrawn. Old or non-increasing snapshots cannot replace newer text.
- DRAWN means drawing calls completed. Readability, optics, gesture timing, and spatial stability each need physical observation.
- A Quest adapter must emit genuine equivalent semantic lifecycle events, clearly labelled browser or native. Only the Halo adapter serializes the ASCII wire protocol; Quest need not execute Lua or emit fictitious Halo device acknowledgements.
- Host-loss watchdog behavior is proposed work; current source does not implement it.

## Acceptance and first assignment

Check blank startup, static snapshot, stale/repeated activation rejection, local dismissal under host stall and notification failure, and ten repeated physical cycles for the selected backend. Measure application-observed dismissal ≤250 ms as a target, separately recording physical input recognition delay. Report failures.

First dispatch: with Transport, reproduce the reported Quest browser display, establish a local clear path and one public static fixture. Capture readability and dismissal evidence before attaching streaming. Native spatial rendering remains a separate unverified capability.
