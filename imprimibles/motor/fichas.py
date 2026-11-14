"""Paquete fichas-bilingues/: fichas español-inglés para niños de 3 a 7 años."""
import math
import random
from datetime import date, timedelta

from . import animales as ani
from .animales import c as circ, e as elip, p as path, ojo
from .arte import f
from .comun import (RAIZ, medir, a_pdf, a_png, cargar, carta_svg, cfg, con_salida, correr_goteo, esc, escribir,
                    fecha_salida, guardar, hoy, miniatura, pagina_html, preview_pin, rss)

PAQ = "fichas-bilingues"
DIR = RAIZ / PAQ

AZUL = "#1f5a7a"
NARANJA = "#c4581c"


# ---------------------------------------------------------------------------
# Objetos extra (caja 200x200)
# ---------------------------------------------------------------------------
def manzana(w):
    return (path("M100,52 C70,30 22,44 26,100 C30,160 70,192 100,176 C130,192 170,160 174,100 C178,44 130,30 100,52Z", w) +
            path("M100,54 Q98,30 106,14", w, False) +
            path("M106,34 C122,14 150,18 152,24 C140,40 120,42 106,34Z", w) +
            path("M50,84 Q54,66 70,60", w * 0.8, False))


def sol(w):
    o = []
    for k in range(12):
        a = k * math.pi / 6
        x1, y1 = 100 + 62 * math.cos(a), 100 + 62 * math.sin(a)
        x2, y2 = 100 + 92 * math.cos(a), 100 + 92 * math.sin(a)
        o.append(path(f"M{f(x1)},{f(y1)} L{f(x2)},{f(y2)}", w, False))
    o.append(circ(100, 100, 52, w))
    o.append(ojo(82, 92, 7, w) + ojo(118, 92, 7, w))
    o.append(path("M78,114 Q100,136 122,114", w, False))
    return "".join(o)


def zanahoria(w):
    return (path("M92,52 C80,26 60,20 52,24 C60,34 76,46 90,56Z", w) +
            path("M100,52 C100,24 106,10 114,8 C116,24 110,42 104,54Z", w) +
            path("M108,56 C124,30 144,26 152,30 C142,42 126,52 112,60Z", w) +
            path("M72,64 C90,48 128,50 136,68 C140,90 116,150 104,190 C96,196 92,192 92,186 C80,150 62,86 72,64Z", w) +
            path("M80,92 L96,94 M88,124 L104,126 M112,104 L124,106 M96,154 L108,156", w * 0.8, False))


def uvas(w):
    o = [path("M100,40 Q104,22 116,12", w, False),
         path("M104,30 C120,10 152,16 156,24 C140,40 120,40 104,30Z", w)]
    filas = [(4, 60), (4, 92), (3, 124), (2, 154), (1, 182)]
    for n, y in filas:
        for k in range(n):
            x = 100 + (k - (n - 1) / 2) * 32
            o.append(circ(x, y, 17, w))
    return "".join(o)


def nube(w):
    return path("M40,140 C10,140 10,96 42,96 C40,60 90,48 104,76 C116,50 168,56 164,98 C196,100 196,140 164,140Z", w)


def estrella(w):
    pts = []
    for k in range(10):
        r = 88 if k % 2 == 0 else 38
        a = -math.pi / 2 + k * math.pi / 5
        pts.append(f"{f(100 + r * math.cos(a))},{f(108 + r * math.sin(a))}")
    return path("M" + " L".join(pts) + "Z", w) + ojo(86, 104, 6, w) + ojo(114, 104, 6, w) + path("M90,124 Q100,134 110,124", w, False)


def corazon(w):
    return path("M100,176 C40,130 14,96 30,64 C46,34 86,38 100,70 C114,38 154,34 170,64 C186,96 160,130 100,176Z", w)


def globo(w):
    return (elip(100, 82, 58, 70, w) + path("M92,150 L108,150 L100,160Z", w) +
            path("M100,160 C88,176 112,184 98,198", w, False) + path("M64,60 Q72,40 90,34", w * 0.8, False))


def queso(w):
    return (path("M20,150 L20,90 L180,60 L180,150Z", w) + path("M20,90 L120,40 L180,60", w) +
            circ(60, 116, 12, w) + circ(120, 104, 9, w) + circ(150, 130, 10, w) + circ(92, 138, 7, w))


