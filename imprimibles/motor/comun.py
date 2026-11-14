"""Funciones compartidas: render SVG->PDF/PNG, plantillas HTML, RSS, datos."""
import html
import io
import json
import os
from datetime import date, datetime, timezone
from email.utils import format_datetime
from pathlib import Path

import cairosvg
from pypdf import PdfWriter, PdfReader

RAIZ = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# Configuracion (se puede cambiar con config.json o variables de entorno)
# ---------------------------------------------------------------------------
_CFG_DEFAULT = {
    # URL publica donde va a vivir la carpeta imprimibles-auto en el sitio.
    "base_url": "https://handycalcs.com/imprimibles",
    "sitio": "Handy Calcs",
    "url_sitio": "https://handycalcs.com/",
    "link_amazon_colorear": "#LIBROS-AMAZON-COLOREAR",
    "link_amazon_juegos": "#LIBROS-AMAZON-SUDOKU",
    "link_amazon_fichas": "#LIBROS-AMAZON-BILINGUES",
    # Sitio propio de paginas para colorear (Cloudflare Pages). Cambiar aca.
    "SITE_NAME": "SITE_NAME",
    "SITE_URL": "https://SITE_URL",
    "email_contacto": "CONTACTO@SITE_URL",
    # Dia 1 del goteo (2 o 3 items nuevos por dia) de cada paquete.
    "goteo_inicio": {"colorear": "2026-11-17", "fichas-bilingues": "2026-11-17"},
}


def cfg():
    c = dict(_CFG_DEFAULT)
    p = RAIZ / "config.json"
    if p.exists():
        c.update(json.loads(p.read_text(encoding="utf-8")))
    if os.environ.get("IMPRIMIBLES_BASE_URL"):
        c["base_url"] = os.environ["IMPRIMIBLES_BASE_URL"]
    if os.environ.get("SITE_URL"):
        c["SITE_URL"] = os.environ["SITE_URL"]
    if os.environ.get("SITE_NAME"):
        c["SITE_NAME"] = os.environ["SITE_NAME"]
    c["base_url"] = c["base_url"].rstrip("/")
    c["SITE_URL"] = c["SITE_URL"].rstrip("/")
    return c


def esc(s):
    return html.escape(str(s), quote=True)


def hoy():
    f = os.environ.get("IMPRIMIBLES_HOY")
    if f:
        return date.fromisoformat(f)
    return date.today()


# ---------------------------------------------------------------------------
# Datos (cada paquete guarda su lista de items en datos.json)
# ---------------------------------------------------------------------------
def cargar(paquete):
    p = RAIZ / "_datos" / f"{paquete}.json"
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    return {"items": []}


def guardar(paquete, datos):
    p = RAIZ / "_datos" / f"{paquete}.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    datos["items"].sort(key=lambda it: (it["fecha"], it["slug"]))
    p.write_text(json.dumps(datos, ensure_ascii=False, indent=1), encoding="utf-8")


# ---------------------------------------------------------------------------
# Render
# ---------------------------------------------------------------------------
def svg_doc(inner, w, h, vw=None, vh=None, unidades=""):
    vw = vw or w
    vh = vh or h
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}{unidades}" height="{h}{unidades}" '
            f'viewBox="0 0 {vw} {vh}">\n{inner}\n</svg>\n')


def carta_svg(inner):
    """Pagina US Letter: sistema de coordenadas 850x1100 (100 = 1 pulgada)."""
    return svg_doc('<rect width="850" height="1100" fill="#fff"/>\n' + inner,
                   8.5, 11, 850, 1100, "in")


def a_pdf(svg_paginas, destino):
    """Recibe una lista de SVG (una por pagina) y escribe un PDF."""
    w = PdfWriter()
    for s in svg_paginas:
        b = cairosvg.svg2pdf(bytestring=s.encode("utf-8"))
        for pg in PdfReader(io.BytesIO(b)).pages:
            w.add_page(pg)
    w.add_metadata({"/Producer": "imprimibles-auto"})
    with open(destino, "wb") as f:
        w.write(f)


def a_png(svg, destino, ancho=None, alto=None):
    cairosvg.svg2png(bytestring=svg.encode("utf-8"), write_to=str(destino),
                     output_width=ancho, output_height=alto)


