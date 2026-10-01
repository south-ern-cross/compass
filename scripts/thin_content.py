#!/usr/bin/env python3
"""Apply / remove noindex,follow on templated slot stubs listed in
scripts/noindex-slots.txt (EN paths; ES/PT counterparts follow hreflang).
Pages stay online and crawlable (follow), they just leave the index and the
sitemap until they get real artwork and unique copy."""
import os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from apply_layout import iter_pages, ROOT, ALT_RE
import site_config as C

TAG = '<meta name="robots" content="noindex, follow" data-reason="thin-template">'


def main():
    listed = {l.strip() for l in open(os.path.join(ROOT, "scripts/noindex-slots.txt")) if l.strip() and not l.startswith("#")}
    targets = set()
    for rel in listed:
        targets.add(rel)
        s = open(os.path.join(ROOT, rel), encoding="utf-8").read(8000)
        for lang, href in ALT_RE.findall(s):
            if lang in ("es", "pt"):
                targets.add(href.replace(C.SITE + "/", ""))
    n = 0
    for rel in iter_pages():
        if "/slots/" not in "/" + rel:
            continue
        p = os.path.join(ROOT, rel)
        s = open(p, encoding="utf-8").read()
        o = s
        s = s.replace(TAG + "\n", "")
        if rel in targets:
            s = s.replace("<title>", TAG + "\n<title>", 1)
        if s != o:
            open(p, "w", encoding="utf-8").write(s)
            n += 1
    print("targets", len(targets), "changed", n)


if __name__ == "__main__":
    main()
