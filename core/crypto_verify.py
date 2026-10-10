import hashlib, base64, time, sys
from colorama import Fore, Style
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

KEY = hashlib.sha256(b"BARA_CRACK_V2_SECRET").digest()
IV  = b"BARA_IV_16BYTE!!"

def encrypt(t):
    c = AES.new(KEY, AES.MODE_CBC, IV)
    return base64.b64encode(c.encrypt(pad(t.encode(), 16))).decode()

def decrypt(e):
    c = AES.new(KEY, AES.MODE_CBC, IV)
    return unpad(c.decrypt(base64.b64decode(e)), 16).decode()

def live_verify():
    print(f"{Fore.CYAN}╭─[ VERIFIKASI LIVE ]──────────────────╮{Style.RESET_ALL}")
    token = input(f"{Fore.YELLOW}│ Token: {Style.RESET_ALL}").strip()
    if not token:
        return False

    # Encrypt real-time
    print(f"{Fore.CYAN}│ [*] Encrypting...{Style.RESET_ALL}", end="", flush=True)
    for _ in range(3):
        time.sleep(0.3); sys.stdout.write("."); sys.stdout.flush()
    enc = encrypt(token)
    print(f"\n{Fore.GREEN}│ [✓] Cipher: {enc[:44]}...{Style.RESET_ALL}")
    time.sleep(0.4)

    # Decrypt real-time
    print(f"{Fore.CYAN}│ [*] Decrypting...{Style.RESET_ALL}", end="", flush=True)
    for _ in range(3):
        time.sleep(0.3); sys.stdout.write("."); sys.stdout.flush()
    dec = decrypt(enc)
    print(f"\n{Fore.GREEN}│ [✓] Plain : {dec}{Style.RESET_ALL}")
    time.sleep(0.4)

    # Compare
    hash_ok = hashlib.sha256(dec.encode()).hexdigest() == hashlib.sha256(b"bara").hexdigest()
    hash_ok = hash_ok or dec.lower() == "bara"

    print(f"{Fore.CYAN}╰──────────────────────────────────────╯{Style.RESET_ALL}")
    if hash_ok:
        print(f"\n{Fore.GREEN}[✓] ACCESS GRANTED{Style.RESET_ALL}\n")
        time.sleep(1)
        return True
    print(f"\n{Fore.RED}[✗] ACCESS DENIED{Style.RESET_ALL}\n")
    time.sleep(1.5)
    return False
