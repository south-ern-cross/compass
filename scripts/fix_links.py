#!/usr/bin/env python3
"""Repair relative internal links that point to non-existent files.

Typical cause: ES/PT pages copied from EN templates one folder deeper, so
"../../best-online-casinos-nigeria.html" resolves to /es/best-online-...
which does not exist. The fix re-resolves the link from the page's EN
location, then swaps in the localized counterpart (from hreflang) when it
exists. /go/ links are never modified.
"""
import os, re, sys, posixpath
from urllib.parse import urlsplit
sys.path.insert(0, os.path.dirname(__file__))
from apply_layout import iter_pages, ROOT, ALT_RE, page_lang
import site_config as C

ATTR_RE = re.compile(r'(<(?:a|img|link|script|source)\b[^>]*?\s(?:href|src)=")([^"]*)(")', re.I)


def exists(path):
    p = path.lstrip("/")
    return os.path.isfile(os.path.join(ROOT, p)) or os.path.isfile(os.path.join(ROOT, p, "index.html")) or (p == "" )


def build_map():
    m = {}
    for rel in iter_pages():
        s = open(os.path.join(ROOT, rel), encoding="utf-8").read(6000)
        alts = dict(ALT_RE.findall(s))
        if page_lang(rel) == "en" and alts:
            m["/" + rel] = {k: v.replace(C.SITE, "") for k, v in alts.items()}
    return m


def main():
    amap = build_map()
    fixed = unresolved = 0
    log = []
    for rel in iter_pages():
        p = os.path.join(ROOT, rel)
        s = open(p, encoding="utf-8").read()
        lang = page_lang(rel)
        base = "/" + rel
        en_base = "/" + rel[3:] if lang != "en" else base

        def sub(m):
            nonlocal fixed, unresolved
            href = m.group(2)
            if not href or "/go/" in href or href.startswith(("#", "http:", "https:", "mailto:", "tel:", "javascript:", "data:", "//")):
                return m.group(0)
            sp = urlsplit(href)
            if not sp.path:
                return m.group(0)
            tgt = posixpath.normpath(posixpath.join(posixpath.dirname(base), sp.path)) if not sp.path.startswith("/") else sp.path
            if exists(tgt):
                return m.group(0)
            cand = None
            en_t = posixpath.normpath(posixpath.join(posixpath.dirname(en_base), sp.path)) if not sp.path.startswith("/") else sp.path
            if en_t.startswith("/es/") or en_t.startswith("/pt/"):
                en_t = en_t[3:]
            if exists(en_t):
                cand = en_t
                if lang != "en":
                    key = en_t if en_t.endswith(".html") else en_t.rstrip("/") + "/index.html"
                    loc = amap.get(key, {}).get(lang)
                    if loc and exists(loc):
                        cand = loc
            else:
                # known moved pages
                alias = {"/payment-methods/crypto-latam-africa.html": "/payment-methods/crypto-casinos-latam-africa.html"}
                k = posixpath.normpath(posixpath.join(posixpath.dirname(base), sp.path))
                for a, b in alias.items():
                    if k.endswith(a.split("/")[-1]):
                        cand = b
            if cand is None:
                unresolved += 1
                log.append(f"UNRESOLVED {rel}: {href}")
                return m.group(0)
            fixed += 1
            new = cand + (("?" + sp.query) if sp.query else "") + (("#" + sp.fragment) if sp.fragment else "")
            return m.group(1) + new + m.group(3)

        n = ATTR_RE.sub(sub, s)
        if n != s:
            open(p, "w", encoding="utf-8").write(n)
    print("fixed", fixed, "unresolved", unresolved)
    for l in log[:50]:
        print(l)


if __name__ == "__main__":
    main()
