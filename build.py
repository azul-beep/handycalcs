# -*- coding: utf-8 -*-
"""Static site generator for Handy Calcs. Run: python3 build.py  -> writes ./site/"""
import html, json, os, shutil, sys, datetime
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
from calcs import CALCS, CATS

# ============================== CONFIG (edit here) ==============================
CONFIG = dict(
    site_url="https://gethandycalcs.pages.dev",   # change if Cloudflare gives another name or a domain is bought
    name="Handy Calcs",
    name_es="Handy Calcs",
    owner="Skye Solutions AI",
    email="support@skyesolutionsai.com",
    ga4="G-794S7HWQJS",
    pixel="",          # Meta Pixel ID, digits only
    adsense="ca-pub-1174178180336933",
    gsc_verify="snG6WI_Ay90gukuDRtPKQLCo42mUWLXTbusn-InyaTk",
    pinterest_verify="0d47d56066e050ff1586ee7b32e60bf2",   # Pinterest "Claim website" meta tag content (p:domain_verify), only the code
    mailerlite_action="",  # MailerLite embedded form action, e.g. https://assets.mailerlite.com/jsonp/ACCOUNT/forms/FORMID/subscribe
)
# Affiliate boxes. A link with an empty url is not shown.
AMAZON_TAG = "cruxreport-20"
INDEXNOW_KEY = "fa73deeb0b15a8fbbf4e7d3b06044329"  # public key for IndexNow (Bing, Yandex, Seznam); file served at /<key>.txt
AMAZON_ON = True       # site added to the Amazon Associates account (15 nov 2026)
AFFILIATES = {
    "restaurant": [
        dict(name="Publer", url="", en="Schedule your restaurant's Instagram, Facebook and TikTok posts for the whole week in one sitting.", es="Programa los posts de Instagram, Facebook y TikTok de tu restaurante para toda la semana de una vez."),
        dict(name="SocialBee", url="", en="Recycle your best menu photos and specials automatically on every social network.", es="Recicla automáticamente tus mejores fotos del menú y promociones en todas las redes."),
    ],
    "work": [
        dict(name="Typefully", url="", en="Write and schedule posts that grow your personal brand for your next job.", es="Escribe y programa publicaciones para hacer crecer tu marca personal y conseguir un mejor trabajo."),
    ],
    "money": [],
    "kitchen": [
        dict(name="Amazon", url="amazon:digital kitchen scale grams", en="A digital kitchen scale (under $15) makes every conversion exact.", es="Una balanza digital de cocina (menos de $15) hace que cada conversión sea exacta."),
        dict(name="Amazon", url="amazon:measuring cups and spoons set stainless", en="Stainless steel measuring cups and spoons that do not wear off.", es="Tazas y cucharas medidoras de acero que no se borran."),
    ],
}
# ================================================================================

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "site")
TODAY = os.environ.get("HC_TODAY") or datetime.date.today().isoformat()  # HC_TODAY=2026-11-20 to preview a date
E = html.escape

UI = {
 "en": dict(home="Home", all="All calculators", calc="Calculate", result="Results", faq="Frequently asked questions",
            related="Related calculators", privacy="Privacy policy", cookies="Cookie policy", terms="Terms of use", about="About", advertise="Advertise",
            other="Español", disclaimer="Results are estimates for information only, not financial, legal, tax or medical advice.",
            cookieset="Cookie settings", rights="All rights reserved.", copy="Copy", aff_title="Useful tools",
            aff_note="Some links are affiliate links: we may earn a commission at no extra cost to you. As an Amazon Associate we earn from qualifying purchases.",
            tagline="Free, fast calculators for tips, pay, budgets, loans, health, school and recipes.", private="Private: everything is calculated on your device."),
 "es": dict(home="Inicio", all="Todas las calculadoras", calc="Calcular", result="Resultados", faq="Preguntas frecuentes",
            related="Otras calculadoras", privacy="Política de privacidad", cookies="Política de cookies", terms="Términos de uso", about="Quiénes somos", advertise="Publicidad",
            other="English", disclaimer="Los resultados son estimaciones a modo informativo, no asesoramiento financiero, legal, impositivo ni médico.",
            cookieset="Configurar cookies", rights="Todos los derechos reservados.", copy="Copiar", aff_title="Herramientas útiles",
            aff_note="Algunos enlaces son de afiliados: podemos ganar una comisión sin costo extra para ti. Como afiliados de Amazon, ganamos con las compras que califican.",
            tagline="Calculadoras gratis y rápidas para propinas, sueldos, presupuestos, préstamos, salud, escuela y recetas.", private="Privado: todo se calcula en tu dispositivo."),
}

def url(lang, slug=""):
    base = "/" if lang == "en" else "/es/"
    return base + (slug + "/" if slug else "")

def abs_url(path):
    return CONFIG["site_url"].rstrip("/") + path

BY_ID = {c["id"]: c for c in CALCS}

def aff_link(u):
    if u.startswith("amazon:"):
        if not AMAZON_ON: return ""
        q = u[7:].replace(" ", "+")
        return "https://www.amazon.com/s?k=%s&tag=%s" % (q, AMAZON_TAG)
    return u

def affiliate_box(cat, lang):
    items = [(a, aff_link(a["url"])) for a in AFFILIATES.get(cat, [])]
    items = [(a, l) for a, l in items if l]
    if not items: return ""
    u = UI[lang]
    spon = "Sponsored" if lang == "en" else "Patrocinado"
    lis = "".join('<li>%s<a href="%s" rel="sponsored noopener" target="_blank">%s</a>: %s</li>' % ('<span class="tag">%s</span> ' % spon if a.get("paid") else "", E(l), E(a["name"]), E(a[lang])) for a, l in items)
    return '<aside class="aff"><h2>%s</h2><ul>%s</ul><p class="small">%s</p></aside>' % (u["aff_title"], lis, u["aff_note"])

CSS_VER = "4"

# ============================== Printable calendars ==============================
# calendarios/calendarios-AAAA/ is made by calendarios/regenerar.py (once a year, every Oct 1).
# build.py copies each year into site/, fills the GA4/AdSense/privacy markers and adds the
# site bar + cookie notice. The RSS goes out in a drip (2-3 pins a day, Azu's rule) with
# tools/goteo.py: rss-completo.xml = the whole queue, rss.xml = what is already out today.
CAL_DIR = os.path.join(ROOT, "calendarios")
GOTEO_FILE = os.path.join(CAL_DIR, "goteo.json")   # {"2027": "2026-11-17"} = first drip day per year

# ============================== Free tools guide (herramientas/, Spanish) ==============================
# herramientas/generar.py writes /herramientas-gratis/ with only the pages already out (drip 2-3 a day from
# herramientas/goteo-inicio.txt) and fills GA4/AdSense from CONFIG. tools/goteo.py writes the public rss.xml.
HERR_DIR = os.path.join(ROOT, "herramientas")

def build_herramientas():
    import subprocess, re
    if not os.path.isfile(os.path.join(HERR_DIR, "generar.py")): return []
    inicio = open(os.path.join(HERR_DIR, "goteo-inicio.txt"), encoding="utf-8").read().strip()
    out = os.path.join(OUT, "herramientas-gratis")
    c = CONFIG
    subprocess.run([sys.executable, os.path.join(HERR_DIR, "generar.py"), "--inicio", inicio, "--salida", out,
                    "--url", abs_url("/herramientas-gratis/"), "--ga4", c["ga4"], "--pixel", c["pixel"],
                    "--adsense", c["adsense"], "--privacidad", "/es/privacy/"], check=True, stdout=subprocess.DEVNULL)
    full = os.path.join(out, "rss-completo.xml")
    subprocess.run([sys.executable, os.path.join(ROOT, "tools", "goteo.py"), full, os.path.join(out, "rss.xml"),
                    "--inicio", inicio], check=True)
    os.remove(full)   # the queue stays private; Pinterest reads rss.xml
    sm = os.path.join(out, "sitemap-herramientas.xml")
    locs = re.findall(r"<loc>([^<]+)</loc>", open(sm, encoding="utf-8").read())
    os.remove(sm)     # merged into the main sitemap
    return locs

