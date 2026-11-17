"""Carrusel de Instagram/Facebook para cada artículo del blog de Cozy Paws (17 nov 2026, pedido de Azu).

Saca los consejos del propio artículo (viñetas en negrita o títulos numerados) y usa el mismo
diseño de carruseles.py. Última lámina: "Read the full guide" con el link del blog.
Salida: site/img/carrusel-blog/<slug>/N.jpg + texto.txt. Lo llama build.py para los artículos ya publicados;
se programan desde el planificador de Meta (la API de Meta está sin permiso).

  python3 cozypaws/carruseles_blog.py [carpeta_salida]
"""
import html, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import carruseles as C

MAX_ITEMS, MIN_ITEMS = 6, 3
SALUD = ('vet', 'toxic', 'vaccine', 'flea', 'feed', 'food', 'paw')


def _limpio(s):
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', s))).strip()


def _frase(s, maximo=115):
    s = _limpio(s)
    for corte in re.split(r'(?<=[.!?])\s+', s)[:2]:
        if 20 <= len(corte) <= maximo:
            return corte
    if len(s) <= maximo:
        return s
    partes = re.split(r'(?<=[.!?])\s+', s)
    if len(partes) > 1 and len(partes[0]) < 20:
        s = ' '.join(partes[1:])
    corte = s[:maximo]
    for sep in ('; ', ', ', ': ', ' (', ' - '):
        i = corte.rfind(sep)
        if i > 40:
            return corte[:i].rstrip(' ,;:(') + '.'
    return corte[:corte.rfind(' ')] + '.'


def _arreglar(t, d):
    d = d.strip(' :,;')
    if d:
        d = d[0].upper() + d[1:]
        if d[-1] not in '.!?':
            d += '.'
    return t, d


def consejos(body):
    """Consejos del artículo: viñetas con título en negrita o, si no alcanzan, los subtítulos <h2>."""
    vinetas, titulos = [], []
    for m in re.finditer(r'<li[^>]*>\s*<b>(.*?)</b>(.*?)</li>', body, re.S):
        t = _limpio(m.group(1)).rstrip('.:')
        d = _frase(m.group(2))
        if 2 <= len(t) <= 40 and len(d) >= 15:
            vinetas.append(_arreglar(t, d))
    for m in re.finditer(r'<h2[^>]*>(.*?)</h2>\s*(?:<p[^>]*>(.*?)</p>|<ul[^>]*>\s*<li[^>]*>(.*?)</li>)', body, re.S):
        t = re.sub(r'^(\d+\.|Step \d+:)\s*', '', _limpio(m.group(1)))
        d = _frase(m.group(2) or m.group(3) or '')
        if len(t) <= 48 and len(d) >= 15 and not t.lower().startswith(('do it the easy', 'how old', 'keep a simple')):
            titulos.append(_arreglar(t, d))
    items = vinetas if len(vinetas) >= 4 else titulos
    return items[:MAX_ITEMS]


def carrusel(a, url_blog):
    items = consejos(a['body'])
    if len(items) < MIN_ITEMS:
        return None
    salud = any(w in (a['slug'] + a['title']).lower() for w in SALUD)
    cap = (f"New on the blog 🐾 {a.get('pin') or a['h1']}: the key tips in one place. Save this and read the full guide on our blog (link in bio)."
           + ("\n\nGeneral information only, not veterinary advice." if salud else ''))
    return dict(id='blog-' + a['slug'], kicker='New on the blog', titulo=a.get('pin') or a['h1'], items=items,
                cierre_titulo='Read the full guide', cierre=f'On our blog: {url_blog} (link in bio)',
                caption=cap, tags='#dogmom #catmom #doglover #catlover #petcare #pettips')


def render(out_dir, articulos, url_blog='cozypawsgifts.pages.dev/blog'):
    hechos = []
    for a in articulos:
        c = carrusel(a, url_blog)
        if not c:
            print('sin consejos suficientes:', a['slug']); continue
        d = os.path.join(out_dir, a['slug'])
        os.makedirs(d, exist_ok=True)
        if not os.path.exists(os.path.join(d, '1.jpg')):
            for n, im in enumerate(C.slides(c), 1):
                im.save(os.path.join(d, f'{n}.jpg'), quality=88)
            with open(os.path.join(d, 'texto.txt'), 'w') as f:
                f.write(C.caption_de(c))
        hechos.append(a['slug'])
    return hechos


def _articulos():
    import importlib.util
    spec = importlib.util.spec_from_file_location('cozypaws_articulos', os.path.join(HERE, 'apps', 'articulos.py'))
    articulos = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(articulos)
    out = []
    for a in articulos.load():
        meta, _, body = open(os.path.join(articulos.SRC, f"{a['n']:02d}-{a['slug']}.html")).read().partition('---')
        info = dict(l.split(':', 1) for l in meta.strip().splitlines() if ':' in l)
        out.append(dict(slug=a['slug'], title=info.get('title', '').strip(), h1=info.get('h1', '').strip(),
                        pin=info.get('pin', '').strip(), live=a['live'], body=body))
    return out


if __name__ == '__main__':
    destino = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'site', 'img', 'carrusel-blog')
    print(render(destino, _articulos()))
