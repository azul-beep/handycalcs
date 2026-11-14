#!/usr/bin/env python3
"""
regenerar.py - Arma el pack de calendarios imprimibles gratis para un año.

Uso:
    python3 regenerar.py 2027
    python3 regenerar.py 2028 --url https://tu-sitio.com/calendarios-2028/ --pie "tu-sitio.com"

Genera (en ./sitio/calendarios-AAAA/ al lado de este archivo, o en --salida):
    pdf/es/... y pdf/en/...   PDFs en Carta (Letter) y A4, 3 estilos, ES y EN
    img/pins/*.png             previews 1000x1500 para Pinterest
    img/mini/*.webp            miniaturas livianas para la página
    index.html                 página en español
    free-printable-AAAA-calendars.html   página en inglés
    rss.xml                    feed para auto-pinear en Pinterest
    estilos.css
    calendarios-AAAA-pack-es.zip / calendars-AAAA-pack-en.zip

Requisitos: pip install reportlab pillow pypdfium2
(si no está pypdfium2, usa el comando pdftoppm de poppler).
"""
import argparse
import calendar
import datetime as dt
import html
import os
import random
import shutil
import subprocess
import sys
import tempfile
import zipfile
from email.utils import format_datetime
from pathlib import Path

from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.utils import simpleSplit
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from PIL import Image, ImageDraw, ImageFilter, ImageFont

AQUI = Path(__file__).resolve().parent
FONTS = AQUI / "fonts"

# ----------------------------------------------------------------- fuentes
FONT_FILES = {
    "Sans": "Carlito-Regular.ttf",
    "Sans-Bold": "Carlito-Bold.ttf",
    "Serif": "Caladea-Regular.ttf",
    "Serif-Bold": "Caladea-Bold.ttf",
}
FALLBACK = {"Sans": "Helvetica", "Sans-Bold": "Helvetica-Bold",
            "Serif": "Times-Roman", "Serif-Bold": "Times-Bold"}
F = {}


def registrar_fuentes():
    for nombre, archivo in FONT_FILES.items():
        p = FONTS / archivo
        if p.exists():
            pdfmetrics.registerFont(TTFont(nombre, str(p)))
            F[nombre] = nombre
        else:
            F[nombre] = FALLBACK[nombre]


def pil_font(nombre, size):
    p = FONTS / FONT_FILES[nombre]
    if p.exists():
        return ImageFont.truetype(str(p), size)
    for alt in ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if "Bold" in nombre
                else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",):
        if os.path.exists(alt):
            return ImageFont.truetype(alt, size)
    return ImageFont.load_default(size=size)


# ----------------------------------------------------------------- textos
MESES = {
    "es": ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio",
           "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"],
    "en": ["January", "February", "March", "April", "May", "June", "July",
           "August", "September", "October", "November", "December"],
}
# dias en orden lunes..domingo (como datetime.weekday())
DIAS = {
    "es": ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"],
    "en": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
}
DIAS_CORTOS = {
    "es": ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"],
    "en": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
}
DIAS_INICIAL = {
    "es": ["L", "M", "M", "J", "V", "S", "D"],
    "en": ["M", "T", "W", "T", "F", "S", "S"],
}
# primer dia de la semana: ES lunes, EN domingo
PRIMER_DIA = {"es": calendar.MONDAY, "en": calendar.SUNDAY}

T = {
    "es": {
        "anual": "Calendario anual", "notas": "Notas", "mes": "Mes", "anio": "Año",
        "semanal": "Planificador semanal", "semana_del": "Semana del",
        "prioridades": "Prioridades", "pendientes": "Pendientes",
        "feriados": "Fechas marcadas",
        "pie": "Gratis para uso personal",
    },
    "en": {
        "anual": "Yearly Calendar", "notas": "Notes", "mes": "Month", "anio": "Year",
        "semanal": "Weekly Planner", "semana_del": "Week of",
        "prioridades": "Top priorities", "pendientes": "To do",
        "feriados": "US federal holidays",
        "pie": "Free for personal use",
    },
}

# ----------------------------------------------------------------- estilos
ESTILOS = {
    "minimal": {
        "slug": {"es": "minimal", "en": "minimal"},
        "nombre": {"es": "Minimal negro", "en": "Minimal Black"},
        "tinta": "#141414", "acento": "#141414", "linea": "#8c8c8c",
        "relleno": "#f1f1f1", "renglon": "#d6d6d6", "titulo": "Sans-Bold", "texto": "Sans",
        "pin_fondo": "#f3f2ef", "pin_texto": "#141414", "montanas": False,
    },
    "lino": {
        "slug": {"es": "lino-salvia", "en": "linen-sage"},
        "nombre": {"es": "Lino y salvia", "en": "Linen & Sage"},
        "tinta": "#4a443d", "acento": "#7f9171", "linea": "#c8baa6",
        "relleno": "#f2ece1", "renglon": "#ddd2c0", "titulo": "Serif", "texto": "Sans",
        "pin_fondo": "#ece4d6", "pin_texto": "#56634c", "montanas": False,
    },
    "montana": {
        "slug": {"es": "montana", "en": "mountain"},
        "nombre": {"es": "Montaña", "en": "Mountain"},
        "tinta": "#2e3a46", "acento": "#557086", "linea": "#a7b3bd",
        "relleno": "#edf1f4", "renglon": "#d3dbe1", "titulo": "Sans-Bold", "texto": "Sans",
        "pin_fondo": "#e3e9ee", "pin_texto": "#2e3a46", "montanas": True,
    },
}

TIPOS = ["anual", "mensual", "blanco", "semanal"]
TAMANOS = {"carta": letter, "a4": A4}
TAM_NOMBRE = {"es": {"carta": "carta", "a4": "a4"}, "en": {"carta": "letter", "a4": "a4"}}
TAM_LABEL = {"es": {"carta": "Carta", "a4": "A4"}, "en": {"carta": "Letter", "a4": "A4"}}
TAM_PRINCIPAL = {"es": "a4", "en": "carta"}  # el que se usa para el preview


# ----------------------------------------------------------------- feriados
def _nth(year, month, weekday, n):
    """n-esimo weekday del mes (n=-1 => ultimo)."""
    dias = [d for d in range(1, calendar.monthrange(year, month)[1] + 1)
            if dt.date(year, month, d).weekday() == weekday]
    return dt.date(year, month, dias[n - 1] if n > 0 else dias[n])


def _observado(d):
    if d.weekday() == 5:
        return d - dt.timedelta(days=1)
    if d.weekday() == 6:
        return d + dt.timedelta(days=1)
    return d


