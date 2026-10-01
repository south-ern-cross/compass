#!/usr/bin/env python3
"""Move slot cards that were appended inside the intro .status-box back into
the #slot-grid catalogue grid (they rendered full-width above the grid), and
keep the search placeholder count equal to the number of cards. Idempotent."""
import os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from apply_layout import iter_pages, ROOT

CARD = r'<div class="card slot-card"[^>]*>.*?\n</div>\n?'
BOX = re.compile(r'(<div class="status-box">(?:(?!<div).)*?)((?:' + CARD + r')+)(</div>)', re.S)
GRID = '<div class="cards-grid" id="slot-grid">\n'

n = 0
for rel in iter_pages():
    f = os.path.join(ROOT, rel)
    s = open(f, encoding="utf-8").read()
    if GRID not in s:
        continue
    ns = s
    m = BOX.search(ns)
    if m:
        cards = m.group(2)
        ns = ns[:m.start()] + m.group(1) + m.group(3) + ns[m.end():]
        ns = ns.replace(GRID, GRID + cards.rstrip("\n") + "\n", 1)
    g = ns.find(GRID)
    total = len(re.findall(r'<div class="card slot-card"', ns[g:]))
    ns = re.sub(r'(placeholder="(?:Search|Buscar|Pesquisar) )\d+', lambda x: x.group(1) + str(total), ns, count=1)
    if ns != s:
        open(f, "w", encoding="utf-8").write(ns); n += 1
print("pages fixed", n)
