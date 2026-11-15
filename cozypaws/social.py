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
  python3 cozypaws/social.py contenido [--prueba] # 1 post que no es de venta (banco de cozypaws/contenido.py) en IG y FB
  python3 cozypaws/social.py historia [--prueba]  # 1 historia en IG y FB (producto nuevo o tarjeta del banco)
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
    # solo productos cuya página ya está en la web publicada (el post lleva ese link)
    prods = [p for p in prods if os.path.exists(os.path.join(HERE, 'site', 'p', p['slug'], 'index.html'))]
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


# ---------------------------------------------------------------- posts que no son de venta e historias
def ig_imagen(img, cap, ig_user, token, story=False):
    params = {'image_url': img, 'access_token': token}
    params.update({'media_type': 'STORIES'} if story else {'caption': cap})
    r = call(f'{FB}/{ig_user}/media', params)
    esperar(FB, r['id'], token)
    return call(f'{FB}/{ig_user}/media_publish', {'creation_id': r['id'], 'access_token': token})


def fb_historia(img, page_id, token):
    foto = call(f'{FB}/{page_id}/photos', {'url': img, 'published': 'false', 'access_token': token})
    return call(f'{FB}/{page_id}/photo_stories', {'photo_id': foto['id'], 'access_token': token})


def en_web(rel):
    return os.path.exists(os.path.join(HERE, 'site', rel))


def siguiente(items, hechos):
    """El primero del banco que esa red todavía no publicó; si ya salieron todos, vuelve a empezar."""
    pend = [it for it in items if it['id'] not in hechos]
    return (pend[0], False) if pend else (items[0], True) if items else (None, False)


def correr(tipo, prueba):
    """tipo 'contenido': 1 post del banco (tips, frases, Social Club, preguntas) en Instagram y Facebook.
    tipo 'historia': 1 historia en Instagram y Facebook: el producto nuevo más viejo que todavía no tuvo historia,
    y si no hay ninguno, una tarjeta del banco en formato historia."""
    import contenido
    state = json.load(open(STATE)) if os.path.exists(STATE) else {}
    env = os.environ.get
    url = build.CONFIG['url']
    banco = [it for it in contenido.BANCO if en_web(f"img/social/{it['id']}.jpg")]
    hoy = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=7)).date()
    prods = sorted(build.load_products(hoy)[0], key=lambda p: (p['live'], p['sku']))
    prods = [p for p in prods if en_web(f"img/story/{p['sku']}.jpg")]
    hay_ig, hay_fb = env('IG_USER_ID') and env('FB_PAGE_TOKEN'), env('FB_PAGE_ID') and env('FB_PAGE_TOKEN')
    redes = {
        'instagram': hay_ig and (lambda img, cap: ig_imagen(img, cap, env('IG_USER_ID'), env('FB_PAGE_TOKEN'), tipo == 'historia')),
        'facebook': hay_fb and ((lambda img, cap: fb_historia(img, env('FB_PAGE_ID'), env('FB_PAGE_TOKEN'))) if tipo == 'historia'
                                else (lambda img, cap: call(f"{FB}/{env('FB_PAGE_ID')}/photos", {'url': img, 'caption': cap, 'access_token': env('FB_PAGE_TOKEN')}))),
    }
    errores = 0
    for red, fn in redes.items():
        clave_p, clave_b = f'historia-{red}', f'{tipo}-banco-{red}'
        p = next((p for p in prods if p['sku'] not in state.get(clave_p, [])), None) if tipo == 'historia' else None
        if p:
            img, cap, nombre = f"{url}/img/story/{p['sku']}.jpg", '', p['sku']
        else:
            it, reinicio = siguiente(banco, set(state.get(clave_b, [])))
            if not it:
                print(f'{red}: no hay imágenes del banco en la web todavía'); continue
            sufijo = '-story' if tipo == 'historia' else ''
            img, cap, nombre = f"{url}/img/social/{it['id']}{sufijo}.jpg", contenido.caption_de(it), it['id']
        if prueba or not fn:
            print(f"{red}: {'(sin token) ' if not fn else ''}{tipo}: publicaría {nombre} {img}\n{cap}\n---")
            continue
        try:
            fn(img, cap)
            if p:
                state.setdefault(clave_p, []).append(p['sku'])
            else:
                state[clave_b] = ([] if reinicio else state.get(clave_b, [])) + [it['id']]
            print(f'{red}: {tipo} publicado {nombre}')
        except Exception as e:
            errores += 1
            print(f"{red}: ERROR {tipo} {nombre}: {e} {getattr(e, 'read', lambda: b'')().decode(errors='ignore')[:400]}")
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



def asegurar_token_de_pagina():
    """Si FB_PAGE_TOKEN es un token de usuario (no de página), pide a Meta el token de la página y usa ese.
    Facebook exige token de página para publicar y leer posts; Instagram funciona con cualquiera de los dos."""
    page, tok = os.environ.get('FB_PAGE_ID'), os.environ.get('FB_PAGE_TOKEN')
    if not (page and tok):
        return
    try:
        url = f"https://graph.facebook.com/v21.0/{page}?" + urllib.parse.urlencode({'fields': 'access_token', 'access_token': tok})
        with urllib.request.urlopen(url, timeout=60) as r:
            nuevo = json.loads(r.read().decode()).get('access_token')
        if nuevo and nuevo != tok:
            os.environ['FB_PAGE_TOKEN'] = nuevo
            print('FB_PAGE_TOKEN era de usuario: se usa el token de la página')
    except Exception as e:
        print(f'no se pudo pedir el token de la página: {e}')

if __name__ == '__main__':
    asegurar_token_de_pagina()
    ap = argparse.ArgumentParser()
    ap.add_argument('accion', choices=['publicar', 'contenido', 'historia', 'renovar', 'revisar'])
    ap.add_argument('--prueba', action='store_true')
    a = ap.parse_args()
    if a.accion == 'publicar':
        sys.exit(1 if publicar(a.prueba) else 0)
    if a.accion in ('contenido', 'historia'):
        sys.exit(1 if correr(a.accion, a.prueba) else 0)
    if a.accion == 'revisar':
        sys.exit(1 if revisar() else 0)
    renovar()
