#!/usr/bin/env python3
"""Site sanity checks: broken internal links, hreflang reciprocity,
sitemap vs indexable pages, single <h1>, rel on /go/ links, and JSON-LD
(valid JSON; page-level url / inLanguage / last breadcrumb consistent with
the page itself).

JSON-LD url rules (to avoid false positives):
  * only top-level nodes (top object / @graph members) are checked; nested
    objects such as itemReviewed, author, publisher are ignored;
  * a page-level "url" is checked only if it points to this site
    (spinorawins.com, with or without www, http or https, or a relative
    path). External URLs (operator site etc.) are allowed;
  * comparison ignores scheme, www, #fragment, a trailing slash and a
    trailing index.html.

Exit code 1 if ANY category has errors. Use --soft to report only (exit 0).
Use --verbose to print up to 20 examples per category."""
import os, re, sys, json
from urllib.parse import unquote, urlsplit, urljoin
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

def _host(h):
    h = (h or "").lower().rstrip(".")
    return h[4:] if h.startswith("www.") else h

SITE_HOST = _host(urlsplit(C.SITE).hostname)

def exists(path):
    p = os.path.join(ROOT, unquote(path).lstrip("/"))
    return os.path.isfile(p) or os.path.isfile(os.path.join(p, "index.html"))

def norm(u):
    return u.replace("/index.html", "/").rstrip("/")

def url_key(u):
    """Comparable key: (host without www, path without index.html / trailing
    slash, query). Scheme and #fragment are ignored. Relative URLs are
    resolved against the site root."""
    u = u.strip()
    if not urlsplit(u).netloc:
        u = urljoin(C.SITE + "/", u)
    p = urlsplit(u)
    path = unquote(p.path or "/")
    if path.endswith("/index.html"):
        path = path[:-len("index.html")]
    path = path.rstrip("/") or "/"
    return (_host(p.hostname), path, p.query)

def is_internal(u):
    p = urlsplit(u.strip())
    if p.scheme and p.scheme.lower() not in ("http", "https"):
        return False
    if not p.netloc:
        return u.strip().startswith("/")
    return _host(p.hostname) == SITE_HOST

def types(n):
    t = n.get("@type")
    return set(t) if isinstance(t, list) else {t}

def ld_nodes(obj):
    """Top-level nodes only: the object itself (or list members) and @graph
    members. Nested objects (itemReviewed, author, ...) are not yielded."""
    if isinstance(obj, list):
        for x in obj:
            yield from ld_nodes(x)
    elif isinstance(obj, dict):
        yield obj
        if "@graph" in obj:
            yield from ld_nodes(obj["@graph"])

def check_jsonld(s, canon, lang, alt_urls, report, self_url=None):
    """alt_urls: set of url_key() of this page's hreflang alternates."""
    own = set()
    if canon:
        own.add(url_key(canon))
    if self_url:
        own.add(url_key(self_url))
    alt_other = alt_urls - own
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
                # External URLs are allowed; only internal ones must be this page.
                if isinstance(u, str) and own and is_internal(u) and url_key(u) not in own:
                    hint = " (another language version)" if url_key(u) in alt_other else ""
                    report("jsonld", f"{'/'.join(sorted(t for t in ts if t))}.url {u} != canonical {canon}{hint}")
                il = n.get("inLanguage")
                if isinstance(il, str) and lang and il.lower().split("-")[0] != lang.lower().split("-")[0]:
                    report("jsonld", f"inLanguage {il} != <html lang> {lang}")
            if "BreadcrumbList" in ts and isinstance(n.get("itemListElement"), list) and n["itemListElement"]:
                last = n["itemListElement"][-1]
                it = last.get("item") if isinstance(last, dict) else None
                if isinstance(it, dict):
                    it = it.get("@id")
                # Only flag a last crumb that points to another language version of this page.
                if isinstance(it, str) and own and is_internal(it) and url_key(it) in alt_other:
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
                         {url_key(u) for u in alts[rel].values()}, report,
                         self_url=C.SITE + "/" + rel.replace(os.sep, "/"))
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
