#!/usr/bin/env python3
"""Verify downloaded files against GitHub release asset metadata."""
from __future__ import annotations
import argparse
import hashlib
import json
import sys
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--release-json", type=Path, required=True)
    parser.add_argument("--input", type=Path, default=Path("firmware"))
    parser.add_argument("--output", type=Path, default=Path("reports/asset-verification.json"))
    args = parser.parse_args()
    if not args.release_json.is_file():
        parser.error(f"Release metadata not found: {args.release_json}")
    if not args.input.is_dir():
        parser.error(f"Input directory does not exist: {args.input}")

    release = json.loads(args.release_json.read_text(encoding="utf-8"))
    assets = release.get("assets", [])
    records, failures = [], []
    for asset in assets:
        name = asset.get("name")
        path = args.input / name if name else None
        expected = asset.get("digest")
        record = {"name": name, "size_expected": asset.get("size"),
                  "digest_expected": expected,
                  "present": bool(path and path.is_file())}
        if not path or not path.is_file():
            record["status"] = "missing"
            failures.append(name or "<unnamed asset>")
        else:
            actual_size = path.stat().st_size
            actual_digest = "sha256:" + sha256(path)
            record.update({"size_actual": actual_size, "digest_actual": actual_digest})
            if actual_size != asset.get("size"):
                record["status"] = "size_mismatch"
                failures.append(name)
            elif not expected:
                record["status"] = "digest_unavailable"
                failures.append(name)
            elif actual_digest.lower() != expected.lower():
                record["status"] = "digest_mismatch"
                failures.append(name)
            else:
                record["status"] = "verified"
        records.append(record)

    report = {"release": release.get("tag_name"),
              "repository_url": release.get("html_url"),
              "asset_count": len(assets),
              "verified_count": sum(r["status"] == "verified" for r in records),
              "failures": failures, "assets": records}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"Verification report written: {args.output}")
    if failures:
        print("Asset verification failed: " + ", ".join(failures), file=sys.stderr)
        return 2
    if not assets:
        print("Release contains no assets.", file=sys.stderr)
        return 3
    print(f"Verified {len(records)} release assets.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
