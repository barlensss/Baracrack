#!/data/data/com.termux/files/usr/bin/bash
clear
echo -e "\033[1;31m"
echo "═══════════════════════════════════════"
echo "      BARA CRACK v2.0 - INSTALLER     "
echo "═══════════════════════════════════════"
echo -e "\033[0m"

pkg update && pkg upgrade -y
pkg install python python-pip git nodejs-lts -y
pip install --upgrade pip
pip install requests colorama pycryptodome beautifulsoup4 lxml
pip install playwright
playwright install chromium

termux-setup-storage 2>/dev/null
mkdir -p /storage/emulated/0/barayk/

echo ""
echo -e "\033[1;32m[✓] INSTALL SELESAI\033[0m"
echo -e "\033[1;33m[!] Jalankan: python bara.py\033[0m"
