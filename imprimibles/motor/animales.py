"""Animales simples hechos con figuras geometricas (caja de 200x200).

Cada funcion recibe w (grosor de trazo en unidades de la caja) y devuelve SVG.
Se usan en las paginas para colorear y en las fichas bilingues.
"""
import math

from .arte import B, T, f


def c(cx, cy, r, w, blanco=True):
    return f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" {B(w) if blanco else T(w)}/>'


def e(cx, cy, rx, ry, w, blanco=True, rot=0):
    tr = f' transform="rotate({rot} {f(cx)} {f(cy)})"' if rot else ""
    return f'<ellipse cx="{f(cx)}" cy="{f(cy)}" rx="{f(rx)}" ry="{f(ry)}"{tr} {B(w) if blanco else T(w)}/>'


def p(d, w, blanco=True):
    return f'<path d="{d}" {B(w) if blanco else T(w)}/>'


def ojo(x, y, r, w):
    """Ojo con pupila negra y brillo."""
    return (c(x, y, r, w) + f'<circle cx="{f(x)}" cy="{f(y + r * 0.1)}" r="{f(r * 0.55)}" fill="#000"/>'
            f'<circle cx="{f(x + r * 0.2)}" cy="{f(y - r * 0.15)}" r="{f(r * 0.18)}" fill="#fff"/>')


def punto(x, y, r):
    return f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r)}" fill="#000"/>'


def sonrisa(x, y, a, w):
    return p(f"M{f(x - a)},{f(y)} Q{f(x)},{f(y + a * 0.8)} {f(x + a)},{f(y)}", w, False)


def gato(w):
    o = []
    # cola
    o.append(p("M138,168 C176,172 192,140 176,108 C172,100 162,104 166,112 C178,138 166,158 136,156 Z", w))
    o.append(e(100, 145, 48, 42, w))  # cuerpo
    o.append(e(78, 182, 14, 9, w))
    o.append(e(122, 182, 14, 9, w))
    o.append(p("M58,62 L62,18 L88,44 Z", w))
    o.append(p("M142,62 L138,18 L112,44 Z", w))
    o.append(p("M66,52 L68,32 L80,46", w, False))
    o.append(p("M134,52 L132,32 L120,46", w, False))
    o.append(c(100, 72, 46, w))  # cabeza
    o.append(ojo(82, 66, 9, w))
    o.append(ojo(118, 66, 9, w))
    o.append(p("M94,82 L106,82 L100,89 Z", w))
    o.append(p("M100,89 Q94,97 88,94 M100,89 Q106,97 112,94", w, False))
    for dy in (-4, 4):
        o.append(p(f"M80,{88 + dy} L52,{84 + dy * 2.2}", w * 0.8, False))
        o.append(p(f"M120,{88 + dy} L148,{84 + dy * 2.2}", w * 0.8, False))
    o.append(p("M100,118 L100,150", w * 0.8, False))
    return "".join(o)


def pez(w):
    o = []
    o.append(p("M150,100 L192,68 Q182,100 192,132 Z", w))  # cola
    o.append(p("M85,62 Q100,30 130,52 Z", w))  # aleta superior
    o.append(p("M90,138 Q104,166 124,142 Z", w))
    o.append(e(95, 100, 62, 42, w))
    o.append(p("M60,66 Q76,100 60,134", w, False))  # agalla
    for x in (82, 104, 126):
        for y in (84, 108):
            o.append(p(f"M{x},{y - 8} Q{x + 10},{y} {x},{y + 8}", w * 0.8, False))
    o.append(ojo(48, 90, 9, w))
    o.append(sonrisa(40, 112, 8, w * 0.9))
    for k, (x, y, r) in enumerate(((22, 70, 6), (14, 50, 4.5), (24, 34, 3.5))):
        o.append(c(x, y, r, w * 0.8))
    return "".join(o)


