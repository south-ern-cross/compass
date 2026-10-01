#!/usr/bin/env python3
"""Casino cards: every toplist card shows the operator's own logo artwork,
large enough to recognise the brand (owner request, October 2026).

* .sw-card (article toplists): one <img class="sw-logo"> per card, from BRANDS.
* .sq-card (homepage sidebar): banner image from BRANDS.
* .article-toplist (sticky sidebar on reviews): logo thumbnail in every row.
Only <img> elements change; /go/ hrefs and anchor attributes stay as they are.
Idempotent."""
import os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from apply_layout import iter_pages, ROOT

L = "/assets/images/logos/"
BRANDS = {
    "bitstarz": (L + "bitstarz-logo.png", "BitStarz"), "cashy": (L + "cashy-logo.png", "Cashy"),
    "cloudbet": (L + "cloudbet-logo.png", "Cloudbet"), "cooked": (L + "cooked-logo.png", "Cooked"),
    "n1-casino": (L + "n1-logo.png", "N1 Casino"), "planbet": (L + "planbet-logo.png", "Planbet"),
    "rollbit": (L + "rollbit-logo.png", "Rollbit"), "vave": (L + "vave-logo.png", "Vave"),
    "duelbits": ("/assets/images/placeholder-duelbits.svg", "Duelbits"),
    "22bet": ("/assets/images/placeholder-22bet.svg", "22Bet"),
    "bc-game": ("/assets/images/placeholder-bc-game.svg", "BC.Game"),
    "trustdice": ("/assets/images/placeholder-trustdice.svg", "TrustDice"),
    "stake": ("/assets/images/brands/stake.svg", "Stake"),
    "betpanda": ("/assets/images/brands/betpanda.svg", "Betpanda"),
    "coincasino": ("/assets/images/brands/coincasino.svg", "CoinCasino"),
}


def img(cls, slug, eager=False):
    src, name = BRANDS[slug]
    load = 'fetchpriority="high" loading="eager"' if eager else 'loading="lazy"'
    return f'<img class="{cls}" src="{src}" alt="{name} logo" width="1200" height="696" {load} decoding="async">'


SW = re.compile(r'(<div class="sw-card[^"]*" data-casino="([^"]+)">\s*<div class="sw-top-row">)(.*?)(</div>)', re.S)
SW_IMG = re.compile(r'\s*<img\b[^>]*class="sw-logo"[^>]*>')
SQ = re.compile(r'(<div class="sq-card" data-casino="([^"]+)">.*?<a class="sq-banner"[^>]*>)<img\b[^>]*>', re.S)
TL = re.compile(r'(<a href="/go/([^/"]+)/"[^>]*>)(<span class="toplist-num">[^<]*</span>)(?:<img class="toplist-logo"[^>]*>)?')


def fix(s):
    n = [0]

    def sw(m):
        slug = m.group(2)
        if slug not in BRANDS:
            return m.group(0)
        body = SW_IMG.sub("", m.group(3))
        body = re.sub(r'(<span class="sw-rank">[^<]*</span>)', lambda r: r.group(1) + "\n        " + img("sw-logo", slug), body, count=1)
        return m.group(1) + body + m.group(4)

    s = SW.sub(sw, s)

    def sq(m):
        n[0] += 1
        return m.group(1) + img("sq-logo", m.group(2), eager=n[0] <= 2) if m.group(2) in BRANDS else m.group(0)

    s = SQ.sub(sq, s)
    if 'class="article-toplist-list"' in s:
        def tl(m):
            slug = m.group(2)
            if slug not in BRANDS:
                return m.group(0)
            return m.group(1) + m.group(3) + f'<img class="toplist-logo" src="{BRANDS[slug][0]}" alt="" width="1200" height="696" loading="lazy" decoding="async">'
        s = TL.sub(tl, s)
    return s


def main():
    c = 0
    for rel in iter_pages():
        f = os.path.join(ROOT, rel)
        s = open(f, encoding="utf-8").read()
        if "sw-card" not in s and "sq-card" not in s and "article-toplist-list" not in s:
            continue
        ns = fix(s)
        if ns != s:
            open(f, "w", encoding="utf-8").write(ns); c += 1
    print("pages changed", c)


if __name__ == "__main__":
    main()