def herr_link():
    return "/herramientas-gratis/" if os.path.exists(os.path.join(OUT, "herramientas-gratis", "index.html")) else None

# ============================== Printables (imprimibles/, Spanish) ==============================
# imprimibles/generar.py (daily GitHub Action: "python3 imprimibles/generar.py diario") makes the daily puzzle
# and the bilingual worksheets in place, with GA4/AdSense read from CONFIG above. Here we only copy them.
IMP_DIR = os.path.join(ROOT, "imprimibles")

def copy_imprimibles():
    import re
    if not os.path.isfile(os.path.join(IMP_DIR, "index.html")): return []
    out = os.path.join(OUT, "imprimibles"); os.makedirs(out)
    shutil.copy(os.path.join(IMP_DIR, "index.html"), out)
    locs = [abs_url("/imprimibles/")]
    for d in ("juego-del-dia", "fichas-bilingues"):
        shutil.copytree(os.path.join(IMP_DIR, d), os.path.join(out, d),
                        ignore=shutil.ignore_patterns("rss-completo.xml", "sitemap.xml", "datos", "__pycache__"))
        sm = os.path.join(IMP_DIR, d, "sitemap.xml")
        if os.path.exists(sm):
            locs += re.findall(r"<loc>([^<]+)</loc>", open(sm, encoding="utf-8").read())
    return list(dict.fromkeys(locs))

# ============================== Pinterest-only pin feeds (pines/) ==============================
# pines/<name>/pines-en|pines-es + rss-completo.xml (queue). Start day per feed in pines/goteo.json.
# Each day tools/goteo.py writes the public /pines/<name>/rss.xml (2-3 pins a day). Feeds without a start date stay empty.
PINES_DIR = os.path.join(ROOT, "pines")

def build_pines():
    import subprocess
    if not os.path.isdir(PINES_DIR): return
    starts = json.load(open(os.path.join(PINES_DIR, "goteo.json"), encoding="utf-8"))
    for name in sorted(os.listdir(PINES_DIR)):
        src = os.path.join(PINES_DIR, name); full = os.path.join(src, "rss-completo.xml")
        if not os.path.isfile(full): continue
        dst = os.path.join(OUT, "pines", name)
        shutil.copytree(src, dst, ignore=shutil.ignore_patterns("rss-completo.xml"))
        inicio = starts.get(name) or "2999-01-01"
        subprocess.run([sys.executable, os.path.join(ROOT, "tools", "goteo.py"), full, os.path.join(dst, "rss.xml"),
                        "--inicio", inicio], check=True)

def cal_years():
    if not os.path.isdir(CAL_DIR): return []
    ys = [d.split("-")[1] for d in os.listdir(CAL_DIR) if d.startswith("calendarios-") and d.split("-")[1].isdigit()
          and os.path.isfile(os.path.join(CAL_DIR, d, "index.html"))]
    return sorted(ys)

def cal_paths(y):
    return "/calendarios-%s/" % y, "/calendarios-%s/free-printable-%s-calendars.html" % (y, y)   # (es, en)

def cal_link(lang):
    ys = cal_years()
    if not ys: return None
    y = ys[-1]; es_p, en_p = cal_paths(y)
    return (en_p, "%s Calendars" % y) if lang == "en" else (es_p, "Calendarios %s" % y)

def copy_calendars():
    import re, subprocess
    ys = cal_years()
    if not ys: return []
    starts = json.load(open(GOTEO_FILE, encoding="utf-8")) if os.path.exists(GOTEO_FILE) else {}
    c = CONFIG
    hc = '<script>window.HC=%s;</script>' % json.dumps({"ga4": c["ga4"], "pixel": c["pixel"]})
    ads = ""
    if c["adsense"]:
        ads = ('<script>window.adsbygoogle=window.adsbygoogle||[];window.adsbygoogle.pauseAdRequests=1;</script>'
               '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=%s" crossorigin="anonymous"></script>' % c["adsense"])
    latest = ys[-1]
    for y in ys:
        src = os.path.join(CAL_DIR, "calendarios-" + y)
        full = os.path.join(src, "rss-completo.xml")
        if not os.path.exists(full) and os.path.exists(os.path.join(src, "rss.xml")):
            os.rename(os.path.join(src, "rss.xml"), full)          # fresh output of regenerar.py
        if y not in starts:                                       # new year: the drip starts tomorrow
            starts[y] = (datetime.date.today() + datetime.timedelta(days=1)).isoformat()
            json.dump(starts, open(GOTEO_FILE, "w", encoding="utf-8"), indent=1)
        dst = os.path.join(OUT, "calendarios-" + y)
        shutil.copytree(src, dst, ignore=shutil.ignore_patterns("rss-completo.xml", "rss.xml"))
        subprocess.run([sys.executable, os.path.join(ROOT, "tools", "goteo.py"), full, os.path.join(dst, "rss.xml"),
                        "--inicio", starts[y]], check=True)
        es_p, en_p = cal_paths(y)
        for lang, path in (("es", es_p), ("en", en_p)):
            fp = os.path.join(OUT, path.strip("/"), "index.html") if path.endswith("/") else os.path.join(OUT, path.strip("/"))
            h = open(fp, encoding="utf-8").read()
            u = UI[lang]; home = url(lang)
            bar = ('<header class="top"><div class="wrap"><a class="logo" href="%s"><span class="mark">=</span> %s</a>'
                   '<nav><a href="%s#all">%s</a></nav></div></header>' % (home, E(c["name"]), home, u["all"]))
            if y != latest:
                ne, nn = cal_paths(latest)
                bar += ('<p class="cal-new"><a href="%s">%s</a></p>' % (ne if lang == "es" else nn,
                        ("Ya están los calendarios %s" if lang == "es" else "The %s calendars are out") % latest))
            h = h.replace("<!-- GA4 -->", hc)
            h = re.sub(r"<!-- ADSENSE: script[^>]*-->", ads, h)
            h = re.sub(r'\s*<div class="cal-ad"><!-- ADSENSE:[^>]*--></div>', "", h)   # Auto ads place themselves
            h = re.sub(r'<!-- PRIVACIDAD:[^>]*--><a href="/privacidad.html" rel="nofollow">',
                       '<a href="%s">' % ("/es/privacy/" if lang == "es" else "/privacy/"), h)
            h = h.replace('<link rel="stylesheet" href="estilos.css">',
                          '<link rel="stylesheet" href="/style.css?v=%s"><link rel="stylesheet" href="estilos.css">' % CSS_VER)
            h = h.replace("<body>", "<body>\n" + bar, 1)
            h = h.replace("</body>", '<script src="/site.js?v=%s" defer></script>\n</body>' % CSS_VER, 1)
            open(fp, "w", encoding="utf-8").write(h)
    # stable address for Pinterest: always the newest year's feed
    shutil.copy(os.path.join(OUT, "calendarios-" + latest, "rss.xml"), os.path.join(OUT, "calendarios-rss.xml"))
    return ys

