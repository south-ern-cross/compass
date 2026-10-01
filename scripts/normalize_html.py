#!/usr/bin/env python3
"""Site-wide HTML hygiene, idempotent. Run after apply_layout.py.

- one stylesheet: /assets/css/style.css?v=<CSS_VERSION>; drops merged
  language.css / banner-slots.css and render-blocking Google Fonts
- removes page-scoped <style> blocks that now live in style.css
- breadcrumbs: <div> text trail -> <nav aria-label><ol> with aria-current
- wraps bare tables in .table-wrap (horizontal scroll on phones)
- images: decoding="async"; loading="lazy" unless already set
- affiliate anchors (/go/): rel always contains sponsored + noopener;
  href is never touched
"""
import os, re, sys, hashlib
sys.path.insert(0, os.path.dirname(__file__))
from apply_layout import iter_pages, ROOT, page_lang
import site_config as C

CSS_VERSION = "20261001"
CSS_TAG = f'<link rel="stylesheet" href="/assets/css/style.css?v={CSS_VERSION}">'
MOVED_STYLE_MARKERS = (
    "/* Top-list compact rows (page-scoped",
    "/* Temporary compact text card: no official Cashy banner",
    "/* --- Homepage two-column layout",
)
SLOTCARD_43 = ".slot-card img { width: 100%; height: auto; aspect-ratio: 4/3;"


def fix_head(s):
    s = re.sub(r'<link rel="stylesheet" href="[^"]*(?:language|banner-slots)\.css[^"]*">\s*\n?', "", s)
    s = re.sub(r'<link rel="preconnect" href="https://fonts\.(?:googleapis|gstatic)\.com"[^>]*>\s*\n?', "", s)
    s = re.sub(r'<link rel="stylesheet" href="https://fonts\.googleapis\.com[^"]*">\s*\n?', "", s)
    s = re.sub(r'<link rel="stylesheet" href="[^"]*assets/css/style\.css[^"]*">', CSS_TAG, s, count=1)
    def drop_style(m):
        body = m.group(1)
        if any(k in body for k in MOVED_STYLE_MARKERS):
            return ""
        if SLOTCARD_43 in body and "16/9" not in body:
            return ""
        return m.group(0)
    s = re.sub(r'<style>(.*?)</style>\s*\n?', drop_style, s, flags=re.S)
    return s


def fix_breadcrumbs(s, lang):
    label = C.LABELS[lang]["breadcrumb"]
    def conv(m):
        inner = m.group(1).strip()
        parts = [p.strip() for p in re.split(r'\s*(?:/|&rsaquo;|›|»)\s*(?![^<]*>)', inner) if p.strip()]
        lis = []
        for i, p in enumerate(parts):
            if i == len(parts) - 1 and not p.startswith("<a"):
                lis.append(f'<li aria-current="page">{p}</li>')
            else:
                lis.append(f"<li>{p}</li>")
        return f'<nav class="breadcrumbs" aria-label="{label}"><ol>{"".join(lis)}</ol></nav>'
    return re.sub(r'<div class="breadcrumbs">(.*?)</div>', conv, s, flags=re.S)


def wrap_tables(s):
    out, i = [], 0
    for m in re.finditer(r'<table\b[^>]*>.*?</table>', s, re.S):
        before = s[max(0, m.start() - 120):m.start()]
        out.append(s[i:m.start()])
        if re.search(r'class="table-wrap"[^>]*>\s*$', before) or re.search(r'overflow-x:\s*auto[^>]*>\s*$', before):
            out.append(m.group(0))
        else:
            out.append('<div class="table-wrap">' + m.group(0) + "</div>")
        i = m.end()
    out.append(s[i:])
    return "".join(out)


def fix_imgs(s):
    def f(m):
        tag = m.group(0)
        if "decoding=" not in tag:
            tag = tag[:-1].rstrip("/").rstrip() + ' decoding="async">'
        if "loading=" not in tag and "fetchpriority" not in tag:
            tag = tag[:-1] + ' loading="lazy">'
        return tag
    body_start = s.find("<body")
    return s[:body_start] + re.sub(r"<img\b[^>]*>", f, s[body_start:])


def fix_go_rel(s):
    def f(m):
        tag = m.group(0)
        if not re.search(r'href="(?:https://spinorawins\.com)?/go/', tag):
            return tag
        rm = re.search(r'\srel="([^"]*)"', tag)
        if rm:
            toks = rm.group(1).split()
            for t in ("sponsored", "noopener"):
                if t not in toks:
                    toks.append(t)
            return tag[:rm.start()] + f' rel="{" ".join(toks)}"' + tag[rm.end():]
        return tag[:-1] + ' rel="sponsored noopener">'
    return re.sub(r"<a\b[^>]*>", f, s)


def main():
    n = 0
    for rel in iter_pages():
        p = os.path.join(ROOT, rel)
        s = open(p, encoding="utf-8").read()
        o = s
        lang = page_lang(rel)
        s = fix_head(s)
        s = fix_breadcrumbs(s, lang)
        s = wrap_tables(s)
        s = fix_imgs(s)
        s = fix_go_rel(s)
        if s != o:
            open(p, "w", encoding="utf-8").write(s)
            n += 1
    print("normalized", n, "pages")


if __name__ == "__main__":
    main()
