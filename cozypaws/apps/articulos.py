"""Artículos de Cozy Paws (/blog/<slug>/): salen solos de a 1 por día, gratis y sin Claude.

Los textos están escritos de antemano en cozypaws/articulos/NN-<slug>.html (cabecera "clave: valor", una línea "---" y el cuerpo en HTML).
El número NN marca el orden: el 01 sale el día START, el 02 al día siguiente, etc. build.py llama a build_blog() en cada corrida
(todos los días a las 2 PM de Utah), así que el artículo del día aparece solo, con su pin 1000x1500 en el feed.xml para Pinterest.
Para sumar artículos: agregar archivos con el número siguiente (no cambiar los nombres de los que ya salieron).
"""
import datetime as dt, html, os, re, shutil
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import afiliados as AF  # afiliados.json en la raíz del repo: la cabecera "socios: chewy, lemonade" muestra esos programas cuando estén activos

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(os.path.dirname(HERE), 'articulos')
START = dt.date(2026, 11, 16)
E = html.escape


def load(src_dir=SRC, start=START):
    """Lee los artículos en orden. Cada uno queda con 'n', 'slug', 'live' (fecha de salida) y 'body'."""
    out = []
    for f in sorted(os.listdir(src_dir)):
        m = re.match(r'(\d+)-([a-z0-9-]+)\.html$', f)
        if not m:
            continue
        raw = open(os.path.join(src_dir, f), encoding='utf-8').read()
        head, body = raw.split('\n---\n', 1)
        a = dict(line.split(': ', 1) for line in head.strip().splitlines())
        a.update(n=int(m.group(1)), slug=m.group(2), body=body.strip())
        a['live'] = start + dt.timedelta(days=a['n'] - 1)
        out.append(a)
    return out


def build_blog(page, config, OUT, DATA, today, pin_maker):
    """Escribe los artículos que ya salieron y el índice /blog/. Devuelve (urls para el sitemap, items para el feed)."""
    urls, items = [], []
    live = [a for a in load() if a['live'] <= today]
    pins_cache = os.path.join(DATA, 'pins')
    os.makedirs(pins_cache, exist_ok=True)
    os.makedirs(os.path.join(OUT, 'img', 'pin'), exist_ok=True)
    pin = pin_maker(DATA)
    shop_box = (f'<a class="feature" href="{E(config["shop"])}" data-etsy="blog" rel="nofollow" style="background:var(--cream2);color:var(--ink);border:2px dashed var(--gold)">'
                '<div><b style="color:var(--plum)">Cozy Paws on Etsy</b>Original designs for dog and cat people on mugs, sweatshirts, ornaments and more, '
                'drawn in Salt Lake City and printed on demand in the USA by our production partners. See the shop →</div></a>')
    apps = ('<div class="tools" style="margin-top:20px"><a class="tool" href="/diary/" style="background:var(--plum)"><b>Paw Diary app 📔</b><span>Weight chart, '
            'vaccine and flea pill reminders and a daily food plan. Free, works offline.</span></a><a class="tool" href="/fun/" style="background:var(--rose)">'
            '<b>Paw Party app 🎉</b><span>Human years, name ideas, a personality quiz and birthday cards for your pet.</span></a></div>')
    for a in live:
        others = [o for o in live if o is not a][-6:]
        more = ''.join(f'<a href="/blog/{o["slug"]}/">{E(o["h1"])}</a>' for o in reversed(others))
        socios = AF.caja(AF.ids_de(a.get('socios')), 'Helpful for this', 'en', 'post aff',
                         'background:var(--cream2);border:2px solid var(--gold);border-radius:14px;padding:6px 20px 12px;margin-top:22px')
        body = (f'<article class="post"><p class="kind">Pet tips · {a["live"].strftime("%B %-d, %Y")}</p><h1>{E(a["h1"])}</h1>{a["body"]}</article>'
                + socios + apps + shop_box + (f'<h2>More pet tips</h2><div class="pills">{more}</div>' if more else ''))
        img = f'a-{a["slug"]}.jpg'
        ld = [{'@context': 'https://schema.org', '@type': 'Article', 'headline': a['h1'], 'description': a['description'],
               'datePublished': a['live'].isoformat(), 'image': config['url'] + f'/img/pin/{img}',
               'author': {'@type': 'Organization', 'name': config['name']}, 'publisher': {'@type': 'Organization', 'name': config['name']},
               'mainEntityOfPage': config['url'] + f'/blog/{a["slug"]}/'},
              {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
                  {'@type': 'ListItem', 'position': 1, 'name': 'Pet tips', 'item': config['url'] + '/blog/'},
                  {'@type': 'ListItem', 'position': 2, 'name': a['h1'], 'item': config['url'] + f'/blog/{a["slug"]}/'}]}]
        stamp = os.path.join(DATA, 'apps', 'stamps', a.get('stamp', '') + '.png')
        pin(os.path.join(pins_cache, img), 'Pet tips', a['pin'], a.get('sub', ''), stamp if a.get('stamp') and os.path.exists(stamp) else None)
        page(f'/blog/{a["slug"]}/', f'{a["title"]} | Cozy Paws', a['description'][:158], body, today, image=f'/img/pin/{img}', jsonld=ld)
        urls.append((f'/blog/{a["slug"]}/', a['live']))
        items.append((a['live'], a['h1'], f'/blog/{a["slug"]}/', f'/img/pin/{img}', a['description'], 'a-' + a['slug']))
    lis = ''.join(f'<a class="tool" href="/blog/{a["slug"]}/" style="background:var(--blue)"><b>{E(a["h1"])}</b><span>{E(a["description"])}</span></a>' for a in reversed(live))
    page('/blog/', 'Pet Care Tips for Dog and Cat Owners | Cozy Paws', 'Simple, practical tips for dog and cat owners: winter care, feeding, vaccines, safety and more. A new article every day.',
         '<h1>Pet tips</h1><p class="lead">Simple, practical tips for dog and cat people. A new article every day.</p>'
         + (f'<div class="tools">{lis}</div>' if lis else '<p>The first article comes out on November 16. Meanwhile, try our <a href="/tools/">free pet tools</a>.</p>')
         + apps, today)
    urls.append(('/blog/', today))
    for f in os.listdir(pins_cache):
        if f.startswith('a-'):
            shutil.copy(os.path.join(pins_cache, f), os.path.join(OUT, 'img', 'pin', f))
    return urls, items, len(live)
