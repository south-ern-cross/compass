#!/usr/bin/env python3
"""Regenerate sitemap.xml from the real, indexable pages.

Included: every HTML page whose canonical points to itself and that has no
robots noindex. Excluded: /go/ redirects, redirect stubs, canonicalized
duplicates, thin templated stubs.
lastmod: kept from the previous sitemap when present, otherwise the date of
the last git commit that touched the file on the base branch (real data,
never invented).
"""
import os, re, sys, subprocess
sys.path.insert(0, os.path.dirname(__file__))
from apply_layout import iter_pages, ROOT
import site_config as C

BASE_BRANCH = os.environ.get("SITEMAP_BASE_BRANCH", "origin/main")


def git_dates():
    out = subprocess.run(["git", "log", BASE_BRANCH, "--format=@%cs", "--name-only"], cwd=ROOT,
                         capture_output=True, text=True).stdout
    dates, cur = {}, None
    for line in out.splitlines():
        if line.startswith("@"):
            cur = line[1:]
        elif line.strip() and line not in dates:
            dates[line] = cur
    return dates


def main():
    old = {}
    sm = os.path.join(ROOT, "sitemap.xml")
    if os.path.exists(sm):
        for loc, lm in re.findall(r"<loc>(.*?)</loc>\s*<lastmod>(.*?)</lastmod>", open(sm).read()):
            old[loc] = lm
    dates = git_dates()
    urls = []
    for rel in iter_pages():
        s = open(os.path.join(ROOT, rel), encoding="utf-8").read(12000)
        if re.search(r'<meta name="robots" content="[^"]*noindex', s):
            continue
        m = re.search(r'<link rel="canonical" href="([^"]+)"', s)
        if not m:
            continue
        canon = m.group(1)
        self_urls = {C.SITE + "/" + rel}
        if rel.endswith("index.html"):
            self_urls.add(C.SITE + "/" + rel[: -len("index.html")])
        if canon not in self_urls:
            continue
        lm = old.get(canon) or dates.get(rel)
        urls.append((canon, lm))
    urls.sort(key=lambda u: (u[0].count("/"), u[0]))
    with open(sm, "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for loc, lm in urls:
            f.write(f"  <url><loc>{loc}</loc>" + (f"<lastmod>{lm}</lastmod>" if lm else "") + "</url>\n")
        f.write("</urlset>\n")
    print("sitemap urls:", len(urls))


if __name__ == "__main__":
    main()
