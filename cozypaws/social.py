#!/usr/bin/env python3
"""Cozy Paws: publica solo en Threads, Instagram y Facebook, con las APIs oficiales de Meta (gratis, sin Claude).

Lo corre GitHub Actions (.github/workflows/cozypaws-redes.yml) dos veces por día. En cada corrida publica
UN producto nuevo (el más viejo que ya esté a la venta y todavía no se publicó) en cada red que tenga
su token cargado. Lo publicado queda anotado en data/redes-publicado.json, así nunca se repite.

Secrets de GitHub (Settings > Secrets and variables > Actions). Si falta uno, esa red se saltea sin error:
  THREADS_TOKEN                 token largo de Threads (60 días; este script lo renueva solo)
  IG_TOKEN                      token largo de Instagram con login de Instagram (60 días; se renueva solo)
  FB_PAGE_ID, FB_PAGE_TOKEN     página de Facebook (el token de página no vence)
  GH_SECRETS_PAT                token de GitHub con permiso "Secrets: write" en este repo, para guardar los tokens renovados

  python3 cozypaws/social.py publicar [--prueba]   # --prueba muestra qué publicaría, sin publicar
  python3 cozypaws/social.py renovar               # renueva los tokens de Threads e Instagram (1 vez por semana)
"""
import argparse, datetime as dt, json, os, subprocess, sys, time, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build  # noqa: E402

STATE = os.path.join(HERE, 'data', 'redes-publicado.json')
TAGS = {
    'dog': '#dogmom #doglover #dogsofinstagram #giftsfordoglovers',
    'cat': '#catmom #catlover #catsofinstagram #giftsforcatlovers',
}


def call(url, params, method='POST'):
    data = urllib.parse.urlencode(params).encode()
    if method == 'GET':
        url, data = url + '?' + data.decode(), None
    req = urllib.request.Request(url, data=data, method=method)
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode())


def caption(p, network):
    url = f"{build.CONFIG['url']}/p/{p['slug']}/"
    pet = 'cat' if ' cat' in ' ' + p['hay'] or 'kitten' in p['hay'] else 'dog'
    xmas = ' #christmasgifts' if 'christmas' in p['hay'] or 'woofmas' in p['hay'] else ''
    text = f"{p['short']} 🐾\n\n{p['texto']}\n\n"
    if network == 'instagram':  # en Instagram los links del texto no se pueden tocar
        text += 'Shop it on Etsy: link in bio (ShopCozyPaws).\n\n'
    else:
        text += f'Shop it here: {url}\n\n'
    text += TAGS[pet] + xmas + ' #cozypaws'
    return text


def post_threads(p, img, token):
    r = call('https://graph.threads.net/v1.0/me/threads', {'media_type': 'IMAGE', 'image_url': img, 'text': caption(p, 'threads'), 'access_token': token})
    time.sleep(30)  # Meta pide esperar a que procese la imagen
    return call('https://graph.threads.net/v1.0/me/threads_publish', {'creation_id': r['id'], 'access_token': token})


def post_instagram(p, img, token):
    r = call('https://graph.instagram.com/v21.0/me/media', {'image_url': img, 'caption': caption(p, 'instagram'), 'access_token': token})
    time.sleep(30)
    return call('https://graph.instagram.com/v21.0/me/media_publish', {'creation_id': r['id'], 'access_token': token})


def post_facebook(p, img, page_id, token):
    return call(f'https://graph.facebook.com/v21.0/{page_id}/photos', {'url': img, 'caption': caption(p, 'facebook'), 'access_token': token})


def publicar(prueba):
    state = json.load(open(STATE)) if os.path.exists(STATE) else {}
    hoy = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=7)).date()
    prods, _ = build.load_products(hoy)
    prods = sorted(prods, key=lambda p: (p['live'], p['sku']))
    redes = {
        'threads': (lambda p, img: post_threads(p, img, os.environ['THREADS_TOKEN'])) if os.environ.get('THREADS_TOKEN') else None,
        'instagram': (lambda p, img: post_instagram(p, img, os.environ['IG_TOKEN'])) if os.environ.get('IG_TOKEN') else None,
        'facebook': (lambda p, img: post_facebook(p, img, os.environ['FB_PAGE_ID'], os.environ['FB_PAGE_TOKEN']))
        if os.environ.get('FB_PAGE_TOKEN') and os.environ.get('FB_PAGE_ID') else None,
    }
    errores = 0
    for red, fn in redes.items():
        hechos = set(state.get(red, []))
        pend = [p for p in prods if p['sku'] not in hechos]
        if not pend:
            print(f'{red}: nada nuevo'); continue
        p = pend[0]
        img = f"{build.CONFIG['url']}/img/p/{p['sku']}.jpg"
        if prueba or fn is None:
            print(f"{red}: {'(sin token) ' if fn is None else ''}publicaría {p['sku']} · {p['short']}\n---\n{caption(p, red)}\n---")
            continue
        try:
            fn(p, img)
            state.setdefault(red, []).append(p['sku'])
            print(f'{red}: publicado {p["sku"]}')
        except Exception as e:  # el error queda en el log y el workflow falla: GitHub le manda mail a Azu
            errores += 1
            body = getattr(e, 'read', lambda: b'')().decode(errors='ignore')
            print(f'{red}: ERROR con {p["sku"]}: {e} {body[:400]}')
    if not prueba:
        json.dump(state, open(STATE, 'w'), indent=1, sort_keys=True)
    return errores


def renovar():
    pat = os.environ.get('GH_SECRETS_PAT')
    nuevos = {}
    if os.environ.get('THREADS_TOKEN'):
        r = call('https://graph.threads.net/refresh_access_token', {'grant_type': 'th_refresh_token', 'access_token': os.environ['THREADS_TOKEN']}, 'GET')
        nuevos['THREADS_TOKEN'] = r['access_token']
    if os.environ.get('IG_TOKEN'):
        r = call('https://graph.instagram.com/refresh_access_token', {'grant_type': 'ig_refresh_token', 'access_token': os.environ['IG_TOKEN']}, 'GET')
        nuevos['IG_TOKEN'] = r['access_token']
    for k, v in nuevos.items():
        if not pat:
            print(f'{k}: renovado pero falta GH_SECRETS_PAT para guardarlo'); continue
        subprocess.run(['gh', 'secret', 'set', k, '--body', v], check=True, env=dict(os.environ, GH_TOKEN=pat))
        print(f'{k}: renovado y guardado')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('accion', choices=['publicar', 'renovar'])
    ap.add_argument('--prueba', action='store_true')
    a = ap.parse_args()
    if a.accion == 'publicar':
        sys.exit(1 if publicar(a.prueba) else 0)
    renovar()
