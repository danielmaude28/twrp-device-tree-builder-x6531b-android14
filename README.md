# TWRP Device Tree Builder — Infinix X6531B (Android 14)

An evidence-driven builder for analyzing stock firmware and generating a **reviewable starting point** for a TWRP device tree for the Infinix Hot 50i (X6531B), targeting the Android 14 firmware installed on the maintainer's device.

> **Status: early development.** This project does not yet produce a recovery image that is confirmed to boot. A successful CI run is not proof of device compatibility. Do not flash generated images until they have been reviewed and tested with a safe recovery procedure.

## Project goals

1. Inventory and verify the stock firmware inputs before modifying or generating anything.
2. Extract boot, init_boot, vendor_boot and DTBO metadata from the actual Android 14 firmware.
3. Preserve device-specific kernel, DTB, vendor ramdisk, fstab, modules and firmware where required.
4. Compare generated findings with community device trees without blindly inheriting Android 12 assumptions.
5. Generate a documented, reproducible device-tree candidate and run static validation.
6. Keep every uncertain value explicit; never silently guess offsets, partition paths, kernel configuration or encryption support.

## Target device

| Property | Target |
|---|---|
| Manufacturer | Infinix |
| Model | Hot 50i |
| Device | X6531B |
| Firmware target | Android 14 |
| Existing firmware dump release | [dump1](https://github.com/danielmaude28/twrp-x6531/releases/tag/dump1) |
| Related recovery build repository | [twrp-x6531](https://github.com/danielmaude28/twrp-x6531) |

The dump release is the source of truth for this project. Its contents must be downloaded and inspected before device-tree values are finalized.

## Planned inputs

- `boot.img`
- `init_boot.img`
- `vendor_boot.img`
- `dtbo.img`
- Kernel modules (`.ko`) and firmware blobs (`.bin`)
- Optional device-side read-only reports (partition map, mount table, kernel release, module vermagic and properties)

Do not commit proprietary firmware binaries or personal device data to this repository unless their redistribution is explicitly permitted. Prefer downloading the published dump as a workflow input.

## Development status

- [x] Repository initialized
- [ ] Firmware asset manifest and checksum verification
- [ ] Boot image and vendor_boot metadata extraction
- [ ] Vendor ramdisk extraction with strict error handling
- [ ] DTB / DTBO inventory and comparison
- [ ] Kernel module compatibility report
- [ ] Partition and fstab analysis
- [ ] Android 14 TWRP branch and build configuration review
- [ ] Device-tree candidate generation
- [ ] Static validation and CI artifact
- [ ] Physical boot and function testing

## Safety and validation

- No automatic flashing.
- No destructive device commands.
- No guessed partition offsets or fstab paths.
- Extraction failures must fail the job; they must not be hidden with `|| true`.
- CI must distinguish analysis success, compilation success and physical device validation.
- Encryption, FBE, metadata encryption and decryption remain unverified until tested on the target firmware.

## Repository layout

```
.
├── .github/workflows/
├── config/
├── docs/
├── scripts/
├── tests/
├── README.md
└── requirements.txt
```

## License

No license has been selected yet. Until one is added, all rights are reserved by default.
