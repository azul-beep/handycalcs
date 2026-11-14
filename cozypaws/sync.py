#!/usr/bin/env python3
"""Trae los productos de Cozy Paws desde la carpeta del proyecto al repo.

Lo corre un hilo de Claude (o cualquiera con la carpeta) cada vez que se suman productos nuevos
a /mnt/project-files/navidad-mascotas-maestros/listados-*.csv. GitHub Actions NO ve esa carpeta,
por eso las filas y las vistas previas quedan guardadas en cozypaws/data/.

  python3 cozypaws/sync.py [--src /mnt/project-files/navidad-mascotas-maestros]

Escribe data/productos.csv (columnas fijas) y data/img/<sku>.jpg (vista previa 900 px, liviana).
Las filas "EN ESPERA" se saltean. Nunca borra filas que ya estaban (si un producto se va de Etsy,
borrarlo a mano de productos.csv).
"""
import argparse, csv, glob, os, re
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
COLS = ['dia', 'sku', 'precio', 'titulo', 'etiquetas', 'texto', 'imagen', 'tinta']


def first_file(*vals):
    for v in vals:
        m = re.search(r'([\w./-]+\.(?:png|jpg))', v or '')
        if m:
            return m.group(1)
    return ''


def preview(src, dst, tinta):
    im = Image.open(src)
    if im.mode == 'RGBA' or tinta:
        # estampa con fondo transparente: tinta clara sobre verde, tinta oscura sobre crema
        bg = (47, 74, 64) if tinta == 'clara' else (250, 244, 235)
        im = im.convert('RGBA')
        bbox = im.getbbox()
        if bbox:
            im = im.crop(bbox)
        side = int(max(im.size) * 1.18)
        canvas = Image.new('RGB', (side, side), bg)
        canvas.paste(im, ((side - im.width) // 2, (side - im.height) // 2), im)
        im = canvas
    else:
        im = im.convert('RGB')
    im.thumbnail((900, 900))
    im.save(dst, 'JPEG', quality=82, optimize=True, progressive=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--src', default='/mnt/project-files/navidad-mascotas-maestros')
    a = ap.parse_args()
    out_csv = os.path.join(HERE, 'data', 'productos.csv')
    rows = {}
    if os.path.exists(out_csv):
        for r in csv.DictReader(open(out_csv, encoding='utf-8')):
            rows[r['sku']] = r
    nuevos = 0
    for path in sorted(glob.glob(os.path.join(a.src, 'listados-*.csv'))):
        for r in csv.DictReader(open(path, encoding='utf-8')):
            if not re.match(r'\d{4}-\d{2}-\d{2}$', r.get('dia', '')):
                continue
            f = first_file(r.get('archivos'), r.get('archivo'), r.get('archivo_colores_claros'), r.get('archivo_colores_oscuros'))
            if not f:
                continue
            src = os.path.join(a.src, 'estampas', f)
            if not os.path.exists(src):
                print('falta imagen', src); continue
            tinta = 'clara' if 'tinta-clara' in f else ('oscura' if 'tinta-oscura' in f else '')
            sku = r['sku']
            img = f'{sku}.jpg'
            dst = os.path.join(HERE, 'data', 'img', img)
            if not os.path.exists(dst):
                preview(src, dst, tinta)
            if sku not in rows:
                nuevos += 1
            rows[sku] = dict(dia=r['dia'], sku=sku, precio=r.get('precio', ''), titulo=r['titulo'].strip(),
                             etiquetas=r.get('etiquetas', ''), texto=r.get('texto', ''), imagen=img, tinta=tinta)
    with open(out_csv, 'w', encoding='utf-8', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=COLS)
        w.writeheader()
        for r in sorted(rows.values(), key=lambda r: (r['dia'], r['sku'])):
            w.writerow({k: r.get(k, '') for k in COLS})
    print(f'{len(rows)} productos ({nuevos} nuevos) en {out_csv}')


if __name__ == '__main__':
    main()