def newsletter(lang):
    act = CONFIG["mailerlite_action"]
    if not act: return ""
    if lang == "en":
        h, t, ph, b, n = ("Free weekly money tips", "One short email a week: tipping, restaurant costs, pay and budgets. Unsubscribe anytime.", "Your email", "Subscribe", "Thanks! Check your inbox to confirm.")
    else:
        h, t, ph, b, n = ("Consejos de dinero gratis cada semana", "Un correo corto por semana: propinas, costos de restaurante, sueldo y presupuesto. Te das de baja cuando quieras.", "Tu correo", "Suscribirme", "¡Gracias! Revisa tu correo para confirmar.")
    priv = "/privacy/" if lang == "en" else "/es/privacy/"
    return f'''<aside class="news"><h2>{h}</h2><p>{t}</p>
<form class="nl" action="{E(act)}" method="post" target="hc_nl" onsubmit="setTimeout(function(){{document.getElementById('nl-ok-{lang}').hidden=false}},600);if(window.hcTrack)hcTrack('newsletter')">
<input type="email" name="fields[email]" required placeholder="{ph}" aria-label="{ph}"><input type="hidden" name="ml-submit" value="1"><input type="hidden" name="fields[language]" value="{lang}">
<button class="btn" type="submit">{b}</button></form><p class="small" id="nl-ok-{lang}" hidden>{n}</p>
<p class="small"><a href="{priv}">{'Privacy policy' if lang == 'en' else 'Política de privacidad'}</a></p><iframe name="hc_nl" title="newsletter" hidden></iframe></aside>'''

def head(lang, title, desc, path, alt_path, extra_ld=None):
    c = CONFIG
    hc = json.dumps({"ga4": c["ga4"], "pixel": c["pixel"]})
    ads = ""
    if c["adsense"]:
        ads = ('<script>window.adsbygoogle=window.adsbygoogle||[];window.adsbygoogle.pauseAdRequests=1;</script>'
               '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=%s" crossorigin="anonymous"></script>' % c["adsense"])
    gsc = '<meta name="google-site-verification" content="%s">' % c["gsc_verify"] if c["gsc_verify"] else ""
    if c.get("pinterest_verify"): gsc += '<meta name="p:domain_verify" content="%s">' % c["pinterest_verify"]
    alts = ""
    if alt_path:
        en_p, es_p = (path, alt_path) if lang == "en" else (alt_path, path)
        alts = ('<link rel="alternate" hreflang="en" href="%s"><link rel="alternate" hreflang="es" href="%s">'
                '<link rel="alternate" hreflang="x-default" href="%s">' % (abs_url(en_p), abs_url(es_p), abs_url(en_p)))
    ld = ""
    for block in (extra_ld or []):
        ld += '<script type="application/ld+json">%s</script>' % json.dumps(block, ensure_ascii=False)
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{abs_url(path)}">
{alts}
<meta property="og:type" content="website">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:url" content="{abs_url(path)}">
<meta property="og:site_name" content="{E(c['name'])}">
<meta property="og:locale" content="{'en_US' if lang == 'en' else 'es_US'}">
<meta property="og:image" content="{abs_url('/og-image.png')}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0f766e">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/style.css?v={CSS_VER}">
{gsc}
<script>window.HC={hc};</script>
{ads}
{ld}
</head>
<body>
"""

def header(lang, alt_path):
    u = UI[lang]
    alt = alt_path or url("es" if lang == "en" else "en")
    cl = cal_link(lang)
    cal_nav = '<a href="%s">%s</a>' % (cl[0], E(cl[1])) if cl else ""
    if TOOLS_LIVE: cal_nav = '<a href="%s">%s</a>' % (TOOL_UI[lang]["hub"], TOOL_UI[lang]["short"]) + cal_nav
    if lang == "es" and herr_link(): cal_nav += '<a href="/herramientas-gratis/">Herramientas gratis</a>'
    if lang == "es" and os.path.isdir(os.path.join(OUT, "imprimibles")): cal_nav += '<a href="/imprimibles/">Imprimibles</a>'
    return f"""<header class="top"><div class="wrap">
<a class="logo" href="{url(lang)}"><span class="mark">=</span> {E(CONFIG['name'])}</a>
<nav><a href="{url(lang)}#all">{u['all']}</a>{cal_nav}<a href="{alt}" hreflang="{'es' if lang == 'en' else 'en'}" lang="{'es' if lang == 'en' else 'en'}">{u['other']}</a></nav>
</div></header>
<main class="wrap">
"""

def footer(lang):
    u = UI[lang]
    p = "" if lang == "en" else "/es"
    cats = ""
    for cid, names in CATS.items():
        items = [c for c in CALCS if c["cat"] == cid]
        cats += '<div><h3>%s</h3><ul>%s</ul></div>' % (names[0 if lang == "en" else 1],
            "".join('<li><a href="%s">%s</a></li>' % (url(lang, c[lang]["slug"]), E(c[lang]["h1"])) for c in items))
    cl = cal_link(lang)
    cal_foot = '<a href="%s">%s</a> · ' % (cl[0], E(cl[1])) if cl else ""
    if TOOLS_LIVE: cal_foot += '<a href="%s">%s</a> · ' % (TOOL_UI[lang]["hub"], TOOL_UI[lang]["name"])
    if lang == "es" and herr_link(): cal_foot += '<a href="/herramientas-gratis/">Herramientas gratis para emprender</a> · '
    if lang == "es" and os.path.isdir(os.path.join(OUT, "imprimibles")): cal_foot += '<a href="/imprimibles/">Sudoku del día y fichas bilingües</a> · '
    if lang == "en" and ARTICLES: cal_foot += '<a href="/guides/">Guides</a> · '
    return f"""</main>
<footer class="foot"><div class="wrap">
<div class="fcols">{cats}</div>
<p class="small">{u['disclaimer']}</p>
<p class="links">{cal_foot}<a href="{p}/about/">{u['about']}</a> · <a href="{p}/privacy/">{u['privacy']}</a> · <a href="{p}/cookies/">{u['cookies']}</a> · <a href="{p}/terms/">{u['terms']}</a> · <a href="{p}/advertise/">{u['advertise']}</a> · <a href="#" data-reset-cookies>{u['cookieset']}</a></p>
<p class="small">© {datetime.date.today().year} {E(CONFIG['name'])} · {E(CONFIG['owner'])}. {u['rights']}</p>
</div></footer>
<script src="/site.js?v={CSS_VER}" defer></script>
"""

def field(inp, lang, cid):
    k = inp["key"]; fid = "%s-%s" % (cid, k)
    lab = E(inp[lang])
    if inp["kind"] == "num":
        unit = inp["unit"]
        pre = '<span class="pre">$</span>' if unit == "$" else ""
        post = '<span class="post">%</span>' if unit == "%" else ""
        return ('<label for="%s">%s</label><div class="inp%s%s">%s<input id="%s" data-in="%s" type="number" inputmode="decimal" step="%s" min="%s" value="%s">%s</div>'
                % (fid, lab, " hp" if pre else "", " hs" if post else "", pre, fid, k, inp["step"], inp["min"], inp["default"], post))
    if inp["kind"] == "select":
        opts = "".join('<option value="%s"%s>%s</option>' % (v, " selected" if v == inp["default"] else "", E(en if lang == "en" else es)) for v, en, es in inp["options"])
        return '<label for="%s">%s</label><div class="inp"><select id="%s" data-in="%s">%s</select></div>' % (fid, lab, fid, k, opts)
    if inp["kind"] == "textarea":
        return '<label for="%s">%s</label><textarea id="%s" data-in="%s" rows="%d" spellcheck="false">%s</textarea>' % (fid, lab, fid, k, inp["rows"], E(inp["default_" + lang]))
    if inp["kind"] in ("date", "time"):
        # default "today" is filled in by calc.js with the visitor's date
        val = "" if inp["default"] == "today" else inp["default"]
        tod = ' data-today="1"' if inp["default"] == "today" else ""
        return '<label for="%s">%s</label><div class="inp"><input id="%s" data-in="%s" type="%s" value="%s"%s></div>' % (fid, lab, fid, k, inp["kind"], E(val), tod)
    if inp["kind"] == "timerow":
        # one line of a time card: start, end and unpaid break (minutes)
        st, en, br = inp["default"]
        ph = ("Start", "End", "Break (min)") if lang == "en" else ("Entrada", "Salida", "Pausa (min)")
        th = '<div class="trow th" aria-hidden="true"><span>%s</span><span>%s</span><span>%s</span></div>' % ph if k.endswith("1") else ""
        return (th + '<span class="lab">%s</span><div class="trow">'
                '<input id="%s" data-in="%s_s" type="time" value="%s" aria-label="%s %s">'
                '<input data-in="%s_e" type="time" value="%s" aria-label="%s %s">'
                '<input data-in="%s_b" type="number" inputmode="numeric" min="0" step="5" value="%s" aria-label="%s %s" placeholder="%s"></div>'
                % (lab, fid, k, st, lab, ph[0], k, en, lab, ph[1], k, br, lab, ph[2], ph[2]))
    return '<label for="%s">%s</label><div class="inp"><input id="%s" data-in="%s" type="text" value="%s"></div>' % (fid, lab, fid, k, E(inp["default"]))

def calc_widget(c, lang):
    u = UI[lang]
    fields = ""
    for inp in c["inputs"]:
        fields += '<div class="f">%s</div>' % field(inp, lang, c["id"])
        if c.get("presets") and c["presets"][0] == inp["key"]:
            k, vals = c["presets"]
            fields += '<div class="chips" role="group">%s</div>' % "".join(
                '<button type="button" class="chip" data-set="%s-%s" data-val="%s">%s%s</button>' % (c["id"], k, v, v, "%" if inp["unit"] == "%" else "") for v in vals)
    outs = ""
    for o in c["outputs"]:
        cls = "out big" if o["big"] else "out"
        tag = "pre" if o["pre"] else "strong"
        cp = '<button type="button" class="chip" data-copy="%s">%s</button>' % (o["key"], u["copy"]) if c.get("copy") == o["key"] else ""
        outs += '<div class="%s"><span>%s</span><%s data-out="%s" aria-live="polite">—</%s>%s</div>' % (cls, E(o[lang]), tag, o["key"], tag, cp)
    return f"""<section class="card calc"><form data-calc="{c['id']}" novalidate>{fields}
