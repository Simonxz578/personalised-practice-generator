#!/usr/bin/env python3
import argparse,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PACKS={"cie-0607-mathematics":"cie-0607-mathematics.md","edexcel-igcse-physics":"edexcel-igcse-physics.md"}
def export(subject):
    if subject not in PACKS: raise ValueError("unknown subject pack")
    template=(ROOT/"assets/teacher-feedback-template.txt").read_text(encoding="utf-8")
    state=json.dumps(json.loads((ROOT/"assets/student-state.schema.json").read_text()),ensure_ascii=False,separators=(",",":"))
    paper=json.dumps(json.loads((ROOT/"assets/generated-paper.schema.json").read_text()),ensure_ascii=False,separators=(",",":"))
    policy=(ROOT/"references/personalisation-policy.md").read_text(encoding="utf-8")
    pack=(ROOT/"references"/PACKS[subject]).read_text(encoding="utf-8")
    return f"# Portable personalised-practice instructions\n\nFollow exactly: (1) parse feedback, (2) output internal student state, (3) create an evidence-linked assessment blueprint, (4) create generated-paper JSON, (5) self-check the schemas, (6) return the structured payload for deterministic validation/rendering. Do not lay out PDFs. Do not ask for extra AI fields. Write original questions only.\n\n## Canonical input\n```text\n{template}\n```\n\n## Parsing\nPreserve independent/prompted/unstable distinctions. Treat vague causes as unknown. Infer missing priorities from unstable, prompted, concrete errors, prerequisites, then secure retrieval.\n\n{policy}\n\n## Subject pack\n{pack}\n\n## Student-state schema\n```json\n{state}\n```\n\n## Generated-paper schema\n```json\n{paper}\n```\n"
def main():
    p=argparse.ArgumentParser();p.add_argument("--subject",required=True,choices=PACKS);p.add_argument("--output",required=True);a=p.parse_args();out=Path(a.output);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(export(a.subject),encoding="utf-8");print(out)
if __name__=="__main__":main()
