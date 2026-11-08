# Working on Quiet Glasses

Dinesh decides what the product should do and whether the demonstrated experience is useful. The coordinating Codex agent assigns small tasks and puts the pieces together. Other Codex agents own a named part: **App, AI, Connection, Screen, Reader, or Testing**.

Read [who does what](docs/AGENT_TEAM.md), [shared rules](docs/contracts/SHARED.md), and the agreement for your assigned part. [Architecture](docs/ARCHITECTURE.md) describes the code today; the proposed boundaries are not claims that new code exists.

## Rules for the work

- Work on the smallest assigned task that helps finish one usable prototype. Prefer integration and testing over more features.
- The coordinating agent can delegate independent tasks. Give each file one editor; use separate branches/worktrees when needed.
- Only the coordinating agent edits `quiet_glasses/core.py` until its App, Screen, and Connection code has been separated.
- Agents make routine compatible implementation choices. Bring Dinesh a concrete proposal and tradeoff when product behavior, target hardware, or an incompatible shared interface must change.
- Keep one runnable app, with small local interfaces and existing SDKs. Add separate processes or infrastructure only for a demonstrated need.
- Screen must clear locally without waiting for AI, the host, or a successful notification. Old answers must not reappear after dismissal.
- Preserve LOCAL / MOCK / MOCK FALLBACK labels. A synthetic answer is not successful model inference.
- Record where and how a test ran. Emulator results, SDK descriptions, and drawing acknowledgements do not establish physical readability or compatibility.
- Run checks appropriate to changed behavior. Record failures and missing prerequisites; physical acceptance needs physical observations.
- Do not merge or declare a release accepted just because an agent says done. Assemble a candidate and get an independent test report.

## Task handoff

State the part and task, starting revision, allowed files, expected inputs/outputs, test for completion, and what is out of scope.

Return the result revision, changed files, pass/fail/blocked checks with evidence, limitations, dependencies, and the smallest remaining action. Agents run for assigned tasks, not continuously in the background.
