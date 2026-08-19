def validate(data):
    qs=data["questions"]; ans=data["answers"]
    nums=[q["number"] for q in qs]
    if nums != list(range(1,len(qs)+1)): raise ValueError("Question numbers must be consecutive from 1")
    if [a["question_number"] for a in ans] != nums: raise ValueError("Answer numbering must match questions")
    for q in qs:
        if q["parts"] and sum(p["marks"] for p in q["parts"]) != q["marks"]: raise ValueError(f"Q{q['number']}: part marks do not total question marks")
    if sum(q["marks"] for q in qs) != data["metadata"]["total_marks"]: raise ValueError("Question marks do not match metadata total")
    return True