<button class="btn wide" type="submit">{u['calc']}</button></form>
<div class="results"><h2 class="sr">{u['result']}</h2>{outs}<p class="small priv">🔒 {u['private']}</p></div></section>"""

def embed_path(c, lang):
    return url(lang, "embed/" + c[lang]["slug"])

def embed_box(c, lang):
    """'Embed this calculator' box: a ready iframe code with a credit link back to the full page."""
    d = c[lang]
    code = ('<iframe src="%s" title="%s" width="100%%" height="720" style="border:0;max-width:640px" loading="lazy"></iframe>'
            '<p style="font-size:13px"><a href="%s">%s</a> %s <a href="%s">Handy Calcs</a></p>'
            % (abs_url(embed_path(c, lang)), E(d["h1"]), abs_url(url(lang, d["slug"])), E(d["h1"]),
               "by" if lang == "en" else "de", abs_url(url(lang))))
    t = ("Embed this calculator on your site" if lang == "en" else "Pon esta calculadora en tu sitio")
    h = ("Free for blogs and websites. Copy this code and paste it into your page:" if lang == "en"
         else "Gratis para blogs y sitios web. Copia este código y pégalo en tu página:")
    return ('<section class="content embed"><details><summary>%s</summary><p class="small">%s</p>'
            '<textarea readonly rows="4" onclick="this.select()" style="width:100%%;font-size:13px">%s</textarea></details></section>' % (t, h, E(code)))

def embed_page(c, lang):
    """Bare calculator for iframes on other sites: no ads, no trackers, noindex, credit link to the full page."""
    d = c[lang]; full = url(lang, d["slug"])
    s = f"""<!DOCTYPE html>
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(d['h1'])} | {E(CONFIG['name'])}</title><meta name="robots" content="noindex">
<link rel="canonical" href="{abs_url(full)}"><link rel="stylesheet" href="/style.css?v={CSS_VER}">
<style>body{{background:transparent}}.wrap{{padding:8px}}.embed-credit{{text-align:center;font-size:13px;margin:8px 0}}</style></head>
<body><main class="wrap">{calc_widget(c, lang)}
<p class="embed-credit"><a href="{abs_url(full)}" target="_blank" rel="noopener">{E(d['h1'])}</a> · {'Free calculators at' if lang == 'en' else 'Calculadoras gratis en'} <a href="{abs_url(url(lang))}" target="_blank" rel="noopener">Handy Calcs</a></p>
</main><script src="/calc.js?v={CSS_VER}" defer></script></body></html>
"""
    return embed_path(c, lang), s

def guides_box(c, lang):
    gs = guides_for(c["id"]) if lang == "en" else []
    if not gs: return ""
    return '<section class="content"><h2>Guides</h2><div class="rels">%s</div></section>' % "".join('<a class="rel" href="/guides/%s/">%s</a>' % (a["slug"], E(a["h1"])) for a in gs)

def calc_page(c, lang):
    d = c[lang]; other = "es" if lang == "en" else "en"
    path = url(lang, d["slug"]); alt = url(other, c[other]["slug"])
    u = UI[lang]
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in d["faq"]]}
    app_ld = {"@context": "https://schema.org", "@type": "WebApplication", "name": d["h1"], "url": abs_url(path),
              "applicationCategory": "UtilitiesApplication", "operatingSystem": "Any", "inLanguage": lang,
              "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "description": d["desc"]}
    crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": CONFIG["name"], "item": abs_url(url(lang))},
        {"@type": "ListItem", "position": 2, "name": d["h1"], "item": abs_url(path)}]}
    faq = "".join('<details><summary>%s</summary><p>%s</p></details>' % (E(q), E(a)) for q, a in d["faq"])
    rel = "".join('<a class="rel" href="%s">%s</a>' % (url(lang, BY_ID[r][lang]["slug"]), E(BY_ID[r][lang]["h1"])) for r in c["related"])
    catname = CATS[c["cat"]][0 if lang == "en" else 1]
    s = head(lang, d["title"], d["desc"], path, alt, [app_ld, faq_ld, crumbs]) + header(lang, alt)
    s += f"""<nav class="crumbs"><a href="{url(lang)}">{u['home']}</a> › <a href="{url(lang)}#{c['cat']}">{E(catname)}</a></nav>
