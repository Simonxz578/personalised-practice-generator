import json,pytest
from pathlib import Path
from validate_marks import validate
ROOT=Path(__file__).resolve().parents[1]
def test_marks():validate(json.loads((ROOT/"examples/generated-paper-example.json").read_text()))
def test_bad_total():
    d=json.loads((ROOT/"examples/generated-paper-example.json").read_text());d["metadata"]["total_marks"]=99
    with pytest.raises(ValueError):validate(d)
