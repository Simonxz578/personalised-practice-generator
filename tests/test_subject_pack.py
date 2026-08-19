import pytest
from pathlib import Path
from validate_pack import validate_subject_pack
def test_invalid_pack(tmp_path):
    p=tmp_path/"pack.md";p.write_text("subject: X")
    with pytest.raises(ValueError):validate_subject_pack(p)
