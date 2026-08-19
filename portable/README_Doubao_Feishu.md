# Doubao / Feishu test path

The teacher completes the standard six-section lesson feedback once in Feishu. The model converts it to structured state, blueprint, and paper JSON; local deterministic validation and rendering produce Questions.pdf, Answers.pdf, and Combined.pdf. Do not assume Doubao natively understands Agent Skills.

## Route A — manual portable-prompt test

1. Export the relevant prompt with `scripts/export_portable_prompt.py`.
2. Paste that prompt into Doubao, followed by the canonical feedback.
3. Require only structured JSON output in the documented sequence.
4. Save the generated-paper object and run `python scripts/validate_pack.py paper.json`.
5. If validation passes, run `python scripts/render_pdfs.py paper.json --output-dir output/`.

## Route B — API integration

Consult the current official Volcano Engine Ark documentation before implementation. Use currently supported JSON Schema/structured output where available and function calling only where appropriate. Do not guess endpoints or hard-code credentials. Read credentials from environment variables in an uncommitted `.env`; the core project requires no paid API.
