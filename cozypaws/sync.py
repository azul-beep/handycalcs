#!/usr/bin/env python3
"""Trae los productos de Cozy Paws desde la carpeta del proyecto al repo.

Lo corre un hilo de Claude (o cualquiera con la carpeta) cada vez que se suman productos nuevos
a /mnt/project-files/navidad-mascotas-maestros/listados-*.csv. GitHub Actions NO ve esa carpeta,
por eso las filas y las vistas previas quedan guardadas en cozypaws/data/.

  python3 cozypaws/sync.py [--src /mnt/project-files/navidad-mascotas-maestros]

Escribe data/productos.csv (columnas fijas) y data/img/<sku>.jpg (vista previa 900 px, liviana).
Si existe calendario-etsy-5xdia.csv, manda la fecha de cada producto y lo que no está ahí queda afuera.
Los personalizados (x..) se saltean hasta que estén en Etsy. Los imprimibles (i..) salen de carga-navidad.md.
"""
import argparse, csv, glob, os, re, sys
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mockups import mockup  # noqa: E402
from build import kind_of  # noqa: E402

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


IMPRIMIBLES = {  # sku -> nombre base del PDF (fotos en imprimibles/fotos-etsy/<base>-1.jpg)
    'i01': 'etiquetas-regalo-from-the-dog', 'i02': 'etiquetas-regalo-from-the-cat', 'i03': 'laminas-colorear-perros-gatos',
    'i04': 'planner-salud-mascota', 'i05': 'calendario-2027-mascotas',
}


def imprimibles(src):
    """Lee título, precio, etiquetas y foto de los imprimibles (i..) desde carga-navidad.md."""
    out = {}
    text = open(os.path.join(src, 'carga-navidad.md'), encoding='utf-8').read()
    for m in re.finditer(r'^### ([^\n]*?)· (i\d\d) · (.+)\n((?:\d\. .+\n?)+)', text, re.M):
        head, sku, titulo, body = m.groups()
        if 'PAUSA' in head and 'ACTIVO' not in head:
            continue
        precio = re.search(r'precio: ([\d.]+) USD', body)
        tags = re.search(r'Etiquetas: (.+)', body)
        foto = re.search(r'Fotos: (\S+?)-1\.\.3\.jpg', body)
        img = (foto.group(1) + '-1.jpg') if foto else os.path.join('imprimibles', 'fotos-etsy', IMPRIMIBLES.get(sku, sku) + '-1.jpg')
        if precio and tags:
            out[sku] = dict(titulo=titulo.strip(), precio=precio.group(1), etiquetas=tags.group(1).strip(), archivo=img)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--src', default='/mnt/project-files/navidad-mascotas-maestros')
    ap.add_argument('--rehacer', action='store_true', help='volver a armar todas las fotos')
    a = ap.parse_args()
    out_csv = os.path.join(HERE, 'data', 'productos.csv')
    rows = {}
    if os.path.exists(out_csv):
        for r in csv.DictReader(open(out_csv, encoding='utf-8')):
            rows[r['sku']] = r
    # calendario maestro de Etsy (manda la fecha de cada producto)
    cal = {}
    cal_path = os.path.join(a.src, 'calendario-etsy-5xdia.csv')
    if os.path.exists(cal_path):
        for r in csv.DictReader(open(cal_path, encoding='utf-8')):
            if 'Personalizado' in r.get('grupo', ''):
                continue  # solo si Printify Free lo permite: se suman a mano cuando estén en Etsy
            cal[r['sku']] = r['dia']
    fuentes = []
    for path in sorted(glob.glob(os.path.join(a.src, 'listados-*.csv'))):
        for r in csv.DictReader(open(path, encoding='utf-8')):
            fuentes.append(r)
    for sku, r in imprimibles(a.src).items():
        fuentes.append(dict(r, sku=sku, dia=cal.get(sku, '')))
    nuevos = 0
    for r in fuentes:
        sku = r.get('sku', '')
        dia = cal.get(sku) if cal else r.get('dia', '')
        if not dia or not re.match(r'\d{4}-\d{2}-\d{2}$', dia):
            continue
        f = first_file(r.get('archivo'), r.get('archivos'), r.get('archivo_colores_claros'), r.get('archivo_colores_oscuros'))
        src = next((p for p in (os.path.join(a.src, f), os.path.join(a.src, 'estampas', f)) if f and os.path.exists(p)), None)
        if not src:
            print('falta imagen', sku, f); continue
        tinta = 'clara' if 'tinta-clara' in f else ('oscura' if 'tinta-oscura' in f else '')
        img = f'{sku}.jpg'
        dst = os.path.join(HERE, 'data', 'img', img)
        foto = os.path.join(HERE, 'data', 'fotos', f'{sku}.jpg')  # foto real (opcional) le gana al mockup
        if a.rehacer or not os.path.exists(dst):
            if os.path.exists(foto):
                im = Image.open(foto).convert('RGB')
            else:
                im = mockup(src, kind_of(r['titulo']), sku, os.path.basename(f))
            im.thumbnail((900, 900))
            im.save(dst, 'JPEG', quality=84, optimize=True, progressive=True)
        if sku not in rows:
            nuevos += 1
        rows[sku] = dict(dia=dia, sku=sku, precio=r.get('precio', ''), titulo=r['titulo'].strip(),
                         etiquetas=r.get('etiquetas', ''), texto=r.get('texto', ''), imagen=img, tinta=tinta)
    if cal:
        sobran = [k for k in rows if k not in cal]
        for k in sobran:
            print('no está en el calendario, queda afuera:', k)
            rows.pop(k)
    with open(out_csv, 'w', encoding='utf-8', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=COLS)
        w.writeheader()
        for r in sorted(rows.values(), key=lambda r: (r['dia'], r['sku'])):
            w.writerow({k: r.get(k, '') for k in COLS})
    faltan = [k for k in cal if k not in rows]
    print(f'{len(rows)} productos ({nuevos} nuevos) en {out_csv}; del calendario faltan: {faltan or "ninguno"}')


if __name__ == '__main__':
    main()