def buho(w):
    o = []
    o.append(p("M30,178 L170,178", w * 1.6, False))  # rama
    o.append(p("M56,40 L44,8 L80,30 Z", w))  # penachos
    o.append(p("M144,40 L156,8 L120,30 Z", w))
    o.append(p("M100,24 C150,24 162,70 160,110 C158,160 132,178 100,178 C68,178 42,160 40,110 C38,70 50,24 100,24Z", w))
    o.append(p("M100,104 C128,104 140,130 136,160 C120,174 80,174 64,160 C60,130 72,104 100,104Z", w))  # panza
    for y in (126, 144):
        for x in (80, 100, 120):
            o.append(p(f"M{x - 7},{y} Q{x},{y + 9} {x + 7},{y}", w * 0.8, False))
    o.append(p("M44,96 Q22,130 52,164 Q60,128 44,96Z", w))  # alas
    o.append(p("M156,96 Q178,130 148,164 Q140,128 156,96Z", w))
    o.append(c(76, 70, 24, w))
    o.append(c(124, 70, 24, w))
    o.append(ojo(76, 70, 12, w))
    o.append(ojo(124, 70, 12, w))
    o.append(p("M92,88 L108,88 L100,104 Z", w))
    for x in (84, 116):
        o.append(p(f"M{x - 8},176 l4,8 M{x},176 l0,9 M{x + 8},176 l-4,8", w * 0.9, False))
    return "".join(o)


def tortuga(w):
    o = []
    o.append(e(42, 150, 14, 18, w, rot=25))  # patas
    o.append(e(158, 150, 14, 18, w, rot=-25))
    o.append(p("M176,128 L196,136 L178,140 Z", w))  # cola
    o.append(c(30, 112, 22, w))  # cabeza
    o.append(ojo(24, 106, 6, w))
    o.append(sonrisa(22, 120, 7, w * 0.9))
    o.append(p("M38,140 C38,70 76,48 104,48 C140,48 176,76 176,140 Z", w))  # caparazon
    o.append(p("M30,140 L184,140 Q186,152 176,152 L38,152 Q28,152 30,140Z", w))
    # hexagonos del caparazon
    def hexa(cx, cy, r):
        pts = " ".join(f"{f(cx + r * math.cos(a))},{f(cy + r * math.sin(a))}"
                       for a in [math.pi / 6 + k * math.pi / 3 for k in range(6)])
        return f'<polygon points="{pts}" {T(w * 0.9)}/>'
    o.append(hexa(106, 96, 22))
    o.append(hexa(66, 118, 15))
    o.append(hexa(146, 118, 15))
    return "".join(o)


def caracol(w):
    o = []
    o.append(p("M20,170 L182,170 Q190,150 170,148 L60,148 Q44,110 30,118 Q16,126 22,150 Z", w))  # cuerpo
    o.append(p("M34,124 L22,86 M42,122 L46,84", w, False))
    o.append(c(22, 84, 6, w))
    o.append(c(46, 82, 6, w))
    o.append(punto(28, 138, 3.5))
    o.append(sonrisa(30, 148, 6, w * 0.9))
    # concha espiral
    pts = []
    cx, cy = 116, 98
    for k in range(0, 720 + 1, 6):
        a = math.radians(k)
        r = 56 * (1 - k / 820)
        pts.append((cx + r * math.cos(a + math.pi), cy + r * math.sin(a + math.pi)))
    o.append(c(cx, cy, 58, w))
    d = "M" + " L".join(f"{f(x)},{f(y)}" for x, y in pts)
    o.append(p(d, w, False))
    return "".join(o)


def pajaro(w):
    o = []
    o.append(p("M30,176 L170,176", w * 1.6, False))
    o.append(p("M150,112 L192,92 L186,124 Z", w))  # cola
    o.append(e(102, 112, 58, 50, w))
    o.append(e(116, 118, 32, 20, w, rot=-15))  # ala
    o.append(p("M96,122 Q116,112 140,110 M100,130 Q118,124 138,122", w * 0.8, False))
    o.append(p("M44,92 L16,102 L44,112 Z", w))  # pico
    o.append(ojo(66, 92, 8, w))
    o.append(p("M90,160 L86,176 M114,160 L118,176", w * 1.2, False))
    o.append(p("M72,36 Q82,46 86,62 Q96,44 110,40", w, False))  # copete
    return "".join(o)


def conejo(w):
    o = []
    o.append(e(76, 44, 14, 40, w, rot=-8))
    o.append(e(124, 44, 14, 40, w, rot=8))
    o.append(e(76, 46, 6, 28, w, rot=-8))
    o.append(e(124, 46, 6, 28, w, rot=8))
    o.append(c(150, 160, 14, w))  # cola
    o.append(e(100, 152, 46, 36, w))
    o.append(e(78, 184, 16, 8, w))
    o.append(e(122, 184, 16, 8, w))
    o.append(c(100, 100, 38, w))
    o.append(ojo(86, 94, 7, w))
    o.append(ojo(114, 94, 7, w))
    o.append(e(100, 110, 6, 4, w))
    o.append(p("M100,114 L100,120 M100,120 Q92,128 86,122 M100,120 Q108,128 114,122", w * 0.9, False))
    o.append(p("M94,121 L94,130 L106,130 L106,121", w * 0.8))
    return "".join(o)


