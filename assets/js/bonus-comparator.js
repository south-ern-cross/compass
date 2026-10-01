
const bonusData = [
  {casino:"Cloudbet", geo:"Nigeria", type:"Cash Rewards", pct:"\u2014", max:"$2,500", wagering:"None", minDep:"None"},
  {casino:"BitStarz", geo:"Nigeria", type:"Deposit Match + FS", pct:"100%", max:"5 BTC + 180 FS", wagering:"40x", minDep:"$20"},
  {casino:"Cloudbet", geo:"Mexico", type:"Cash Rewards", pct:"\u2014", max:"$2,500", wagering:"None", minDep:"None"},
  {casino:"BitStarz", geo:"Mexico", type:"Deposit Match + FS", pct:"100%", max:"5 BTC + 180 FS", wagering:"40x", minDep:"$20"},
  {casino:"BitStarz", geo:"Colombia", type:"Deposit Match", pct:"100%", max:"$500 + 180 FS", wagering:"40x", minDep:"$20"},
  {casino:"Cloudbet", geo:"Colombia", type:"Cash Rewards", pct:"\u2014", max:"$2,500", wagering:"None", minDep:"None"},
  {casino:"Cloudbet", geo:"Kenya", type:"Cash Rewards", pct:"\u2014", max:"$2,500", wagering:"None", minDep:"None"},
  {casino:"Rollbit", geo:"Kenya", type:"Rakeback", pct:"Boosted", max:"Daily/Weekly", wagering:"0x", minDep:"$10"},
];

function renderBonusTable(geo){
  const tbody = document.getElementById('bonus-tbody');
  const filtered = geo === 'all' ? bonusData : bonusData.filter(b => b.geo === geo);
  tbody.innerHTML = filtered.map(b => `<tr>
    <td>${b.casino}</td><td>${b.geo}</td><td>${b.type}</td><td>${b.pct}</td><td>${b.max}</td><td>${b.wagering}</td><td>${b.minDep}</td>
  </tr>`).join('');
  const cards = document.getElementById('bonus-cards');
  if(cards){
    cards.innerHTML = filtered.map(b => `<div class="bonus-card">
      <div class="bonus-card-head"><strong>${b.casino}</strong><span class="bonus-card-geo">${b.geo}</span></div>
      <div class="bonus-card-type">${b.type}</div>
      <div class="bonus-card-grid">
        <div><span>Match</span><b>${b.pct}</b></div>
        <div><span>Max bonus</span><b>${b.max}</b></div>
        <div><span>Wagering</span><b>${b.wagering}</b></div>
        <div><span>Min deposit</span><b>${b.minDep}</b></div>
      </div>
    </div>`).join('');
  }
}

document.addEventListener('DOMContentLoaded', () => {
  renderBonusTable('all');
  document.getElementById('f-geo').addEventListener('change', (e) => renderBonusTable(e.target.value));
});
