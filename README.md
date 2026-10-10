# Spinora Wins

Independent affiliate guides for LATAM and Africa.

## License

MIT
## Build scripts

Pages are static HTML. Shared parts are maintained by idempotent scripts in `scripts/`
(run from the repo root, in this order, after adding or editing pages):

1. `python3 scripts/apply_layout.py` – header, footer, language switch (config: `scripts/site_config.py`, SVGs in `partials/`)
2. `python3 scripts/fix_links.py` – repair relative/broken internal links and stylesheet paths
3. `python3 scripts/normalize_html.py` – single stylesheet link, breadcrumbs, table wrappers, image attributes, `rel="sponsored noopener"` on `/go/` links (hrefs never changed)
4. `python3 scripts/localize_links.py` – ES/PT pages link to same-language counterparts
5. `python3 scripts/seo_meta.py` – Open Graph/Twitter, reciprocal hreflang, unique titles, canonicals
6. `python3 scripts/thin_content.py` – `noindex,follow` for templated slot stubs listed in `scripts/noindex-slots.txt`
7. `python3 scripts/related_links.py` – contextual internal-link blocks
8. `python3 scripts/build_sitemap.py` – `sitemap.xml` from indexable self-canonical pages
9. `python3 scripts/img_dims.py` – width/height on local images
10. `python3 scripts/author.py` – unified JSON-LD author
11. `python3 scripts/helplines.py` – helpline table on responsible-gambling pages (data: `HELPLINES` in `site_config.py`, also used in the footer)
12. `python3 scripts/cards.py` – brand logos on all casino cards (map: `BRANDS`)
13. `python3 scripts/check_site.py` – broken links, hreflang reciprocity, sitemap, h1, `/go/` rel

Styles live in one file: `assets/css/style.css` (design tokens at the top). Bump `?v=` in
`normalize_html.py` when it changes. Affiliate redirects in `go/` are never touched by the scripts.


Retired markets (India, October 2026; Brazil was restored the same month and is an active target market): `scripts/remove_markets.py` turns the pages in `scripts/removed-pages.txt` into noindex redirect stubs and removes links to them; `scripts/market_text.py` drops those countries from "our markets" lists in copy. Run both before `related_links.py` if pages are regenerated.

Retired language (Portuguese, October 2026, restored the same month): `python3 scripts/retire_language.py pt` turns every `/pt/` page into a noindex redirect stub to its English counterpart and removes `pt` hreflang/links. PT was restored in October 2026 (Brazil is an active target market); `LANGS` in `site_config.py` is now `("en", "es", "pt")`. Never run `retire_language.py pt` - it would destroy 5,584 live PT pages.
