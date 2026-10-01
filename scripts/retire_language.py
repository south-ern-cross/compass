#!/usr/bin/env python3
"""Retire a whole language version (owner decision, October 2026: Portuguese).

* Every page under /pt/ becomes a noindex redirect stub to its English
  counterpart (from hreflang="en"), or to the English homepage.
* On the remaining pages, hreflang="pt" alternates, og:locale:alternate pt_BR
  and any links into /pt/ are removed (link text kept).
Old pages remain in git history and can be restored. Idempotent.
Usage: python3 scripts/retire_language.py pt
"""
import os, re, sys, html
sys.path.insert(0, os.path.dirname(__file__))
from apply_layout import iter_pages, ROOT, ALT_RE
import site_config as C

LANG = sys.argv[1] if len(sys.argv) > 1 else "pt"
TXT = {"pt": ("Versão em português descontinuada", "A versão em português do site foi descontinuada.", "Ir para a versão em inglês")}
REFRESH = re.compile(r'<meta http-equiv="refresh" content="0; ?url=([^"]+)"')


def target(rel, s):
    alts = dict(ALT_RE.findall(s[:12000]))
    en = alts.get("en")
    if en and not REFRESH.search(s[:3000]):
        r = en.replace(C.SITE, "")
        if os.path.isfile(os.path.join(ROOT, r.lstrip("/"))) or r == "/":
            return r
    return "/"


def stub(to):
    t, p, a = TXT[LANG]
    return f'''<!DOCTYPE html>
<html lang="{LANG}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="noindex, follow">
<title>{t} | Spinora Wins</title>
<link rel="canonical" href="{C.SITE}{to}">
<meta http-equiv="refresh" content="0; url={to}">
</head>
<body>
<p>{p} <a href="{to}">{a}</a>.</p>
</body>
</html>
'''


ALT_LINE = re.compile(r'[ \t]*<link rel="alternate" hreflang="' + LANG + r'(?:-[A-Za-z]+)?" href="[^"]*"\s*/?>\n?')
OG_ALT = re.compile(r'[ \t]*<meta property="og:locale:alternate" content="' + LANG + r'_[A-Z]+"\s*/?>\n?')
LINK = re.compile(r'<a\b[^>]*href="(?:https://spinorawins\.com)?/' + LANG + r'(?:/[^"]*)?"[^>]*>(.*?)</a>', re.S)


def main():
    stubs = n = 0
    for rel in list(iter_pages()):
        f = os.path.join(ROOT, rel)
        s = open(f, encoding="utf-8").read()
        if rel.startswith(LANG + "/"):
            ns = stub(target(rel, s))
            if ns != s and not (REFRESH.search(s[:3000]) and 'lang="%s"' % LANG in s[:200] and TXT[LANG][1] in s):
                open(f, "w", encoding="utf-8").write(ns); stubs += 1
            continue
        ns = OG_ALT.sub("", ALT_LINE.sub("", s))
        ns = LINK.sub(lambda m: m.group(1), ns)
        if ns != s:
            open(f, "w", encoding="utf-8").write(ns); n += 1
    print("stubs", stubs, "pages cleaned", n)


if __name__ == "__main__":
    main()
