#!/usr/bin/env python3
"""Arma la sección "Herramientas gratis para emprender online" de Handy Calcs.

Uso:
  # Vista previa con TODAS las páginas (noindex, para revisar):
  python3 generar.py --todo --salida vista-previa/herramientas-gratis

  # Lo que va a la web, respetando el goteo (2-3 por día; solo páginas ya salidas):
  python3 generar.py --inicio 2026-11-27 [--hoy 2026-11-28]

Lee: contenido.py (textos), orden.txt (orden de salida), afiliados.json (links).
Escribe en --salida: páginas HTML ya salidas, estilos.css, img/pins/*.png (todas),
rss-completo.xml (todas, en orden; goteo.py arma rss.xml) y sitemap-herramientas.xml.
Las páginas que todavía no salieron NO se escriben (y se borran si estaban).
Necesita: pip install pillow
"""
import argparse, datetime as dt, html, importlib.util, json, os, re, sys
from email.utils import format_datetime

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import contenido as C  # noqa: E402

URL_BASE = "https://gethandycalcs.pages.dev/herramientas-gratis/"
GOTEO_DEF = os.path.normpath(os.path.join(AQUI, "..", "tools", "goteo.py"))


# ------------------------------------------------------------------ utilidades
def leer_orden():
    with open(os.path.join(AQUI, "orden.txt"), encoding="utf-8") as f:
        orden = [l.strip() for l in f if l.strip() and not l.startswith("#")]
    faltan = [s for s in orden if s not in C.PAGINAS]
    if faltan:
        sys.exit(f"orden.txt nombra páginas que no existen en contenido.py: {faltan}")
    sin_orden = [s for s in C.PAGINAS if s not in orden]
    if sin_orden:
        print(f"Aviso: páginas sin lugar en orden.txt (no salen): {sin_orden}")
    return orden


def funcion_dia(goteo_path):
    """Usa la misma cuenta que goteo.py para que web y RSS salgan juntos."""
    if os.path.exists(goteo_path):
        spec = importlib.util.spec_from_file_location("goteo", goteo_path)
        m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
        return m.dia_de_salida
    print(f"Aviso: no encontré {goteo_path}; uso la cuenta 2+3 por defecto.")
    def dia(i, inicio):
        b, r = divmod(i, 5)
        return inicio + dt.timedelta(days=b * 2 + (0 if r < 2 else 1))
    return dia


def archivo(slug):
    return "index.html" if slug == "index" else slug + ".html"


def url_rel(slug):
    return "./" if slug == "index" else slug + ".html"


def esc(t):
    return html.escape(t, quote=True)


def texto_plano(h):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", h))).strip()


# ------------------------------------------------------------------ links
def resolver_links(h, afiliados, publicadas):
    usados = set()

    def aff(m):
        clave = m.group(1)
        a = afiliados.get(clave)
        if not a:
            sys.exit(f"Falta {clave} en afiliados.json")
        usados.add(clave)
        url = a.get("url_afiliado") or a["url_oficial"]
        rel = "sponsored nofollow noopener" if a.get("programa") else "nofollow noopener"
        return f'href="{esc(url)}" rel="{rel}" target="_blank" data-aff="{clave}"'

    h = re.sub(r'href="(AFF_[A-Z0-9_]+)"', aff, h)

    def pag(m):
        slug, texto = m.group(1), m.group(2)
        if slug not in C.PAGINAS:
            sys.exit(f"Link interno a página inexistente: {slug}")
        if slug in publicadas:
            return f'<a href="{url_rel(slug)}">{texto}</a>'
        return texto  # todavía no salió: queda el texto sin link

    h = re.sub(r'<a href="PAG:([a-z0-9-]+)">(.*?)</a>', pag, h, flags=re.S)
    return h, usados


