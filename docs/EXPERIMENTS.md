# Experiments and engineering log

Preserve measured evidence separately from interpretation. Existing artifacts and the earlier README/environment notes were audited on **2026-11-06**. The original reports contain no wall-clock date, machine inventory, model digest or full dependency snapshot. Their run dates and unrecorded commands cannot be reconstructed as fact. No artifacts were deleted or overwritten for this handoff.

## Historical synthetic HUD observation

Evidence: local `artifacts/metrics.json`, `artifacts/blank.png`, `artifacts/response.png`.

| Metric | Recorded value |
| --- | ---: |
| First provider chunk | 22.709 ms |
| First Lua draw acknowledgment | 26.214 ms |

The earlier README identifies this as a mock measurement. The JSON alone does not identify provider, command or versions; no script reproducing these exact files is present. A fresh functional mock demo is `./launch --provider mock`; the automated HUD test measures the same timing fields but does not recreate this artifact run. These numbers are not local-model performance.

## Historical real Ollama desktop demonstration

Evidence: `artifacts/real-demo/report.json` and four numbered PNGs. Existing report identifies Ollama `gpt-oss:20b`, X11, public question “In two short sentences, why does the sky look blue?” and blank-after-dismissal=true.

Reproduction from repository root, in a desktop terminal with that local model already available:

```bash
.venv/bin/python scripts/verify_demo.py
```

This is the current reproduction command; no shell transcript proves the original invocation. The script uses a hardcoded endpoint/model and overwrites its five output files. Archive them separately before rerunning if comparison is needed. Artifacts are Git-ignored and may not accompany a source clone.

| Metric | Recorded value |
| --- | ---: |
| Activation → first content | 3686.742 ms |
| Activation → first draw acknowledgment | 3688.308 ms |
| Activation → first nonblack window flip | 3705.402 ms |
| Acknowledged snapshots | 41 |
| Injected button → observed blank framebuffer | 2.469 ms |

Earlier environment notes record Python 3.12.12, pygame 2.6.1 and SDL 2.28.4, and state the model had already served a verification request. This is one warm observation, not a cold-start or statistically representative benchmark. The record says no weights were downloaded/changed and no SDK internals modified; those historical actions cannot be independently reconstructed from this snapshot. Window flip does not establish photon timing. Polling contributes to button timing. See [measurement definitions](TESTING.md).

## Historical warnings, failures and fixes

The original [ENVIRONMENT.md](../ENVIRONMENT.md) is retained verbatim as historical evidence. It records:

- `Failed to create stream fd: Operation not permitted` reproduced with systemd-cat without importing the project. Login-shell input-method logging was identified as the source. A non-login shell avoided the warning; no shell configuration was changed.
- Restricted local socket creation prevented Ollama access; restricted downloads failed DNS. The notes report approved outside-sandbox inference/X11 execution. This handoff has not repeated that privileged execution.
- ptrace investigation inside the restricted sandbox failed. The external trace was recorded as successful, but its raw trace is not included.
- Threaded console input reportedly hung during executor shutdown. Current code uses asynchronous POSIX stdin; clean `/quit` is now covered by a subprocess test. Original failing code/transcript is unavailable.

Commands retained in the earlier record include `curl http://127.0.0.1:11434/api/tags` and `/usr/bin/systemd-cat -t quiet-glasses-check /usr/bin/true`. Treat these as recorded investigations, not new measurements. No warning suppression or SDK patch was introduced.

## Documentation audit — 2026-11-06

Commands executed against this workspace:

```bash
.venv/bin/python --version
.venv/bin/python -m pip list
.venv/bin/python -m pip check
.venv/bin/python -m quiet_glasses.cli --help
.venv/bin/pytest -q
git -C ../quiet-glasses-sdk rev-parse HEAD
```

Observed: Python 3.12.12; SDK commit `9d17e96ce1b0f1d33d270315a3816d2e8cd0523b`; **23 passed in 3.22s**; no broken requirements. pip warned that its cache directory was not writable and disabled caching; dependency checks still succeeded.

Relevant installed versions: halo-emulator 2.3.0, httpx 0.28.1, pytest 9.2.0, pytest-asyncio 1.4.1.post1, lupa 2.8, pygame 2.6.1, Pillow 11.3.0, numpy 2.5.4, lz4 4.4.5. brilliant-ble 3.5.1 and bleak 3.0.2 are present but unused by the application. These are observed versions, not a lockfile.

Source, configuration, all four test modules, launcher, verification script and available experiment reports were inspected. `git status --short` failed because the exposed project `.git` directory contains no accessible metadata. Therefore project commit history, remote, provenance and tracked-file status cannot be audited here. The external SDK commit was readable. There is no project LICENSE or CI configuration in the visible source.

Fresh online installation, current real inference, current person-visible window and all physical-device behavior remain unverified in this audit. Existing tests use mocked HTTP and virtual SDL. No physical compatibility or new benchmark claim follows from this run. [Hardware](HARDWARE.md) defines the next acceptance procedure.

### Final documentation validation

Repeated `.venv/bin/python -m pytest -q`: **23 passed in 3.19s**. `bash -n launch` passed. A local Markdown-link check across README, ENVIRONMENT and eight docs found zero broken relative file links.

A subprocess ran `./launch --provider mock` with `SDL_VIDEODRIVER=dummy`, submitted `/ask hello`, waited one second, then submitted `/dismiss` and `/quit`; it exited 0. Reported synthetic timings were first-provider 25.261 ms, first-draw 27.618 ms and virtual-window flip 38.451 ms. This was a functional startup check, not a visible desktop experiment or a benchmark. No historical artifact was overwritten.
