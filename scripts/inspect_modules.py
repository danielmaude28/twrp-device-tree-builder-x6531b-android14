#!/usr/bin/env python3
"""Inventory kernel modules and firmware blobs without modifying them."""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import struct
from pathlib import Path

MACHINE_NAMES = {3: "x86", 40: "ARM", 62: "x86_64", 183: "AArch64"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def elf_metadata(data: bytes) -> dict:
    if len(data) < 20 or data[:4] != b"\x7fELF":
        return {"is_elf": False}
    elf_class, encoding = data[4], data[5]
    if encoding not in (1, 2):
        return {"is_elf": True, "error": "unknown ELF byte order"}
    endian = "<" if encoding == 1 else ">"
    machine = struct.unpack_from(endian + "H", data, 18)[0]
    return {
        "is_elf": True,
        "elf_class": {1: 32, 2: 64}.get(elf_class, elf_class),
        "machine_id": machine,
        "architecture": MACHINE_NAMES.get(machine, "unknown"),
    }


def module_strings(data: bytes) -> dict:
    result = {}
    for key in ("name", "vermagic", "depends", "license", "description"):
        match = re.search(rb"(?:^|\x00)" + key.encode() + rb"=([^\x00]+)", data)
        if match:
            result[key] = match.group(1).decode("utf-8", errors="replace")
    return result


def inspect_tree(root: Path) -> dict:
    modules, blobs = [], []
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        record = {"path": str(path.relative_to(root)), "size_bytes": path.stat().st_size,
                  "sha256": sha256(path)}
        if path.suffix == ".ko":
            data = path.read_bytes()
            record.update(elf_metadata(data))
            record.update(module_strings(data))
            modules.append(record)
        elif path.suffix == ".bin":
            blobs.append(record)
    return {"root": str(root), "module_count": len(modules),
            "firmware_blob_count": len(blobs), "modules": modules,
            "firmware_blobs": blobs}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=Path("firmware"))
    parser.add_argument("--output", type=Path, default=Path("reports/module-inventory.json"))
    args = parser.parse_args()
    if not args.input.is_dir():
        parser.error(f"Input directory does not exist: {args.input}")
    result = inspect_tree(args.input)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"Module report written: {args.output} ({result['module_count']} modules)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
