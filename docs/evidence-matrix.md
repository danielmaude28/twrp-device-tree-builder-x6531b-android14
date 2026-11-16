# Device-tree evidence matrix

Replace PENDING only after the cited evidence has actually been inspected.

| Area | Evidence required | Preferred source | Status |
|---|---|---|---|
| Device identity | model, build fingerprint, Android release | live device properties | PENDING |
| Boot format | header version, page size, offsets, cmdline | Android 14 boot images + unpack report | PENDING |
| Recovery ramdisk | location, format, contents, init scripts | boot/init_boot/vendor_boot extraction | PENDING |
| Vendor ramdisk | fragment table, board IDs, fstab, init files | vendor_boot extraction | PENDING |
| Kernel | release, architecture, config clues, cmdline | boot image + device report | PENDING |
| DTB | compatible strings, board/revision identifiers | extracted DTB blobs | PENDING |
| DTBO | table header and overlay entries | dtbo.img | PENDING |
| Modules | vermagic, dependencies, symbols | firmware dump + live device | PENDING |
| Touchscreen | driver, module, firmware blob mapping | vendor files + device report | PENDING |
| Partitions | names, sizes, symlinks, logical layout | device report + fstab | PENDING |
| Filesystems | ext4/f2fs/EROFS and mount flags | fstab + live mounts | PENDING |
| Encryption | FBE, metadata encryption, key handling | fstab, properties, recovery evidence | PENDING |
| SELinux | policy files, contexts, init labels | vendor ramdisk and vendor image | PENDING |
| TWRP compatibility | target branch requirements and flags | current TWRP source documentation | PENDING |

## Confidence labels

- **Confirmed** — directly supported by target Android 14 firmware or a
  matching read-only report from the target handset.
- **Corroborated** — independently supported by more than one relevant source.
- **Reference only** — seen in Android 12 community source or another device;
  must not be copied as a final value.
- **Unknown** — insufficient evidence.
- **Physical test required** — static analysis cannot establish behavior.

## Acceptance gate

No generated device-tree file may silently turn a Reference only or Unknown
value into a confirmed configuration. Every generated file must include a
provenance note or be covered by the machine-readable report. This repository
does not build or flash a TWRP recovery image at this stage.
