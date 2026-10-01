function calcEV(){
  const bonus = Math.max(0, parseFloat(document.getElementById('ev-bonus').value) || 0);
  const multiplier = Math.max(0, parseFloat(document.getElementById('ev-multiplier').value) || 0);
  const contribution = Math.min(Math.max(parseFloat(document.getElementById('ev-contribution').value) || 100, 1), 100);
  const rtp = Math.min(100, Math.max(0, parseFloat(document.getElementById('ev-rtp').value) || 96));

  const totalWagering = bonus * multiplier;
  const effectiveWagering = totalWagering / (contribution / 100);
  const expectedLoss = effectiveWagering * (1 - rtp / 100);
  const ev = bonus - expectedLoss;

  document.getElementById('ev-total').textContent = totalWagering.toLocaleString(undefined, {maximumFractionDigits:2});
  document.getElementById('ev-loss').textContent = expectedLoss.toLocaleString(undefined, {maximumFractionDigits:2});
  const evEl = document.getElementById('ev-value');
  evEl.textContent = (ev < 0 ? '−$' : '$') + Math.abs(ev).toLocaleString(undefined, {maximumFractionDigits:2});

  const verdict = document.getElementById('ev-verdict');
  let label, text, color;
  if (ev > bonus * 0.25) {
    label = 'Worth it';
    text = 'This bonus has a clearly positive expected value — mathematically it is in your favour. Still read the max-bet and game rules before claiming.';
    color = '#4ade80';
  } else if (ev >= -bonus * 0.25) {
    label = 'Marginal';
    text = 'Roughly break-even. Take it only if you enjoy the games anyway — there is no real edge here.';
    color = '#e9b860';
  } else {
    label = 'Trap';
    text = 'Negative expected value: on average you lose the bonus and then some just clearing the wagering. Skip this one.';
    color = '#f87171';
  }
  verdict.innerHTML = '<strong style="color:' + color + ';">' + label + '.</strong> ' + text;

  document.getElementById('ev-result').style.display = 'block';
}
document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('ev-btn').addEventListener('click', calcEV);
});
