# Product and architecture decisions

These document the requested product direction and its relationship to the audited implementation. They are not reconstructed historical approvals or dated architecture records.

| Decision | Rationale and current consequence |
| --- | --- |
| Minimalist monochrome interface | White text on blank black framebuffer minimizes visual clutter; optical effect remains untested |
| Text-first, then diagrams | Brief answers are the current interaction; diagram rendering is planned |
| Local-first AI where practical | Loopback-only SSE keeps the application request local; model server behavior remains outside app control |
| Existing SDKs/libraries preferred | Use official Halo emulator, httpx and pygame; physical work should use the existing BLE SDK |
| Hardware-agnostic software where feasible | Provider/HUD responsibilities are separate, but transport construction and Lua APIs remain Halo-specific; portability is a goal, not a delivered abstraction |
| Open-source development | Publish understandable source and reproducible results under Apache-2.0; third-party components retain their own licenses |
| One physical prototype initially | Validate optics and transport before buying multiple devices |
| Product completion before extra complexity | Complete the smallest working physical text experience before broader platform work |
| Privacy and user control | Explicit activation, no automatic conversation files, loopback endpoint restriction and deliberate screenshot saving |
| Immediate dismissal | Device callback clears before host notification; host queues clear before provider cleanup; real physical responsiveness remains unmeasured |
| Blank by default | Startup and dismissal clear display; no always-on contextual overlay |

Tradeoffs include ASCII-only output, no reader navigation, no world anchoring, host-side inference requirements, and no host-loss watchdog. A blank display does not securely erase memory. See [architecture](ARCHITECTURE.md) and [hardware limitations](HARDWARE.md) before treating these decisions as guarantees.
