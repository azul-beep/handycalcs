"""Paquete colorear/: sitio propio de paginas para colorear (Cloudflare Pages)."""
import math
import random
from datetime import date, timedelta
from pathlib import Path

from . import animales as ani
from . import arte
from .arte import B, T, f, circulo, camino, pol
from .comun import (RAIZ, a_pdf, a_png, cargar, carta_svg, cfg, con_salida, correr_goteo, esc, escribir,
                    fecha_salida, guardar, hoy, miniatura, pagina_html, preview_pin, rss)

PAQ = "colorear"
DIR = RAIZ / PAQ

CATEGORIAS = {
    "mandalas": {
        "nombre": "Mandalas",
        "titulo": "Mandalas para colorear gratis (PDF para imprimir)",
        "h1": "Mandalas para colorear",
        "desc": "Mandalas para colorear gratis en PDF tamaño carta: diseños relajantes para adultos y niños, listos para imprimir.",
        "intro": "Mandalas simétricos con trazo limpio, pensados para relajarse. Hay diseños más simples para niños y otros con más detalle. Todos se imprimen en tamaño carta (y también salen bien en A4).",
        "color": "#f3e9ff", "banda": "#5b3f8c",
    },
    "animales": {
        "nombre": "Animales",
        "titulo": "Dibujos de animales para colorear para niños (PDF gratis)",
        "h1": "Animales para colorear",
        "desc": "Dibujos de animales para colorear para niños de 2 a 7 años: gato, perro, búho, león y más. PDF gratis para imprimir.",
        "intro": "Animales tiernos con líneas gruesas y áreas grandes, ideales para manos chiquitas. Cada página trae el nombre del animal para practicar la lectura.",
        "color": "#e6f6ea", "banda": "#2e6b45",
    },
    "geometricos": {
        "nombre": "Patrones geométricos",
        "titulo": "Patrones geométricos para colorear (PDF gratis)",
        "h1": "Patrones geométricos para colorear",
        "desc": "Patrones geométricos para colorear: hexágonos, mosaicos, ondas y escamas. Láminas antiestrés gratis en PDF.",
        "intro": "Mosaicos y patrones repetitivos para colorear sin pensar: ideales para relajarte, probar combinaciones de colores o practicar degradés.",
        "color": "#e4f1f8", "banda": "#1f5a7a",
    },
    "paisajes": {
        "nombre": "Paisajes",
        "titulo": "Paisajes de montaña para colorear (PDF gratis para imprimir)",
        "h1": "Paisajes para colorear",
        "desc": "Paisajes para colorear gratis: montañas, lagos, pinos y sol. Dibujos simples en PDF para imprimir en casa o en el aula.",
        "intro": "Montañas, lagos y bosques con trazo simple. Funcionan muy bien con lápices de colores, crayones o acuarelas.",
        "color": "#fdf0dc", "banda": "#8a4b1c",
    },
}

ROTACION = ["mandalas", "animales", "geometricos", "mandalas", "paisajes", "animales", "geometricos", "mandalas",
            "animales", "paisajes"]

ORDEN_ANIMALES = ["gato", "buho", "pez", "leon", "tortuga", "conejo", "elefante", "mariposa", "oso", "pato",
                  "caracol", "rana", "perro", "abeja", "ballena", "cerdo", "pajaro", "mariquita", "raton"]
ACUATICOS = {"pez", "ballena", "tortuga", "pato"}
VOLADORES = {"mariposa", "abeja", "pajaro", "buho", "mariquita"}


# ---------------------------------------------------------------------------
# Escenas para animales
# ---------------------------------------------------------------------------
def _flor(x, y, r, w=2.4):
    o = [camino(f"M{f(x)},{f(y)} Q{f(x + r * 0.4)},{f(y + r * 2)} {f(x)},{f(y + r * 3.4)}", w)]
    o.append(camino(f"M{f(x + r * 0.2)},{f(y + r * 2.2)} q{f(r * 1.2)},{f(-r * 0.8)} {f(r * 1.6)},{f(r * 0.2)} "
                    f"q{f(-r * 0.8)},{f(r * 0.8)} {f(-r * 1.6)},{f(-r * 0.2)}Z", w, blanco=True))
    for k in range(6):
        p = pol(x, y, r * 0.95, k * math.pi / 3)
        o.append(circulo(p[0], p[1], r * 0.62, w, blanco=True))
    o.append(circulo(x, y, r * 0.55, w, blanco=True))
    return "\n".join(o)


