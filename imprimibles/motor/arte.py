"""Generadores de arte lineal para colorear (todo por codigo, sin IA).

Sistema de coordenadas de pagina: 850 x 1100 (US Letter, 100 = 1 pulgada).
Todo es trazo negro sobre blanco; los objetos "de adelante" llevan relleno blanco
para tapar lo que queda detras.
"""
import math
import random

TRAZO = 'fill="none" stroke="#000" stroke-width="{w}" stroke-linejoin="round" stroke-linecap="round"'
BLANCO = 'fill="#fff" stroke="#000" stroke-width="{w}" stroke-linejoin="round" stroke-linecap="round"'


def T(w=2.6):
    return TRAZO.format(w=w)


def B(w=2.6):
    return BLANCO.format(w=w)


def f(v):
    return f"{v:.1f}"


def pol(cx, cy, r, a):
    return cx + r * math.cos(a), cy + r * math.sin(a)


def P(*pts):
    return " ".join(f"{f(x)},{f(y)}" for x, y in pts)


def circulo(cx, cy, r, w=2.6, blanco=False):
    return f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" {B(w) if blanco else T(w)}/>'


def camino(d, w=2.6, blanco=False):
    return f'<path d="{d}" {B(w) if blanco else T(w)}/>'


def poligono(pts, w=2.6, blanco=False):
    return f'<polygon points="{P(*pts)}" {B(w) if blanco else T(w)}/>'


def linea(p1, p2, w=2.6):
    return f'<line x1="{f(p1[0])}" y1="{f(p1[1])}" x2="{f(p2[0])}" y2="{f(p2[1])}" {T(w)}/>'


def elipse(cx, cy, rx, ry, w=2.6, blanco=False, rot=0):
    tr = f' transform="rotate({f(rot)} {f(cx)} {f(cy)})"' if rot else ""
    return f'<ellipse cx="{f(cx)}" cy="{f(cy)}" rx="{f(rx)}" ry="{f(ry)}"{tr} {B(w) if blanco else T(w)}/>'


def pie_pagina(texto):
    return (f'<text x="425" y="1072" text-anchor="middle" font-family="Inter" font-size="13" '
            f'fill="#888">{texto}</text>')


