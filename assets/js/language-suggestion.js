(() => {
  const root = document.documentElement;
  const button = document.querySelector('.theme-toggle');
  if (!button) return;

  const systemDark = window.matchMedia ? window.matchMedia('(prefers-color-scheme: dark)') : { matches: false };
  let saved;
  try { saved = localStorage.getItem('spinora-theme'); } catch (error) {}
  root.dataset.theme = saved === 'light' || saved === 'dark'
    ? saved : (systemDark.matches ? 'dark' : 'light');

  const syncButton = () => {
    button.setAttribute('aria-pressed', String(root.dataset.theme === 'dark'));
  };
  syncButton();

  button.addEventListener('click', () => {
    root.classList.add('theme-anim');
    void root.offsetWidth;
    root.dataset.theme = root.dataset.theme === 'dark' ? 'light' : 'dark';
    try { localStorage.setItem('spinora-theme', root.dataset.theme); } catch (error) {}
    syncButton();
    setTimeout(() => root.classList.remove('theme-anim'), 420);
  });

  systemDark.addEventListener?.('change', event => {
    try { saved = localStorage.getItem('spinora-theme'); } catch (error) {}
    if (saved === 'light' || saved === 'dark') return;
    root.dataset.theme = event.matches ? 'dark' : 'light';
    syncButton();
  });
})();

(() => {
  const banner = document.getElementById('language-suggestion');
  let dismissed = false;
  try { dismissed = !!sessionStorage.getItem('spinora-language-suggestion-dismissed'); } catch (e) {}
  if (!banner || dismissed) return;
  const current = document.documentElement.lang.slice(0, 2).toLowerCase();
  const preferred = (navigator.languages || [navigator.language || ''])
    .map(value => value.slice(0, 2).toLowerCase())
    .find(value => value === 'es' || value === 'pt');
  if (!preferred || preferred === current) return;
  const alternate = document.querySelector(`link[rel="alternate"][hreflang="${preferred}"]`) ||
    document.querySelector(`link[rel="alternate"][hreflang="${preferred}-BR"]`);
  if (!alternate) return;
  const link = document.getElementById('language-suggestion-link');
  link.href = alternate.href;
  link.textContent = preferred === 'pt' ? 'Disponível em português' : 'Disponible en español';
  banner.hidden = false;
  document.getElementById('language-suggestion-close').addEventListener('click', () => {
    banner.hidden = true;
    try { sessionStorage.setItem('spinora-language-suggestion-dismissed', '1'); } catch (e) {}
  });
})();

// Mobile menu: the button is rendered in the shared header (scripts/apply_layout.py)
(function(){
  function initNav(){
    var btn = document.querySelector('.site-header .nav-toggle');
    var links = document.getElementById('primary-menu');
    if(!btn || !links) return;
    function set(open){
      links.classList.toggle('open', open);
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      btn.setAttribute('aria-label', btn.getAttribute(open ? 'data-label-close' : 'data-label-open') || 'Menu');
      document.documentElement.classList.toggle('menu-open', open);
    }
    btn.addEventListener('click', function(){ set(!links.classList.contains('open')); });
    document.addEventListener('keydown', function(e){
      if(e.key === 'Escape' && links.classList.contains('open')){ set(false); btn.focus(); }
    });
    links.addEventListener('click', function(e){ if(e.target.closest('a')) set(false); });
  }
  if(document.readyState === 'loading') document.addEventListener('DOMContentLoaded', initNav);
  else initNav();
})();

// Slim sticky bar on scroll up (mobile, 25.09.2026)
(function(){
  function initSlimBar(){
    if(window.innerWidth > 768) return;
    if(document.querySelector('.slim-bar')) return;
    var h1 = document.querySelector('main h1');
    var title = h1 ? h1.textContent.trim().substring(0, 30) : 'Top 10 Crypto Casinos';
    // Find the main CTA link (first /go/ link in main)
    var ctaLink = document.querySelector('main a[href^="/go/"]');
    var ctaHref = ctaLink ? ctaLink.getAttribute('href') : '/go/duelbits/';
    var claimLabel = ({es:'Ver oferta', pt:'Ver oferta'})[(document.documentElement.lang||'en').slice(0,2)] || 'Claim';
    var bar = document.createElement('div');
    bar.className = 'slim-bar has-content';
    bar.innerHTML = '<span class="slim-logo">SpinoraWins</span>' +
      '<span class="slim-title">' + title.replace(/</g, '&lt;') + '</span>' +
      '<a class="slim-cta" href="' + ctaHref + '" rel="nofollow sponsored noopener">' + claimLabel + '</a>';
    document.body.appendChild(bar);
    var lastY = window.scrollY || 0;
    var ticking = false;
    function onScroll(){
      var y = window.scrollY || 0;
      // Show when scrolling up and past 400px
      if(y > 400 && y < lastY - 5) bar.classList.add('show');
      else if(y < lastY + 5 || y <= 400) bar.classList.remove('show');
      lastY = y;
      ticking = false;
    }
    window.addEventListener('scroll', function(){
      if(!ticking){ window.requestAnimationFrame(onScroll); ticking = true; }
    }, {passive:true});
  }
  if(document.readyState === 'loading') document.addEventListener('DOMContentLoaded', initSlimBar);
  else initSlimBar();
})();
