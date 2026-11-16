# Project status

This repository is the Android 14 firmware-analysis and device-tree preparation
workspace for Infinix Hot 50i X6531B. The current scope ends at a validated
device-tree candidate; it does not include building or flashing TWRP Recovery.

## Known facts

- Existing firmware dump release: dump1 in danielmaude28/twrp-x6531.
- Release metadata lists boot-related images and Novatek touchscreen assets.
- An earlier TWRP build workflow completed successfully, but that only confirms
  that its CI build command produced an output artifact.
- Prior workflow assumptions still require review, including boot offsets,
  vendor ramdisk extraction behavior, module handling and fstab paths.
- Community device trees located so far target Android 12 and are not proof of
  Android 14 compatibility.

## Repository materials now present

- Firmware inventory script and unit tests.
- Workflow to download every release asset and verify the GitHub-published
  size and SHA-256 digest before inspection.
- AOSP unpack_bootimg.py integration for boot, init_boot and vendor_boot.
- Read-only ADB and optional temporary-root data collection guide.
- Evidence matrix with confidence labels and explicit unknown states.
- Analysis plan and firmware configuration.

## Blocking evidence

- Actual Android 14 boot/vendor_boot header metadata and ramdisk table.
- Correct location and composition of the recovery ramdisk.
- Correct DTB and DTBO selection.
- Kernel release, configuration clues and module vermagic compatibility.
- Correct partition symlinks, fstab and logical partition layout.
- SELinux policy integration.
- Data and metadata decryption support.

## Current milestone

Milestone 1: analysis materials and automated source-asset verification
workflow are prepared. The workflow has not yet been run against dump1, so
no firmware metadata or extracted contents have been validated by CI.

## Acceptance rules

Do not mark evidence as confirmed until the actual artifact or read-only
device report has been inspected. Do not generate final device-tree values
from Android 12 assumptions. No TWRP recovery image is being built at this
stage, and no image is approved for flashing.
