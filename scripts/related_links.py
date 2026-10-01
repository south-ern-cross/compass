#!/usr/bin/env python3
"""Contextual internal-link blocks (idempotent, marker-wrapped).

1. Country clusters: every page about one market links to the other pages
   about that market (hub, best list, crypto list, bonuses, payments,
   EN in-depth guides).
2. Crypto topic cluster: evergreen crypto-casino guides link to each other.
3. Operator reviews: "Ranked in" block listing the toplist pages that
   already link to that review (derived from real links, no new claims).
Anchors are the target page's own <h1>. ES/PT use the localized
counterparts from hreflang; EN-only pages are not linked from ES/PT.
"""
import os, re, sys, html
sys.path.insert(0, os.path.dirname(__file__))
from apply_layout import iter_pages, ROOT, ALT_RE, page_lang
import site_config as C

START, END = "<!-- related:start -->", "<!-- related:end -->"
BLOCK_RE = re.compile(r"\n?" + re.escape(START) + r".*?" + re.escape(END), re.S)

COUNTRIES = {
    "nigeria": ["online-casinos-nigeria.html", "best-online-casinos-nigeria.html", "best-bitcoin-casinos-nigeria.html",
                "crypto-casino-bonuses-nigeria.html", "payment-methods/nigeria-casino-deposits.html", "guides/nigeria/*"],
    "mexico": ["online-casinos-mexico.html", "best-online-casinos-mexico.html", "best-crypto-casinos-mexico.html",
               "crypto-casino-bonuses-mexico.html", "payment-methods/spei-mexico-casinos.html", "guides/mexico/*"],
    "colombia": ["online-casinos-colombia.html", "best-online-casinos-colombia.html", "best-crypto-casinos-colombia.html",
                 "payment-methods/pse-colombia-casinos.html", "guides/colombia/*"],
    "kenya": ["online-casinos-kenya.html", "best-online-casinos-kenya.html", "best-crypto-casinos-kenya.html",
              "crypto-casino-bonuses-kenya.html", "guides/kenya/*"],
    "south-africa": ["online-casinos-south-africa.html", "best-online-casinos-south-africa.html", "best-crypto-casinos-south-africa.html",
                     "crypto-casino-bonuses-south-africa.html", "guides/south-africa/*"],
}
COUNTRY_NAMES = {
    "nigeria": ("Nigeria", "Nigeria", "Nigéria"),
    "mexico": ("Mexico", "México", "México"), "colombia": ("Colombia", "Colombia", "Colômbia"),
    "kenya": ("Kenya", "Kenia", "Quênia"), "south-africa": ("South Africa", "Sudáfrica", "África do Sul"),
}
CRYPTO = ["top-10-crypto-casinos.html", "new-crypto-casinos.html", "best-bitcoin-casinos.html", "best-ethereum-casinos.html",
          "usdt-tether-casinos.html", "no-kyc-crypto-casinos.html", "best-instant-withdrawal-crypto-casinos.html",
          "best-low-minimum-deposit-crypto-casinos.html", "best-crypto-casino-bonuses.html", "best-crypto-casino-free-spins.html",
          "no-deposit-crypto-casino-bonuses.html", "crypto-casino-mobile-apps.html", "how-to-buy-crypto-for-online-casinos.html",
          "how-to-stay-private-at-crypto-casinos.html", "bitstarz-vs-cloudbet.html", "cloudbet-vs-stake.html",
          "payment-methods/bitcoin-casino-guide.html", "payment-methods/ethereum-casino-guide.html", "payment-methods/usdt-casino-guide.html"]
REVIEWS = ["cloudbet", "bitstarz", "duelbits", "rollbit", "cashy", "vave", "n1-casino", "cooked", "planbet", "22bet", "bc-game", "trustdice"]
TXT = {
    "country": ("More on {c}", "Más sobre {c}", "Mais sobre {c}"),
    "crypto": ("Related crypto casino guides", "Guías relacionadas de casinos cripto", "Guias relacionados de cassinos cripto"),
    "ranked": ("Where {n} is ranked", "Dónde aparece {n} en nuestras listas", "Onde {n} aparece nas nossas listas"),
}
LI = {"en": 0, "es": 1, "pt": 2}


def expand(lst):
    out = []
    for x in lst:
        if x.endswith("/*"):
            d = x[:-2]
            out += sorted(os.path.join(d, f) for f in os.listdir(os.path.join(ROOT, d)) if f.endswith(".html"))
        elif os.path.isfile(os.path.join(ROOT, x)):
            out.append(x)
    return out


