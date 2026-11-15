/* Handy Calcs online tools. Everything runs in the visitor's browser: no file, text or name is sent anywhere.
   Each widget is <div class="tool" data-tool="ENGINE" data-mode="..."> built by build.py from src/tools.py. */
(function () {
  var ES = document.documentElement.lang === 'es';
  function T(en, es) { return ES ? es : en; }
  function $(root, sel) { return root.querySelector(sel); }
  function $$(root, sel) { return [].slice.call(root.querySelectorAll(sel)); }
  function track(name) { if (window.hcTrack) window.hcTrack(name); }
  function lines(txt) { return txt.split(/\r?\n/).map(function (s) { return s.trim(); }).filter(Boolean); }
  function rnd(n) { var a = new Uint32Array(1); crypto.getRandomValues(a); return a[0] % n; }   // 0..n-1
  function shuffle(a) { a = a.slice(); for (var i = a.length - 1; i > 0; i--) { var j = rnd(i + 1), t = a[i]; a[i] = a[j]; a[j] = t; } return a; }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function fmt(n) { return n.toLocaleString(ES ? 'es-US' : 'en-US'); }
  function kb(b) { return b < 1024 * 1024 ? (b / 1024).toFixed(1) + ' KB' : (b / 1048576).toFixed(2) + ' MB'; }
  function copyBtn(btn, getText) {
    btn.addEventListener('click', function () {
      var t = getText(), done = function () { var o = btn.textContent; btn.textContent = T('Copied!', '¡Copiado!'); setTimeout(function () { btn.textContent = o; }, 1400); };
      if (navigator.clipboard) navigator.clipboard.writeText(t).then(done, done); else { var x = document.createElement('textarea'); x.value = t; document.body.appendChild(x); x.select(); document.execCommand('copy'); x.remove(); done(); }
    });
  }
  function download(name, blobOrUrl) {
    var a = document.createElement('a'); a.download = name;
    a.href = typeof blobOrUrl === 'string' ? blobOrUrl : URL.createObjectURL(blobOrUrl);
    document.body.appendChild(a); a.click(); a.remove();
  }

  var E = {};

  /* ------------------------------------------------------------------ QR codes */
  E.qr = function (el) {
    var mode = el.getAttribute('data-mode') || 'text', box = $(el, '.qr-out'), last = null;
    function val(k) { var i = $(el, '[data-k="' + k + '"]'); return i ? (i.type === 'checkbox' ? i.checked : i.value) : ''; }
    function escWifi(s) { return s.replace(/([\\;,:"])/g, '\\$1'); }
    function payload() {
      if (mode === 'wifi') {
        if (!val('ssid')) return '';
        var sec = val('sec');
        return 'WIFI:T:' + (sec === 'nopass' ? 'nopass' : sec) + ';S:' + escWifi(val('ssid')) + ';' + (sec === 'nopass' ? '' : 'P:' + escWifi(val('pass')) + ';') + (val('hidden') ? 'H:true;' : '') + ';';
      }
      if (mode === 'whatsapp') {
        var ph = val('phone').replace(/\D/g, '');
        if (!ph) return '';
        return 'https://wa.me/' + ph + (val('msg') ? '?text=' + encodeURIComponent(val('msg')) : '');
      }
      return val('text').trim();
    }
    function draw() {
      var data = payload(), size = +val('size') || 300, fg = val('fg') || '#000000', bg = val('bg') || '#ffffff';
      if (!data) { box.innerHTML = '<p class="small">' + T('Type something to create your QR code.', 'Escribe algo para crear tu código QR.') + '</p>'; last = null; return; }
      qrcode.stringToBytes = qrcode.stringToBytesFuncs['UTF-8'];
      var q;
      try { q = qrcode(0, 'M'); q.addData(data, 'Byte'); q.make(); }
      catch (e) { box.innerHTML = '<p class="small">' + T('Too much text for one QR code. Make it shorter.', 'Demasiado texto para un código QR. Acórtalo.') + '</p>'; last = null; return; }
      var n = q.getModuleCount(), quiet = 4, cell = Math.max(1, Math.floor(size / (n + quiet * 2))), px = cell * (n + quiet * 2);
      var c = document.createElement('canvas'); c.width = c.height = px; var g = c.getContext('2d');
      g.fillStyle = bg; g.fillRect(0, 0, px, px); g.fillStyle = fg;
      var path = '';
      for (var r = 0; r < n; r++) for (var k = 0; k < n; k++) if (q.isDark(r, k)) { g.fillRect((k + quiet) * cell, (r + quiet) * cell, cell, cell); path += 'M' + (k + quiet) + ' ' + (r + quiet) + 'h1v1h-1z'; }
      var w = n + quiet * 2;
      var svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ' + w + ' ' + w + '" shape-rendering="crispEdges"><rect width="100%" height="100%" fill="' + bg + '"/><path fill="' + fg + '" d="' + path + '"/></svg>';
      c.className = 'qr-canvas'; c.setAttribute('role', 'img'); c.setAttribute('aria-label', T('QR code', 'Código QR'));
      box.innerHTML = ''; box.appendChild(c); last = { canvas: c, svg: svg };
    }
    $$(el, 'input,textarea,select').forEach(function (i) { i.addEventListener('input', draw); i.addEventListener('change', draw); });
    $(el, '[data-act="png"]').addEventListener('click', function () { if (last) { download('qr-code.png', last.canvas.toDataURL('image/png')); track('qr-png'); } });
    $(el, '[data-act="svg"]').addEventListener('click', function () { if (last) { download('qr-code.svg', new Blob([last.svg], { type: 'image/svg+xml' })); track('qr-svg'); } });
    draw();
  };

  /* ------------------------------------------------------------------ text tools */
  E.words = function (el) {
    var ta = $(el, 'textarea'), out = $(el, '.stats'), kw = $(el, '.kw');
    var STOP = ES ? 'de la que el en y a los se del las un por con no una su para es al lo como más o pero sus le ya fue este ha sí porque esta son entre cuando muy sin sobre también me hasta hay donde quien desde todo nos durante todos uno les ni contra otros ese eso ante ellos e esto mí antes algunos qué unos yo otro otras otra él tanto esa estos mucho quienes nada muchos cual poco ella estar estas algunas algo nosotros mi mis tú te ti tu tus'.split(' ')
      : 'the a an and or but of to in on at for with by from is are was were be been it its this that these those as not no you your we our they their he she his her i me my so if then than there here what which who will would can could should do does did have has had just about into over also'.split(' ');
    function run() {
      var t = ta.value, words = t.match(/[\p{L}\p{N}'’-]+/gu) || [];
      var sent = (t.match(/[^.!?¡¿\n]+[.!?]+/g) || []).length || (words.length ? 1 : 0);
      var paras = t.split(/\n\s*\n/).filter(function (p) { return p.trim(); }).length;
      var stats = [[T('Words', 'Palabras'), fmt(words.length)], [T('Characters', 'Caracteres'), fmt(t.length)],
        [T('Characters without spaces', 'Caracteres sin espacios'), fmt(t.replace(/\s/g, '').length)], [T('Sentences', 'Oraciones'), fmt(sent)],
        [T('Paragraphs', 'Párrafos'), fmt(paras)], [T('Reading time', 'Tiempo de lectura'), Math.max(words.length ? 1 : 0, Math.round(words.length / 230)) + ' min'],
        [T('Speaking time', 'Tiempo para decirlo en voz alta'), Math.max(words.length ? 1 : 0, Math.round(words.length / 140)) + ' min']];
      out.innerHTML = stats.map(function (s, i) { return '<div class="out' + (i === 0 ? ' big' : '') + '"><span>' + s[0] + '</span><strong>' + s[1] + '</strong></div>'; }).join('');
      var freq = {};
      words.forEach(function (w) { w = w.toLowerCase(); if (w.length > 2 && STOP.indexOf(w) < 0) freq[w] = (freq[w] || 0) + 1; });
      var top = Object.keys(freq).sort(function (a, b) { return freq[b] - freq[a]; }).slice(0, 8);
      kw.innerHTML = top.length ? '<h3>' + T('Most used words', 'Palabras más usadas') + '</h3>' + top.map(function (w) { return '<span class="chip">' + esc(w) + ' · ' + freq[w] + '</span>'; }).join(' ') : '';
    }
    ta.addEventListener('input', run); run();
  };

  function smallWords(w, i) { return i > 0 && (ES ? /^(de|del|la|las|el|los|y|o|a|en|con|por|para|un|una)$/ : /^(a|an|the|and|or|but|of|to|in|on|at|for|by|with)$/).test(w); }
  var CASES = {
    upper: function (s) { return s.toUpperCase(); },
    lower: function (s) { return s.toLowerCase(); },
    title: function (s) { return s.toLowerCase().replace(/[\p{L}\p{N}'’]+/gu, function (w, off) { return smallWords(w, off) ? w : w.charAt(0).toUpperCase() + w.slice(1); }); },
    sentence: function (s) { return s.toLowerCase().replace(/(^\s*|[.!?]\s+|\n\s*)([¡¿]?)(\p{L})/gu, function (m, a, b, c) { return a + b + c.toUpperCase(); }); },
    alt: function (s) { var i = 0; return s.replace(/\p{L}/gu, function (c) { return (i++ % 2) ? c.toUpperCase() : c.toLowerCase(); }); },
    invert: function (s) { return s.replace(/\p{L}/gu, function (c) { return c === c.toUpperCase() ? c.toLowerCase() : c.toUpperCase(); }); }
  };
  E.textx = function (el) {   // text in -> transform -> text out (case, accents, line breaks)
    var mode = el.getAttribute('data-mode'), inp = $(el, '[data-k="in"]'), out = $(el, '[data-k="out"]'), cur = 'upper';
    function opt(k) { var i = $(el, '[data-k="' + k + '"]'); return i ? (i.type === 'checkbox' ? i.checked : i.value) : null; }
    function run() {
      var s = inp.value;
      if (mode === 'case') s = CASES[cur](s);
      if (mode === 'accents') {
        var keep = opt('keepn');
        s = s.replace(keep ? /[^ñÑ]/g : /[\s\S]/g, function (c) { return c.normalize('NFD').replace(/[̀-ͯ]/g, ''); });
      }
      if (mode === 'breaks') {
        var how = opt('how');
        if (how === 'empty') s = s.split(/\r?\n/).filter(function (l) { return l.trim(); }).join('\n');
        else if (how === 'para') s = s.split(/\n\s*\n/).map(function (p) { return p.replace(/\s*\r?\n\s*/g, ' ').trim(); }).filter(Boolean).join('\n\n');
        else s = s.replace(/\s*\r?\n\s*/g, ' ').trim();
        if (opt('spaces')) s = s.replace(/[ \t]{2,}/g, ' ');
      }
      out.value = s;
    }
    $$(el, '[data-case]').forEach(function (b) { b.addEventListener('click', function () { cur = b.getAttribute('data-case'); $$(el, '[data-case]').forEach(function (x) { x.classList.toggle('on', x === b); }); run(); track('case-' + cur); }); });
    $$(el, 'input,select,textarea').forEach(function (i) { if (i !== out) { i.addEventListener('input', run); i.addEventListener('change', run); } });
    copyBtn($(el, '[data-act="copy"]'), function () { return out.value; });
    run();
  };

  var LATIN = 'lorem ipsum dolor sit amet consectetur adipiscing elit sed do eiusmod tempor incididunt ut labore et dolore magna aliqua enim ad minim veniam quis nostrud exercitation ullamco laboris nisi aliquip ex ea commodo consequat duis aute irure in reprehenderit voluptate velit esse cillum fugiat nulla pariatur excepteur sint occaecat cupidatat non proident sunt culpa qui officia deserunt mollit anim id est laborum'.split(' ');
  var SPAN = 'el texto de relleno sirve para ver cómo queda un diseño antes de tener las palabras finales una página web un folleto o una tarjeta se ven mejor cuando el espacio está lleno con frases que parecen reales pero no distraen al lector la tipografía el tamaño y el color se pueden probar con calma mientras se escribe el contenido definitivo cada párrafo cambia de largo para que la prueba sea más natural'.split(' ');
  E.lorem = function (el) {
    var out = $(el, '[data-k="out"]');
    function sentence(bank) { var n = 8 + rnd(9), w = []; for (var i = 0; i < n; i++) w.push(bank[rnd(bank.length)]); var s = w.join(' '); return s.charAt(0).toUpperCase() + s.slice(1) + '.'; }
    function run() {
      var bank = $(el, '[data-k="lang"]').value === 'es' ? SPAN : LATIN, n = Math.min(50, Math.max(1, +$(el, '[data-k="n"]').value || 3)), unit = $(el, '[data-k="unit"]').value, res = [];
      if (unit === 'words') { var w = []; for (var i = 0; i < n * 10; i++) w.push(bank[rnd(bank.length)]); res = [w.join(' ')]; }
      else if (unit === 'sentences') { var s = []; for (var j = 0; j < n; j++) s.push(sentence(bank)); res = [s.join(' ')]; }
      else for (var p = 0; p < n; p++) { var ss = []; for (var k = 0; k < 4 + rnd(4); k++) ss.push(sentence(bank)); res.push(ss.join(' ')); }
      if (bank === LATIN && $(el, '[data-k="start"]').checked) res[0] = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. ' + res[0];
      out.value = res.join('\n\n');
    }
    $(el, '[data-act="gen"]').addEventListener('click', function () { run(); track('lorem'); });
    $$(el, 'select,input').forEach(function (i) { i.addEventListener('change', run); });
    copyBtn($(el, '[data-act="copy"]'), function () { return out.value; });
    run();
  };

  /* ------------------------------------------------------------------ images (compress, resize, convert) */
  E.img = function (el) {
    var mode = el.getAttribute('data-mode'), file = $(el, 'input[type=file]'), list = $(el, '.img-list'), drop = $(el, '.drop');
    function opt(k) { var i = $(el, '[data-k="' + k + '"]'); return i ? (i.type === 'checkbox' ? i.checked : i.value) : null; }
    var q = $(el, '[data-k="quality"]'), qv = $(el, '.qv');
    if (q) q.addEventListener('input', function () { qv.textContent = q.value + '%'; });
    var w = $(el, '[data-k="w"]'), h = $(el, '[data-k="h"]');
    $$(el, '[data-size]').forEach(function (b) { b.addEventListener('click', function () { var s = b.getAttribute('data-size').split('x'); w.value = s[0]; h.value = s[1]; $(el, '[data-k="fit"]').value = 'cover'; }); });
    function toBlob(c, type, qual) { return new Promise(function (ok) { c.toBlob(ok, type, qual); }); }
    function load(f) {
      return new Promise(function (ok, bad) {
        var u = URL.createObjectURL(f), im = new Image();
        im.onload = function () { ok(im); }; im.onerror = function () { bad(new Error('read')); }; im.src = u;
      });
    }
    function canvasFor(im, tw, th, fit, type) {
      var c = document.createElement('canvas'), g = c.getContext('2d'), sw = im.naturalWidth, sh = im.naturalHeight;
      c.width = tw; c.height = th;
      if (type === 'image/jpeg') { g.fillStyle = '#ffffff'; g.fillRect(0, 0, tw, th); }
      g.imageSmoothingQuality = 'high';
      if (fit === 'cover') { var r = Math.max(tw / sw, th / sh), cw = tw / r, ch = th / r; g.drawImage(im, (sw - cw) / 2, (sh - ch) / 2, cw, ch, 0, 0, tw, th); }
      else if (fit === 'contain') { var r2 = Math.min(tw / sw, th / sh), dw = sw * r2, dh = sh * r2; if (type !== 'image/jpeg') g.clearRect(0, 0, tw, th); g.drawImage(im, (tw - dw) / 2, (th - dh) / 2, dw, dh); }
      else g.drawImage(im, 0, 0, tw, th);
      return c;
    }
    async function one(f) {
      var row = document.createElement('div'); row.className = 'img-row'; row.innerHTML = '<span>' + esc(f.name) + '</span><span class="small">' + T('Working…', 'Procesando…') + '</span>'; list.appendChild(row);
      try {
        var im = await load(f), sw = im.naturalWidth, sh = im.naturalHeight, tw = sw, th = sh, fit = 'stretch';
        var type = opt('format') || 'keep';
        if (type === 'keep') type = /png/.test(f.type) ? 'image/png' : /webp/.test(f.type) ? 'image/webp' : 'image/jpeg';
        if (mode === 'compress') {
          var mw = +opt('maxw'); if (mw && sw > mw) { tw = mw; th = Math.round(sh * mw / sw); }
        }
        if (mode === 'resize') {
          var W = +w.value, H = +h.value; fit = opt('fit');
          if (W && !H) { tw = W; th = Math.round(sh * W / sw); fit = 'stretch'; }
          else if (H && !W) { th = H; tw = Math.round(sw * H / sh); fit = 'stretch'; }
          else if (W && H) { tw = W; th = H; }
          var pct = +opt('pct'); if (!W && !H && pct) { tw = Math.round(sw * pct / 100); th = Math.round(sh * pct / 100); }
        }
        var c = canvasFor(im, tw, th, fit, type), blob, qual = q ? q.value / 100 : 0.92;
        var target = mode === 'compress' ? +opt('target') * 1024 : 0;
        if (target && type !== 'image/png') {   // binary search the quality that fits the target size
          var lo = 0.05, hi = 0.95, best = null;
          for (var i = 0; i < 8; i++) { var mid = (lo + hi) / 2, b = await toBlob(c, type, mid); if (b.size <= target) { best = b; lo = mid; } else hi = mid; }
          var scale = 0.85;
          while (!best && tw > 200) { tw = Math.round(tw * scale); th = Math.round(th * scale); c = canvasFor(im, tw, th, fit, type); var b2 = await toBlob(c, type, 0.6); if (b2.size <= target) best = b2; }
          blob = best || await toBlob(c, type, 0.5);
        } else blob = await toBlob(c, type, qual);
        if (mode === 'compress' && blob.size >= f.size && tw === sw && f.type === type) blob = f;   // already as small as it gets: keep the original
        var ext = type === 'image/png' ? 'png' : type === 'image/webp' ? 'webp' : 'jpg';
        var name = f.name.replace(/\.[^.]+$/, '') + (mode === 'resize' ? '-' + tw + 'x' + th : mode === 'compress' ? '-small' : '') + '.' + ext;
        var saved = f.size ? Math.round((1 - blob.size / f.size) * 100) : 0;
        var url = URL.createObjectURL(blob);
        row.innerHTML = '<img src="' + url + '" alt=""><span><strong>' + esc(name) + '</strong><br><span class="small">' + sw + '×' + sh + ' → ' + tw + '×' + th + ' · ' + kb(f.size) + ' → ' + kb(blob.size) +
          (saved > 0 ? ' (−' + saved + '%)' : '') + '</span></span><a class="btn" download="' + esc(name) + '" href="' + url + '">' + T('Download', 'Descargar') + '</a>';
        track('img-' + mode);
      } catch (e) {
        row.innerHTML = '<span>' + esc(f.name) + '</span><span class="small">' + T('This file could not be opened. Try a JPG, PNG or WebP image.', 'No se pudo abrir este archivo. Prueba con una imagen JPG, PNG o WebP.') + '</span>';
      }
    }
    async function handle(files) { list.innerHTML = ''; for (var i = 0; i < files.length && i < 30; i++) await one(files[i]); }
    file.addEventListener('change', function () { handle(file.files); });
    $(el, '[data-act="redo"]').addEventListener('click', function () { if (file.files.length) handle(file.files); });
    ['dragover', 'dragenter'].forEach(function (ev) { drop.addEventListener(ev, function (e) { e.preventDefault(); drop.classList.add('over'); }); });
    ['dragleave', 'drop'].forEach(function (ev) { drop.addEventListener(ev, function () { drop.classList.remove('over'); }); });
    drop.addEventListener('drop', function (e) { e.preventDefault(); if (e.dataTransfer.files.length) handle(e.dataTransfer.files); });
  };

  /* ------------------------------------------------------------------ random tools */
  E.wheel = function (el) {
    var ta = $(el, 'textarea'), cv = $(el, 'canvas'), g = cv.getContext('2d'), res = $(el, '.wheel-res'), angle = 0, spinning = false;
    var COLORS = ['#0f766e', '#fb923c', '#2563eb', '#db2777', '#65a30d', '#9333ea', '#ca8a04', '#0891b2', '#dc2626', '#4f46e5'];
    function names() { return lines(ta.value).slice(0, 200); }
    function draw() {
      var n = names(), W = cv.width, R = W / 2 - 6;
      g.clearRect(0, 0, W, W);
      if (!n.length) return;
      var step = Math.PI * 2 / n.length;
      for (var i = 0; i < n.length; i++) {
        var a0 = angle + i * step;
        g.beginPath(); g.moveTo(W / 2, W / 2); g.arc(W / 2, W / 2, R, a0, a0 + step); g.closePath();
        g.fillStyle = COLORS[i % COLORS.length]; if (n.length % COLORS.length === 1 && i === n.length - 1) g.fillStyle = COLORS[1]; g.fill();
        g.save(); g.translate(W / 2, W / 2); g.rotate(a0 + step / 2); g.fillStyle = '#fff';
        g.font = 'bold ' + Math.max(11, Math.min(22, 260 / n.length + 8)) + 'px system-ui,sans-serif'; g.textAlign = 'right'; g.textBaseline = 'middle';
        var label = n[i].length > 18 ? n[i].slice(0, 17) + '…' : n[i]; g.fillText(label, R - 12, 0); g.restore();
      }
      g.beginPath(); g.arc(W / 2, W / 2, 22, 0, Math.PI * 2); g.fillStyle = '#fff'; g.fill();
      g.beginPath(); g.moveTo(W - 2, W / 2 - 14); g.lineTo(W - 2, W / 2 + 14); g.lineTo(W - 34, W / 2); g.closePath(); g.fillStyle = '#1c2321'; g.fill();
    }
    function spin() {
      var n = names(); if (spinning || n.length < 2) { if (n.length < 2) res.textContent = T('Add at least 2 names.', 'Agrega al menos 2 nombres.'); return; }
      spinning = true; res.textContent = '';
      var winner = rnd(n.length), step = Math.PI * 2 / n.length;
      // the pointer is at angle 0 (right side). Final angle puts the middle of the winner slice there.
      var target = -(winner * step + step / 2) + (Math.random() - 0.5) * step * 0.7;
      var start = angle, end = start - (((start - target) % (Math.PI * 2)) + Math.PI * 2) % (Math.PI * 2) - Math.PI * 2 * (6 + rnd(3));
      var t0 = performance.now(), dur = 4200;
      (function frame(now) {
        var p = Math.min(1, (now - t0) / dur), e = 1 - Math.pow(1 - p, 3);
        angle = start + (end - start) * e; draw();
        if (p < 1) return requestAnimationFrame(frame);
        spinning = false;
        res.innerHTML = '🎉 <strong>' + esc(n[winner]) + '</strong>';
        track('wheel');
        if ($(el, '[data-k="remove"]').checked) { var all = lines(ta.value); all.splice(winner, 1); ta.value = all.join('\n'); angle = 0; setTimeout(draw, 1200); }
      })(t0);
    }
    $(el, '[data-act="spin"]').addEventListener('click', spin);
    cv.addEventListener('click', spin);
    $(el, '[data-act="shuffle"]').addEventListener('click', function () { ta.value = shuffle(lines(ta.value)).join('\n'); draw(); });
    ta.addEventListener('input', draw); draw();
  };

  E.teams = function (el) {
    var ta = $(el, 'textarea'), out = $(el, '.teams-out');
    function run() {
      var n = shuffle(lines(ta.value)), by = $(el, '[data-k="by"]').value, k = Math.max(1, +$(el, '[data-k="n"]').value || 2);
      if (n.length < 2) { out.innerHTML = '<p class="small">' + T('Add at least 2 names, one per line.', 'Agrega al menos 2 nombres, uno por línea.') + '</p>'; return; }
      var teams = by === 'teams' ? Math.min(k, n.length) : Math.max(1, Math.ceil(n.length / k)), g = [];
      for (var i = 0; i < teams; i++) g.push([]);
      n.forEach(function (x, i) { g[i % teams].push(x); });
      out.innerHTML = g.map(function (t, i) { return '<div class="team"><h3>' + T('Team ', 'Equipo ') + (i + 1) + ' <span class="small">(' + t.length + ')</span></h3><ol>' + t.map(function (x) { return '<li>' + esc(x) + '</li>'; }).join('') + '</ol></div>'; }).join('');
      track('teams');
    }
    $(el, '[data-act="go"]').addEventListener('click', run);
    copyBtn($(el, '[data-act="copy"]'), function () { return $$(out, '.team').map(function (t) { return $(t, 'h3').textContent + '\n' + $$(t, 'li').map(function (l) { return '- ' + l.textContent; }).join('\n'); }).join('\n\n'); });
  };

  E.giveaway = function (el) {
    var ta = $(el, 'textarea[data-k="entries"]'), out = $(el, '.give-out');
    function user(line) { var m = line.match(/@[\w.]+/); return (m ? m[0] : line.split(/\s+/)[0]).toLowerCase(); }
    function run() {
      var raw = lines(ta.value), excl = lines($(el, '[data-k="exclude"]').value).map(function (x) { return x.toLowerCase().replace(/^@?/, '@'); });
      var minTags = +$(el, '[data-k="tags"]').value || 0, unique = $(el, '[data-k="unique"]').checked, seen = {}, pool = [];
      raw.forEach(function (l) {
        var u = user(l), uu = u.replace(/^@?/, '@');
        if (excl.indexOf(uu) > -1) return;
        if (minTags && ((l.match(/@[\w.]+/g) || []).length - (/^@/.test(l.trim()) ? 1 : 0)) < minTags) return;
        if (unique) { if (seen[u]) return; seen[u] = 1; }
        pool.push(l);
      });
      var w = Math.max(1, +$(el, '[data-k="winners"]').value || 1), alt = Math.max(0, +$(el, '[data-k="alts"]').value || 0);
      if (!pool.length) { out.innerHTML = '<p class="small">' + T('No valid entries yet. Paste one comment or name per line.', 'Todavía no hay participantes válidos. Pega un comentario o nombre por línea.') + '</p>'; return; }
      var s = shuffle(pool), now = new Date().toLocaleString(ES ? 'es-US' : 'en-US');
      out.innerHTML = '<p class="small">' + T('Valid entries: ', 'Participantes válidos: ') + fmt(pool.length) + ' · ' + now + '</p><h3>' + T('Winners', 'Ganadores') + '</h3><ol class="win">' + s.slice(0, w).map(function (x) { return '<li>' + esc(x) + '</li>'; }).join('') + '</ol>' +
        (alt ? '<h3>' + T('Alternates', 'Suplentes') + '</h3><ol>' + s.slice(w, w + alt).map(function (x) { return '<li>' + esc(x) + '</li>'; }).join('') + '</ol>' : '');
      track('giveaway');
    }
    $(el, '[data-act="go"]').addEventListener('click', run);
  };

  E.randnum = function (el) {
    var out = $(el, '.rn-out');
    $(el, '[data-act="go"]').addEventListener('click', function () {
      var a = Math.ceil(+$(el, '[data-k="min"]').value), b = Math.floor(+$(el, '[data-k="max"]').value), n = Math.min(1000, Math.max(1, +$(el, '[data-k="n"]').value || 1)), uniq = $(el, '[data-k="unique"]').checked;
      if (isNaN(a) || isNaN(b) || b < a) { out.innerHTML = '<p class="small">' + T('The maximum must be bigger than the minimum.', 'El máximo tiene que ser mayor que el mínimo.') + '</p>'; return; }
      var span = b - a + 1, r = [];
      if (uniq && n > span) n = span;
      if (uniq) { var seen = {}; while (r.length < n) { var x = a + rnd(span); if (!seen[x]) { seen[x] = 1; r.push(x); } } }
      else for (var i = 0; i < n; i++) r.push(a + rnd(span));
      if ($(el, '[data-k="sort"]').checked) r.sort(function (x, y) { return x - y; });
      out.innerHTML = '<div class="big-num' + (r.length > 1 ? ' many' : '') + '">' + r.map(fmt).join(r.length > 1 ? ', ' : '') + '</div>';
      track('randnum');
    });
  };

  E.coin = function (el) {
    var coin = $(el, '.coin'), res = $(el, '.coin-res'), hist = $(el, '.coin-hist'), h = 0, t = 0;
    $(el, '[data-act="go"]').addEventListener('click', function () {
      var heads = rnd(2) === 0;
      coin.classList.remove('flip-h', 'flip-t'); void coin.offsetWidth; coin.classList.add(heads ? 'flip-h' : 'flip-t');
      res.textContent = '';
      setTimeout(function () {
        heads ? h++ : t++;
        res.textContent = heads ? T('Heads', 'Cara') : T('Tails', 'Cruz');
        hist.textContent = T('Heads', 'Cara') + ': ' + h + ' · ' + T('Tails', 'Cruz') + ': ' + t;
      }, 1000);
      track('coin');
    });
  };

  var PIPS = { 1: [4], 2: [0, 8], 3: [0, 4, 8], 4: [0, 2, 6, 8], 5: [0, 2, 4, 6, 8], 6: [0, 2, 3, 5, 6, 8] };
  E.dice = function (el) {
    var out = $(el, '.dice-out'), tot = $(el, '.dice-total');
    function face(v, sides) {
      if (sides === 6) { var p = ''; for (var i = 0; i < 9; i++) p += '<i' + (PIPS[v].indexOf(i) > -1 ? ' class="on"' : '') + '></i>'; return '<div class="die d6" aria-label="' + v + '">' + p + '</div>'; }
      return '<div class="die dn"><b>' + v + '</b><small>d' + sides + '</small></div>';
    }
    $(el, '[data-act="go"]').addEventListener('click', function () {
      var n = Math.min(10, Math.max(1, +$(el, '[data-k="n"]').value || 1)), sides = +$(el, '[data-k="sides"]').value || 6, r = [];
      for (var i = 0; i < n; i++) r.push(1 + rnd(sides));
      out.classList.remove('roll'); void out.offsetWidth; out.classList.add('roll');
      out.innerHTML = r.map(function (v) { return face(v, sides); }).join('');
      tot.textContent = n > 1 ? T('Total: ', 'Total: ') + r.reduce(function (a, b) { return a + b; }, 0) : '';
      track('dice');
    });
  };

  E.password = function (el) {
    var out = $(el, '.pw-out'), len = $(el, '[data-k="len"]'), lv = $(el, '.lv');
    var SETS = { lower: 'abcdefghijklmnopqrstuvwxyz', upper: 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', digits: '0123456789', symbols: '!@#$%^&*()-_=+[]{};:,.?/' };
    function on(k) { return $(el, '[data-k="' + k + '"]').checked; }
    function gen() {
      var L = +len.value, sets = Object.keys(SETS).filter(on).map(function (k) { var s = SETS[k]; return on('ambig') ? s.replace(/[Il1O0o]/g, '') : s; });
      lv.textContent = L;
      if (!sets.length) { out.innerHTML = '<p class="small">' + T('Pick at least one type of character.', 'Elige al menos un tipo de carácter.') + '</p>'; return; }
      var all = sets.join(''), bits = Math.round(L * Math.log2(all.length)), n = Math.min(10, +$(el, '[data-k="count"]').value || 1), html = '';
      for (var j = 0; j < n; j++) {
        var p = sets.map(function (s) { return s[rnd(s.length)]; });   // at least one of each chosen type
        while (p.length < L) p.push(all[rnd(all.length)]);
        p = shuffle(p).slice(0, L).join('');
        html += '<div class="pw"><code>' + esc(p) + '</code><button type="button" class="btn-ghost" data-pw="' + esc(p) + '">' + T('Copy', 'Copiar') + '</button></div>';
      }
      var lvl = bits < 50 ? T('Weak', 'Débil') : bits < 75 ? T('Good', 'Buena') : bits < 100 ? T('Strong', 'Fuerte') : T('Very strong', 'Muy fuerte');
      out.innerHTML = html + '<p class="small">' + T('Strength: ', 'Seguridad: ') + '<strong>' + lvl + '</strong> (' + bits + ' bits)</p>';
      $$(out, '[data-pw]').forEach(function (b) { copyBtn(b, function () { return b.getAttribute('data-pw'); }); });
    }
    $$(el, 'input').forEach(function (i) { i.addEventListener('input', gen); });
    $(el, '[data-act="go"]').addEventListener('click', function () { gen(); track('password'); });
    gen();
  };

  E.timer = function (el) {
    var disp = $(el, '.t-disp'), mode = 'down', left = 0, total = 0, startAt = 0, elapsed = 0, run = null, ac = null;
    function pad(n) { return (n < 10 ? '0' : '') + n; }
    function show(ms) { var s = Math.ceil(ms / 1000); if (mode === 'up') s = Math.floor(ms / 1000); var hh = Math.floor(s / 3600), mm = Math.floor(s % 3600 / 60), ss = s % 60; disp.textContent = (hh ? hh + ':' : '') + pad(mm) + ':' + pad(ss) + (mode === 'up' ? '.' + Math.floor(ms % 1000 / 100) : ''); document.title = disp.textContent + ' · ' + document.title.replace(/^[\d:.]+ · /, ''); }
    function beep() {
      try { ac = ac || new (window.AudioContext || window.webkitAudioContext)(); for (var i = 0; i < 3; i++) { var o = ac.createOscillator(), g = ac.createGain(); o.frequency.value = 880; o.connect(g); g.connect(ac.destination); g.gain.setValueAtTime(0.3, ac.currentTime + i * 0.5); g.gain.setValueAtTime(0, ac.currentTime + i * 0.5 + 0.3); o.start(ac.currentTime + i * 0.5); o.stop(ac.currentTime + i * 0.5 + 0.32); } } catch (e) {}
    }
    function tick() {
      var now = performance.now();
      if (mode === 'down') { var l = left - (now - startAt); if (l <= 0) { stop(); left = 0; show(0); disp.classList.add('done'); beep(); if (navigator.vibrate) navigator.vibrate([300, 150, 300]); return; } show(l); }
      else show(elapsed + now - startAt);
    }
    function start() {
      if (run) return;
      try { ac = ac || new (window.AudioContext || window.webkitAudioContext)(); } catch (e) {}
      if (mode === 'down' && !left) { total = left = ((+$(el, '[data-k="h"]').value || 0) * 3600 + (+$(el, '[data-k="m"]').value || 0) * 60 + (+$(el, '[data-k="s"]').value || 0)) * 1000; if (!left) return; }
      disp.classList.remove('done'); startAt = performance.now(); run = setInterval(tick, 100); track('timer-' + mode);
    }
    function stop() { if (!run) return; clearInterval(run); run = null; var now = performance.now(); if (mode === 'down') left -= now - startAt; else elapsed += now - startAt; }
    function reset() { stop(); left = 0; elapsed = 0; disp.classList.remove('done'); show(mode === 'down' ? ((+$(el, '[data-k="m"]').value || 0) * 60 + (+$(el, '[data-k="s"]').value || 0) + (+$(el, '[data-k="h"]').value || 0) * 3600) * 1000 : 0); }
    $(el, '[data-act="start"]').addEventListener('click', start);
    $(el, '[data-act="pause"]').addEventListener('click', stop);
    $(el, '[data-act="reset"]').addEventListener('click', reset);
    $(el, '[data-act="full"]').addEventListener('click', function () { var b = $(el, '.t-box'); if (b.requestFullscreen) b.requestFullscreen(); });
    $$(el, '[data-min]').forEach(function (b) { b.addEventListener('click', function () { $(el, '[data-k="h"]').value = 0; $(el, '[data-k="m"]').value = b.getAttribute('data-min'); $(el, '[data-k="s"]').value = 0; reset(); start(); }); });
    $$(el, '[data-mode-btn]').forEach(function (b) { b.addEventListener('click', function () { mode = b.getAttribute('data-mode-btn'); $$(el, '[data-mode-btn]').forEach(function (x) { x.classList.toggle('on', x === b); }); $(el, '.t-set').hidden = mode !== 'down'; reset(); }); });
    $$(el, '.t-set input').forEach(function (i) { i.addEventListener('input', function () { if (!run) reset(); }); });
    reset();
  };

  /* ------------------------------------------------------------------ unit converter */
  var UNITS = {
    length: { m: 1, km: 1000, cm: 0.01, mm: 0.001, mi: 1609.344, yd: 0.9144, ft: 0.3048, 'in': 0.0254, nmi: 1852 },
    weight: { kg: 1, g: 0.001, mg: 1e-6, lb: 0.45359237, oz: 0.028349523125, st: 6.35029318, t: 1000, 'US ton': 907.18474 },
    volume: { L: 1, mL: 0.001, 'm³': 1000, 'US gal': 3.785411784, 'US qt': 0.946352946, 'US pt': 0.473176473, 'US cup': 0.2365882365, 'US fl oz': 0.0295735295625, tbsp: 0.01478676478125, tsp: 0.00492892159375, 'UK gal': 4.54609 },
    area: { 'm²': 1, 'km²': 1e6, 'cm²': 1e-4, ha: 1e4, acre: 4046.8564224, 'ft²': 0.09290304, 'yd²': 0.83612736, 'in²': 0.00064516, 'mi²': 2589988.110336 },
    speed: { 'km/h': 1, 'mph': 1.609344, 'm/s': 3.6, knot: 1.852, 'ft/s': 1.09728 },
    temp: { '°C': 'c', '°F': 'f', K: 'k' },
    data: { B: 1, KB: 1e3, MB: 1e6, GB: 1e9, TB: 1e12, KiB: 1024, MiB: 1048576, GiB: 1073741824 }
  };
  function toC(v, u) { return u === 'c' ? v : u === 'f' ? (v - 32) * 5 / 9 : v - 273.15; }
  function fromC(v, u) { return u === 'c' ? v : u === 'f' ? v * 9 / 5 + 32 : v + 273.15; }
  function nice(x) { if (!isFinite(x)) return '—'; var a = Math.abs(x); return a !== 0 && (a < 1e-4 || a >= 1e12) ? x.toExponential(4) : (+x.toPrecision(8)).toLocaleString(ES ? 'es-US' : 'en-US', { maximumFractionDigits: 8 }); }
  E.units = function (el) {
    var cat = $(el, '[data-k="cat"]'), from = $(el, '[data-k="from"]'), to = $(el, '[data-k="to"]'), v = $(el, '[data-k="v"]'), out = $(el, '.u-out'), all = $(el, '.u-all');
    var DEF = { length: ['ft', 'm'], weight: ['lb', 'kg'], volume: ['US cup', 'mL'], area: ['ft²', 'm²'], speed: ['mph', 'km/h'], temp: ['°F', '°C'], data: ['GB', 'MB'] };
    function fill() {
      var u = Object.keys(UNITS[cat.value]), o = u.map(function (k) { return '<option>' + k + '</option>'; }).join('');
      from.innerHTML = o; to.innerHTML = o; from.value = DEF[cat.value][0]; to.value = DEF[cat.value][1]; run();
    }
    function conv(x, a, b) {
      var U = UNITS[cat.value];
      if (cat.value === 'temp') return fromC(toC(x, U[a]), U[b]);
      return x * U[a] / U[b];
    }
    function run() {
      var x = parseFloat(v.value);
      if (isNaN(x)) { out.textContent = '—'; all.innerHTML = ''; return; }
      out.textContent = nice(conv(x, from.value, to.value)) + ' ' + to.value;
      all.innerHTML = Object.keys(UNITS[cat.value]).filter(function (k) { return k !== from.value; }).map(function (k) { return '<div class="out"><span>' + k + '</span><strong>' + nice(conv(x, from.value, k)) + '</strong></div>'; }).join('');
    }
    cat.addEventListener('change', fill);
    [from, to, v].forEach(function (i) { i.addEventListener('input', run); i.addEventListener('change', run); });
    $(el, '[data-act="swap"]').addEventListener('click', function () { var a = from.value; from.value = to.value; to.value = a; run(); });
    var pre = el.getAttribute('data-mode'); if (pre && UNITS[pre]) cat.value = pre;
    fill();
  };

  /* ------------------------------------------------------------------ time zone converter */
  E.tz = function (el) {
    var ZONES = ['America/Los_Angeles', 'America/Denver', 'America/Phoenix', 'America/Chicago', 'America/New_York', 'America/Anchorage', 'Pacific/Honolulu', 'America/Puerto_Rico',
      'America/Mexico_City', 'America/Tijuana', 'America/Cancun', 'America/Guatemala', 'America/El_Salvador', 'America/Tegucigalpa', 'America/Costa_Rica', 'America/Panama',
      'America/Bogota', 'America/Lima', 'America/Caracas', 'America/Santo_Domingo', 'America/Havana', 'America/Guayaquil', 'America/La_Paz', 'America/Santiago',
      'America/Argentina/Buenos_Aires', 'America/Montevideo', 'America/Asuncion', 'America/Sao_Paulo', 'America/Toronto', 'America/Vancouver',
      'Europe/London', 'Europe/Madrid', 'Europe/Paris', 'Europe/Berlin', 'Europe/Rome', 'Europe/Lisbon', 'Africa/Lagos', 'Africa/Johannesburg', 'Asia/Dubai',
      'Asia/Kolkata', 'Asia/Manila', 'Asia/Shanghai', 'Asia/Tokyo', 'Asia/Seoul', 'Asia/Singapore', 'Australia/Sydney', 'Pacific/Auckland', 'UTC'];
    var mine = Intl.DateTimeFormat().resolvedOptions().timeZone || 'UTC';
    if (ZONES.indexOf(mine) < 0) ZONES.unshift(mine);
    function label(z) { return z.replace(/^.*\//, '').replace(/_/g, ' ') + ' (' + ({ America: T('Americas', 'América'), Europe: 'Europa', Africa: 'África', Pacific: T('Pacific', 'Pacífico') }[z.split('/')[0]] || z.split('/')[0]) + ')'; }
    var opts = ZONES.map(function (z) { return '<option value="' + z + '">' + esc(label(z)) + '</option>'; }).join('');
    var from = $(el, '[data-k="from"]'), dt = $(el, '[data-k="dt"]'), list = $(el, '.tz-list'), add = $(el, '[data-k="add"]');
    from.innerHTML = opts; add.innerHTML = '<option value="">' + T('+ Add a city', '+ Agregar ciudad') + '</option>' + opts; from.value = mine;
    var shown = ES ? ['America/Mexico_City', 'America/New_York', 'America/Bogota', 'America/Argentina/Buenos_Aires', 'Europe/Madrid'] : ['America/New_York', 'America/Chicago', 'America/Los_Angeles', 'Europe/London', 'Asia/Tokyo'];
    shown = shown.filter(function (z) { return z !== mine; });
    function offsetOf(z, d) {   // minutes east of UTC for zone z at instant d
      var p = new Intl.DateTimeFormat('en-US', { timeZone: z, hourCycle: 'h23', year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit', second: '2-digit' }).formatToParts(d), o = {};
      p.forEach(function (x) { o[x.type] = x.value; });
      return (Date.UTC(+o.year, o.month - 1, +o.day, +o.hour, +o.minute, +o.second) - Math.floor(d.getTime() / 1000) * 1000) / 60000;
    }
    function instant() {   // the typed local time in the "from" zone, as a real instant
      var m = dt.value.match(/(\d+)-(\d+)-(\d+)T(\d+):(\d+)/); if (!m) return new Date();
      var guess = Date.UTC(+m[1], m[2] - 1, +m[3], +m[4], +m[5]), off = offsetOf(from.value, new Date(guess));
      var d = new Date(guess - off * 60000), off2 = offsetOf(from.value, d);
      return off2 === off ? d : new Date(guess - off2 * 60000);
    }
    function fmtIn(z, d) { return new Intl.DateTimeFormat(ES ? 'es-US' : 'en-US', { timeZone: z, weekday: 'short', day: 'numeric', month: 'short', hour: 'numeric', minute: '2-digit' }).format(d); }
    function run() {
      var d = instant();
      list.innerHTML = shown.map(function (z, i) {
        var diff = (offsetOf(z, d) - offsetOf(from.value, d)) / 60;
        return '<div class="out"><span>' + esc(label(z)) + ' <span class="small">(' + (diff >= 0 ? '+' : '') + diff + ' h)</span></span><strong>' + esc(fmtIn(z, d)) + ' <button type="button" class="chip" data-rm="' + i + '" aria-label="' + T('Remove', 'Quitar') + '">×</button></strong></div>';
      }).join('');
      $$(list, '[data-rm]').forEach(function (b) { b.addEventListener('click', function () { shown.splice(+b.getAttribute('data-rm'), 1); run(); }); });
    }
    function nowLocal() { var d = new Date(), p = {}; new Intl.DateTimeFormat('en-US', { timeZone: from.value, hourCycle: 'h23', year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' }).formatToParts(d).forEach(function (x) { p[x.type] = x.value; }); dt.value = p.year + '-' + p.month + '-' + p.day + 'T' + p.hour + ':' + p.minute; }
    add.addEventListener('change', function () { if (add.value && shown.indexOf(add.value) < 0) shown.push(add.value); add.value = ''; run(); track('tz'); });
    from.addEventListener('change', run); dt.addEventListener('input', run);
    $(el, '[data-act="now"]').addEventListener('click', function () { nowLocal(); run(); });
    nowLocal(); run();
  };

  /* ------------------------------------------------------------------ color palette */
  function hsl2hex(h, s, l) { s /= 100; l /= 100; var k = function (n) { return (n + h / 30) % 12; }, a = s * Math.min(l, 1 - l), f = function (n) { return l - a * Math.max(-1, Math.min(k(n) - 3, Math.min(9 - k(n), 1))); }; return '#' + [f(0), f(8), f(4)].map(function (x) { return Math.round(x * 255).toString(16).padStart(2, '0'); }).join(''); }
  function hex2rgb(h) { h = h.replace('#', ''); return [0, 2, 4].map(function (i) { return parseInt(h.substr(i, 2), 16); }); }
  function rgb2hsl(r, g, b) { r /= 255; g /= 255; b /= 255; var mx = Math.max(r, g, b), mn = Math.min(r, g, b), h = 0, s = 0, l = (mx + mn) / 2, d = mx - mn; if (d) { s = l > 0.5 ? d / (2 - mx - mn) : d / (mx + mn); h = mx === r ? (g - b) / d + (g < b ? 6 : 0) : mx === g ? (b - r) / d + 2 : (r - g) / d + 4; h *= 60; } return [Math.round(h), Math.round(s * 100), Math.round(l * 100)]; }
  function inkFor(hex) { var c = hex2rgb(hex); return (c[0] * 299 + c[1] * 587 + c[2] * 114) / 1000 > 140 ? '#1c2321' : '#ffffff'; }
  E.palette = function (el) {
    var box = $(el, '.pal'), scheme = $(el, '[data-k="scheme"]'), base = $(el, '[data-k="base"]'), cols = [], locked = [false, false, false, false, false];
    function gen(fromBase) {
      var h0 = fromBase ? rgb2hsl.apply(null, hex2rgb(base.value))[0] : rnd(360), sc = scheme.value, hs;
      if (sc === 'analog') hs = [h0 - 40, h0 - 20, h0, h0 + 20, h0 + 40];
      else if (sc === 'comp') hs = [h0, h0, h0 + 180, h0 + 180, h0 + 15];
      else if (sc === 'triad') hs = [h0, h0 + 120, h0 + 240, h0, h0 + 120];
      else if (sc === 'mono') hs = [h0, h0, h0, h0, h0];
      else hs = [h0, h0 + 30 + rnd(60), h0 + 150 + rnd(60), h0 + 210 + rnd(60), rnd(360)];
      var ls = sc === 'mono' ? [20, 35, 50, 68, 85] : [30 + rnd(15), 45 + rnd(15), 55 + rnd(15), 70 + rnd(12), 88 + rnd(6)], ss = sc === 'pastel' ? 55 : 45 + rnd(35);
      if (sc === 'pastel') ls = [78, 82, 85, 88, 92].map(function (x) { return x - rnd(8); });
      for (var i = 0; i < 5; i++) if (!locked[i]) cols[i] = hsl2hex(((hs[i] % 360) + 360) % 360, sc === 'mono' ? 40 + i * 6 : ss + rnd(10), ls[i]);
      if (fromBase && !locked[2]) cols[2] = base.value;
      draw(); track('palette');
    }
    function draw() {
      box.innerHTML = cols.map(function (c, i) {
        var r = hex2rgb(c), h = rgb2hsl(r[0], r[1], r[2]), ink = inkFor(c);
        return '<div class="sw" style="background:' + c + ';color:' + ink + '"><button type="button" class="sw-lock" data-lock="' + i + '" aria-pressed="' + locked[i] + '" title="' + T('Lock', 'Fijar') + '">' + (locked[i] ? '🔒' : '🔓') + '</button><button type="button" class="sw-hex" data-hex="' + c + '">' + c.toUpperCase() + '</button><small>rgb(' + r.join(', ') + ')<br>hsl(' + h[0] + ', ' + h[1] + '%, ' + h[2] + '%)</small></div>';
      }).join('');
      $$(box, '[data-lock]').forEach(function (b) { b.addEventListener('click', function () { var i = +b.getAttribute('data-lock'); locked[i] = !locked[i]; draw(); }); });
      $$(box, '[data-hex]').forEach(function (b) { copyBtn(b, function () { return b.getAttribute('data-hex'); }); });
    }
    $(el, '[data-act="gen"]').addEventListener('click', function () { gen(false); });
    $(el, '[data-act="base"]').addEventListener('click', function () { gen(true); });
    scheme.addEventListener('change', function () { gen(false); });
    copyBtn($(el, '[data-act="css"]'), function () { return ':root {\n' + cols.map(function (c, i) { return '  --color-' + (i + 1) + ': ' + c + ';'; }).join('\n') + '\n}'; });
    document.addEventListener('keydown', function (e) { if (e.code === 'Space' && e.target === document.body) { e.preventDefault(); gen(false); } });
    gen(false);
  };

  /* ------------------------------------------------------------------ name generator */
  var NAMES = {
    dog: ['Biscuit', 'Maple', 'Pepper', 'Mochi', 'Ziggy', 'Bear', 'Luna', 'Waffles', 'Juniper', 'Rocco', 'Pistachio', 'Nala', 'Bruno', 'Cookie', 'Hazel', 'Toby', 'Olive', 'Moose', 'Pancho', 'Kona', 'Bowie', 'Clover', 'Gus', 'Ruby', 'Taco', 'Sunny', 'Ranger', 'Peanut', 'Willow', 'Bandit', 'Dakota', 'Churro', 'Lola', 'Teddy', 'Marley', 'Frida', 'Chico', 'Daisy', 'Ollie', 'Canela'],
    cat: ['Mittens', 'Salem', 'Cleo', 'Miso', 'Tofu', 'Smokey', 'Nova', 'Pumpkin', 'Oreo', 'Jasper', 'Pixel', 'Ginger', 'Shadow', 'Mango', 'Sushi', 'Luna', 'Felix', 'Nutmeg', 'Onyx', 'Biscotti', 'Pepita', 'Misha', 'Coco', 'Simba', 'Kiki', 'Figaro', 'Noodle', 'Ash', 'Bombón', 'Michi', 'Pelusa', 'Tigre', 'Nieve', 'Chispa', 'Lulú', 'Garfield', 'Sombra', 'Panqué', 'Mía', 'Olivia'],
    babyf: ['Sofía', 'Valentina', 'Isabella', 'Camila', 'Emma', 'Olivia', 'Mía', 'Luna', 'Lucía', 'Victoria', 'Ava', 'Elena', 'Gabriela', 'Amelia', 'Natalia', 'Aitana', 'Renata', 'Ximena', 'Mariana', 'Daniela', 'Zoe', 'Abigail', 'Regina', 'Julieta', 'Emilia', 'Paula', 'Antonella', 'Isla', 'Valeria', 'Catalina'],
    babym: ['Mateo', 'Santiago', 'Liam', 'Sebastián', 'Lucas', 'Noah', 'Diego', 'Daniel', 'Leonardo', 'Gael', 'Emiliano', 'Thiago', 'Nicolás', 'Adrián', 'Benjamín', 'Julián', 'Ethan', 'Elías', 'Gabriel', 'Tomás', 'Samuel', 'Joaquín', 'Iker', 'Dylan', 'Lorenzo', 'Isaac', 'Andrés', 'Alejandro', 'Martín', 'Bruno'],
    biz1: ['Bright', 'Golden', 'Little', 'True', 'Happy', 'Blue', 'Wild', 'Cozy', 'Bold', 'Urban', 'Sunny', 'North', 'Fresh', 'Pure', 'Silver', 'Clever', 'Rustic', 'Prime', 'Maple', 'Cedar'],
    biz2: ['Studio', 'Co.', 'Collective', 'Market', 'Lab', 'Kitchen', 'Works', 'House', 'Supply', 'Corner', 'Atelier', 'Goods', 'Shop', 'Hub', 'Nest', 'Spot', 'Craft', 'Garden', 'Bakery', 'Society'],
    biz1es: ['Luz', 'Dulce', 'Raíz', 'Sol', 'Nido', 'Brisa', 'Canela', 'Cielo', 'Alma', 'Lima', 'Arena', 'Tierra', 'Miel', 'Coral', 'Bambú', 'Selva', 'Aurora', 'Olivo', 'Faro', 'Ámbar'],
    biz2es: ['Estudio', 'Taller', 'Mercado', 'Casa', 'Cocina', 'Café', 'Rincón', 'Tienda', 'Atelier', 'Colectivo', 'Huerta', 'Botica', 'Almacén', 'Panadería', 'Club']
  };
  E.names = function (el) {
    var out = $(el, '.nm-out'), kind = $(el, '[data-k="kind"]'), letter = $(el, '[data-k="letter"]'), fav = [];
    function gen() {
      var k = kind.value, L = (letter.value || '').trim().toLowerCase(), pool, res = [];
      if (k === 'biz') {
        var a = ES ? NAMES.biz2es : NAMES.biz1, b = ES ? NAMES.biz1es : NAMES.biz2, kw = $(el, '[data-k="word"]').value.trim();
        for (var i = 0; i < 40 && res.length < 12; i++) {
          var n = ES ? a[rnd(a.length)] + ' ' + (kw && rnd(2) ? kw : b[rnd(b.length)]) : (kw && rnd(2) ? kw.charAt(0).toUpperCase() + kw.slice(1) : a[rnd(a.length)]) + ' ' + b[rnd(b.length)];
          if (L && n.toLowerCase().indexOf(L) !== 0) continue;
          if (res.indexOf(n) < 0) res.push(n);
        }
      } else {
        pool = k === 'baby' ? NAMES.babyf.concat(NAMES.babym) : NAMES[k];
        if (k === 'babyf' || k === 'babym') pool = NAMES[k];
        pool = pool.filter(function (n) { return !L || n.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').indexOf(L) === 0; });
        res = shuffle(pool).slice(0, 12);
      }
      out.innerHTML = res.length ? res.map(function (n) { return '<button type="button" class="chip nm" data-n="' + esc(n) + '">' + esc(n) + ' ♡</button>'; }).join(' ') : '<p class="small">' + T('No names with that letter. Try another one.', 'No hay nombres con esa letra. Prueba con otra.') + '</p>';
      $$(out, '[data-n]').forEach(function (b) { b.addEventListener('click', function () { var n = b.getAttribute('data-n'); if (fav.indexOf(n) < 0) fav.push(n); $(el, '.nm-fav').textContent = fav.join(' · '); }); });
      $(el, '.biz-only').hidden = k !== 'biz';
      track('names-' + k);
    }
    $(el, '[data-act="go"]').addEventListener('click', gen);
    kind.addEventListener('change', gen); letter.addEventListener('input', gen);
    var m = el.getAttribute('data-mode'); if (m) kind.value = m;
    gen();
  };

  /* ------------------------------------------------------------------ pet age in human years */
  E.petage = function (el) {
    var out = $(el, '.pa-out');
    function stage(pet, y) {
      if (pet === 'cat') return y < 0.5 ? T('Kitten', 'Gatito') : y < 2 ? T('Junior', 'Joven') : y < 7 ? T('Adult', 'Adulto') : y < 11 ? T('Mature', 'Maduro') : y < 15 ? T('Senior', 'Mayor') : T('Geriatric', 'Anciano');
      return y < 1 ? T('Puppy', 'Cachorro') : y < 3 ? T('Young adult', 'Adulto joven') : y < 7 ? T('Adult', 'Adulto') : T('Senior', 'Mayor');
    }
    function run() {
      var pet = $(el, '[data-k="pet"]').value, y = (+$(el, '[data-k="y"]').value || 0) + (+$(el, '[data-k="m"]').value || 0) / 12, size = +$(el, '[data-k="size"]').value;
      $(el, '.dog-only').hidden = pet !== 'dog';
      var per = pet === 'cat' ? 4 : size, h = y <= 1 ? y * 15 : y <= 2 ? 15 + (y - 1) * 9 : 24 + (y - 2) * per;
      var dna = pet === 'dog' && y >= 1 ? '<div class="out"><span>' + T('DNA formula (UC San Diego, 2019)', 'Fórmula de ADN (UC San Diego, 2019)') + '</span><strong>' + Math.round(16 * Math.log(y) + 31) + '</strong></div>' : '';
      out.innerHTML = '<div class="out big"><span>' + T('Age in human years', 'Edad en años humanos') + '</span><strong>' + Math.round(h) + '</strong></div><div class="out"><span>' + T('Life stage', 'Etapa de vida') + '</span><strong>' + stage(pet, y) + '</strong></div>' + dna;
    }
    $$(el, 'input,select').forEach(function (i) { i.addEventListener('input', run); i.addEventListener('change', run); });
    var m = el.getAttribute('data-mode'); if (m) $(el, '[data-k="pet"]').value = m;
    run();
  };

  /* ------------------------------------------------------------------ invoice generator (print / save as PDF) */
  E.invoice = function (el) {
    var rows = $(el, '.inv-rows'), prev = $(el, '.inv-preview');
    function v(k) { var i = $(el, '[data-k="' + k + '"]'); return i ? i.value : ''; }
    function addRow(d, q, p) {
      var r = document.createElement('div'); r.className = 'inv-row';
      r.innerHTML = '<input data-r="d" placeholder="' + T('Description', 'Descripción') + '" value="' + esc(d || '') + '"><input data-r="q" type="number" min="0" step="any" value="' + (q || 1) + '" aria-label="' + T('Quantity', 'Cantidad') + '"><input data-r="p" type="number" min="0" step="0.01" value="' + (p || 0) + '" aria-label="' + T('Price', 'Precio') + '"><button type="button" class="chip" aria-label="' + T('Remove line', 'Quitar línea') + '">×</button>';
      $(r, 'button').addEventListener('click', function () { r.remove(); draw(); });
      $$(r, 'input').forEach(function (i) { i.addEventListener('input', draw); });
      rows.appendChild(r); draw();
    }
    function money(x) { var c = v('cur') || 'USD'; try { return x.toLocaleString(ES ? 'es-US' : 'en-US', { style: 'currency', currency: c }); } catch (e) { return x.toFixed(2) + ' ' + c; } }
    function nl(s) { return esc(s).replace(/\n/g, '<br>'); }
    function draw() {
      var items = $$(rows, '.inv-row').map(function (r) { return { d: $(r, '[data-r=d]').value, q: +$(r, '[data-r=q]').value || 0, p: +$(r, '[data-r=p]').value || 0 }; });
      var sub = items.reduce(function (a, x) { return a + x.q * x.p; }, 0), disc = sub * (+v('disc') || 0) / 100, tax = (sub - disc) * (+v('tax') || 0) / 100, total = sub - disc + tax;
      prev.innerHTML = '<div class="inv-head"><div><h2>' + T('INVOICE', 'FACTURA') + '</h2><p>#' + esc(v('num')) + '</p></div><div class="inv-from">' + nl(v('from')) + '</div></div>' +
        '<div class="inv-meta"><div><strong>' + T('Bill to', 'Facturar a') + '</strong><br>' + nl(v('to')) + '</div><div>' + T('Date', 'Fecha') + ': ' + esc(v('date')) + (v('due') ? '<br>' + T('Due', 'Vence') + ': ' + esc(v('due')) : '') + '</div></div>' +
        '<table><tr><th>' + T('Description', 'Descripción') + '</th><th>' + T('Qty', 'Cant.') + '</th><th>' + T('Price', 'Precio') + '</th><th>' + T('Amount', 'Importe') + '</th></tr>' +
        items.map(function (x) { return '<tr><td>' + esc(x.d) + '</td><td>' + x.q + '</td><td>' + money(x.p) + '</td><td>' + money(x.q * x.p) + '</td></tr>'; }).join('') + '</table>' +
        '<div class="inv-tot"><div><span>' + T('Subtotal', 'Subtotal') + '</span><span>' + money(sub) + '</span></div>' + (disc ? '<div><span>' + T('Discount', 'Descuento') + ' (' + v('disc') + '%)</span><span>−' + money(disc) + '</span></div>' : '') +
        (tax ? '<div><span>' + T('Tax', 'Impuesto') + ' (' + v('tax') + '%)</span><span>' + money(tax) + '</span></div>' : '') + '<div class="inv-total"><span>' + T('Total', 'Total') + '</span><span>' + money(total) + '</span></div></div>' +
        (v('notes') ? '<p class="inv-notes">' + nl(v('notes')) + '</p>' : '');
    }
    $$(el, '.inv-form input, .inv-form textarea, .inv-form select').forEach(function (i) { if (!i.closest('.inv-rows')) { i.addEventListener('input', draw); i.addEventListener('change', draw); } });
    $(el, '[data-act="add"]').addEventListener('click', function () { addRow(); });
    $(el, '[data-act="print"]').addEventListener('click', function () {
      var pa = document.createElement('div'); pa.id = 'print-area'; pa.className = 'inv-preview'; pa.innerHTML = prev.innerHTML; document.body.appendChild(pa);
      document.body.classList.add('printing-invoice'); track('invoice'); window.print();
      setTimeout(function () { document.body.classList.remove('printing-invoice'); pa.remove(); }, 800);
    });
    var d = new Date(), due = new Date(Date.now() + 14 * 864e5), iso = function (x) { return x.getFullYear() + '-' + String(x.getMonth() + 1).padStart(2, '0') + '-' + String(x.getDate()).padStart(2, '0'); };
    $(el, '[data-k="date"]').value = iso(d); $(el, '[data-k="due"]').value = iso(due); $(el, '[data-k="num"]').value = d.getFullYear() + '-001';
    addRow(T('Website design', 'Diseño de página web'), 1, 450); addRow(T('Logo (3 versions)', 'Logo (3 versiones)'), 1, 150);
  };

  $$(document, '.tool[data-tool]').forEach(function (el) { var f = E[el.getAttribute('data-tool')]; if (f) f(el); });
})();
