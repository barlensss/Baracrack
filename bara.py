#!/usr/bin/env python3
import os, sys, time
from colorama import Fore, Style, init
init(autoreset=True)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core.crypto_verify import live_verify
from core.web_extract import extract_full
from core.lua_deob import deobfuscate
from core.output import tree, ROOT

def clear(): os.system("clear")

def banner():
    print(f"""{Fore.RED}{Style.BRIGHT}
╔═══════════════════════════════════════════╗
║         🔥  B A R A   C R A C K  👿       ║
║              {Fore.YELLOW}v2.0 — by CJ{Fore.RED}                ║
╚═══════════════════════════════════════════╝
{Style.RESET_ALL}""")

def animate_title():
    clear()
    frames = ["BARA CRACK", "B A R A  C R A C K", "BARA CRACK 🔥", "BARA CRACK"]
    for _ in range(2):
        for f in frames:
            sys.stdout.write(f"\r{Fore.RED}{Style.BRIGHT}   {f}{Style.RESET_ALL}")
            sys.stdout.flush(); time.sleep(0.12)
    print("\n")

def menu():
    while True:
        clear(); banner()
        print(f"""{Fore.WHITE}
  {Fore.RED}[1]{Fore.WHITE} Full Website Extract
  {Fore.RED}[2]{Fore.WHITE} Lua Deobfuscate (Luraph / MoonSec / IronBrew)
  {Fore.RED}[3]{Fore.WHITE} Crack App {Fore.YELLOW}(Coming Soon){Fore.WHITE}
  {Fore.RED}[4]{Fore.WHITE} Lihat Hasil Tersimpan
  {Fore.RED}[0]{Fore.WHITE} Keluar
""")
        p = input(f"{Fore.CYAN}[BARA]─[~]╼ {Style.RESET_ALL}").strip()

        if p == "1":
            if not live_verify(): continue
            url = input(f"{Fore.YELLOW}URL target: {Style.RESET_ALL}").strip()
            if not url.startswith("http"): url = "https://" + url
            extract_full(url)
            input(f"\n{Fore.CYAN}[ENTER] Balik...{Style.RESET_ALL}")
        elif p == "2":
            if not live_verify(): continue
            path = input(f"{Fore.YELLOW}Path file .lua: {Style.RESET_ALL}").strip()
            if not os.path.isfile(path):
                print(f"{Fore.RED}[✗] File tidak ada.{Style.RESET_ALL}"); time.sleep(1); continue
            out = os.path.join(ROOT, "lua_deob")
            deobfuscate(path, out)
            input(f"\n{Fore.CYAN}[ENTER] Balik...{Style.RESET_ALL}")
        elif p == "3":
            clear(); banner()
            for ch in "  C O M I N G   S O O N . . .":
                sys.stdout.write(f"{Fore.MAGENTA}{ch}"); sys.stdout.flush(); time.sleep(0.06)
            print()
            time.sleep(1.5)
            input(f"{Fore.CYAN}[ENTER] Balik...{Style.RESET_ALL}")
        elif p == "4":
            clear(); banner()
            print(f"{Fore.CYAN}{ROOT}{Style.RESET_ALL}")
            tree(ROOT)
            input(f"\n{Fore.CYAN}[ENTER] Balik...{Style.RESET_ALL}")
        elif p == "0":
            print(f"\n{Fore.RED}[!] Keluar.{Style.RESET_ALL}"); sys.exit(0)

if __name__ == "__main__":
    try:
        animate_title()
        menu()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}[!] Stop.{Style.RESET_ALL}"); sys.exit(0)
