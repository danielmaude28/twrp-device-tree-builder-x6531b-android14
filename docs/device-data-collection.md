# Android 14 device data collection (read-only)

This guide collects evidence needed to build the X6531B device tree. It does
not flash, unlock, wipe, remount or modify the phone.

## Before collecting

- Confirm the handset is Infinix Hot 50i, model X6531B.
- Record the full Android build number, security patch and build fingerprint.
- Use a trusted ADB installation and USB cable.
- Temporary root may be used only for read-only inspection.
- Review output before sharing. Redact serial numbers, IMEI, account names,
  unique identifiers and other private values.

## ADB collection

Run these commands from a computer with ADB. Output is written to the computer.

~~~sh
mkdir -p x6531b-device-report
adb devices
adb shell getprop > x6531b-device-report/getprop.txt
adb shell uname -a > x6531b-device-report/uname.txt
adb shell cat /proc/version > x6531b-device-report/kernel-version.txt
adb shell cat /proc/cmdline > x6531b-device-report/kernel-cmdline.txt
adb shell cat /proc/bootconfig > x6531b-device-report/bootconfig.txt
adb shell cat /proc/partitions > x6531b-device-report/partitions.txt
adb shell cat /proc/mounts > x6531b-device-report/mounts.txt
adb shell cat /proc/filesystems > x6531b-device-report/filesystems.txt
adb shell ls -l /dev/block/by-name > x6531b-device-report/by-name.txt
adb shell ls -l /dev/block/mapper > x6531b-device-report/mapper.txt
adb shell cat /proc/modules > x6531b-device-report/modules-loaded.txt
adb shell 'find /vendor/lib/modules /vendor_dlkm/lib/modules /odm/lib/modules -type f 2>/dev/null' > x6531b-device-report/module-paths.txt
adb shell 'find /vendor/etc /odm/etc -name "fstab*" -type f 2>/dev/null' > x6531b-device-report/fstab-paths.txt
~~~

Some commands may return permission denied or paths may not exist. Keep the
error text; do not fill missing information by guessing.

## Optional read-only root collection

If temporary root is already available, these commands add evidence without
changing device state.

~~~sh
adb shell su -c 'cat /proc/1/mountinfo' > x6531b-device-report/mountinfo.txt
adb shell su -c 'for f in /vendor/etc/fstab* /odm/etc/fstab*; do [ -f "$f" ] && { echo "### $f"; cat "$f"; }; done' > x6531b-device-report/fstab-content.txt
adb shell su -c 'find /vendor/lib/modules /vendor_dlkm/lib/modules /odm/lib/modules -name "*.ko" -type f 2>/dev/null' > x6531b-device-report/module-files.txt
~~~

Do not upload private keys, credentials, app data, user data or complete
personal logs. Do not provide raw serial/IMEI values.

## Required evidence checklist

- [ ] Exact model and Android 14 build fingerprint (redacted if needed)
- [ ] Kernel release and compiler/build string
- [ ] Kernel command line and bootconfig
- [ ] Partition names and symlink targets
- [ ] Filesystem and mount information
- [ ] Actual fstab paths and contents
- [ ] Loaded modules and module file locations
- [ ] Module vermagic and dependencies, where readable
- [ ] Encryption and metadata-encryption properties (evidence only)

Device reports complement the stock firmware dump; they do not replace it.
A live mount table can differ from recovery expectations. A partition symlink,
module name or property alone is insufficient to finalize a device-tree entry.
Android 12 community trees remain comparison material only.
