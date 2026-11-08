# Reader — agreement v0.1

Eventually prepares documents, pages, translations, and field-guide questions. For this milestone it only supplies test text; feature work is parked.

Assigned Codex agent: Reader.

## Boundary

Input: ContentRequest(mode, explicit user_input, optional source_ref, optional target_language).
Output: TextTask(kind=literal|inference, text, optional source_ref, constraints) or ContentError.

Initial target supported tasks: a literal public test fixture and a bounded ask prompt. The Reader adapter is unimplemented; the first dispatch delivers fixtures and constraints only. Proposed reader, translate, and guide modes remain unsupported until individually implemented and verified. They return UNSUPPORTED_MODE; do not silently route them to generic Q&A.

## Obligations

- Validate nonblank input. Preserve original source identity and requested language when those capabilities are added.
- Distinguish quoted source content from generated explanation. A generated answer is not verified manual text.
- Return INVALID_INPUT, SOURCE_UNAVAILABLE, UNSUPPORTED_MODE, or UNSUPPORTED_GLYPHS as appropriate.
- Do not silently transliterate a translation into an ASCII-only display and report multilingual success.
- Never activate the display, allocate generations, own inference transport, collect camera data, or change device state. App controls when a prepared task runs.
- No document ingestion, OCR, translation, diagrams, navigation, anchoring, or retrieval infrastructure in the first wearable milestone.

## Ownership and acceptance

Proposed path: `quiet_glasses/content/` with assigned fixtures/tests. Existing generic provider system prompt remains in AI until a separately coordinated extraction.

Checks when the adapter is implemented: valid literal/question task, rejected blank input, explicit unsupported modes, preserved provenance, and glyph incompatibility. These are future checks, not tests run by this documentation change.

First dispatch: supply one short public ASCII fixture and one short question with expected output constraints. Then remain parked until the wearable text interaction is accepted.
