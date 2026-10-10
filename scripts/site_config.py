"""Shared navigation, footer and label config for Spinora Wins (EN/ES/PT).

Edited by hand. scripts/apply_layout.py renders these into every page, so a
change here (plus one run of the script) updates the whole site.
All links are root-absolute so they work at any folder depth.
"""

SITE = "https://spinorawins.com"
LANGS = ("en", "es", "pt")  # "pt" restored October 2026 - Brazil is an active target market
HOME = {"en": "/", "es": "/es/", "pt": "/pt/"}
OG_LOCALE = {"en": "en_US", "es": "es_LA", "pt": "pt_BR"}

LABELS = {
    "en": {
        "skip": "Skip to content", "menu": "Menu", "close": "Close menu",
        "theme": "Toggle theme", "lang": "Language", "main_nav": "Main",
        "footer_nav": "Footer", "breadcrumb": "Breadcrumb",
        "home": "Home", "claim": "Claim",
        "disclaimer": "18+ | Gambling can be addictive. Play responsibly. This site contains affiliate links and earns commission from featured operators.",
        "rg_link": "Get help",
        "copyright": "&copy; 2026 Spinora Wins. Independent affiliate publisher. Not a gambling operator. Odds, bonuses and legal status vary by jurisdiction and change frequently - always confirm on the operator's site.",
        "age_gate": "18+ only. Gambling help: {short}.",
        "lang_missing": "This page is not translated yet - opens the {name} homepage",
    },
    "es": {
        "skip": "Saltar al contenido", "menu": "Menú", "close": "Cerrar menú",
        "theme": "Cambiar tema", "lang": "Idioma", "main_nav": "Principal",
        "footer_nav": "Pie de página", "breadcrumb": "Ruta de navegación",
        "home": "Inicio", "claim": "Ver oferta",
        "disclaimer": "18+. Jugar puede causar adicción. Hazlo con responsabilidad. Este sitio incluye enlaces de afiliados.",
        "rg_link": "Pedir ayuda",
        "copyright": "&copy; 2026 Spinora Wins. Publicador afiliado independiente. No somos un operador de juegos. Las cuotas, bonos y la situación legal varían según la jurisdicción y cambian con frecuencia: confirma siempre los datos en el sitio del operador.",
        "age_gate": "Solo mayores de 18 años. Ayuda con el juego: {short}.",
        "lang_missing": "Esta página aún no está traducida: abre la portada en {name}",
    },
    "pt": {
        "skip": "Pular para o conteúdo", "menu": "Menu", "close": "Fechar menu",
        "theme": "Alternar tema", "lang": "Idioma", "main_nav": "Principal",
        "footer_nav": "Rodapé", "breadcrumb": "Trilha de navegação",
        "home": "Início", "claim": "Ver oferta",
        "disclaimer": "18+. Apostar pode causar dependência. Jogue com responsabilidade. Este site contém links de afiliados.",
        "rg_link": "Buscar ajuda",
        "copyright": "&copy; 2026 Spinora Wins. Publicador afiliado independente. Não somos um operador de jogos. Odds, bônus e situação legal variam por jurisdição e mudam com frequência; confirme sempre no site do operador.",
        "age_gate": "Somente maiores de 18 anos. Ajuda com o jogo: {short}.",
        "lang_missing": "Esta página ainda não foi traduzida: abre a página inicial em {name}",
    },
}
LANG_NAMES = {"en": "English", "es": "Español", "pt": "Português"}

RG = {"en": "/responsible-gambling/index.html", "es": "/es/juego-responsable.html", "pt": "/pt/jogo-responsavel.html"}

NAV = {
    "en": [
        ("Top 10 Casinos", "/top-10-crypto-casinos.html"),
        ("Slots", "/slots/index.html"),
        ("RTP Database", "/tools/slot-rtp-database.html"),
        ("Tools", "/tools/index.html"),
        ("Payments", "/payment-methods/index.html"),
        ("Blog", "/blog/index.html"),
        ("Responsible Gambling", "/responsible-gambling/index.html"),
    ],
    "es": [
        ("Top 10 casinos", "/es/top-10-casinos-cripto.html"),
        ("Tragamonedas", "/es/slots/index.html"),
        ("RTP de tragamonedas", "/es/base-datos-rtp-tragamonedas.html"),
        ("Herramientas", "/es/herramientas.html"),
        ("Métodos de pago", "/es/metodos-de-pago.html"),
        ("Blog", "/es/blog.html"),
        ("Juego responsable", "/es/juego-responsable.html"),
    ],
    "pt": [
        ("Top 10 cassinos", "/pt/top-10-cassinos-cripto.html"),
        ("Caça-níqueis", "/pt/slots/index.html"),
        ("RTP dos caça-níqueis", "/pt/banco-de-dados-rtp-caca-niqueis.html"),
        ("Ferramentas", "/pt/ferramentas.html"),
        ("Pagamentos", "/pt/metodos-de-pagamento.html"),
        ("Blog", "/pt/blog.html"),
        ("Jogo responsável", "/pt/jogo-responsavel.html"),
    ],
}

