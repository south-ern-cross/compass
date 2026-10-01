#!/usr/bin/env python3
"""Render the shared header and footer into every HTML page.

Usage:  python3 scripts/apply_layout.py [--check]

* Header and footer come from scripts/site_config.py (one source per language).
* The language switch of each page is built from that page's own
  <link rel="alternate" hreflang> tags, so it always matches hreflang.
* /go/ redirect files are never touched.
* Idempotent: running it twice gives the same output.
"""
import os, re, sys, html
sys.path.insert(0, os.path.dirname(__file__))
import site_config as C

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PART = os.path.join(ROOT, "partials")
LOGO = open(os.path.join(PART, "logo.svg")).read().strip()
CHIP = open(os.path.join(PART, "footer-chip.svg")).read().strip()
ICONS = open(os.path.join(PART, "theme-icons.svg")).read().strip()
MENU_ICON = ('<svg class="nav-toggle-icon" viewBox="0 0 24 24" aria-hidden="true">'
             '<path d="M4 7h16M4 12h16M4 17h16"/></svg>')

HEADER_RE = re.compile(r'(?:<a class="skip-link"[^>]*>.*?</a>\s*)?<header class="site-header">.*?</header>', re.S)
FOOTER_RE = re.compile(r'<footer( class="site-footer")?>.*?</footer>', re.S)
ALT_RE = re.compile(r'<link rel="alternate" hreflang="([^"]+)" href="([^"]+)"\s*/?>')


def page_lang(rel):
    if rel.startswith("es/"):
        return "es"
    if rel.startswith("pt/"):
        return "pt"
    return "en"


def page_url(rel):
    if rel in ("index.html", "es/index.html", "pt/index.html"):
        return "/" + rel[: -len("index.html")]
    return "/" + rel


def norm(u):
    u = u.replace(C.SITE, "")
    return u or "/"


def is_current(href, rel):
    me = "/" + rel
    return href == me or (href.endswith("/") and me == href + "index.html")


def render_header(lang, rel, alts):
    L = C.LABELS[lang]
    items = []
    for label, href in C.NAV[lang]:
        cur = ' aria-current="page"' if is_current(href, rel) else ""
        items.append(f'<li><a href="{href}"{cur}>{label}</a></li>')
    sw = []
    for l in C.LANGS:
        name = C.LANG_NAMES[l]
        if l == lang:
            sw.append(f'<a href="{page_url(rel)}" lang="{l}" hreflang="{l}" aria-current="page" title="{name}">{l.upper()}</a>')
        elif l in alts:
            sw.append(f'<a href="{norm(alts[l])}" lang="{l}" hreflang="{l}" title="{name}">{l.upper()}</a>')
        else:
            t = html.escape(C.LABELS[l]["lang_missing"].format(name=name))
            sw.append(f'<a href="{C.HOME[l]}" lang="{l}" hreflang="{l}" title="{t}">{l.upper()}</a>')
    return (
        f'<a class="skip-link" href="#main">{L["skip"]}</a>\n'
        '<header class="site-header">\n'
        f'  <div class="disclaimer-banner" role="note">{L["disclaimer"]} <a href="{C.RG[lang]}">{L["rg_link"]}</a></div>\n'
        '  <div class="container nav">\n'
        f'    <a href="{C.HOME[lang]}" class="logo">{LOGO}</a>\n'
        f'    <nav class="primary-nav" aria-label="{L["main_nav"]}">\n'
        f'      <ul class="nav-links" id="primary-menu">\n        ' + "\n        ".join(items) + "\n      </ul>\n    </nav>\n"
        f'    <nav class="language-switch" aria-label="{L["lang"]}">' + " ".join(sw) + "</nav>\n"
        f'    <button class="theme-toggle" type="button" aria-label="{L["theme"]}" aria-pressed="false">{ICONS}</button>\n'
        f'    <button class="nav-toggle" type="button" aria-controls="primary-menu" aria-expanded="false" aria-label="{L["menu"]}" data-label-open="{L["menu"]}" data-label-close="{L["close"]}">{MENU_ICON}</button>\n'
        "  </div>\n"
        "</header>"
    )


def render_footer(lang):
    L = C.LABELS[lang]
    cols = []
    for title, links in C.FOOTER[lang]:
        a = "\n".join(f'          <li><a href="{h}">{t}</a></li>' for t, h in links)
        cols.append(f"      <div>\n        <h2>{title}</h2>\n        <ul>\n{a}\n        </ul>\n      </div>")
    return (
        '<footer class="site-footer">\n'
        f'  <div class="container"><div class="footer-brand"><a href="{C.HOME[lang]}">{CHIP}</a><span class="age-badge" aria-label="18+">18+</span></div>\n'
        f'    <nav class="footer-grid" aria-label="{L["footer_nav"]}">\n' + "\n".join(cols) + "\n    </nav>\n"
        '    <div class="footer-bottom">\n'
        f'      <p>{L["copyright"]}</p>\n'
        f'      <p class="age-gate">{L["age_gate"].format(short=C.helplines_short(lang))} <a href="{C.RG[lang]}">{L["rg_link"]}</a></p>\n'
        "    </div>\n  </div>\n</footer>"
    )


def iter_pages():
    for dp, dn, fn in os.walk(ROOT):
        rel_dp = os.path.relpath(dp, ROOT)
        dn[:] = [d for d in dn if d not in (".git", "go", "partials", "scripts", "node_modules") or rel_dp != "."]
        for f in fn:
            if f.endswith(".html"):
                rel = os.path.relpath(os.path.join(dp, f), ROOT).replace(os.sep, "/")
                if rel.startswith(("go/", "partials/")):
                    continue
                yield rel


def apply(rel, s):
    lang = page_lang(rel)
    alts = {k: v for k, v in ALT_RE.findall(s)}
    if HEADER_RE.search(s):
        s = HEADER_RE.sub(lambda m: render_header(lang, rel, alts), s, count=1)
    if FOOTER_RE.search(s):
        s = FOOTER_RE.sub(lambda m: render_footer(lang), s, count=1)
    # skip-link target
    s = re.sub(r'<main(?![^>]*\bid=)([^>]*)>', r'<main id="main"\1>', s, count=1)
    return s


def main():
    check = "--check" in sys.argv
    changed = 0
    for rel in iter_pages():
        p = os.path.join(ROOT, rel)
        s = open(p, encoding="utf-8").read()
        n = apply(rel, s)
        if n != s:
            changed += 1
            if not check:
                open(p, "w", encoding="utf-8").write(n)
    print(("would change" if check else "changed"), changed, "pages")
    if check and changed:
        sys.exit(1)


if __name__ == "__main__":
    main()