def _alga(x, ybase, h, w=2.4):
    d = (f"M{f(x)},{f(ybase)} C{f(x - 30)},{f(ybase - h * 0.3)} {f(x + 30)},{f(ybase - h * 0.6)} {f(x)},{f(ybase - h)} "
         f"C{f(x + 40)},{f(ybase - h * 0.6)} {f(x - 10)},{f(ybase - h * 0.3)} {f(x + 22)},{f(ybase)} Z")
    return camino(d, w, blanco=True)


def animal_pagina(clave, seed):
    rng = random.Random(seed)
    x, y, w, h = arte.MARCO
    nombre = ani.ANIMALES[clave][1].upper()
    o = []
    if clave in ACUATICOS and clave != "pato":
        # fondo marino
        for k in range(rng.choice([6, 8])):
            bx, by = rng.uniform(110, 740), rng.uniform(240, 420)
            o.append(circulo(bx, by, rng.uniform(8, 18), 2.2))
        o.append(camino("M60,960 Q200,920 330,955 T600,950 T800,940 L800,1040 L60,1040 Z", 2.8, blanco=True))
        for ax in (110, 200, 640, 730):
            o.append(_alga(ax, 975, rng.uniform(150, 230)))
        for k in range(5):
            px, py = rng.uniform(260, 600), rng.uniform(985, 1015)
            o.append(arte.elipse(px, py, rng.uniform(14, 22), 8, 2.2, blanco=True))
    else:
        # sol y nubes + suelo con flores
        sx = rng.choice([150, 700])
        o.append(circulo(sx, 330, 40, 2.6, blanco=True))
        for k in range(12):
            a = k * math.pi / 6
            o.append(arte.linea(pol(sx, 330, 52, a), pol(sx, 330, 70, a), 2.6))
        o.append(arte._nube(850 - sx, 320, 0.9))
        if clave == "pato":
            o.append(camino("M60,930 Q250,900 425,930 T800,925 L800,1040 L60,1040 Z", 2.8, blanco=True))
            for k in range(6):
                lx = rng.uniform(90, 680)
                ly = rng.uniform(960, 1015)
                o.append(arte.linea((lx, ly), (lx + rng.uniform(50, 110), ly), 2))
        else:
            o.append(camino("M60,920 Q240,890 425,915 T800,905 L800,1040 L60,1040 Z", 2.8, blanco=True))
            for fx in (115, 205, 645, 735):
                o.append(_flor(fx + rng.uniform(-10, 10), 830 + rng.uniform(0, 30), rng.uniform(17, 22)))
            for gx in (150, 300, 425, 550, 700):
                gx += rng.uniform(-25, 25)
                gy = rng.uniform(985, 1015)
                o.append(camino(f"M{f(gx - 14)},{f(gy)} Q{f(gx - 12)},{f(gy - 18)} {f(gx - 22)},{f(gy - 30)} "
                                f"M{f(gx)},{f(gy)} L{f(gx)},{f(gy - 34)} M{f(gx + 14)},{f(gy)} "
                                f"Q{f(gx + 12)},{f(gy - 18)} {f(gx + 22)},{f(gy - 30)}", 2.2))
    # animal grande
    tam = 540
    o.append(ani.dibujar(clave, 425 - tam / 2, 370, tam, trazo=4.0))
    # nombre en letras huecas
    fs = min(120, 640 / (len(nombre) * 0.8))
    o.append(f'<text x="425" y="{f(150 + fs * 0.62)}" text-anchor="middle" font-family="Inter" font-weight="900" font-size="{f(fs)}" '
             f'fill="#fff" stroke="#000" stroke-width="3.5" stroke-linejoin="round" letter-spacing="6">{esc(nombre)}</text>')
    return arte._marco("\n".join(o), seed)


