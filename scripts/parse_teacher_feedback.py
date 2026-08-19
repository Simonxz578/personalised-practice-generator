#!/usr/bin/env python3
import argparse, json, re
from pathlib import Path

EMPTY = {"", "无", "none", "n/a", "无明显问题"}

def clean_list(value):
    value = value.strip().strip("[]")
    if value.lower() in EMPTY: return []
    return [x.strip() for x in re.split(r"[；;、]", value) if x.strip() and x.strip().lower() not in EMPTY]

def field(text, labels, default=""):
    pat = "|".join(map(re.escape, labels))
    m = re.search(rf"(?:{pat})\s*[：:]\s*([^\n]+)", text, re.I)
    return m.group(1).strip() if m else default

def section(text, title):
    m = re.search(rf"【{re.escape(title)}】\s*(.*?)(?=\n【|\Z)", text, re.S)
    return m.group(1).strip() if m else ""

def course_parts(raw):
    low = raw.lower(); board = subject = code = level = ""
    if "cambridge" in low: board = "Cambridge International"
    elif "pearson" in low or "edexcel" in low: board = "Pearson Edexcel"
    if "math" in low or "数学" in raw: subject = "Mathematics"
    elif "physics" in low or "物理" in raw: subject = "Physics"
    m = re.search(r"\b(0607|4PH1)\b", raw, re.I); code = m.group(1).upper() if m else ""
    for candidate in ("Extended", "Core", "Higher", "Foundation"):
        if candidate.lower() in low: level = candidate; break
    return board, subject, code, level

def parse(text):
    course_raw = section(text, "课程").splitlines()[0].strip() if section(text, "课程") else ""
    board, subject_name, code, level = course_parts(course_raw)
    dt = section(text, "日期 / 时间") or section(text, "日期/时间")
    dm = re.search(r"(\d{4}[.\-/]\d{1,2}[.\-/]\d{1,2})", dt)
    tm = re.search(r"(\d{1,2}:\d{2}\s*[–—-]\s*\d{1,2}:\d{2})", dt)
    content = section(text, "课程内容"); perf = section(text, "课堂表现"); diag = section(text, "存在问题与建议")
    specific = field(diag, ["具体问题", "Specific problem", "Specific problems"])
    priorities_raw = field(diag, ["下一步重点", "Next priorities"])
    priorities = [] if priorities_raw in ("由系统判断", "system to infer") else [re.sub(r"^\s*\d+[.、]\s*", "", x) for x in clean_list(priorities_raw)]
    evidence = [] if specific.lower() in EMPTY else clean_list(specific)
    vague = [x for x in evidence if x.lower() in {"粗心", "基础不好", "careless", "weak foundation"}]
    state = {
      "course": {"exam_board_or_curriculum": board, "subject": subject_name, "syllabus_or_specification_code": code, "level_or_tier": level},
      "lesson": {"date": dm.group(1) if dm else "", "time": tm.group(1) if tm else "", "topic": field(content, ["Topic", "主题"]), "skills_taught_or_practised": clean_list(field(content, ["本节练习/学习", "本节练习／学习", "Skills practised", "Lesson skills"]))},
      "performance": {"independent_skills": clean_list(field(perf, ["独立完成哪些技能", "Independent skills"])), "prompted_skills": clean_list(field(perf, ["提示后完成哪些技能", "Prompted skills"])), "prompt_types": clean_list(field(perf, ["提示类型", "Prompt types"])), "unstable_or_incomplete_skills": clean_list(field(perf, ["尚不稳定/未完成", "尚不稳定／未完成", "Unstable or incomplete"]))},
      "diagnosis": {"specific_error_evidence": [x for x in evidence if x not in vague], "error_patterns": [], "unknown_causes": vague},
      "teacher_priorities": priorities[:3], "existing_homework": section(text, "课后作业") or section(text, "Homework"), "internal_micro_skill_state": [], "assumptions": []}
    if not course_raw: state["assumptions"].append("Course identity missing; clarification required.")
    if priorities_raw in ("由系统判断", "system to infer") or not priorities_raw: state["assumptions"].append("Next priorities must be inferred from performance evidence.")
    return state

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("input"); ap.add_argument("--output"); args=ap.parse_args()
    state=parse(Path(args.input).read_text(encoding="utf-8")); out=json.dumps(state,ensure_ascii=False,indent=2)
    if args.output: Path(args.output).parent.mkdir(parents=True,exist_ok=True); Path(args.output).write_text(out+"\n",encoding="utf-8")
    else: print(out)
if __name__ == "__main__": main()
