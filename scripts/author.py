#!/usr/bin/env python3
"""Unify JSON-LD author to the owner-confirmed byline (idempotent).
Author: "Spinora Wins Editorial Team" (Organization, links to About us).
Also adds the author to Article/WebPage-type schema blocks on methodology pages that lack it."""
import os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from apply_layout import iter_pages, ROOT
import site_config as C

AUTHOR = '"author": {"@type": "Organization", "name": "Spinora Wins Editorial Team", "url": "%s/about-us.html"}' % C.SITE
RE = re.compile(r'"author"\s*:\s*\{[^{}]*?"name"\s*:\s*"Spinora Wins[^"]*"[^{}]*\}')
ADD = {"how-we-rate.html", "es/como-evaluamos.html", "pt/como-avaliamos.html"}
ART = re.compile(r'("@type"\s*:\s*"Article"\s*,)')

n = 0
for rel in iter_pages():
    f = os.path.join(ROOT, rel)
    s = open(f, encoding="utf-8").read()
    ns = RE.sub(AUTHOR, s)
    if rel in ADD and '"author"' not in ns:
        ns = ART.sub(lambda m: m.group(1) + " " + AUTHOR + ",", ns, count=1)
    if ns != s:
        open(f, "w", encoding="utf-8").write(ns); n += 1
print("pages changed", n)