# ---------------------------------------------------------------------------
# Catalogo: que pagina corresponde al item numero n
# ---------------------------------------------------------------------------
def receta(n):
    cat = ROTACION[(n - 1) % len(ROTACION)]
    # cuantas veces aparecio esta categoria antes (para numerar dentro de la categoria)
    k = sum(1 for i in range(1, n) if ROTACION[(i - 1) % len(ROTACION)] == cat) + 1
    seed = n * 7919 + 13
    if cat == "mandalas":
        return dict(cat=cat, k=k, seed=seed, tipo="mandala",
                    titulo=f"Mandala para colorear n.º {k}", slug=f"mandala-para-colorear-{k:03d}",
                    alt=f"Mandala para colorear número {k}, dibujo de líneas en blanco y negro para imprimir")
    if cat == "geometricos":
        g = arte.GEOMETRICOS[(k - 1) % len(arte.GEOMETRICOS)]
        nom = arte.NOMBRES_GEO[g.__name__]
        return dict(cat=cat, k=k, seed=seed, tipo=g.__name__,
                    titulo=f"Patrón geométrico para colorear: {nom} ({k})",
                    slug=f"patron-geometrico-{k:03d}",
                    alt=f"Patrón geométrico de {nom.lower()} para colorear, lámina antiestrés en blanco y negro")
    if cat == "paisajes":
        return dict(cat=cat, k=k, seed=seed, tipo="paisaje",
                    titulo=f"Paisaje de montaña para colorear n.º {k}", slug=f"paisaje-montana-{k:03d}",
                    alt=f"Paisaje de montañas con pinos y sol para colorear, número {k}")
    clave = ORDEN_ANIMALES[(k - 1) % len(ORDEN_ANIMALES)]
    vuelta = (k - 1) // len(ORDEN_ANIMALES)
    nom = ani.ANIMALES[clave][1]
    art = ani.ANIMALES[clave][3]
    suf = f"-{vuelta + 1}" if vuelta else ""
    return dict(cat=cat, k=k, seed=seed, tipo="animal", clave=clave,
                titulo=f"Dibujo de {nom} para colorear" + (f" ({vuelta + 1})" if vuelta else ""),
                slug=f"{clave}-para-colorear{suf}",
                alt=f"Dibujo de {art} {nom} para colorear para niños, con el nombre en letras grandes")


def arte_de(r):
    if r["tipo"] == "mandala":
        return arte.mandala(r["seed"])
    if r["tipo"] == "paisaje":
        return arte.paisaje(r["seed"])
    if r["tipo"] == "animal":
        return animal_pagina(r["clave"], r["seed"])
    return getattr(arte, r["tipo"])(r["seed"])


def generar_item(n, fecha):
    c = cfg()
    r = receta(n)
    inner = arte_de(r) + "\n" + arte.pie_pagina(esc(c["SITE_NAME"]) + " · gratis para uso personal")
    carp = DIR / "archivos"
    carp.mkdir(parents=True, exist_ok=True)
    (DIR / "miniaturas").mkdir(parents=True, exist_ok=True)
    svg = carta_svg(inner)
    (carp / f"{r['slug']}.svg").write_text(svg, encoding="utf-8")
    a_pdf([svg], carp / f"{r['slug']}.pdf")
    cat = CATEGORIAS[r["cat"]]
    sub = "Para colorear · PDF gratis"
    titulo_pin = {"mandalas": f"Mandala n.º {r['k']}", "geometricos": "Patrón geométrico",
                  "paisajes": "Paisaje de montaña", "animales": ani.ANIMALES.get(r.get("clave", ""), ("", "", ""))[1].capitalize() if r["tipo"] == "animal" else ""}[r["cat"]]
    pv = preview_pin(inner, titulo_pin, sub, cat["color"], cat["banda"], marca=c["SITE_NAME"])
    a_png(pv, carp / f"{r['slug']}.png", 1000, 1500)
    miniatura(carp / f"{r['slug']}.png", DIR / "miniaturas" / f"{r['slug']}.jpg")
    r["n"] = n
    r["fecha"] = fecha.isoformat()
    return r


def agregar(cantidad=None, fecha=None, dias_buffer=None):
    """Agrega `cantidad` paginas nuevas, o (con dias_buffer) las que hagan falta para que
    la cola del goteo tenga material hasta hoy + dias_buffer."""
    fecha = fecha or hoy()
    datos = cargar(PAQ)
    hechos = {it["n"] for it in datos["items"]}
    descartados = set(datos.get("descartados", []))

    def falta():
        if cantidad is not None:
            return nuevos < cantidad
        total = len(datos["items"])
        return total == 0 or fecha_salida(total - 1, PAQ) < fecha + timedelta(days=dias_buffer)

    n = 1
    nuevos = 0
    while falta():
        if n not in hechos and n not in descartados:
            datos["items"].append(generar_item(n, fecha))
            nuevos += 1
            print(f"  colorear: item {n} -> {datos['items'][-1]['slug']}")
        n += 1
    guardar(PAQ, datos)
    return nuevos


