---
name: personalised-practice-generator
description: Use this skill when a teacher provides post-lesson feedback and wants personalised, syllabus-aware practice questions, worked answers and exam-style PDFs based on what the student could complete independently, what required prompting, what remains unstable, and the teacher's stated next priorities. Supports structured Chinese or English lesson feedback and subject-specific packs. Do not reproduce copyrighted official past-paper questions.
license: MIT
metadata:
  version: "0.2.1"
---

# Personalised Practice Generator

Turn one ordinary post-lesson feedback record into original, evidence-led practice and fixed-format PDFs. Never require a second AI-specific form.

## Required workflow

1. Read [teacher-feedback-input.md](references/teacher-feedback-input.md) and parse the feedback with `scripts/parse_teacher_feedback.py`. If course identity is missing and cannot be inferred safely, ask one concise question. Otherwise proceed, recording assumptions.
2. Preserve independent, prompted, and unstable performance separately. Do not convert prompted success into secure mastery or invent a cause for vague feedback. Read [student-state.md](references/student-state.md) when diagnosis is needed.
3. Read [personalisation-policy.md](references/personalisation-policy.md), then create an evidence-linked blueprint conforming to `assets/assessment-blueprint.schema.json`. Use secure skills lightly and devote most practice to prompted or unstable skills.
4. Load exactly one relevant subject pack: [Cambridge 0607 Mathematics](references/cie-0607-mathematics.md) or [Edexcel 4PH1 Physics](references/edexcel-igcse-physics.md). If none matches, explain that a pack is required and use [subject-pack-authoring.md](references/subject-pack-authoring.md) only when asked to add one.
5. Write original questions and concise worked answers as JSON conforming to `assets/generated-paper.schema.json`. Never copy or closely paraphrase official questions, use board logos, or imply endorsement. Include “Original examination-style practice material”.
6. Run `scripts/validate_pack.py PAPER.json`. Revise any failing question and repeat until every required check passes. Never render a known-invalid paper.
7. Run `scripts/render_pdfs.py PAPER.json --output-dir OUTPUT`. Inspect with `scripts/inspect_pdf.py OUTPUT/Questions.pdf OUTPUT/Answers.pdf OUTPUT/Combined.pdf`. Normal short sets must be 1, 1, and 2 A4 pages, with no answer leakage.
8. Return `Questions.pdf`, `Answers.pdf`, and `Combined.pdf`. Keep student-facing pages free of feedback, diagnostic labels, mastery levels, and question-selection rationales.

## Defaults and boundaries

- Choose 3 questions for one focused skill cluster, or 4–5 short questions for broader retrieval; target 15–30 minutes.
- Teacher priorities override inferred priorities unless outside the named syllabus. If priorities are absent or “由系统判断”, infer from unstable skills, prompted skills, concrete errors, prerequisites, then secure retrieval.
- Existing homework is context or a constraint; do not silently replace it.
- Adjust scaffolding, representations, number cleanliness, reasoning steps, and transfer demand—not decorative story context.
- Keep normal PDFs readable and fixed in the [house format](references/pdf-style-guide.md). If content cannot fit, shorten wording or reduce an unspecified count before reducing type; split into numbered two-page sets if needed.
- Use fictional/aliased student data. Do not commit real feedback or generated local outputs.

For the complete workflow and schemas, read [core-workflow.md](references/core-workflow.md) and [assessment-blueprint.md](references/assessment-blueprint.md) only when implementing or debugging the pipeline.
