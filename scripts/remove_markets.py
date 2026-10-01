#!/usr/bin/env python3
"""Retire markets the site no longer covers (owner decision, October 2026: Brazil, India).

* Every page listed in scripts/removed-pages.txt becomes a small noindex
  redirect stub to the language homepage (old inbound links keep working).
* On all other pages, links to those pages are removed: country cards and
  single-link list items are dropped, "A | B | C" and "A · B" link lists lose
  the entry, buttons point to the language top list, any other link is
  unwrapped (text kept). /go/ links are never touched.
Idempotent.
"""
import os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from apply_layout import iter_pages, ROOT, page_lang
import site_config as C

HERE = os.path.dirname(__file__)
REMOVED = [l.strip() for l in open(os.path.join(HERE, "removed-pages.txt")) if l.strip()]
RSET = set(REMOVED)
TOPLIST = {"en": "/top-10-crypto-casinos.html", "es": "/es/top-10-casinos-cripto.html", "pt": "/pt/top-10-cassinos-cripto.html"}
STUB_TXT = {
    "en": ("Page retired", "We no longer cover this market. This page has been retired.", "Go to the homepage"),
    "es": ("Página retirada", "Ya no cubrimos este mercado. Esta página se ha retirado.", "Ir a la portada"),
    "pt": ("Página removida", "Não cobrimos mais este mercado. Esta página foi removida.", "Ir para a página inicial"),
}

href_alt = "|".join(re.escape(r) for r in sorted(RSET, key=len, reverse=True))
H = r'href="(?:/|(?:\.\./)*)(?:' + href_alt + r')(?:[?#][^"]*)?"'
A = r'<a\b[^>]*?' + H + r'[^>]*>.*?</a>'
CARD = re.compile(r'[ \t]*<div class="card[^"]*">(?:(?!<div\b|</div>).)*?' + H + r'(?:(?!<div\b|</div>).)*?</div>\n?', re.S)
LI = re.compile(r'[ \t]*<li>\s*' + A + r'\s*</li>\n?', re.S)
SEP_AFTER = re.compile(r'' + A + r'\s*(?:\||·|&middot;)\s*', re.S)
SEP_BEFORE = re.compile(r'\s*(?:\||·|&middot;)\s*' + A, re.S)
COMMA = re.compile(r'' + A + r',\s*', re.S)
BTN = re.compile(r'(<a\b[^>]*?)' + H + r'([^>]*class="[^"]*btn[^"]*"[^>]*>)', re.S)
BTN2 = re.compile(r'(<a\b[^>]*?class="[^"]*btn[^"]*"[^>]*?)' + H, re.S)
UNWRAP = re.compile(r'<a\b[^>]*?' + H + r'[^>]*>(.*?)</a>', re.S)
JSONLD_ITEM = re.compile(r'"(?:https://spinorawins\.com/)(?:' + href_alt + r')"')


def patterns(H):
    A = r'<a\b[^>]*?' + H + r'[^>]*>.*?</a>'
    return dict(
        CARD=re.compile(r'[ \t]*<div class="card[^"]*">(?:(?!<div\b|</div>).)*?' + H + r'(?:(?!<div\b|</div>).)*?</div>\n?', re.S),
        LI=re.compile(r'[ \t]*<li>\s*' + A + r'\s*</li>\n?', re.S),
        SEP_AFTER=re.compile(A + r'\s*(?:\||·|&middot;)\s*', re.S),
        SEP_BEFORE=re.compile(r'\s*(?:\||·|&middot;)\s*' + A, re.S),
        COMMA=re.compile(A + r',\s*', re.S),
        BTN=re.compile(r'(<a\b[^>]*?)' + H + r'([^>]*class="[^"]*btn[^"]*"[^>]*>)', re.S),
        BTN2=re.compile(r'(<a\b[^>]*?class="[^"]*btn[^"]*"[^>]*?)' + H, re.S),
        UNWRAP=re.compile(r'<a\b[^>]*?' + H + r'[^>]*>(.*?)</a>', re.S),
    )


def rel_H(rel):
    d = os.path.dirname(rel) or "."
    rels = {os.path.relpath(r, d) for r in RSET}
    rels = [x for x in rels if not x.startswith("/")]
    return r'href="(?:' + "|".join(re.escape(x) for x in sorted(rels, key=len, reverse=True)) + r')(?:[?#][^"]*)?"'


def clean(s, lang, P=None):
    if P is not None:
        CARD, LI, SEP_AFTER, SEP_BEFORE, COMMA, BTN, BTN2, UNWRAP = (P[k] for k in ("CARD", "LI", "SEP_AFTER", "SEP_BEFORE", "COMMA", "BTN", "BTN2", "UNWRAP"))
    else:
        CARD, LI, SEP_AFTER, SEP_BEFORE, COMMA, BTN, BTN2, UNWRAP = (globals()[k] for k in ("CARD", "LI", "SEP_AFTER", "SEP_BEFORE", "COMMA", "BTN", "BTN2", "UNWRAP"))
    s = CARD.sub("", s)
    s = LI.sub("", s)
    s = BTN.sub(lambda m: m.group(1) + f'href="{TOPLIST[lang]}"' + m.group(2), s)
    s = BTN2.sub(lambda m: m.group(1) + f'href="{TOPLIST[lang]}"', s)
    s = SEP_AFTER.sub("", s)
    s = SEP_BEFORE.sub("", s)
    s = COMMA.sub("", s)
    s = UNWRAP.sub(lambda m: m.group(1), s)
    return s


def stub(rel):
    lang = page_lang(rel)
    t, p, a = STUB_TXT[lang]
    home = C.HOME[lang]
    return f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="noindex, follow">
<title>{t} | Spinora Wins</title>
<link rel="canonical" href="{C.SITE}{home}">
<meta http-equiv="refresh" content="0; url={home}">
</head>
<body>
<p>{p} <a href="{home}">{a}</a>.</p>
</body>
</html>
'''


def main():
    for rel in REMOVED:
        f = os.path.join(ROOT, rel)
        open(f, "w", encoding="utf-8").write(stub(rel))
    n = 0
    for rel in iter_pages():
        if rel in RSET:
            continue
        f = os.path.join(ROOT, rel)
        s = open(f, encoding="utf-8").read()
        ns = clean(s, page_lang(rel)) if re.search(H, s) else s
        if any(os.path.basename(r) in ns for r in RSET):
            rh = rel_H(rel)
            if re.search(rh, ns):
                ns = clean(ns, page_lang(rel), patterns(rh))
        if ns != s:
            open(f, "w", encoding="utf-8").write(ns); n += 1
    print("stubs", len(REMOVED), "pages cleaned", n)


if __name__ == "__main__":
    main()
