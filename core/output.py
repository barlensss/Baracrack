import os

ROOT = "/storage/emulated/0/barayk/"

def ensure(*paths):
    for p in paths:
        os.makedirs(p, exist_ok=True)

def tree(path, prefix="", maxdepth=3, depth=0):
    if depth > maxdepth: return
    try: items = sorted(os.listdir(path))
    except: return
    for i, it in enumerate(items):
        full = os.path.join(path, it)
        last = i == len(items) - 1
        print(f"{prefix}{'└── ' if last else '├── '}{it}")
        if os.path.isdir(full):
            tree(full, prefix + ("    " if last else "│   "), maxdepth, depth + 1)