FOOTER = {
    "en": [
        ("Country Guides", [
            ("Casinos in Nigeria", "/online-casinos-nigeria.html"),
            ("Casinos in Mexico", "/online-casinos-mexico.html"),
            ("Casinos in Colombia", "/online-casinos-colombia.html"),
            ("Casinos in Kenya", "/online-casinos-kenya.html"),
            ("Casinos in South Africa", "/online-casinos-south-africa.html"),
        ]),
        ("Best Casinos", [
            ("Top 10 Crypto Casinos", "/top-10-crypto-casinos.html"),
            ("Best in Nigeria", "/best-online-casinos-nigeria.html"),
            ("Best in Mexico", "/best-online-casinos-mexico.html"),
            ("Best in Colombia", "/best-online-casinos-colombia.html"),
            ("Best in Kenya", "/best-online-casinos-kenya.html"),
            ("Best in South Africa", "/best-online-casinos-south-africa.html"),
        ]),
        ("Casino Reviews", [
            ("Cloudbet", "/cloudbet-review.html"),
            ("BitStarz", "/bitstarz-review.html"),
            ("Duelbits", "/duelbits-review.html"),
            ("Rollbit", "/rollbit-review.html"),
            ("Cashy", "/cashy-review.html"),
            ("Vave", "/vave-review.html"),
            ("N1 Casino", "/n1-casino-review.html"),
            ("Cooked", "/cooked-review.html"),
            ("Planbet", "/planbet-review.html"),
            ("22Bet", "/22bet-review.html"),
        ]),
        ("Payments & Tools", [
            ("SPEI (Mexico)", "/payment-methods/spei-mexico-casinos.html"),
            ("PSE (Colombia)", "/payment-methods/pse-colombia-casinos.html"),
            ("Crypto Payments", "/payment-methods/crypto-casinos-latam-africa.html"),
            ("Wagering Calculator", "/tools/wagering-requirement-calculator.html"),
            ("Bonus Comparator", "/tools/bonus-comparator.html"),
            ("Bonus EV Calculator", "/tools/bonus-expected-value-calculator.html"),
            ("Free Spins Value Calculator", "/tools/free-spins-value-calculator.html"),
        ]),
        ("Trust & Safety", [
            ("Responsible Gambling", "/responsible-gambling/index.html"),
            ("Self-Exclusion Tools", "/responsible-gambling/self-exclusion-tools.html"),
            ("How We Rate", "/how-we-rate.html"),
            ("Methodology", "/methodology.html"),
            ("Casino Blacklist", "/blacklist-rogue-casinos.html"),
            ("Complaints", "/complaints.html"),
            ("About Us", "/about-us.html"),
            ("Contact", "/contact.html"),
            ("Privacy Policy", "/privacy.html"),
        ]),
    ],
    "es": [
        ("Guías por país", [
            ("Casinos en Nigeria", "/es/casinos-online-nigeria.html"),
            ("Casinos en México", "/es/casinos-online-mexico.html"),
            ("Casinos en Colombia", "/es/casinos-online-colombia.html"),
            ("Casinos en Kenia", "/es/casinos-online-kenia.html"),
            ("Casinos en Sudáfrica", "/es/casinos-online-sudafrica.html"),
        ]),
        ("Mejores casinos", [
            ("Top 10 casinos cripto", "/es/top-10-casinos-cripto.html"),
            ("Mejores en Nigeria", "/es/mejores-casinos-online-nigeria.html"),
            ("Mejores en México", "/es/mejores-casinos-online-mexico.html"),
            ("Mejores en Colombia", "/es/mejores-casinos-online-colombia.html"),
            ("Mejores en Kenia", "/es/mejores-casinos-online-kenia.html"),
            ("Mejores en Sudáfrica", "/es/mejores-casinos-online-sudafrica.html"),
        ]),
        ("Reseñas de casinos", [
            ("Cloudbet", "/es/resena-cloudbet.html"),
            ("BitStarz", "/es/resena-bitstarz.html"),
            ("Duelbits", "/es/resena-duelbits.html"),
            ("Rollbit", "/es/resena-rollbit.html"),
            ("Cashy", "/es/resena-cashy.html"),
            ("Vave", "/es/resena-vave.html"),
            ("N1 Casino", "/es/resena-n1-casino.html"),
            ("Cooked", "/es/resena-cooked.html"),
        ]),
        ("Pagos y herramientas", [
            ("SPEI en México", "/es/casinos-spei-mexico.html"),
            ("PSE en Colombia", "/es/casinos-pse-colombia.html"),
            ("Pagos con criptomonedas", "/es/casinos-cripto-latam-africa.html"),
            ("Calculadora de requisitos de apuesta", "/es/calculadora-requisitos-apuesta.html"),
            ("Comparador de bonos", "/es/comparador-de-bonos.html"),
            ("Valor esperado de los bonos", "/es/calculadora-valor-esperado-bono.html"),
            ("Calculadora de giros gratis", "/es/calculadora-valor-giros-gratis.html"),
        ]),
        ("Confianza y seguridad", [
            ("Juego responsable", "/es/juego-responsable.html"),
            ("Herramientas de autoexclusión", "/es/herramientas-autoexclusion.html"),
            ("Cómo evaluamos", "/es/como-evaluamos.html"),
            ("Metodología", "/es/metodologia.html"),
            ("Quiénes somos", "/es/quienes-somos.html"),
            ("Contacto", "/es/contacto.html"),
            ("Política de Privacidad", "/privacy.html"),
        ]),
    ],
    "pt": [
        ("Guias por país", [
            ("Cassinos na Nigéria", "/pt/cassinos-online-nigeria.html"),
            ("Cassinos no México", "/pt/cassinos-online-mexico.html"),
            ("Cassinos na Colômbia", "/pt/cassinos-online-colombia.html"),
            ("Cassinos no Quênia", "/pt/cassinos-online-quenia.html"),
            ("Cassinos na África do Sul", "/pt/cassinos-online-africa-do-sul.html"),
        ]),
        ("Melhores cassinos", [
            ("Top 10 cassinos cripto", "/pt/top-10-cassinos-cripto.html"),
            ("Melhores na Nigéria", "/pt/melhores-cassinos-online-nigeria.html"),
            ("Melhores no México", "/pt/melhores-cassinos-online-mexico.html"),
            ("Melhores na Colômbia", "/pt/melhores-cassinos-online-colombia.html"),
            ("Melhores no Quênia", "/pt/melhores-cassinos-online-quenia.html"),
            ("Melhores na África do Sul", "/pt/melhores-cassinos-online-africa-do-sul.html"),
        ]),
        ("Avaliações de cassinos", [
            ("Cloudbet", "/pt/avaliacao-cloudbet.html"),
            ("BitStarz", "/pt/avaliacao-bitstarz.html"),
            ("Duelbits", "/pt/avaliacao-duelbits.html"),
            ("Rollbit", "/pt/avaliacao-rollbit.html"),
            ("Cashy", "/pt/avaliacao-cashy.html"),
            ("Vave", "/pt/avaliacao-vave.html"),
            ("N1 Casino", "/pt/avaliacao-n1-casino.html"),
            ("Cooked", "/pt/avaliacao-cooked.html"),
        ]),
        ("Pagamentos e ferramentas", [
            ("SPEI no México", "/pt/cassinos-spei-mexico.html"),
            ("PSE na Colômbia", "/pt/cassinos-pse-colombia.html"),
            ("Pagamentos com criptomoedas", "/pt/cassinos-cripto-latam-africa.html"),
            ("Calculadora de rollover", "/pt/calculadora-requisitos-aposta.html"),
            ("Comparador de bônus", "/pt/comparador-de-bonus.html"),
            ("Valor esperado dos bônus", "/pt/calculadora-valor-esperado-bonus.html"),
            ("Valor das rodadas grátis", "/pt/calculadora-valor-rodadas-gratis.html"),
        ]),
        ("Confiança e segurança", [
            ("Jogo responsável", "/pt/jogo-responsavel.html"),
            ("Ferramentas de autoexclusão", "/pt/ferramentas-autoexclusao.html"),
            ("Como avaliamos", "/pt/como-avaliamos.html"),
            ("Metodologia", "/pt/metodologia.html"),
            ("Quem somos", "/pt/quem-somos.html"),
            ("Fale com a gente", "/pt/contato.html"),
            ("Política de Privacidade", "/privacy.html"),
        ]),
    ],
}


