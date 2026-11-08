# Transport service v0.1

Owner: Transport Codex agent.

## Boundary

Input: connection/deployment commands and complete application message bytes.
Output: complete ordered replies, connection identity/capabilities, or explicit startup/disconnect/timeout/delivery/runtime failure. This byte boundary is the Halo transport contract. A Quest backend maps its actual rendering/input events into the shared semantic display events through an adapter; define and test that local boundary before implementation, without imposing fictitious Halo wire acknowledgements.

During the emulator extraction preserve `start()`, `send(bytes)`, `receive() -> list[str]`, `close()`. Calls must be bounded and nonblocking in the host loop. A physical asynchronous adapter requires a coordinated interface amendment; do not hide blocking radio waits behind this surface.

## Obligations

- Own SDK pairing/upload/start and transport lifecycle; distinguish each result. Successful pairing is not successful deployment.
- Deliver complete messages in order. Handle fragmentation/reassembly inside the adapter using negotiated backend limits. Never truncate a message.
- Existing emulator maximum is 240 bytes; it is not a physical BLE MTU. Advertise verified application payload capacity or reject unsupported frames before sending.
- A successful send means transport acceptance only. Never synthesize ACTIVE, DRAWN, or DISMISSED to hide device failure.
- Close is idempotent and releases SDK/resources. Report receiver failure promptly. Do not replay stale frames after reconnect.
- Require a verified fresh session/reset before using reset host generations against a persistent device. Otherwise remain disconnected and report the reason.
- Record backend, SDK and firmware versions. Keep personal device identifiers out of public evidence.

## Ownership and acceptance

After extraction: `quiet_glasses/transports/`, assigned transport tests and backend setup procedure. Integrator owns the current EmulatorTransport extraction from `core.py`.

Checks: complete-message round trip; oversize rejection; startup failure; receiver failure; fragmentation boundaries where supported; disconnect and bounded cleanup; no reconnect replay. Emulator tests do not establish physical message delivery.

First dispatch: identify and reproduce the existing Quest browser path with Display, documenting host↔browser delivery and limitations. Quest is a distinct backend; the Halo ASCII adapter remains supported for emulator testing. Park physical Halo implementation until it is the chosen target.
