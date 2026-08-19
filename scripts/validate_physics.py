from math import isclose

def validate_question(q):
    d=q.get("verification_data") or {}; kind=d.get("kind")
    if not kind: return "no deterministic physics payload"
    if kind=="resultant_force": got=float(d["forward"])-float(d["backward"])
    elif kind=="fma": got=float(d["force"])/float(d["mass"])
    elif kind=="momentum": got=float(d["mass"])*float(d["velocity"])
    elif kind=="hooke": got=float(d["spring_constant"])*float(d["extension_m"])
    elif kind=="speed": got=float(d["distance_m"])/float(d["time_s"])
    else: raise ValueError(f"Q{q['number']}: unsupported physics verification kind {kind}")
    if not isclose(got,float(d["expected"]),rel_tol=1e-9,abs_tol=1e-9): raise ValueError(f"Q{q['number']}: physics check failed ({got} != {d['expected']})")
    return f"Q{q['number']} {kind}: passed"
def validate(data): return [validate_question(q) for q in data["questions"]]
