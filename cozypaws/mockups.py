"""Fotos de producto simples para la web de Cozy Paws (sin Printify ni Claude).

mockup(src, kind, sku, file_name) -> imagen RGB 1000x1000:
  tazas: taza blanca con asa y el diseño del frente
  adornos: adorno con forma (redondo, corazón, estrella) con tapita dorada y cinta
  ropa: remera o buzo de color con el diseño en el pecho
  lo demás (mantas, papel, imprimibles...): la imagen sobre fondo de color con sombra
Si existe data/fotos/<sku>.jpg (por ejemplo una foto real de Etsy o Printify), sync.py usa esa.
"""
import math, zlib
from PIL import Image, ImageDraw, ImageFilter, ImageChops

CREAM = (243, 233, 215)
BGS = [(243, 233, 215), (234, 223, 203), (220, 231, 230), (238, 221, 214), (230, 226, 210)]
GOLD = (200, 150, 46)
W = 1000


def bg_for(sku):
    return BGS[zlib.crc32(sku.encode()) % len(BGS)]


def soft_shadow(canvas, mask, offset=(0, 18), blur=28, opacity=70):
    sh = Image.new('L', canvas.size, 0)
    sh.paste(mask, offset, mask)
    sh = sh.filter(ImageFilter.GaussianBlur(blur)).point(lambda v: v * opacity // 255)
    dark = Image.new('RGB', canvas.size, (60, 40, 40))
    canvas.paste(dark, (0, 0), sh)


def fit(im, box_w, box_h):
    im = im.copy()
    im.thumbnail((box_w, box_h), Image.LANCZOS)
    return im


def trim(im):
    if im.mode != 'RGBA':
        return im
    b = im.getbbox()
    return im.crop(b) if b else im


def mug(src, sku):
    c = Image.new('RGB', (W, W), bg_for(sku))
    body = (230, 250, 680, 810)
    m = Image.new('L', (W, W), 0)
    d = ImageDraw.Draw(m)
    d.rounded_rectangle(body, 40, fill=255)
    d.ellipse((800 - 150, 380, 800 + 70, 690), fill=255)  # asa (exterior)
    soft_shadow(c, m)
    mug_img = Image.new('RGB', (W, W), (252, 251, 248))
    g = ImageDraw.Draw(mug_img)
    for x in range(body[0], body[2]):  # sombreado suave en los bordes
        t = (x - body[0]) / (body[2] - body[0])
        v = int(252 - 22 * (abs(t - 0.42) * 2) ** 2.2)
        g.line([(x, 0), (x, W)], fill=(v, v - 1, v - 4))
    c.paste(mug_img, (0, 0), m)
    d2 = ImageDraw.Draw(c)
    d2.ellipse((800 - 100, 440, 800 + 18, 630), fill=bg_for(sku))  # hueco del asa
    d2.ellipse((body[0], body[1] - 26, body[2], body[1] + 26), fill=(236, 233, 228), outline=(225, 221, 214), width=3)
    art = Image.open(src).convert('RGBA')
    half = art.crop((0, 0, art.width // 2, art.height))
    half = trim(half)
    half = fit(half, 330, 380)
    c.paste(half, ((body[0] + body[2]) // 2 - half.width // 2, 540 - half.height // 2), half)
    return c


def shape_mask(shape, size=640):
    m = Image.new('L', (size, size), 0)
    d = ImageDraw.Draw(m)
    if shape == 'heart':
        r = size * 0.27
        d.ellipse((size * 0.5 - 2 * r + 4, size * 0.1, size * 0.5 + 4, size * 0.1 + 2 * r), fill=255)
        d.ellipse((size * 0.5 - 4, size * 0.1, size * 0.5 + 2 * r - 4, size * 0.1 + 2 * r), fill=255)
        d.polygon([(size * 0.5 - 2 * r * 0.98, size * 0.1 + r * 1.25), (size * 0.5 + 2 * r * 0.98, size * 0.1 + r * 1.25), (size * 0.5, size * 0.95)], fill=255)
    elif shape == 'star':
        pts = []
        for i in range(10):
            ang = -math.pi / 2 + i * math.pi / 5
            rad = size * (0.49 if i % 2 == 0 else 0.22)
            pts.append((size / 2 + rad * math.cos(ang), size / 2 + rad * math.sin(ang) + size * 0.03))
        d.polygon(pts, fill=255)
    else:
        d.ellipse((0, 0, size - 1, size - 1), fill=255)
    return m


def ornament(src, sku, shape):
    c = Image.new('RGB', (W, W), bg_for(sku))
    S = 640
    art = Image.open(src).convert('RGB')
    side = min(art.size)
    art = art.crop(((art.width - side) // 2, (art.height - side) // 2, (art.width + side) // 2, (art.height + side) // 2)).resize((S, S), Image.LANCZOS)
    m = shape_mask(shape, S)
    pos = ((W - S) // 2, 250)
    full = Image.new('L', (W, W), 0)
    full.paste(m, pos)
    soft_shadow(c, full, offset=(0, 22))
    c.paste(art, pos, m)
    d = ImageDraw.Draw(c)
    top = pos[1] + (int(S * 0.1) + 8 if shape == 'heart' else 6 if shape != 'star' else int(S * 0.04))
    d.line([(W // 2, 70), (W // 2, top - 34)], fill=(150, 40, 50), width=7)  # cinta
    d.ellipse((W // 2 - 34, 40, W // 2 + 34, 100), outline=(150, 40, 50), width=7)
    d.rounded_rectangle((W // 2 - 34, top - 40, W // 2 + 34, top + 6), 8, fill=GOLD)  # tapita
    d.ellipse((W // 2 - 12, top - 56, W // 2 + 12, top - 32), outline=GOLD, width=6)
    return c


TEE = [(395, 175), (270, 215), (120, 400), (215, 465), (300, 370), (300, 905), (700, 905), (700, 370), (785, 465), (880, 400), (730, 215), (605, 175)]
SWEAT = [(395, 175), (270, 215), (170, 420), (110, 820), (205, 840), (285, 470), (300, 905), (700, 905), (715, 470), (795, 840), (890, 820), (830, 420), (730, 215), (605, 175)]


def garment(src, sku, long_sleeve, ink):
    c = Image.new('RGB', (W, W), bg_for(sku))
    col = (226, 214, 190) if ink != 'clara' else (59, 36, 51)
    if ink == 'clara' and zlib.crc32(sku.encode()) % 2:
        col = (52, 82, 70)
    m = Image.new('L', (W, W), 0)
    d = ImageDraw.Draw(m)
    d.polygon(SWEAT if long_sleeve else TEE, fill=255)
    d.ellipse((392, 120, 608, 245), fill=0)  # cuello
    soft_shadow(c, m)
    c.paste(Image.new('RGB', (W, W), col), (0, 0), m)
    d2 = ImageDraw.Draw(c)
    edge = tuple(max(0, v - 18) for v in col)
    d2.arc((392, 120, 608, 245), 0, 180, fill=edge, width=14)
    if long_sleeve:
        d2.rectangle((300, 860, 700, 905), fill=edge)
    art = trim(Image.open(src).convert('RGBA'))
    art = fit(art, 300, 300)
    c.paste(art, (W // 2 - art.width // 2, 300 + (300 - art.height) // 2 - 20), art)
    return c


def flat(src, sku):
    c = Image.new('RGB', (W, W), bg_for(sku))
    art = Image.open(src)
    if art.mode == 'RGBA':
        base = Image.new('RGB', art.size, CREAM)
        base.paste(art, (0, 0), art)
        art = base
    art = fit(art.convert('RGB'), 820, 820)
    pos = ((W - art.width) // 2, (W - art.height) // 2)
    m = Image.new('L', (W, W), 0)
    ImageDraw.Draw(m).rounded_rectangle((pos[0], pos[1], pos[0] + art.width, pos[1] + art.height), 18, fill=255)
    soft_shadow(c, m)
    rm = Image.new('L', art.size, 0)
    ImageDraw.Draw(rm).rounded_rectangle((0, 0, art.width - 1, art.height - 1), 18, fill=255)
    c.paste(art, pos, rm)
    return c


def mockup(src, kind, sku, name):
    k = kind.lower()
    n = name.lower()
    if 'mug' in k or 'tumbler' in k:
        return mug(src, sku)
    if 'ornament' in k:
        shape = 'heart' if 'corazon' in n else 'star' if 'estrella' in n else 'round'
        return ornament(src, sku, shape)
    if any(w in k for w in ('t-shirt', 'sweatshirt')) and ('tinta' in n):
        ink = 'clara' if 'tinta-clara' in n else 'oscura'
        return garment(src, sku, 'sweatshirt' in k, ink)
    return flat(src, sku)