<h1>{E(d['h1'])}</h1>
<p class="lead">{E(d['intro'])}</p>
{calc_widget(c, lang)}
<article class="content">{d['body']}</article>
{guides_box(c, lang)}{affiliate_box(c['aff'], lang)}
{newsletter(lang)}
<section class="content"><h2>{u['faq']}</h2>{faq}</section>
<section class="content"><h2>{u['related']}</h2><div class="rels">{rel}</div></section>
{embed_box(c, lang)}
<p class="small upd">{'Updated' if lang == 'en' else 'Actualizado'}: {TODAY}</p>
"""
    s += footer(lang) + '<script src="/calc.js?v=%s" defer></script>\n</body></html>\n' % CSS_VER
    return path, s

def home_page(lang):
    u = UI[lang]; other = "es" if lang == "en" else "en"
    path = url(lang); alt = url(other)
    title = ("Handy Calcs: Free Tip, Recipe, Pay and Budget Calculators" if lang == "en"
             else "Handy Calcs: calculadoras gratis de propinas, recetas, sueldo y presupuesto")
    desc = u["tagline"] + (" No sign-up, works on your phone." if lang == "en" else " Sin registrarte, funciona en el celular.")
    site_ld = {"@context": "https://schema.org", "@type": "WebSite", "name": CONFIG["name"], "url": abs_url(path), "inLanguage": lang}
    s = head(lang, title, desc, path, alt, [site_ld]) + header(lang, alt)
    s += '<section class="hero"><h1>%s</h1><p class="lead">%s</p>%s</section>' % (
        "Free calculators for everyday money" if lang == "en" else "Calculadoras gratis para el dinero de todos los días",
        E(u["tagline"]),
        '<input class="search" type="search" placeholder="%s" aria-label="%s" oninput="hcFilter(this.value)">' % (
            "Search: tip, salary, cups…" if lang == "en" else "Buscar: propina, sueldo, tazas…",
            "Search calculators" if lang == "en" else "Buscar calculadoras"))
    s += '<div id="all">'
    for cid, names in CATS.items():
        items = [c for c in CALCS if c["cat"] == cid]
        s += '<section class="cat" id="%s"><h2>%s</h2><div class="grid">' % (cid, names[0 if lang == "en" else 1])
        for c in items:
            s += '<a class="tile" href="%s" data-k="%s"><strong>%s</strong><span>%s</span></a>' % (
                url(lang, c[lang]["slug"]), E((c[lang]["h1"] + " " + c[lang]["title"]).lower()), E(c[lang]["h1"]), E(c[lang]["intro"]))
        s += '</div></section>'
    s += '</div>'
    if TOOLS_LIVE:
        s += '<section class="cat" id="tools"><h2>%s</h2><div class="grid">%s</div><p><a href="%s">%s →</a></p></section>' % (
            TOOL_UI[lang]["name"], tools_tiles(lang, TOOLS_LIVE[-6:][::-1]), TOOL_UI[lang]["hub"], "All tools" if lang == "en" else "Todas las herramientas")
    if lang == "en" and ARTICLES:
        s += '<section class="cat" id="guides"><h2>Guides</h2><div class="grid">%s</div><p><a href="/guides/">All guides →</a></p></section>' % "".join(
            '<a class="tile" href="/guides/%s/"><strong>%s</strong><span>%s</span></a>' % (a["slug"], E(a["h1"]), E(a["description"])) for a in list(reversed(ARTICLES))[:6])
    s += newsletter(lang)
    s += ("""<script>function hcFilter(q){q=q.toLowerCase().trim();document.querySelectorAll('.tile').forEach(function(t){t.style.display=!q||t.getAttribute('data-k').indexOf(q)>-1?'':'none'});document.querySelectorAll('.cat').forEach(function(c){c.style.display=[].some.call(c.querySelectorAll('.tile'),function(t){return t.style.display!=='none'})?'':'none'})}</script>""")
    s += footer(lang) + "</body></html>\n"
    return path, s

# ------------------------------ legal pages ------------------------------
def legal(lang, key):
    c = CONFIG; mail = c["email"]
    T = {}
    T["about"] = dict(
      en=("About Handy Calcs", f"""<p>{E(c['name'])} is a small collection of free, fast calculators for the money questions people have every day: how much to tip, how to split a check, what a dish should cost, what an hourly wage means per year, and how to make a household budget work.</p>
<p>Every calculator runs in your browser. We do not ask for your name or email and we do not store the numbers you type.</p>
<p>The site is made by {E(c['owner'])}, a small business in Utah, USA, with experience in restaurants and hospitality. It is available in English and Spanish.</p>
<p>Found a mistake or want a new calculator? Write to <a href="mailto:{mail}">{mail}</a>.</p>"""),
      es=("Quiénes somos", f"""<p>{E(c['name'])} es una colección de calculadoras gratis y rápidas para las preguntas de dinero de todos los días: cuánta propina dejar, cómo dividir la cuenta, cuánto cobrar un plato, cuánto es un sueldo por hora al año y cómo hacer que cierre el presupuesto de la casa.</p>
<p>Todas las calculadoras funcionan en tu navegador. No te pedimos nombre ni correo y no guardamos los números que escribes.</p>
<p>El sitio lo hace {E(c['owner'])}, una pequeña empresa de Utah, Estados Unidos, con experiencia en restaurantes y gastronomía. Está en inglés y en español.</p>
<p>¿Encontraste un error o quieres una calculadora nueva? Escríbenos a <a href="mailto:{mail}">{mail}</a>.</p>"""))
    T["privacy"] = dict(
      en=("Privacy Policy", f"""<p>Last updated: {TODAY}. This policy explains what data {E(c['name'])} ({abs_url('/')}), operated by {E(c['owner'])}, collects and why.</p>
<h2>Numbers you type</h2><p>All calculations happen on your device. The values you enter are not sent to us or stored.</p>
<h2>Analytics</h2><p>If you accept cookies, we use Google Analytics 4 to count visits and see which calculators are used. Google may collect your IP address (shortened), device and browser information, and pages visited. See <a href="https://policies.google.com/privacy" rel="noopener">Google's privacy policy</a>.</p>
<h2>Advertising</h2><p>We show ads through Google AdSense. Google and its partners use cookies to serve ads based on your visits to this and other websites. You can turn off personalized ads at <a href="https://adssettings.google.com" rel="noopener">Google Ads Settings</a> or <a href="https://www.aboutads.info" rel="noopener">aboutads.info</a>. If you choose "Necessary only", we ask Google to show non-personalized ads. Learn <a href="https://policies.google.com/technologies/partner-sites" rel="noopener">how Google uses data from partner sites</a>.</p>
<h2>Meta Pixel</h2><p>If you accept cookies, we use the Meta Pixel to measure visits that come from Facebook or Instagram ads. See <a href="https://www.facebook.com/privacy/policy/" rel="noopener">Meta's privacy policy</a>.</p>
<h2>Affiliate links</h2><p>Some pages contain affiliate links. If you buy through them we may earn a commission. The partner may set its own cookies when you click. As an Amazon Associate we earn from qualifying purchases.</p>
<h2>Your choices and rights</h2><p>You can change your cookie choice at any time with "Cookie settings" at the bottom of every page. Residents of California and other US states with privacy laws can ask what data is collected about them and request deletion; because we do not store personal data ourselves, requests about analytics and ads are handled by Google and Meta, and we will help you with them. We do not sell personal information. We honor Global Privacy Control signals as an opt-out of personalized ads.</p>
<h2>Children</h2><p>This site is not directed to children under 13 and we do not knowingly collect their data.</p>
<h2>Contact</h2><p><a href="mailto:{mail}">{mail}</a></p>"""),
      es=("Política de privacidad", f"""<p>Última actualización: {TODAY}. Esta política explica qué datos recoge {E(c['name'])} ({abs_url('/es/')}), operado por {E(c['owner'])}, y para qué.</p>
<h2>Los números que escribes</h2><p>Todos los cálculos se hacen en tu dispositivo. Los valores que ingresas no se nos envían ni se guardan.</p>
<h2>Estadísticas</h2><p>Si aceptas las cookies, usamos Google Analytics 4 para contar visitas y ver qué calculadoras se usan. Google puede recoger tu dirección IP (acortada), datos del dispositivo y del navegador, y las páginas visitadas. Mira la <a href="https://policies.google.com/privacy?hl=es" rel="noopener">política de privacidad de Google</a>.</p>
<h2>Publicidad</h2><p>Mostramos anuncios de Google AdSense. Google y sus socios usan cookies para mostrar anuncios según tus visitas a este y otros sitios. Puedes desactivar los anuncios personalizados en <a href="https://adssettings.google.com" rel="noopener">Configuración de anuncios de Google</a> o en <a href="https://www.aboutads.info" rel="noopener">aboutads.info</a>. Si eliges "Solo necesarias", le pedimos a Google que muestre anuncios no personalizados. Más información sobre <a href="https://policies.google.com/technologies/partner-sites?hl=es" rel="noopener">cómo usa Google los datos de sitios asociados</a>.</p>
<h2>Píxel de Meta</h2><p>Si aceptas las cookies, usamos el Píxel de Meta para medir las visitas que llegan desde anuncios de Facebook o Instagram. Mira la <a href="https://www.facebook.com/privacy/policy/" rel="noopener">política de privacidad de Meta</a>.</p>
<h2>Enlaces de afiliados</h2><p>Algunas páginas tienen enlaces de afiliados. Si compras a través de ellos podemos ganar una comisión. El socio puede usar sus propias cookies cuando haces clic. Como afiliados de Amazon, ganamos con las compras que califican.</p>
<h2>Tus opciones y derechos</h2><p>Puedes cambiar tu elección de cookies cuando quieras con "Configurar cookies" al pie de cada página. Los residentes de California y otros estados con leyes de privacidad pueden pedir saber qué datos se recogen y pedir que se borren; como nosotros no guardamos datos personales, esos pedidos los resuelven Google y Meta, y te ayudamos con ellos. No vendemos información personal. Respetamos la señal Global Privacy Control como rechazo de anuncios personalizados.</p>
<h2>Menores</h2><p>Este sitio no está dirigido a menores de 13 años y no recogemos sus datos a sabiendas.</p>
<h2>Contacto</h2><p><a href="mailto:{mail}">{mail}</a></p>"""))
    T["cookies"] = dict(
      en=("Cookie Policy", f"""<p>Cookies are small files a website saves in your browser. This is how {E(c['name'])} uses them.</p>
