# Initial status

This repository is a clean project scaffold for the Infinix X6531B Android 14 target.

## Known facts from the existing work

- The existing firmware dump release is `dump1` in `danielmaude28/twrp-x6531`.
- The release contains boot-related images and Novatek touchscreen assets.
- An earlier TWRP build workflow completed successfully, but that only confirms that the CI build command produced its expected output.
- The prior workflow configuration contains assumptions that still require review, including boot offsets, vendor ramdisk extraction behavior, module handling and fstab paths.
- The community device trees located so far target Android 12 and must not be treated as proof of Android 14 compatibility.

## Blocking unknowns

- Actual Android 14 boot/vendor_boot header metadata and ramdisk table
- Correct location and composition of the recovery ramdisk
- Correct DTB and DTBO selection
- Kernel release and module vermagic compatibility
- Correct partition symlinks and fstab
- SELinux policy integration
- Data and metadata decryption support

## Current milestone

Milestone 0: repository scaffold and source-of-truth documentation.

No device tree has been declared complete and no image from this repository is approved for flashing.
