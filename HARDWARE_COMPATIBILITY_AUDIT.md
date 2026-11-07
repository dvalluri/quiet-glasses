# Quiet Glasses v0.1: pre-purchase hardware audit

Checked **2026-11-06**. No device was connected and nothing was purchased.

## Decision: CONDITIONAL GO for one personal development pair

**Buy only if a small glanceable monocular display, a nearby computer, and roughly
half-second physical single-click dismissal are acceptable.** The stock Halo
platform has the APIs needed for our text HUD and local-AI streaming. There is no
evidence that this needs custom hardware, a firmware rewrite, or a replacement AI
architecture. Optical fit/readability remain the largest purchase risks.

**Our existing launcher cannot connect to physical glasses today.** It constructs
`EmulatorTransport` unconditionally. Deployment needs a bounded integration with
the existing `BrilliantBle` SDK: pairing, Lua upload/start, notification delivery,
negotiated packet sizing, and disconnect handling. The inference provider and
text/generation protocol can remain. This is a targeted port, not plug-and-play
compatibility; its size and reliability cannot be guaranteed before device testing.

**NO-GO if your buying requirement is an unchanged executable, a standalone
on-glasses Ollama system, a large comfortable document screen, or physical
single-click dismissal under 100 ms without firmware changes.** The firmware
already waits 400 ms after button release before classifying a single click.
That is independent of our code's speed. [Button configuration](https://github.com/brilliantlabsAR/halo-firmware/blob/0.8.25/boards/arm/halo/halo.dts#L78),
[button classification](https://github.com/brilliantlabsAR/halo-firmware/blob/0.8.25/drivers/input/input_gpio_button.c#L223).

## What to order and budget

| Item | Verified finding |
| --- | --- |
| Required model | **Brilliant Labs Halo**, current retail glasses. Do not substitute Brilliant Labs **Frame**: its display, input and drawing APIs differ. No separate developer-edition requirement is documented. |
| Current advertised price | **US$399 per pair**. This is not a CAD landed price. |
| Availability | Manufacturer product page says **shipping now** and exposes ordering. Destination-specific stock, Canadian delivery time and fulfillment were not confirmed. No checkout was entered. |
| Extra costs | Import taxes can apply on delivery; shipping and prescription-lens charges are not included in this assessment. |
| Fit/return exposure | Manufacturer gives IPD 58–72 mm and optic adjustment +2 to −6 diopters. Nondefect returns incur a US$49 restocking fee plus return shipping; defects are offered exchange. Confirm fit and delivery with the seller before committing. |

Price, availability, fit and return terms are from the [official Halo store](https://brilliant.xyz/products/halo),
read on the audit date. Old US$299 launch/preorder prices and third-party
640×400/20° claims were not used as current purchase specifications. A public
product-JSON request did not yield usable metadata, so no variant SKU or numerical
inventory count is asserted.

## Evidence and version baseline

Evidence labels in this report:

- **Verified in our software**: observed code behavior, tests or existing demo artifacts.
- **Officially implemented/documented**: upstream source or documentation; not a claim we exercised physical hardware.
- **Inference/unverified**: engineering judgment or a wearer/hardware property still needing measurement.

Sources inspected locally and cross-checked against the official repositories:

| Component | Audit baseline |
| --- | --- |
| Our app | `/home/dvalluri/quiet-glasses`, v0.1.0; Python host, Lua device script |
| Official SDK | `9d17e96ce1b0f1d33d270315a3816d2e8cd0523b`; GitHub main was still this commit when checked |
| SDK packages | `halo-emulator` 2.3.0, `brilliant-ble` 3.5.1; optional higher-level `brilliant-msg` 7.3.0 |
| Released firmware | **0.8.25**, published November 4, 2026, commit `cc692f71868e1405a47103b9e199f268a04ce28f` |
| Firmware main inspected | `50d9e57db98773e1beb8bb37780e112eee0f88db`; the display, button, Bluetooth Lua, sleep, board and button-driver files used for conclusions were unchanged from release 0.8.25 |
| Official documentation checkout | `236f9b25acd623529985fe48acf23759537accd1` |

Use stock **0.8.25 as the initial hardware-validation target**, rather than assuming
whatever firmware ships is equivalent. This is a recommended tested-against-source
baseline, not a proven minimum firmware requirement. Fonts changed in 0.8.8; 0.8.10
fixed queued BLE/callback delivery; 0.8.12 fixed app restart/require behavior; later
releases fix display wake and camera interactions. Earlier versions were not
qualified for this app. [Released firmware](https://github.com/brilliantlabsAR/halo-firmware/releases/tag/0.8.25),
[firmware change history](https://github.com/brilliantlabsAR/halo-firmware/blob/0.8.25/CHANGELOG.md).

Firmware update uses signed application images through the existing SDK's BLE SMP
OTA support; there is no reason to build firmware. The official
[OTA example](https://github.com/brilliantlabsAR/brilliant_sdk/blob/9d17e96ce1b0f1d33d270315a3816d2e8cd0523b/python/packages/brilliant_ble/examples/ota_flash.py)
distinguishes test boot from confirmation. Do not use factory-test or bootloader
images as an application update. No update was attempted in this audit.

## Complete API and interaction inventory

This table describes current app code, including the two minimal fixes below.
Sources: [device/main.lua](quiet_glasses/device/main.lua), [core.py](quiet_glasses/core.py),
[cli.py](quiet_glasses/cli.py), [providers.py](quiet_glasses/providers.py),
[verification script](scripts/verify_demo.py), and tests.

| API or mechanism used | Current use | Physical compatibility |
| --- | --- | --- |
| `frame.display.set_font(0, 8, 1)` | Native Dogica regular, 8 px, scale 1 | Implemented in stock firmware; correct post-0.8.8 signature. |
| `frame.display.set_pan(0, 0)` | Fixed screen placement | Implemented; hardware persists this setting. This resets any wearer-selected electronic pan. |
| `frame.display.clear(0x000000)` | Blank startup, redraw, dismissal, disconnected loop | Implemented; writes black pixels, does not itself power off the optic. |
| `frame.display.text(line, 13, 77 + row*16, 0xFFFFFF)` | At most six white text lines | Implemented with 1-based coordinates and integer RGB. |
| `frame.display.show()` | Called after clear/text | Exists but is a **no-op** on Halo, on hardware as well as emulator. It is not a frame swap or wake operation. |
| `frame.display.power_save(false)` | Explicit panel wake, added by this audit | Hardware supported and required when panel is suspended; emulator only tracks the state. |
| `frame.button.single(dismiss)` | Local dismissal | Supported; actual event includes double-click classification delay. |
| `frame.button.long(dismiss)` | Alternative dismissal | Supported for hold ≥1 s and release before 2 s; longer holds are system controls. |
| `frame.bluetooth.receive_callback(func)` | Receives A/T/D app messages | Hardware API; one raw ATT data write maps to one callback on current firmware. |
| `frame.bluetooth.send(message)` | READY, ACTIVE, DRAWN, DISMISSED acknowledgments | Hardware API; can raise when disconnected or sending fails. Now guarded/protected. |
| `frame.bluetooth.is_connected()` | Disconnect blanking and guarded sends | Implemented; actual disconnect recognition includes radio supervision delay. |
| `frame.sleep(0.005)` | Yield/delay in loop | Positive duration is a timed delay in firmware. It is not deep sleep; no battery-life claim follows. |
| Lua standard operations | Local state, tables/strings, patterns, iteration, `tonumber`, `pcall` | Available Lua functionality; app does not depend on desktop `io`, `os`, or `package`. |
| `HaloEmulator(sandbox_dir, print_handler=None)` | Creates virtual device | Emulator-only host object. |
| `load_directory`, `start('main.lua')`, `stop`, `get_error` | Script loading/lifecycle/error observation | Emulator-only; physical equivalents require SDK upload, execution and disconnect lifecycle. |
| `inject_bluetooth_data`, `get_bluetooth_sent` | Simulated data transport | Emulator-only; there is no radio, marker framing, negotiation or bonding here. |
| `get_framebuffer()` | GUI, pixel checks and `/save` | Emulator-only. A physical transport cannot expose this method without a separate host-side mirror; a mirror is not required for deployment. |
| `inject_button_single()` | Space key and automated dismissal | Emulator-only injection of an already-classified event. |
| pygame display/event/image APIs | 512×512 preview of 256×256 buffer, Space dismissal and flip timing | Desktop-only preview, not a glasses API or hardware latency measurement. |
| HTTPX async HTTP + SSE | Ollama `/v1/chat/completions`; `/v1/models` probe; configurable loopback endpoint/model | Host-only; unaffected by Halo transport. No inference runs in the glasses. |
| `launch`, POSIX asynchronous stdin | `/ask`, `/dismiss`, `/save`, `/quit` | Linux terminal interface; no physical-glasses selector exists. |

Hardware API evidence: [display implementation](https://github.com/brilliantlabsAR/halo-firmware/blob/0.8.25/modules/halo/src/lua_display.c),
[Bluetooth implementation](https://github.com/brilliantlabsAR/halo-firmware/blob/0.8.25/modules/halo/src/lua_bluetooth.c),
[button implementation](https://github.com/brilliantlabsAR/halo-firmware/blob/0.8.25/modules/halo/src/lua_button.c),
[timed sleep implementation](https://github.com/brilliantlabsAR/halo-firmware/blob/0.8.25/modules/halo/src/lua_system.c).

No current runtime code uses camera, microphone, audio, IMU, Wikipedia, man pages,
page navigation, bitmap or shape APIs. Tests inject raw messages and button events;
they do not connect BLE. The only declared device-related runtime dependency is
`halo-emulator`; installing `brilliant-ble` for this audit's tests did not add a
physical transport or change the package declaration.

### Existing app protocol

ASCII `A|generation` activates; `T|generation|sequence|text` carries a complete
visible-text snapshot; `D|generation` dismisses. Responses are READY, ACTIVE,
DRAWN and DISMISSED strings with corresponding IDs. Dismissed/stale generations
and non-increasing sequences cannot redraw the HUD. The host awaits an activation
or draw acknowledgment for at most one second; one snapshot is in flight.

Host `layout()` normalizes to printable ASCII, collapses whitespace, wraps at 28
characters, and retains the last six lines from at most 4096 source characters.
Subsequent updates are capped at 30 Hz. These are software choices, not physical
Halo capabilities. Current firmware examples support the same small-host/looping-Lua
pattern. [Official plain-text host and Lua example](https://github.com/brilliantlabsAR/brilliant_sdk/tree/9d17e96ce1b0f1d33d270315a3816d2e8cd0523b/python/packages/brilliant_msg/examples).

## Display suitability

**A compact monochrome answer display is technically viable. Comfortable reading
of our native 8 px text is unverified.** Plan for short answers, not a replacement
monitor or full-page browser.

- **Usable resolution:** 256×256 application framebuffer. The technical hardware
  manual separately describes a 640×480 underlying panel; the larger panel number
  does not grant the application that resolution. The Lua reference describes the
  view as round. The firmware configures a 256×256 RGB framebuffer.
  [Hardware manual](https://github.com/brilliantlabsAR/docs/blob/236f9b25acd623529985fe48acf23759537accd1/halo/hardware.md),
  [framebuffer configuration](https://github.com/brilliantlabsAR/halo-firmware/blob/0.8.25/boards/arm/halo/halo.dts#L204).
- **Optical experience:** the official photo shows a small separate monocular optic
  mounted above a lens. The mount slides and tilts; the focusing lens rotates.
  This is not evidence of a transparent binocular image covering normal vision.
  Fixed display coordinates give a head-relative image, not world anchoring.
  Whether the wearer can glance at it comfortably must be tried.
  [Official fitting guide and optical photo](https://github.com/brilliantlabsAR/docs/blob/236f9b25acd623529985fe48acf23759537accd1/halo/using-halo.md).
- **Field of view:** no current numerical **Halo optical FOV** was established from
  the official store, current Halo hardware manual or Lua reference. The 81.2°
  number is the camera's horizontal FOV. Do not use it for the display, or import
  Frame's 20° specification. Ask the manufacturer for Halo's angular image size
  and usable eye box if these determine the purchase.
- **Fonts:** firmware contains Dogica regular and bold, native 8 px, printable
  ASCII 0x20–0x7E; larger sizes are integer multiples of eight. Our font call is
  valid. Doubling glyph size roughly halves columns, so a more comfortable font
  might require a simple layout-constant adjustment after fit testing. Current
  ASCII normalization loses many non-Latin translations.
  [Font glyph data](https://github.com/brilliantlabsAR/halo-firmware/blob/0.8.25/modules/canvas/Fonts/dogica/Dogica8px.h),
  [physical text example/test](https://github.com/brilliantlabsAR/brilliant_sdk/blob/9d17e96ce1b0f1d33d270315a3816d2e8cd0523b/python/packages/brilliant_ble/tests/test_text_api.py).
- **Current layout geometry:** an emulator calculation with six full rows of 28
  `W` characters produced bounding box `(12,76)-(236,163)` in zero-based pixels.
  All lit pixels fit inside an ideal radius-128 circle (largest radius 126.46).
  This rules out obvious ideal-circle overflow, not optical clipping or poor fit.
- **Brightness:** hardware exposes percentage brightness 0–100 and levels −2…2;
  our app does not set it. Check for a persisted low/zero setting on arrival.
  The hardware manual's 5000-nit panel peak is not a measured at-eye luminance.
- **Refresh:** the manual gives a panel range of 25–120 Hz; our 30 Hz update cap is
  not a verified hardware refresh rate. Drawing changes shared display memory
  immediately. Clear-and-redraw can be seen in progress, unlike an atomic frame
  flip; tearing/flicker and draw duration need physical observation. A DRAWN
  acknowledgment means Lua draw calls completed, not that scanout reached the eye.

## Connection to our existing local Ollama

The smallest useful topology is unchanged Python/Ollama on the same Linux laptop,
plus that laptop's Bluetooth LE adapter:

```text
terminal question → Python HUD → local HTTP/SSE ↔ Ollama gpt-oss:20b
                         ↓ BLE text snapshots
                      Halo Lua HUD
                         ↑ BLE acknowledgments / button dismissal
```

No phone relay or internet/cloud inference is required for this topology. The
manufacturer documents Python desktop hosts and direct BLE Lua access. A charged,
factory-programmed Halo, magnetic charging lead/USB power, working host Bluetooth
and OS pairing permissions are required. An external BLE adapter is necessary
only if the computer lacks a usable one. A smartphone/Noa app is optional for our
custom-host path, not an inference or subscription dependency.
[Official host-app model](https://github.com/brilliantlabsAR/docs/blob/236f9b25acd623529985fe48acf23759537accd1/halo/halo-sdk.md),
[official desktop hello-world example](https://github.com/brilliantlabsAR/brilliant_sdk/blob/9d17e96ce1b0f1d33d270315a3816d2e8cd0523b/python/packages/brilliant_ble/examples/hello_world.py).

Halo requires BLE bonding. It stores up to five hosts, accepts **one active
connection**, and advertises as `Halo XX`. Hold its button five seconds to open
the approximately 60-second pairing window for a new host; accept the OS prompt.
Disconnect Noa/other host apps before the Python host connects. Single/double
clicks, a short long-press and IMU taps exist; there is no documented continuous
scroll wheel or touch-position input to assume.
[Pairing and connection specification](https://github.com/brilliantlabsAR/docs/blob/236f9b25acd623529985fe48acf23759537accd1/halo/halo-sdk-bluetooth-specs.md).

Use `BrilliantBle.connect`, `upload_file`, `send_lua`, `send_data`, its data response
handler and disconnect handler, and `max_data_payload()`; do not implement raw GATT
again. The SDK adds/removes the `0x01` raw-data marker. Unmarked ASCII on the wire
would be parsed as Lua instead of reaching our callback. Use SDK data notifications
for our acknowledgments; they are **not** Lua print responses. Register handlers
before starting the script so READY is not lost.
[Official Bluetooth SDK implementation](https://github.com/brilliantlabsAR/brilliant_sdk/blob/9d17e96ce1b0f1d33d270315a3816d2e8cd0523b/python/packages/brilliant_ble/src/brilliant_ble/brilliant_ble.py).

Our localhost restriction is compatible with the laptop topology. Running the host
on a phone and Ollama on a LAN computer would require a separate networking change:
the current provider deliberately rejects non-loopback endpoints. That mobile
workflow is not delivered or recommended as the first hardware experiment.

## Emulator discrepancies and necessary deployment changes

| Finding | Consequence / smallest action |
| --- | --- |
| No physical transport; synchronous emulator start/send methods | Add an SDK-backed transport and await connection/start/write completion or use one ordered SDK writer. Preserve the existing host/device split. Pairing must complete before the app's one-second READY timeout starts. |
| GUI and `/save` access `.emulator` directly | Physical launch must omit the pygame preview and emulator-only screenshot path. No on-glasses screenshot feature is needed. |
| Hardware panel can be suspended; emulator still renders while suspended | **Fixed:** clear black before calling `power_save(false)` at startup. |
| Emulator captures sends even when physical sending would fail | **Fixed:** guard connection and protect send with `pcall`; local clearing is not aborted by notification failure. Missing acknowledgments still cause the host timeout. |
| Emulator injects complete packets, no MTU | Current 240-byte host bound is not a negotiated BLE limit. Typical MTU 247 gives SDK raw payload 243; MTU 23 gives only 19. Use the actual SDK limit before every write. For the first port, fail clearly if the negotiated payload cannot fit snapshots. |
| Raw writes are separate callbacks, not an accumulating stream | Do not arbitrarily split a T message. If smaller MTUs must be supported, reuse SDK `send_message` plus its existing device `data.lua` reassembly shim. Do not combine it with a second competing receive callback or build a new fragmentation protocol. |
| Emulator suppresses classification delay | Physical single click waits >400 ms after release, plus 20 ms driver polling, Lua dispatch/draw and scanout. Long press needs ≥1 second. Local clearing avoids a host round trip, but does not bypass the driver. |
| Emulated startup always begins fresh/connected | On each host session, subscribe, break the old app, upload our script and restart it so generations match and READY is delivered. A host restart with generation 0 cannot reuse an old Lua session at generation 42. |
| `READY` is sent only at script start | An app auto-started offline does not announce READY later just because BLE connects. Explicit restart on attachment is the simplest existing-SDK solution. |
| Boot/wake behavior is simplified | Stock app configuration enables a firmware boot splash before Lua runs. Blank-by-default applies after our Lua initialization, not every instant after power-on. No custom firmware is proposed to remove that splash. |
| Emulator framebuffer is an ideal square and brightness is not optical | Fit, circular aperture, contrast, 8 px legibility and comfort are unverified. |
| No real radio loss, power management or scanout | Host loss, sleep/wake, reconnect and battery life remain unqualified. The current offline loop repeatedly clears; it is not an all-day battery design. |
| One-second acknowledgment timeout and 30 Hz redraw cap are host choices | Start conservatively with the existing values; measure on-device. Do not assume BLE plus redraw can sustain 30 visible updates/s or every one-second timeout is appropriate. |

Packet-budget note: a maximal six-line page is 173 text bytes plus ASCII headers
(e.g. 179 bytes at one-digit generation and sequence). Header growth also counts.
Official documentation and firmware express MTU overhead differently; query the
SDK's limit and device `max_length()` rather than hardcoding a subtraction from a
marketing MTU. SDK `send_data` frames a single write; `send_message` fragmentation
requires the matching SDK Lua library.
[Protocol/source](https://github.com/brilliantlabsAR/halo-firmware/blob/0.8.25/applications/halo/PROTOCOL.md),
[SDK messaging example](https://github.com/brilliantlabsAR/brilliant_sdk/blob/9d17e96ce1b0f1d33d270315a3816d2e8cd0523b/python/packages/brilliant_msg/examples/plain_text.py).

The official Lua documentation still describes cached `require()` and a
`package.loaded` global, but released firmware 0.8.12+ and the emulator load modules
on every require and have no `package` global. The discrepancy does not affect our
current script, which uses neither. Treat versioned firmware as authoritative.
[Lua documentation](https://github.com/brilliantlabsAR/docs/blob/236f9b25acd623529985fe48acf23759537accd1/halo/halo-sdk-lua.md),
[firmware history](https://github.com/brilliantlabsAR/halo-firmware/blob/0.8.25/CHANGELOG.md).

The enabled boot splash is visible in the [stock app configuration](https://github.com/brilliantlabsAR/halo-firmware/blob/0.8.25/applications/halo/prj.conf)
and [startup sequence](https://github.com/brilliantlabsAR/halo-firmware/blob/0.8.25/applications/halo/src/main.c).
The emulator explicitly keeps rendering while power-saved and captures raw sends
without enforcing physical sending failures:
[display stub](https://github.com/brilliantlabsAR/brilliant_sdk/blob/9d17e96ce1b0f1d33d270315a3816d2e8cd0523b/python/packages/halo_emulator/src/halo_emulator/display.py),
[Bluetooth stub](https://github.com/brilliantlabsAR/brilliant_sdk/blob/9d17e96ce1b0f1d33d270315a3816d2e8cd0523b/python/packages/halo_emulator/src/halo_emulator/stubs/bluetooth.py).

## Planned-feature classification

Here “supported” means platform/API capability established by official sources;
no row means we physically validated it. Implementation status is separate.

| Planned feature | Classification | What the evidence allows / current implementation |
| --- | --- | --- |
| Minimal text-only HUD | **Supported with limitations** | Native ASCII text, black clear and fixed coordinates exist. Current software works in emulator; BLE port and optical legibility remain. It is a small monocular glance display. |
| Streaming AI responses | **Supported with limitations** | Host-side Ollama/SSE already demonstrated; BLE can carry the bounded snapshots. Real throughput, display flicker and latency need measurement. No on-glasses LLM is implied. |
| Wikipedia/man-page reader | **Supported with limitations** | Plain text can be displayed, but retrieval, paging/history and formatting are not implemented. Current layout discards earlier lines and whitespace structure. Full web pages, tables and full-width terminal output will not fit. |
| Fine-grained page navigation | **Supported with limitations** | Discrete single/double/long actions and IMU tap events permit line/page commands. Our app currently uses only single/long for dismiss, so no reader navigation exists. Continuous touch scrolling is not established. Gesture recognition is not emulated. |
| Camera-based OCR and translation | **Unverified** | Physical camera capture/transfer is implemented, but useful document OCR accuracy is not established. VGA input, framing, lighting and BLE transfer constrain it. No OCR pipeline is built; gpt-oss text streaming alone is not an image/OCR integration. Non-Latin results are not supported by our present ASCII renderer. |
| Simple monochrome diagrams | **Supported** | Stock `line`, `rect`, `circle`, `polygon`, pixels and indexed bitmap APIs provide basic diagrams. Our current protocol renders text only; diagram commands are not implemented, and no addition was made in this audit. |
| Immediate dismissal | **Supported with limitations** | Clearing inside the device callback is supported and independent of inference. The physical single-click recognition delay prevents a <100 ms promise. Host dismissal additionally depends on BLE. |

Camera evidence is code, not Noa marketing: the SDK has a physical capture example
that transfers JPEG bytes. The hardware manual identifies a 640×480 global-shutter
camera; capture uses the same BLE data channel as other messages. Existing
`RxPhoto`/camera libraries should be reused if that later project is pursued.
[Physical camera test/example](https://github.com/brilliantlabsAR/brilliant_sdk/blob/9d17e96ce1b0f1d33d270315a3816d2e8cd0523b/python/packages/brilliant_ble/tests/test_camera.py),
[SDK photo example](https://github.com/brilliantlabsAR/brilliant_sdk/tree/9d17e96ce1b0f1d33d270315a3816d2e8cd0523b/python/packages/brilliant_msg/examples),
[shape/text test](https://github.com/brilliantlabsAR/brilliant_sdk/blob/9d17e96ce1b0f1d33d270315a3816d2e8cd0523b/python/packages/brilliant_ble/tests/test_display.py).

## Changes and tests performed without glasses

Only two production-code compatibility fixes were made, both in
[main.lua](quiet_glasses/device/main.lua): explicit panel wake and protected
connection-aware notifications. No features, SDK internals, architecture, BLE
transport, OCR or reader were added.

Results on this audit:

- **23 app tests passed**, including two new hardware-contract fault injections:
  start with panel suspended and require a wake before drawing; simulate physical
  BLE send failures at startup and during use and verify button clearing survives.
- **104 upstream tests passed**: all emulator tests plus selected hardware-free
  Bluetooth tests for Lua upload chunking, disconnect handling, message flow
  control, write-without-response fallback and SMP packet handling.
- Compared the relevant released firmware files to current main; no differences
  in the files supporting the compatibility conclusions above.
- Calculated worst-case current text layout against an ideal circular aperture.
- Inspected official desktop hello-world, plain-text host/Lua, text/font, button,
  camera and OTA examples. Physical test scripts were inspected, **not run**.

Reproduce the app tests:

```bash
cd /home/dvalluri/quiet-glasses
.venv/bin/pytest -q
```

Reproduce the selected upstream checks (the audit environment has `brilliant-ble`
installed; a fresh environment needs that official package first):

```bash
.venv/bin/pytest -q \
  ../quiet-glasses-sdk/python/packages/halo_emulator/tests/ \
  ../quiet-glasses-sdk/python/packages/brilliant_ble/tests/test_chunk_lua_string.py \
  ../quiet-glasses-sdk/python/packages/brilliant_ble/tests/test_disconnect.py \
  ../quiet-glasses-sdk/python/packages/brilliant_ble/tests/test_send_message_flow.py \
  ../quiet-glasses-sdk/python/packages/brilliant_ble/tests/test_write_without_response_fallback.py \
  ../quiet-glasses-sdk/python/packages/brilliant_ble/tests/test_smp.py
```

The existing real-Ollama demo report records 3705 ms to first X11 window flip,
41 text snapshots and 2.5 ms from an injected classified button event to a blank
emulator framebuffer. Those are **not Halo optical or physical-button timings**.
No new AI performance benchmark was needed for this hardware audit.
[Existing report](artifacts/real-demo/report.json).

Environment restrictions are documented separately in [ENVIRONMENT.md](ENVIRONMENT.md):
agent sandbox sockets/display access are restricted, and the stream-fd warning
comes from desktop shell `systemd-cat` logging. That warning is not evidence of
Halo BLE incompatibility. Linux BlueZ pairing/access and this computer's actual
radio connection to Halo have not been tested.

## Smallest experiment after arrival

Do this at a desk with the existing laptop, without introducing a phone bridge.

1. Charge Halo, fit/focus the optic and check IPD/visibility. Connect with the
   official SDK hello-world example and record hardware type, firmware version,
   git tag, battery and negotiated maximum data payload. Release other BLE host
   connections. If fonts cannot be read comfortably at this stage, stop rather
   than invest in the port.
2. If necessary update stock firmware through the documented SDK flow to 0.8.25;
   verify the reported version after reboot. Do not customize firmware.
3. Complete only the required SDK transport integration described above. Subscribe
   first, restart our script, receive READY and confirm blank after initialization.
   Reject too-small packet budgets explicitly before sending text.
4. Enter `/ask What is 2 plus 2? Answer in one short sentence.` Keep Ollama on
   localhost. Observe a real streamed answer; record activation-to-DRAWN time and
   whether partial redraws are distracting. Use an external video recording if
   actual visible latency matters; software ACK alone is insufficient.
5. Press/release the device button while text is streaming. Record release-to-blank
   on video, allowing for the documented 400 ms classification window. Verify no
   late tokens redraw the dismissed generation. Repeat ten activation/dismiss cycles.
6. Disconnect the host, reconnect/restart the script and repeat once. Confirm
   expected blanking and READY behavior, then assess the native font with a short
   paragraph for several minutes. These tests do not establish all-day comfort or
   battery life.

**Acceptance gate:** readable short answers, stable pairing, correct streaming,
no reappearance after dismissal, and a dismissal delay you personally tolerate.
If those fail, do not expand into readers/OCR to justify the purchase. Fit and the
stock button delay cannot be solved merely by swapping the emulator for BLE.

## Remaining untested properties and open-source boundary

No physical upload, firmware update, radio pairing, MTU negotiation, BLE loss,
reconnect, supervision timeout, actual gesture timing, display wake, scanout,
optical readability/brightness, sustained use, thermals or battery life has been
validated by us. Native-language typography, useful camera OCR and translation,
server-side cancellation timing and server retention also remain unqualified.
Physical BLE confidentiality/security was not audited. Black pixels and local
inference do not guarantee secure erasure or OS/model-server privacy.

Using the published BSD-3-Clause SDK and stock firmware preserves the current
open-source approach. Keep the eventual physical transport separate from the
provider and HUD logic, as the current transport boundary already permits. No
Noa-specific cloud dependency is needed. The app currently has no declared license
field or standalone LICENSE file; select an explicit project license before
redistributing it as an open-source release. This audit does not select a license
on the owner's behalf. [SDK license](https://github.com/brilliantlabsAR/brilliant_sdk/blob/9d17e96ce1b0f1d33d270315a3816d2e8cd0523b/LICENSE).
