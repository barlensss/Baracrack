#!/usr/bin/env python3
# BARA CRACK v1.0
# Author: CJ

import os, sys, time, json, hashlib, base64, random, string
import requests
from colorama import Fore, Style, init
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

init(autoreset=True)

OUTPUT_DIR = "/storage/emulated/0/barayk/"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ============ UTIL ============

def clear():
    os.system("clear")

def typewriter(text, delay=0.03, color=Fore.RED):
    for ch in text:
        sys.stdout.write(color + ch + Style.RESET_ALL)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def banner_animasi():
    clear()
    frames = ["BARA CRACK", "BARA  CRACK", "B A R A   C R A C K", "BARA CRACK 🔥", "BARA CRACK"]
    for _ in range(3):
        for f in frames:
            sys.stdout.write(f"\r{Fore.RED}{Style.BRIGHT}  {f}  {Style.RESET_ALL}")
            sys.stdout.flush()
            time.sleep(0.15)
    print("\n")

def banner_static():
    print(f"""{Fore.RED}{Style.BRIGHT}
╔══════════════════════════════════════════╗
║            🔥  BARA CRACK  🔥            ║
║         {Fore.YELLOW}v1.0 - by CJ{Fore.RED}                 ║
╚══════════════════════════════════════════╝
{Style.RESET_ALL}""")

# ============ ENKRIPSI REAL-TIME (AES-256-CBC) ============

KEY = hashlib.sha256(b"BARA_CRACK_SECRET_CJ").digest()
IV  = b"16byte_iv_bara!!"

def encrypt(text):
    cipher = AES.new(KEY, AES.MODE_CBC, IV)
    ct = cipher.encrypt(pad(text.encode(), AES.block_size))
    return base64.b64encode(ct).decode()

def decrypt(enc):
    cipher = AES.new(KEY, AES.MODE_CBC, IV)
    pt = unpad(cipher.decrypt(base64.b64decode(enc)), AES.block_size)
    return pt.decode()

# ============ VERIFIKASI ============

def verifikasi():
    clear()
    banner_static()
    print(f"{Fore.CYAN}[*] Verifikasi Keamanan Aktif{Style.RESET_ALL}\n")

    token_input = input(f"{Fore.YELLOW}[?] Masukkan Token Verifikasi: {Style.RESET_ALL}").strip()
    if not token_input:
        print(f"{Fore.RED}[✗] Token kosong.{Style.RESET_ALL}")
        time.sleep(1.5)
        return False

    # Enkripsi real-time
    print(f"{Fore.CYAN}[*] Mengenkripsi token...{Style.RESET_ALL}")
    time.sleep(0.4)
    enc = encrypt(token_input)
    print(f"{Fore.GREEN}[✓] Encrypted : {enc[:40]}...{Style.RESET_ALL}")
    time.sleep(0.5)

    # Decrypt balik
    print(f"{Fore.CYAN}[*] Mendekripsi token...{Style.RESET_ALL}")
    time.sleep(0.4)
    dec = decrypt(enc)
    print(f"{Fore.GREEN}[✓] Decrypted : {dec}{Style.RESET_ALL}")
    time.sleep(0.4)

    # Cek hash verifikasi
    expected_hash = hashlib.sha256(b"CJ_BARA_AUTH").hexdigest()
    input_hash    = hashlib.sha256(dec.encode()).hexdigest()

    if input_hash == expected_hash or dec.lower() == "bara":
        print(f"\n{Fore.GREEN}[✓] VERIFIKASI BERHASIL{Style.RESET_ALL}")
        time.sleep(1)
        return True
    else:
        print(f"\n{Fore.RED}[✗] VERIFIKASI GAGAL{Style.RESET_ALL}")
        time.sleep(1.5)
        return False

# ============ CRACK ENGINE ============

