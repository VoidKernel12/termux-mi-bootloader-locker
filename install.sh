#!/data/data/com.termux/files/usr/bin/bash
# termux-mi-bootloader-locker setup
# Created by VoidKernel12

set -euo pipefail

RED='\033[0;31m'
GRN='\033[0;32m'
YEL='\033[1;33m'
CYN='\033[0;36m'
NC='\033[0m'

echo -e "${CYN}==============================================${NC}"
echo -e "${CYN}  termux-mi-bootloader-locker — installer${NC}"
echo -e "${CYN}  Created by VoidKernel12${NC}"
echo -e "${CYN}==============================================${NC}"
echo
echo -e "${YEL}Use Termux + Termux:API from F-Droid only.${NC}"
echo -e "${YEL}Play Store Termux is unsupported.${NC}"
echo

echo -e "${GRN}[*] Updating packages...${NC}"
pkg update -y
pkg upgrade -y

echo -e "${GRN}[*] Installing python, android-tools, termux-api...${NC}"
pkg install -y python android-tools termux-api

if command -v termux-setup-storage >/dev/null 2>&1; then
    echo -e "${GRN}[*] Requesting storage permission...${NC}"
    termux-setup-storage || true
fi

chmod +x locker.py 2>/dev/null || true

echo
if command -v fastboot >/dev/null 2>&1; then
    echo -e "${GRN}[+] fastboot: $(fastboot --version 2>/dev/null | head -n1 || echo ready)${NC}"
else
    echo -e "${RED}[!] fastboot not found after install. Check pkg mirrors.${NC}"
fi

echo
echo -e "${GRN}[+] Setup complete.${NC}"
echo -e "    Run:  ${CYN}python locker.py${NC}"
echo