def preview_pin(inner_pagina, titulo, subtitulo, color_fondo="#f4efe6", color_banda="#2f4858", marca=None):
    """Imagen 1000x1500 (formato Pinterest) con la pagina carta y un rotulo abajo."""
    s = 860 / 850
    alto_pag = 1100 * s
    x0 = 70
    y0 = 50
    partes = [
        f'<rect width="1000" height="1500" fill="{color_fondo}"/>',
        f'<rect x="{x0 + 8}" y="{y0 + 10}" width="860" height="{alto_pag:.0f}" fill="#000" opacity="0.10"/>',
        f'<g transform="translate({x0},{y0}) scale({s:.5f})">',
        '<rect width="850" height="1100" fill="#fff"/>',
        inner_pagina,
        '</g>',
        f'<rect x="0" y="1225" width="1000" height="275" fill="{color_banda}"/>',
        f'<text x="500" y="1318" text-anchor="middle" font-family="Inter" font-weight="800" '
        f'font-size="{_tam_titulo(titulo)}" fill="#fff">{esc(titulo)}</text>',
        f'<text x="500" y="1390" text-anchor="middle" font-family="Inter" font-weight="500" '
        f'font-size="40" fill="#ffe8b0">{esc(subtitulo)}</text>',
        f'<text x="500" y="1458" text-anchor="middle" font-family="Inter" font-weight="600" '
        f'font-size="30" fill="#d7e3ea">{esc(marca or cfg()["sitio"])}</text>',
    ]
    return svg_doc("\n".join(partes), 1000, 1500)


def _tam_titulo(t):
    n = len(t)
    if n <= 22:
        return 64
    if n <= 28:
        return 54
    if n <= 34:
        return 46
    return 40


# ---------------------------------------------------------------------------
# HTML
# ---------------------------------------------------------------------------
CSS = """
*{box-sizing:border-box}body{margin:0;font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif;color:#1f2a33;background:#faf8f4;line-height:1.55}
header.sitio{background:#2f4858;color:#fff;padding:.7rem 1rem}header.sitio a{color:#fff;text-decoration:none;font-weight:700}
main{max-width:1040px;margin:0 auto;padding:1rem}
h1{font-size:1.8rem;line-height:1.2;margin:.6rem 0}h2{font-size:1.3rem;margin-top:1.6rem}
.migas{font-size:.9rem;color:#5b6b75}.migas a{color:#2f6f8f}
.grilla{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:1rem;padding:0;list-style:none}
.grilla li{background:#fff;border:1px solid #e5e0d6;border-radius:10px;overflow:hidden}
.grilla a{color:inherit;text-decoration:none;display:block}.grilla img{width:100%;height:auto;display:block;background:#fff}
.grilla span{display:block;padding:.5rem .6rem;font-size:.92rem;font-weight:600}
.boton{display:inline-block;background:#e07a2f;color:#fff;padding:.75rem 1.2rem;border-radius:8px;text-decoration:none;font-weight:700;margin:.3rem .4rem .3rem 0;border:0;cursor:pointer;font-size:1rem}
.boton.sec{background:#2f6f8f}
.ficha{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:1.5rem;align-items:start}
.ficha img{width:100%;height:auto;border:1px solid #e5e0d6;border-radius:8px;background:#fff}
@media(max-width:720px){.ficha{grid-template-columns:1fr}}
.anuncio{margin:1.2rem 0;min-height:90px}
.amazon{background:#fff7e8;border:1px solid #f1d9a8;border-radius:10px;padding:.8rem 1rem;margin:1.2rem 0}
footer{color:#5b6b75;font-size:.85rem;text-align:center;padding:2rem 1rem}
@media print{header.sitio,.anuncio,.amazon,footer,.no-imprimir{display:none!important}body{background:#fff}}
"""


def _hc_ids():
    """GA4, Pixel y AdSense de Handy Calcs: se leen del CONFIG de ../build.py (un solo lugar donde cambiarlos)."""
    import re as _re
    ids = {"ga4": "", "pixel": "", "adsense": ""}
    b = RAIZ.parent / "build.py"
    if b.exists():
        t = b.read_text(encoding="utf-8")
        for k in ids:
            m = _re.search(r'^\s*%s="([^"]*)"' % k, t, _re.M)
            if m: ids[k] = m.group(1)
    return ids


