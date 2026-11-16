import struct
from pathlib import Path

from scripts.inspect_modules import elf_metadata, inspect_tree


def test_elf_metadata_arm64():
    data = bytearray(20)
    data[:4] = b"\x7fELF"
    data[4] = 2
    data[5] = 1
    struct.pack_into("<H", data, 18, 183)
    result = elf_metadata(bytes(data))
    assert result["architecture"] == "AArch64"
    assert result["elf_class"] == 64


def test_inspect_tree_counts_modules_and_blobs(tmp_path: Path):
    (tmp_path / "driver.ko").write_bytes(b"module\x00vermagic=6.1-test SMP")
    (tmp_path / "touch.bin").write_bytes(b"firmware")
    result = inspect_tree(tmp_path)
    assert result["module_count"] == 1
    assert result["firmware_blob_count"] == 1
    assert result["modules"][0]["vermagic"] == "6.1-test SMP"
