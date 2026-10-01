#!/usr/bin/env python3
"""Add intrinsic width/height to local <img> tags that lack them (prevents layout shift). Idempotent."""
import os, re, sys
from urllib.parse import unquote
from PIL import Image
sys.path.insert(0, os.path.dirname(__file__))
from apply_layout import iter_pages, ROOT

IMG = re.compile(r"<img\b[^>]*>", re.I)
cache = {}

def size(path):
    if path not in cache:
        try:
            with Image.open(path) as im:
                cache[path] = im.size
        except Exception:
            cache[path] = None
    return cache[path]

def fix(rel, tag):
    if re.search(r"\bwidth=", tag) and re.search(r"\bheight=", tag):
        return tag
    m = re.search(r'\bsrc="([^"]+)"', tag)
    if not m or m.group(1).startswith(("http", "data:", "//")):
        return tag
    src = unquote(m.group(1).split("?")[0])
    p = os.path.join(ROOT, src.lstrip("/")) if src.startswith("/") else os.path.normpath(os.path.join(ROOT, os.path.dirname(rel), src))
    wh = size(p)
    if not wh or re.search(r"\b(width|height)=", tag):
        return tag
    return tag[:4] + f' width="{wh[0]}" height="{wh[1]}"' + tag[4:]

n = 0
for rel in iter_pages():
    f = os.path.join(ROOT, rel)
    s = open(f, encoding="utf-8").read()
    ns = IMG.sub(lambda m: fix(rel, m.group(0)), s)
    if ns != s:
        open(f, "w", encoding="utf-8").write(ns); n += 1
print("pages changed", n)
