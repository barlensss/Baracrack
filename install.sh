#!/data/data/com.termux/files/usr/bin/bash
# BARA CRACK - Installer

clear
echo -e "\033[1;31m"
echo "═══════════════════════════════════════"
echo "        BARA CRACK - INSTALLER        "
echo "═══════════════════════════════════════"
echo -e "\033[0m"

pkg update && pkg upgrade -y
pkg install python python-pip git -y
pip install --upgrade pip
pip install requests colorama pycryptodome

termux-setup-storage 2>/dev/null

mkdir -p /storage/emulated/0/barayk/

echo ""
echo -e "\033[1;32m[✓] INSTALL SELESAI\033[0m"
echo -e "\033[1;33m[!] Jalankan: python bara.py\033[0m"
