import hashlib
from pathlib import Path

from scripts.inspect_firmware import inspect_magic, sha256


def test_sha256(tmp_path: Path):
    sample = tmp_path / "sample.img"
    sample.write_bytes(b"firmware")
    assert sha256(sample) == hashlib.sha256(b"firmware").hexdigest()


def test_android_magic(tmp_path: Path):
    sample = tmp_path / "boot.img"
    sample.write_bytes(b"ANDROID!" + b"\x00" * 8)
    assert inspect_magic(sample) == "ANDROID!"


def test_unknown_magic(tmp_path: Path):
    sample = tmp_path / "unknown.img"
    sample.write_bytes(b"not-an-image")
    assert inspect_magic(sample) == b"not-an-i".hex()
