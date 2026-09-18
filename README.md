# termux-mi-bootloader-locker

**Created by VoidKernel12**

A Termux-based interactive tool to lock the bootloader on Xiaomi / Redmi / Poco devices over USB OTG using `fastboot`.

This project follows the same layout and conventions as **termux-image-dumper**.

---

## Features

- Interactive color-coded terminal menu
- Device detection via `fastboot devices`
- Xiaomi / Redmi / Poco device family selection
- Lock sequences:
  - `fastboot flashing lock` (modern devices)
  - `fastboot oem lock` (legacy devices)
- Pre-lock checks: device online, unlocked state
- Explicit typed confirmation (`LOCK`) before any lock command is sent
- Designed to run from a second Android phone with Termux + OTG

---

## Requirements

> **IMPORTANT:** Install **Termux** and **Termux:API** from **F-Droid APKs only**.  
> Do **not** use the old Google Play Store Termux. That build is unmaintained and will break `pkg`, `python`, `android-tools`, and USB accessories.

You need:

1. [Termux (F-Droid)](https://f-droid.org/en/packages/com.termux/)
2. [Termux:API (github)](https://github.com/termux/termux-api)
3. A USB-OTG adapter
4. The target Xiaomi / Redmi / Poco device in **fastboot** mode
5. An already **unlocked** bootloader (you cannot lock what was never unlocked)

Packages installed by `install.sh`:

- `python`
- `android-tools` (provides `fastboot` / `adb`)
- `termux-api`

---

## Installation

If you cloned from GitHub:

```bash
git clone https://github.com/VoidKernel12/termux-mi-bootloader-locker.git

```

```bash
cd termux-mi-bootloader-locker

```

```bash
chmod +x install.sh locker.py

```

```bash
bash install.sh

```

```bash
python locker.py
```

---

## Fastboot locking usage

1. Power off the **target** Xiaomi / Poco / Redmi device.
2. Boot it to fastboot (usually Volume Down + Power).
3. Connect target → OTG adapter → host phone.
4. On Termux run `python locker.py`.
5. Choose **Detect device**. Confirm a serial appears.
6. Choose the lock method that matches your device generation.
7. Type `LOCK` exactly when prompted.
8. Confirm on the target phone screen if it asks to lock.

### Recommended command mapping

| Generation | Menu option | Command |
|---|---|---|
| MIUI 12+ / HyperOS | Flashing lock | `fastboot flashing lock` |
| Older MIUI | OEM lock | `fastboot oem lock` |

After a successful lock the device usually factory-resets and boots stock-signed firmware only.

---

## Safety

Read **DISCLAIMER.md** before you touch a lock command.

Locking with a custom ROM, modified `vbmeta`, Magisk, or unsigned partitions can **hard-brick** Xiaomi devices (especially those with anti-rollback). Relock only on clean official stock firmware.

---

## License

Provided as-is for personal use on devices you own. No warranty.
