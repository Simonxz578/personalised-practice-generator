from pathlib import Path

from pypdf import PdfReader
from render_pdfs import format_math_text, render

ROOT = Path(__file__).resolve().parents[1]

CASES = {
    "x₁ x₂ y₁ y₂ v₁ v₂ x₁₂": "x<sub>1</sub> x<sub>2</sub> y<sub>1</sub> y<sub>2</sub> v<sub>1</sub> v<sub>2</sub> x<sub>12</sub>",
    "m/s² m/s³ cm² m³ s⁻¹ x² x³": "m/s<super>2</super> m/s<super>3</super> cm<super>2</super> m<super>3</super> s<super>-1</super> x<super>2</super> x<super>3</super>",
    "Gradient = (y₂ - y₁)/(x₂ - x₁)": "Gradient = (y<sub>2</sub> - y<sub>1</sub>)/(x<sub>2</sub> - x<sub>1</sub>)",
    "Gradient = (−3 - 7)/(6 - (−4))": "Gradient = (-3 - 7)/(6 - (-4))",
    "v² = u² + 2as; 25 cm²; 1200 kg/m³": "v<super>2</super> = u<super>2</super> + 2as; 25 cm<super>2</super>; 1200 kg/m<super>3</super>",
}

def test_math_unicode_is_normalised_after_escaping():
    for raw, expected in CASES.items():
        assert format_math_text(raw) == expected

def test_literal_markup_and_entities_remain_escaped():
    rendered = format_math_text("A < B & x₁; literal <sub>9</sub> & \'quote\'")
    assert rendered == "A &lt; B &amp; x<sub>1</sub>; literal &lt;sub&gt;9&lt;/sub&gt; &amp; &#x27;quote&#x27;"

def test_typography_sample_renders_without_raw_tags(tmp_path):
    questions, answers, combined = render(ROOT / "examples/generated-paper-typography.json", tmp_path)
    assert [len(PdfReader(str(path)).pages) for path in (questions, answers, combined)] == [1, 1, 2]
    text = " ".join((page.extract_text() or "") for page in PdfReader(str(combined)).pages)
    assert "<sub>" not in text and "<super>" not in text
    for fragment in ("Gradient = (y", "m/s", "cm", "kg/m", "s-1", "x12"):
        assert fragment in text.replace(" ", "") or fragment in text