# ------------------------------------------------------------------ HTML
CSS = """*{box-sizing:border-box}
body{margin:0;font-family:system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif;color:#2f2b27;background:#faf8f4;line-height:1.6}
.hg-wrap{max-width:820px;margin:0 auto;padding:22px 18px 48px}
.hg-migas{font-size:.85rem;color:#6c645b}.hg-migas a{color:#55663f}
.hg-aviso{background:#fff7e0;border:1px solid #e8d49a;border-radius:8px;padding:10px 14px;font-size:.9rem;margin:12px 0 18px}
h1{font-size:clamp(1.7rem,4vw,2.4rem);line-height:1.2;margin:.3em 0;color:#3f4a38}
h2{margin-top:2em;color:#3f4a38;border-bottom:2px solid #d9cfbf;padding-bottom:4px}
h3{margin-top:1.4em}
.hg-meta{font-size:.88rem;color:#6c645b;margin-bottom:1em}
.hg-wrap a{color:#4a6d2f}
.tabla-scroll{overflow-x:auto}
table{border-collapse:collapse;width:100%;font-size:.93rem;background:#fff}
th,td{border:1px solid #e1d8ca;padding:8px 10px;text-align:left;vertical-align:top}
th{background:#eef1ea}
.hg-ad{margin:26px 0;min-height:90px;text-align:center}
.hg-faq h3{font-size:1.02rem;margin:18px 0 4px}
.hg-fuentes{font-size:.88rem}
.hg-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:16px;padding:0;list-style:none}
.hg-grid li{background:#fff;border:1px solid #e6ddcf;border-radius:10px;padding:14px}
.hg-grid li a{font-weight:600;text-decoration:none}
.hg-grid li p{margin:6px 0 0;font-size:.92rem;color:#5b544c}
.hg-pronto{font-size:.92rem;color:#6c645b}
footer{margin-top:44px;font-size:.85rem;color:#6c645b;border-top:1px solid #e6ddcf;padding-top:14px}
"""


