#!/usr/bin/env python3
"""Cozy Paws: publica solo en Threads, Instagram y Facebook, con las APIs oficiales de Meta (gratis, sin Claude).

Lo corre GitHub Actions (.github/workflows/cozypaws-redes.yml) dos veces por día. En cada corrida publica
UN producto nuevo (el más viejo que ya esté a la venta y todavía no se publicó) en cada red que tenga
su token cargado. Lo publicado queda anotado en data/redes-publicado.json, así nunca se repite.

Secrets de GitHub (Settings > Secrets and variables > Actions). Si falta uno, esa red se saltea sin error:
  THREADS_TOKEN                 token largo de Threads (60 días; este script lo renueva solo los lunes)
  FB_PAGE_ID, FB_PAGE_TOKEN     página de Facebook y su token de página largo (no vence)
  IG_USER_ID                    id de la cuenta de Instagram profesional vinculada a esa página. Instagram se publica
                                por graph.facebook.com con el mismo FB_PAGE_TOKEN (no hace falta un token aparte)
  GH_SECRETS_PAT                token de GitHub con permiso "Secrets: write" en este repo, para guardar el token renovado

  python3 cozypaws/social.py publicar [--prueba]   # --prueba muestra qué publicaría, sin publicar
  python3 cozypaws/social.py renovar               # renueva el token de Threads (1 vez por semana)
  python3 cozypaws/social.py revisar               # comprueba que cada token funcione, sin publicar nada
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


FB = 'https://graph.facebook.com/v21.0'


def esperar(base, cid, token):
    """Meta procesa la imagen antes de dejar publicar: espera hasta que el contenedor esté listo (máx. ~3 min)."""
    for _ in range(12):
        time.sleep(15)
        st = call(f'{base}/{cid}', {'fields': 'status_code' if 'facebook' in base else 'status', 'access_token': token}, 'GET')
        estado = st.get('status_code') or st.get('status')
        if estado == 'FINISHED':
            return
        if estado in ('ERROR', 'EXPIRED'):
            raise RuntimeError(f'Meta no pudo procesar la imagen: {st}')
    raise RuntimeError('Meta tardó demasiado en procesar la imagen')


def post_threads(p, img, token):
    base = 'https://graph.threads.net/v1.0'
    r = call(f'{base}/me/threads', {'media_type': 'IMAGE', 'image_url': img, 'text': caption(p, 'threads'), 'access_token': token})
    esperar(base, r['id'], token)
    return call(f'{base}/me/threads_publish', {'creation_id': r['id'], 'access_token': token})


def post_instagram(p, img, ig_user, token):
    r = call(f'{FB}/{ig_user}/media', {'image_url': img, 'caption': caption(p, 'instagram'), 'access_token': token})
    esperar(FB, r['id'], token)
    return call(f'{FB}/{ig_user}/media_publish', {'creation_id': r['id'], 'access_token': token})


def post_facebook(p, img, page_id, token):
    return call(f'{FB}/{page_id}/photos', {'url': img, 'caption': caption(p, 'facebook'), 'access_token': token})


def publicar(prueba):
    state = json.load(open(STATE)) if os.path.exists(STATE) else {}
    hoy = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=7)).date()
    prods, _ = build.load_products(hoy)
    prods = sorted(prods, key=lambda p: (p['live'], p['sku']))
    redes = {
        'threads': (lambda p, img: post_threads(p, img, os.environ['THREADS_TOKEN'])) if os.environ.get('THREADS_TOKEN') else None,
        'instagram': (lambda p, img: post_instagram(p, img, os.environ['IG_USER_ID'], os.environ['FB_PAGE_TOKEN']))
        if os.environ.get('IG_USER_ID') and os.environ.get('FB_PAGE_TOKEN') else None,
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
    for k, v in nuevos.items():
        if not pat:
            print(f'{k}: renovado pero falta GH_SECRETS_PAT para guardarlo'); continue
        subprocess.run(['gh', 'secret', 'set', k, '--body', v], check=True, env=dict(os.environ, GH_TOKEN=pat))
        print(f'{k}: renovado y guardado')


def revisar():
    """Comprueba cada token (no publica). Sirve después de cargar los secrets en GitHub."""
    env, mal = os.environ.get, 0
    pruebas = [
        ('threads', env('THREADS_TOKEN'), lambda: call('https://graph.threads.net/v1.0/me', {'fields': 'username', 'access_token': env('THREADS_TOKEN')}, 'GET')['username']),
        ('facebook', env('FB_PAGE_TOKEN') and env('FB_PAGE_ID'), lambda: call(f"{FB}/{env('FB_PAGE_ID')}", {'fields': 'name', 'access_token': env('FB_PAGE_TOKEN')}, 'GET')['name']),
        ('instagram', env('FB_PAGE_TOKEN') and env('IG_USER_ID'), lambda: call(f"{FB}/{env('IG_USER_ID')}", {'fields': 'username', 'access_token': env('FB_PAGE_TOKEN')}, 'GET')['username']),
    ]
    for red, hay, fn in pruebas:
        if not hay:
            print(f'{red}: falta el secret, se saltea'); continue
        try:
            print(f'{red}: OK, publica como {fn()}')
        except Exception as e:
            mal += 1
            print(f"{red}: ERROR {e} {getattr(e, 'read', lambda: b'')().decode(errors='ignore')[:400]}")
    return mal


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('accion', choices=['publicar', 'renovar', 'revisar'])
    ap.add_argument('--prueba', action='store_true')
    a = ap.parse_args()
    if a.accion == 'publicar':
        sys.exit(1 if publicar(a.prueba) else 0)
    if a.accion == 'revisar':
        sys.exit(1 if revisar() else 0)
    renovar()