<table><tr><th>Cookie / storage</th><th>Who</th><th>Purpose</th><th>When</th></tr>
<tr><td>hc_consent (local storage)</td><td>Us</td><td>Remembers your cookie choice</td><td>Always</td></tr>
<tr><td>_ga, _ga_*</td><td>Google Analytics</td><td>Visit statistics (up to 2 years)</td><td>Only if you accept</td></tr>
<tr><td>_fbp</td><td>Meta</td><td>Ad measurement (3 months)</td><td>Only if you accept</td></tr>
<tr><td>__gads, __gpi, IDE and others</td><td>Google AdSense</td><td>Show and measure ads; personalized only if you accept</td><td>When ads are shown</td></tr></table>
<p>Change your choice: <a href="#" data-reset-cookies>open cookie settings</a>. You can also delete cookies in your browser settings.</p>"""),
      es=("Política de cookies", f"""<p>Las cookies son archivos niños que un sitio guarda en tu navegador. Así las usa {E(c['name'])}.</p>
<table><tr><th>Cookie / almacenamiento</th><th>Quién</th><th>Para qué</th><th>Cuándo</th></tr>
<tr><td>hc_consent (almacenamiento local)</td><td>Nosotros</td><td>Recordar tu elección de cookies</td><td>Siempre</td></tr>
<tr><td>_ga, _ga_*</td><td>Google Analytics</td><td>Estadísticas de visitas (hasta 2 años)</td><td>Solo si aceptas</td></tr>
<tr><td>_fbp</td><td>Meta</td><td>Medición de anuncios (3 meses)</td><td>Solo si aceptas</td></tr>
<tr><td>__gads, __gpi, IDE y otras</td><td>Google AdSense</td><td>Mostrar y medir anuncios; personalizados solo si aceptas</td><td>Cuando hay anuncios</td></tr></table>
<p>Cambiar tu elección: <a href="#" data-reset-cookies>abrir configuración de cookies</a>. También puedes borrar las cookies desde tu navegador.</p>"""))
    T["terms"] = dict(
      en=("Terms of Use", f"""<p>By using {E(c['name'])} you agree to these terms.</p>
<ol><li>The calculators are free and provided "as is". Results are estimates for general information and are not financial, tax, legal or professional advice.</li>
<li>We try to keep formulas and content correct but we do not guarantee accuracy. Check important numbers with a professional.</li>
<li>{E(c['owner'])} is not liable for decisions made using this site.</li>
<li>Do not copy the site or its content for commercial use without permission.</li>
<li>Pages may contain ads and affiliate links. We are not responsible for third-party websites.</li>
<li>These terms are governed by the laws of the State of Utah, USA.</li></ol>
<p>Contact: <a href="mailto:{mail}">{mail}</a></p>"""),
      es=("Términos de uso", f"""<p>Al usar {E(c['name'])} aceptas estos términos.</p>
<ol><li>Las calculadoras son gratis y se ofrecen "tal cual". Los resultados son estimaciones a modo informativo y no son asesoramiento financiero, impositivo, legal ni profesional.</li>
<li>Tratamos de que las fórmulas y el contenido sean correctos, pero no garantizamos su exactitud. Verifica los números importantes con un profesional.</li>
<li>{E(c['owner'])} no se hace responsable de las decisiones tomadas con este sitio.</li>
<li>No copies el sitio ni su contenido para uso comercial sin permiso.</li>
<li>Las páginas pueden tener anuncios y enlaces de afiliados. No somos responsables de sitios de terceros.</li>
<li>Estos términos se rigen por las leyes del Estado de Utah, EE. UU.</li></ol>
<p>Contacto: <a href="mailto:{mail}">{mail}</a></p>"""))
    T["advertise"] = dict(
      en=("Advertise with Handy Calcs", f"""<p>{E(c['name'])} helps people in the US with everyday money decisions in English and Spanish: restaurant workers and owners, home cooks, families on a budget and hourly workers.</p>
<h2>What we offer</h2><ol><li><strong>Sponsored placement</strong> on a related calculator page (for example a restaurant software on the menu price calculator).</li>
<li><strong>Sponsored article or guide</strong> written by us, useful to readers and clearly labeled as sponsored.</li>
<li><strong>Newsletter mention</strong> in our weekly email.</li></ol>
<h2>Our rules</h2><ul><li>Every paid link is labeled "Sponsored" and uses rel="sponsored", as Google requires.</li>
<li>We only accept products we would recommend to our own readers. No gambling, payday loans, crypto schemes or adult content.</li>
<li>Sponsors never change calculator results.</li></ul>
<p>Write to <a href="mailto:{mail}?subject=Advertising%20on%20Handy%20Calcs">{mail}</a> with your product, the pages you are interested in and your budget. We reply within 3 business days.</p>"""),
      es=("Publicidad en Handy Calcs", f"""<p>{E(c['name'])} ayuda a personas en EE. UU. con decisiones de dinero de todos los días, en inglés y en español: trabajadores y dueños de restaurantes, gente que cocina en casa, familias con presupuesto y trabajadores por hora.</p>
