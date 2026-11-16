import struct
from pathlib import Path

import pytest

from scripts.inspect_dtbo import inspect_dtbo


def make_dtbo(path: Path):
    header = struct.pack(">8I", 0xD7B7AB1E, 72, 32, 32, 1, 32, 4096, 0)
    entry = struct.pack(">8I", 8, 64, 123, 4, 0, 0, 0, 0)
    path.write_bytes(header + entry + b"DTB!")


def test_inspect_dtbo_entry(tmp_path: Path):
    sample = tmp_path / "dtbo.img"
    make_dtbo(sample)
    report = inspect_dtbo(sample)
    assert report["entry_count"] == 1
    assert report["entries"][0]["id"] == 123
    assert report["entries"][0]["rev"] == 4


def test_reject_bad_magic(tmp_path: Path):
    sample = tmp_path / "bad.img"
    sample.write_bytes(bytes(64))
    with pytest.raises(ValueError, match="magic"):
        inspect_dtbo(sample)