# ===========================================================================
# MANDALAS
# ===========================================================================
def _anillo(cx, cy, r1, r2, n, tipo, rot, rng):
    """Dibuja un anillo de motivos entre r1 y r2 con simetria n."""
    out = []
    da = 2 * math.pi / n
    rm = (r1 + r2) / 2
    h = r2 - r1
    for i in range(n):
        a = rot + i * da
        ancho_p = 0.55 if n >= 12 else 0.42
        if tipo == "petalo":
            p0 = pol(cx, cy, r1, a)
            p1 = pol(cx, cy, r2, a)
            c1 = pol(cx, cy, rm, a - da * ancho_p)
            c2 = pol(cx, cy, rm, a + da * ancho_p)
            out.append(camino(f"M{f(p0[0])},{f(p0[1])} Q{f(c1[0])},{f(c1[1])} {f(p1[0])},{f(p1[1])} "
                              f"Q{f(c2[0])},{f(c2[1])} {f(p0[0])},{f(p0[1])}Z"))
        elif tipo == "petalo_doble":
            for k, esc in ((0, ancho_p), (1, ancho_p * 0.5)):
                ra = r1 + h * 0.18 * k
                rb = r2 - h * 0.18 * k
                p0 = pol(cx, cy, ra, a)
                p1 = pol(cx, cy, rb, a)
                c1 = pol(cx, cy, (ra + rb) / 2, a - da * esc)
                c2 = pol(cx, cy, (ra + rb) / 2, a + da * esc)
                out.append(camino(f"M{f(p0[0])},{f(p0[1])} Q{f(c1[0])},{f(c1[1])} {f(p1[0])},{f(p1[1])} "
                                  f"Q{f(c2[0])},{f(c2[1])} {f(p0[0])},{f(p0[1])}Z", w=2.6 if k == 0 else 2))
        elif tipo == "circulos":
            rr = min(h * 0.42, rm * math.sin(da / 2) * 0.9)
            x, y = pol(cx, cy, rm, a + da / 2)
            out.append(circulo(x, y, rr))
            if rr > 11:
                out.append(circulo(x, y, rr * 0.45, w=2))
        elif tipo == "festones":
            p0 = pol(cx, cy, r1, a)
            p1 = pol(cx, cy, r1, a + da)
            c = pol(cx, cy, r2 + h * 0.35, a + da / 2)
            out.append(camino(f"M{f(p0[0])},{f(p0[1])} Q{f(c[0])},{f(c[1])} {f(p1[0])},{f(p1[1])}"))
            q0 = pol(cx, cy, r1, a + da * 0.22)
            q1 = pol(cx, cy, r1, a + da * 0.78)
            qc = pol(cx, cy, r1 + h * 0.9, a + da / 2)
            out.append(camino(f"M{f(q0[0])},{f(q0[1])} Q{f(qc[0])},{f(qc[1])} {f(q1[0])},{f(q1[1])}", w=2))
        elif tipo == "zigzag":
            p0 = pol(cx, cy, r1, a)
            p1 = pol(cx, cy, r2, a + da / 2)
            p2 = pol(cx, cy, r1, a + da)
            out.append(f'<polyline points="{P(p0, p1, p2)}" {T()}/>')
            q = pol(cx, cy, r1 + h * 0.45, a + da / 2)
            out.append(circulo(q[0], q[1], min(h * 0.14, 7), w=2))
        elif tipo == "gota":
            p0 = pol(cx, cy, r1 + h * 0.08, a)
            p1 = pol(cx, cy, r2, a)
            ancho = min(rm * da * 0.36, h * 0.38)
            perp = a + math.pi / 2
            b1 = (pol(cx, cy, r1 + h * 0.62, a)[0] + ancho * math.cos(perp),
                  pol(cx, cy, r1 + h * 0.62, a)[1] + ancho * math.sin(perp))
            b2 = (pol(cx, cy, r1 + h * 0.62, a)[0] - ancho * math.cos(perp),
                  pol(cx, cy, r1 + h * 0.62, a)[1] - ancho * math.sin(perp))
            out.append(camino(f"M{f(p0[0])},{f(p0[1])} C{f(b1[0])},{f(b1[1])} {f(p1[0])},{f(p1[1])} {f(p1[0])},{f(p1[1])} "
                              f"C{f(p1[0])},{f(p1[1])} {f(b2[0])},{f(b2[1])} {f(p0[0])},{f(p0[1])}Z"))
        elif tipo == "radios":
            p0 = pol(cx, cy, r1, a)
            p1 = pol(cx, cy, r2, a)
            out.append(linea(p0, p1, w=2))
            x, y = pol(cx, cy, rm, a + da / 2)
            out.append(circulo(x, y, min(h * 0.22, rm * da * 0.25), w=2))
        elif tipo == "hojas":
            p0 = pol(cx, cy, r1, a)
            p1 = pol(cx, cy, r2, a + da * 0.5)
            c1 = pol(cx, cy, rm, a - da * 0.05)
            c2 = pol(cx, cy, rm + h * 0.1, a + da * 0.62)
            out.append(camino(f"M{f(p0[0])},{f(p0[1])} Q{f(c1[0])},{f(c1[1])} {f(p1[0])},{f(p1[1])} "
                              f"Q{f(c2[0])},{f(c2[1])} {f(p0[0])},{f(p0[1])}Z"))
            m0 = pol(cx, cy, r1 + h * 0.15, a + da * 0.05)
            out.append(camino(f"M{f(m0[0])},{f(m0[1])} L{f(p1[0])},{f(p1[1])}", w=1.6))
        elif tipo == "arcos":
            p0 = pol(cx, cy, r2, a)
            p1 = pol(cx, cy, r2, a + da)
            c = pol(cx, cy, r1 - h * 0.25, a + da / 2)
            out.append(camino(f"M{f(p0[0])},{f(p0[1])} Q{f(c[0])},{f(c[1])} {f(p1[0])},{f(p1[1])}"))
    return out


