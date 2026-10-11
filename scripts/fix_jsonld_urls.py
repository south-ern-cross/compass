#!/usr/bin/env python3
"""Fix JSON-LD that points to another language version of the page.

Target bug: ES/PT reviews (es/resena-*.html, pt/avaliacao-*.html) whose
Review.url and last BreadcrumbList item are the EN page URL while
inLanguage is es / pt-BR.

Safety rules:
  * only page-level nodes (Review, WebPage, Article, ...) "url" and the LAST
    breadcrumb item are touched;
  * a value is replaced ONLY if it equals one of the page's own hreflang
    alternates (i.e. it is a translation of this page) and differs from the
    page canonical; it is replaced with the canonical;
  * pages without canonical or with meta refresh are skipped;
  * only the changed <script type="application/ld+json"> block is rewritten,
    and the result is re-parsed before writing.

Dry-run by default. Pass --write to modify files."""
import os, re, sys, json
sys.path.insert(0, os.path.dirname(__file__))
from apply_layout import iter_pages, ROOT, ALT_RE

CANON = re.compile(r'<link rel="canonical" href="([^"]+)"')
LD = re.compile(r'(<script type="application/ld\+json">)(.*?)(</script>)', re.S | re.I)
PAGE_TYPES = {"Review", "WebPage", "Article", "BlogPosting", "NewsArticle",
              "FAQPage", "CollectionPage"}

def types(n):
    t = n.get("@type")
    return set(t) if isinstance(t, list) else {t}

def top_nodes(obj):
    if isinstance(obj, list):
        return [x for x in obj if isinstance(x, dict)]
    if isinstance(obj, dict):
        g = obj.get("@graph")
        return [obj] + ([x for x in g if isinstance(x, dict)] if isinstance(g, list) else [])
    return []

def fix_data(data, canon, alt_urls, log):
    changed = False
    for n in top_nodes(data):
        ts = types(n)
        u = n.get("url")
        if ts & PAGE_TYPES and isinstance(u, str) and u != canon and u in alt_urls:
            log.append(f"url: {u} -> {canon}")
            n["url"] = canon; changed = True
        items = n.get("itemListElement")
        if "BreadcrumbList" in ts and isinstance(items, list) and items and isinstance(items[-1], dict):
            last = items[-1]; it = last.get("item")
            if isinstance(it, str) and it != canon and it in alt_urls:
                log.append(f"breadcrumb: {it} -> {canon}")
                last["item"] = canon; changed = True
            elif isinstance(it, dict) and it.get("@id") != canon and it.get("@id") in alt_urls:
                log.append(f"breadcrumb: {it['@id']} -> {canon}")
                it["@id"] = canon; changed = True
    return changed

def fix_page(s):
    if 'http-equiv="refresh"' in s:
        return s, []
    c = CANON.search(s)
    if not c:
        return s, []
    canon = c.group(1)
    alt_urls = {u for _, u in ALT_RE.findall(s[:12000])} - {canon}
    log = []

    def repl(m):
        try:
            data = json.loads(m.group(2))
        except ValueError:
            return m.group(0)  # leave invalid JSON for check_site.py to report
        if not fix_data(data, canon, alt_urls, log):
            return m.group(0)
        body = json.dumps(data, ensure_ascii=False, indent=2).replace("</", "<\\/")
        json.loads(body)
        return m.group(1) + "\n" + body + "\n" + m.group(3)

    return LD.sub(repl, s), log

def main():
    write = "--write" in sys.argv
    total = 0
    for rel in iter_pages():
        p = os.path.join(ROOT, rel)
        s = open(p, encoding="utf-8").read()
        new, log = fix_page(s)
        if log:
            total += 1
            print(rel)
            for line in log:
                print("   ", line)
            if write:
                open(p, "w", encoding="utf-8").write(new)
    print(f"{total} page(s) {'fixed' if write else 'would be fixed (dry-run, use --write)'}")

if __name__ == "__main__":
    main()
