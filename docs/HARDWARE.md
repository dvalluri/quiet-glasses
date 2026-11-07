# Hardware compatibility and first-device plan

## Assessment as of 2026-11-06

**Quiet Glasses is an emulator prototype, not a deployable physical Halo application.** The host instantiates `EmulatorTransport` directly; there is no transport selector, BLE adapter, uploader or physical reconnect path. A local installation of brilliant-ble does not change this.

| Requirement | Verified status |
| --- | --- |
| SDK checkout | `9d17e96ce1b0f1d33d270315a3816d2e8cd0523b`, halo-emulator 2.3.0 |
| Project Lua execution and rendering | Tested only in that emulator |
| Physical firmware version | None tested; minimum compatible release unknown |
| Lua API needs | Display clear/show/text/set_font/set_pan/power_save, button single/long, Bluetooth callback/send/is_connected, sleep |
| Physical host requirements | BLE-capable host and OS Bluetooth access; SDK integration still required |
| AI connectivity | Inference stays on host; server uses loopback HTTP, not glasses networking |

The pinned emulator README describes firmware 0.8.8 semantics in several areas. That is not a minimum firmware certification for Quiet Glasses. Record the actual device version and test each required API before claiming compatibility.

## Upstream evidence

The official [Halo Lua reference](https://raw.githubusercontent.com/brilliantlabsAR/docs/main/halo/halo-sdk-lua.md), checked during this audit, describes a round 256×256 display with direct writes, RGB colors and button callbacks. Its system constants expose hardware and firmware identity. These are upstream capabilities, not project hardware test results.

The official [Bluetooth protocol](https://github.com/brilliantlabsAR/halo-firmware/blob/main/applications/halo/PROTOCOL.md) requires negotiated-MTU-aware handling and makes USERDATA fragmentation/reassembly the application's responsibility. Consequently the project's 240-byte emulator packet ceiling cannot be treated as a proven physical payload limit. Use the [SDK](https://github.com/brilliantlabsAR/brilliant_sdk/tree/9d17e96ce1b0f1d33d270315a3816d2e8cd0523b) rather than implementing a new radio stack.

Firmware build and OTA guidance exists in the official [firmware repository](https://github.com/brilliantlabsAR/halo-firmware). No firmware flashing procedure was exercised for this project; do not infer a required update or flash an arbitrary release from the emulator pin. Upstream references can change and should be checked against the chosen device firmware.

## Display and emulator differences

The app uses white ASCII text on a black framebuffer, six lines at native Dogica 8 px. Halo's round viewport may constrain optical readability even when pixels fit. Black pixels do not demonstrate optical transparency. Direct clear-and-redraw may produce visible flicker absent from screenshots.

The emulator models fonts/pixels and callback injection, not optics, head motion, display scanout, actual gestures, power consumption, heat or BLE delivery. `show()` is a no-op; panel power state is tracked without gating emulator rendering. Contract tests force panel/send failures to expose some hidden assumptions but cannot replace device measurements. The script keeps the loop awake and has no host-loss watchdog. A host stall may leave text visible until local dismissal.

## Purchase readiness

Recommend **one device only as an explicitly experimental developer prototype**, provided its cost is acceptable and the owner is prepared to implement and test a physical transport. Do not purchase on the assumption that this repository is ready to deploy or that optical comfort has been proven. Before ordering, confirm current availability, supported firmware, pairing/upload/recovery instructions and return policy directly with the vendor. No current price, stock or shipping claim is made here.

## Exact first-device acceptance sequence

This is a planned procedure, not a record of execution. Steps requiring a new adapter are blocked today; there is no honest end-to-end deploy command to provide.

1. On the host, run `.venv/bin/python -m pytest -q` and `./launch --provider mock`; verify blank → text → Space dismissal. Keep this baseline before touching hardware.
2. Record date, device model, host OS/Bluetooth adapter, SDK commit and tool versions. Pair using the vendor's instructions for the installed firmware. Capture `frame.HARDWARE_VERSION`, `frame.FIRMWARE_VERSION` and, if available, `frame.GIT_TAG` through the official SDK Lua console. Keep device identifiers out of public logs.
3. Before overwriting device files, inventory and back up the existing device application with supported SDK tooling. Confirm recovery/interrupt access. Do not perform a firmware update solely for this test.
4. Using the matching SDK example, draw one short white text string, clear it, and exercise single/long button callbacks. Record API errors, legibility, focus, clipping and clear behavior. Stop and resolve API incompatibilities before loading the project script.
5. Implement the missing physical adapter as a separately reviewed development task: script upload/start, USERDATA routing, notifications, negotiated packet sizing/reassembly, timeouts, disconnect and cleanup. Preserve the existing HUD interface and protocol semantics. Test with mock first; installing brilliant-ble alone is insufficient.
6. Upload the unchanged `quiet_glasses/device/main.lua` with the verified tooling and start it. Require blank startup and `READY`; send `A|1`, expect `ACTIVE|1`; send `T|1|1|Hello Halo`, expect visible text and `DRAWN|1|1`; press the actual button, require immediate local blank and `DISMISSED|1`. Repeat with long press.
7. Send late `T|1|2|LATE` and `A|1`; require blank. Send `A|2`, then `T|2|1|Second trial`; require text. Send `D|2`; require blank and acknowledgment. Exercise maximum six-line snapshots only after negotiated payload handling is verified.
8. Test dismissal while the host/provider is blocked, forced host termination, out-of-range/disconnect and reconnect. Record whether the last text remains; a stalled host is a known unresolved case. Confirm a working local clear path every time before wearing the device for extended tests.
9. Connect local AI only after mock protocol success. Repeat the public sky question. Record content, acknowledgment and physical display observations separately; use synchronized external observation for any photon-latency claim.
10. Record repeated failures as well as successes, ambient lighting, readability during movement, flicker, comfort, battery and heat over a documented interval. Set acceptance thresholds before the trial; none have yet been established. Add the firmware-specific results to [EXPERIMENTS.md](EXPERIMENTS.md) before changing compatibility claims.

The upload/adapter gap in steps 4–6 prevents a copy-paste full-device test today. Exact SDK commands must be validated against the acquired hardware and firmware, rather than invented in this handoff.
