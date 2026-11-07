# Roadmap

Milestones below are evidence-based states, not promised dates.

## Completed in software

- Python host with bounded ASCII layout and explicit request activation.
- Lua blank-by-default HUD with generation/sequence rejection and local dismissal.
- Official Halo emulator transport, framebuffer viewing and screenshot capture.
- Synthetic provider, local SSE provider, explicit automatic fallback reporting.
- Cancellation, failure clearing, emulator contract tests and clean CLI exit.
- Recorded real Ollama/X11 experiment; 23 automated tests pass at handoff.

## Current state

A Linux/POSIX emulator demonstration is reproducible with the installed environment. A clean online installation remains to be verified. No physical deployment has been established. Before public release, choose a project license, establish a source remote/history and decide how to distribute ignored experiment artifacts. No application features were added in the documentation audit.

## Next milestone: one physical prototype

Follow the [hardware sequence](HARDWARE.md). First confirm SDK pairing/recovery and installed firmware APIs, then implement a minimal physical transport using existing SDK libraries. Demonstrate blank startup, static text and reliable local dismissal before streaming AI. Measure negotiated payload behavior, disconnect/reconnect, optics and power. Publish exact versions and observed failures; only then claim device compatibility.

Prioritize known CLI input/save error handling and host-stall behavior when preparing that milestone. These are acknowledged gaps, not fixes delivered here.

## Subsequent product work

1. Reader: deliberate document loading, bounded pages and explicit next/previous controls; currently no file ingestion or navigation.
2. Translation: user-initiated text translation after a suitable glyph/font strategy. ASCII-only output cannot support general multilingual reading.
3. Diagrams: small, readable monochrome diagrams alongside text; no diagram renderer exists today.
4. Longer term, spatial annotation: investigate sensing, pose tracking and anchoring only after a usable physical text prototype. Fixed HUD coordinates are not world anchors.

Keep privacy controls, immediate dismissal and one physical prototype as constraints. Expand complexity only when a demonstrated product need requires it. See [decisions](DECISIONS.md).