<h2>Qué ofrecemos</h2><ol><li><strong>Lugar patrocinado</strong> en una calculadora relacionada (por ejemplo un software para restaurantes en la calculadora de precio de menú).</li>
<li><strong>Artículo o guía patrocinada</strong> escrita por nosotros, útil para los lectores y marcada como patrocinada.</li>
<li><strong>Mención en el newsletter</strong> semanal.</li></ol>
<h2>Nuestras reglas</h2><ul><li>Todo enlace pago lleva la etiqueta "Patrocinado" y rel="sponsored", como pide Google.</li>
<li>Solo aceptamos productos que les recomendaríamos a nuestros lectores. Nada de apuestas, préstamos de día de pago, esquemas cripto ni contenido para adultos.</li>
<li>Los patrocinadores nunca cambian los resultados de las calculadoras.</li></ul>
<p>Escríbenos a <a href="mailto:{mail}?subject=Publicidad%20en%20Handy%20Calcs">{mail}</a> con tu producto, las páginas que te interesan y tu presupuesto. Respondemos en 3 días hábiles.</p>"""))
    title, body = T[key][lang]
    path = ("/" if lang == "en" else "/es/") + key + "/"
    alt = ("/es/" if lang == "en" else "/") + key + "/"
    blurb = (" for Handy Calcs, free online calculators for tips, recipes, pay and budgets." if lang == "en"
             else " de Handy Calcs, calculadoras gratis de propinas, recetas, sueldo y presupuesto.")
    s = head(lang, "%s | %s" % (title, CONFIG["name"]), title + blurb, path, alt) + header(lang, alt)
    s += '<article class="content legal"><h1>%s</h1>%s</article>' % (E(title), body)
    s += footer(lang) + "</body></html>\n"
    return path, s


# ------------------------------ guides (articles) ------------------------------
# Articles written in advance in src/articles/NN-<slug>.html ("key: value" header, a "---" line, then the HTML body).
# NN sets the order: 01 goes live on ARTICLES_START, 02 the next day, and so on. The daily workflow (8 AM Utah) runs build.py,
# so each article appears on its day by itself, free and without Claude. To add more, add files with the next number.
import re as _re
ARTICLES_START = datetime.date(2026, 11, 16)
def load_articles():
    d = os.path.join(ROOT, "src", "articles"); out = []
    for f in sorted(os.listdir(d)) if os.path.isdir(d) else []:
        m = _re.match(r"(\d+)-([a-z0-9-]+)\.html$", f)
        if not m: continue
        head_, body = open(os.path.join(d, f), encoding="utf-8").read().split("\n---\n", 1)
        a = dict(line.split(": ", 1) for line in head_.strip().splitlines())
        a.update(n=int(m.group(1)), slug=m.group(2), body=body.strip())
        a["calcs"] = [x.strip() for x in a.get("calcs", "").split(",") if x.strip() in BY_ID]
        a["live"] = ARTICLES_START + datetime.timedelta(days=a["n"] - 1)
        out.append(a)
    return out
ALL_ARTICLES = load_articles()
ARTICLES = [a for a in ALL_ARTICLES if a["live"] <= datetime.date.fromisoformat(TODAY)]

def guides_for(cid):
    return [a for a in ARTICLES if cid in a["calcs"]]

def article_page(a):
    path = "/guides/%s/" % a["slug"]
    ld = [{"@context": "https://schema.org", "@type": "Article", "headline": a["h1"], "description": a["description"],
           "datePublished": a["live"].isoformat(), "inLanguage": "en", "mainEntityOfPage": abs_url(path),
           "author": {"@type": "Organization", "name": CONFIG["name"]}, "publisher": {"@type": "Organization", "name": CONFIG["name"]}},
          {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
              {"@type": "ListItem", "position": 1, "name": CONFIG["name"], "item": abs_url("/")},
              {"@type": "ListItem", "position": 2, "name": "Guides", "item": abs_url("/guides/")},
              {"@type": "ListItem", "position": 3, "name": a["h1"], "item": abs_url(path)}]}]
    tiles = "".join('<a class="tile" href="%s"><strong>%s</strong><span>%s</span></a>' % (url("en", BY_ID[c]["en"]["slug"]), E(BY_ID[c]["en"]["h1"]), E(BY_ID[c]["en"]["intro"])) for c in a["calcs"])
    more = "".join('<a class="rel" href="/guides/%s/">%s</a>' % (o["slug"], E(o["h1"])) for o in reversed(ARTICLES) if o is not a)[:4000]
    s = head("en", a["title"], a["description"], path, None, ld) + header("en", None)
    s += '<nav class="crumbs"><a href="/">Home</a> › <a href="/guides/">Guides</a></nav>'
    s += '<article class="content post"><p class="kicker">Guide · %s</p><h1>%s</h1>%s</article>' % (a["live"].strftime("%B %d, %Y").replace(" 0", " "), E(a["h1"]), a["body"])
    if tiles: s += '<section class="content"><h2>Calculators for this</h2><div class="grid">%s</div></section>' % tiles
    s += newsletter("en")
    if more: s += '<section class="content"><h2>More guides</h2><div class="rels">%s</div></section>' % more
    s += footer("en") + "</body></html>\n"
    return path, s

def guides_index():
    path = "/guides/"
    tiles = "".join('<a class="tile" href="/guides/%s/"><strong>%s</strong><span>%s</span></a>' % (a["slug"], E(a["h1"]), E(a["description"])) for a in reversed(ARTICLES))
    s = head("en", "Money, Pay and Kitchen Guides | " + CONFIG["name"], "Plain-English guides to tipping, pay, budgets, debt, discounts and kitchen math, each with a free calculator.", path, None) + header("en", None)
    s += '<h1>Guides</h1><p class="lead">Plain-English guides to everyday money and kitchen math, each with a free calculator. A new guide every day.</p><div class="grid">%s</div>' % tiles
    s += footer("en") + "</body></html>\n"
    return path, s

# ------------------------------ online tools (/tools/ and /es/herramientas/) ------------------------------
# Definitions and texts in src/tools.py, widgets in src/tools.js (everything runs in the visitor's browser).
# Drip (Azu's rule: a little every day): tools n=1 and n=2 go live on TOOLS_START, then one more tool per day (EN + ES).
# The daily workflow runs build.py at 8 AM Utah, so each tool appears on its day by itself, free and without Claude.
# To add tools: add entries to src/tools.py with the next "n".
import tools as TL
TOOLS_START = datetime.date(2026, 11, 16)
def tool_live(x): return TOOLS_START + datetime.timedelta(days=max(0, x["n"] - 2))
TOOLS_LIVE = sorted([x for x in TL.TOOLS if tool_live(x) <= datetime.date.fromisoformat(TODAY)], key=lambda x: x["n"])
LIVE_IDS = {x["id"] for x in TOOLS_LIVE}
TOOL_UI = {"en": dict(hub="/tools/", name="Free online tools", short="Tools", how="How to use it", faq="Frequently asked questions", more="More free tools",
                      priv="Private: everything happens on your device. Nothing you type or upload is sent anywhere."),
           "es": dict(hub="/es/herramientas/", name="Herramientas online gratis", short="Herramientas", how="Cómo se usa", faq="Preguntas frecuentes", more="Más herramientas gratis",
                      priv="Privado: todo pasa en tu dispositivo. Nada de lo que escribes o subes se envía a ningún lado.")}

def tool_url(x, lang):
    return TOOL_UI[lang]["hub"] + x[lang]["slug"] + "/"

def tools_css(s):
    return s.replace("</head>", '<link rel="stylesheet" href="/tools.css?v=%s">\n</head>' % CSS_VER, 1)

def tool_page(x, lang):
    d = x[lang]; other = "es" if lang == "en" else "en"; tu = TOOL_UI[lang]
    path = tool_url(x, lang); alt = tool_url(x, other)
    app_ld = {"@context": "https://schema.org", "@type": "WebApplication", "name": d["h1"], "url": abs_url(path),
              "applicationCategory": "UtilitiesApplication", "operatingSystem": "Any", "inLanguage": lang, "browserRequirements": "Requires JavaScript",
              "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "description": d["desc"]}
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in d["faq"]]}
    howto = {"@context": "https://schema.org", "@type": "HowTo", "name": d["h1"], "inLanguage": lang,
             "step": [{"@type": "HowToStep", "position": i + 1, "text": st} for i, st in enumerate(d["steps"])]}
    crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": CONFIG["name"], "item": abs_url(url(lang))},
        {"@type": "ListItem", "position": 2, "name": tu["name"], "item": abs_url(tu["hub"])},
        {"@type": "ListItem", "position": 3, "name": d["h1"], "item": abs_url(path)}]}
    faq = "".join('<details><summary>%s</summary><p>%s</p></details>' % (E(q), E(a)) for q, a in d["faq"])
    rel_ids = [r for r in x["related"] if r in LIVE_IDS] + [o["id"] for o in TOOLS_LIVE if o["id"] not in x["related"] and o is not x]
    rel = "".join('<a class="rel" href="%s">%s</a>' % (tool_url(TL.BY_ID[r], lang), E(TL.BY_ID[r][lang]["h1"])) for r in rel_ids[:8])
    steps = "".join("<li>%s</li>" % E(st) for st in d["steps"])
    s = tools_css(head(lang, d["title"], d["desc"], path, alt, [app_ld, howto, faq_ld, crumbs])) + header(lang, alt)
    s += f"""<nav class="crumbs"><a href="{url(lang)}">{UI[lang]['home']}</a> › <a href="{tu['hub']}">{E(tu['name'])}</a></nav>
