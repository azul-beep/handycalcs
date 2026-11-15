/* Cookie notice + consent-gated GA4, Meta Pixel and AdSense. IDs come from window.HC (set in each page). */
(function () {
  var C = window.HC || {}, KEY = 'hc_consent';
  var es = document.documentElement.lang === 'es';
  function get() { try { return localStorage.getItem(KEY); } catch (e) { return null; } }
  function set(v) { try { localStorage.setItem(KEY, v); } catch (e) {} }
  function load(src, attrs) { var s = document.createElement('script'); s.async = true; s.src = src; for (var k in (attrs || {})) s.setAttribute(k, attrs[k]); document.head.appendChild(s); }

  window.dataLayer = window.dataLayer || [];
  function gtag() { window.dataLayer.push(arguments); }
  window.gtag = gtag;
  gtag('consent', 'default', { ad_storage: 'denied', analytics_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied', wait_for_update: 500 });

  var started = false;
  function startTracking() {
    if (started) return; started = true;
    gtag('consent', 'update', { ad_storage: 'granted', analytics_storage: 'granted', ad_user_data: 'granted', ad_personalization: 'granted' });
    if (C.ga4) { load('https://www.googletagmanager.com/gtag/js?id=' + C.ga4); gtag('js', new Date()); gtag('config', C.ga4); }
    if (C.pixel) {
      !function (f, b, e, v, n, t, s) { if (f.fbq) return; n = f.fbq = function () { n.callMethod ? n.callMethod.apply(n, arguments) : n.queue.push(arguments); }; if (!f._fbq) f._fbq = n; n.push = n; n.loaded = !0; n.version = '2.0'; n.queue = []; t = b.createElement(e); t.async = !0; t.src = v; s = b.getElementsByTagName(e)[0]; s.parentNode.insertBefore(t, s); }(window, document, 'script', 'https://connect.facebook.net/en_US/fbevents.js');
      window.fbq('init', C.pixel); window.fbq('track', 'PageView');
    }
  }
  function startAds(personalized) {
    var q = window.adsbygoogle = window.adsbygoogle || [];
    if (!personalized) q.requestNonPersonalizedAds = 1;
    q.pauseAdRequests = 0;
  }
  window.hcTrack = function (name) {
    if (window.gtag && started) gtag('event', 'calculate', { calculator: name });
    if (window.fbq && started) window.fbq('trackCustom', 'Calculate', { calculator: name });
  };

  // Clicks on affiliate / sponsored links -> GA4 event "affiliate_click" (shows in Analytics which programs get clicks).
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[rel~="sponsored"]');
    if (!a || !started) return;
    var label = a.getAttribute('data-aff') || a.textContent.trim().slice(0, 60);
    if (window.gtag) gtag('event', 'affiliate_click', { program: label, link_domain: a.hostname, page: location.pathname });
    if (window.fbq) window.fbq('trackCustom', 'AffiliateClick', { program: label });
  });

  function banner() {
    var d = document.createElement('div');
    d.className = 'cookie';
    d.setAttribute('role', 'dialog');
    d.setAttribute('aria-label', es ? 'Aviso de cookies' : 'Cookie notice');
    d.innerHTML = '<p>' + (es
      ? 'Usamos cookies para estadísticas (Google Analytics), medir anuncios (Meta) y mostrar publicidad (Google AdSense). <a href="/es/cookies/">Más info</a>'
      : 'We use cookies for statistics (Google Analytics), ad measurement (Meta) and to show ads (Google AdSense). <a href="/cookies/">Learn more</a>') +
      '</p><div class="cookie-b"><button type="button" class="btn-ghost" data-c="no">' + (es ? 'Solo necesarias' : 'Necessary only') +
      '</button><button type="button" class="btn" data-c="yes">' + (es ? 'Aceptar' : 'Accept') + '</button></div>';
    document.body.appendChild(d);
    d.addEventListener('click', function (e) {
      var c = e.target.getAttribute && e.target.getAttribute('data-c');
      if (!c) return;
      set(c); d.remove();
      if (c === 'yes') { startTracking(); startAds(true); } else startAds(false);
    });
  }
  var c = get();
  if (c === 'yes') { startTracking(); startAds(true); }
  else if (c === 'no' || navigator.globalPrivacyControl) startAds(false);
  else banner();

  var reset = document.querySelectorAll('[data-reset-cookies]');
  for (var i = 0; i < reset.length; i++) reset[i].addEventListener('click', function (e) { e.preventDefault(); try { localStorage.removeItem(KEY); } catch (x) {} location.reload(); });
})();
