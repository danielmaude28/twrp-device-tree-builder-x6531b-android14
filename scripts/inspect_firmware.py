#!/usr/bin/env python3
"""Create a safe inventory of stock firmware images and optionally unpack them.

This script does not flash devices and does not modify input images.
It requires AOSP unpack_bootimg.py for detailed boot/vendor_boot inspection.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

IMAGE_NAMES = ("boot.img", "init_boot.img", "vendor_boot.img", "dtbo.img")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def is_all_zero(path: Path) -> bool:
    """Return True when an image is a zero-filled placeholder."""
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            if any(chunk):
                return False
    return path.stat().st_size > 0


def inspect_magic(path: Path) -> str:
    with path.open("rb") as stream:
        magic = stream.read(8)
    if magic.startswith(b"ANDROID!"):
        return "ANDROID!"
    if magic.startswith(b"\xd7\xb7\xab\x1e"):
        return "DTBO (standard magic)"
    if magic.startswith(b"\x3a\xff\x26\xed"):
        return "DTB (FDT)"
    return magic.hex() or "empty"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=Path("firmware"))
    parser.add_argument("--output", type=Path, default=Path("reports"))
    parser.add_argument("--unpack-bootimg", type=Path, help="Path to AOSP unpack_bootimg.py")
    args = parser.parse_args()

    if not args.input.is_dir():
        parser.error(f"Input directory does not exist: {args.input}")

    args.output.mkdir(parents=True, exist_ok=True)
    records = []
    missing = []

    for name in IMAGE_NAMES:
        path = args.input / name
        if not path.is_file():
            missing.append(name)
            records.append({"name": name, "present": False})
            continue
        records.append({
            "name": name,
            "present": True,
            "size_bytes": path.stat().st_size,
            "sha256": sha256(path),
            "magic": inspect_magic(path),
            "content_status": "zero_filled_placeholder" if is_all_zero(path) else "present",
        })

    report = {
        "input_directory": str(args.input),
        "images": records,
        "missing_required_images": missing,
        "unpack_bootimg": str(args.unpack_bootimg) if args.unpack_bootimg else None,
        "unpack_results": [],
    }

    if args.unpack_bootimg:
        tool = args.unpack_bootimg
        if not tool.is_file():
            parser.error(f"unpack_bootimg.py not found: {tool}")
        for name in ("boot.img", "init_boot.img", "vendor_boot.img"):
            image = args.input / name
            if not image.is_file():
                continue
            if is_all_zero(image):
                report["unpack_results"].append({
                    "image": name,
                    "status": "skipped_zero_filled_placeholder",
                    "returncode": None,
                    "output_directory": None,
                })
                print(f"INFO: skipping zero-filled placeholder {name}")
                continue
            destination = args.output / image.stem
            destination.mkdir(parents=True, exist_ok=True)
            command = [
                sys.executable, str(tool),
                "--boot_img", str(image.resolve()),
                "--out", str(destination.resolve()),
            ]
            result = subprocess.run(command, text=True, capture_output=True)
            (destination / "stdout.txt").write_text(result.stdout, encoding="utf-8")
            (destination / "stderr.txt").write_text(result.stderr, encoding="utf-8")
            report["unpack_results"].append({
                "image": name,
                "status": "unpacked" if result.returncode == 0 else "failed",
                "returncode": result.returncode,
                "output_directory": str(destination),
            })
            if result.returncode != 0:
                report_path = args.output / "firmware-inventory.json"
                report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
                print(f"ERROR: unpack failed for {name}; see {destination}/stderr.txt", file=sys.stderr)
                return result.returncode

    report_path = args.output / "firmware-inventory.json"
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"Report written: {report_path}")
    if missing:
        print("Missing required images: " + ", ".join(missing), file=sys.stderr)
        return 2
    if not args.unpack_bootimg:
        print("Metadata unpack skipped: provide --unpack-bootimg for detailed inspection.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
