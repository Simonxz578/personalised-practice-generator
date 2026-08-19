# Core workflow and failure policy

Pipeline: teacher feedback → student-state JSON → blueprint JSON → generated-paper JSON → schema/subject/mark verification → Questions.pdf, Answers.pdf, Combined.pdf.

The model owns evidence interpretation and original content; deterministic scripts own structural checks, calculations where verification data is supplied, and document layout. On failure, identify the question, revise structured content, revalidate, and render only after success. The same validated object generates all three PDFs.

Essential input is course identity, lesson scope, and observable performance. Ask one concise clarification only when course identity cannot be inferred safely. Preserve existing homework as context. Teacher priorities prevail within syllabus limits; otherwise infer from unstable, prompted, concrete error evidence, prerequisites, then light secure retrieval.
