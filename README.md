# TWRP Device Tree Builder — Infinix X6531B (Android 14)

An evidence-driven project for analyzing stock firmware and generating a
**reviewable starting point** for a TWRP device tree for the Infinix Hot 50i
(X6531B), targeting the Android 14 firmware installed on the handset.

> **Scope:** this stage builds and validates the device tree only. It does not
> build a TWRP recovery image or flash the device. A successful analysis or CI
> run is not proof of recovery boot compatibility.

## Project goals

1. Inventory and verify every published stock-dump release asset.
2. Extract boot, init_boot and vendor_boot metadata from Android 14 firmware.
3. Preserve device-specific kernel, DTB, vendor ramdisk, fstab, modules and firmware.
4. Inventory DTBO and compare device-tree evidence with community sources.
5. Collect read-only live-device evidence for partitions, mounts and kernel modules.
6. Generate a documented, reproducible device-tree candidate and run static validation.
7. Keep uncertain values explicit; never guess offsets, partition paths, kernel
   configuration or encryption support.

## Target device

| Property | Target |
|---|---|
| Manufacturer | Infinix |
| Model | Hot 50i |
| Device | X6531B |
| Firmware target | Android 14 |
| Existing firmware dump | [dump1](https://github.com/danielmaude28/twrp-x6531/releases/tag/dump1) |
| Related source repository | [twrp-x6531](https://github.com/danielmaude28/twrp-x6531) |

The Android 14 dump and read-only reports from the target handset are the
primary evidence. Android 12 community trees are comparison material only.

## Materials and workflow

- Required images: boot.img, init_boot.img, vendor_boot.img and dtbo.img.
- Additional release assets: kernel modules (.ko) and firmware blobs (.bin).
- Release API metadata and SHA-256 verification for every downloaded asset.
- AOSP unpack_bootimg.py output for boot-related images.
- DTBO table header and entry parser plus .ko / .bin inventory.
- Read-only ADB/root collection guide: docs/device-data-collection.md.
- Evidence and confidence tracking: docs/evidence-matrix.md.

Run **Actions → Firmware inspection → Run workflow** and select release tag
dump1. The workflow runs tests, downloads every release asset, verifies file
sizes and SHA-256 digests, then inventories and unpacks the boot images. It
uploads reports and downloaded inputs as a temporary artifact.

## Development status

- [x] Repository scaffold and source-of-truth documentation
- [x] Read-only device data collection guide
- [x] Evidence matrix and confidence labels
- [x] Release asset download and SHA-256 verification
- [ ] Run inspection against dump1 and review the artifact
- [ ] Boot image and vendor_boot metadata analysis
- [ ] Vendor ramdisk extraction and inventory
- [ ] DTB / DTBO inventory and comparison
- [ ] Kernel and module compatibility report
- [ ] Partition, fstab and encryption analysis
- [ ] Android 14 TWRP device-tree candidate
- [ ] Static validation of generated device-tree files

## Safety and validation

- No automatic flashing or destructive device commands.
- No guessed partition offsets or fstab paths.
- Extraction failures must fail the job; they must not be hidden.
- CI analysis success is not build success or physical validation.
- Encryption, FBE, metadata encryption and decryption remain unverified until
  supported by evidence and tested on the target device.

## Repository layout

~~~text
.
├── .github/workflows/
├── config/
├── docs/
├── scripts/
├── tests/
├── README.md
└── requirements.txt
~~~

## License

No license has been selected yet. Until one is added, all rights are reserved
by default.