def hoja(w):
    return (path("M100,186 C30,140 30,60 100,14 C170,60 170,140 100,186Z", w) +
            path("M100,186 L100,30 M100,80 L70,60 M100,80 L130,60 M100,120 L64,96 M100,120 L136,96", w * 0.8, False))


OBJETOS = {"manzana": manzana, "sol": sol, "zanahoria": zanahoria, "uvas": uvas, "nube": nube, "estrella": estrella,
           "corazon": corazon, "globo": globo, "queso": queso, "hoja": hoja}


def dibujo(clave, x, y, tam, trazo=4):
    s = tam / 200
    fn = OBJETOS[clave] if clave in OBJETOS else ani.ANIMALES[clave][0]
    return f'<g transform="translate({f(x)},{f(y)}) scale({s:.4f})">{fn(trazo / s)}</g>'


# ---------------------------------------------------------------------------
# Contenido
# ---------------------------------------------------------------------------
COLORES = [("rojo", "red", "manzana", "la manzana", "the apple"),
           ("azul", "blue", "ballena", "la ballena", "the whale"),
           ("amarillo", "yellow", "sol", "el sol", "the sun"),
           ("verde", "green", "rana", "la rana", "the frog"),
           ("naranja", "orange", "zanahoria", "la zanahoria", "the carrot"),
           ("morado", "purple", "uvas", "las uvas", "the grapes"),
           ("rosa", "pink", "cerdo", "el cerdo", "the pig"),
           ("café", "brown", "oso", "el oso", "the bear"),
           ("gris", "gray", "elefante", "el elefante", "the elephant"),
           ("negro", "black", "gato", "el gato", "the cat")]
NUM_ES = "cero uno dos tres cuatro cinco seis siete ocho nueve diez once doce trece catorce quince dieciséis diecisiete dieciocho diecinueve veinte".split()
NUM_EN = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty".split()
LETRAS = [("A", "abeja", "abeja", "apple", "manzana"), ("B", "ballena", "ballena", "bear", "oso"),
          ("C", "conejo", "conejo", "cat", "gato"), ("D", "dos", None, "dog", "perro"),
          ("E", "elefante", "elefante", "egg", None), ("F", "flor", None, "fish", "pez"),
          ("G", "gato", "gato", "grapes", "uvas"), ("H", "hoja", "hoja", "heart", "corazon"),
          ("I", "isla", None, "ice", None), ("J", "jirafa", None, "jump", None),
          ("K", "koala", None, "kite", None), ("L", "león", "leon", "leaf", "hoja"),
          ("M", "mariposa", "mariposa", "mouse", "raton"), ("N", "nube", "nube", "nest", None),
          ("Ñ", "ñandú", None, "", None), ("O", "oso", "oso", "owl", "buho"),
          ("P", "pato", "pato", "pig", "cerdo"), ("Q", "queso", "queso", "queen", None),
          ("R", "rana", "rana", "rabbit", "conejo"), ("S", "sol", "sol", "sun", "sol"),
          ("T", "tortuga", "tortuga", "turtle", "tortuga"), ("U", "uvas", "uvas", "umbrella", None),
          ("V", "vaca", None, "van", None), ("W", "wafle", None, "whale", "ballena"),
          ("X", "xilófono", None, "x-ray", None), ("Y", "yoyó", None, "yellow", None),
          ("Z", "zanahoria", "zanahoria", "zebra", None)]
ORDEN_ANIMALES = ["gato", "perro", "pez", "pato", "conejo", "oso", "leon", "elefante", "rana", "buho", "cerdo",
                  "mariposa", "tortuga", "abeja", "raton", "pajaro", "ballena", "caracol", "mariquita"]
NOMBRES_EN_ART = {"el": "the", "la": "the"}


def catalogo():
    """Lista ordenada de fichas base (se intercalan los 4 tipos)."""
    listas = [[("color", i) for i in range(len(COLORES))],
              [("numero", i) for i in range(1, 21)],
              [("animal", k) for k in ORDEN_ANIMALES],
              [("letra", i) for i in range(len(LETRAS))]]
    out = []
    i = 0
    while any(listas):
        l = listas[i % 4]
        if l:
            out.append(l.pop(0))
        i += 1
    return out


