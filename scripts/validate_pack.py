#!/usr/bin/env python3
import argparse, json, re
from pathlib import Path
from validate_schema import validate as schema_validate
from validate_marks import validate as marks_validate
from validate_math import validate as math_validate
from validate_physics import validate as physics_validate

ROOT=Path(__file__).resolve().parents[1]
def validate_paper(path):
    data=schema_validate(path,ROOT/"assets/generated-paper.schema.json"); marks_validate(data)
    subject=data["metadata"]["subject"].lower()
    checks=physics_validate(data) if "physics" in subject else math_validate(data)
    if data["verification"]["status"]!="passed": raise ValueError("verification.status must be passed before rendering")
    return ["schema: passed","marks: passed",*checks]
def validate_subject_pack(path):
    text=Path(path).read_text(encoding="utf-8"); required=["subject","qualification","exam_board","version","last_verified","official_sources","supported_topics","verification_rules"]
    missing=[k for k in required if not re.search(rf"\b{k}\s*:",text,re.I)]
    if missing: raise ValueError("subject pack missing: "+", ".join(missing))
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("paper",nargs="?"); ap.add_argument("--subject-pack"); a=ap.parse_args()
    if a.subject_pack: validate_subject_pack(a.subject_pack); print("subject pack: passed")
    elif a.paper:
        for c in validate_paper(a.paper): print(c)
    else: ap.error("paper or --subject-pack is required")
if __name__=="__main__": main()
