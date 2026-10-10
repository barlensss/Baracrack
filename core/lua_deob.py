import re, os, time, subprocess, json
from colorama import Fore, Style

def detect_obf(code):
    sigs = {
        "Luraph": r"Luraph|luraph",
        "Luraph v14": r"return\(function\(local [A-Za-z_, ]+\)",
        "MoonSec": r"MoonSec|moonSec",
        "IronBrew": r"IronBrew|ironbrew",
        "Prometheus": r"Prometheus",
        "loadstring": r"loadstring\(",
        "string.char": r"string\.char\(",
    }
    return [k for k, p in sigs.items() if re.search(p, code, re.I)]

def extract_strings(code):
    """Tarik semua string literal dari file Lua."""
    strings = set()
    strings |= set(re.findall(r'"((?:[^"\\]|\\.){3,})"', code))
    strings |= set(re.findall(r"'((?:[^'\\]|\\.){3,})'", code))
    strings |= set(re.findall(r'\[\[(.{3,}?)\]\]', code, re.S))
    return sorted(strings)

def beautify(code):
    """Rapihin indentasi Lua sederhana."""
    out, indent = [], 0
    for line in code.splitlines():
        s = line.strip()
        if not s: continue
        if re.match(r'^(end|until|else|elseif|\})', s): indent = max(0, indent - 1)
        out.append("  " * indent + s)
        if re.search(r'\b(function|if|for|while|do|repeat|then)\b.*(?!end)$', s) or s.endswith("{"):
            indent += 1
    return "\n".join(out)

def rename_locals(code):
    """Rename local var obfuscated jadi v1, v2, ..."""
    counter = {}
    def repl(m):
        name = m.group(1)
        if len(name) <= 2:  # cuma rename yg pendek (obfuscated)
            if name not in counter:
                counter[name] = f"v{len(counter)+1}"
            return f"local {counter[name]}"
        return m.group(0)
    return re.sub(r'local ([A-Za-z_]\w*)', repl, code)

def deobfuscate(input_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    raw = open(input_path, encoding="utf-8", errors="ignore").read()

    name = os.path.basename(input_path)
    base = os.path.splitext(name)[0]

    print(f"{Fore.CYAN}[LUA] Menganalisis {name}...{Style.RESET_ALL}")
    time.sleep(0.3)

    # 1. Deteksi obfuscator
    det = detect_obf(raw)
    print(f"      → Terdeteksi: {', '.join(det) if det else 'Tidak dikenal'}")

    # 2. Extract strings
    strs = extract_strings(raw)
    str_file = os.path.join(output_dir, f"{base}.strings.txt")
    open(str_file, "w", encoding="utf-8").write("\n".join(strs))
    print(f"      → {len(strs)} string diekstrak: {str_file}")

    # 3. Beautify
    try:
        pretty = beautify(raw)
        pretty_file = os.path.join(output_dir, f"{base}.pretty.lua")
        open(pretty_file, "w", encoding="utf-8").write(pretty)
        print(f"      → Pretty: {pretty_file}")
    except Exception as e:
        print(f"      ✗ Beautify gagal: {e}")

    # 4. Rename locals
    try:
        renamed = rename_locals(raw)
        ren_file = os.path.join(output_dir, f"{base}.renamed.lua")
        open(ren_file, "w", encoding="utf-8").write(renamed)
        print(f"      → Renamed: {ren_file}")
    except Exception as e:
        print(f"      ✗ Rename gagal: {e}")

    # 5. Report
    report = {
        "file": name,
        "size": len(raw),
        "detected": det,
        "strings_found": len(strs),
        "outputs": [str_file, pretty_file, ren_file]
    }
    rpt = os.path.join(output_dir, f"{base}.report.json")
    open(rpt, "w").write(json.dumps(report, indent=2))
    print(f"{Fore.GREEN}      [✓] Report: {rpt}{Style.RESET_ALL}")
    return report
