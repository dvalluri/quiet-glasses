# Quiet Glasses

Quiet Glasses is an experimental, blank-by-default text HUD for AR glasses. A Python host streams short answers from a local AI server; a Lua app renders them in the Brilliant Labs Halo emulator. **No physical glasses have been tested, and no physical BLE transport is implemented.**

The vision is a quiet, user-controlled interface: brief text and eventually diagrams, visible only when requested and immediately dismissible. The current release is text-only. See [product decisions](docs/DECISIONS.md) and the [roadmap](docs/ROADMAP.md).

## Status

| Capability | Evidence and limits |
| --- | --- |
| Blank startup, streamed text, cancellation, dismissal, stale-packet rejection | Implemented; automated emulator tests pass |
| Local OpenAI-compatible SSE and automatic mock fallback | Implemented; mocked HTTP tests pass; historical real Ollama demo preserved |
| Desktop window and Space dismissal | Implemented; SDL dummy test passes; historical X11 captures available |
| Panel wake and Bluetooth-send failure handling | Emulator fault-injection tests only |
| Physical Halo deployment and radio communication | Not implemented or demonstrated |
| Optical readability, battery, head-motion stability | Unverified on hardware |
| Reader, manual scrolling, translation, diagrams, spatial annotations | Not implemented; planned |

Latest audit: **23 tests passed on 2026-11-06**. See [testing](docs/TESTING.md) for environment and coverage. Host code requires Python 3.11+ and a POSIX console; Linux/Python 3.12 is the validated environment.

## Quick start

From the repository root, with Git, Python and package download access:

```bash
git clone https://github.com/brilliantlabsAR/brilliant_sdk.git ../quiet-glasses-sdk
git -C ../quiet-glasses-sdk checkout 9d17e96ce1b0f1d33d270315a3816d2e8cd0523b
python3 -m venv .venv
.venv/bin/python -m pip install -e ../quiet-glasses-sdk/python/packages/halo_emulator -e '.[test]'
.venv/bin/python -m pytest -q
./launch --provider mock
```

The project repository URL is not available in this workspace; obtain the source from its maintainer before these steps. The synthetic provider always returns the same sample, irrespective of the question. For local AI, run `./launch` with an already-running Ollama server and installed `gpt-oss:20b` model. The terminal reports LOCAL or MOCK FALLBACK. Full [setup](docs/SETUP.md) includes explicit local mode and troubleshooting.

## Demo

In the launched terminal, enter:

```text
/ask In two short sentences, why does the sky look blue?
/dismiss
/quit
```

Pause after `/ask` to watch the answer stream. Focus the window and press Space to dismiss at any point. See [usage](docs/USAGE.md) for all controls and screenshot instructions.

Historical captures are kept under `artifacts/real-demo/`: `01-blank.png`, `02-first-visible.png`, `03-answer.png`, `04-dismissed.png`, and `report.json`. Artifacts are ignored by Git and may be absent from a fresh checkout. The [experiment log](docs/EXPERIMENTS.md) preserves their findings and reproduction command.

## Repository map

| Path | Purpose |
| --- | --- |
| `quiet_glasses/core.py` | HUD lifecycle, layout, emulator transport, timing |
| `quiet_glasses/providers.py` | Synthetic and local SSE providers, selection |
| `quiet_glasses/cli.py` | POSIX console and pygame viewer |
| `quiet_glasses/device/main.lua` | Device-side drawing and dismissal |
| `quiet_glasses/__init__.py` | Package marker |
| `launch` | Start project virtual environment with a window |
| `scripts/verify_demo.py` | Explicit real-model screenshot/timing experiment |
| `tests/` | Four test modules; see testing guide |
| `pyproject.toml` | Packaging, dependencies, CLI entry point, pytest configuration |
| `artifacts/` | Existing local experiment output; ignored by Git |
| `ENVIRONMENT.md` | Preserved historical sandbox investigation |
| `docs/` | Architecture, setup, usage, tests, hardware, roadmap, decisions, experiments |

## Handoff and contribution

Read [architecture](docs/ARCHITECTURE.md), [testing](docs/TESTING.md), and [hardware readiness](docs/HARDWARE.md) before modifying the host/device protocol. Run the existing suite after changes; report environment and evidence separately for emulator and hardware results. Prefer a small, complete prototype over extra infrastructure.

Source is published at [dvalluri/quiet-glasses](https://github.com/dvalluri/quiet-glasses). CI configuration and a dependency lockfile have not been added.

## License

Copyright 2026 Dinesh Valluri. Quiet Glasses is licensed under the [Apache License 2.0](LICENSE); see [NOTICE](NOTICE) for attribution.

Commercial use, modification, and distribution are permitted, including proprietary products, subject to the license's notice and redistribution requirements. The license includes an explicit contributor patent grant and does not require publishing modifications. These permissions apply to everyone, including commercial competitors, and already granted permissions cannot simply be withdrawn. Third-party dependencies, fonts, services, and model weights retain their own terms.
