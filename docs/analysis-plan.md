# Firmware-first analysis plan

## 1. Establish provenance

Record the release tag, asset names, sizes and SHA-256 digests from GitHub
release metadata. Keep original inputs immutable. A checksum proves that a
download matches the published asset digest; it does not prove that the dump
is complete or that it came from the correct handset. Record the device build
fingerprint separately.

## 2. Inspect all boot-related images

Inspect boot.img, init_boot.img, vendor_boot.img and dtbo.img independently.

Capture, where applicable:
- boot header version and page size
- kernel and ramdisk sizes
- kernel command line and bootconfig
- vendor ramdisk fragments, names, types and board IDs
- DTB location and DTB count
- recovery-DTBO metadata
- compression formats and extraction errors

Do not assume that the recovery ramdisk belongs in the same image or partition
as an Android 12 community tree.

## 3. Inspect vendor ramdisk contents

Preserve and inventory:
- first-stage init files and fstab
- recovery-related init and ueventd rules
- SELinux policy and file contexts
- kernel modules and dependency metadata
- vendor firmware blobs
- dynamic partition and metadata-encryption configuration

Extraction errors are fatal. Never continue with a partially extracted ramdisk.

## 4. Inspect kernel and modules

Record kernel release, architecture, compiler/build string and available
configuration evidence. Record each module's vermagic, dependencies and
architecture where tooling permits. Check symbol requirements when matching
kernel symbol data is available. A module filename alone does not establish
compatibility.

## 5. Inspect DTB and DTBO

Extract and enumerate all DTBs and overlays. Capture compatible strings,
board identifiers and relevant hardware nodes. Compare overlays against
device properties and boot logs. Do not select an overlay by filename alone.

## 6. Inspect partitions and encryption

Use both firmware fstab/init evidence and read-only device reports. Derive
partition names and symlinks from the target device. Verify logical partition
layout, filesystem types, metadata partition and encryption behavior. Do not
enable decryption based solely on community configuration.

## 7. Collect live-device evidence

Follow docs/device-data-collection.md. Collect build properties, kernel
release, command line, bootconfig, partition symlinks, mounts, filesystem
types, loaded modules and actual fstab contents when readable. Redact
identifiers and personal information before sharing.

## 8. Compare community sources

Community trees are references, not authoritative firmware data. Record every
adopted value with its source and confidence:
- confirmed by Android 14 stock image
- confirmed by read-only device report
- borrowed from community tree and still unverified
- unknown / requires physical test

## 9. Generate and validate

Generation must be deterministic and preserve provenance. Static validation
should check required files, paths, image metadata, fstab syntax and build
configuration. CI success is not physical validation.

## 10. Physical test gate

No flashing is performed by this project. Before any future test, prepare a
verified stock restore path and confirm the exact target partition and image
format. Test boot, touch, ADB, storage, MTP, logs, reboot and encryption
separately.