def mandala(seed):
    rng = random.Random(seed)
    cx, cy = 425, 535
    R = 385
    out = []
    # petalos grandes exteriores
    n_ext = rng.choice([8, 12, 16])
    tipos = ["petalo", "petalo_doble", "circulos", "festones", "zigzag", "gota", "radios", "hojas", "arcos"]
    # radios de los anillos
    n_anillos = rng.choice([5, 6, 6, 7])
    bordes = [55]
    r_int = R * 0.80
    paso = (r_int - 55) / n_anillos
    for i in range(n_anillos):
        bordes.append(55 + paso * (i + 1) + rng.uniform(-paso * 0.18, paso * 0.18) * (i < n_anillos - 1))
    # exterior: petalos grandes por fuera del ultimo circulo
    ext = rng.choice(["petalo_doble", "petalo", "gota"]) if n_ext >= 12 else rng.choice(["petalo_doble", "petalo"])
    out += _anillo(cx, cy, bordes[-1], R, n_ext, ext, -math.pi / 2, rng)
    out.append(circulo(cx, cy, bordes[-1], blanco=True))
    previo = None
    sim = rng.choice([12, 16, 18, 24])
    for i in range(n_anillos - 1, -1, -1):
        r1, r2 = bordes[i], bordes[i + 1] if i + 1 < len(bordes) else bordes[-1]
        if i == n_anillos - 1:
            r1, r2 = bordes[i], bordes[i + 1]
        # mas motivos en anillos externos
        n = max(8, int(sim * (r2 / r_int) * rng.choice([1, 1, 1.5])) // 4 * 4)
        tipo = rng.choice([t for t in tipos if t != previo])
        previo = tipo
        out += _anillo(cx, cy, r1, r2, n, tipo, -math.pi / 2 + (math.pi / n if i % 2 else 0), rng)
        out.append(circulo(cx, cy, r1, w=2.6))
    # centro
    nc = rng.choice([6, 8, 10])
    out += _anillo(cx, cy, 12, 55, nc, "petalo", -math.pi / 2, rng)
    out.append(circulo(cx, cy, 12, w=2.4))
    return "\n".join(out)


# ===========================================================================
# PATRONES GEOMETRICOS (recortados a un marco redondeado)
# ===========================================================================
MARCO = (60, 70, 730, 960)  # x, y, ancho, alto


def _marco(contenido, uid):
    x, y, w, h = MARCO
    return (f'<defs><clipPath id="m{uid}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="28"/></clipPath></defs>\n'
            f'<g clip-path="url(#m{uid})">\n{contenido}\n</g>\n'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="28" {T(4)}/>')


def geo_hexagonos(seed):
    rng = random.Random(seed)
    r = rng.choice([58, 66, 74])
    out = []
    dx = r * math.sqrt(3)
    dy = r * 1.5
    var = rng.choice(["estrella", "anidado", "flor"])
    fila = 0
    y = 40
    while y < 1080:
        x = 30 + (dx / 2 if fila % 2 else 0)
        while x < 860:
            pts = [pol(x, y, r, math.pi / 6 + k * math.pi / 3) for k in range(6)]
            out.append(poligono(pts))
            if var == "estrella":
                a = [pol(x, y, r * 0.78, math.pi / 6 + k * math.pi / 3) for k in range(6)]
                out.append(poligono([a[0], a[2], a[4]], w=2))
                out.append(poligono([a[1], a[3], a[5]], w=2))
                out.append(circulo(x, y, r * 0.2, w=2))
            elif var == "anidado":
                out.append(poligono([pol(x, y, r * 0.62, k * math.pi / 3) for k in range(6)], w=2))
                out.append(poligono([pol(x, y, r * 0.3, math.pi / 6 + k * math.pi / 3) for k in range(6)], w=2))
            else:
                for k in range(6):
                    p = pol(x, y, r * 0.5, k * math.pi / 3)
                    out.append(circulo(p[0], p[1], r * 0.32, w=1.8))
                out.append(circulo(x, y, r * 0.18, w=2))
            x += dx
        y += dy
        fila += 1
    return _marco("\n".join(out), seed)


def geo_flor_de_vida(seed):
    rng = random.Random(seed)
    r = rng.choice([70, 80, 90])
    out = []
    dx = r
    dy = r * math.sqrt(3) / 2
    fila = 0
    y = 20
    while y < 1100:
        x = 20 + (r / 2 if fila % 2 else 0)
        while x < 880:
            out.append(circulo(x, y, r, w=2.2))
            x += dx
        y += dy
        fila += 1
    # medallon central blanco con mandala chico
    cx, cy = 425, 550
    rc = rng.choice([150, 170])
    out.append(circulo(cx, cy, rc, w=4, blanco=True))
    out += _anillo(cx, cy, 30, rc - 12, 12, rng.choice(["petalo_doble", "gota"]), -math.pi / 2, rng)
    out.append(circulo(cx, cy, rc - 12, w=2))
    out.append(circulo(cx, cy, 30, w=2.4))
    out += _anillo(cx, cy, 8, 30, 8, "petalo", -math.pi / 2, rng)
    return _marco("\n".join(out), seed)


def geo_truchet(seed):
    rng = random.Random(seed)
    t = rng.choice([90, 104, 122])
    out = []
    for gy in range(0, 1100, t):
        for gx in range(0, 860, t):
            if rng.random() < 0.5:
                out.append(camino(f"M{gx + t / 2},{gy} A{t / 2},{t / 2} 0 0 1 {gx},{gy + t / 2}"))
                out.append(camino(f"M{gx + t},{gy + t / 2} A{t / 2},{t / 2} 0 0 0 {gx + t / 2},{gy + t}"))
                out.append(camino(f"M{gx + t * 0.25},{gy} A{t * 0.25},{t * 0.25} 0 0 1 {gx},{gy + t * 0.25}", w=1.8))
                out.append(camino(f"M{gx + t * 0.75},{gy} A{t * 0.75},{t * 0.75} 0 0 1 {gx},{gy + t * 0.75}", w=1.8))
                out.append(camino(f"M{gx + t},{gy + t * 0.25} A{t * 0.75},{t * 0.75} 0 0 0 {gx + t * 0.25},{gy + t}", w=1.8))
                out.append(camino(f"M{gx + t},{gy + t * 0.75} A{t * 0.25},{t * 0.25} 0 0 0 {gx + t * 0.75},{gy + t}", w=1.8))
            else:
                out.append(camino(f"M{gx + t / 2},{gy} A{t / 2},{t / 2} 0 0 0 {gx + t},{gy + t / 2}"))
                out.append(camino(f"M{gx},{gy + t / 2} A{t / 2},{t / 2} 0 0 1 {gx + t / 2},{gy + t}"))
                out.append(camino(f"M{gx + t * 0.75},{gy} A{t * 0.25},{t * 0.25} 0 0 0 {gx + t},{gy + t * 0.25}", w=1.8))
                out.append(camino(f"M{gx + t * 0.25},{gy} A{t * 0.75},{t * 0.75} 0 0 0 {gx + t},{gy + t * 0.75}", w=1.8))
                out.append(camino(f"M{gx},{gy + t * 0.25} A{t * 0.75},{t * 0.75} 0 0 1 {gx + t * 0.75},{gy + t}", w=1.8))
                out.append(camino(f"M{gx},{gy + t * 0.75} A{t * 0.25},{t * 0.25} 0 0 1 {gx + t * 0.25},{gy + t}", w=1.8))
    return _marco("\n".join(out), seed)


def geo_estrellas8(seed):
    """Teselado de estrellas de 8 puntas (estilo mosaico)."""
    rng = random.Random(seed)
    t = rng.choice([120, 136, 150])
    out = []
    for gy in range(-t, 1150, t):
        for gx in range(-t, 900, t):
            cx, cy = gx + t / 2, gy + t / 2
            r = t * 0.5
            sq1 = [pol(cx, cy, r * 0.92, math.pi / 4 + k * math.pi / 2) for k in range(4)]
            sq2 = [pol(cx, cy, r * 0.92, k * math.pi / 2) for k in range(4)]
            out.append(poligono(sq1, w=2.2))
            out.append(poligono(sq2, w=2.2))
            out.append(poligono([pol(cx, cy, r * 0.38, math.pi / 8 + k * math.pi / 4) for k in range(8)], w=2))
            out.append(circulo(cx, cy, r * 0.14, w=1.8))
            # rombo de union en las esquinas
            out.append(poligono([(gx, gy - t * 0.17), (gx + t * 0.17, gy), (gx, gy + t * 0.17), (gx - t * 0.17, gy)], w=2))
    return _marco("\n".join(out), seed)


def geo_escamas(seed):
    rng = random.Random(seed)
    r = rng.choice([46, 54, 62])
    out = []
    fila = 0
    y = 1100 + r
    filas = []
    while y > -r:
        filas.append((y, fila))
        y -= r * 0.62
        fila += 1
    # se dibuja de abajo hacia arriba para que cada fila tape a la anterior
    for y, fila in reversed(filas):
        x = (r if fila % 2 else 0)
        while x < 900:
            out.append(camino(f"M{f(x - r)},{f(y)} A{r},{r} 0 0 1 {f(x + r)},{f(y)} Z", blanco=True))
            out.append(camino(f"M{f(x - r * 0.62)},{f(y)} A{r * 0.62},{r * 0.62} 0 0 1 {f(x + r * 0.62)},{f(y)}", w=1.8))
            out.append(camino(f"M{f(x - r * 0.28)},{f(y)} A{r * 0.28},{r * 0.28} 0 0 1 {f(x + r * 0.28)},{f(y)}", w=1.6))
            x += 2 * r
    return _marco("\n".join(out), seed)


def geo_ondas(seed):
    rng = random.Random(seed)
    out = []
    amp = rng.choice([26, 32, 38])
    lam = rng.choice([180, 210, 240])
    sep = rng.choice([44, 52])
    y = 40
    k = 0
    while y < 1080:
        pts = []
        for x in range(0, 880, 8):
            pts.append((x, y + amp * math.sin(2 * math.pi * x / lam + k * 0.6)))
        out.append(f'<polyline points="{P(*pts)}" {T(2.4)}/>')
        if k % 2 == 0:
            for x0 in range(int(lam / 4 + (k % 4) * lam / 4), 880, lam):
                yy = y + amp * math.sin(2 * math.pi * x0 / lam + k * 0.6) + sep / 2
                out.append(circulo(x0, yy, sep * 0.22, w=1.8))
        y += sep
        k += 1
    return _marco("\n".join(out), seed)


GEOMETRICOS = [geo_hexagonos, geo_flor_de_vida, geo_truchet, geo_estrellas8, geo_escamas, geo_ondas]
NOMBRES_GEO = {
    "geo_hexagonos": "Hexágonos",
    "geo_flor_de_vida": "Flor de la vida",
    "geo_truchet": "Laberinto de curvas",
    "geo_estrellas8": "Estrellas de mosaico",
    "geo_escamas": "Escamas",
    "geo_ondas": "Ondas",
}


# ===========================================================================
# PAISAJES DE MONTANA
# ===========================================================================
def _cresta(rng, x0, x1, ybase, alt, picos):
    """Silueta de montanas con picos separados y desplazamiento de punto medio."""
    ancho = (x1 - x0) / picos
    clave = [(x0 - 10, ybase - alt * rng.uniform(0.15, 0.35))]
    picos_idx = []
    for k in range(picos):
        px = x0 + ancho * (k + rng.uniform(0.3, 0.7))
        py = ybase - alt * rng.uniform(0.7, 1.0)
        if k > 0:
            vx = (clave[-1][0] + px) / 2 + rng.uniform(-ancho * 0.1, ancho * 0.1)
            clave.append((vx, ybase - alt * rng.uniform(0.15, 0.4)))
        picos_idx.append(len(clave))
        clave.append((px, py))
    clave.append((x1 + 10, ybase - alt * rng.uniform(0.15, 0.35)))
    # desplazamiento de punto medio (2 pasadas) sin tocar picos ni valles
    pts = [clave[0]]
    marcas = {0}
    for a, b in zip(clave, clave[1:]):
        seg = [a, b]
        for _ in range(2):
            nuevo = [seg[0]]
            for p, q in zip(seg, seg[1:]):
                d = math.hypot(q[0] - p[0], q[1] - p[1])
                m = ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2 + rng.uniform(-d * 0.06, d * 0.06))
                nuevo += [m, q]
            seg = nuevo
        pts += seg[1:]
    picos_pts = []
    for idx in picos_idx:
        x, y = clave[idx]
        picos_pts.append((x, y, ybase - y))
    return pts, picos_pts


def _x_en_altura(pts, x_pico, y_obj, lado):
    """Busca sobre la cresta el x donde la ladera cruza la altura y_obj."""
    i = min(range(len(pts)), key=lambda k: abs(pts[k][0] - x_pico))
    paso = -1 if lado < 0 else 1
    while 0 <= i + paso < len(pts):
        a, b = pts[i], pts[i + paso]
        if (a[1] - y_obj) * (b[1] - y_obj) <= 0 and a[1] != b[1]:
            t = (y_obj - a[1]) / (b[1] - a[1])
            return a[0] + t * (b[0] - a[0])
        i += paso
    return None


def _nieve(pts, px, py, h, rng):
    s = h * 0.24
    y0 = py + s
    xa = _x_en_altura(pts, px, y0, -1)
    xb = _x_en_altura(pts, px, y0, 1)
    if xa is None or xb is None:
        return ""
    puntos = [(xa, y0)]
    n = 4
    for i in range(1, n):
        x = xa + (xb - xa) * i / n
        puntos.append((x, py + s * (0.6 if i % 2 else 1.18)))
    puntos.append((xb, y0))
    return f'<polyline points="{P(*puntos)}" {T(2)}/>'


def _pino(x, ybase, h, w=2.4):
    out = []
    ancho = h * 0.42
    out.append(f'<rect x="{f(x - h * 0.05)}" y="{f(ybase - h * 0.14)}" width="{f(h * 0.1)}" height="{f(h * 0.14)}" {B(w)}/>')
    for i, (y0, esc) in enumerate(((0.12, 1.0), (0.4, 0.8), (0.65, 0.58))):
        yb = ybase - h * y0
        yt = yb - h * 0.42
        a = ancho * esc
        out.append(poligono([(x - a, yb), (x, yt), (x + a, yb)], w=w, blanco=True))
    return "\n".join(out)


def _nube(x, y, s):
    d = (f"M{f(x - 60 * s)},{f(y)} "
         f"A{f(22 * s)},{f(22 * s)} 0 0 1 {f(x - 30 * s)},{f(y - 24 * s)} "
         f"A{f(30 * s)},{f(30 * s)} 0 0 1 {f(x + 18 * s)},{f(y - 34 * s)} "
         f"A{f(26 * s)},{f(26 * s)} 0 0 1 {f(x + 58 * s)},{f(y - 8 * s)} "
         f"A{f(14 * s)},{f(14 * s)} 0 0 1 {f(x + 60 * s)},{f(y)} Z")
    return camino(d, w=2.4, blanco=True)


def _pajaro(x, y, s):
    return camino(f"M{f(x - 14 * s)},{f(y - 4 * s)} Q{f(x - 7 * s)},{f(y - 10 * s)} {f(x)},{f(y)} "
                  f"Q{f(x + 7 * s)},{f(y - 10 * s)} {f(x + 14 * s)},{f(y - 4 * s)}", w=2.2)


def paisaje(seed):
    rng = random.Random(seed)
    x, y, w, h = MARCO
    out = []
    # sol
    sx, sy = rng.choice([(610, 250), (250, 240), (430, 300)])
    sr = rng.choice([58, 66, 74])
    estilo_sol = rng.choice(["rayos", "anillos"])
    if estilo_sol == "rayos":
        for k in range(16):
            a = k * math.pi / 8
            p1 = pol(sx, sy, sr + 14, a - 0.07)
            p2 = pol(sx, sy, sr + (46 if k % 2 == 0 else 30), a)
            p3 = pol(sx, sy, sr + 14, a + 0.07)
            out.append(poligono([p1, p2, p3], w=2))
    else:
        out.append(circulo(sx, sy, sr + 22, w=2))
        out.append(circulo(sx, sy, sr + 44, w=2))
    out.append(circulo(sx, sy, sr, w=2.6, blanco=True))
    # nubes (lejos del sol y sin pisarse)
    nubes = []
    intentos = 0
    while len(nubes) < 2 and intentos < 200:
        intentos += 1
        nx, ny = rng.uniform(150, 700), rng.uniform(150, 300)
        if math.hypot(nx - sx, ny - sy) < sr + 150:
            continue
        if any(abs(nx - a) < 190 and abs(ny - b) < 80 for a, b in nubes):
            continue
        nubes.append((nx, ny))
        out.append(_nube(nx, ny, rng.uniform(0.9, 1.2)))
    # pajaros (del lado contrario al sol)
    bx = 180 if sx > 425 else 520
    by = rng.uniform(330, 380)
    for k in range(rng.choice([3, 4, 5])):
        out.append(_pajaro(bx + k * 38 + rng.uniform(-8, 8), by + rng.uniform(-20, 20), rng.uniform(0.8, 1.2)))
    # tres capas de montanas: lejos -> cerca
    capas = [(600, 220, rng.choice([2, 3])), (700, 200, rng.choice([2, 3])), (790, 120, 2)]
    for i, (yb, alt, picos) in enumerate(capas):
        pts, picos_pts = _cresta(rng, 20, 830, yb, alt, picos)
        out.append(poligono(pts + [(840, 1100), (10, 1100)], w=2.8, blanco=True))
        if i < 2:
            for px, py, ph in picos_pts:
                out.append(_nieve(pts, px, py, ph, rng))

    # lago o pradera
    if rng.random() < 0.5:
        izq = rng.random() < 0.5
        out.append(f'<rect x="0" y="800" width="850" height="400" {B(2.8)}/>')
        for k in range(8):
            yy = 830 + k * 26
            x0 = rng.uniform(420, 640) if izq else rng.uniform(80, 300)
            out.append(linea((x0, yy), (x0 + rng.uniform(70, 150), yy), w=2))
        # orilla con pinos
        ladera = "M0,1100 L0,890 Q300,860 440,1100 Z" if izq else "M850,1100 L850,890 Q550,860 410,1100 Z"
        out.append(camino(ladera, w=2.8, blanco=True))
        for k in range(3):
            px = (95 + k * 95) if izq else (755 - k * 95)
            out.append(_pino(px, 935 + k * 30, 190 - k * 25))
    else:
        out.append(camino("M0,850 Q260,770 520,840 T850,830 L850,1100 L0,1100 Z", w=2.8, blanco=True))
        for k in range(rng.choice([5, 6, 7])):
            px = 60 + k * 125 + rng.uniform(-25, 25)
            out.append(_pino(px, 900 + rng.uniform(0, 70), rng.uniform(140, 210)))
        # flores en primer plano
        for k in range(7):
            fx = 100 + k * 108 + rng.uniform(-20, 20)
            fy = rng.uniform(985, 1005)
            out.append(camino(f"M{f(fx)},{f(fy)} Q{f(fx + 6)},{f(fy + 25)} {f(fx)},{f(fy + 50)}", w=2))
            for j in range(6):
                p = pol(fx, fy, 14, j * math.pi / 3)
                out.append(circulo(p[0], p[1], 9, w=2, blanco=True))
            out.append(circulo(fx, fy, 7, w=2, blanco=True))
    return _marco("\n".join(out), seed)