def feriados_us(year):
    """Feriados federales de EE.UU. (5 U.S.C. 6103), con el dia 'observed' si cae finde."""
    fijos = [
        (dt.date(year, 1, 1), "New Year's Day"),
        (_nth(year, 1, 0, 3), "Martin Luther King Jr. Day"),
        (_nth(year, 2, 0, 3), "Washington's Birthday (Presidents' Day)"),
        (_nth(year, 5, 0, -1), "Memorial Day"),
        (dt.date(year, 6, 19), "Juneteenth"),
        (dt.date(year, 7, 4), "Independence Day"),
        (_nth(year, 9, 0, 1), "Labor Day"),
        (_nth(year, 10, 0, 2), "Columbus Day"),
        (dt.date(year, 11, 11), "Veterans Day"),
        (_nth(year, 11, 3, 4), "Thanksgiving Day"),
        (dt.date(year, 12, 25), "Christmas Day"),
    ]
    out = {}
    for d, n in fijos:
        out.setdefault(d, []).append(n)
        o = _observado(d)
        if o != d and o.year == year:
            out.setdefault(o, []).append(n + " (observed)")
    # Año Nuevo del año siguiente cae sabado -> se observa el 31/12 de este año
    sig = dt.date(year + 1, 1, 1)
    o = _observado(sig)
    if o.year == year:
        out.setdefault(o, []).append("New Year's Day (observed)")
    return dict(sorted(out.items()))


def feriados_es(year):
    return {dt.date(year, 1, 1): ["Año Nuevo"], dt.date(year, 12, 25): ["Navidad"]}


def feriados(lang, year):
    return feriados_us(year) if lang == "en" else feriados_es(year)


def corto(nombre):
    return (nombre.replace("Washington's Birthday (Presidents' Day)", "Presidents' Day")
                  .replace("Martin Luther King Jr. Day", "MLK Jr. Day"))


# ----------------------------------------------------------------- dibujo
def montanas(c, x, y, w, h, est, seed=7):
    """Linea de montañas vectorial: cordillera de fondo (relleno suave) + frente (trazo)."""
    rnd = random.Random(seed)
    acento, linea, relleno = HexColor(est["acento"]), HexColor(est["linea"]), HexColor(est["relleno"])

    def cordillera(n, alto_min, alto_max, desf):
        pts = [(x, y + h * 0.15)]
        paso = w / n
        for i in range(n):
            px = x + paso * (i + 0.5) + rnd.uniform(-paso * 0.2, paso * 0.2) + desf
            px = min(max(px, x), x + w)
            pts.append((px, y + h * rnd.uniform(alto_min, alto_max)))
            vx = min(x + paso * (i + 1) + rnd.uniform(-paso * .1, paso * .1), x + w)
            pts.append((vx, y + h * rnd.uniform(0.12, 0.35)))
        pts[-1] = (x + w, y + h * 0.15)
        return pts

    paso_desf = w / 30
    atras = cordillera(7, 0.55, 0.85, paso_desf)
    p = c.beginPath()
    p.moveTo(x, y)
    for px, py in atras:
        p.lineTo(px, py)
    p.lineTo(x + w, y)
    p.close()
    c.setFillColor(relleno)
    c.setStrokeColor(linea)
    c.setLineWidth(0.8)
    c.setLineJoin(1)
    c.drawPath(p, fill=1, stroke=1)
    frente = cordillera(5, 0.45, 1.0, -paso_desf)
    p = c.beginPath()
    p.moveTo(*frente[0])
    for px, py in frente[1:]:
        p.lineTo(px, py)
    c.setStrokeColor(acento)
    c.setLineWidth(1.6)
    c.setLineCap(1)
    c.drawPath(p, fill=0, stroke=1)
    # sol
    c.setLineWidth(1)
    c.circle(x + w * 0.83, y + h * 0.82, h * 0.13, stroke=1, fill=0)
    # base
    c.setStrokeColor(linea)
    c.setLineWidth(0.6)
    c.line(x, y, x + w, y)


class Pagina:
    def __init__(self, c, size, est, lang, year, pie):
        self.c, self.est, self.lang, self.year = c, est, lang, year
        self.W, self.H = size
        self.M = 36
        self.pie = pie
        self.tinta = HexColor(est["tinta"])
        self.acento = HexColor(est["acento"])
        self.linea = HexColor(est["linea"])
        self.relleno = HexColor(est["relleno"])

    def encabezado(self, izq, der=None, sub=None):
        """Dibuja el encabezado y devuelve la coordenada y donde termina."""
        c, M, W, H = self.c, self.M, self.W, self.H
        top = H - M
        if self.est["montanas"]:
            montanas(c, M, top - 62, W - 2 * M, 62, self.est, seed=self.year + len(izq))
            top -= 74
        c.setFillColor(self.acento if self.est["titulo"].startswith("Serif") else self.tinta)
        fs = 34
        c.setFont(F[self.est["titulo"]], fs)
        c.drawString(M, top - fs * 0.8, izq)
        if der:
            c.setFillColor(self.acento)
            c.setFont(F[self.est["titulo"]], fs)
            c.drawRightString(W - M, top - fs * 0.8, der)
        y = top - fs - 4
        if sub:
            c.setFillColor(self.tinta)
            c.setFont(F["Sans"], 10)
            c.drawString(M, y - 6, sub.upper())
            y -= 16
        if not self.est["montanas"]:
            c.setStrokeColor(self.acento)
            c.setLineWidth(1.2 if self.est["titulo"].startswith("Serif") else 2)
            c.line(M, y - 4, W - M, y - 4)
        return y - 14

    def pie_pagina(self):
        c = self.c
        c.setFillColor(self.linea)
        c.setFont(F["Sans"], 7.5)
        c.drawCentredString(self.W / 2, self.M * 0.55, self.pie)

    def caja_notas(self, y0, y1, titulo):
        c, M, W = self.c, self.M, self.W
        c.setStrokeColor(self.linea)
        c.setLineWidth(0.6)
        c.roundRect(M, y0, W - 2 * M, y1 - y0, 4, stroke=1, fill=0)
        c.setFillColor(self.acento)
        c.setFont(F["Sans-Bold"], 9)
        c.drawString(M + 8, y1 - 14, titulo.upper())
        c.setStrokeColor(HexColor(self.est["renglon"]))
        yy = y1 - 30
        while yy > y0 + 8:
            c.line(M + 8, yy, W - M - 8, yy)
            yy -= 18


def orden_dias(lang):
    p = PRIMER_DIA[lang]
    return [(p + i) % 7 for i in range(7)]


