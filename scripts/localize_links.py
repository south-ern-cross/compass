#!/usr/bin/env python3
"""ES/PT pages: point internal links at the same-language version.

If an ES/PT page links to an EN page that has an ES/PT counterpart
(declared in the EN page's hreflang), the link is switched to that
counterpart. Header/footer are skipped (rendered by apply_layout.py).
/go/ links are never modified.
"""
import os, re, sys, posixpath
from urllib.parse import urlsplit
sys.path.insert(0, os.path.dirname(__file__))
from apply_layout import iter_pages, ROOT, page_lang
from fix_links import build_map

A_RE = re.compile(r'(<a\b[^>]*?\shref=")([^"]*)(")')


def main():
    amap = build_map()
    n = 0
    for rel in iter_pages():
        lang = page_lang(rel)
        if lang == "en":
            continue
        p = os.path.join(ROOT, rel)
        s = open(p, encoding="utf-8").read()
        h = s.find("</header>")
        f = s.rfind('<footer class="site-footer">')
        if h < 0:
            h = 0
        if f < 0:
            f = len(s)
        body = s[h:f]
        base = "/" + rel

        def sub(m):
            nonlocal n
            href = m.group(2)
            if "/go/" in href or href.startswith(("#", "mailto:", "tel:", "javascript:")):
                return m.group(0)
            sp = urlsplit(href)
            if sp.scheme and sp.netloc not in ("spinorawins.com", "www.spinorawins.com"):
                return m.group(0)
            if not sp.path:
                return m.group(0)
            t = sp.path if sp.path.startswith("/") else posixpath.normpath(posixpath.join(posixpath.dirname(base), sp.path))
            if t.startswith(("/es/", "/pt/")) or t in ("/es", "/pt"):
                return m.group(0)
            key = t if t.endswith(".html") else t.rstrip("/") + "/index.html"
            loc = amap.get(key, {}).get(lang)
            if not loc or not os.path.isfile(os.path.join(ROOT, (loc.lstrip("/") or "index.html") if not loc.endswith("/") else loc.lstrip("/") + "index.html")):
                return m.group(0)
            n += 1
            return m.group(1) + loc + (("#" + sp.fragment) if sp.fragment else "") + m.group(3)

        nb = A_RE.sub(sub, body)
        if nb != body:
            open(p, "w", encoding="utf-8").write(s[:h] + nb + s[f:])
    print("localized", n, "links")


if __name__ == "__main__":
    main()
