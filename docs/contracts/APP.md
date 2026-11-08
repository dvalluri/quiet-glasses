# App — agreement v0.1

Handles asking, dismissing, and replacing a question. Keeps the current answer moving through the app and stops an old answer from coming back.

Assigned Codex agent: App. The coordinating agent handles the shared file until it is split.

## Boundary

Inputs: start, explicit activation with a nonblank question or Reader TextTask, dismissal, close, provider chunks, display events, and transport failures.

Outputs: lifecycle status and timing/error metadata; calls to AI; versioned activation/snapshot/clear commands to Screen through its backend. No prompt/answer logging by default.

Existing public surface to preserve during extraction:
`start()`, `activate(prompt) -> asyncio.Task`, `dismiss()`, `close()`.
The Reader task input is a proposed extension behind an adapter, not an existing API.

## Obligations

- Serialize activation/replacement/dismissal; allocate strictly increasing generations.
- Clear the old request before activating a new one. Cancel its producer, and reject its late output even if cancellation is ignored.
- Bound text accumulation to the existing 4096-character window; delegate layout to Screen policy. Maintain one outstanding draw acknowledgement and the current 30 Hz maximum redraw rate.
- Queue remote clear before awaiting provider cleanup. Target cleanup has a separate 1-second budget; timeout is reported.
- On local dismissal, mark the generation inactive immediately and cancel upstream work; do not wait for a host round trip to clear.
- Surface receive-task failure to lifecycle/UI status immediately. Do not leave a dead receiver masquerading as a running request.
- Preserve the shared deadlines and accurately distinguish provider, draw-acknowledgement, and observed pixel timings.
- Close cleans up tasks and transport even after failed startup or cancellation.

## Ownership and acceptance

After extraction: `quiet_glasses/session.py`, assigned session unit tests. Before extraction: request changes to the integrator; do not concurrently edit `core.py`.

Required checks: blank → activation → streamed text → dismissal; overlapping activation ordering; replacement cancellation; provider ignoring cancellation; missing acknowledgement; receive failure; failed clear; bounded close. Late chunks and queued snapshots must never revive a dismissed generation.

First task: define a fake provider/backend interaction fixture for the extraction. No new UI or features.