def oso(w):
    o = []
    o.append(c(56, 46, 20, w))
    o.append(c(144, 46, 20, w))
    o.append(c(56, 46, 10, w))
    o.append(c(144, 46, 10, w))
    o.append(e(100, 154, 52, 42, w))
    o.append(e(100, 160, 30, 26, w))
    o.append(e(52, 188, 18, 10, w))
    o.append(e(148, 188, 18, 10, w))
    o.append(c(100, 90, 54, w))
    o.append(e(100, 108, 24, 18, w))
    o.append(e(100, 100, 9, 6, w))
    o.append(punto(100, 100, 0.1))
    o.append(p("M100,106 L100,112 Q92,120 86,114 M100,112 Q108,120 114,114", w * 0.9, False))
    o.append(ojo(80, 80, 7, w))
    o.append(ojo(120, 80, 7, w))
    return "".join(o)


def cerdo(w):
    o = []
    o.append(p("M60,52 L52,16 L88,40 Z", w))
    o.append(p("M140,52 L148,16 L112,40 Z", w))
    o.append(p("M168,150 q14,-8 6,-18 q-8,-6 -10,6", w, False))
    o.append(e(100, 152, 64, 40, w))
    for x in (64, 88, 112, 136):
        o.append(f'<rect x="{x - 9}" y="176" width="18" height="18" rx="4" {B(w)}/>')
    o.append(c(100, 88, 54, w))
    o.append(e(100, 104, 24, 17, w))
    o.append(e(92, 104, 4, 6, w, blanco=False))
    o.append(e(108, 104, 4, 6, w, blanco=False))
    o.append(ojo(78, 76, 7, w))
    o.append(ojo(122, 76, 7, w))
    o.append(sonrisa(100, 126, 10, w * 0.9))
    return "".join(o)


def rana(w):
    o = []
    o.append(e(46, 176, 30, 12, w))
    o.append(e(154, 176, 30, 12, w))
    o.append(p("M30,130 C30,80 60,66 100,66 C140,66 170,80 170,130 C170,170 140,182 100,182 C60,182 30,170 30,130Z", w))
    o.append(e(100, 146, 40, 30, w))
    o.append(c(68, 64, 22, w))
    o.append(c(132, 64, 22, w))
    o.append(ojo(68, 64, 12, w))
    o.append(ojo(132, 64, 12, w))
    o.append(p("M60,108 Q100,136 140,108", w, False))
    o.append(punto(92, 92, 2.5))
    o.append(punto(108, 92, 2.5))
    return "".join(o)


def mariquita(w):
    o = []
    for x, y, dx in ((50, 120, -22), (48, 150, -26), (56, 176, -22), (150, 120, 22), (152, 150, 26), (144, 176, 22)):
        o.append(p(f"M{x + (-dx) * 0.2},{y} L{x + dx},{y + 6}", w, False))
    o.append(c(100, 52, 30, w))  # cabeza
    o.append(p("M88,28 Q80,8 68,10 M112,28 Q120,8 132,10", w, False))
    o.append(c(68, 10, 4, w))
    o.append(c(132, 10, 4, w))
    o.append(ojo(88, 52, 7, w))
    o.append(ojo(112, 52, 7, w))
    o.append(sonrisa(100, 66, 8, w * 0.9))
    o.append(c(100, 136, 62, w))
    o.append(p("M100,74 L100,198", w, False))
    for x, y, r in ((74, 108, 11), (126, 108, 11), (64, 148, 13), (136, 148, 13), (82, 178, 9), (118, 178, 9)):
        o.append(c(x, y, r, w))
    return "".join(o)


def abeja(w):
    o = []
    o.append(e(84, 56, 26, 38, w, rot=-25))  # alas
    o.append(e(120, 56, 26, 38, w, rot=25))
    o.append(p("M176,112 L196,116 L176,122 Z", w))
    o.append(e(112, 116, 66, 44, w))
    for x in (100, 126, 152):
        o.append(p(f"M{x},{74 + (x - 100) * 0.12} Q{x + 12},116 {x},{158 - (x - 100) * 0.12}", w, False))
    o.append(c(52, 110, 34, w))
    o.append(p("M40,80 Q30,52 18,50 M60,78 Q66,50 78,44", w, False))
    o.append(c(18, 50, 5, w))
    o.append(c(78, 44, 5, w))
    o.append(ojo(42, 104, 7, w))
    o.append(ojo(64, 104, 7, w))
    o.append(sonrisa(52, 124, 9, w * 0.9))
    return "".join(o)


