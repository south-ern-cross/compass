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
9. `python3 scripts/check_site.py` – broken links, hreflang reciprocity, sitemap, h1, `/go/` rel

Styles live in one file: `assets/css/style.css` (design tokens at the top). Bump `?v=` in
`normalize_html.py` when it changes. Affiliate redirects in `go/` are never touched by the scripts.
