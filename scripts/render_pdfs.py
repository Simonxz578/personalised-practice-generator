#!/usr/bin/env python3
import argparse, json
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, PageBreak
from reportlab.graphics.shapes import Drawing, Line, String, Rect, PolyLine
from pypdf import PdfReader, PdfWriter
from validate_pack import validate_paper

INK=colors.HexColor("#18212B"); ACCENT=colors.HexColor("#24527A"); RULE=colors.HexColor("#AAB7C4"); SHADE=colors.HexColor("#EEF3F7")
BODY=ParagraphStyle("body",fontName="Helvetica",fontSize=9.5,leading=12,textColor=INK,spaceAfter=3)
SMALL=ParagraphStyle("small",parent=BODY,fontSize=8,leading=10)
TITLE=ParagraphStyle("title",parent=BODY,fontName="Helvetica-Bold",fontSize=15,leading=18,textColor=ACCENT,spaceAfter=2)
Q=ParagraphStyle("q",parent=BODY,fontSize=10,leading=13,spaceAfter=4)

def safe(s): return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace("\n","<br/>")
def diagram_flowable(spec):
    if not spec: return None
    kind=spec.get("type",""); d=Drawing(155*mm,38*mm)
    if kind in {"coordinate_plane","straight_line","line_graph"}:
        ox,oy=77*mm,18*mm; d.add(Line(8*mm,oy,147*mm,oy,strokeColor=RULE)); d.add(Line(ox,3*mm,ox,35*mm,strokeColor=RULE))
        for p in spec.get("points",[]):
            x=ox+float(p[0])*8*mm; y=oy+float(p[1])*4*mm; d.add(Rect(x-1.2,y-1.2,2.4,2.4,fillColor=ACCENT,strokeColor=ACCENT)); d.add(String(x+3,y+2,str(p[2] if len(p)>2 else ""),fontSize=7))
        if "line" in spec:
            (x1,y1),(x2,y2)=spec["line"]; d.add(Line(ox+x1*8*mm,oy+y1*4*mm,ox+x2*8*mm,oy+y2*4*mm,strokeColor=ACCENT,strokeWidth=1.2))
    elif kind in {"force","parachutist_force"}:
        cx,cy=77*mm,18*mm; d.add(Rect(cx-8*mm,cy-4*mm,16*mm,8*mm,strokeColor=INK,fillColor=SHADE))
        for a in spec.get("arrows",[]):
            dx=float(a.get("dx",0))*mm; dy=float(a.get("dy",0))*mm; d.add(Line(cx,cy,cx+dx,cy+dy,strokeColor=ACCENT,strokeWidth=1.3)); d.add(String(cx+dx+2,cy+dy+2,str(a.get("label","")),fontSize=7))
    elif kind=="spring":
        pts=[]
        for i in range(17): pts.extend([12*mm+i*7*mm,18*mm+(4*mm if i%2 else -4*mm)])
        d.add(PolyLine(pts,strokeColor=ACCENT,strokeWidth=1.2)); d.add(Line(8*mm,5*mm,8*mm,31*mm,strokeColor=INK)); d.add(String(125*mm,17*mm,str(spec.get("label","spring")),fontSize=8))
    elif kind=="table":
        rows=spec.get("rows",[]); return Table([[Paragraph(safe(c),SMALL) for c in row] for row in rows],style=[("GRID",(0,0),(-1,-1),0.4,RULE),("BACKGROUND",(0,0),(-1,0),SHADE),("LEFTPADDING",(0,0),(-1,-1),4),("RIGHTPADDING",(0,0),(-1,-1),4)])
    else: raise ValueError(f"Unsupported diagram type: {kind}")
    return d
def header(data, answer=False):
    m=data["metadata"]; label="Answers and Worked Solutions" if answer else "Question Paper"
    rows=[[Paragraph(safe(m["qualification"]+" · "+m["subject"]),SMALL),Paragraph(label,ParagraphStyle("r",parent=SMALL,alignment=2,fontName="Helvetica-Bold"))]]
    t=Table(rows,colWidths=[120*mm,41*mm]); t.setStyle(TableStyle([("BOTTOMPADDING",(0,0),(-1,-1),4),('LINEBELOW',(0,0),(-1,-1),0.7,ACCENT)]))
    return [t,Spacer(1,4),Paragraph(safe(m["title"]),TITLE),Paragraph(f"Topic: {safe(m['topic'])}",BODY),Paragraph("Original examination-style practice material",SMALL)]

def footer(canvas,doc):
    canvas.saveState(); canvas.setStrokeColor(RULE); canvas.line(17*mm,12*mm,193*mm,12*mm); canvas.setFont("Helvetica",7.5); canvas.setFillColor(INK); canvas.drawString(17*mm,8*mm,"Independent practice material — not endorsed by an examination board"); canvas.drawRightString(193*mm,8*mm,str(doc.page)); canvas.restoreState()

