from sympy import Eq, Symbol, expand, simplify, solve, sympify

def validate_question(q):
    d=q.get("verification_data") or {}; kind=d.get("kind")
    if not kind: return "no deterministic math payload"
    if kind=="gradient":
        x1,y1,x2,y2=map(sympify,[d[k] for k in ("x1","y1","x2","y2")]); got=simplify((y2-y1)/(x2-x1)); exp=sympify(d["expected"])
    elif kind=="midpoint":
        x1,y1,x2,y2=map(sympify,[d[k] for k in ("x1","y1","x2","y2")]); got=[simplify((x1+x2)/2),simplify((y1+y2)/2)]; exp=[sympify(x) for x in d["expected"]]
    elif kind=="line":
        x=Symbol("x"); m=sympify(d["m"]); c=sympify(d["c"]); px=sympify(d["x"]); py=sympify(d["y"]); got=simplify(m*px+c); exp=py
    elif kind=="equation":
        x=Symbol(d.get("variable","x")); got=solve(Eq(sympify(d["lhs"]),sympify(d["rhs"])),x); exp=[sympify(v) for v in d["expected"]]
    elif kind=="factorisation": got=expand(sympify(d["factorised"])); exp=expand(sympify(d["expanded"]))
    elif kind=="percentage": got=simplify(sympify(d["base"])*(1+sympify(d["rate"])/100)**int(d.get("periods",1))); exp=sympify(d["expected"])
    else: raise ValueError(f"Q{q['number']}: unsupported math verification kind {kind}")
    if got != exp: raise ValueError(f"Q{q['number']}: math check failed ({got} != {exp})")
    return f"Q{q['number']} {kind}: passed"

def validate(data): return [validate_question(q) for q in data["questions"]]
