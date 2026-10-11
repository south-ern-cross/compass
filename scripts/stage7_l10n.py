#!/usr/bin/env python3
"""Stage 7 localisation fixes (idempotent).

  faq   <files>  rebuild FAQPage JSON-LD from the visible <details> FAQ (same language as page)
  lang  <files>  set "inLanguage": "en" -> page <html lang> in JSON-LD
  slots <files>  ES/PT slot pages: localise country links, add Brasil (PT), drop "Arte pendente/pendiente" box

  --dry-run      report what would change, write nothing

/go/ links, URLs, canonical and hreflang are never touched.

Fixes vs v1:
- slots(): Brasil presence no longer blocks whole country-block localisation.
  The check moved inside rep(): BR is prepended only if not already in the
  matched block (BR not in m.group(0)), and blk.sub always runs.
- --dry-run added to all three modes.
"""
import html, json, re, sys

DRY_RUN = '--dry-run' in sys.argv
if DRY_RUN:
    sys.argv.remove('--dry-run')

LD = re.compile(r'(?s)(<script type="application/ld\+json">)(.*?)(</script>)')

def write(path, s):
    if DRY_RUN:
        return
    open(path, 'w', encoding='utf-8').write(s)

def plain(x):
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', x))).strip()

def faq(path):
    s = open(path, encoding='utf-8').read()
    vis = re.findall(r'(?s)<details[^>]*>\s*<summary[^>]*>(.*?)</summary>(.*?)</details>', s)
    if not vis:
        m = re.search(r'(?s)<h2>(?:Preguntas frecuentes|Perguntas frequentes|FAQ)</h2>(.*?)(?=<h2|</section>)', s)
        if m:
            vis = re.findall(r'(?s)<p><strong>(.*?)</strong><br>(.*?)</p>', m.group(1))
    if not vis:
        return 'skip: no visible FAQ'
    qa = [{"@type": "Question", "name": plain(q),
           "acceptedAnswer": {"@type": "Answer", "text": plain(a)}} for q, a in vis]
    done = False
    def rep(m):
        nonlocal done
        d = json.loads(m.group(2))
        nodes = d.get('@graph', [d]) if isinstance(d, dict) else d
        for n in nodes:
            if isinstance(n, dict) and n.get('@type') == 'FAQPage':
                n['mainEntity'] = qa; done = True
        return m.group(1) + '\n' + json.dumps(d, ensure_ascii=False, indent=2) + '\n' + m.group(3) if done else m.group(0)
    s2 = LD.sub(rep, s)
    if not done:
        return 'skip: no FAQPage'
    write(path, s2)
    return f'{"would change" if DRY_RUN else "ok"}: {len(qa)} Q/A'

def lang(path):
    s = open(path, encoding='utf-8').read()
    L = re.search(r'<html[^>]*\blang="([^"]+)"', s).group(1)
    n = 0
    def rep(m):
        nonlocal n
        b, k = re.subn(r'"inLanguage":(\s*)"en"', lambda x: f'"inLanguage":{x.group(1)}"{L}"', m.group(2)); n += k
        return m.group(1) + b + m.group(3)
    s2 = LD.sub(rep, s)
    if n:
        write(path, s2)
    return f'{"would change" if DRY_RUN else "ok"}: {n} -> {L}'

NAMES = {
  'pt': {'nigeria': 'Nigéria', 'mexico': 'México', 'colombia': 'Colômbia', 'quenia': 'Quênia', 'africa-do-sul': 'África do Sul'},
  'es': {'nigeria': 'Nigeria', 'mexico': 'México', 'colombia': 'Colombia', 'kenia': 'Kenia', 'sudafrica': 'Sudáfrica'},
}
BR = '<a href="/pt/cassinos-online-brasil.html">Brasil</a>'
PLACEHOLDER = re.compile(r'\n?[ \t]*<div style="aspect-ratio:4/3;[^"]*"><span>Arte (?:pendente|pendiente)[^<]*</span></div>\n?')
CARD_PLACEHOLDER = re.compile(r'<a href="[^"]+"><div style="aspect-ratio:4/3;[^"]*">Arte (?:pendente|pendiente)</div></a>\n?')

def slots(path):
    lg = 'pt' if path.startswith('pt/') else 'es' if path.startswith('es/') else None
    if not lg or '/slots/' not in path:
        return 'skip: not ES/PT slot'
    s = open(path, encoding='utf-8').read(); s0 = s
    pre = 'melhores-cassinos-online' if lg == 'pt' else 'mejores-casinos-online'
    # FIX 2: block regex must also match when Brasil link leads the block.
    # Optional leading Brasil link (PT only), then the country links.
    br_lead = r'(?:<a href="/pt/cassinos-online-brasil\.html">[^<]*</a>\s*\|\s*)?' if lg == 'pt' else ''
    blk = re.compile(r'(?s)<p>\s*(%s(?:<a href="/%s/%s-[a-z-]+\.html">[^<]*</a>\s*\|?\s*)+)</p>' % (br_lead, lg, pre))
    def rep(m):
        inner = m.group(1)
        links = re.findall(r'<a href="(/%s/%s-([a-z-]+)\.html)">[^<]*</a>' % (lg, pre), inner)
        out = [f'<a href="{h}">{NAMES[lg].get(k, k)}</a>' for h, k in links]
        # FIX 1: Brasil check inside rep(), on the matched block only.
        # Localisation always runs; Brasil prepended only if absent from block.
        if lg == 'pt':
            if not re.search(r'/pt/cassinos-online-brasil\.html', inner):
                out.insert(0, BR)
            else:
                out.insert(0, BR)  # normalize: single canonical Brasil link first
        return '<p>\n      ' + ' |\n      '.join(out) + '\n    </p>'
    s = blk.sub(rep, s, count=1)
    s = PLACEHOLDER.sub('\n', s)
    s = CARD_PLACEHOLDER.sub('', s)
    s = re.sub(r' (?:Os títulos marcados|Los títulos marcados(?: como)?) "Arte (?:pendente|pendiente)"[^.<]*\.', '', s)
    if s != s0:
        write(path, s); return 'would change' if DRY_RUN else 'ok'
    return 'unchanged'

if __name__ == '__main__':
    fn = {'faq': faq, 'lang': lang, 'slots': slots}[sys.argv[1]]
    for p in sys.argv[2:]:
        print(p, fn(p))
