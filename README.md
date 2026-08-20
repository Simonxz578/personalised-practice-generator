# Personalised Practice Generator

Paste the lesson feedback you already write. The Skill identifies what the student should practise next and produces a matching question sheet and worked answers.

Teachers do not write a second AI report, mastery table, JSON profile, rubric, or question specification. The normal six-section lesson report in [`assets/teacher-feedback-template.txt`](assets/teacher-feedback-template.txt) is the complete preferred input.

## What it does

The Skill separates independently completed, prompted, and unstable skills; preserves concrete error evidence; creates an internal evidence-linked blueprint; writes original syllabus-aware questions; validates structured data and calculations; and renders a fixed one-page question paper, one-page answer sheet, and two-page combined PDF. Prompted success is never treated as secure mastery. Personalisation changes scaffolding, reasoning steps, representation, numerical cleanliness, and transfer—not superficial story contexts.

Initial production packs cover Cambridge IGCSE International Mathematics 0607 (percentages, straight lines/coordinate geometry, quadratics, algebra, statistics, and common graph skills) and Pearson Edexcel International GCSE Physics 4PH1 (Forces and Motion, including resultant force, F = ma, kinematics, Hooke's law, terminal velocity, momentum, and force diagrams). Check current examination-year board documents before high-stakes use.

## Use as an Agent Skill

Place or symlink this directory into a supported skill location, or open the repository in Codex and explicitly invoke `$personalised-practice-generator`. Paste the completed six-section feedback and ask for personalised practice. Codex also supports implicit activation from the `description` in `SKILL.md`.

## Local deterministic workflow

```bash
python -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python scripts/parse_teacher_feedback.py examples/feedback_math_zh.txt --output dist/student-state.json
.venv/bin/python scripts/validate_pack.py examples/generated-paper-example.json
.venv/bin/python scripts/render_pdfs.py examples/generated-paper-example.json --output-dir samples/math
.venv/bin/python scripts/inspect_pdf.py samples/math/Questions.pdf samples/math/Answers.pdf samples/math/Combined.pdf
```

The model generates state, blueprint, and paper JSON; the scripts validate and lay out PDFs. On a failed validator, revise the specific structured question and do not render.

## Portable and Doubao / Feishu

Export a compact instruction bundle:

```bash
.venv/bin/python scripts/export_portable_prompt.py --subject cie-0607-mathematics --output dist/cie0607-portable-prompt.md
```

Use it with the same teacher feedback in a client without native Skills, save the resulting structured paper JSON, then validate and render locally. See [`portable/README_Doubao_Feishu.md`](portable/README_Doubao_Feishu.md).

## Contributing a subject pack

Follow [`references/subject-pack-authoring.md`](references/subject-pack-authoring.md). Add official scope metadata, topics, command words, conventions, misconceptions, verification, and diagrams without changing the core pipeline. Numerical subjects should use deterministic checks; non-numerical subjects may use explicit rubric verification.

## Privacy, copyright, and limitations

Use aliases; full student names and unrelated personal attributes are unnecessary. Never commit real lesson feedback to a public repository, and generated local outputs are ignored by default. All included questions are original. The project does not redistribute official papers, use board logos, or claim endorsement by Cambridge International or Pearson.

This v0.2 parser handles the canonical Chinese template plus common English field labels; genuinely free-form reports may need model-assisted extraction. Deterministic verification covers declared common maths/physics payloads, while written explanations still need rubric/human review. PDF layout supports normal short sets and intentionally rejects overflow instead of shrinking text excessively.

Renderer v0.2.1 safely normalises Unicode mathematical subscripts and superscripts (for example `x₁`, `m/s²`, and `s⁻¹`) into ReportLab markup after escaping model-generated text.