def _marcadores_hc(h):
    """Páginas de Handy Calcs: GA4/Pixel/AdSense cargan solo si aceptan cookies (lo hace /site.js)."""
    ids = _hc_ids()
    hc = '<script>window.HC=%s;</script>' % json.dumps({"ga4": ids["ga4"], "pixel": ids["pixel"]})
    ads = ""
    if ids["adsense"]:
        ads = ('<script>window.adsbygoogle=window.adsbygoogle||[];window.adsbygoogle.pauseAdRequests=1;</script>'
               '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=%s" '
               'crossorigin="anonymous"></script>' % ids["adsense"])
    h = h.replace("<!-- GA4 -->", '<link rel="stylesheet" href="/cookie.css">' + hc, 1)
    h = h.replace("<!-- ADSENSE -->\n", ads + "\n", 1)            # el del <head>
    h = h.replace('<div class="anuncio"><!-- ADSENSE --></div>\n', "")  # anuncios automáticos: se ubican solos
    h = h.replace("</footer>", ' &middot; <a href="/es/privacy/">Privacidad</a> &middot; <a href="#" data-reset-cookies>Cookies</a></footer>'
                  '\n<script src="/site.js" defer></script>', 1)
    return h


def pagina_html(*, titulo, descripcion, h1, canonical, cuerpo, imagen=None, migas=None,
                extra_head="", jsonld=None, amazon=None, texto_amazon=None, sitio=None):
    c = cfg()
    es_hc = sitio is None
    if sitio is None:
        sitio = {"nombre": c["sitio"], "home": c["url_sitio"],
                 "nav": [("Imprimibles gratis", c["base_url"] + "/")], "pie": "", "pixel": False,
                 "cookies": False}
    m = ""
    if migas:
        m = '<nav class="migas">' + " &rsaquo; ".join(
            f'<a href="{esc(u)}">{esc(t)}</a>' if u else esc(t) for t, u in migas) + "</nav>"
    og_img = f'<meta property="og:image" content="{esc(imagen)}">\n' if imagen else ""
    ld = ""
    if jsonld:
        ld = '<script type="application/ld+json">' + json.dumps(jsonld, ensure_ascii=False) + "</script>\n"
    am = ""
    if amazon:
        am = (f'<!-- AMAZON: reemplazar el href por el link de afiliado -->\n'
              f'<aside class="amazon">&#128218; {esc(texto_amazon or "¿Quieres más? Mira estos libros")}: '
              f'<a href="{esc(amazon)}" rel="nofollow sponsored noopener" target="_blank">libros en Amazon</a></aside>')
    nav = "".join(f' &middot; <a href="{esc(u)}">{esc(t)}</a>' for t, u in sitio.get("nav", []))
    h = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(titulo)}</title>
