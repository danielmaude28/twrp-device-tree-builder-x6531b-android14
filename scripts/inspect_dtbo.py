#!/usr/bin/env python3
"""Parse and validate the Android DTBO table header and entries."""
from __future__ import annotations
import argparse
import hashlib
import json
import struct
from pathlib import Path

DT_TABLE_MAGIC = 0xD7B7AB1E
HEADER_SIZE = 32
ENTRY_MIN_SIZE = 32


def inspect_dtbo(path: Path) -> dict:
    data = path.read_bytes()
    if len(data) < HEADER_SIZE:
        raise ValueError("file is smaller than DT table header")
    values = struct.unpack_from(">8I", data, 0)
    magic, total_size, header_size, entry_size, count, entries_offset, page_size, version = values
    if magic != DT_TABLE_MAGIC:
        raise ValueError(f"unexpected DTBO magic: 0x{magic:08x}")
    if header_size < HEADER_SIZE or header_size > len(data):
        raise ValueError("invalid DTBO header_size")
    if entry_size < ENTRY_MIN_SIZE:
        raise ValueError("DTBO entry_size is smaller than 32 bytes")
    if total_size > len(data) or total_size < header_size:
        raise ValueError("invalid DTBO total_size")
    entries_end = entries_offset + count * entry_size
    if entries_offset < header_size or entries_end > total_size:
        raise ValueError("DTBO entry table exceeds total_size")

    entries = []
    for index in range(count):
        offset = entries_offset + index * entry_size
        dt_size, dt_offset, board_id, rev, *custom = struct.unpack_from(">8I", data, offset)
        if dt_offset + dt_size > total_size:
            raise ValueError(f"DTBO entry {index} payload exceeds total_size")
        entries.append({
            "index": index, "dt_size": dt_size, "dt_offset": dt_offset,
            "id": board_id, "rev": rev, "custom": custom,
        })
    return {
        "file": path.name, "size_bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
        "magic": f"0x{magic:08x}", "total_size": total_size,
        "header_size": header_size, "entry_size": entry_size,
        "entry_count": count, "entries_offset": entries_offset,
        "page_size": page_size, "version": version, "entries": entries,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=Path("firmware/dtbo.img"))
    parser.add_argument("--output", type=Path, default=Path("reports/dtbo-inventory.json"))
    args = parser.parse_args()
    try:
        result = inspect_dtbo(args.input)
    except (OSError, ValueError, struct.error) as exc:
        parser.error(str(exc))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"DTBO report written: {args.output} ({result['entry_count']} entries)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
