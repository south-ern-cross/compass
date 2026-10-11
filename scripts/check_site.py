#!/usr/bin/env python3
"""Site sanity checks: broken internal links, hreflang reciprocity,
sitemap vs indexable pages, single <h1>, rel on /go/ links, and JSON-LD
(valid JSON; page-level url / inLanguage / last breadcrumb consistent with
the page itself).

Exit code 1 if ANY category has errors. Use --soft to report only (exit 0).
Use --verbose to print up to 20 examples per category."""
import os, re, sys, json
from urllib.parse import unquote
sys.path.insert(0, os.path.dirname(__file__))
from apply_layout import iter_pages, ROOT, ALT_RE
import site_config as C

HREF = re.compile(r'<a\b[^>]*?href="([^"#?]*)[^"]*"', re.I)
CANON = re.compile(r'<link rel="canonical" href="([^"]+)"')
LD = re.compile(r'<script type="application/ld\+json">(.*?)</script>', re.S | re.I)
HTML_LANG = re.compile(r'<html\b[^>]*\blang="([^"]+)"', re.I)
# Node types whose "url" must be the page's own canonical URL.
PAGE_TYPES = {"Review", "WebPage", "Article", "BlogPosting", "NewsArticle",
              "FAQPage", "CollectionPage"}

def exists(path):
    p = os.path.join(ROOT, unquote(path).lstrip("/"))
    return os.path.isfile(p) or os.path.isfile(os.path.join(p, "index.html"))

def norm(u):
    return u.replace("/index.html", "/").rstrip("/")

def types(n):
    t = n.get("@type")
    return set(t) if isinstance(t, list) else {t}

def ld_nodes(obj):
    if isinstance(obj, list):
        for x in obj:
            yield from ld_nodes(x)
    elif isinstance(obj, dict):
        yield obj
        if "@graph" in obj:
            yield from ld_nodes(obj["@graph"])

def check_jsonld(s, canon, lang, alt_urls, report):
    for block in LD.findall(s):
        try:
            data = json.loads(block)
        except ValueError as e:
            report("jsonld", f"invalid JSON: {e}")
            continue
        for n in ld_nodes(data):
            ts = types(n)
            if ts & PAGE_TYPES:
                u = n.get("url")
                if isinstance(u, str) and canon and norm(u) != norm(canon):
                    report("jsonld", f"{'/'.join(sorted(t for t in ts if t))}.url {u} != canonical {canon}")
                il = n.get("inLanguage")
                if isinstance(il, str) and lang and il.lower().split("-")[0] != lang.lower().split("-")[0]:
                    report("jsonld", f"inLanguage {il} != <html lang> {lang}")
            if "BreadcrumbList" in ts and isinstance(n.get("itemListElement"), list) and n["itemListElement"]:
                last = n["itemListElement"][-1]
                it = last.get("item") if isinstance(last, dict) else None
                if isinstance(it, dict):
                    it = it.get("@id")
                # Only flag a last crumb that points to another language version of this page.
                if isinstance(it, str) and canon and norm(it) != norm(canon) and norm(it) in alt_urls:
                    report("jsonld", f"last breadcrumb {it} is another language version, expected {canon}")

def main():
    soft = "--soft" in sys.argv
    verbose = "--verbose" in sys.argv or "-v" in sys.argv
    err = {"broken": 0, "hreflang": 0, "h1": 0, "go_rel": 0, "sitemap": 0, "jsonld": 0}
    samples = {k: [] for k in err}
    cur = [""]

    def report(kind, msg=""):
        err[kind] += 1
        if len(samples[kind]) < 20:
            samples[kind].append(f"{cur[0]}: {msg}" if msg else cur[0])

    pages = list(iter_pages()); alts = {}; indexable = set()
    for rel in pages:
        cur[0] = rel
        s = open(os.path.join(ROOT, rel), encoding="utf-8").read()
        base = "/" + os.path.dirname(rel)
        for h in HREF.findall(s):
            if not h or h.startswith(("http", "mailto:", "tel:", "javascript:", "data:")) or h.startswith("/go/"):
                continue
            path = h if h.startswith("/") else os.path.normpath(os.path.join(base, h))
            if not exists(path):
                report("broken", h)
        redirect = 'http-equiv="refresh"' in s
        if s.count("<h1") != 1 and not redirect:
            report("h1", f"{s.count('<h1')} <h1>")
        for a in re.findall(r'<a\b[^>]*href="/go/[^"]*"[^>]*>', s):
            r = re.search(r'rel="([^"]*)"', a)
            if not r or "sponsored" not in r.group(1) or "noopener" not in r.group(1):
                report("go_rel", a[:120])
        alts[rel] = dict(ALT_RE.findall(s[:10000]))
        c = CANON.search(s)
        if c and 'content="noindex' not in s[:10000] and norm(c.group(1)) == norm(C.SITE + "/" + rel):
            indexable.add(c.group(1))
        if not redirect:
            m = HTML_LANG.search(s)
            check_jsonld(s, c.group(1) if c else None, m.group(1) if m else None,
                         {norm(u) for u in alts[rel].values()}, report)
    for rel, a in alts.items():
        cur[0] = rel
        me = C.SITE + "/" + rel
        for lang, u in a.items():
            r = u.replace(C.SITE + "/", "")
            if r in alts and alts[r] and me not in alts[r].values() and me.replace("/index.html", "/") not in alts[r].values():
                report("hreflang", f"{lang} -> {u} does not link back")
    cur[0] = "sitemap.xml"
    sm_path = os.path.join(ROOT, "sitemap.xml")
    sm = set(re.findall(r"<loc>([^<]+)</loc>", open(sm_path, encoding="utf-8").read())) if os.path.isfile(sm_path) else set()
    nz = lambda u: u.replace("/index.html", "/")
    sm_n = {nz(u) for u in sm}; ix_n = {nz(u) for u in indexable}
    for u in sorted(sm_n - ix_n):
        report("sitemap", f"in sitemap but not indexable: {u}")
    for u in sorted(ix_n - sm_n):
        report("sitemap", f"indexable but missing from sitemap: {u}")
    for k, v in err.items():
        print(f"{k:10} {v}")
        if verbose:
            for line in samples[k]:
                print(f"    {line}")
    failed = any(err.values())
    if failed and soft:
        print("errors found (--soft: exit 0)")
    sys.exit(1 if failed and not soft else 0)

if __name__ == "__main__":
    main()