def read(rel):
    return open(os.path.join(ROOT, rel), encoding="utf-8").read()


def counterpart(en_rel, lang):
    if lang == "en":
        return en_rel
    alts = dict(ALT_RE.findall(read(en_rel)[:8000]))
    u = alts.get(lang)
    if not u:
        return None
    r = u.replace(C.SITE + "/", "")
    return r if os.path.isfile(os.path.join(ROOT, r)) else None


def is_indexable(rel):
    return 'content="noindex' not in read(rel)[:8000]


def anchor(rel):
    s = read(rel)
    m = re.search(r"<h1[^>]*>(.*?)</h1>", s, re.S)
    t = re.sub(r"<[^>]+>", "", m.group(1)) if m else re.search(r"<title>(.*?)</title>", s).group(1).split(" | ")[0]
    t = re.sub(r"[\U0001F1E6-\U0001F1FF]", "", html.unescape(t))
    return html.escape(re.sub(r"\s+", " ", t).strip())


def block(title, links):
    lis = "\n".join(f'    <li><a href="/{r}">{anchor(r)}</a></li>' for r in links)
    return f'{START}\n<aside class="related-links" aria-label="{html.escape(title)}">\n  <h2>{title}</h2>\n  <ul>\n{lis}\n  </ul>\n</aside>\n{END}'


def insert(s, blk):
    s = BLOCK_RE.sub("", s)
    if not blk:
        return s
    i = s.find('<div class="byline"')
    j = s.find("</main>")
    if i < 0 or i > j:
        i = j
    i = s.rfind("\n", 0, i) + 1
    return s[:i] + blk + "\n" + s[i:]


def main():
    plan = {}
    for lang in C.LANGS:
        k = LI[lang]
        for c, lst in COUNTRIES.items():
            pages = [p for p in (counterpart(e, lang) for e in expand(lst)) if p and is_indexable(p)]
            for p in pages:
                others = [q for q in pages if q != p]
                if others:
                    plan.setdefault(p, []).append(block(TXT["country"][k].format(c=COUNTRY_NAMES[c][k]), others[:10]))
        cpages = [p for p in (counterpart(e, lang) for e in expand(CRYPTO)) if p and is_indexable(p)]
        for p in cpages:
            others = [q for q in cpages if q != p][:8]
            plan.setdefault(p, []).append(block(TXT["crypto"][k], others))
    # reviews: ranked in (from real inbound links on toplist pages)
    toplists = {}
    for rel in iter_pages():
        if "/slots/" in "/" + rel:
            continue
        b = os.path.basename(rel)
        if any(x in b for x in ("best-", "top-10", "mejores-", "melhores-", "new-crypto")):
            toplists[rel] = read(rel)
    for lang in C.LANGS:
        for op in REVIEWS:
            en = f"{op}-review.html"
            if not os.path.isfile(os.path.join(ROOT, en)):
                continue
            r = counterpart(en, lang)
            if not r:
                continue
            refs = sorted(t for t, s in toplists.items() if page_lang(t) == lang and re.search(r'href="(?:/|\.\./)?' + re.escape(r if lang == "en" else r) + '"', s.split("<footer")[0]) or (page_lang(t) == lang and f'href="/{r}"' in s.split("<footer")[0]))
            refs = [t for t in refs if is_indexable(t)]
            if refs:
                name = re.search(r'<h1[^>]*>(.*?)</h1>', read(r), re.S)
                nm = {"cloudbet": "Cloudbet", "bitstarz": "BitStarz", "duelbits": "Duelbits", "rollbit": "Rollbit", "cashy": "Cashy", "vave": "Vave", "n1-casino": "N1 Casino", "cooked": "Cooked", "planbet": "Planbet", "22bet": "22Bet", "bc-game": "BC.Game", "trustdice": "TrustDice"}[op]
                plan.setdefault(r, []).append(block(TXT["ranked"][LI[lang]].format(n=nm), refs[:10]))
    n = 0
    for rel in iter_pages():
        if "/slots/" in "/" + rel and rel not in plan:
            continue
        s = read(rel)
        blk = "\n".join(plan.get(rel, []))
        ns = insert(s, blk)
        if ns != s:
            open(os.path.join(ROOT, rel), "w", encoding="utf-8").write(ns)
            n += 1
    print("pages with related blocks:", sum(1 for v in plan.values() if v), "changed", n)


if __name__ == "__main__":
    main()
