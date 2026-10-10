import os, re, time, json, hashlib
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from colorama import Fore, Style
from playwright.sync_api import sync_playwright

def slug(url):
    return urlparse(url).netloc.replace(":", "_")

def safe_name(url):
    return re.sub(r'[^a-zA-Z0-9._-]', '_', url)[:120]

def extract_full(url, out_root="/storage/emulated/0/barayk/"):
    domain = slug(url)
    base   = os.path.join(out_root, domain)
    dirs   = {k: os.path.join(base, k) for k in
              ["html", "js", "css", "img", "api", "routes", "meta"]}
    for d in dirs.values(): os.makedirs(d, exist_ok=True)

    print(f"{Fore.CYAN}[1/7] Fetch halaman utama...{Style.RESET_ALL}")
    r = requests.get(url, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
    html_path = os.path.join(dirs["html"], "index.html")
    with open(html_path, "w", encoding="utf-8") as f: f.write(r.text)
    print(f"      → {html_path}")

    soup = BeautifulSoup(r.text, "lxml")

    # CSS
    print(f"{Fore.CYAN}[2/7] Ambil CSS...{Style.RESET_ALL}")
    css_list = [urljoin(url, l["href"]) for l in soup.find_all("link", rel="stylesheet") if l.get("href")]
    for u in css_list:
        try:
            c = requests.get(u, timeout=10).text
            fn = os.path.join(dirs["css"], safe_name(u.split("/")[-1] or "style.css"))
            open(fn, "w", encoding="utf-8").write(c)
            print(f"      → {fn}")
        except Exception as e: print(f"      ✗ {u}: {e}")

    # JS
    print(f"{Fore.CYAN}[3/7] Ambil JavaScript...{Style.RESET_ALL}")
    js_list = [urljoin(url, s["src"]) for s in soup.find_all("script", src=True)]
    for u in js_list:
        try:
            c = requests.get(u, timeout=10).text
            fn = os.path.join(dirs["js"], safe_name(u.split("/")[-1] or "app.js"))
            open(fn, "w", encoding="utf-8").write(c)
            print(f"      → {fn}")
        except Exception as e: print(f"      ✗ {u}: {e}")

    # IMG
    print(f"{Fore.CYAN}[4/7] Ambil gambar...{Style.RESET_ALL}")
    img_list = [urljoin(url, i["src"]) for i in soup.find_all("img", src=True)]
    for u in img_list[:30]:
        try:
            c = requests.get(u, timeout=10).content
            fn = os.path.join(dirs["img"], safe_name(u.split("/")[-1] or "img.png"))
            open(fn, "wb").write(c)
            print(f"      → {fn}")
        except Exception: pass

    # Extract endpoint dari JS bundle
    print(f"{Fore.CYAN}[5/7] Extract endpoint dari JS...{Style.RESET_ALL}")
    endpoints = set()
    routes    = set()
    for jsf in os.listdir(dirs["js"]):
        try:
            code = open(os.path.join(dirs["js"], jsf), encoding="utf-8", errors="ignore").read()
            endpoints |= set(re.findall(r'["\'](/api/[^"\']+)["\']', code))
            endpoints |= set(re.findall(r'https?://[a-z0-9.-]+\.(?:supabase|firebase|railway|render|vercel)\.[a-z]+[^"\']*', code, re.I))
            routes    |= set(re.findall(r'["\'](/[a-zA-Z][a-zA-Z0-9/_-]{2,})["\']', code))
        except: pass

    open(os.path.join(dirs["api"], "endpoints.json"), "w").write(json.dumps(sorted(endpoints), indent=2))
    open(os.path.join(dirs["routes"], "routes.json"), "w").write(json.dumps(sorted(routes), indent=2))
    print(f"      → {len(endpoints)} endpoints, {len(routes)} routes")

    # SPA screenshot + network capture
    print(f"{Fore.CYAN}[6/7] Buka pakai browser (capture XHR)...{Style.RESET_ALL}")
    net_log = []
    try:
        with sync_playwright() as p:
            b = p.chromium.launch(headless=True)
            pg = b.new_page()
            pg.on("response", lambda resp: net_log.append({
                "url": resp.url, "status": resp.status,
                "method": resp.request.method,
                "type": resp.request.resource_type
            }))
            pg.goto(url, wait_until="networkidle", timeout=30000)
            pg.screenshot(path=os.path.join(dirs["meta"], "screenshot.png"), full_page=True)
            pg.content()  # trigger render
            b.close()
        open(os.path.join(dirs["meta"], "network.json"), "w").write(json.dumps(net_log, indent=2))
        print(f"      → screenshot + {len(net_log)} request tercatat")
    except Exception as e:
        print(f"      ✗ Playwright gagal: {e}")

    # Metadata + hash
    print(f"{Fore.CYAN}[7/7] Simpan metadata...{Style.RESET_ALL}")
    meta = {
        "url": url,
        "domain": domain,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "status": r.status_code,
        "html_sha256": hashlib.sha256(r.content).hexdigest(),
        "files": {
            "html": len(os.listdir(dirs["html"])),
            "js":   len(os.listdir(dirs["js"])),
            "css":  len(os.listdir(dirs["css"])),
            "img":  len(os.listdir(dirs["img"])),
        },
        "endpoints": len(endpoints),
        "routes": len(routes)
    }
    open(os.path.join(dirs["meta"], "info.json"), "w").write(json.dumps(meta, indent=2))
    print(f"\n{Fore.GREEN}[✓] Selesai. Semua tersimpan di: {base}{Style.RESET_ALL}")
    return base