# ---------------------------------------------------------------------------
# Sitio estatico
# ---------------------------------------------------------------------------
def _sitio():
    c = cfg()
    nav = [(v["nombre"], f"/{k}/") for k, v in CATEGORIAS.items()]
    pie = (' &middot; <a href="/acerca.html">Acerca de</a> &middot; <a href="/privacidad.html">Privacidad</a>'
           ' &middot; <a href="/cookies.html">Cookies</a>')
    return {"nombre": c["SITE_NAME"], "home": "/", "nav": nav, "pie": pie, "pixel": True, "cookies": True}


def _tarjetas(items):
    li = []
    for it in items:
        li.append(f'<li><a href="/{it["cat"]}/{it["slug"]}.html"><img src="/miniaturas/{it["slug"]}.jpg" '
                  f'width="400" height="600" loading="lazy" alt="{esc(it["alt"])}"><span>{esc(it["titulo"])}</span></a></li>')
    return '<ul class="grilla">' + "".join(li) + "</ul>"


def _desc_item(it):
    cat = it["cat"]
    if cat == "mandalas":
        return (f"Descarga gratis este mandala para colorear (n.º {it['k']}) en PDF tamaño carta. "
                "Trazo limpio, ideal para relajarse; sirve para adultos y niños.")
    if cat == "geometricos":
        return ("Lámina de patrón geométrico para colorear, gratis en PDF. Perfecta para colorear antiestrés, "
                "probar paletas de colores o practicar degradés.")
    if cat == "paisajes":
        return ("Paisaje de montaña para colorear gratis: picos nevados, sol, nubes y pinos. "
                "PDF tamaño carta listo para imprimir.")
    nom = ani.ANIMALES[it["clave"]][1]
    return (f"Dibujo de {nom} para colorear para niños, con líneas gruesas y el nombre en letras grandes. "
            "Gratis en PDF para imprimir en casa o en el preescolar.")


