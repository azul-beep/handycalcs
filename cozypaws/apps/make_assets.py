#!/usr/bin/env python3
"""Arma (una sola vez) las estampas e íconos de las apps de Cozy Paws en cozypaws/data/apps/.
Lee las estampas originales de la carpeta del proyecto. Volver a correr solo si cambian los diseños.
  python3 cozypaws/apps/make_assets.py [/mnt/project-files/navidad-mascotas-maestros/estampas]
"""
import os, sys
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, '..', 'data')
OUT = os.path.join(DATA, 'apps')
SRC = sys.argv[1] if len(sys.argv) > 1 else '/mnt/project-files/navidad-mascotas-maestros/estampas'
# id de la estampa -> archivo original (tinta oscura, fondo transparente)
STAMPS = {
    'dog-mom': 'a01-dog-mom-paw-tinta-oscura', 'dog-dad': 'a02-dog-dad-paw-tinta-oscura',
    'cat-mom': 'a03-cat-mom-tinta-oscura', 'cat-dad': 'a04-cat-dad-tinta-oscura',
    'golden': 'a05-golden-retriever-mom-tinta-oscura', 'frenchie': 'a06-frenchie-mom-tinta-oscura',
    'doodle': 'a07-doodle-mom-tinta-oscura', 'labrador': 'p04-labrador-dog-mom-tinta-oscura',
    'german-shepherd': 'p06-german-shepherd-dog-mom-tinta-oscura', 'dachshund': 'p07-dachshund-dog-mom-tinta-oscura',
    'cozy-pup': 'w08-cozy-pup-tinta-oscura', 'dog-mom-club': 'w06-dog-mom-club-tinta-oscura',
    'cat-mom-club': 'w07-cat-mom-club-tinta-oscura', 'comfy': 'a09-my-dog-was-comfy-tinta-oscura',
    'woofmas': 'p11-merry-woofmas-tinta-oscura', 'meowy': 'a10-meowy-christmas-tinta-oscura',
    'good-boy': 'p13-santas-favorite-good-boy-tinta-oscura',
}
CREAM = (243, 233, 215)

os.makedirs(os.path.join(OUT, 'stamps'), exist_ok=True)
for k, f in STAMPS.items():
    im = Image.open(os.path.join(SRC, f + '.png')).convert('RGBA')
    im = im.crop(im.getbbox())
    im.thumbnail((520, 520), Image.LANCZOS)
    im.quantize(64, method=Image.FASTOCTREE).save(os.path.join(OUT, 'stamps', k + '.png'), optimize=True)

logo = Image.open(os.path.join(DATA, 'brand', 'logo-ilustrado.png')).convert('RGBA')
logo = logo.crop(logo.getbbox())


def icon(size, frac, name, round_=False):
    c = Image.new('RGBA', (size, size), CREAM + (255,))
    lg = logo.copy(); lg.thumbnail((int(size * frac), int(size * frac)), Image.LANCZOS)
    c.paste(lg, ((size - lg.width) // 2, (size - lg.height) // 2), lg)
    c.convert('RGB').save(os.path.join(OUT, name), optimize=True)


for s in (192, 512):
    icon(s, .9, f'icon-{s}.png')
icon(512, .66, 'icon-maskable-512.png')
icon(180, .86, 'apple-touch-icon.png')
print('listo:', OUT)