def raton(w):
    o = []
    o.append(p("M150,168 C190,170 196,130 172,124", w * 1.2, False))
    o.append(c(60, 52, 30, w))
    o.append(c(140, 52, 30, w))
    o.append(c(60, 52, 18, w))
    o.append(c(140, 52, 18, w))
    o.append(e(100, 150, 50, 38, w))
    o.append(e(80, 186, 14, 7, w))
    o.append(e(120, 186, 14, 7, w))
    o.append(p("M60,86 C60,60 140,60 140,86 C140,108 112,126 100,134 C88,126 60,108 60,86Z", w))
    o.append(c(100, 132, 7, w))
    o.append(ojo(84, 88, 7, w))
    o.append(ojo(116, 88, 7, w))
    for dy in (-3, 5):
        o.append(p(f"M90,{124 + dy} L58,{118 + dy * 2}", w * 0.8, False))
        o.append(p(f"M110,{124 + dy} L142,{118 + dy * 2}", w * 0.8, False))
    return "".join(o)


def pato(w):
    o = []
    o.append(p("M20,170 Q60,160 100,170 T180,170", w, False))
    o.append(p("M40,120 C40,170 160,176 172,120 L190,96 L160,104 C150,90 60,92 40,120Z", w))  # cuerpo
    o.append(p("M80,124 Q110,104 146,118 Q128,150 92,144 Q98,134 80,124Z", w))  # ala
    o.append(c(62, 74, 32, w))
    o.append(p("M34,80 L6,86 Q4,96 18,98 L36,94 Z", w))  # pico
    o.append(p("M8,92 L34,90", w * 0.8, False))
    o.append(ojo(62, 66, 8, w))
    return "".join(o)


def ballena(w):
    o = []
    o.append(p("M92,40 Q80,20 70,24 M100,40 L100,16 M108,40 Q120,20 130,24", w, False))
    o.append(p("M20,110 C20,60 90,48 130,72 C150,84 160,104 172,104 L196,78 L188,116 L196,150 L170,124 C150,150 110,166 70,160 C38,156 20,140 20,110Z", w))
    o.append(p("M24,124 C60,150 110,150 146,128", w, False))
    for x in (54, 76, 98, 120):
        o.append(p(f"M{x},{136 + (x - 54) * 0.05} L{x + 4},{148 - (x - 54) * 0.1}", w * 0.8, False))
    o.append(ojo(54, 100, 8, w))
    return "".join(o)


def mariposa(w):
    o = []
    o.append(e(62, 70, 46, 40, w, rot=-20))
    o.append(e(138, 70, 46, 40, w, rot=20))
    o.append(e(70, 138, 34, 30, w, rot=20))
    o.append(e(130, 138, 34, 30, w, rot=-20))
    o.append(c(58, 66, 16, w))
    o.append(c(142, 66, 16, w))
    o.append(c(70, 140, 12, w))
    o.append(c(130, 140, 12, w))
    o.append(c(84, 44, 6, w))
    o.append(c(116, 44, 6, w))
    o.append(e(100, 112, 12, 58, w))
    o.append(c(100, 50, 15, w))
    o.append(p("M94,38 Q84,12 72,10 M106,38 Q116,12 128,10", w, False))
    o.append(c(72, 10, 4, w))
    o.append(c(128, 10, 4, w))
    o.append(punto(95, 48, 2.5))
    o.append(punto(105, 48, 2.5))
    return "".join(o)


def leon(w):
    o = []
    o.append(p("M150,176 C186,176 190,140 176,130", w * 1.2, False))
    o.append(c(176, 128, 7, w))
    o.append(e(100, 158, 52, 34, w))
    o.append(e(74, 188, 15, 8, w))
    o.append(e(126, 188, 15, 8, w))
    n = 14
    for k in range(n):
        a = k * 2 * math.pi / n
        x, y = 100 + 58 * math.cos(a), 84 + 58 * math.sin(a)
        o.append(c(x, y, 20, w))
    o.append(c(64, 48, 11, w))
    o.append(c(136, 48, 11, w))
    o.append(c(100, 86, 46, w))
    o.append(ojo(84, 78, 7, w))
    o.append(ojo(116, 78, 7, w))
    o.append(p("M92,96 L108,96 L100,104 Z", w))
    o.append(p("M100,104 L100,110 Q92,118 86,112 M100,110 Q108,118 114,112", w * 0.9, False))
    return "".join(o)


