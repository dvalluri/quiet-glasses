# Environment findings

## `Failed to create stream fd: Operation not permitted`

This warning originates in `systemd-cat`, not Halo, Lua, the AI SSE stream, or the
HUD transport. On this machine, login-shell initialization loads
`/etc/profile.d/im-config_wayland.sh`, which loads `/usr/share/im-config/initializer`.
The initializer chooses `/usr/bin/systemd-cat -p 6 -t im-config echo` as its logger.
Several startup log messages therefore produce several warnings in the restricted
agent environment.

Investigation:

- A non-login shell running `true` produces no warning.
- In the restricted sandbox, `/usr/bin/systemd-cat -t quiet-glasses-check /usr/bin/true`
  reproduces the exact warning without importing or executing the project.
- Tracing a login shell outside the sandbox showed input-method logging invoking
  `systemd-cat`, which opens an `AF_UNIX`, `SOCK_STREAM|SOCK_CLOEXEC` socket.
- The same login-shell trace outside the sandbox completed without the warning.
  Tracing inside the sandbox itself is denied (`PTRACE_TRACEME: Operation not permitted`).

The evidence identifies the denied system-journal stream socket as the source.
No system shell configuration or SDK code was changed, and stderr is not suppressed.
A normal desktop terminal avoids this agent-specific logging restriction. For
agent-run checks, a non-login shell avoids these unrelated startup calls.

## Other restrictions encountered

The restricted agent sandbox also rejects creation of local network sockets:
`curl http://127.0.0.1:11434/api/tags` initially failed with
`failed to open socket: Operation not permitted`. This restriction prevents real
model access even though Ollama is healthy. Sandboxed remote downloads also failed
DNS resolution. Approved execution outside that sandbox successfully reached the
local server, ran the real inference demonstration, and opened an X11 pygame
window. These are execution-environment restrictions; the app does not disable or
bypass them. If run under such a policy, get the required execution approval or use
the mock provider/headless tests. Auto selection explicitly reports mock fallback
when it cannot reach the local service.

The initial prototype's threaded console input also hung during Python executor
shutdown in this environment. The current interface uses asynchronous POSIX stdin
instead; the automated CLI exit test validates clean `/quit` behavior.

The desktop demonstration used pygame 2.6.1, SDL 2.28.4, Python 3.12.12 and the X11
driver. SDL's dummy driver is used only in automated window tests. A dummy driver
can test rendering and input handling, but does not demonstrate a person-visible
window. The real-demo report records `x11`, not `dummy`.

A working desktop session and display permissions are required for `launch`.
There is no Windows console implementation. Model load, reasoning, and host GPU
or CPU availability dominate real first-response latency; the initial 26 ms mock
measurement is not representative of real inference.

## Exactly what physical-glasses testing has not established

No physical glasses were connected or used. The emulator-only release has not
established any of the following:

1. Firmware upload, execution on actual Halo hardware, or compatibility of the
   script with a particular installed firmware version beyond emulator behavior.
2. Actual BLE discovery, pairing, authentication, confidentiality, negotiated MTU,
   fragmentation, radio delivery/order/loss, reconnects, or disconnect handling.
   The application currently supplies only an emulator transport.
3. Optical focus, eye box, field of view, position/alignment, head-lock stability
   while moving, readability, color/brightness, transparency, ambient-light
   performance, comfort, or accessibility. Fixed screen coordinates are all the
   emulator validates about the intended head-locked placement.
4. Physical display scanout, tearing/flicker during clear-and-redraw, scheduling
   against inference/communications, and activation-to-photon or button-to-photon
   latency. Window flip and framebuffer measurements are software observations.
5. Actual button/gesture sensing, debounce, false activations, user-perceived
   responsiveness, or dismissal reliability under real firmware/radio load.
6. Battery consumption, thermals, sleep/wake, standby, sustained CPU/memory limits,
   wearability, or long-duration stability. The Lua runtime stays awake.
7. On-device data retention/erasure, firmware security, or privacy of physical
   communication. Neither emulator dismissal nor a blank screen securely erases
   RAM. Host/model-server security and server-side request retention also remain
   outside this app's guarantees.

Camera, microphone, audio, spatial anchoring, and a physical BLE transport are not
implemented in this prototype and were not tested. A stalled host can leave the
last answer visible until device-button dismissal or a detected disconnect; no
host-loss watchdog is implemented. The emulator does not reproduce a real radio
disconnect. These limitations are unchanged by the successful local-model demo.