def grilla_mes(pg, y_top, y_bot, year=None, month=None, fer=None):
    """Grilla mensual. Si year es None => grilla en blanco (6 filas)."""
    c, M, W, lang = pg.c, pg.M, pg.W, pg.lang
    ancho = (W - 2 * M) / 7
    # cabecera de dias
    hcab = 18
    c.setFillColor(pg.relleno)
    c.rect(M, y_top - hcab, W - 2 * M, hcab, stroke=0, fill=1)
    c.setFillColor(pg.tinta)
    c.setFont(F["Sans-Bold"], 9)
    for i, wd in enumerate(orden_dias(lang)):
        c.drawCentredString(M + ancho * (i + 0.5), y_top - hcab + 5.5, DIAS[lang][wd].upper())
    if year is None:
        semanas = [[0] * 7 for _ in range(6)]
    else:
        semanas = calendar.Calendar(PRIMER_DIA[lang]).monthdayscalendar(year, month)
    filas = len(semanas)
    alto = (y_top - hcab - y_bot) / filas
    c.setStrokeColor(pg.linea)
    c.setLineWidth(0.6)
    for r, sem in enumerate(semanas):
        for i, d in enumerate(sem):
            x = M + ancho * i
            y = y_top - hcab - alto * (r + 1)
            wd = orden_dias(lang)[i]
            if d == 0 and year is not None:
                c.setFillColor(HexColor("#fafafa") if pg.est["tinta"] == "#141414" else pg.relleno)
                c.setFillAlpha(0.5)
                c.rect(x, y, ancho, alto, stroke=0, fill=1)
                c.setFillAlpha(1)
            c.rect(x, y, ancho, alto, stroke=1, fill=0)
            if d:
                fecha = dt.date(year, month, d)
                nombres = (fer or {}).get(fecha)
                if nombres:
                    c.setFillColor(pg.acento)
                    c.circle(x + 13, y + alto - 13, 9.5, stroke=0, fill=1)
                    c.setFillColor(white)
                else:
                    c.setFillColor(pg.acento if wd >= 5 and pg.est["acento"] != pg.est["tinta"] else pg.tinta)
                c.setFont(F["Sans-Bold"], 11)
                c.drawCentredString(x + 13, y + alto - 16.5, str(d))
                if nombres:
                    c.setFillColor(pg.acento)
                    c.setFont(F["Sans"], 6.4)
                    yy = y + 5
                    lineas = []
                    for n in nombres:
                        lineas += simpleSplit(corto(n), F["Sans"], 6.4, ancho - 6)
                    for ln in reversed(lineas[:3]):
                        c.drawString(x + 3, yy, ln)
                        yy += 7.5
    c.setLineWidth(1)
    c.rect(M, y_bot, W - 2 * M, y_top - y_bot, stroke=1, fill=0)


def pagina_mensual(c, size, est, lang, year, month, pie):
    pg = Pagina(c, size, est, lang, year, pie)
    y = pg.encabezado(MESES[lang][month - 1], str(year))
    notas_alto = 105
    grilla_mes(pg, y, pg.M + notas_alto + 14, year, month, feriados(lang, year))
    pg.caja_notas(pg.M + 4, pg.M + notas_alto, T[lang]["notas"])
    pg.pie_pagina()
    c.showPage()


def pagina_blanco(c, size, est, lang, year, pie):
    pg = Pagina(c, size, est, lang, year, pie)
    t = T[lang]
    y = pg.encabezado(f"{t['mes']}:", None)
    # lineas para completar mes y año
    c.setStrokeColor(pg.linea)
    c.setLineWidth(0.8)
    base = y + 24
    c.line(pg.M + 92, base, pg.W - pg.M - 140, base)
    c.setFillColor(pg.tinta)
    c.setFont(F["Sans-Bold"], 12)
    c.drawString(pg.W - pg.M - 128, base + 2, f"{t['anio']}:")
    c.line(pg.W - pg.M - 90, base, pg.W - pg.M, base)
    notas_alto = 105
    grilla_mes(pg, y, pg.M + notas_alto + 14)
    pg.caja_notas(pg.M + 4, pg.M + notas_alto, t["notas"])
    pg.pie_pagina()
    c.showPage()


