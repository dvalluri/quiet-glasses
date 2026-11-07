# Setup

## Supported environment

Use Linux with a POSIX terminal and Python 3.11+; the audited installation uses Python 3.12.12. A desktop session with SDL display access is required for the visible window. Headless emulator tests need no glasses, camera, microphone, cloud account or model. Windows console support is not implemented; macOS has not been validated.

## Install

Obtain the Quiet Glasses source and enter its root. No project clone URL can be verified from this snapshot. Install the pinned external SDK beside it:

```bash
git clone https://github.com/brilliantlabsAR/brilliant_sdk.git ../quiet-glasses-sdk
git -C ../quiet-glasses-sdk checkout 9d17e96ce1b0f1d33d270315a3816d2e8cd0523b
python3 -m venv .venv
.venv/bin/python -m pip install -e ../quiet-glasses-sdk/python/packages/halo_emulator -e '.[test]'
.venv/bin/python -m pip check
.venv/bin/python -m pytest -q
```

Do not overwrite an existing SDK checkout with local changes. The pin provides `halo-emulator==2.3.0`. Project runtime also requires `httpx>=0.27,<1`; test extras install pytest and pytest-asyncio. Emulator dependencies include lupa, numpy, Pillow, lz4 and pygame (pygame-ce on Python 3.14+). There is no lockfile: the SDK pin does not freeze all transitive versions. No SDK modifications are required.

The existing virtual environment and dependency consistency were verified during this handoff. A clean online install was not performed: this environment restricts network access. Python 3.11 minimum is declared rather than separately tested. See [recorded versions](EXPERIMENTS.md).

## Start

```bash
./launch --provider mock
```

`launch` selects `.venv/bin/python`, changes to the project root and adds `--window`. After installation this is one-command startup, not one-command installation. From another working directory use the path to `launch` in your checkout.

For a headless console (no visible rendering window):

```bash
.venv/bin/python -m quiet_glasses.cli --provider mock
```

## Local AI

Start your local Ollama service separately and install a suitable model using its own instructions. This project neither installs Ollama nor downloads weights. The historical demonstration used the exact model ID `gpt-oss:20b`; resource requirements depend on the server/model and are not measured here.

```bash
./launch
./launch --provider local --endpoint http://127.0.0.1:11434/v1/chat/completions --model gpt-oss:20b
```

The first command auto-selects LOCAL or announces MOCK FALLBACK; the second requires local inference and reports request failures. Run either command, not both simultaneously. For another compatible loopback server:

```bash
./launch --provider local --endpoint http://127.0.0.1:8080/v1/chat/completions --model YOUR_MODEL
```

Optional configuration (CLI flags take precedence):

```bash
export QUIET_GLASSES_ENDPOINT=http://127.0.0.1:11434/v1/chat/completions
export QUIET_GLASSES_MODEL=gpt-oss:20b
./launch
```

`localhost`, remote hosts and HTTPS are rejected; use a literal loopback IP. The server must support the [request fields and SSE format](ARCHITECTURE.md). No API key or `.env` file is used.

## Troubleshooting

| Symptom | Action |
| --- | --- |
| Missing project environment | Create `.venv` and install above; launcher does not use a global Python |
| Cannot import halo_emulator | Check editable SDK installation and pinned checkout |
| MOCK FALLBACK | Confirm local service is reachable and `/v1/models` lists the configured exact ID |
| Provider failed; HUD cleared | Check server logs, request compatibility, `[DONE]` termination and timeouts; try explicit mock |
| Invalid endpoint | Use HTTP with literal loopback address and no credentials/fragment |
| No display / SDL error | Run from a normal desktop session with display permissions; omit `--window` for headless use |
| Headless window testing | Use `SDL_VIDEODRIVER=dummy`; this does not create a person-visible demo |
| Socket/DNS denied | Restricted execution environment; use mock or a normal authorized local terminal |
| Stream-fd warning at shell startup | See preserved [environment investigation](../ENVIRONMENT.md); unrelated to SSE |
| Blank prompt or bad save path | Use a nonempty `/ask` and writable existing parent directory; these errors can terminate CLI |
| Close window but terminal stays open | Expected; enter `/quit` in terminal |

Do not suppress errors or change SDK internals to hide environment restrictions.
