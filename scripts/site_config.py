"""Shared navigation, footer and label config for Spinora Wins (EN/ES/PT).

Edited by hand. scripts/apply_layout.py renders these into every page, so a
change here (plus one run of the script) updates the whole site.
All links are root-absolute so they work at any folder depth.
"""

SITE = "https://spinorawins.com"
LANGS = ("en", "es", "pt")
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
        "age_gate": "Gambling is restricted to legal age (18+/21+ depending on jurisdiction). If you or someone you know has a gambling problem, seek help: BeGambleAware (UK), National Council on Problem Gambling (US/NG resources), CVV (Brazil) 188.",
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
        "age_gate": "El juego está restringido a la mayoría de edad (18+/21+ según la jurisdicción). Si tú o alguien que conoces tiene un problema con el juego, busca ayuda: BeGambleAware (Reino Unido), National Council on Problem Gambling (EE. UU. y recursos para Nigeria), CVV (Brasil) 188.",
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
        "age_gate": "O jogo é restrito à idade legal (18+/21+ conforme a jurisdição). Se você ou alguém que você conhece tem problema com jogo, busque ajuda: BeGambleAware (Reino Unido), National Council on Problem Gambling (EUA/recursos NG), CVV (Brasil) 188.",
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
            ("Casinos in Brazil", "/online-casinos-brazil.html"),
            ("Casinos in Mexico", "/online-casinos-mexico.html"),
            ("Casinos in Colombia", "/online-casinos-colombia.html"),
            ("Casinos in Kenya", "/online-casinos-kenya.html"),
            ("Casinos in South Africa", "/online-casinos-south-africa.html"),
            ("Casinos in India", "/online-casinos-india.html"),
        ]),
        ("Best Casinos", [
            ("Top 10 Crypto Casinos", "/top-10-crypto-casinos.html"),
            ("Best in Nigeria", "/best-online-casinos-nigeria.html"),
            ("Best in Brazil", "/best-online-casinos-brazil.html"),
            ("Best in Mexico", "/best-online-casinos-mexico.html"),
            ("Best in Colombia", "/best-online-casinos-colombia.html"),
            ("Best in Kenya", "/best-online-casinos-kenya.html"),
            ("Best in South Africa", "/best-online-casinos-south-africa.html"),
            ("Best in India", "/best-online-casinos-india.html"),
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
            ("PIX (Brazil)", "/payment-methods/pix-brazil-casinos.html"),
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
            ("Casinos en Brasil", "/es/casinos-online-brasil.html"),
            ("Casinos en México", "/es/casinos-online-mexico.html"),
            ("Casinos en Colombia", "/es/casinos-online-colombia.html"),
            ("Casinos en Kenia", "/es/casinos-online-kenia.html"),
            ("Casinos en Sudáfrica", "/es/casinos-online-sudafrica.html"),
            ("Casinos en India", "/es/casinos-online-india.html"),
        ]),
        ("Mejores casinos", [
            ("Top 10 casinos cripto", "/es/top-10-casinos-cripto.html"),
            ("Mejores en Nigeria", "/es/mejores-casinos-online-nigeria.html"),
            ("Mejores en Brasil", "/es/mejores-casinos-online-brasil.html"),
            ("Mejores en México", "/es/mejores-casinos-online-mexico.html"),
            ("Mejores en Colombia", "/es/mejores-casinos-online-colombia.html"),
            ("Mejores en Kenia", "/es/mejores-casinos-online-kenia.html"),
            ("Mejores en Sudáfrica", "/es/mejores-casinos-online-sudafrica.html"),
            ("Mejores en India", "/es/mejores-casinos-online-india.html"),
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
            ("PIX en Brasil", "/es/casinos-pix-brasil.html"),
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
            ("Cassinos no Brasil", "/pt/cassinos-online-brasil.html"),
            ("Cassinos no México", "/pt/cassinos-online-mexico.html"),
            ("Cassinos na Colômbia", "/pt/cassinos-online-colombia.html"),
            ("Cassinos no Quênia", "/pt/cassinos-online-quenia.html"),
            ("Cassinos na África do Sul", "/pt/cassinos-online-africa-do-sul.html"),
            ("Cassinos na Índia", "/pt/cassinos-online-india.html"),
        ]),
        ("Melhores cassinos", [
            ("Top 10 cassinos cripto", "/pt/top-10-cassinos-cripto.html"),
            ("Melhores na Nigéria", "/pt/melhores-cassinos-online-nigeria.html"),
            ("Melhores no Brasil", "/pt/melhores-cassinos-online-brasil.html"),
            ("Melhores no México", "/pt/melhores-cassinos-online-mexico.html"),
            ("Melhores na Colômbia", "/pt/melhores-cassinos-online-colombia.html"),
            ("Melhores no Quênia", "/pt/melhores-cassinos-online-quenia.html"),
            ("Melhores na África do Sul", "/pt/melhores-cassinos-online-africa-do-sul.html"),
            ("Melhores na Índia", "/pt/melhores-cassinos-online-india.html"),
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
            ("PIX no Brasil", "/pt/cassinos-pix-brasil.html"),
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