def pagina_anual(c, size, est, lang, year, pie):
    pg = Pagina(c, size, est, lang, year, pie)
    fer = feriados(lang, year)
    y = pg.encabezado(str(year), None, T[lang]["anual"])
    M, W = pg.M, pg.W
    leyenda_alto = 92 if lang == "en" else 40
    y_bot = M + leyenda_alto + 6
    cols, filas, gap = 3, 4, 18
    cw = (W - 2 * M - gap * (cols - 1)) / cols
    ch = (y - y_bot) / filas
    cel = cw / 7
    for m in range(12):
        col, fila = m % cols, m // cols
        x0 = M + col * (cw + gap)
        y0 = y - fila * ch
        c.setFillColor(pg.acento)
        c.setFont(F[est["titulo"]], 13)
        c.drawString(x0 + 2, y0 - 15, MESES[lang][m])
        c.setStrokeColor(pg.linea)
        c.setLineWidth(0.5)
        c.line(x0, y0 - 20, x0 + cw, y0 - 20)
        c.setFont(F["Sans-Bold"], 7.5)
        c.setFillColor(pg.tinta)
        for i, wd in enumerate(orden_dias(lang)):
            c.drawCentredString(x0 + cel * (i + 0.5), y0 - 31, DIAS_INICIAL[lang][wd])
        rh = (ch - 44) / 6
        for r, sem in enumerate(calendar.Calendar(PRIMER_DIA[lang]).monthdayscalendar(year, m + 1)):
            for i, d in enumerate(sem):
                if not d:
                    continue
                cx = x0 + cel * (i + 0.5)
                cy = y0 - 33 - rh * (r + 1) + rh * 0.3
                if dt.date(year, m + 1, d) in fer:
                    c.setFillColor(pg.acento)
                    c.circle(cx, cy + 2.6, min(rh, cel) * 0.46, stroke=0, fill=1)
                    c.setFillColor(white)
                    c.setFont(F["Sans-Bold"], 8)
                else:
                    wd = orden_dias(lang)[i]
                    c.setFillColor(pg.acento if wd >= 5 and est["acento"] != est["tinta"] else pg.tinta)
                    c.setFont(F["Sans"], 8)
                c.drawCentredString(cx, cy, str(d))
    # leyenda
    c.setStrokeColor(pg.linea)
    c.setLineWidth(0.5)
    c.line(M, M + leyenda_alto, W - M, M + leyenda_alto)
    c.setFillColor(pg.acento)
    c.setFont(F["Sans-Bold"], 8)
    c.drawString(M, M + leyenda_alto - 12, T[lang]["feriados"].upper())
    items = []
    for d, ns in fer.items():
        for n in ns:
            if lang == "en":
                items.append(f"{MESES['en'][d.month - 1][:3]} {d.day}  {corto(n)}")
            else:
                items.append(f"{d.day} de {MESES['es'][d.month - 1].lower()}  {n}")
    ncol = 3
    porcol = -(-len(items) // ncol)
    c.setFont(F["Sans"], 7.5)
    c.setFillColor(pg.tinta)
    for k, it in enumerate(items):
        cx = M + (k // porcol) * (W - 2 * M) / ncol
        cy = M + leyenda_alto - 25 - (k % porcol) * 10.5
        c.drawString(cx, cy, it)
    pg.pie_pagina()
    c.showPage()


def pagina_semanal(c, size, est, lang, year, pie):
    pg = Pagina(c, size, est, lang, year, pie)
    t = T[lang]
    M, W = pg.M, pg.W
    y = pg.encabezado(t["semanal"], None)
    # "Semana del ____"
    c.setFillColor(pg.tinta)
    c.setFont(F["Sans-Bold"], 10)
    c.drawString(M, y - 6, f"{t['semana_del']}:")
    c.setStrokeColor(pg.linea)
    c.setLineWidth(0.8)
    c.line(M + 70, y - 8, M + 260, y - 8)
    y -= 22
    y_bot = M + 6
    izq_w = (W - 2 * M) * 0.60
    der_x = M + izq_w + 16
    der_w = W - M - der_x
    # dias
    h = (y - y_bot) / 7
    for i, wd in enumerate(orden_dias(lang)):
        yy = y - h * (i + 1)
        c.setStrokeColor(pg.linea)
        c.setLineWidth(0.6)
        c.roundRect(M, yy + 3, izq_w, h - 6, 4, stroke=1, fill=0)
        c.setFillColor(pg.relleno)
        c.roundRect(M, yy + h - 21, izq_w, 18, 4, stroke=0, fill=1)
        c.setFillColor(pg.acento)
        c.setFont(F["Sans-Bold"], 9)
        c.drawString(M + 8, yy + h - 15.5, DIAS[lang][wd].upper())
        c.setStrokeColor(HexColor(est["renglon"]))
        ly = yy + h - 38
        while ly > yy + 10:
            c.line(M + 8, ly, M + izq_w - 8, ly)
            ly -= 16
    # columna derecha
    bloques = [(t["prioridades"], 0.22, "num"), (t["pendientes"], 0.46, "check"), (t["notas"], 0.32, "lin")]
    yy = y
    total = y - y_bot
    for titulo, frac, tipo in bloques:
        bh = total * frac
        c.setStrokeColor(pg.linea)
        c.setLineWidth(0.6)
        c.roundRect(der_x, yy - bh + 3, der_w, bh - 6, 4, stroke=1, fill=0)
        c.setFillColor(pg.acento)
        c.setFont(F["Sans-Bold"], 9)
        c.drawString(der_x + 8, yy - 17, titulo.upper())
        ly = yy - 38
        n = 1
        while ly > yy - bh + 12:
            c.setStrokeColor(HexColor(est["renglon"]))
            x_ini = der_x + 8
            if tipo == "num":
                c.setFillColor(pg.tinta)
                c.setFont(F["Sans-Bold"], 9)
                c.drawString(der_x + 8, ly + 3, f"{n}.")
                x_ini += 14
                n += 1
            elif tipo == "check":
                c.setStrokeColor(pg.linea)
                c.rect(der_x + 8, ly + 1.5, 8, 8, stroke=1, fill=0)
                c.setStrokeColor(HexColor(est["renglon"]))
                x_ini += 14
            c.line(x_ini, ly, der_x + der_w - 8, ly)
            ly -= 18
        yy -= bh
    pg.pie_pagina()
    c.showPage()


# ----------------------------------------------------------------- nombres de archivo
def nombre_pdf(lang, est_key, tipo, tam, year, mes=None):
    s = ESTILOS[est_key]["slug"][lang]
    tn = TAM_NOMBRE[lang][tam]
    if lang == "es":
        base = {
            "anual": f"calendario-{year}-anual-{s}-{tn}",
            "mensual": f"calendario-{year}-mensual-{s}-{tn}",
            "blanco": f"calendario-mensual-en-blanco-{s}-{tn}",
            "semanal": f"planificador-semanal-{s}-{tn}",
        }.get(tipo)
        if mes:
            base = f"calendario-{MESES['es'][mes - 1].lower()}-{year}-{s}-{tn}"
    else:
        base = {
            "anual": f"{year}-yearly-calendar-{s}-{tn}",
            "mensual": f"{year}-monthly-calendar-{s}-{tn}",
            "blanco": f"blank-monthly-calendar-{s}-{tn}",
            "semanal": f"weekly-planner-{s}-{tn}",
        }.get(tipo)
        if mes:
            base = f"{MESES['en'][mes - 1].lower()}-{year}-calendar-{s}-{tn}"
    return base + ".pdf"


def ruta_pdf(lang, est_key, tipo, tam, year, mes=None):
    sub = "meses" if mes else ""
    p = Path("pdf") / lang / ESTILOS[est_key]["slug"][lang]
    if sub:
        p = p / sub
    return p / nombre_pdf(lang, est_key, tipo, tam, year, mes)


def nuevo_canvas(path, size, titulo, lang):
    path.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(path), pagesize=size, pageCompression=1)
    c.setTitle(titulo)
    c.setAuthor("Skye Solutions AI")
    c.setSubject(titulo)
    c.setCreator("regenerar.py")
    return c


def generar_pdfs(out, year, pie_txt):
    hechos = []
    for lang in ("es", "en"):
        pie = f"{T[lang]['pie']}" + (f"  ·  {pie_txt}" if pie_txt else "")
        for ek, est in ESTILOS.items():
            nom = est["nombre"][lang]
            for tam, size in TAMANOS.items():
                # anual
                p = out / ruta_pdf(lang, ek, "anual", tam, year)
                c = nuevo_canvas(p, size, f"{T[lang]['anual']} {year} - {nom}", lang)
                pagina_anual(c, size, est, lang, year, pie)
                c.save(); hechos.append(p)
                # 12 meses
                p = out / ruta_pdf(lang, ek, "mensual", tam, year)
                tit = ("Calendario mensual" if lang == "es" else "Monthly Calendar") + f" {year} - {nom}"
                c = nuevo_canvas(p, size, tit, lang)
                for m in range(1, 13):
                    pagina_mensual(c, size, est, lang, year, m, pie)
                c.save(); hechos.append(p)
                # meses sueltos
                for m in range(1, 13):
                    p = out / ruta_pdf(lang, ek, "mensual", tam, year, m)
                    c = nuevo_canvas(p, size, f"{MESES[lang][m - 1]} {year} - {nom}", lang)
                    pagina_mensual(c, size, est, lang, year, m, pie)
                    c.save(); hechos.append(p)
                # en blanco
                p = out / ruta_pdf(lang, ek, "blanco", tam, year)
                tit = ("Calendario mensual en blanco" if lang == "es" else "Blank Monthly Calendar") + f" - {nom}"
                c = nuevo_canvas(p, size, tit, lang)
                pagina_blanco(c, size, est, lang, year, pie)
                c.save(); hechos.append(p)
                # semanal
                p = out / ruta_pdf(lang, ek, "semanal", tam, year)
                c = nuevo_canvas(p, size, f"{T[lang]['semanal']} - {nom}", lang)
                pagina_semanal(c, size, est, lang, year, pie)
                c.save(); hechos.append(p)
    return hechos


# ----------------------------------------------------------------- render a PNG
def render_pagina(pdf_path, ancho_px, pagina=0):
    try:
        import pypdfium2 as pdfium
        doc = pdfium.PdfDocument(str(pdf_path))
        pg = doc[pagina]
        escala = ancho_px / pg.get_width()
        img = pg.render(scale=escala).to_pil().convert("RGB")
        doc.close()
        return img
    except ImportError:
        with tempfile.TemporaryDirectory() as td:
            pref = Path(td) / "p"
            subprocess.run(["pdftoppm", "-png", "-r", "150", "-f", str(pagina + 1), "-l", str(pagina + 1),
                            "-singlefile", str(pdf_path), str(pref)], check=True)
            img = Image.open(str(pref) + ".png").convert("RGB")
            return img.resize((ancho_px, round(img.height * ancho_px / img.width)), Image.LANCZOS)


TITULO_PIN = {
    "es": {"anual": "Calendario anual {y}", "mensual": "Calendario mensual {y}",
           "blanco": "Calendario mensual en blanco", "semanal": "Planificador semanal"},
    "en": {"anual": "{y} Yearly Calendar", "mensual": "{y} Monthly Calendar",
           "blanco": "Blank Monthly Calendar", "semanal": "Weekly Planner"},
}
KICKER = {"es": "IMPRIMIBLE GRATIS", "en": "FREE PRINTABLE"}
PIE_PIN = {"es": "PDF gratis · Carta y A4", "en": "Free PDF · Letter & A4"}
DETALLE = {
    "es": {"anual": "12 meses en una hoja", "mensual": "12 páginas · semana desde el lunes",
           "blanco": "Sin fecha: usalo cualquier mes", "semanal": "Prioridades, pendientes y notas"},
    "en": {"anual": "All 12 months on one page", "mensual": "12 pages · US holidays marked",
           "blanco": "Undated: use it any month", "semanal": "Priorities, to-do list and notes"},
}


def _centrado(d, y, txt, font, fill, W):
    w = d.textlength(txt, font=font)
    d.text(((W - w) / 2, y), txt, font=font, fill=fill)


def hacer_pin(pdf_path, destino, lang, ek, tipo, year, pie_txt):
    est = ESTILOS[ek]
    W, H = 1000, 1500
    img = Image.new("RGB", (W, H), est["pin_fondo"])
    d = ImageDraw.Draw(img)
    col = est["pin_texto"]
    # kicker
    k = KICKER[lang]
    fk = pil_font("Sans-Bold", 30)
    kw = sum(d.textlength(ch, font=fk) for ch in k) + 6 * (len(k) - 1)
    x = (W - kw) / 2
    for ch in k:
        d.text((x, 58), ch, font=fk, fill=est["acento"])
        x += d.textlength(ch, font=fk) + 6
    # titulo
    titulo = TITULO_PIN[lang][tipo].format(y=year)
    tf = "Serif-Bold" if est["titulo"].startswith("Serif") else "Sans-Bold"
    size = 92
    while True:
        ft = pil_font(tf, size)
        if d.textlength(titulo, font=ft) <= W - 110 or size < 50:
            break
        size -= 4
    _centrado(d, 102, titulo, ft, col, W)
    fs = pil_font("Sans", 34)
    _centrado(d, 112 + size + 8, f"{est['nombre'][lang]}  ·  {DETALLE[lang][tipo]}", fs, est["tinta"], W)
    # pagina con sombra
    pagina = render_pagina(pdf_path, 790)
    max_h = 1075
    if pagina.height > max_h:
        pagina = pagina.resize((round(pagina.width * max_h / pagina.height), max_h), Image.LANCZOS)
    px = (W - pagina.width) // 2
    py = 290
    sombra = Image.new("L", (W, H), 0)
    ImageDraw.Draw(sombra).rectangle([px + 10, py + 16, px + pagina.width + 10, py + pagina.height + 16], fill=110)
    sombra = sombra.filter(ImageFilter.GaussianBlur(18))
    img.paste(Image.new("RGB", (W, H), "#000000"), (0, 0), sombra.point(lambda v: v * 0.55))
    img.paste(pagina, (px, py))
    # pie
    yb = py + pagina.height + 40
    fp = pil_font("Sans-Bold", 40)
    _centrado(d, yb, PIE_PIN[lang], fp, col, W)
    if pie_txt:
        _centrado(d, yb + 56, pie_txt, pil_font("Sans", 30), est["tinta"], W)
    destino.parent.mkdir(parents=True, exist_ok=True)
    img.save(destino, optimize=True)
    mini = img.resize((400, 600), Image.LANCZOS)
    mpath = destino.parent.parent / "mini" / (destino.stem + ".webp")
    mpath.parent.mkdir(parents=True, exist_ok=True)
    mini.save(mpath, quality=82)
    return destino, mpath


def nombre_pin(lang, ek, tipo, year):
    s = ESTILOS[ek]["slug"][lang]
    t = {"es": {"anual": f"calendario-{year}-anual", "mensual": f"calendario-{year}-mensual",
                "blanco": "calendario-mensual-en-blanco", "semanal": "planificador-semanal"},
         "en": {"anual": f"{year}-yearly-calendar", "mensual": f"{year}-monthly-calendar",
                "blanco": "blank-monthly-calendar", "semanal": "weekly-planner"}}[lang][tipo]
    return f"{lang}-{t}-{s}.png"


def generar_pins(out, year, pie_txt):
    pins = {}
    for lang in ("es", "en"):
        for ek in ESTILOS:
            for tipo in TIPOS:
                pdf = out / ruta_pdf(lang, ek, tipo, TAM_PRINCIPAL[lang], year)
                dest = out / "img" / "pins" / nombre_pin(lang, ek, tipo, year)
                pins[(lang, ek, tipo)] = hacer_pin(pdf, dest, lang, ek, tipo, year, pie_txt)
    return pins


# ----------------------------------------------------------------- HTML
CSS = """*{box-sizing:border-box}
body{margin:0;font-family:system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif;color:#2f2b27;background:#faf8f4;line-height:1.55}
.cal-wrap{max-width:1080px;margin:0 auto;padding:24px 18px 48px}
.cal-wrap header h1{font-size:clamp(1.8rem,4vw,2.6rem);margin:.2em 0;color:#3f4a38}
.cal-intro{font-size:1.08rem;max-width:760px}
.cal-lang{font-size:.9rem}
.cal-nav{display:flex;flex-wrap:wrap;gap:8px;margin:14px 0 6px;padding:0;list-style:none}
.cal-nav a{display:inline-block;padding:6px 12px;border:1px solid #cfc3b1;border-radius:20px;text-decoration:none;color:#3f4a38;font-size:.92rem}
.cal-estilo{margin:40px 0 0}
.cal-estilo h2{border-bottom:2px solid #8a9a7b;padding-bottom:6px;color:#3f4a38}
.cal-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:22px}
.cal-card{background:#fff;border:1px solid #e6ddcf;border-radius:10px;padding:14px;display:flex;flex-direction:column}
.cal-card img{width:100%;height:auto;border-radius:6px;display:block}
.cal-card h3{font-size:1.05rem;margin:12px 0 4px}
.cal-card p{font-size:.92rem;margin:0 0 10px;color:#5b544c}
.cal-btns{display:flex;gap:8px;margin-top:auto;flex-wrap:wrap}
.cal-btns a{flex:1;text-align:center;padding:9px 6px;border-radius:6px;background:#7f9171;color:#fff;text-decoration:none;font-weight:600;font-size:.92rem}
.cal-btns a.alt{background:#efe8dc;color:#3f4a38}
.cal-meses{margin-top:16px;background:#fff;border:1px solid #e6ddcf;border-radius:10px;padding:10px 14px}
.cal-meses summary{cursor:pointer;font-weight:600}
.cal-meses ul{columns:3 160px;padding-left:18px;font-size:.92rem}
.cal-ad{margin:28px 0;min-height:90px;text-align:center}
.cal-pack{background:#eef1ea;border-radius:10px;padding:16px 18px;margin:30px 0}
.cal-faq h2{margin-top:44px}
.cal-faq h3{font-size:1.02rem;margin:18px 0 4px}
.cal-wrap footer{margin-top:44px;font-size:.85rem;color:#6c645b;border-top:1px solid #e6ddcf;padding-top:14px}
.cal-wrap a{color:#55663f}
"""

TXT_WEB = {
    "es": {
        "title": "Calendarios {y} para imprimir gratis (PDF A4 y Carta)",
        "meta": "Descarga gratis calendarios {y} para imprimir en PDF: anual, mensual de 12 meses, mensual en blanco y planificador semanal. 3 estilos, tamaño A4 y Carta, semana desde el lunes.",
        "h1": "Calendarios {y} para imprimir gratis",
        "intro": "Calendarios {y} listos para imprimir en casa, en PDF y sin registrarte. Elige el estilo que más te guste: minimal negro, lino y salvia, o montaña. Todos vienen en tamaño A4 y Carta, con la semana empezando el lunes y los meses en español.",
        "otro": "English version: Free Printable {y} Calendars",
        "pack": "¿Los quieres todos? Descarga el pack completo en un solo archivo ZIP:",
        "pack_btn": "Descargar pack completo (ZIP)",
        "meses": "Meses sueltos {y} (un PDF por mes)",
        "privacidad": "Política de privacidad y cookies",
        "pie": "Calendarios gratis para uso personal, escolar y de oficina. No se permite revender los archivos. Puedes compartir el enlace a esta página.",
        "faq_t": "Preguntas frecuentes",
        "faq": [
            ("¿Los calendarios son gratis de verdad?", "Sí. Puedes descargarlos e imprimirlos todas las veces que quieras para uso personal, en la escuela o en la oficina. No hace falta registrarte ni dejar tu correo."),
            ("¿Qué tamaño de hoja tengo que usar?", "Cada calendario viene en dos tamaños: A4 (el más común en España y gran parte de Latinoamérica) y Carta (el que se usa en México, Estados Unidos y otros países). Elige el botón que coincida con tu papel."),
            ("¿Cómo los imprimo para que salgan bien?", "Abre el PDF y en las opciones de impresión elige \"Tamaño real\" o escala al 100%. Si tu impresora corta los bordes, usa \"Ajustar al área de impresión\"."),
            ("¿En qué día empieza la semana?", "En la versión en español la semana empieza el lunes. La versión en inglés empieza el domingo y marca los feriados federales de Estados Unidos."),
            ("¿Tienen feriados?", "La versión en español solo marca el 1 de enero y el 25 de diciembre, porque los feriados cambian según el país. Te dejamos espacio para anotar los de tu país."),
            ("¿Puedo vender o compartir los archivos?", "Puedes compartir el enlace a esta página todas las veces que quieras. Lo que no se permite es vender los archivos o subirlos a otro sitio."),
        ],
        "tipos": {
            "anual": ("Calendario anual {y}", "Los 12 meses en una sola hoja. Ideal para la heladera o el escritorio."),
            "mensual": ("Calendario mensual {y}", "12 páginas, una por mes, con espacio para notas."),
            "blanco": ("Calendario mensual en blanco", "Sin fechas: escribe el mes y los números. Sirve para cualquier año."),
            "semanal": ("Planificador semanal", "Los 7 días, prioridades, pendientes y notas en una hoja."),
        },
        "alt": "{t} para imprimir gratis, estilo {e}, PDF A4 y Carta",
        "estilo": "Estilo {e}",
    },
    "en": {
        "title": "Free Printable {y} Calendars (PDF, Letter & A4)",
        "meta": "Download free printable {y} calendars in PDF: yearly, 12-month monthly, blank monthly and a weekly planner. 3 styles, US Letter and A4, US federal holidays marked.",
        "h1": "Free Printable {y} Calendars",
        "intro": "Free {y} calendars you can print at home, as PDFs, no sign-up needed. Pick your favorite style: minimal black, linen & sage, or mountain. Every calendar comes in US Letter and A4, weeks start on Sunday, and US federal holidays are marked.",
        "otro": "Versión en español: Calendarios {y} para imprimir gratis",
        "pack": "Want them all? Download the complete pack as one ZIP file:",
        "pack_btn": "Download the full pack (ZIP)",
        "meses": "Single months {y} (one PDF per month)",
        "privacidad": "Privacy & cookie policy",
        "pie": "Free for personal, classroom and office use. Please do not resell the files. You are welcome to share a link to this page.",
        "faq_t": "Frequently asked questions",
        "faq": [
            ("Are these calendars really free?", "Yes. Download and print them as many times as you like for personal, classroom or office use. No sign-up or email required."),
            ("What paper size should I use?", "Every calendar comes in US Letter (8.5 x 11 in) and A4. Pick the button that matches the paper in your printer."),
            ("How do I print them so they look right?", "Open the PDF and choose \"Actual size\" or 100% scale in the print dialog. If your printer cuts off the edges, use \"Fit to printable area\"."),
            ("Which holidays are included?", "The English calendars mark all US federal holidays for {y}, including the observed dates when a holiday falls on a weekend."),
            ("Does the week start on Sunday or Monday?", "The English version starts on Sunday. The Spanish version starts on Monday."),
            ("Can I share or sell the files?", "You can share a link to this page anytime. Please do not sell the files or upload them to another website."),
        ],
        "tipos": {
            "anual": ("{y} Yearly Calendar", "All 12 months on a single page. Great for the fridge or your desk."),
            "mensual": ("{y} Monthly Calendar", "12 pages, one per month, with US holidays and a notes box."),
            "blanco": ("Blank Monthly Calendar", "Undated: fill in the month and numbers. Works for any year."),
            "semanal": ("Weekly Planner", "All 7 days plus priorities, to-do list and notes on one page."),
        },
        "alt": "Free printable {t}, {e} style, PDF in Letter and A4",
        "estilo": "{e} style",
    },
}

PAGINA = {"es": "index.html", "en": "free-printable-{y}-calendars.html"}


def esc(s):
    return html.escape(s, quote=True)


def generar_html(out, year, url_base, pins, pie_txt):
    paginas = {l: PAGINA[l].format(y=year) for l in ("es", "en")}
    (out / "estilos.css").write_text(CSS, encoding="utf-8")
    for lang in ("es", "en"):
        tx = TXT_WEB[lang]
        otro = "en" if lang == "es" else "es"
        canon = url_base + (paginas[lang] if lang == "en" else "")
        og_img = url_base + "img/pins/" + nombre_pin(lang, "lino", "anual", year)
        faq = [(q.format(y=year), a.format(y=year)) for q, a in tx["faq"]]
        import json
        ld = {
            "@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q,
                            "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq],
        }
        h = []
        a = h.append
        a(f'<!DOCTYPE html>\n<html lang="{lang}">\n<head>\n<meta charset="utf-8">')
        a('<meta name="viewport" content="width=device-width, initial-scale=1">')
        a(f'<title>{esc(tx["title"].format(y=year))}</title>')
        a(f'<meta name="description" content="{esc(tx["meta"].format(y=year))}">')
        a(f'<link rel="canonical" href="{esc(canon)}">')
        a(f'<link rel="alternate" hreflang="es" href="{esc(url_base)}">')
        a(f'<link rel="alternate" hreflang="en" href="{esc(url_base + paginas["en"])}">')
        a(f'<link rel="alternate" hreflang="x-default" href="{esc(url_base + paginas["en"])}">')
        a(f'<meta property="og:type" content="website">')
        a(f'<meta property="og:title" content="{esc(tx["h1"].format(y=year))}">')
        a(f'<meta property="og:description" content="{esc(tx["meta"].format(y=year))}">')
        a(f'<meta property="og:url" content="{esc(canon)}">')
        a(f'<meta property="og:image" content="{esc(og_img)}">')
        a('<meta name="twitter:card" content="summary_large_image">')
        a(f'<link rel="alternate" type="application/rss+xml" title="{esc(tx["h1"].format(y=year))}" href="rss.xml">')
        a('<link rel="stylesheet" href="estilos.css">')
        a(f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>')
        a('<!-- GA4 -->')
        a('<!-- ADSENSE: script de AdSense (auto ads) va acá, en el head -->')
        a('</head>\n<body>\n<main class="cal-wrap">')
        a('<header>')
        a(f'<p class="cal-lang"><a href="{esc(paginas[otro])}" hreflang="{otro}">{esc(tx["otro"].format(y=year))}</a></p>')
        a(f'<h1>{esc(tx["h1"].format(y=year))}</h1>')
        a(f'<p class="cal-intro">{esc(tx["intro"].format(y=year))}</p>')
        a('<ul class="cal-nav">')
        for ek, est in ESTILOS.items():
            a(f'<li><a href="#{est["slug"][lang]}">{esc(tx["estilo"].format(e=est["nombre"][lang]))}</a></li>')
        a(f'<li><a href="#faq">{esc(tx["faq_t"])}</a></li></ul>')
        a('</header>')
        a('<div class="cal-ad"><!-- ADSENSE: bloque 1 (debajo de la intro) --></div>')
        primero, segundo = ("a4", "carta") if lang == "es" else ("carta", "a4")
        for n, (ek, est) in enumerate(ESTILOS.items()):
            nom = est["nombre"][lang]
            a(f'<section class="cal-estilo" id="{est["slug"][lang]}">')
            a(f'<h2>{esc(tx["estilo"].format(e=nom))}</h2>\n<div class="cal-grid">')
            for tipo in TIPOS:
                tt, desc = tx["tipos"][tipo]
                tt = tt.format(y=year)
                mini = f'img/mini/{Path(nombre_pin(lang, ek, tipo, year)).stem}.webp'
                ancla = f'{est["slug"][lang]}-{tipo}'
                a(f'<article class="cal-card" id="{ancla}">')
                a(f'<img src="{mini}" width="400" height="600" loading="lazy" alt="{esc(tx["alt"].format(t=tt, e=nom))}">')
                a(f'<h3>{esc(tt)}</h3><p>{esc(desc)}</p><div class="cal-btns">')
                for k, tam in enumerate((primero, segundo)):
                    href = ruta_pdf(lang, ek, tipo, tam, year).as_posix()
                    cls = "" if k == 0 else ' class="alt"'
                    a(f'<a{cls} href="{href}" download>PDF {TAM_LABEL[lang][tam]}</a>')
                a('</div></article>')
            a('</div>')
            a(f'<details class="cal-meses"><summary>{esc(tx["meses"].format(y=year))} · {esc(nom)}</summary><ul>')
            for m in range(1, 13):
                l1 = ruta_pdf(lang, ek, "mensual", primero, year, m).as_posix()
                l2 = ruta_pdf(lang, ek, "mensual", segundo, year, m).as_posix()
                a(f'<li>{MESES[lang][m - 1]} {year}: <a href="{l1}" download>{TAM_LABEL[lang][primero]}</a> · '
                  f'<a href="{l2}" download>{TAM_LABEL[lang][segundo]}</a></li>')
            a('</ul></details></section>')
            if n < len(ESTILOS) - 1:
                a(f'<div class="cal-ad"><!-- ADSENSE: bloque {n + 2} (entre estilos) --></div>')
        zipn = f"calendarios-{year}-pack-es.zip" if lang == "es" else f"calendars-{year}-pack-en.zip"
        a(f'<div class="cal-pack"><p>{esc(tx["pack"])}</p><div class="cal-btns"><a href="{zipn}" download>{esc(tx["pack_btn"])}</a></div></div>')
        a('<section class="cal-faq" id="faq">')
        a(f'<h2>{esc(tx["faq_t"])}</h2>')
        for q, r in faq:
            a(f'<h3>{esc(q)}</h3>\n<p>{esc(r)}</p>')
        a('</section>')
        a('<div class="cal-ad"><!-- ADSENSE: bloque final (antes del pie) --></div>')
        a('<footer>')
        a(f'<p>{esc(tx["pie"])}</p>')
        a(f'<p><!-- PRIVACIDAD: cambiar el href por la URL real de la política de privacidad y cookies -->'
          f'<a href="/privacidad.html" rel="nofollow">{esc(tx["privacidad"])}</a>'
          + (f' · {esc(pie_txt)}' if pie_txt else "") + '</p>')
        a(f'<p>© {year} Skye Solutions AI</p>')
        a('</footer>\n</main>\n</body>\n</html>\n')
        (out / paginas[lang]).write_text("\n".join(h), encoding="utf-8")
    return paginas


def generar_rss(out, year, url_base, pins, paginas):
    ahora = format_datetime(dt.datetime.now(dt.timezone.utc))
    items = []
    for lang in ("es", "en"):
        tx = TXT_WEB[lang]
        pag = url_base + ("" if lang == "es" else paginas["en"])
        for ek, est in ESTILOS.items():
            for tipo in TIPOS:
                tt, desc = tx["tipos"][tipo]
                tt = tt.format(y=year)
                nom = est["nombre"][lang]
                titulo = (f"{tt} para imprimir gratis - {nom}" if lang == "es"
                          else f"Free Printable {tt} - {nom}")
                png = pins[(lang, ek, tipo)][0]
                img_url = url_base + "img/pins/" + png.name
                link = f'{pag}#{est["slug"][lang]}-{tipo}'
                extra = (" PDF gratis en A4 y Carta." if lang == "es" else " Free PDF in US Letter and A4.")
                descr = f'<img src="{img_url}" alt="{esc(tt)}"/><p>{esc(desc + extra)}</p>'
                items.append(f"""  <item>
    <title>{esc(titulo)}</title>
    <link>{esc(link)}</link>
    <guid isPermaLink="false">calendarios-{year}-{lang}-{ek}-{tipo}</guid>
    <pubDate>{ahora}</pubDate>
    <description><![CDATA[{descr}]]></description>
    <enclosure url="{esc(img_url)}" length="{png.stat().st_size}" type="image/png"/>
    <media:content url="{esc(img_url)}" medium="image" type="image/png" width="1000" height="1500"/>
  </item>""")
    rss = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:media="http://search.yahoo.com/mrss/" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
  <title>Calendarios {year} para imprimir gratis / Free Printable {year} Calendars</title>
  <link>{esc(url_base)}</link>
  <atom:link href="{esc(url_base)}rss.xml" rel="self" type="application/rss+xml"/>
  <description>Calendarios {year} gratis en PDF (A4 y Carta) / Free printable {year} calendars (Letter and A4).</description>
  <language>es</language>
  <lastBuildDate>{ahora}</lastBuildDate>
{chr(10).join(items)}
</channel>
</rss>
"""
    (out / "rss.xml").write_text(rss, encoding="utf-8")


def generar_zips(out, year):
    for lang, nombre in (("es", f"calendarios-{year}-pack-es.zip"), ("en", f"calendars-{year}-pack-en.zip")):
        zp = out / nombre
        with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
            for p in sorted((out / "pdf" / lang).rglob("*.pdf")):
                z.write(p, p.relative_to(out / "pdf" / lang).as_posix())


# ----------------------------------------------------------------- chequeos
def chequear_fechas(year):
    # chequeo cruzado con datetime: el dia de la semana del 1/1 y la cantidad de dias
    d = dt.date(year, 1, 1)
    total = sum(calendar.monthrange(year, m)[1] for m in range(1, 13))
    assert total == (366 if calendar.isleap(year) else 365)
    if year == 2027:
        assert d.weekday() == 4, "El 1/1/2027 tiene que ser viernes"
        esperados = {dt.date(2027, 1, 1), dt.date(2027, 1, 18), dt.date(2027, 2, 15), dt.date(2027, 5, 31),
                     dt.date(2027, 6, 18), dt.date(2027, 6, 19), dt.date(2027, 7, 4), dt.date(2027, 7, 5),
                     dt.date(2027, 9, 6), dt.date(2027, 10, 11), dt.date(2027, 11, 11), dt.date(2027, 11, 25),
                     dt.date(2027, 12, 24), dt.date(2027, 12, 25), dt.date(2027, 12, 31)}
        assert set(feriados_us(2027)) == esperados, sorted(feriados_us(2027))
    return DIAS["es"][d.weekday()]


def main():
    ap = argparse.ArgumentParser(description="Regenera el pack de calendarios para un año.")
    ap.add_argument("anio", type=int, help="Año, por ejemplo 2028")
    ap.add_argument("--url", default=None,
                    help="URL pública donde va a quedar la carpeta (terminada en /). "
                         "Por defecto https://TU-SITIO.com/calendarios-AAAA/")
    ap.add_argument("--salida", default=None, help="Carpeta de salida (por defecto ./sitio/calendarios-AAAA/)")
    ap.add_argument("--pie", default="", help="Texto chico al pie de cada hoja y pin (por ej. tu dominio)")
    args = ap.parse_args()
    year = args.anio
    url = args.url or f"https://TU-SITIO.com/calendarios-{year}/"
    if not url.endswith("/"):
        url += "/"
    out = Path(args.salida) if args.salida else AQUI / "sitio" / f"calendarios-{year}"
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    registrar_fuentes()
    dia = chequear_fechas(year)
    print(f"[ok] {year}: el 1 de enero cae {dia}")
    pdfs = generar_pdfs(out, year, args.pie)
    print(f"[ok] {len(pdfs)} PDFs")
    pins = generar_pins(out, year, args.pie)
    print(f"[ok] {len(pins)} pins")
    paginas = generar_html(out, year, url, pins, args.pie)
    generar_rss(out, year, url, pins, paginas)
    generar_zips(out, year)
    print(f"[ok] HTML, rss.xml y zips en {out}")


if __name__ == "__main__":
    main()