def schema(p, slug, url_base, hoy):
    url = url_base + ("" if slug == "index" else archivo(slug))
    faq = {"@context": "https://schema.org", "@type": "FAQPage",
           "mainEntity": [{"@type": "Question", "name": q,
                           "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in p["faq"]]}
    migas = [{"@type": "ListItem", "position": 1, "name": "Handy Calcs", "item": url_base.split("/herramientas")[0] + "/"},
             {"@type": "ListItem", "position": 2, "name": "Herramientas gratis", "item": url_base}]
    if slug != "index":
        migas.append({"@type": "ListItem", "position": 3, "name": p["h1"], "item": url})
    bc = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": migas}
    art = {"@context": "https://schema.org", "@type": "Article", "headline": p["h1"], "inLanguage": "es",
           "author": {"@type": "Person", "name": "Azu"},
           "publisher": {"@type": "Organization", "name": "Skye Solutions AI"},
           "dateModified": hoy.isoformat(), "image": url_base + f"img/pins/{slug}.png", "mainEntityOfPage": url}
    return "\n".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in (faq, bc, art))


def pagina(slug, p, orden, publicadas, afiliados, url_base, hoy, preview):
    rev = C.REVISADO
    cuerpo = p["cuerpo"]
    if p.get("es_hub"):
        items = []
        for s in orden:
            if s == "index":
                continue
            q = C.PAGINAS[s]
            if s in publicadas:
                items.append(f'<li><a href="PAG:{s}">{esc(q["h1"])}</a><p>{esc(q["resumen"])}</p></li>')
        lista = '<ul class="hg-grid">' + "\n".join(items) + "</ul>" if items else ""
        pendientes = sum(1 for s in orden if s != "index" and s not in publicadas)
        if pendientes:
            lista += f'\n<p class="hg-pronto">Estamos sumando guías nuevas cada semana.</p>'
        cuerpo = cuerpo.replace("{{LISTA_GUIAS}}", lista)
    intro = p["intro"].replace("{rev}", rev)
    faq_html = "\n".join(f"<h3>{esc(q)}</h3>\n<p>{esc(a)}</p>" for q, a in p["faq"])
    fuentes = ""
    if p["fuentes"]:
        li = "\n".join(f'<li><a href="{esc(C.F[k][1])}" rel="nofollow noopener" target="_blank">{esc(C.F[k][0])}</a></li>' for k in p["fuentes"])
        fuentes = f'<section class="hg-fuentes"><h2>Fuentes (consultadas en {rev})</h2>\n<ol>\n{li}\n</ol></section>'
    relacionadas = [s for s in orden if s not in ("index", slug) and s in publicadas]
    rel_html = ""
    if relacionadas and not p.get("es_hub"):
        rel_html = "<h2>Más guías</h2>\n<ul>" + "".join(f'<li><a href="PAG:{s}">{esc(C.PAGINAS[s]["h1"])}</a></li>' for s in relacionadas[:5]) + "</ul>"
    cuerpo_total = "\n".join([intro, '<div class="hg-ad"><!-- ADSENSE bloque 1 --></div>', cuerpo,
                              '<div class="hg-ad"><!-- ADSENSE bloque 2 --></div>',
                              f'<section class="hg-faq"><h2>Preguntas frecuentes</h2>\n{faq_html}</section>', fuentes, rel_html])
    cuerpo_total, usados = resolver_links(cuerpo_total, afiliados, publicadas)
    con_programa = any(afiliados[k].get("programa") for k in usados)
    if p.get("es_hub") or con_programa:
        aviso = ("<strong>Aviso:</strong> algunos enlaces de esta guía son de afiliado. Si te registras o pagas un plan "
                 "desde ellos, podemos recibir una comisión, sin costo extra para ti. Eso no cambia lo que recomendamos: "
                 "también incluimos herramientas que no nos pagan nada.")
    else:
        aviso = ("<strong>Aviso:</strong> esta página no tiene enlaces de afiliado. Otras guías de esta sección sí tienen; "
                 "si te registras desde ellos, podemos recibir una comisión sin costo extra para ti.")
    url = url_base + ("" if slug == "index" else archivo(slug))
    migas = '<a href="/">Handy Calcs</a> › ' + ('Herramientas gratis' if slug == "index" else '<a href="./">Herramientas gratis</a> › ' + esc(p["h1"]))
    robots = '<meta name="robots" content="noindex,nofollow">\n' if preview else ""
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(p["titulo"])}</title>
<meta name="description" content="{esc(p["meta"])}">
{robots}<link rel="canonical" href="{url}">
<meta property="og:type" content="article">
<meta property="og:locale" content="es_US">
<meta property="og:title" content="{esc(p["titulo"])}">
<meta property="og:description" content="{esc(p["meta"])}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{url_base}img/pins/{slug}.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="alternate" type="application/rss+xml" title="Herramientas gratis para emprender" href="{url_base}rss.xml">
<link rel="stylesheet" href="estilos.css">
<!-- GA4 -->
<!-- ADSENSE (script de anuncios automáticos) -->
{schema(p, slug, url_base, hoy)}
</head>
<body>
<div class="hg-wrap">
<nav class="hg-migas" aria-label="Migas de pan">{migas}</nav>
<p class="hg-aviso">{aviso}</p>
<header>
<h1>{esc(p["h1"])}</h1>
<p class="hg-meta">Por {esc(C.AUTORA)} · Revisado en {rev}</p>
</header>
<main>
{cuerpo_total}
</main>
<footer>
<p>Por {esc(C.AUTORA)}. Usamos estas herramientas en nuestro propio negocio. Los precios y límites pueden cambiar: confirma siempre en la página oficial.</p>
<p><a href="/privacidad.html"><!-- PRIVACIDAD -->Política de privacidad</a> · <a href="./">Todas las guías</a></p>
</footer>
</div>
</body>
</html>
"""


# ------------------------------------------------------------------ pins
def pins(dir_img, orden, pie):
    from PIL import Image, ImageDraw, ImageFont
    fb = os.path.join(AQUI, "fonts", "Carlito-Bold.ttf")
    fr = os.path.join(AQUI, "fonts", "Carlito-Regular.ttf")
    os.makedirs(dir_img, exist_ok=True)
    W, H = 1000, 1500
    for slug in orden:
        p = C.PAGINAS[slug]
        oscuro, claro = p["color"]
        im = Image.new("RGB", (W, H), claro)
        d = ImageDraw.Draw(im)
        d.rectangle([0, 0, W, 26], fill=oscuro)
        d.rectangle([0, H - 150, W, H], fill=oscuro)
        lineas, sub = p["pin"][:3], p["pin"][3]
        # tamaño de letra que entra en 860 px
        def ajusta(texto, maximo, fuente):
            t = maximo
            while t > 30:
                f = ImageFont.truetype(fuente, t)
                if d.textlength(texto, font=f) <= 860:
                    return f
                t -= 4
            return ImageFont.truetype(fuente, 30)
        fuentes = [ajusta(l, 150, fb) for l in lineas]
        tam = min(f.size for f in fuentes)
        f = ImageFont.truetype(fb, tam)
        alto_linea = int(tam * 1.12)
        fs = ajusta(sub, 66, fr)
        bloque = alto_linea * len(lineas) + 40 + 30 + fs.size
        y = (H - 150 - bloque) // 2 + 10
        for l in lineas:
            d.text((W // 2, y), l, font=f, fill=oscuro, anchor="ma")
            y += alto_linea
        y += 30
        d.rectangle([W // 2 - 70, y, W // 2 + 70, y + 8], fill=oscuro)
        y += 40
        d.text((W // 2, y), sub, font=fs, fill=oscuro, anchor="ma")
        fp = ImageFont.truetype(fb, 46)
        d.text((W // 2, H - 75), pie, font=fp, fill=claro, anchor="mm")
        fe = ImageFont.truetype(fr, 30)
        d.text((W // 2, 70), "GUÍA GRATIS EN ESPAÑOL", font=fe, fill=oscuro, anchor="mm")
        im.save(os.path.join(dir_img, f"{slug}.png"), optimize=True)


# ------------------------------------------------------------------ RSS y sitemap
def rss(path, orden, url_base, ahora):
    items = []
    for slug in orden:
        p = C.PAGINAS[slug]
        url = url_base + ("" if slug == "index" else archivo(slug))
        img = url_base + f"img/pins/{slug}.png"
        items.append(f"""  <item>
    <title>{esc(p["titulo"])}</title>
    <link>{url}</link>
    <guid isPermaLink="true">{url}</guid>
    <description>{esc(p["meta"])}</description>
    <enclosure url="{img}" type="image/png" length="0"/>
    <media:content url="{img}" type="image/png" medium="image" width="1000" height="1500"/>
  </item>""")
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:media="http://search.yahoo.com/mrss/" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
  <title>Herramientas gratis para emprender online</title>
  <link>{url_base}</link>
  <atom:link href="{url_base}rss.xml" rel="self" type="application/rss+xml"/>
  <description>Guías en español de herramientas gratis para vender productos digitales y emprender online.</description>
  <language>es</language>
  <lastBuildDate>{format_datetime(ahora)}</lastBuildDate>
{chr(10).join(items)}
</channel>
</rss>
"""
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(xml)


def sitemap(path, publicadas, orden, url_base, hoy):
    urls = "\n".join(f"  <url><loc>{url_base + ('' if s == 'index' else archivo(s))}</loc><lastmod>{hoy.isoformat()}</lastmod></url>"
                     for s in orden if s in publicadas)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n')


# ------------------------------------------------------------------ GA4, AdSense, cookies (Handy Calcs)
def marcadores(h, a):
    """Rellena <!-- GA4 -->, <!-- ADSENSE ... --> y <!-- PRIVACIDAD --> con lo mismo que usa Handy Calcs:
    GA4/Pixel/AdSense solo cargan si la persona acepta cookies (lo maneja /site.js). Los IDs llegan
    por --ga4, --pixel y --adsense (build.py de Handy Calcs los pasa desde su CONFIG)."""
    if a.todo:  # vista previa: sin seguimiento ni anuncios
        return h
    hc = '<script>window.HC=%s;</script>' % json.dumps({"ga4": a.ga4, "pixel": a.pixel})
    ads = ""
    if a.adsense:
        ads = ('<script>window.adsbygoogle=window.adsbygoogle||[];window.adsbygoogle.pauseAdRequests=1;</script>'
               '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=%s" '
               'crossorigin="anonymous"></script>' % a.adsense)
    h = h.replace("<!-- GA4 -->", hc, 1)
    h = h.replace("<!-- ADSENSE (script de anuncios automáticos) -->", ads, 1)
    h = re.sub(r'<div class="hg-ad"><!-- ADSENSE bloque \d+ --></div>\n?', "", h)  # anuncios automáticos: se ubican solos
    h = h.replace('<a href="/privacidad.html"><!-- PRIVACIDAD -->', '<a href="%s">' % a.privacidad)
    h = h.replace('<link rel="stylesheet" href="estilos.css">',
                  '<link rel="stylesheet" href="/cookie.css"><link rel="stylesheet" href="estilos.css">', 1)
    h = h.replace("</body>", '<script src="/site.js" defer></script>\n</body>', 1)
    return h


# ------------------------------------------------------------------ main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", default=URL_BASE)
    ap.add_argument("--salida", default=os.path.join(AQUI, "sitio", "herramientas-gratis"))
    ap.add_argument("--todo", action="store_true", help="vista previa: todas las páginas, con noindex")
    ap.add_argument("--inicio", help="día 1 del goteo (AAAA-MM-DD)")
    ap.add_argument("--hoy", default=dt.date.today().isoformat())
    ap.add_argument("--goteo", default=GOTEO_DEF)
    ap.add_argument("--pie", default="gethandycalcs.pages.dev")
    ap.add_argument("--sin-pins", action="store_true")
    ap.add_argument("--ga4", default="", help="ID de GA4 (G-...)")
    ap.add_argument("--pixel", default="", help="ID del Pixel de Meta")
    ap.add_argument("--adsense", default="", help="ID de AdSense (ca-pub-...)")
    ap.add_argument("--privacidad", default="/es/privacy/", help="URL de la política de privacidad")
    a = ap.parse_args()
    url_base = a.url if a.url.endswith("/") else a.url + "/"
    hoy = dt.date.fromisoformat(a.hoy)
    orden = leer_orden()
    with open(os.path.join(AQUI, "afiliados.json"), encoding="utf-8") as fh:
        afiliados = {k: v for k, v in json.load(fh).items() if k.startswith("AFF_")}
    if a.todo:
        publicadas = set(orden)
    else:
        if not a.inicio:
            sys.exit("Falta --inicio (o usá --todo para la vista previa)")
        dia = funcion_dia(a.goteo)
        inicio = dt.date.fromisoformat(a.inicio)
        publicadas = {s for i, s in enumerate(orden) if dia(i, inicio) <= hoy}
    sal = a.salida
    os.makedirs(sal, exist_ok=True)
    with open(os.path.join(sal, "estilos.css"), "w", encoding="utf-8") as fh:
        fh.write(CSS)
    for slug in orden:
        destino = os.path.join(sal, archivo(slug))
        if slug in publicadas:
            with open(destino, "w", encoding="utf-8") as fh:
                fh.write(marcadores(pagina(slug, C.PAGINAS[slug], orden, publicadas, afiliados, url_base, hoy, a.todo), a))
        elif os.path.exists(destino):
            os.remove(destino)
    if not a.sin_pins:
        pins(os.path.join(sal, "img", "pins"), orden, a.pie)
    ahora = dt.datetime.now(dt.timezone.utc).replace(microsecond=0)
    rss(os.path.join(sal, "rss-completo.xml"), orden, url_base, ahora)
    sitemap(os.path.join(sal, "sitemap-herramientas.xml"), publicadas, orden, url_base, hoy)
    print(f"Páginas publicadas: {len([s for s in orden if s in publicadas])} de {len(orden)} -> {sal}")
    for s in orden:
        print(("  [sale] " if s in publicadas else "  [cola] ") + archivo(s))


if __name__ == "__main__":
    main()