# ---------------------------------------------------------------------------
# Piezas de dibujo de la ficha
# ---------------------------------------------------------------------------
def linea_mixta(y, partes, centro=425, maximo=730):
    """partes: lista de (texto, tam, peso, color, italica). Se centran en una linea."""
    anchos = [medir(t, tam, peso, it) for t, tam, peso, col, it in partes]
    total = sum(anchos)
    k = min(1.0, maximo / total) if total else 1
    x = centro - total * k / 2
    o = []
    for (t, tam, peso, col, it), a in zip(partes, anchos):
        estilo = ' font-style="italic"' if it else ""
        o.append(f'<text x="{f(x)}" y="{y}" font-family="Inter" font-weight="{peso}" font-size="{f(tam * k)}" '
                 f'fill="{col}"{estilo} xml:space="preserve">{esc(t)}</text>')
        x += a * k
    return "\n".join(o)


def encabezado(es, en, instr_es, instr_en):
    tit = [(es, 66, 900, NARANJA, False)]
    if en:
        tit += [("  ·  ", 66, 900, "#aaaaaa", False), (en, 66, 900, AZUL, False)]
    return "\n".join([
        f'<text x="60" y="58" font-family="Inter" font-size="17" fill="#333">Nombre / Name: ______________________</text>',
        f'<text x="790" y="58" text-anchor="end" font-family="Inter" font-size="14" fill="#888">{esc(cfg()["sitio"])}</text>',
        linea_mixta(140, tit),
        linea_mixta(182, [(instr_es, 20, 700, NARANJA, False), ("  /  ", 20, 400, "#333333", False),
                          (instr_en, 20, 400, AZUL, True)]),
    ])


def renglon(x, y, ancho, alto):
    """Renglon de caligrafia: linea superior, media punteada, base. y = linea base."""
    xh = y - alto * 0.75
    return "\n".join([
        f'<line x1="{x}" y1="{f(y - alto)}" x2="{x + ancho}" y2="{f(y - alto)}" stroke="#7aa6c2" stroke-width="1.5"/>',
        f'<line x1="{x}" y1="{f(xh)}" x2="{x + ancho}" y2="{f(xh)}" stroke="#7aa6c2" stroke-width="1.2" stroke-dasharray="8 6"/>',
        f'<line x1="{x}" y1="{y}" x2="{x + ancho}" y2="{y}" stroke="#d26a3a" stroke-width="2"/>',
    ])


def texto_repasar(x, y, txt, fs, modelo=False, anchor="start", peso=600):
    if modelo:
        return (f'<text x="{f(x)}" y="{f(y)}" text-anchor="{anchor}" font-family="Inter" font-weight="{peso}" '
                f'font-size="{f(fs)}" fill="#2b2b2b">{esc(txt)}</text>')
    return (f'<text x="{f(x)}" y="{f(y)}" text-anchor="{anchor}" font-family="Inter" font-weight="{peso}" font-size="{f(fs)}" '
            f'fill="#ececec" stroke="#8c8c8c" stroke-width="{f(max(1.2, fs / 60))}" stroke-dasharray="{f(fs / 22)} {f(fs / 30)}" '
            f'stroke-linejoin="round">{esc(txt)}</text>')


