var SITE = 'https://gethandycalcs.pages.dev';
var L = {
  en: { bill: 'Bill', tip: 'Tip %', people: 'People', otip: 'Tip', ototal: 'Total', oeach: 'Each pays', other: 'ES', loc: 'en-US',
        links: [['/split-the-bill-calculator/', 'Split with tax →'], ['/tip-pool-calculator/', 'Tip pool by hours →'], ['/', 'All 19 calculators →']] },
  es: { bill: 'Cuenta', tip: 'Propina %', people: 'Personas', otip: 'Propina', ototal: 'Total', oeach: 'Paga cada uno', other: 'EN', loc: 'es-US',
        links: [['/es/calculadora-dividir-la-cuenta/', 'Dividir con impuesto →'], ['/es/calculadora-pozo-de-propinas/', 'Repartir propinas por horas →'], ['/es/', 'Las 19 calculadoras →']] }
};
var lang = (localStorage.getItem('lang') || (navigator.language || 'en').slice(0, 2)) === 'es' ? 'es' : 'en';
function $(id) { return document.getElementById(id); }
function money(x) { return isFinite(x) ? x.toLocaleString(L[lang].loc, { style: 'currency', currency: 'USD' }) : '—'; }
function calc() {
  var b = parseFloat($('bill').value) || 0, t = parseFloat($('tip').value) || 0, p = Math.max(1, Math.round(parseFloat($('people').value) || 1));
  var tip = b * t / 100;
  $('tipv').textContent = money(tip); $('totv').textContent = money(b + tip); $('eachv').textContent = money((b + tip) / p);
  [].forEach.call($('chips').children, function (c) { c.className = +c.dataset.v === t ? 'on' : ''; });
  localStorage.setItem('tip', t);
}
function paint() {
  var s = L[lang];
  $('l-bill').textContent = s.bill; $('l-tip').textContent = s.tip; $('l-people').textContent = s.people;
  $('o-tip').textContent = s.otip; $('o-total').textContent = s.ototal; $('o-each').textContent = s.oeach; $('lang').textContent = s.other;
  $('links').innerHTML = '';
  s.links.forEach(function (l) { var a = document.createElement('a'); a.href = SITE + l[0] + '?utm_source=chrome_ext&utm_medium=extension'; a.target = '_blank'; a.textContent = l[1]; $('links').appendChild(a); });
  calc();
}
[15, 18, 20, 22, 25].forEach(function (v) { var b = document.createElement('button'); b.type = 'button'; b.textContent = v + '%'; b.dataset.v = v; b.onclick = function () { $('tip').value = v; calc(); }; $('chips').appendChild(b); });
if (localStorage.getItem('tip')) $('tip').value = localStorage.getItem('tip');
['bill', 'tip', 'people'].forEach(function (id) { $(id).addEventListener('input', calc); });
$('lang').onclick = function () { lang = lang === 'en' ? 'es' : 'en'; localStorage.setItem('lang', lang); paint(); };
paint();
