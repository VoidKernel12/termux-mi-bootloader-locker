# DISCLAIMER — READ BEFORE LOCKING

**termux-mi-bootloader-locker** — Created by VoidKernel12

This tool sends irreversible `fastboot` lock commands to a connected Android device.

## You can brick the device

Relocking the bootloader on a Xiaomi / Redmi / Poco phone that is **not** running unmodified official stock firmware can permanently brick the unit. That includes:

- Custom ROMs (Xiaomi.eu, Pixel Experience, LineageOS, Evolution X, etc.)
- Magisk / KernelSU / APatch patched `boot` or `init_boot`
- Modified `vbmeta`, `cust`, `persist`, `modem`, or `abl`
- Downgraded firmware that trips anti-rollback (ARB)
- Fastboot-flashed images that do not match the locked AVB state

A locked bootloader will refuse to boot unsigned or mismatched partitions. Some Xiaomi boards have no documented unbrick path once that happens.

## No liability

By running `locker.py` or any command it wraps, you accept that:

1. You own the target device or have explicit authorization to modify it.
2. You understand locking may wipe userdata and may render the device unusable.
3. **VoidKernel12**, contributors, and distributors are **not responsible** for bricks, data loss, warranty void, anti-rollback trips, EDL-only states, or any other damage.
4. This software is provided **AS IS**, without warranty of any kind, express or implied.

If you are not 100% sure the device is on clean official stock and that locking is what you want — **stop**. Do not run the lock options.

Type `LOCK` in the tool only after you have read this file.
