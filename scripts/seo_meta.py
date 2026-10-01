#!/usr/bin/env python3
"""SEO head hygiene, idempotent.

- Open Graph + Twitter tags from each page's own <title>, description,
  canonical and (if present) its real artwork image. Wrapped in
  <!-- og:start --> ... <!-- og:end --> so re-runs replace them.
- JSON-LD: removes self-assigned "reviewRating" / "aggregateRating" blocks
  (editorial star scores are not verifiable third-party ratings).
- Redirect stubs and duplicate pages: noindex + no hreflang.
"""
import os, re, sys, json, html
sys.path.insert(0, os.path.dirname(__file__))
from apply_layout import iter_pages, ROOT, page_lang
import site_config as C

OG_RE = re.compile(r'\n?<!-- og:start -->.*?<!-- og:end -->', re.S)

# Pages that duplicate another URL: page -> canonical target
DUPLICATES = {
    "es/slots/pragmatic-play/index.html": "https://spinorawins.com/es/tragamonedas-pragmatic-play.html",
    "pt/slots/pragmatic-play/index.html": "https://spinorawins.com/pt/caca-niqueis-pragmatic-play.html",
    # same game listed twice in the Yggdrasil catalog
    "slots/yggdrasil/jokers-spin-fest-2.html": "https://spinorawins.com/slots/yggdrasil/jokers-spin-fest.html",
    "es/slots/yggdrasil/jokers-spin-fest-2.html": "https://spinorawins.com/es/slots/yggdrasil/jokers-spin-fest.html",
    "pt/slots/yggdrasil/jokers-spin-fest-2.html": "https://spinorawins.com/pt/slots/yggdrasil/jokers-spin-fest.html",
}
# Pure meta-refresh redirect stubs
REDIRECT_STUBS = {"sweet-bonanza-review.html"}
# Missing reciprocal hreflang on EN pages whose ES/PT versions already point here
ADD_ALTERNATES = {
    "bitstarz-vs-cloudbet.html": {"es": "/es/bitstarz-vs-cloudbet.html", "pt": "/pt/bitstarz-vs-cloudbet.html"},
    "cloudbet-vs-stake.html": {"es": "/es/cloudbet-vs-stake.html", "pt": "/pt/cloudbet-vs-stake.html"},
}


def attr(s):
    return html.escape(html.unescape(s), quote=True)


def first(pattern, s):
    m = re.search(pattern, s, re.S)
    return m.group(1).strip() if m else None


def og_block(rel, s):
    lang = page_lang(rel)
    title = first(r"<title>(.*?)</title>", s)
    desc = first(r'<meta name="description" content="([^"]*)"', s)
    canon = first(r'<link rel="canonical" href="([^"]*)"', s)
    if not (title and canon):
        return None
    img = None
    m = re.search(r'"image":\s*"(https://spinorawins\.com/assets/images/[^"]+)"', s)
    if m and os.path.isfile(os.path.join(ROOT, m.group(1).replace(C.SITE + "/", ""))):
        img = m.group(1)
    else:
        main = s[s.find("<main"):] if "<main" in s else ""
        m = re.search(r'<img[^>]*src="(/assets/images/(?:slots|news|banners)/[^"]+\.(?:jpe?g|png|webp))"', main)
        if m and os.path.isfile(os.path.join(ROOT, m.group(1).lstrip("/"))):
            img = C.SITE + m.group(1)
    otype = "website" if rel in ("index.html", "es/index.html", "pt/index.html") else "article"
    lines = [
        '<meta property="og:site_name" content="Spinora Wins">',
        f'<meta property="og:type" content="{otype}">',
        f'<meta property="og:title" content="{attr(title)}">',
    ]
    if desc:
        lines.append(f'<meta property="og:description" content="{attr(desc)}">')
    lines.append(f'<meta property="og:url" content="{canon}">')
    lines.append(f'<meta property="og:locale" content="{C.OG_LOCALE[lang]}">')
    for l in C.LANGS:
        if l != lang and f'hreflang="{l}"' in s:
            lines.append(f'<meta property="og:locale:alternate" content="{C.OG_LOCALE[l]}">')
    if img:
        lines.append(f'<meta property="og:image" content="{img}">')
    lines.append(f'<meta name="twitter:card" content="{"summary_large_image" if img else "summary"}">')
    return "\n<!-- og:start -->\n" + "\n".join(lines) + "\n<!-- og:end -->"


def strip_ratings(s):
    def fix(m):
        raw = m.group(2)
        if "reviewRating" not in raw and "aggregateRating" not in raw:
            return m.group(0)
        try:
            data = json.loads(raw)
        except Exception:
            return m.group(0)
        def walk(o):
            if isinstance(o, dict):
                o.pop("reviewRating", None); o.pop("aggregateRating", None)
                for v in o.values(): walk(v)
            elif isinstance(o, list):
                for v in o: walk(v)
        walk(data)
        return m.group(1) + "\n" + json.dumps(data, ensure_ascii=False, indent=2) + "\n" + m.group(3)
    return re.sub(r'(<script type="application/ld\+json">)(.*?)(</script>)', fix, s, flags=re.S)


def main():
    n = 0
    for rel in iter_pages():
        p = os.path.join(ROOT, rel)
        s = open(p, encoding="utf-8").read()
        o = s
        s = OG_RE.sub("", s)
        if rel in REDIRECT_STUBS or rel in DUPLICATES:
            s = re.sub(r'<link rel="alternate" hreflang="[^"]*" href="[^"]*">\n?', "", s)
            if rel in REDIRECT_STUBS and 'name="robots"' not in s:
                s = s.replace("<title>", '<meta name="robots" content="noindex, follow">\n<title>', 1)
            if rel in DUPLICATES:
                # canonical only; noindex + canonical sends mixed signals
                s = s.replace('<meta name="robots" content="noindex, follow">\n', "")
                s = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{DUPLICATES[rel]}">', s)
        if rel in ADD_ALTERNATES:
            for l, u in ADD_ALTERNATES[rel].items():
                if f'hreflang="{l}"' not in s:
                    s = s.replace('<link rel="alternate" hreflang="x-default"', f'<link rel="alternate" hreflang="{l}" href="{C.SITE}{u}">\n<link rel="alternate" hreflang="x-default"', 1)
        s = strip_ratings(s)
        if rel not in REDIRECT_STUBS:
            blk = og_block(rel, s)
            if blk:
                s = re.sub(r'(<link rel="canonical" href="[^"]*">)', lambda m: m.group(1) + blk, s, count=1)
        if s != o:
            open(p, "w", encoding="utf-8").write(s)
            n += 1
    print("updated", n)


if __name__ == "__main__":
    main()
