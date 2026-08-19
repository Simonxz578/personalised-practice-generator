from pathlib import Path
from pypdf import PdfReader
from render_pdfs import render
ROOT=Path(__file__).resolve().parents[1]
def test_pdf_house_format(tmp_path):
    q,a,c=render(ROOT/"examples/generated-paper-example.json",tmp_path)
    assert [len(PdfReader(str(x)).pages) for x in (q,a,c)]==[1,1,2]
    qt="".join((p.extract_text() or "") for p in PdfReader(str(q)).pages)
    assert "Answers and Worked Solutions" not in qt and "y = -2x + 3" not in qt
    ct=[" ".join((p.extract_text() or "").split()) for p in PdfReader(str(c)).pages]
    assert "Question Paper" in ct[0] and "Answers and Worked Solutions" in ct[1]
