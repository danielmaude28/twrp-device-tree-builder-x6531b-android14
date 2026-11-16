import hashlib
import json
from pathlib import Path

from scripts.inspect_firmware import inspect_magic, sha256
from scripts.verify_release_assets import main as verify_main


def test_sha256(tmp_path: Path):
    sample = tmp_path / "sample.img"
    sample.write_bytes(b"firmware")
    assert sha256(sample) == hashlib.sha256(b"firmware").hexdigest()


def test_android_magic(tmp_path: Path):
    sample = tmp_path / "boot.img"
    sample.write_bytes(b"ANDROID!" + bytes(8))
    assert inspect_magic(sample) == "ANDROID!"


def test_unknown_magic(tmp_path: Path):
    sample = tmp_path / "unknown.img"
    sample.write_bytes(b"not-an-image")
    assert inspect_magic(sample) == b"not-an-i".hex()


def test_release_asset_verification_passes(tmp_path: Path, monkeypatch):
    firmware = tmp_path / "firmware"
    firmware.mkdir()
    payload = b"stock-image"
    (firmware / "boot.img").write_bytes(payload)
    release = {
        "tag_name": "dump1",
        "html_url": "https://github.com/example/repo/releases/tag/dump1",
        "assets": [{
            "name": "boot.img",
            "size": len(payload),
            "digest": "sha256:" + hashlib.sha256(payload).hexdigest(),
        }],
    }
    metadata = tmp_path / "release.json"
    metadata.write_text(json.dumps(release), encoding="utf-8")
    output = tmp_path / "report.json"
    monkeypatch.setattr("sys.argv", [
        "verify_release_assets", "--release-json", str(metadata),
        "--input", str(firmware), "--output", str(output),
    ])
    assert verify_main() == 0
    result = json.loads(output.read_text(encoding="utf-8"))
    assert result["verified_count"] == 1
    assert result["failures"] == []


def test_release_asset_verification_detects_mismatch(tmp_path: Path, monkeypatch):
    firmware = tmp_path / "firmware"
    firmware.mkdir()
    (firmware / "boot.img").write_bytes(b"wrong")
    release = {"tag_name": "dump1", "assets": [{
        "name": "boot.img", "size": 5, "digest": "sha256:" + "0" * 64,
    }]}
    metadata = tmp_path / "release.json"
    metadata.write_text(json.dumps(release), encoding="utf-8")
    output = tmp_path / "report.json"
    monkeypatch.setattr("sys.argv", [
        "verify_release_assets", "--release-json", str(metadata),
        "--input", str(firmware), "--output", str(output),
    ])
    assert verify_main() == 2
    result = json.loads(output.read_text(encoding="utf-8"))
    assert result["failures"] == ["boot.img"]