def perro(w):
    o = []
    o.append(p("M150,150 Q178,140 176,112", w * 2, False))
    o.append(e(100, 154, 50, 38, w))
    o.append(e(78, 186, 14, 8, w))
    o.append(e(122, 186, 14, 8, w))
    o.append(c(100, 82, 48, w))
    o.append(p("M58,58 C40,62 34,106 48,120 C60,120 66,90 64,64Z", w))  # orejas caidas
    o.append(p("M142,58 C160,62 166,106 152,120 C140,120 134,90 136,64Z", w))
    o.append(e(118, 72, 13, 15, w))  # mancha
    o.append(ojo(84, 74, 7, w))
    o.append(ojo(116, 74, 7, w))
    o.append(e(100, 102, 22, 16, w))
    o.append(e(100, 94, 9, 6, w, blanco=False))
    o.append(f'<ellipse cx="100" cy="94" rx="9" ry="6" fill="#000"/>')
    o.append(p("M100,100 L100,106 Q92,114 86,108 M100,106 Q108,114 114,108", w * 0.9, False))
    o.append(p("M94,110 Q100,124 106,110", w * 0.9))
    return "".join(o)


def elefante(w):
    o = []
    o.append(p("M172,112 Q190,124 186,146", w, False))
    for x in (78, 104, 138, 162):
        o.append(f'<rect x="{x - 12}" y="146" width="24" height="44" rx="7" {B(w)}/>')
    o.append(e(120, 122, 62, 44, w))
    o.append(p("M40,100 C30,130 34,158 18,170 C10,174 4,164 12,158 C22,148 18,124 26,106Z", w))  # trompa
    o.append(c(56, 84, 36, w))
    o.append(p("M70,50 C118,36 130,112 80,118 C72,100 68,72 70,50Z", w))  # oreja
    o.append(p("M80,64 C104,60 110,98 84,104", w * 0.8, False))
    o.append(ojo(46, 78, 7, w))
    o.append(p("M38,108 Q46,118 58,112", w * 0.9, False))
    return "".join(o)


ANIMALES = {
    # clave: (funcion, nombre_es, nombre_en, articulo_es, sonido_es, sonido_en)
    "gato": (gato, "gato", "cat", "el", "miau", "meow"),
    "perro": (perro, "perro", "dog", "el", "guau", "woof"),
    "pez": (pez, "pez", "fish", "el", "glu glu", "blub"),
    "buho": (buho, "búho", "owl", "el", "uh uh", "hoot"),
    "tortuga": (tortuga, "tortuga", "turtle", "la", "", ""),
    "caracol": (caracol, "caracol", "snail", "el", "", ""),
    "pajaro": (pajaro, "pájaro", "bird", "el", "pío pío", "tweet"),
    "conejo": (conejo, "conejo", "rabbit", "el", "", ""),
    "oso": (oso, "oso", "bear", "el", "grrr", "grrr"),
    "cerdo": (cerdo, "cerdo", "pig", "el", "oink", "oink"),
    "rana": (rana, "rana", "frog", "la", "croac", "ribbit"),
    "mariquita": (mariquita, "mariquita", "ladybug", "la", "", ""),
    "abeja": (abeja, "abeja", "bee", "la", "bzzz", "buzz"),
    "raton": (raton, "ratón", "mouse", "el", "iii", "squeak"),
    "pato": (pato, "pato", "duck", "el", "cuac", "quack"),
    "ballena": (ballena, "ballena", "whale", "la", "", ""),
    "mariposa": (mariposa, "mariposa", "butterfly", "la", "", ""),
    "leon": (leon, "león", "lion", "el", "grrr", "roar"),
    "elefante": (elefante, "elefante", "elephant", "el", "", ""),
}


def dibujar(clave, x, y, tam, trazo=2.6):
    """Ubica el animal en (x, y) = esquina sup. izq., tam = lado de la caja."""
    fn = ANIMALES[clave][0]
    s = tam / 200
    return f'<g transform="translate({f(x)},{f(y)}) scale({s:.4f})">{fn(trazo / s)}</g>'
