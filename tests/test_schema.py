import json,pytest
from pathlib import Path
from validate_schema import validate
ROOT=Path(__file__).resolve().parents[1]
def test_paper_schema(): validate(ROOT/"examples/generated-paper-example.json",ROOT/"assets/generated-paper.schema.json")
def test_malformed_json(tmp_path):
    p=tmp_path/"bad.json";p.write_text("{")
    with pytest.raises(json.JSONDecodeError):validate(p,ROOT/"assets/generated-paper.schema.json")