def crack_website(url):
    clear()
    banner_static()
    print(f"{Fore.CYAN}[*] Target : {url}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}[*] Memulai crack...{Style.RESET_ALL}\n")

    hasil = {
        "target": url,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "findings": []
    }

    try:
        # Fase 1: Fetch
        print(f"{Fore.YELLOW}[1/5] Fetching target...{Style.RESET_ALL}")
        r = requests.get(url, timeout=10, headers={"User-Agent": "BaraCrack/1.0"})
        time.sleep(0.6)
        print(f"      → Status: {r.status_code}")
        print(f"      → Size  : {len(r.content)} bytes")
        hasil["findings"].append({"phase": "fetch", "status": r.status_code, "size": len(r.content)})

        # Fase 2: Header recon
        print(f"{Fore.YELLOW}[2/5] Header recon...{Style.RESET_ALL}")
        for k, v in list(r.headers.items())[:6]:
            print(f"      → {k}: {v}")
        hasil["findings"].append({"phase": "headers", "data": dict(r.headers)})
        time.sleep(0.5)

        # Fase 3: Hash signature
        print(f"{Fore.YELLOW}[3/5] Generating signature...{Style.RESET_ALL}")
        sig = hashlib.sha256(r.content).hexdigest()
        print(f"      → SHA256: {sig[:32]}...")
        hasil["findings"].append({"phase": "signature", "sha256": sig})
        time.sleep(0.5)

        # Fase 4: Endpoint probe
        print(f"{Fore.YELLOW}[4/5] Endpoint probing...{Style.RESET_ALL}")
        endpoints = ["/admin", "/login", "/api", "/.env", "/robots.txt"]
        for ep in endpoints:
            try:
                rr = requests.get(url.rstrip("/") + ep, timeout=5)
                print(f"      → {ep} [{rr.status_code}]")
                hasil["findings"].append({"endpoint": ep, "status": rr.status_code})
            except Exception:
                print(f"      → {ep} [TIMEOUT]")
            time.sleep(0.2)

        # Fase 5: Save
        print(f"\n{Fore.YELLOW}[5/5] Menyimpan hasil...{Style.RESET_ALL}")
        fname = f"crack_{int(time.time())}.json"
        fpath = os.path.join(OUTPUT_DIR, fname)
        with open(fpath, "w") as f:
            json.dump(hasil, f, indent=2)
        print(f"{Fore.GREEN}[✓] Tersimpan: {fpath}{Style.RESET_ALL}")

    except Exception as e:
        print(f"{Fore.RED}[✗] Error: {e}{Style.RESET_ALL}")
        time.sleep(1.5)

    input(f"\n{Fore.CYAN}[ENTER] Balik ke menu...{Style.RESET_ALL}")

# ============ MENU ============

def menu_crack():
    clear()
    banner_static()

    if not verifikasi():
        input(f"\n{Fore.CYAN}[ENTER] Balik...{Style.RESET_ALL}")
        return

    clear()
    banner_static()
    print(f"{Fore.GREEN}[✓] Akses Diberikan{Style.RESET_ALL}\n")

    url = input(f"{Fore.YELLOW}[?] Masukkan URL target: {Style.RESET_ALL}").strip()
    if not url.startswith("http"):
        url = "https://" + url

    crack_website(url)

def menu_coming_soon():
    clear()
    banner_static()
    print()
    typewriter("  C O M I N G   S O O N . . .", delay=0.08, color=Fore.MAGENTA)
    print()
    time.sleep(2)
    input(f"{Fore.CYAN}[ENTER] Balik...{Style.RESET_ALL}")

def main_menu():
    while True:
        clear()
        banner_static()
        print(f"""{Fore.WHITE}
  {Fore.RED}[1]{Fore.WHITE} Crack Website
  {Fore.RED}[2]{Fore.WHITE} Crack App {Fore.YELLOW}(Coming Soon){Fore.WHITE}
  {Fore.RED}[0]{Fore.WHITE} Keluar
""")
        pilih = input(f"{Fore.CYAN}┌─[BARA]─[~]\n└──╼ {Style.RESET_ALL}").strip()

        if pilih == "1":
            menu_crack()
        elif pilih == "2":
            menu_coming_soon()
        elif pilih == "0":
            print(f"\n{Fore.RED}[!] Keluar...{Style.RESET_ALL}")
            sys.exit(0)
        else:
            print(f"{Fore.RED}[✗] Pilihan salah.{Style.RESET_ALL}")
            time.sleep(1)

# ============ ENTRY ============

if __name__ == "__main__":
    try:
        banner_animasi()
        time.sleep(0.5)
        main_menu()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}[!] Dihentikan.{Style.RESET_ALL}")
        sys.exit(0)
