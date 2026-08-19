import json
from pathlib import Path
from validate_math import validate
ROOT=Path(__file__).resolve().parents[1]
def test_math_checks():
    checks=validate(json.loads((ROOT/"examples/generated-paper-example.json").read_text()))
    assert all("passed" in x for x in checks)
