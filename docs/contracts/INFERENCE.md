# Inference service v0.1

Owner: Inference Codex agent.

## Boundary

Input: one prompt string. Output: `stream(prompt) -> AsyncIterator[str]`, yielding content chunks until normal completion or exception. Provider selection returns a provider and explicit mode label.

Own `quiet_glasses/providers.py` and assigned provider tests. Do not own session IDs, page navigation, text layout, device transport, or release claims.

## Obligations

- Preserve LOCAL / MOCK / MOCK FALLBACK labels through the composition root. Mock is deterministic and never claims to answer the question.
- Local mode uses the existing literal-loopback HTTP policy, no redirects or environment proxies; connect timeout 2 seconds and read timeout 30 seconds.
- Consume the supported OpenAI-compatible SSE content subset. Ignore reasoning-only chunks; require DONE; malformed data, non-success HTTP and premature EOF terminate with failure.
- Cancellation closes the client context. Session owns the total 60-second answer deadline and bounded cancellation cleanup.
- Auto fallback is only during explicit provider selection, with its visible label. Once a local answer starts, errors fail the request rather than substitute mock text.
- No prompt/response persistence or autonomous data collection. Server logging is outside this component's guarantees.
- Missing model or unavailable endpoint is a provider-selection failure, not proof that a wearable backend failed.

## Acceptance and first assignment

Mocked tests cover chunks/DONE, reasoning-only events, malformed payload, missing DONE, HTTP failure, unavailable model, timeout, and cancellation. A real-model test is a separately labelled integration observation; no test-only mock counts as real inference.

First task: document/preserve this existing interface and provide one deterministic response for the selected wearable interaction. No model changes, remote services, or new provider expansion.
