from pathlib import Path
from parse_teacher_feedback import parse
ROOT=Path(__file__).resolve().parents[1]
def test_canonical_parser():
    s=parse((ROOT/"examples/feedback_math_zh.txt").read_text())
    assert s["course"]["syllabus_or_specification_code"]=="0607"
    assert s["performance"]["independent_skills"]==["midpoint","distance"]
    assert "perpendicular gradient" in s["performance"]["unstable_or_incomplete_skills"]
def test_none_and_system_infer():
    s=parse("【课程】\nCambridge IGCSE International Mathematics 0607 Core\n【课程内容】\nTopic：Algebra\n本节练习/学习：expand；solve\n【课堂表现】\n独立完成哪些技能：无\n提示后完成哪些技能：solve\n提示类型：步骤\n尚不稳定/未完成：无\n【存在问题与建议】\n具体问题：无明显问题\n下一步重点：由系统判断\n【课后作业】\n无")
    assert s["performance"]["independent_skills"]==[] and s["diagnosis"]["specific_error_evidence"]==[] and s["teacher_priorities"]==[]
def test_missing_course_recorded():
    s=parse("【课程内容】\nTopic：Algebra\n【课堂表现】\n独立完成哪些技能：solve")
    assert "clarification required" in s["assumptions"][0]