<meta name="description" content="{esc(descripcion)}">
<link rel="canonical" href="{esc(canonical)}">
<meta property="og:type" content="website">
<meta property="og:title" content="{esc(titulo)}">
<meta property="og:description" content="{esc(descripcion)}">
<meta property="og:url" content="{esc(canonical)}">
{og_img}<meta name="twitter:card" content="summary_large_image">
<!-- GA4 -->
<!-- ADSENSE -->
{"<!-- META_PIXEL -->" if sitio.get("pixel") else ""}
<style>{CSS}</style>
{extra_head}{ld}</head>
<body>
<header class="sitio"><a href="{esc(sitio['home'])}">{esc(sitio['nombre'])}</a>{nav}</header>
<main>
{m}
<h1>{esc(h1)}</h1>
<div class="anuncio"><!-- ADSENSE --></div>
{cuerpo}
<div class="anuncio"><!-- ADSENSE --></div>
{am}
</main>
<footer>&copy; {date.today().year} {esc(sitio['nombre'])} &middot; Gratis para uso personal y en el aula. No se permite revender.{sitio.get('pie','')}</footer>
{_COOKIES if sitio.get("cookies") else ""}
</body>
</html>
"""
    return _marcadores_hc(h) if es_hc else h


_COOKIES = """<div id="aviso-cookies" class="no-imprimir" style="display:none;position:fixed;bottom:0;left:0;right:0;background:#1f2a33;color:#fff;padding:.8rem 1rem;font-size:.9rem;z-index:99;text-align:center">
Usamos cookies para estadísticas y anuncios. <a href="/cookies.html" style="color:#ffd27a">Más información</a>
<button onclick="localStorage.setItem('ok-cookies','1');this.parentNode.style.display='none'" style="margin-left:.6rem;background:#e07a2f;color:#fff;border:0;border-radius:6px;padding:.35rem .9rem;cursor:pointer">Aceptar</button></div>
<script>if(!localStorage.getItem('ok-cookies'))document.getElementById('aviso-cookies').style.display='block';</script>"""


def rss(*, titulo, link, descripcion, items, destino, self_url=None):
    """items: dicts con titulo, link, descripcion, imagen, fecha (date), guid."""
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<rss version="2.0" xmlns:media="http://search.yahoo.com/mrss/" xmlns:atom="http://www.w3.org/2005/Atom">',
           '<channel>',
           f'<title>{esc(titulo)}</title>', f'<link>{esc(link)}</link>',
           f'<description>{esc(descripcion)}</description>', '<language>es</language>',
           f'<atom:link href="{esc(self_url or link + "rss.xml")}" rel="self" type="application/rss+xml"/>']
    for it in items:
        d = it["fecha"]
        dt = datetime(d.year, d.month, d.day, 12, 0, tzinfo=timezone.utc)
        desc_html = f'<img src="{it["imagen"]}" alt="{esc(it["titulo"])}"/><p>{esc(it["descripcion"])}</p>'
        out += ['<item>',
                f'<title>{esc(it["titulo"])}</title>',
                f'<link>{esc(it["link"])}</link>',
                f'<guid isPermaLink="false">{esc(it["guid"])}</guid>',
                f'<pubDate>{format_datetime(dt)}</pubDate>',
                f'<description><![CDATA[{desc_html}]]></description>',
                f'<enclosure url="{esc(it["imagen"])}" type="image/png" length="0"/>',
                f'<media:content url="{esc(it["imagen"])}" medium="image" type="image/png"/>',
                '</item>']
    out += ['</channel>', '</rss>', '']
    Path(destino).write_text("\n".join(out), encoding="utf-8")


def escribir(ruta, texto):
    ruta = Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(texto, encoding="utf-8")


def miniatura(png_origen, destino, ancho=400):
    from PIL import Image
    im = Image.open(png_origen).convert("RGB")
    h = round(im.height * ancho / im.width)
    im.resize((ancho, h), Image.LANCZOS).save(destino, "JPEG", quality=82, optimize=True)


# ---------------------------------------------------------------------------
# Goteo: 2 o 3 items nuevos por dia (misma regla que goteo.py)
# ---------------------------------------------------------------------------
def _goteo_mod():
    import importlib.util
    spec = importlib.util.spec_from_file_location("goteo", RAIZ / "goteo.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def inicio_goteo(paquete):
    return date.fromisoformat(cfg().get("goteo_inicio", {}).get(paquete, "2026-11-17"))


def fecha_salida(i, paquete):
    """Dia en que sale el item numero i (0 = el primero) del paquete."""
    return _goteo_mod().dia_de_salida(i, inicio_goteo(paquete))


def con_salida(items, paquete):
    """Devuelve los items (ordenados por n) con su fecha de salida en it['salida']."""
    orden = sorted(items, key=lambda it: it["n"])
    ini = inicio_goteo(paquete)
    g = _goteo_mod()
    for i, it in enumerate(orden):
        it["salida"] = g.dia_de_salida(i, ini).isoformat()
    return orden


def liberados(items, paquete, dia=None):
    dia = dia or hoy()
    return [it for it in con_salida(items, paquete) if date.fromisoformat(it["salida"]) <= dia]


def correr_goteo(completo, salida, paquete, dia=None):
    """Llama a goteo.py (el mismo de la carpeta goteo/) para armar el rss.xml publico."""
    import sys
    import xml.etree.ElementTree as ET
    ET.register_namespace("media", "http://search.yahoo.com/mrss/")
    ET.register_namespace("atom", "http://www.w3.org/2005/Atom")
    g = _goteo_mod()
    viejo = sys.argv
    sys.argv = ["goteo.py", str(completo), str(salida), "--inicio", inicio_goteo(paquete).isoformat(),
                "--hoy", (dia or hoy()).isoformat()]
    try:
        g.main()
    finally:
        sys.argv = viejo


# ---------------------------------------------------------------------------
# Medir texto (para armar renglones sin depender de <tspan>)
# ---------------------------------------------------------------------------
_FUENTES = {}


def medir(texto, tam, peso=400, italica=False):
    """Ancho aproximado en unidades SVG de `texto` en Inter con tamano `tam`."""
    import subprocess
    from PIL import ImageFont
    clave = (peso, italica)
    if clave not in _FUENTES:
        patron = f"Inter:weight={ {400: 80, 500: 100, 600: 180, 700: 200, 800: 205, 900: 210}.get(peso, 80) }"
        if italica:
            patron += ":italic"
        try:
            ruta = subprocess.run(["fc-match", "-f", "%{file}", patron], capture_output=True, text=True).stdout.strip()
            _FUENTES[clave] = ruta
        except Exception:
            _FUENTES[clave] = None
    ruta = _FUENTES[clave]
    if ruta:
        try:
            fnt = ImageFont.truetype(ruta, 200)
            return fnt.getlength(texto) * tam / 200
        except Exception:
            pass
    return len(texto) * tam * 0.6
