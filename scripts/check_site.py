#!/usr/bin/env python3
"""Site sanity checks: broken internal links, hreflang reciprocity,
sitemap vs indexable pages, single <h1>, rel on /go/ links.
Exit code 1 if any hard error is found."""
import os, re, sys
from urllib.parse import urlparse, unquote
sys.path.insert(0, os.path.dirname(__file__))
from apply_layout import iter_pages, ROOT, ALT_RE
import site_config as C

HREF = re.compile(r'<a\b[^>]*?href="([^"#?]*)[^"]*"', re.I)
CANON = re.compile(r'<link rel="canonical" href="([^"]+)"')

def exists(path):
    p = os.path.join(ROOT, unquote(path).lstrip("/"))
    return os.path.isfile(p) or os.path.isfile(os.path.join(p, "index.html"))

def main():
    err = {"broken": 0, "hreflang": 0, "h1": 0, "go_rel": 0, "sitemap": 0}
    pages = list(iter_pages()); alts = {}; indexable = set()
    for rel in pages:
        s = open(os.path.join(ROOT, rel), encoding="utf-8").read()
        base = "/" + os.path.dirname(rel)
        for h in HREF.findall(s):
            if not h or h.startswith(("http", "mailto:", "tel:", "javascript:", "data:")) or h.startswith("/go/"):
                continue
            path = h if h.startswith("/") else os.path.normpath(os.path.join(base, h))
            if not exists(path):
                err["broken"] += 1
        if s.count("<h1") != 1 and "http-equiv=\"refresh\"" not in s:
            err["h1"] += 1
        for a in re.findall(r'<a\b[^>]*href="/go/[^"]*"[^>]*>', s):
            r = re.search(r'rel="([^"]*)"', a)
            if not r or "sponsored" not in r.group(1) or "noopener" not in r.group(1):
                err["go_rel"] += 1
        alts[rel] = dict(ALT_RE.findall(s[:10000]))
        c = CANON.search(s)
        if c and 'content="noindex' not in s[:10000] and c.group(1).replace("/index.html", "").rstrip("/") == (C.SITE + "/" + rel).replace("/index.html", "").rstrip("/"):
            indexable.add(c.group(1))
    for rel, a in alts.items():
        me = C.SITE + "/" + rel
        for lang, u in a.items():
            r = u.replace(C.SITE + "/", "")
            if r in alts and alts[r] and me not in alts[r].values() and me.replace("/index.html", "/") not in alts[r].values():
                err["hreflang"] += 1
    sm = set(re.findall(r"<loc>([^<]+)</loc>", open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8").read()))
    norm = lambda u: u.replace("/index.html", "/")
    err["sitemap"] = len({norm(u) for u in sm} ^ {norm(u) for u in indexable})
    for k, v in err.items():
        print(f"{k:10} {v}")
    sys.exit(1 if err["broken"] or err["go_rel"] else 0)

if __name__ == "__main__":
    main()
