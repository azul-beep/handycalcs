/* Handy Calcs: all calculator logic. Runs 100% in the browser, nothing is sent anywhere. */
(function () {
  var LANG = document.documentElement.lang === 'es' ? 'es' : 'en';
  var LOC = LANG === 'es' ? 'es-US' : 'en-US';
  function T(en, es) { return LANG === 'es' ? es : en; }
  function money(x) {
    if (!isFinite(x)) return '—';
    return x.toLocaleString(LOC, { style: 'currency', currency: 'USD' });
  }
  function num(x, d) {
    if (!isFinite(x)) return '—';
    return x.toLocaleString(LOC, { maximumFractionDigits: d === undefined ? 2 : d });
  }
  function pct(x, d) { return isFinite(x) ? num(x, d === undefined ? 1 : d) + '%' : '—'; }

  // Fractions like "1 1/2", "3/4", "½"
  var UNI = { '¼': .25, '½': .5, '¾': .75, '⅓': 1 / 3, '⅔': 2 / 3, '⅛': .125, '⅜': .375, '⅝': .625, '⅞': .875 };
  function fmtQty(x) {
    if (x <= 0 || !isFinite(x)) return '0';
    var whole = Math.floor(x + 1e-9), frac = x - whole;
    var opts = [[0, ''], [1 / 8, '1/8'], [1 / 4, '1/4'], [1 / 3, '1/3'], [3 / 8, '3/8'], [1 / 2, '1/2'], [5 / 8, '5/8'], [2 / 3, '2/3'], [3 / 4, '3/4'], [7 / 8, '7/8'], [1, '']];
    var best = opts[0], err = 9;
    for (var i = 0; i < opts.length; i++) { var e = Math.abs(frac - opts[i][0]); if (e < err) { err = e; best = opts[i]; } }
    if (err > 0.03) return num(x, 2);
    if (best[0] === 1) return String(whole + 1);
    if (!best[1]) return String(whole);
    return whole ? whole + ' ' + best[1] : best[1];
  }
  // Simpler, robust fraction parser used by the scaler
  function leadQty(line) {
    var s = line.trim(), m;
    if ((m = s.match(/^(\d+)\s+(\d+)\/(\d+)(.*)$/))) return { qty: +m[1] + m[2] / m[3], rest: m[4] };
    if ((m = s.match(/^(\d+)\/(\d+)(.*)$/))) return { qty: m[1] / m[2], rest: m[3] };
    if ((m = s.match(/^(\d+)?\s*([¼½¾⅓⅔⅛⅜⅝⅞])(.*)$/))) return { qty: (m[1] ? +m[1] : 0) + UNI[m[2]], rest: m[3] };
    if ((m = s.match(/^(\d+(?:[.,]\d+)?)(.*)$/))) return { qty: parseFloat(m[1].replace(',', '.')), rest: m[2] };
    return null;
  }

  // Cooking units. Volume in ml, weight in g.
  var VOL = { tsp: 4.92892, tbsp: 14.7868, floz: 29.5735, cup: 236.588, pint: 473.176, quart: 946.353, gallon: 3785.41, ml: 1, l: 1000 };
  var WT = { g: 1, kg: 1000, oz: 28.3495, lb: 453.592 };
  // grams per US cup
  var DENS = { water: 236.6, milk: 242, flour: 125, sugar: 200, brownsugar: 220, powdered: 120, butter: 227, oil: 218, honey: 340, rice: 185, oats: 90, cocoa: 85, salt: 292 };

  var CALCS = {
    tip: function (v) {
      var tip = v.bill * v.tip / 100, total = v.bill + tip, p = Math.max(1, Math.round(v.people || 1));
      return { tipAmt: money(tip), total: money(total), perPerson: money(total / p), tipPerPerson: money(tip / p) };
    },
    split: function (v) {
      var p = Math.max(1, Math.round(v.people || 1));
      var base = v.pretax === 'yes' ? v.subtotal : v.subtotal + v.tax;
      var tip = base * v.tip / 100, total = v.subtotal + v.tax + tip;
      var each = total / p, rounded = Math.ceil(each);
      return { tipAmt: money(tip), total: money(total), each: money(each), rounded: money(rounded) + ' (' + T('extra ', 'sobran ') + money(rounded * p - total) + ')' };
    },
    tipout: function (v) {
      var hrs = String(v.hours || '').split(/[,;\s]+/).map(function (x) { return parseFloat(x.replace(',', '.')); }).filter(function (x) { return x > 0; });
      var pool = v.pool * (v.share / 100), total = 0, i;
      for (i = 0; i < hrs.length; i++) total += hrs[i];
      if (!hrs.length || !total) return { rate: '—', shares: T('Enter the hours of each person.', 'Escribe las horas de cada persona.') };
      var rate = pool / total, out = [];
      for (i = 0; i < hrs.length; i++) out.push(T('Person ', 'Persona ') + (i + 1) + ' (' + num(hrs[i]) + ' h): ' + money(hrs[i] * rate));
      return { shared: money(pool), kept: money(v.pool - pool), rate: money(rate) + T(' per hour', ' por hora'), shares: out.join('\n') };
    },
    menuprice: function (v) {
      var price = v.cost / (v.target / 100), profit = price - v.cost;
      return { price: money(price), rounded: money(Math.ceil(price - 0.99) + 0.99), profit: money(profit), markup: pct((price / v.cost - 1) * 100, 0) };
    },
    foodcost: function (v) {
      var cogs = v.begin + v.purchases - v.end;
      return { cogs: money(cogs), pctOut: pct(cogs / v.sales * 100), verdict: (function (p) {
        if (!isFinite(p)) return '—';
        if (p < 25) return T('Very low: check portion sizes and the inventory count.', 'Muy bajo: revisa porciones y el conteo de inventario.');
        if (p <= 35) return T('Healthy: most restaurants aim for 28%–35%.', 'Sano: la mayoría de los restaurantes apunta a 28%–35%.');
        return T('High: review prices, waste and supplier costs.', 'Alto: revisa precios, desperdicio y proveedores.');
      })(cogs / v.sales * 100) };
    },
    scaler: function (v) {
      var f = v.to / v.from;
      if (!isFinite(f) || f <= 0) return { factor: '—', list: '' };
      var lines = String(v.list || '').split('\n'), out = [];
      for (var i = 0; i < lines.length; i++) {
        var l = lines[i]; if (!l.trim()) continue;
        var q = leadQty(l);
        out.push(q ? fmtQty(q.qty * f) + q.rest : l.trim());
      }
      return { factor: '× ' + num(f, 3), list: out.join('\n') };
    },
    cooking: function (v) {
      var a = v.amount, from = v.from, to = v.to, d = DENS[v.ingredient] || DENS.water, x;
      var gPerMl = d / VOL.cup;
      if (VOL[from] && VOL[to]) x = a * VOL[from] / VOL[to];
      else if (WT[from] && WT[to]) x = a * WT[from] / WT[to];
      else if (VOL[from] && WT[to]) x = a * VOL[from] * gPerMl / WT[to];
      else if (WT[from] && VOL[to]) x = a * WT[from] / gPerMl / VOL[to];
      var mixed = (VOL[from] && WT[to]) || (WT[from] && VOL[to]);
      return { result: num(x, 3) + ' ' + to, note: mixed ? T('Volume ↔ weight uses the density of the ingredient you picked.', 'Volumen ↔ peso usa la densidad del ingrediente que elegiste.') : T('Same type of unit: works for any ingredient.', 'Mismo tipo de unidad: sirve para cualquier ingrediente.') };
    },
    oven: function (v) {
      var c, f;
      if (v.dir === 'f2c') { f = v.temp; c = (f - 32) * 5 / 9; } else { c = v.temp; f = c * 9 / 5 + 32; }
      var gas = c < 135 ? '½' : Math.max(1, Math.min(10, Math.round((c - 121) / 14)));
      return { f: num(f, 0) + ' °F', c: num(c, 0) + ' °C', gas: c < 107 ? '—' : String(gas), fan: num(c - 20, 0) + ' °C' };
    },
    hourly: function (v) {
      var week = v.wage * v.hours, year = week * v.weeks;
      return { weekly: money(week), biweekly: money(week * 2), monthly: money(year / 12), yearly: money(year) };
    },
    salary: function (v) {
      var hourly = v.salary / (v.hours * v.weeks);
      return { hourly: money(hourly), weekly: money(v.salary / v.weeks), monthly: money(v.salary / 12), daily: money(hourly * v.hours / 5) };
    },
    overtime: function (v) {
      var reg = v.rate * v.reg, otRate = v.rate * v.mult, ot = otRate * v.ot;
      return { otRate: money(otRate), regPay: money(reg), otPay: money(ot), total: money(reg + ot) };
    },
    rule503020: function (v) {
      return { needs: money(v.income * .5), wants: money(v.income * .3), savings: money(v.income * .2), yearly: money(v.income * .2 * 12) };
    },
    budget: function (v) {
      var keys = ['housing', 'utilities', 'groceries', 'transport', 'insurance', 'debt', 'childcare', 'other'], spent = 0;
      for (var i = 0; i < keys.length; i++) spent += v[keys[i]] || 0;
      var left = v.income - spent;
      return { spent: money(spent), left: money(left), spentPct: pct(spent / v.income * 100), housingPct: pct(v.housing / v.income * 100) + (v.housing / v.income > .3 ? T(' (above the 30% guideline)', ' (más que el 30% recomendado)') : '') };
    },
    percent: function (v) {
      var a = v.a, b = v.b, r;
      if (v.mode === 'of') r = num(a / 100 * b, 4);
      else if (v.mode === 'is') r = pct(a / b * 100, 2);
      else r = pct((b - a) / Math.abs(a) * 100, 2) + ((b - a) >= 0 ? T(' increase', ' de aumento') : T(' decrease', ' de baja'));
      return { result: r };
    },
    discount: function (v) {
      var save = v.price * v.off / 100, after = v.price - save, tax = after * v.tax / 100;
      return { save: money(save), after: money(after), tax: money(tax), total: money(after + tax) };
    },
    salestax: function (v) {
      if (v.mode === 'add') { var t = v.amount * v.rate / 100; return { tax: money(t), total: money(v.amount + t), pre: money(v.amount) }; }
      var pre = v.amount / (1 + v.rate / 100); return { tax: money(v.amount - pre), total: money(v.amount), pre: money(pre) };
    },
    loan: function (v) {
      var n = v.years * 12, r = v.apr / 100 / 12;
      var pay = r === 0 ? v.amount / n : v.amount * r / (1 - Math.pow(1 + r, -n));
      return { monthly: money(pay), interest: money(pay * n - v.amount), total: money(pay * n) };
    },
    savings: function (v) {
      var bal = v.current, r = v.rate / 100 / 12, m = 0;
      if (v.current >= v.goal) return { months: '0', date: T('You already reached it!', '¡Ya llegaste!'), contrib: money(0) };
      if (v.monthly <= 0 && r <= 0) return { months: '—', date: T('Add a monthly amount.', 'Agrega un monto mensual.'), contrib: '—' };
      while (bal < v.goal && m < 1200) { bal = bal * (1 + r) + v.monthly; m++; }
      if (m >= 1200) return { months: '100+ ' + T('years', 'años'), date: '—', contrib: '—' };
      var d = new Date(); d.setMonth(d.getMonth() + m);
      return { months: m + ' (' + num(m / 12, 1) + T(' years', ' años') + ')', date: d.toLocaleDateString(LOC, { month: 'long', year: 'numeric' }), contrib: money(v.monthly * m) };
    },
    gas: function (v) {
      var miles = v.distance * (v.round === 'yes' ? 2 : 1), gal = miles / v.mpg, cost = gal * v.price, p = Math.max(1, Math.round(v.people || 1));
      return { gallons: num(gal, 1) + ' gal', cost: money(cost), each: money(cost / p) };
    }
  };

  function readForm(form) {
    var v = {};
    var els = form.querySelectorAll('[data-in]');
    for (var i = 0; i < els.length; i++) {
      var el = els[i], k = el.getAttribute('data-in');
      if (el.type === 'number' || el.getAttribute('data-num') === '1') { var x = parseFloat(String(el.value).replace(',', '.')); v[k] = isNaN(x) ? 0 : x; }
      else v[k] = el.value;
    }
    return v;
  }
  function run(form) {
    var fn = CALCS[form.getAttribute('data-calc')];
    if (!fn) return;
    var out = fn(readForm(form));
    for (var k in out) {
      var el = form.parentNode.querySelector('[data-out="' + k + '"]');
      if (el) el.textContent = out[k];
    }
  }
  var forms = document.querySelectorAll('form[data-calc]');
  for (var i = 0; i < forms.length; i++) {
    (function (f) {
      f.addEventListener('input', function () { run(f); });
      f.addEventListener('change', function () { run(f); });
      f.addEventListener('submit', function (e) { e.preventDefault(); run(f); if (window.hcTrack) window.hcTrack(f.getAttribute('data-calc')); });
      run(f);
    })(forms[i]);
  }
  // Copy buttons
  var cps = document.querySelectorAll('[data-copy]');
  for (i = 0; i < cps.length; i++) cps[i].addEventListener('click', function () {
    var t = document.querySelector('[data-out="' + this.getAttribute('data-copy') + '"]');
    if (t && navigator.clipboard) { navigator.clipboard.writeText(t.textContent); this.textContent = T('Copied', 'Copiado'); }
  });
  window.HC_CALCS = CALCS;
})();