def question_block(q):
    elems=[Paragraph(f"<b>{q['number']}</b>&nbsp;&nbsp;{safe(q['stem'])}",Q)]
    diag=diagram_flowable(q.get("diagram"))
    if diag is not None: elems += [diag,Spacer(1,3)]
    for p in q["parts"]:
        elems.append(Table([[Paragraph(f"({safe(p['label'])}) {safe(p['text'])}",BODY),Paragraph(f"[{p['marks']}]",ParagraphStyle("marks",parent=BODY,alignment=2))]],colWidths=[153*mm,8*mm]))
    if not q["parts"]: elems.append(Paragraph(f"[{q['marks']}]",ParagraphStyle("marks2",parent=BODY,alignment=2)))
    space={"small":10,"medium":20,"large":31}[q["working_space"]]*mm
    elems += [Spacer(1,space),Table([[""]],colWidths=[161*mm],rowHeights=[0.1],style=[("LINEABOVE",(0,0),(-1,-1),0.25,colors.HexColor("#D7DEE5"))]),Spacer(1,3)]
    return KeepTogether(elems)

def answer_block(a,marks):
    parts=[Paragraph(f"<b>{a['question_number']}</b>&nbsp;&nbsp;<b>{safe(a['final_answer'])}</b>",Q)]
    parts += [Paragraph(safe(x),BODY) for x in a["working"]]
    if a["mark_scheme"]: parts.append(Paragraph("Marks: "+safe(" · ".join(a["mark_scheme"]))+f" [{marks}]",SMALL))
    if a["acceptable_alternatives"]: parts.append(Paragraph("Accept: "+safe("; ".join(a["acceptable_alternatives"])),SMALL))
    parts += [Spacer(1,3),Table([[""]],colWidths=[161*mm],rowHeights=[0.1],style=[("LINEABOVE",(0,0),(-1,-1),0.35,RULE)]),Spacer(1,3)]
    return KeepTogether(parts)

def build(path,data,answer=False):
    doc=SimpleDocTemplate(str(path),pagesize=A4,rightMargin=17*mm,leftMargin=17*mm,topMargin=14*mm,bottomMargin=16*mm,title=data["metadata"]["title"])
    story=header(data,answer)
    m=data["metadata"]
    if answer:
        story += [Spacer(1,4),Paragraph(f"Total: {m['total_marks']} marks",SMALL),Spacer(1,5)]
        marks={q["number"]:q["marks"] for q in data["questions"]}
        story += [answer_block(a,marks[a["question_number"]]) for a in data["answers"]]
    else:
        meta=Table([[Paragraph("Name: ______________________________",BODY),Paragraph("Date: __________________",BODY)],[Paragraph(f"Time allowed: {m['time_allowed_minutes']} minutes",SMALL),Paragraph(f"Total marks: {m['total_marks']}",ParagraphStyle("metaR",parent=SMALL,alignment=2))]],colWidths=[105*mm,56*mm])
        meta.setStyle(TableStyle([("BACKGROUND",(0,1),(-1,1),SHADE),("BOX",(0,0),(-1,-1),0.45,RULE),("INNERGRID",(0,0),(-1,-1),0.25,RULE),("LEFTPADDING",(0,0),(-1,-1),5),("RIGHTPADDING",(0,0),(-1,-1),5)]))
        story += [Spacer(1,5),meta,Spacer(1,5),Paragraph("Show all necessary working. Give units where appropriate. Answer every question.",SMALL),Spacer(1,6)]
        story += [question_block(q) for q in data["questions"]]
        story += [Paragraph("End of Question Paper — check your answers.",ParagraphStyle("end",parent=SMALL,alignment=1,fontName="Helvetica-Bold"))]
    doc.build(story,onFirstPage=footer,onLaterPages=footer)

def merge(q,a,out):
    w=PdfWriter()
    for p in (q,a):
        for page in PdfReader(str(p)).pages: w.add_page(page)
    with open(out,"wb") as f:w.write(f)

def render(paper,output_dir):
    validate_paper(paper); data=json.loads(Path(paper).read_text(encoding="utf-8")); out=Path(output_dir); out.mkdir(parents=True,exist_ok=True)
    q,a,c=out/"Questions.pdf",out/"Answers.pdf",out/"Combined.pdf"; build(q,data); build(a,data,True); merge(q,a,c)
    counts=[len(PdfReader(str(x)).pages) for x in (q,a,c)]
    if counts != [1,1,2]: raise RuntimeError(f"House-format page count failed: {counts}; shorten content or split the set")
    return q,a,c
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("paper"); ap.add_argument("--output-dir",required=True); a=ap.parse_args();
    for p in render(a.paper,a.output_dir): print(p)
if __name__=="__main__":main()
