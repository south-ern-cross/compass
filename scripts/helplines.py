#!/usr/bin/env python3
"""Render the per-market helpline table (site_config.HELPLINES) into the
responsible-gambling pages. Idempotent (marker-wrapped)."""
import os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
import site_config as C
from apply_layout import ROOT

PAGES = {"en": "responsible-gambling/index.html", "es": "es/juego-responsable.html", "pt": "pt/jogo-responsavel.html"}
MARK = re.compile(r"<!-- helplines:start -->.*?<!-- helplines:end -->", re.S)
OLD = re.compile(r'<div class="table-wrap"><table>\s*<tr><th>(?:Country|País)</th><th>(?:Resource|Recurso)</th></tr>.*?</table>\s*</div>', re.S)

for lang, rel in PAGES.items():
    f = os.path.join(ROOT, rel)
    s = open(f, encoding="utf-8").read()
    t = C.helplines_table(lang)
    ns = MARK.sub(lambda m: t, s) if MARK.search(s) else OLD.sub(lambda m: t, s, count=1)
    if ns != s:
        open(f, "w", encoding="utf-8").write(ns)
        print("updated", rel)