# Problem-gambling help per market (owner-verified, October 2026).
# Rendered into the footer (short form) and the responsible-gambling pages (table).
# Each entry: (country EN/ES/PT, [(label EN/ES/PT, value, href or None)], short footer number)
HELPLINES = [
    (("Nigeria", "Nigeria", "Nigéria"), [
        (("Gamble Alert", "Gamble Alert", "Gamble Alert"), "+234 916 295 7989", "tel:+2349162957989"),
        (None, "+234 705 889 0073", "tel:+2347058890073"),
        (None, "+234 705 889 0074", "tel:+2347058890074"),
        (None, "gamblealert.org", "https://gamblealert.org/"),
    ], ("Gamble Alert", "+234 916 295 7989", "tel:+2349162957989")),
    (("Kenya", "Kenia", "Quênia"), [
        (("Gamhelp Kenya", "Gamhelp Kenya", "Gamhelp Kenya"), "+254 700 656 284", "tel:+254700656284"),
        (None, "+254 725 492 006", "tel:+254725492006"),
        (None, "gamhelpkenya.com", "https://gamhelpkenya.com/"),
        (("Ministry of Health helpline", "Línea del Ministerio de Salud", "Linha do Ministério da Saúde"), "719", "tel:719"),
    ], ("Gamhelp Kenya", "+254 700 656 284", "tel:+254700656284")),
    (("South Africa", "Sudáfrica", "África do Sul"), [
        (("Problem gambling counselling line (free, 24/7)", "Línea de ayuda por juego problemático (gratuita, 24/7)", "Linha de apoio para jogo problemático (gratuita, 24h)"), "0800 006 008", "tel:0800006008"),
        (("WhatsApp", "WhatsApp", "WhatsApp"), "076 675 0710", "https://wa.me/27766750710"),
        (None, "responsiblegambling.org.za", "https://responsiblegambling.org.za/"),
    ], ("", "0800 006 008", "tel:0800006008")),
    (("Mexico", "México", "México"), [
        (("Línea de la Vida (24/7)", "Línea de la Vida (24/7)", "Línea de la Vida (24h)"), "800 911 2000", "tel:8009112000"),
        (("Gambling player support (SEGOB)", "Atención a jugadores (SEGOB)", "Atendimento a jogadores (SEGOB)"), "atnjugadores@segob.mx", "mailto:atnjugadores@segob.mx"),
    ], ("Línea de la Vida", "800 911 2000", "tel:8009112000")),
    (("Colombia", "Colombia", "Colômbia"), [
        (("No dedicated gambling helpline. Coljuegos \u201cJuega bien\u201d", "No hay línea específica para el juego. Coljuegos \u201cJuega bien\u201d", "Não há linha específica para jogo. Coljuegos \u201cJuega bien\u201d"), "coljuegos.gov.co", "https://www.coljuegos.gov.co/"),
        (("Mental health line", "Línea de salud mental", "Linha de saúde mental"), "106", "tel:106"),
    ], ("Línea", "106", "tel:106")),
]
LI = {"en": 0, "es": 1, "pt": 2}


def helplines_short(lang):
    out = []
    for names, _, (label, num, href) in HELPLINES:
        lab = (label + " ") if label else ""
        out.append(f'{names[LI[lang]]} – {lab}<a href="{href}">{num}</a>')
    return "; ".join(out)


def helplines_table(lang):
    k = LI[lang]
    head = {"en": ("Country", "Where to get help"), "es": ("País", "Dónde pedir ayuda"), "pt": ("País", "Onde pedir ajuda")}[lang]
    rows = []
    for names, items, _ in HELPLINES:
        parts = []
        for lab, val, href in items:
            ext = ' rel="noopener" target="_blank"' if href.startswith("http") else ""
            a = f'<a href="{href}"{ext}>{val}</a>'
            parts.append(f"{lab[k]}: {a}" if lab else a)
        rows.append(f"      <tr><td>{names[k]}</td><td>{', '.join(parts)}</td></tr>")
    return ("<!-- helplines:start -->\n<div class=\"table-wrap\"><table>\n"
            f"      <tr><th>{head[0]}</th><th>{head[1]}</th></tr>\n" + "\n".join(rows) + "\n    </table></div>\n<!-- helplines:end -->")
