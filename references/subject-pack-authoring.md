# Subject-pack authoring

Add a focused Markdown reference without changing the core pipeline. Validate it with `scripts/validate_pack.py --subject-pack FILE`.

Required metadata:

```yaml
subject: Physics
qualification: International GCSE
exam_board: Example Board
route_or_level: Higher
version: "1.0"
valid_from: YYYY-MM
valid_to: YYYY-MM or current
last_verified: YYYY-MM-DD
official_sources: [official URLs]
supported_topics: []
command_words: []
assessment_style: ""
marking_rules: []
verification_rules: []
common_misconceptions: []
diagram_types: []
```

Document boundaries, levels/routes, current official sources, command words, mark density, conventions, misconceptions, verification, and diagrams. Use deterministic validation for numerical subjects and explicit rubric checks for non-numerical subjects. Include only original examples; never bundle official papers or logos. Suitable extensions include GCSE Chemistry, IGCSE Biology, A-level Physics, SAT Mathematics, AMC 8, English, and Geography.
