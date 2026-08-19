from export_portable_prompt import export
def test_export_is_focused():
    x=export("cie-0607-mathematics")
    assert "Canonical input" in x and "Generated-paper schema" in x and "Do not lay out PDFs" in x