def construir_sitio():
    c = cfg()
    U = c["SITE_URL"]
    datos = cargar(PAQ)
    todos = con_salida(datos["items"], PAQ)  # orden de salida
    dia = hoy()
    items = [it for it in todos if date.fromisoformat(it["salida"]) <= dia]
    items.reverse()  # lo mas nuevo primero
    S = _sitio()
    urls = [("/", None)]
    # paginas de item
    por_cat = {k: [it for it in items if it["cat"] == k] for k in CATEGORIAS}
    publicados = {it["slug"] for it in items}
    for it in todos:
        cat = CATEGORIAS[it["cat"]]
        hermanos = [x for x in por_cat[it["cat"]] if x["slug"] != it["slug"]][:8]
        desc = _desc_item(it)
        canon = f"{U}/{it['cat']}/{it['slug']}.html"
        cuerpo = f"""
<div class="ficha">
<div><img src="/archivos/{it['slug']}.png" width="1000" height="1500" alt="{esc(it['alt'])}"></div>
<div>
<p>{esc(desc)}</p>
<p><a class="boton" href="/archivos/{it['slug']}.pdf" download>Descargar PDF gratis</a>
<a class="boton sec" href="/archivos/{it['slug']}.svg" download>Descargar SVG</a></p>
<h2>Cómo imprimirlo</h2>
<ol><li>Descarga el PDF y ábrelo.</li><li>Elige tamaño carta (o A4, "ajustar a página").</li>
<li>Imprime en blanco y negro: no gasta tinta de color.</li></ol>
<p class="no-imprimir">¿Te gustó? Guárdalo en Pinterest para encontrarlo después.</p>
<!-- ADSENSE -->
</div></div>
{f"<h2>Más {esc(cat['nombre'].lower())} para colorear</h2>" + _tarjetas(hermanos) if hermanos else ""}
<p><a href="/{it['cat']}/">Ver todos los {esc(cat['nombre'].lower())}</a></p>
"""
        ld = {"@context": "https://schema.org", "@type": "ImageObject", "name": it["titulo"],
              "description": desc, "contentUrl": f"{U}/archivos/{it['slug']}.png",
              "license": f"{U}/acerca.html", "acquireLicensePage": f"{U}/acerca.html",
              "creditText": c["SITE_NAME"], "datePublished": it["salida"]}
        html = pagina_html(titulo=f"{it['titulo']} | PDF gratis – {c['SITE_NAME']}", descripcion=desc,
                           h1=it["titulo"], canonical=canon, cuerpo=cuerpo,
                           imagen=f"{U}/archivos/{it['slug']}.png",
                           migas=[("Inicio", "/"), (cat["nombre"], f"/{it['cat']}/"), (it["titulo"], None)],
                           jsonld=ld, amazon=c["link_amazon_colorear"],
                           texto_amazon="¿Quieres un libro entero para colorear?", sitio=S,
                           extra_head="" if it["slug"] in publicados else '<meta name="robots" content="noindex">\n')
        escribir(DIR / it["cat"] / f"{it['slug']}.html", html)
        if it["slug"] in publicados:
            urls.append((f"/{it['cat']}/{it['slug']}.html", it["salida"]))
    # paginas de categoria + rss por categoria
    for k, cat in CATEGORIAS.items():
        lista = por_cat[k]
        cuerpo = (f"<p>{esc(cat['intro'])}</p>\n<p>Hay {len(lista)} láminas en esta sección y sumamos nuevas cada semana. "
                  f'Sigue las novedades en <a href="/rss-{k}.xml">RSS</a>.</p>\n' + _tarjetas(lista))
        html = pagina_html(titulo=f"{cat['titulo']} – {c['SITE_NAME']}", descripcion=cat["desc"], h1=cat["h1"],
                           canonical=f"{U}/{k}/", cuerpo=cuerpo,
                           imagen=f"{U}/archivos/{lista[0]['slug']}.png" if lista else None,
                           migas=[("Inicio", "/"), (cat["nombre"], None)], amazon=c["link_amazon_colorear"],
                           texto_amazon="Libros para colorear recomendados", sitio=S)
        escribir(DIR / k / "index.html", html)
        if lista:
            urls.append((f"/{k}/", lista[0]["salida"]))
        rss(titulo=f"{cat['nombre']} para colorear – {c['SITE_NAME']}", link=f"{U}/{k}/",
            descripcion=cat["desc"], items=[_item_rss(it, U) for it in lista[:50]],
            destino=DIR / f"rss-{k}.xml", self_url=f"{U}/rss-{k}.xml")
    # rss-completo.xml: todo, en orden de salida. rss.xml publico: lo arma goteo.py
    rss(titulo=f"{c['SITE_NAME']} – páginas para colorear gratis", link=f"{U}/",
        descripcion="Páginas para colorear gratis en PDF: mandalas, animales, patrones y paisajes.",
        items=[_item_rss(it, U) for it in todos], destino=DIR / "rss-completo.xml", self_url=f"{U}/rss.xml")
    correr_goteo(DIR / "rss-completo.xml", DIR / "rss.xml", PAQ, dia)
    # home
    bloques = []
    for k, cat in CATEGORIAS.items():
        if por_cat[k]:
            bloques.append(f'<h2><a href="/{k}/">{esc(cat["h1"])}</a></h2>\n{_tarjetas(por_cat[k][:4])}')
    cuerpo = (f"<p>Páginas para colorear gratis, listas para imprimir en PDF tamaño carta. Mandalas para relajarse, "
              f"animales para los más niños, patrones geométricos y paisajes. Todas hechas por nosotros y gratis para "
              f"uso personal y en el aula. Hay {len(items)} láminas y sumamos nuevas cada semana.</p>\n"
              f"<h2>Lo más nuevo</h2>\n{_tarjetas(items[:8])}\n" + "\n".join(bloques))
    html = pagina_html(titulo=f"Páginas para colorear gratis para imprimir (PDF) – {c['SITE_NAME']}",
                       descripcion="Dibujos y páginas para colorear gratis en PDF: mandalas, animales para niños, patrones geométricos y paisajes. Nuevos cada semana.",
                       h1="Páginas para colorear gratis para imprimir", canonical=f"{U}/", cuerpo=cuerpo,
                       imagen=f"{U}/archivos/{items[0]['slug']}.png" if items else None,
                       amazon=c["link_amazon_colorear"], texto_amazon="Libros para colorear recomendados", sitio=S,
                       jsonld={"@context": "https://schema.org", "@type": "WebSite", "name": c["SITE_NAME"], "url": f"{U}/"})
    escribir(DIR / "index.html", html)
    _paginas_legales(S)
    urls += [("/acerca.html", None), ("/privacidad.html", None), ("/cookies.html", None)]
    # sitemap, robots, headers, 404
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u, fch in urls:
        sm.append(f"<url><loc>{esc(U + u)}</loc>" + (f"<lastmod>{fch}</lastmod>" if fch else "") + "</url>")
    sm.append("</urlset>\n")
    escribir(DIR / "sitemap.xml", "\n".join(sm))
    escribir(DIR / "robots.txt", f"User-agent: *\nAllow: /\nDisallow: /rss-completo.xml\n\nSitemap: {U}/sitemap.xml\n")
    escribir(DIR / "_headers", """/archivos/*
  Cache-Control: public, max-age=2592000
/miniaturas/*
  Cache-Control: public, max-age=2592000
/*.xml
  Cache-Control: public, max-age=3600
/*
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  X-Frame-Options: SAMEORIGIN
""")
    escribir(DIR / "404.html", pagina_html(titulo=f"Página no encontrada – {c['SITE_NAME']}",
                                           descripcion="La página no existe.", h1="Uy, esta página no existe",
                                           canonical=f"{U}/404.html",
                                           cuerpo='<p>Vuelve al <a href="/">inicio</a> para ver todas las páginas para colorear.</p>',
                                           sitio=S).replace("<head>", '<head>\n<meta name="robots" content="noindex">', 1))


