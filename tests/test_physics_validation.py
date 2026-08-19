import json
from pathlib import Path
from validate_physics import validate
ROOT=Path(__file__).resolve().parents[1]
def test_physics_checks():
    checks=validate(json.loads((ROOT/"examples/generated-paper-physics.json").read_text()))
    assert checks[0].endswith("passed") and checks[1].endswith("passed")
