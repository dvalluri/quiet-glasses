# Who does what

This is a proposed way to divide the work, written on 2026-11-08. The app has not been split into these parts yet.

**You decide what Quiet Glasses should do and whether it feels useful. I coordinate the work and put the pieces together.** Each Codex agent gets one part, a small task, and a clear test for being done.

## The six parts

| Name | What it does | What it hands to the next part |
| --- | --- | --- |
| **App** | Handles “ask,” “dismiss,” and replacing one question with another. Stops old work so old answers cannot reappear. | A current request, or a clear/stop instruction |
| **AI** | Talks to Ollama and receives the answer a little at a time. Reports when the model fails or when a mock is being used. | Answer text, completion, or an error |
| **Connection** | Gets commands and text from the host to the selected headset/backend, and brings events back. | Delivered messages, replies, or a connection error |
| **Screen** | Fits text on the display, draws it, and clears it when dismissed—even if the host is stuck. | Display/input events and visible results to test |
| **Reader** | Eventually loads a document, prepares pages, or prepares a translation/field-guide request. For now, supplies test text only. | Prepared text or a question with its source |
| **Testing** | Tries the assembled app, checks failure cases, and records what actually worked on each device. | Pass/fail/blocked results with evidence |

These names describe parts of one app. Codex agents work on them when assigned a task; the product does not require six agents running while you use it.

## One example

You ask “What does this sign mean?”

- **App** starts the request and cancels an older one.
- **Reader**, once that feature exists, prepares the supplied sign text and requested language. Reading the camera image/OCR is not built yet.
- **AI** generates the answer.
- **Connection** carries updates to the selected headset/backend.
- **Screen** shows the text. If you dismiss it, Screen clears locally; App stops the answer and rejects late updates.
- **Testing** checks that this sequence actually works, including when AI or the connection fails.

That is the intended flow. The current prototype supports asking a text question and showing streamed text in the Halo emulator; general sign translation is not implemented.

## Where the code lives

| Code today | Responsible agent | Intended home after the first extraction |
| --- | --- | --- |
| HUD in `quiet_glasses/core.py` | App | `quiet_glasses/session.py` |
| Layout in `quiet_glasses/core.py` and device Lua | Screen | `quiet_glasses/rendering.py`, `quiet_glasses/device/` |
| Emulator transport in `quiet_glasses/core.py` | Connection | `quiet_glasses/transports/emulator.py` |
| `quiet_glasses/providers.py` | AI | Same |
| No document-reading module yet | Reader, parked | `quiet_glasses/content/` |
| Integration tests, demo checks, evidence | Testing | Existing tests/scripts/docs plus assigned additions |
| CLI, launch, shared interfaces, wiring | Me, coordinating | Existing composition code |

For now only I edit `core.py`, because it holds three of these parts. I extract those boundaries before assigning overlapping code work. Each test file also has one editor at a time.

## What we do next

One goal: **a repeatable text interaction on one wearable.** The working target is your Quest 3S, following the latest discussion. Connection and Screen first reproduce the reported browser demo and identify the smallest reliable path. Browser and native results are recorded separately. Halo hardware work stays parked.

| Part | First task |
| --- | --- |
| App | Preserve the existing behavior while separating the shared code |
| AI | Keep the current Ollama interface and provide a clearly labelled deterministic mock |
| Connection | Establish a reproducible way to get text to the chosen wearable/backend |
| Screen | Show one short text and make local dismissal work while the host is stalled |
| Reader | Supply a public test sentence and one question; then stay parked |
| Testing | Check the software baseline, then record the same interaction on the wearable |

Provisional test: blank startup → explicitly requested text → readable display → local dismissal → late text cannot bring it back. Try ten cycles. The proposed application-input-to-clear target is 250 ms; this is not a measurement or an approved usability threshold. Measure physical gesture recognition delay separately. Only after static text works do we attach streamed AI.

OCR, translation, diagrams, navigation, and world anchoring wait until that interaction works.

## What “done” means

An agent returns its changed files/revision, the test it ran, the actual result, what remains blocked, and the smallest next action. A compatible implementation choice is the agent's to make. If a change affects what you see, the chosen hardware, or another part's agreed interface, I bring you the concrete change and tradeoff.

I assemble a runnable candidate; Testing checks it; you judge whether the demonstrated experience is useful. Passing emulator tests does not establish a working physical headset.

Current evidence: repository revision `83a86b2fa5b91891fd1c6b8486e28f82fd3ee80a` records 23 tests passing on November 6, historical real-Ollama desktop output, and Halo emulator behavior. These tests were not rerun for the naming change. The Quest browser demo is user-reported; no reproducible Quest setup was found in this repository. Native Quest and physical Halo behavior remain unverified.

## Detailed agreements

Each agreement records inputs, outputs, ownership, failure behavior, and how to test it:

[Shared rules](contracts/SHARED.md) · [App](contracts/APP.md) · [AI](contracts/AI.md) · [Connection](contracts/CONNECTION.md) · [Screen](contracts/SCREEN.md) · [Reader](contracts/READER.md) · [Testing](contracts/TESTING.md)
