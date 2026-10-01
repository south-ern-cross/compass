#!/usr/bin/env python3
"""Drop retired markets (Brazil, India) from "our markets" enumerations in
page copy, e.g. "Nigeria, Brazil, Mexico and India" -> "Nigeria and Mexico".
Lists that quote operator terms (they also name Spain, the UK, ...) are left
as they are. Core pages only; idempotent."""
import os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from apply_layout import iter_pages, ROOT

RETIRED = {"Brazil", "Brasil", "India", "Índia"}
NAMES = ["South Africa", "Sudáfrica", "África do Sul", "Nigeria", "Nigéria", "Kenya", "Kenia", "Quênia",
         "Mexico", "México", "Colombia", "Colômbia", "Brazil", "Brasil", "India", "Índia"]
ART = r"(?:(?:da|do|na|no|en|em) )?"
ITEM = ART + "(?:" + "|".join(re.escape(n) for n in NAMES) + r")\b"
CONJ = r"(?:,? (?:and|or|y|e|o|ou) | (?:&amp;|&) )"
LIST = re.compile(ITEM + r"(?:(?:, |" + CONJ + ")" + ITEM + ")+")
SKIP = re.compile(r"Spain|España|Espanha|United Kingdom|Reino Unido|\bSPA\b|licen[cs]e section|secci[oó]n de licencia")
SPLIT = re.compile(r"(, |" + CONJ + ")")


def name_of(item):
    return re.sub(r"^(?:da|do|na|no|en|em) ", "", item)


def fix_list(m, s):
    txt = m.group(0)
    if not any(r in txt for r in RETIRED):
        return txt
    ctx = s[max(0, m.start() - 200): m.end() + 200]
    if SKIP.search(ctx):
        return txt
    parts = SPLIT.split(txt)
    items, seps = parts[0::2], parts[1::2]
    keep = [i for i in items if name_of(i) not in RETIRED]
    if not keep or len(keep) == len(items):
        return txt
    conj = seps[-1] if seps else " and "
    if conj.startswith(","):
        conj = conj[1:]
    if conj.strip() == "":
        conj = ", "
    if len(keep) == 1:
        # "en Brasil y Nigeria" -> "en Nigeria": carry over a leading preposition
        m0 = re.match(r"(en|em) ", items[0])
        if m0 and not keep[0].startswith(m0.group(0)):
            return m0.group(0) + keep[0]
        return keep[0]
    return ", ".join(keep[:-1]) + conj + keep[-1]


def main():
    n = 0
    for rel in iter_pages():
        if "/slots/" in "/" + rel:
            continue
        f = os.path.join(ROOT, rel)
        s = open(f, encoding="utf-8").read()
        if 'content="0; url=' in s[:2000]:
            continue
        ns = LIST.sub(lambda m: fix_list(m, s), s)
        if ns != s:
            open(f, "w", encoding="utf-8").write(ns); n += 1
    print("pages changed", n)


if __name__ == "__main__":
    main()
