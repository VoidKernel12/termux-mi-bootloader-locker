#!/usr/bin/env python3
"""
termux-mi-bootloader-locker
Interactive fastboot locker for Xiaomi / Redmi / Poco via Termux + OTG
Created by VoidKernel12
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from typing import List, Optional


class C:
    R = "\033[0;31m"
    G = "\033[0;32m"
    Y = "\033[1;33m"
    M = "\033[0;35m"
    C = "\033[0;36m"
    W = "\033[1;37m"
    D = "\033[2m"
    N = "\033[0m"
    BOLD = "\033[1m"


BANNER = f"""
{C.C}╔══════════════════════════════════════════════════════╗
║{C.W}     termux-mi-bootloader-locker                      {C.C}║
║{C.D}     Created by VoidKernel12                          {C.C}║
╚══════════════════════════════════════════════════════╝{C.N}
"""

FAMILIES = [
    "Xiaomi (Mi / Mix / Civi)",
    "Redmi (Note / Number series)",
    "POCO",
    "Other Xiaomi-family / unknown",
]


def clear() -> None:
    os.system("clear" if os.name != "nt" else "cls")


def run_fastboot(args: List[str], timeout: int = 30) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["fastboot", *args],
        capture_output=True,
        text=True,
        timeout=timeout,
    )


def which_fastboot() -> Optional[str]:
    return shutil.which("fastboot")


def list_devices() -> List[str]:
    try:
        p = run_fastboot(["devices"], timeout=10)
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return []
    lines = []
    for raw in (p.stdout or "").splitlines():
        raw = raw.strip()
        if not raw:
            continue
        parts = raw.split()
        if parts:
            lines.append(parts[0])
    return lines


def print_cmd_result(p: subprocess.CompletedProcess) -> None:
    out = (p.stdout or "").strip()
    err = (p.stderr or "").strip()
    if out:
        print(f"{C.W}{out}{C.N}")
    if err:
        print(f"{C.Y}{err}{C.N}")
    if p.returncode == 0:
        print(f"{C.G}[+] Command finished (exit {p.returncode}){C.N}")
    else:
        print(f"{C.R}[!] Command failed (exit {p.returncode}){C.N}")


def require_device() -> Optional[str]:
    devs = list_devices()
    if not devs:
        print(f"{C.R}[!] No fastboot device detected.{C.N}")
        print(f"{C.Y}    Put the target in fastboot and connect it over OTG.{C.N}")
        return None
    if len(devs) == 1:
        print(f"{C.G}[+] Device: {devs[0]}{C.N}")
        return devs[0]
    print(f"{C.Y}Multiple devices:{C.N}")
    for i, d in enumerate(devs, 1):
        print(f"  {i}) {d}")
    try:
        n = int(input(f"{C.C}Select device number: {C.N}").strip())
        return devs[n - 1]
    except (ValueError, IndexError):
        print(f"{C.R}[!] Invalid selection.{C.N}")
        return None


def confirm_lock() -> bool:
    print(f"{C.R}{C.BOLD}")
    print("  WARNING: This will LOCK the bootloader.")
    print("  Custom ROMs / patched partitions can BRICK Xiaomi devices.")
    print("  Userdata is usually wiped. Author assumes NO liability.")
    print(f"{C.N}")
    print("  Read DISCLAIMER.md. Type LOCK in capitals to proceed.")
    ans = input(f"{C.Y}  Confirmation: {C.N}").strip()
    return ans == "LOCK"


def do_lock(method: str) -> None:
    if not which_fastboot():
        print(f"{C.R}[!] fastboot not in PATH. Run install.sh first.{C.N}")
        return
    serial = require_device()
    if not serial:
        return

    print(f"{C.C}[*] Querying unlocked state...{C.N}")
    try:
        info = run_fastboot(["getvar", "unlocked"], timeout=10)
        print_cmd_result(info)
    except subprocess.TimeoutExpired:
        print(f"{C.Y}[!] getvar timed out (device still usable).{C.N}")

    if not confirm_lock():
        print(f"{C.Y}[-] Aborted. Nothing sent.{C.N}")
        return

    args = ["flashing", "lock"] if method == "flashing" else ["oem", "lock"]
    print(f"{C.M}[*] Sending: fastboot {' '.join(args)}{C.N}")
    try:
        p = run_fastboot(args, timeout=60)
        print_cmd_result(p)
    except subprocess.TimeoutExpired:
        print(f"{C.Y}[!] Timed out. Check the phone screen for a confirm dialog.{C.N}")
        return

    print(f"{C.C}[*] Re-checking devices...{C.N}")
    left = list_devices()
    if left:
        print(f"{C.W}    Still in fastboot: {', '.join(left)}{C.N}")
    else:
        print(f"{C.G}    Device left fastboot (often expected after lock + wipe).{C.N}")


def show_vars() -> None:
    if not which_fastboot():
        print(f"{C.R}[!] fastboot missing.{C.N}")
        return
    if not require_device():
        return
    for var in ("product", "unlocked", "secure", "current-slot", "anti"):
        print(f"{C.C}--- {var} ---{C.N}")
        try:
            print_cmd_result(run_fastboot(["getvar", var], timeout=8))
        except subprocess.TimeoutExpired:
            print(f"{C.Y}timeout{C.N}")


def menu_family() -> None:
    print(f"{C.W}Device family (informational only):{C.N}")
    for i, name in enumerate(FAMILIES, 1):
        print(f"  {C.C}{i}{C.N}) {name}")
    choice = input(f"{C.C}Select [1-{len(FAMILIES)}]: {C.N}").strip()
    try:
        idx = int(choice) - 1
        print(f"{C.G}[+] Selected: {FAMILIES[idx]}{C.N}")
        print(f"{C.D}    Use flashing lock on HyperOS / recent MIUI.{C.N}")
        print(f"{C.D}    Use oem lock only on older devices that reject flashing lock.{C.N}")
    except (ValueError, IndexError):
        print(f"{C.R}[!] Invalid family.{C.N}")


def print_menu() -> None:
    print(f"""
{C.W}  [1]{C.N} Detect fastboot device
{C.W}  [2]{C.N} Select device family
{C.W}  [3]{C.N} Show fastboot variables
{C.R}  [4]{C.N} Lock bootloader  {C.D}(fastboot flashing lock){C.N}
{C.R}  [5]{C.N} Lock bootloader  {C.D}(fastboot oem lock){C.N}
{C.W}  [6]{C.N} Reboot device    {C.D}(fastboot reboot){C.N}
{C.W}  [0]{C.N} Exit
""")


def reboot_device() -> None:
    if not require_device():
        return
    try:
        print_cmd_result(run_fastboot(["reboot"], timeout=15))
    except subprocess.TimeoutExpired:
        print(f"{C.Y}[!] reboot timed out.{C.N}")


def main() -> int:
    clear()
    print(BANNER)
    print(f"{C.Y}Termux + Termux:API must come from F-Droid, not Play Store.{C.N}")
    print(f"{C.Y}Read DISCLAIMER.md before using options 4 or 5.{C.N}")

    if not which_fastboot():
        print(f"{C.R}[!] fastboot not found. Run: bash install.sh{C.N}")

    while True:
        print_menu()
        choice = input(f"{C.C}void@locker > {C.N}").strip()
        if choice == "1":
            devs = list_devices()
            if devs:
                print(f"{C.G}[+] {len(devs)} device(s): {', '.join(devs)}{C.N}")
            else:
                print(f"{C.R}[!] No devices. Check OTG, cable, and fastboot mode.{C.N}")
        elif choice == "2":
            menu_family()
        elif choice == "3":
            show_vars()
        elif choice == "4":
            do_lock("flashing")
        elif choice == "5":
            do_lock("oem")
        elif choice == "6":
            reboot_device()
        elif choice == "0":
            print(f"{C.C}Bye.{C.N}")
            return 0
        else:
            print(f"{C.R}[!] Unknown option.{C.N}")
        print()


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print(f"\n{C.Y}Interrupted.{C.N}")
        sys.exit(130)
