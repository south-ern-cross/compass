// Slot RTP database: providers' default (published) RTP figures.
const slotData = [
  {name:"Sweet Bonanza", provider:"Pragmatic Play", rtp:96.51, volatility:"High", maxWin:21100, page:"slots/pragmatic-play/sweet-bonanza.html", img:"/assets/images/slots/pragmatic/sweet-bonanza.jpg"},
  {name:"Gates of Olympus", provider:"Pragmatic Play", rtp:96.50, volatility:"High", maxWin:5000, page:"slots/pragmatic-play/gates-of-olympus.html", img:"/assets/images/slots/pragmatic/gates-of-olympus.jpg"},
  {name:"Wolf Gold", provider:"Pragmatic Play", rtp:96.01, volatility:"Medium", maxWin:5000, page:"slots/pragmatic-play/wolf-gold.html", img:"/assets/images/slots/pragmatic/wolf-gold.jpg"},
  {name:"Book of Dead", provider:"Play'n GO", rtp:96.21, volatility:"High", maxWin:5000, img:"/assets/images/slots/playngo/book-of-dead.jpg"},
  {name:"Starburst", provider:"NetEnt", rtp:96.09, volatility:"Low", maxWin:500, page:"slots/netent/starburst.html", img:"/assets/images/slots/netent/starburst.jpg"},
  {name:"Gonzo's Quest", provider:"NetEnt", rtp:95.97, volatility:"Medium", maxWin:2500, page:"slots/netent/gonzos-quest.html", img:"/assets/images/slots/netent/gonzos-quest.jpg"},
  {name:"Big Bass Bonanza", provider:"Pragmatic Play", rtp:96.71, volatility:"Medium", maxWin:2100, page:"slots/pragmatic-play/big-bass-bonanza.html", img:"/assets/images/slots/pragmatic/big-bass-bonanza.jpg"},
  {name:"Money Train 2", provider:"Relax Gaming", rtp:96.40, volatility:"High", maxWin:50000, page:"slots/relax-gaming/money-train-2.html", img:"/assets/images/slots/relax/money-train-2.jpg"},
];
const LANG = (document.documentElement.lang || 'en').slice(0, 2);
const T = {
  en: {vol:{Low:"Low",Medium:"Medium",High:"High"}, review:"Review", rtp:"RTP", volatility:"Volatility", max:"Max win", none:"No slots match these filters.", summary:(n,a,b)=>`${n} slots · average RTP ${a}% · highest ${b}%`},
  es: {vol:{Low:"Baja",Medium:"Media",High:"Alta"}, review:"Reseña", rtp:"RTP", volatility:"Volatilidad", max:"Ganancia máx.", none:"Ningún juego coincide con estos filtros.", summary:(n,a,b)=>`${n} tragamonedas · RTP medio ${a}% · máximo ${b}%`},
}[LANG] || null;
const L = T || {vol:{Low:"Low",Medium:"Medium",High:"High"}, review:"Review", rtp:"RTP", volatility:"Volatility", max:"Max win", none:"No slots match.", summary:(n,a,b)=>`${n} slots · average RTP ${a}% · highest ${b}%`};
const prefix = LANG === 'es' ? '/es/' : '/';
const fmtX = n => n.toLocaleString('en-US') + 'x';
let sortKey = 'rtp', sortDir = -1;

function thumb(s){
  const initials = s.name.split(/\s+/).map(w => w[0]).join('').slice(0, 3);
  return s.img ? `<img class="rtp-thumb" src="${s.img}" alt="" width="64" height="48" loading="lazy" decoding="async">`
               : `<span class="rtp-thumb rtp-thumb--ph" aria-hidden="true">${initials}</span>`;
}
function nameCell(s){ return s.page ? `<a href="${prefix}${s.page}">${s.name}</a>` : s.name; }
function bar(s){ const w = Math.max(4, Math.min(100, (s.rtp - 94) / 3 * 100)); return `<span class="rtp-val"><b>${s.rtp.toFixed(2)}%</b><span class="rtp-bar"><i style="width:${w}%"></i></span></span>`; }
function vol(s){ return `<span class="vol-pill vol-${s.volatility.toLowerCase()}">${L.vol[s.volatility]}</span>`; }

function render(data){
  const tbody = document.getElementById('rtp-tbody');
  tbody.innerHTML = data.length ? data.map(s => `<tr>
    <td><span class="rtp-slot">${thumb(s)}${nameCell(s)}</span></td><td>${s.provider}</td><td>${bar(s)}</td><td>${vol(s)}</td><td>${fmtX(s.maxWin)}</td>
  </tr>`).join('') : `<tr><td colspan="5">${L.none}</td></tr>`;
  const cards = document.getElementById('rtp-cards');
  if (cards) cards.innerHTML = data.map(s => `<div class="rtp-card">
      <div class="rtp-card-head"><span class="rtp-slot">${thumb(s)}<strong>${nameCell(s)}</strong></span><span class="rtp-card-provider">${s.provider}</span></div>
      <div class="rtp-card-grid">
        <div><span>${L.rtp}</span><b>${s.rtp.toFixed(2)}%</b></div>
        <div><span>${L.volatility}</span><b>${L.vol[s.volatility]}</b></div>
        <div><span>${L.max}</span><b>${fmtX(s.maxWin)}</b></div>
      </div>
    </div>`).join('');
  const sum = document.getElementById('rtp-summary');
  if (sum && data.length) {
    const avg = (data.reduce((a, s) => a + s.rtp, 0) / data.length).toFixed(2);
    sum.textContent = L.summary(data.length, avg, Math.max(...data.map(s => s.rtp)).toFixed(2));
  } else if (sum) sum.textContent = '';
}

function apply(){
  const provider = document.getElementById('f-provider').value;
  const volatility = document.getElementById('f-volatility').value;
  const minRtp = parseFloat(document.getElementById('f-minrtp').value) || 0;
  const order = {Low:1, Medium:2, High:3};
  const data = slotData.filter(s => (provider === 'all' || s.provider === provider) && (volatility === 'all' || s.volatility === volatility) && s.rtp >= minRtp)
    .sort((a, b) => {
      const va = sortKey === 'volatility' ? order[a.volatility] : a[sortKey], vb = sortKey === 'volatility' ? order[b.volatility] : b[sortKey];
      return (typeof va === 'string' ? va.localeCompare(vb) : va - vb) * sortDir;
    });
  render(data);
  document.querySelectorAll('#rtp-head th').forEach(th => th.setAttribute('aria-sort', th.dataset.key === sortKey ? (sortDir > 0 ? 'ascending' : 'descending') : 'none'));
}

document.addEventListener('DOMContentLoaded', () => {
  const keys = ['name', 'provider', 'rtp', 'volatility', 'maxWin'];
  const head = document.querySelector('#rtp-tbody').closest('table').querySelector('thead tr');
  head.id = 'rtp-head';
  head.querySelectorAll('th').forEach((th, i) => {
    th.dataset.key = keys[i];
    const b = document.createElement('button'); b.type = 'button'; b.className = 'th-sort'; b.textContent = th.textContent;
    th.textContent = ''; th.appendChild(b);
    b.addEventListener('click', () => { if (sortKey === keys[i]) sortDir = -sortDir; else { sortKey = keys[i]; sortDir = (keys[i] === 'name' || keys[i] === 'provider') ? 1 : -1; } apply(); });
  });
  ['f-provider', 'f-volatility'].forEach(id => document.getElementById(id).addEventListener('change', apply));
  document.getElementById('f-minrtp').addEventListener('input', apply);
  apply();
});
