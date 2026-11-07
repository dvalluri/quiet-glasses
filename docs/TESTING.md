# Testing

## Execute

From the installed repository root:

```bash
.venv/bin/python -m pytest -q
.venv/bin/python -m pip check
```

No real AI service or glasses are needed. HTTP provider tests use `httpx.MockTransport`; Lua tests execute the real project script inside the official emulator. Window coverage uses SDL dummy, not a visible desktop. CLI coverage uses a POSIX subprocess pipe.

## Suites

| File | What it verifies |
| --- | --- |
| `tests/test_hud.py` | Blank startup, streamed pixels/timing, cancellation, single-button dismissal, stale generations/sequences, malformed packets, provider failure clearing, missing draw acknowledgment timeout, bounded ASCII layout, endpoint rejection, virtual window rendering/Space |
| `tests/test_provider.py` | SSE request/content, auto selection and fallback; HTTP 500, redirect, malformed JSON and missing DONE failures |
| `tests/test_hardware_contract.py` | Panel state is awake before drawing; forced Bluetooth send exceptions do not prevent startup or local button clear |
| `tests/test_cli.py` | `/quit` exits mock CLI cleanly within subprocess timeout |

Fault-injected hardware contracts are emulator tests, not evidence of a radio connection, offline physical boot or panel behavior. Some branches (long-button injection, real disconnect, full deadline expiry, CLI save/input errors) have no dedicated automated coverage.

## Latest reproducible audit result

On **2026-11-06**, Linux, Python 3.12.12, halo-emulator 2.3.0, pytest 9.2.0, pytest-asyncio 1.4.1.post1:

```text
23 passed in 3.19s
No broken requirements found.
```

Final repeat: 23 passed in 3.19s (initial audit: 3.22s). The launcher also completed mock `/ask hello` → `/dismiss` → `/quit` with exit 0 under SDL dummy. `bash -n launch` passed, and all 10 Markdown documents had zero broken local file links. This run used the existing virtual environment. A clean package download/install, current real Ollama request and person-visible window were not revalidated in the restricted handoff environment. Historical real-demo evidence is preserved separately in [EXPERIMENTS.md](EXPERIMENTS.md).

## Performance methodology

`HUD.activate` samples `time.perf_counter()` before dismissing previous work. Metrics therefore include any previous cleanup and activation handshake:

| Metric | Endpoint |
| --- | --- |
| `first_provider_ms` | First yielded provider content chunk |
| `first_display_ms` | First nonempty snapshot draw acknowledgment received from Lua |
| `first_visible_ms` | First nonblack window image immediately after `pygame.display.flip()` |
| `failed` | Stream or draw path exception occurred |

Provider chunks need not correspond to tokenizer tokens. Acknowledgment timing includes inference/layout/transport/Lua round trip; window timing adds GUI scheduling. Neither measures compositor scanout or photon emission. The stream timeout is 60 seconds, activation/draw acknowledgment wait is one second, and redraw/window loops target at most 30 Hz.

For the deliberate real-model run and captures:

```bash
.venv/bin/python scripts/verify_demo.py
```

This requires the default local Ollama model and desktop access; it overwrites `artifacts/real-demo/`. The script measures injected button to observed blank framebuffer by polling at approximately 2 ms; this is not physical button latency. It captures the scaled window, unlike CLI `/save`.

For new benchmarks, record versions, host CPU/GPU/RAM, model settings, cold/warm state, display driver, prompt, repeated samples and failures. Report distributions only from recorded samples. The existing reports do not provide hardware inventory, sample distributions or sustained throughput. Do not compare synthetic latency to real inference as equivalent measurements.

## Limitations

The suite cannot establish optics, BLE fragmentation/order/loss, pairing security, firmware upload, battery, thermals, model correctness, physical gesture reliability or physical display latency. Timing assertions are smoke-test bounds, not performance guarantees. See [hardware acceptance procedure](HARDWARE.md).