<h1>{E(d['h1'])}</h1>
<p class="lead">{E(d['intro'])}</p>
{TL.widget(x, lang)}
<p class="small priv">🔒 {tu['priv']}</p>
<section class="content"><h2>{tu['how']}</h2><ol class="tool-steps">{steps}</ol>{d['body']}</section>
{newsletter(lang)}
<section class="content"><h2>{tu['faq']}</h2>{faq}</section>
{'<section class="content"><h2>%s</h2><div class="rels">%s</div></section>' % (tu['more'], rel) if rel else ''}
<p class="small upd">{'Updated' if lang == 'en' else 'Actualizado'}: {TODAY}</p>
"""
    extra = '<script src="/vendor/qrcode.js?v=%s" defer></script>\n' % CSS_VER if x["engine"] == "qr" else ""
    s += footer(lang) + extra + '<script src="/tools.js?v=%s" defer></script>\n</body></html>\n' % CSS_VER
    return path, s

def tools_tiles(lang, items):
    return "".join('<a class="tile" href="%s"><strong>%s</strong><span>%s</span></a>' % (tool_url(x, lang), E(x[lang]["h1"]), E(x[lang]["intro"])) for x in items)

def tools_hub(lang):
    tu = TOOL_UI[lang]; other = "es" if lang == "en" else "en"
    path = tu["hub"]; alt = TOOL_UI[other]["hub"]
    title = ("Free Online Tools: QR Codes, Images, Text and Random Pickers | " if lang == "en" else "Herramientas online gratis: códigos QR, imágenes, texto y sorteos | ") + CONFIG["name"]
    desc = ("Free tools that work in your browser: QR code generator, image compressor, word counter, name picker wheel, password generator and more. No sign-up, nothing uploaded."
            if lang == "en" else "Herramientas gratis que funcionan en tu navegador: generador de QR, comprimir imágenes, contador de palabras, ruleta de nombres, contraseñas y más. Sin registro y sin subir nada.")
    s = tools_css(head(lang, title, desc, path, alt)) + header(lang, alt)
    s += '<h1>%s</h1><p class="lead">%s</p>' % (E(tu["name"]), E(tu["priv"]) + (" A new tool almost every day." if lang == "en" else " Una herramienta nueva casi todos los días."))
    for cid, names in TL.CATS.items():
        items = [x for x in TOOLS_LIVE if x["cat"] == cid]
        if items: s += '<section class="cat"><h2>%s</h2><div class="grid">%s</div></section>' % (names[0 if lang == "en" else 1], tools_tiles(lang, items))
    s += footer(lang) + "</body></html>\n"
    return path, s

def write(path, content):
    fp = os.path.join(OUT, path.strip("/"), "index.html") if path.endswith("/") else os.path.join(OUT, path.strip("/"))
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    with open(fp, "w", encoding="utf-8") as f: f.write(content)

def main():
    if os.path.exists(OUT): shutil.rmtree(OUT)
    os.makedirs(OUT)
    cal_ys = copy_calendars()
    herr_locs = build_herramientas() + copy_imprimibles()
    build_pines()
    pages = []
    for lang in ("en", "es"):
        pages.append(home_page(lang))
        for c in CALCS: pages.append(calc_page(c, lang)); pages.append(embed_page(c, lang))
        for k in ("about", "privacy", "cookies", "terms", "advertise"): pages.append(legal(lang, k))
    if TOOLS_LIVE:
        for lang in ("en", "es"):
            pages.append(tools_hub(lang))
            for x in TOOLS_LIVE: pages.append(tool_page(x, lang))
    if ARTICLES:
        pages.append(guides_index())
        for a in ARTICLES: pages.append(article_page(a))
    for p, s in pages: write(p, s)
    # Pinterest pins for every calculator and guide, 2 a day (tools/pines_calculadoras.py, queue in pines/calculadoras/cola.json)
    sys.path.insert(0, os.path.join(ROOT, "tools"))
    import pines_calculadoras
    pines_calculadoras.build(OUT, CALCS, CATS, ALL_ARTICLES, CONFIG["site_url"], TODAY)
    # chips: presets click -> set input (inline in calc.js would need ids; tiny add-on)
    for f in ("style.css", "cookie.css", "site.js", "calc.js", "favicon.svg", "og-image.png", "tools.js", "tools.css"):
        shutil.copy(os.path.join(ROOT, "src", f), os.path.join(OUT, f))
    os.makedirs(os.path.join(OUT, "vendor"), exist_ok=True)
    shutil.copy(os.path.join(ROOT, "src", "vendor", "qrcode.js"), os.path.join(OUT, "vendor", "qrcode.js"))
    with open(os.path.join(OUT, "calc.js"), "a", encoding="utf-8") as f:
        f.write("""
document.querySelectorAll('[data-set]').forEach(function(b){b.addEventListener('click',function(){var i=document.getElementById(b.getAttribute('data-set'));i.value=b.getAttribute('data-val');i.dispatchEvent(new Event('input',{bubbles:true}));});});
""")
    # 404
    nf = head("en", "Page not found | " + CONFIG["name"], "Page not found", "/404.html", None) + header("en", "/es/")
    nf += '<h1>Page not found</h1><p>Página no encontrada.</p><p><a class="btn" href="/">All calculators</a> <a class="btn-ghost" href="/es/">Todas las calculadoras</a></p>' + footer("en") + "</body></html>"
    write("/404.html", nf)
    # sitemap with hreflang
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    pairs = [(url("en"), url("es"))] + [(url("en", c["en"]["slug"]), url("es", c["es"]["slug"])) for c in CALCS] + \
            [("/%s/" % k, "/es/%s/" % k) for k in ("about", "privacy", "cookies", "terms", "advertise")]
    pairs += [(cal_paths(y)[1], cal_paths(y)[0]) for y in cal_ys]
    if TOOLS_LIVE:
        pairs += [(TOOL_UI["en"]["hub"], TOOL_UI["es"]["hub"])] + [(tool_url(x, "en"), tool_url(x, "es")) for x in TOOLS_LIVE]
    for en_p, es_p in pairs:
        for p in (en_p, es_p):
            sm.append('<url><loc>%s</loc><lastmod>%s</lastmod><xhtml:link rel="alternate" hreflang="en" href="%s"/><xhtml:link rel="alternate" hreflang="es" href="%s"/></url>'
                      % (abs_url(p), TODAY, abs_url(en_p), abs_url(es_p)))
    if ARTICLES:
        sm.append("<url><loc>%s</loc><lastmod>%s</lastmod></url>" % (abs_url("/guides/"), TODAY))
        for a in ARTICLES:
            sm.append("<url><loc>%s</loc><lastmod>%s</lastmod></url>" % (abs_url("/guides/%s/" % a["slug"]), a["live"].isoformat()))
    for loc in herr_locs:
        sm.append("<url><loc>%s</loc><lastmod>%s</lastmod></url>" % (loc, TODAY))
    sm.append("</urlset>")
    write("/sitemap.xml", "\n".join(sm) + "\n")
    write("/%s.txt" % INDEXNOW_KEY, INDEXNOW_KEY + "\n")
    write("/robots.txt", "User-agent: *\nAllow: /\n\nSitemap: %s\n" % abs_url("/sitemap.xml"))
    if CONFIG["adsense"]:
        write("/ads.txt", "google.com, %s, DIRECT, f08c47fec0942fa0\n" % CONFIG["adsense"].replace("ca-", ""))
    write("/_headers", "/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n/*.css\n  Cache-Control: public, max-age=86400\n/*.js\n  Cache-Control: public, max-age=86400\n")
    print("Built %d pages into %s (guides %d/%d, tools %d/%d)" % (len(pages) + 1, OUT, len(ARTICLES), len(ALL_ARTICLES), len(TOOLS_LIVE), len(TL.TOOLS)))

if __name__ == "__main__":
    main()