def _item_rss(it, U):
    return {"titulo": it["titulo"] + " (PDF gratis)", "link": f"{U}/{it['cat']}/{it['slug']}.html",
            "descripcion": _desc_item(it), "imagen": f"{U}/archivos/{it['slug']}.png",
            "fecha": date.fromisoformat(it["salida"]), "guid": f"colorear-{it['slug']}"}


def _paginas_legales(S):
    c = cfg()
    U = c["SITE_URL"]
    nombre = esc(c["SITE_NAME"])
    mail = esc(c["email_contacto"])
    paginas = {
        "acerca.html": ("Acerca de " + c["SITE_NAME"], f"""
<p>{nombre} es un sitio de páginas para colorear gratis. Todos los dibujos están hechos por nosotros con
programación (geometría y trazos simples), así que son originales.</p>
<h2>Licencia de uso</h2>
<ol><li>Puedes imprimirlas gratis para uso personal, en familia y en el aula, todas las veces que quieras.</li>
<li>No se permite revender los archivos ni subirlos a otros sitios. Si quieres compartirlas, comparte el enlace.</li>
<li>Para uso comercial (por ejemplo, incluirlas en un producto), escríbenos.</li></ol>
<h2>Contacto</h2><p>Escríbenos a <a href="mailto:{mail}">{mail}</a>.</p>"""),
        "privacidad.html": ("Política de privacidad", f"""
<p>Última actualización: {date.today().isoformat()}.</p>
<p>{nombre} no pide registro ni datos personales para descargar las láminas.</p>
<h2>Qué datos se recolectan</h2>
<ol><li>Estadísticas anónimas de visitas (Google Analytics 4): páginas vistas, país, tipo de dispositivo.</li>
<li>Anuncios (Google AdSense): Google y sus socios pueden usar cookies para mostrar anuncios según tus visitas a este y otros sitios. Puedes desactivar los anuncios personalizados en <a href="https://adssettings.google.com" rel="nofollow">Configuración de anuncios de Google</a>.</li>
<li>Medición de campañas (Meta Pixel), si está activo: registra visitas para medir anuncios en Facebook e Instagram.</li></ol>
<h2>Tus derechos</h2>
<p>Puedes pedir información o la eliminación de datos escribiendo a <a href="mailto:{mail}">{mail}</a>. Si vives en California
o en otros estados con leyes de privacidad, puedes pedir que no se vendan ni compartan tus datos escribiendo al mismo correo.</p>
<p>Este sitio no está dirigido a menores de 13 años como usuarios; los dibujos para niños están pensados para que los descarguen
los adultos.</p>"""),
        "cookies.html": ("Aviso de cookies", f"""
<p>Usamos cookies propias y de terceros:</p>
<ol><li>Necesarias: recordar que aceptaste este aviso (se guarda en tu navegador).</li>
<li>Estadísticas: Google Analytics 4.</li><li>Publicidad: Google AdSense y, si está activo, Meta Pixel.</li></ol>
<p>Puedes borrar o bloquear las cookies desde la configuración de tu navegador. Más detalles en la
<a href="/privacidad.html">política de privacidad</a>.</p>"""),
    }
    for arch, (tit, cuerpo) in paginas.items():
        escribir(DIR / arch, pagina_html(titulo=f"{tit} – {c['SITE_NAME']}", descripcion=tit, h1=tit,
                                         canonical=f"{U}/{arch}", cuerpo=cuerpo, sitio=S))
