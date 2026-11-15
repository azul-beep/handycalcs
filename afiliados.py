"""Links de afiliados (además de Amazon) para Handy Calcs y Cozy Paws, leídos de afiliados.json.

Cada artículo muestra sus "socios:" activos y, si falta lugar, los programas activos cuyas "temas" aparecen en el texto (auto). Un programa se muestra solo si tiene 'link' (el que da el programa al aprobarte), o si tiene "red": true y hay una
clave de Sovrn Commerce o Skimlinks en 'red_automatica' (esas redes convierten el link normal de la tienda en afiliado).
Sin nada cargado no se muestra nada: la web sigue igual. Corre con cada build, gratis y sin Claude.
"""
import html, json, os, re
from urllib.parse import quote

_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "afiliados.json")
DATA = json.load(open(_FILE, encoding="utf-8"))
PROG = DATA["programas"]
RED = DATA.get("red_automatica", {})
E = html.escape


def link(pid):
    """Link de afiliado del programa, o "" si todavía no está activo."""
    p = PROG.get(pid)
    if not p:
        return ""
    if p.get("link"):
        return p["link"]
    if p.get("red") and p.get("tienda"):
        if RED.get("sovrn_key"):
            return "https://redirect.viglink.com?key=%s&u=%s" % (quote(RED["sovrn_key"]), quote(p["tienda"], safe=""))
        if RED.get("skimlinks_id"):
            return "https://go.skimresources.com/?id=%s&xs=1&url=%s" % (quote(RED["skimlinks_id"]), quote(p["tienda"], safe=""))
    return ""


def activos(ids):
    """[(programa, link)] de los ids que ya están activos, en el mismo orden."""
    out = []
    for pid in ids:
        u = link(pid)
        if u:
            out.append((PROG[pid], u))
    return out


def ids_de(texto):
    """'ynab, monarch' -> ['ynab', 'monarch'] (cabecera 'socios:' de un artículo)."""
    return [x.strip() for x in (texto or "").split(",") if x.strip() in PROG]


def auto(texto, sitio, maximo=2):
    """Elige solos los programas ACTIVOS de un sitio cuyas 'temas' aparecen en el texto (título + cuerpo).

    Así los artículos nuevos (y los que tienen socios todavía sin link) muestran el recuadro sin que nadie elija a mano.
    Puntaje = cuántas veces aparece cada palabra; hace falta al menos 2 apariciones para entrar.
    """
    t = " " + re.sub(r"<[^>]+>", " ", (texto or "")).lower() + " "
    puntos = []
    for pid, p in PROG.items():
        if p.get("sitio") != sitio or not link(pid):
            continue
        n = sum(len(re.findall(r"(?<![a-z])" + re.escape(w.lower()) + r"(?![a-z])", t)) for w in p.get("temas", []))
        if n >= 2:
            puntos.append((-n, pid))
    return [pid for _, pid in sorted(puntos)[:maximo]]


def ids_para(articulo, sitio, maximo=2):
    """Programas para el recuadro de un artículo: primero los de 'socios:' que ya estén activos; si falta lugar, completa con auto()."""
    elegidos = [pid for pid in ids_de(articulo.get("socios")) if link(pid)][:maximo]
    if len(elegidos) < maximo:
        texto = " ".join([articulo.get("title", ""), articulo.get("h1", ""), articulo.get("h1", ""), articulo.get("body", "")])
        elegidos += [pid for pid in auto(texto, sitio, maximo) if pid not in elegidos][:maximo - len(elegidos)]
    return elegidos


NOTA = {"en": "Some links in this box are affiliate links: if you sign up or buy through them we may earn a commission, at no extra cost to you. It never changes what we recommend.",
        "es": "Algunos enlaces de este recuadro son de afiliados: si te registras o compras a través de ellos podemos ganar una comisión, sin costo extra para ti. Nunca cambia lo que recomendamos."}


def caja(ids, titulo, lang="en", clase="aff", estilo=""):
    """Recuadro HTML con los programas activos de un artículo, o "" si no hay ninguno."""
    items = activos(ids)
    if not items:
        return ""
    lis = "".join('<li><a href="%s" rel="sponsored noopener" target="_blank" data-aff="%s"><b>%s</b></a>: %s</li>'
                  % (E(u), E(p["nombre"]), E(p["nombre"]), E(p.get(lang) or p.get("en", ""))) for p, u in items)
    return '<aside class="%s"%s><h2>%s</h2><ul>%s</ul><p class="small">%s</p></aside>' % (
        clase, (' style="%s"' % estilo) if estilo else "", E(titulo), lis, NOTA[lang])