def fila_repaso(y, txt, alto=70, veces=None, x0=60, ancho=730):
    """Renglon con el modelo + copias para repasar. Ancho por caracter aprox 0.62*fs."""
    fs = alto / 0.727
    w_txt = max(medir(txt, fs, 500), 0.5 * fs)
    sep = 0.45 * fs
    if veces is None:
        veces = max(1, int((ancho + sep) // (w_txt + sep)))
    o = [renglon(x0, y, ancho, alto)]
    x = x0 + 6
    for k in range(veces):
        o.append(texto_repasar(x, y, txt, fs, modelo=(k == 0), peso=500))
        x += w_txt + sep
    return "\n".join(o)


def palabra_repaso(y, txt, color, etiqueta, alto=56):
    fs = alto / 0.727
    # achicar si no entran al menos el modelo y una copia
    while 2 * medir(txt, fs, 500) + 60 > 715 and fs > 30:
        fs *= 0.92
    o = [renglon(60, y, 730, alto),
         f'<text x="60" y="{f(y - alto - 10)}" font-family="Inter" font-weight="700" font-size="16" fill="{color}">{esc(etiqueta)}</text>',
         texto_repasar(70, y, txt, fs, modelo=True, peso=500)]
    a = medir(txt, fs, 500) + 50
    x = 70 + a
    while x + a - 50 < 785:
        o.append(texto_repasar(x, y, txt, fs, peso=500))
        x += a
    return "\n".join(o)


def pie():
    return (f'<text x="425" y="1072" text-anchor="middle" font-family="Inter" font-size="12" fill="#888">'
            f'{esc(cfg()["sitio"])} · Fichas bilingües gratis para uso personal y en el aula</text>')


# ---------------------------------------------------------------------------
# Tipos de ficha
# ---------------------------------------------------------------------------
def ficha_color(i):
    es, en, obj, obj_es, obj_en = COLORES[i]
    o = [encabezado(es.upper(), en.upper(), f"Colorea {obj_es} de {es}", f"Color {obj_en} {en}")]
    o.append(f'<rect x="60" y="215" width="730" height="440" rx="24" fill="none" stroke="#000" stroke-width="2.5"/>')
    o.append(dibujo(obj, 425 - 185, 228, 370))
    # crayon para pintar del color
    o.append('<g transform="translate(700,520)"><path d="M0,40 L18,0 L36,40 Z" fill="#fff" stroke="#000" stroke-width="2.5"/>'
             '<rect x="0" y="40" width="36" height="70" rx="4" fill="#fff" stroke="#000" stroke-width="2.5"/>'
             '<line x1="0" y1="60" x2="36" y2="60" stroke="#000" stroke-width="2"/><line x1="0" y1="90" x2="36" y2="90" stroke="#000" stroke-width="2"/></g>')
    o.append(f'<text x="90" y="640" font-family="Inter" font-size="15" fill="#555">Pinta también el crayón / Color the crayon too</text>')
    o.append(palabra_repaso(780, es, NARANJA, "Repasa la palabra en español"))
    o.append(palabra_repaso(900, en, AZUL, "Trace the word in English"))
    o.append(f'<text x="60" y="985" font-family="Inter" font-size="18" fill="#333">'
             f'¿Qué más es {esc(es)}? / What else is {esc(en)}? ______________________________</text>')
    titulo = f"Ficha bilingüe del color {es} ({en}) para niños"
    alt = f"Ficha para colorear y repasar el color {es} / {en} en español e inglés, con dibujo de {obj_es}"
    return o, titulo, f"color-{_slug(es)}-{en}", alt, f"{es.capitalize()} · {en.capitalize()}"


def ficha_numero(n):
    es, en = NUM_ES[n], NUM_EN[n]
    o = [encabezado(f"{n} · {es}", en, "Repasa y cuenta", "Trace and count")]
    # numero grande a repasar
    o.append(texto_repasar(250, 520, str(n), 330 if n < 10 else 290, anchor="middle", peso=700))
    # estrellas para contar y colorear
    cols = 5 if n <= 10 else 5
    filas = math.ceil(n / cols)
    tam = 62 if n <= 10 else 52
    x0 = 470
    y0 = 240 if n > 10 else 260
    for k in range(n):
        r, c = divmod(k, cols)
        o.append(dibujo("estrella", x0 + c * (tam + 4), y0 + r * (tam + 2), tam, trazo=2.6))
    o.append(f'<text x="600" y="{y0 + filas * (tam + 2) + 30}" text-anchor="middle" font-family="Inter" font-size="16" fill="#555">'
             f'Colorea {n} {"estrella" if n == 1 else "estrellas"} / Color {n} {"star" if n == 1 else "stars"}</text>')
    o.append(fila_repaso(660, str(n), alto=72))
    o.append(palabra_repaso(800, es, NARANJA, "Repasa en español"))
    o.append(palabra_repaso(930, en, AZUL, "Trace in English"))
    titulo = f"Número {n} para repasar: {es} / {en} (ficha bilingüe)"
    alt = f"Ficha para repasar el número {n}, contar estrellas y escribir {es} y {en}"
    return o, titulo, f"numero-{n}-{_slug(es)}-{en}", alt, f"Número {n} · {en}"


def ficha_animal(clave):
    fn, nom, en, art, son_es, son_en = ani.ANIMALES[clave]
    o = [encabezado(f"{art} {nom}".upper(), f"the {en}".upper(), "Colorea y repasa", "Color and trace")]
    o.append(f'<rect x="60" y="215" width="730" height="440" rx="24" fill="none" stroke="#000" stroke-width="2.5"/>')
    o.append(ani.dibujar(clave, 425 - 185, 228, 370, trazo=4))
    if son_es:
        o.append(f'<text x="80" y="640" font-family="Inter" font-size="20" fill="#333">Hace / It says: '
                 f'<tspan font-weight="800" fill="{NARANJA}">“{esc(son_es)}”</tspan> / '
                 f'<tspan font-weight="800" fill="{AZUL}">“{esc(son_en)}”</tspan></text>')
    o.append(palabra_repaso(780, nom, NARANJA, "Repasa la palabra en español"))
    o.append(palabra_repaso(900, en, AZUL, "Trace the word in English"))
    o.append(f'<text x="60" y="985" font-family="Inter" font-size="18" fill="#333">'
             f'¿De qué color es? / What color is it? ______________________________</text>')
    titulo = f"{nom.capitalize()} en inglés: {en} – ficha para colorear y repasar"
    alt = f"Ficha bilingüe: dibujo de {art} {nom} ({en}) para colorear y palabras para repasar"
    return o, titulo, f"animal-{_slug(nom)}-{en}", alt, f"{nom.capitalize()} · {en.capitalize()}"


def ficha_letra(i):
    L, pal_es, dib_es, pal_en, dib_en = LETRAS[i]
    o = [encabezado(f"{L} {L.lower()}", "", f"{L} de {pal_es}",
                    f"{L} is for {pal_en}" if pal_en else "Only in Spanish!")]
    o.append(texto_repasar(150, 470, L, 260, anchor="middle", peso=700))
    o.append(texto_repasar(330, 470, L.lower(), 260, anchor="middle", peso=700))
    # dibujos
    if dib_es:
        o.append(dibujo(dib_es, 440, 230, 160, trazo=3))
    o.append(f'<text x="520" y="420" text-anchor="middle" font-family="Inter" font-weight="800" font-size="26" fill="{NARANJA}">{esc(pal_es)}</text>')
    if pal_en:
        if dib_en:
            o.append(dibujo(dib_en, 620, 230, 160, trazo=3))
        o.append(f'<text x="700" y="420" text-anchor="middle" font-family="Inter" font-weight="800" font-size="26" fill="{AZUL}">{esc(pal_en)}</text>')
    o.append(fila_repaso(580, L, alto=70))
    o.append(fila_repaso(700, L.lower() + " ", alto=70) if False else fila_repaso(700, L.lower(), alto=70))
    o.append(palabra_repaso(830, pal_es, NARANJA, "Repasa en español"))
    if pal_en:
        o.append(palabra_repaso(950, pal_en, AZUL, "Trace in English"))
    titulo = f"Letra {L} para repasar: {L} de {pal_es}" + (f" / {L} is for {pal_en}" if pal_en else "")
    alt = f"Ficha de caligrafía de la letra {L} mayúscula y minúscula, con palabras en español e inglés"
    return o, titulo, f"letra-{_slug(L)}", alt, f"Letra {L} {L.lower()}"


def ficha_unir(k):
    """Repaso infinito: une cada animal con su nombre en ingles."""
    rng = random.Random(k * 101 + 5)
    claves = rng.sample(ORDEN_ANIMALES, 4)
    ingles = [ani.ANIMALES[c][2] for c in claves]
    orden = ingles[:]
    while orden == ingles:
        rng.shuffle(orden)
    o = [encabezado("UNE", "MATCH", "Une cada animal con su nombre en inglés", "Match each animal to its name")]
    for i, c in enumerate(claves):
        y = 230 + i * 200
        o.append(ani.dibujar(c, 90, y, 170, trazo=3))
        o.append(f'<text x="175" y="{y + 190}" text-anchor="middle" font-family="Inter" font-weight="700" font-size="20" fill="{NARANJA}">{esc(ani.ANIMALES[c][1])}</text>')
        o.append(f'<circle cx="300" cy="{y + 90}" r="9" fill="#000"/>')
        o.append(f'<circle cx="540" cy="{y + 90}" r="9" fill="#000"/>')
        o.append(f'<text x="570" y="{y + 102}" font-family="Inter" font-weight="800" font-size="40" fill="{AZUL}">{esc(orden[i])}</text>')
    titulo = f"Une el animal con su nombre en inglés – repaso n.º {k}"
    alt = "Ficha bilingüe para unir con flechas cuatro animales con su nombre en inglés"
    return o, titulo, f"une-animales-ingles-{k:03d}", alt, "Une con flechas · Match"


def _slug(s):
    import unicodedata
    s = "".join(ch for ch in unicodedata.normalize("NFD", s.lower()) if unicodedata.category(ch) != "Mn")
    return "".join(ch if ch.isalnum() else "-" for ch in s).strip("-")


def receta(n):
    cat = catalogo()
    if n <= len(cat):
        tipo, arg = cat[n - 1]
    else:
        tipo, arg = "unir", n - len(cat)
    fn = {"color": ficha_color, "numero": ficha_numero, "animal": ficha_animal, "letra": ficha_letra,
          "unir": ficha_unir}[tipo]
    o, titulo, slug, alt, corto = fn(arg)
    return tipo, "\n".join(o + [pie()]), titulo, slug, alt, corto


TIPOS = {"color": "Colores", "numero": "Números del 1 al 20", "animal": "Animales", "letra": "Letras",
         "unir": "Repaso: une con flechas"}


def generar_item(n, fecha):
    tipo, inner, titulo, slug, alt, corto = receta(n)
    carp = DIR / "archivos"
    carp.mkdir(parents=True, exist_ok=True)
    svg = carta_svg(inner)
    a_pdf([svg], carp / f"{slug}.pdf")
    pv = preview_pin(inner, corto, "Ficha bilingüe gratis · PDF", "#fff4e6", "#c4581c")
    a_png(pv, carp / f"{slug}.png", 1000, 1500)
    miniatura(carp / f"{slug}.png", carp / f"{slug}-mini.jpg")
    return {"n": n, "tipo": tipo, "titulo": titulo, "slug": slug, "alt": alt, "fecha": fecha.isoformat()}


def agregar(cantidad=None, fecha=None, dias_buffer=None):
    fecha = fecha or hoy()
    datos = cargar(PAQ)
    hechos = {it["n"] for it in datos["items"]}
    descartados = set(datos.get("descartados", []))
    nuevos = 0

    def falta():
        if cantidad is not None:
            return nuevos < cantidad
        total = len(datos["items"])
        return total == 0 or fecha_salida(total - 1, PAQ) < fecha + timedelta(days=dias_buffer)

    n = 1
    while falta():
        if n not in hechos and n not in descartados:
            it = generar_item(n, fecha)
            datos["items"].append(it)
            nuevos += 1
            print(f"  fichas: item {n} -> {it['slug']}")
        n += 1
    guardar(PAQ, datos)
    return nuevos


def _desc(it):
    t = it["tipo"]
    base = {"color": "Ficha para aprender los colores en español e inglés: colorear el dibujo y repasar las palabras.",
            "numero": "Ficha para repasar el número, contar y colorear estrellas y escribir el nombre en español e inglés.",
            "animal": "Ficha bilingüe de animales: colorear el dibujo, aprender el sonido y repasar el nombre en español e inglés.",
            "letra": "Ficha de caligrafía para repasar la letra mayúscula y minúscula con palabras en español e inglés.",
            "unir": "Ficha de repaso: unir con flechas cada animal con su nombre en inglés."}[t]
    return base + " Para niños de 3 a 7 años. PDF gratis tamaño carta."


def construir():
    c = cfg()
    B = c["base_url"]
    U = f"{B}/fichas-bilingues"
    datos = cargar(PAQ)
    todos = con_salida(datos["items"], PAQ)
    dia = hoy()
    pub = [it for it in todos if date.fromisoformat(it["salida"]) <= dia]
    pub_set = {it["slug"] for it in pub}
    pub_rev = list(reversed(pub))

    def tarjetas(items):
        return '<ul class="grilla">' + "".join(
            f'<li><a href="{it["slug"]}.html"><img src="archivos/{it["slug"]}-mini.jpg" width="400" height="600" loading="lazy" '
            f'alt="{esc(it["alt"])}"><span>{esc(it["titulo"])}</span></a></li>' for it in items) + "</ul>"

    for it in todos:
        rel = [x for x in pub_rev if x["tipo"] == it["tipo"] and x["slug"] != it["slug"]][:8]
        desc = _desc(it)
        cuerpo = f"""
<div class="ficha"><div><img src="archivos/{it['slug']}.png" width="1000" height="1500" alt="{esc(it['alt'])}"></div>
<div><p>{esc(desc)}</p>
<p><a class="boton" href="archivos/{it['slug']}.pdf" download>Descargar PDF gratis</a></p>
<h2>Ideas para usarla</h2>
<ol><li>Lean juntos la palabra en voz alta en los dos idiomas.</li>
<li>Repasen las letras grises siguiendo la línea punteada.</li>
<li>Colorear al final, como premio.</li></ol>
<!-- ADSENSE --></div></div>
{f"<h2>Más fichas de {esc(TIPOS[it['tipo']].lower())}</h2>" + tarjetas(rel) if rel else ""}
<p><a href="./">Ver todas las fichas bilingües</a></p>"""
        html = pagina_html(titulo=f"{it['titulo']} | PDF gratis", descripcion=desc, h1=it["titulo"],
                           canonical=f"{U}/{it['slug']}.html", cuerpo=cuerpo, imagen=f"{U}/archivos/{it['slug']}.png",
                           migas=[("Imprimibles", f"{B}/"), ("Fichas bilingües", f"{U}/"), (it["titulo"], None)],
                           amazon=c["link_amazon_fichas"], texto_amazon="Libros bilingües para niños",
                           extra_head="" if it["slug"] in pub_set else '<meta name="robots" content="noindex">\n')
        escribir(DIR / f"{it['slug']}.html", html)
    secciones = ""
    for t, nom in TIPOS.items():
        xs = [x for x in pub if x["tipo"] == t]
        if xs:
            secciones += f"<h2>{esc(nom)}</h2>{tarjetas(xs)}"
    cuerpo = (f"<p>Fichas gratis en español e inglés para niños de 3 a 7 años: colores, números del 1 al 20, animales y "
              f"letras para repasar. Cada ficha se imprime en tamaño carta y combina colorear, contar y escribir. "
              f"Hay {len(pub)} fichas y salen nuevas casi todos los días.</p>"
              f"<h2>Lo más nuevo</h2>{tarjetas(pub_rev[:8])}{secciones}")
    html = pagina_html(titulo="Fichas bilingües español-inglés para niños (PDF gratis)",
                       descripcion="Fichas para imprimir en español e inglés para niños de 3 a 7 años: colores, números, animales y letras para repasar. PDF gratis.",
                       h1="Fichas bilingües español–inglés para niños", canonical=f"{U}/", cuerpo=cuerpo,
                       imagen=f"{U}/archivos/{pub_rev[0]['slug']}.png" if pub_rev else None,
                       migas=[("Imprimibles", f"{B}/"), ("Fichas bilingües", None)],
                       amazon=c["link_amazon_fichas"], texto_amazon="Libros bilingües para niños")
    escribir(DIR / "index.html", html)
    items = [{"titulo": it["titulo"] + " (PDF gratis)", "link": f"{U}/{it['slug']}.html", "descripcion": _desc(it),
              "imagen": f"{U}/archivos/{it['slug']}.png", "fecha": date.fromisoformat(it["salida"]),
              "guid": f"fichas-{it['slug']}"} for it in todos]
    rss(titulo="Fichas bilingües español-inglés para niños", link=f"{U}/",
        descripcion="Fichas gratis para imprimir en español e inglés.", items=items,
        destino=DIR / "rss-completo.xml", self_url=f"{U}/rss.xml")
    correr_goteo(DIR / "rss-completo.xml", DIR / "rss.xml", PAQ, dia)
    # sitemap parcial para sumar al del sitio
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
          f"<url><loc>{esc(U)}/</loc></url>"]
    sm += [f"<url><loc>{esc(U)}/{it['slug']}.html</loc><lastmod>{it['salida']}</lastmod></url>" for it in pub]
    sm.append("</urlset>\n")
    escribir(DIR / "sitemap.xml", "\n".join(sm))
