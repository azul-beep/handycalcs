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

  function parseD(s) { var m = String(s || '').match(/^(\d{4})-(\d{2})-(\d{2})$/); return m ? new Date(+m[1], m[2] - 1, +m[3]) : null; }
  function dayDiff(a, b) { return Math.round((Date.UTC(b.getFullYear(), b.getMonth(), b.getDate()) - Date.UTC(a.getFullYear(), a.getMonth(), a.getDate())) / 864e5); }
  // date inputs marked data-today start on the visitor's local date
  (function () { var d = new Date(), iso = d.getFullYear() + '-' + ('0' + (d.getMonth() + 1)).slice(-2) + '-' + ('0' + d.getDate()).slice(-2);
    var t = document.querySelectorAll('input[data-today]'); for (var i = 0; i < t.length; i++) if (!t[i].value) t[i].value = iso; })();

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
    // ---------------- added Nov 2026 ----------------
    mortgage: function (v) {
      var down = v.price * v.down / 100, loan = v.price - down, n = v.years * 12, r = v.rate / 100 / 12;
      var pi = loan <= 0 ? 0 : (r === 0 ? loan / n : loan * r / (1 - Math.pow(1 + r, -n)));
      var tax = v.price * v.taxrate / 100 / 12, ins = v.insurance / 12, pmi = (v.down < 20 && loan > 0) ? loan * v.pmi / 100 / 12 : 0;
      var total = pi + tax + ins + pmi + v.hoa;
      return { monthly: money(total), pi: money(pi), taxes: money(tax) + ' / ' + money(ins), pmiOut: v.down < 20 ? money(pmi) : T('None (20% down or more)', 'No (20% o más de enganche)'),
        loanAmt: money(loan), interest: money(pi * n - loan) };
    },
    compound: function (v) {
      var n = { '1': 1, '4': 4, '12': 12, '365': 365 }[v.freq] || 12, months = Math.round(v.years * 12);
      var mr = Math.pow(1 + v.rate / 100 / n, n / 12) - 1, bal = v.initial;
      for (var i = 0; i < months; i++) bal = bal * (1 + mr) + v.monthly;
      var put = v.initial + v.monthly * months;
      return { fv: money(bal), contrib: money(put), earned: money(bal - put), doubling: v.rate > 0 ? num(72 / v.rate, 1) + T(' years', ' años') : '—' };
    },
    autoloan: function (v) {
      var taxable = Math.max(0, v.price - (v.tradetax === 'yes' ? v.trade : 0)), tax = taxable * v.tax / 100;
      var loan = Math.max(0, v.price + tax + v.fees - v.down - v.trade), n = Math.max(1, +v.months), r = v.apr / 100 / 12;
      var pay = loan <= 0 ? 0 : (r === 0 ? loan / n : loan * r / (1 - Math.pow(1 + r, -n)));
      return { monthly: money(pay), loanAmt: money(loan), salesTax: money(tax), interest: money(pay * n - loan), total: money(pay * n + v.down + v.trade) };
    },
    ccpayoff: function (v) {
      var r = v.apr / 100 / 12, bal = v.balance, m = 0, paid = 0, res = {};
      if (v.payment <= bal * r) res.months = T('Never: the payment does not cover the interest.', 'Nunca: el pago no cubre los intereses.');
      else {
        while (bal > 0.005 && m < 1200) { bal = bal * (1 + r); var p = Math.min(v.payment, bal); bal -= p; paid += p; m++; }
        var d = new Date(); d.setMonth(d.getMonth() + m);
        res.months = m + T(' months', ' meses') + ' (' + d.toLocaleDateString(LOC, { month: 'long', year: 'numeric' }) + ')';
        res.interest = money(paid - v.balance);
      }
      var n = Math.max(1, Math.round(v.target));
      res.needed = money(r === 0 ? v.balance / n : v.balance * r / (1 - Math.pow(1 + r, -n)));
      if (!res.interest) res.interest = '—';
      return res;
    },
    timecard: function (v) {
      function mins(t) { var m = String(t || '').match(/^(\d{1,2}):(\d{2})/); return m ? +m[1] * 60 + +m[2] : null; }
      var days = ['d1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7'], total = 0, lines = [];
      var names = T('Mon,Tue,Wed,Thu,Fri,Sat,Sun', 'Lun,Mar,Mié,Jue,Vie,Sáb,Dom').split(',');
      for (var i = 0; i < days.length; i++) {
        var s = mins(v[days[i] + '_s']), e = mins(v[days[i] + '_e']);
        if (s === null || e === null) continue;
        if (e <= s) e += 1440; // overnight shift
        var w = Math.max(0, e - s - (v[days[i] + '_b'] || 0));
        total += w; lines.push(names[i] + ': ' + Math.floor(w / 60) + 'h ' + ('0' + Math.round(w % 60)).slice(-2) + 'm (' + num(w / 60, 2) + ')');
      }
      var h = total / 60, reg = Math.min(h, 40), ot = Math.max(0, h - 40), pay = reg * v.rate + ot * v.rate * 1.5;
      return { hours: Math.floor(total / 60) + 'h ' + ('0' + Math.round(total % 60)).slice(-2) + 'm (' + num(h, 2) + ' h)', ot: num(ot, 2) + ' h',
        pay: v.rate > 0 ? money(pay) : '—', days: lines.join('\n') || T('Enter at least one start and end time.', 'Escribe al menos una entrada y una salida.') };
    },
    age: function (v) {
      var b = parseD(v.birth), t = parseD(v.asof);
      if (!b || !t || t < b) return { age: '—', total: '—', days: '—', next: '—' };
      var y = t.getFullYear() - b.getFullYear(), m = t.getMonth() - b.getMonth(), d = t.getDate() - b.getDate();
      if (d < 0) { m--; d += new Date(t.getFullYear(), t.getMonth(), 0).getDate(); }
      if (m < 0) { y--; m += 12; }
      var nb = new Date(t.getFullYear(), b.getMonth(), b.getDate()); if (nb < t) nb.setFullYear(t.getFullYear() + 1);
      var dn = dayDiff(t, nb);
      return { age: y + T(' years, ', ' años, ') + m + T(' months, ', ' meses, ') + d + T(' days', ' días'), total: num(y * 12 + m, 0) + T(' months', ' meses'),
        days: num(dayDiff(b, t), 0) + T(' days', ' días'), next: dn === 0 ? T('Today! Happy birthday 🎉', '¡Hoy! Feliz cumpleaños 🎉') : T('In ', 'En ') + dn + T(' days', ' días') };
    },
    datediff: function (v) {
      var a = parseD(v.start), b = parseD(v.end);
      if (!a || !b) return { days: '—', weeks: '—', months: '—', work: '—' };
      var sign = b < a ? -1 : 1; if (sign < 0) { var x = a; a = b; b = x; }
      var d = dayDiff(a, b) + (v.incl === 'yes' ? 1 : 0), w = 0, c = new Date(a);
      for (var i = 0; i < d; i++) { var wd = c.getDay(); if (wd && wd < 6) w++; c.setDate(c.getDate() + 1); }
      var mm = (b.getFullYear() - a.getFullYear()) * 12 + b.getMonth() - a.getMonth(); if (b.getDate() < a.getDate()) mm--;
      return { days: num(d * sign, 0) + T(' days', ' días'), weeks: Math.floor(d / 7) + T(' weeks and ', ' semanas y ') + d % 7 + T(' days', ' días'),
        months: num(mm, 0) + T(' full months', ' meses completos') + ' (' + num(d / 365.2425, 2) + T(' years', ' años') + ')', work: num(w, 0) + T(' weekdays (Mon–Fri)', ' días hábiles (lun–vie)') };
    },
    sqft: function (v) {
      var f = { ft: 1, in: 1 / 144, yd: 9, m: 10.7639 }[v.unit] || 1, area = v.length * v.width * f * Math.max(1, Math.round(v.count || 1));
      var withWaste = area * (1 + v.waste / 100);
      return { area: num(area, 2) + ' sq ft', metric: num(area / 10.7639, 2) + ' m² · ' + num(area / 9, 2) + ' sq yd', buy: num(Math.ceil(withWaste), 0) + ' sq ft',
        cost: v.cost > 0 ? money(Math.ceil(withWaste) * v.cost) : '—' };
    },
    bmi: function (v) {
      var inches = v.ft * 12 + v.inch, bmi = 703 * v.lb / (inches * inches);
      var cat = !isFinite(bmi) || bmi <= 0 ? '—' : bmi < 18.5 ? T('Underweight', 'Bajo peso') : bmi < 25 ? T('Healthy weight', 'Peso saludable') : bmi < 30 ? T('Overweight', 'Sobrepeso') : T('Obesity', 'Obesidad');
      return { bmi: isFinite(bmi) && bmi > 0 ? num(bmi, 1) : '—', cat: cat, range: inches > 0 ? num(18.5 * inches * inches / 703, 0) + '–' + num(24.9 * inches * inches / 703, 0) + ' lb' : '—',
        metric: num(inches * 2.54, 0) + ' cm · ' + num(v.lb * 0.453592, 1) + ' kg' };
    },
    calorie: function (v) {
      var kg = v.lb * 0.453592, cm = (v.ft * 12 + v.inch) * 2.54;
      var bmr = 10 * kg + 6.25 * cm - 5 * v.age + (v.sex === 'm' ? 5 : -161), tdee = bmr * (parseFloat(v.activity) || 1.2);
      var floor = v.sex === 'm' ? 1500 : 1200;
      function cal(x) { return isFinite(x) && x > 0 ? num(Math.round(x / 10) * 10, 0) + T(' calories/day', ' calorías/día') : '—'; }
      function cut(x) { return x < floor ? cal(floor) + T(' (minimum; talk to a doctor)', ' (mínimo; consulta a un médico)') : cal(x); }
      return { tdee: cal(tdee), lose1: cut(tdee - 500), lose05: cut(tdee - 250), gain: cal(tdee + 250), bmr: cal(bmr) };
    },
    gpa: function (v) {
      var P = { 'A+': 4, 'A': 4, 'A-': 3.7, 'B+': 3.3, 'B': 3, 'B-': 2.7, 'C+': 2.3, 'C': 2, 'C-': 1.7, 'D+': 1.3, 'D': 1, 'D-': 0.7, 'F': 0 };
      var lines = String(v.list || '').split('\n'), pts = 0, cr = 0, bad = 0;
      for (var i = 0; i < lines.length; i++) {
        var m = lines[i].trim().toUpperCase().match(/([A-DF][+-]?|\d(?:[.,]\d+)?)\s*[,;\s]\s*(\d+(?:[.,]\d+)?)\s*$/);
        if (!lines[i].trim()) continue;
        if (!m) { bad++; continue; }
        var g = P.hasOwnProperty(m[1]) ? P[m[1]] : parseFloat(m[1].replace(',', '.')), c = parseFloat(m[2].replace(',', '.'));
        if (!isFinite(g) || g > 4.5 || !(c > 0)) { bad++; continue; }
        pts += g * c; cr += c;
      }
      var sem = cr ? pts / cr : NaN, cum = (cr + v.prevcr) ? (pts + v.prevgpa * v.prevcr) / (cr + v.prevcr) : NaN;
      return { gpa: isFinite(sem) ? num(sem, 2) : '—', cum: v.prevcr > 0 && isFinite(cum) ? num(cum, 2) : T('Add previous GPA and credits', 'Agrega tu GPA y créditos anteriores'),
        credits: num(cr, 1) + (bad ? T(' (' + bad + ' line(s) not understood)', ' (' + bad + ' línea(s) sin entender)') : '') };
    },
    finalgrade: function (v) {
      var w = v.weight / 100, need = (v.want - v.current * (1 - w)) / w;
      var note = !isFinite(need) ? '—' : need > 100 ? T('Above 100%: not possible without extra credit.', 'Más de 100%: no alcanza sin puntos extra.') : need <= 0 ? T('You already have it, even with a 0 on the final.', 'Ya lo tienes, aunque saques 0 en el final.') : T('Doable. Good luck!', 'Se puede. ¡Suerte!');
      return { need: isFinite(need) ? pct(need, 1) : '—', note: note, ifzero: pct(v.current * (1 - w), 1), ifhundred: pct(v.current * (1 - w) + 100 * w, 1) };
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
