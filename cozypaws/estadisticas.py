#!/usr/bin/env python3
"""Cozy Paws: estadísticas de Instagram y Facebook todos los días, gratis y sin Claude (GitHub Actions + Graph API de Meta).

Escribe:
  cozypaws/estadisticas/redes.md          resumen legible (seguidores, alcance, últimos posts, comentarios nuevos)
  cozypaws/estadisticas/redes-historial.csv  una fila por día con los números de la cuenta (para ver cómo crecen)

Usa los mismos secrets que social.py: FB_PAGE_ID, FB_PAGE_TOKEN, IG_USER_ID.
Si al token le falta un permiso, el dato se saltea y el archivo dice qué permiso agregar.
  python3 cozypaws/estadisticas.py
"""
import csv, datetime as dt, io, json, os, urllib.error, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get('STATS_DIR') or os.path.join(HERE, 'estadisticas')  # Blue usa blue/estadisticas
FB = 'https://graph.facebook.com/v21.0'
env = os.environ.get
faltan = {}  # permiso -> qué dato necesita
notas = []  # errores crudos de Meta (para entender qué pasó)


def get(path, **params):
    params['access_token'] = env('FB_PAGE_TOKEN')
    url = f'{FB}/{path}?{urllib.parse.urlencode(params)}'
    with urllib.request.urlopen(url, timeout=60) as r:
        return json.loads(r.read().decode())


def probar(permiso, que, fn, defecto=None):
    """Corre fn; si Meta dice que falta un permiso, lo anota y sigue."""
    try:
        return fn()
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors='ignore')
        try:
            err = json.loads(body).get('error', {})
        except ValueError:
            err = {'message': body[:200]}
        msg = err.get('message', '')
        notas.append(f"{que}: código {err.get('code')} · {msg[:180]}")
        if err.get('code') in (200, 190) or 'permission' in msg.lower() and 'Public Content Access' not in msg:
            faltan.setdefault(permiso, set()).add(que)
        print(f'{que}: {msg[:200]}')
        return defecto
    except Exception as e:
        print(f'{que}: {e}')
        return defecto


def valor_insight(data):
    out = {}
    for m in data.get('data', []):
        if 'total_value' in m:
            out[m['name']] = m['total_value'].get('value')
        elif m.get('values'):
            out[m['name']] = m['values'][-1].get('value')
    return out


def metricas(path, opciones, **params):
    """Pide cada métrica por separado y usa la primera variante que Meta acepte (algunas se renombraron)."""
    out = {}
    for nombre, variantes in opciones.items():
        for v in variantes:
            try:
                d = valor_insight(get(path, metric=v, **params))
                if v in d:
                    out[nombre] = d[v]
                    break
            except urllib.error.HTTPError as e:
                body = e.read().decode(errors='ignore')
                try:
                    code = json.loads(body).get('error', {}).get('code')
                except ValueError:
                    code = None
                if code in (10, 200, 210, 190):
                    raise urllib.error.HTTPError(e.url, e.code, e.msg, e.hdrs, io.BytesIO(body.encode()))
    return out


def instagram():
    ig = env('IG_USER_ID')
    if not ig:
        return None
    cuenta = probar('instagram_basic', 'datos de la cuenta de Instagram',
                    lambda: get(ig, fields='username,followers_count,follows_count,media_count'), {})
    hasta = int(dt.datetime.now(dt.timezone.utc).timestamp())
    desde = hasta - 86400
    ins = probar('instagram_manage_insights', 'alcance y visitas de la cuenta de Instagram',
                 lambda: valor_insight(get(f'{ig}/insights', metric='reach,profile_views,accounts_engaged,website_clicks,profile_links_taps',
                                           period='day', metric_type='total_value', since=desde, until=hasta)), {})
    media = probar('instagram_basic', 'posts de Instagram',
                   lambda: get(f'{ig}/media', fields='id,caption,media_type,timestamp,permalink,like_count,comments_count', limit=12).get('data', []), [])
    for m in media:
        m['insights'] = probar('instagram_manage_insights', 'alcance de cada post de Instagram',
                               lambda m=m: valor_insight(get(f"{m['id']}/insights", metric='reach,saved,shares,total_interactions')), {})
        if m.get('comments_count'):
            m['comentarios'] = probar('instagram_manage_comments', 'texto de los comentarios de Instagram',
                                      lambda m=m: get(f"{m['id']}/comments", fields='text,username,timestamp', limit=10).get('data', []), [])
    return dict(cuenta=cuenta, insights=ins, media=media)


def facebook():
    page = env('FB_PAGE_ID')
    if not page:
        return None
    cuenta = probar('pages_read_engagement', 'datos de la página de Facebook',
                    lambda: get(page, fields='name,followers_count,fan_count,link'), {})
    ins = probar('read_insights', 'alcance de la página de Facebook',
                 lambda: metricas(f'{page}/insights', {
                     'alcance': ['page_total_media_view_unique', 'page_impressions_unique'],
                     'vistas': ['page_media_view', 'page_impressions'],
                     'interacciones': ['page_post_engagements'],
                     'visitas': ['page_views_total']}, period='day'), {})
    campos = 'id,message,created_time,permalink_url,shares,reactions.summary(true).limit(0),comments.summary(true).limit(0)'

    def leer_posts():
        try:  # /posts alcanza con pages_read_engagement; /published_posts pide además pages_read_user_content
            return get(f'{page}/posts', fields=campos, limit=10).get('data', [])
        except urllib.error.HTTPError:
            pass
        try:
            return get(f'{page}/published_posts', fields=campos, limit=10).get('data', [])
        except urllib.error.HTTPError:
            pass
        # Sin pages_read_user_content: los posts de la tienda son fotos, y /photos las lista igual.
        fotos = get(f'{page}/photos', type='uploaded', fields='id,name,created_time,link,page_story_id', limit=10).get('data', [])
        posts = []
        for f in fotos:
            pid = f.get('page_story_id') or f['id']
            try:
                posts.append(get(pid, fields=campos))
            except urllib.error.HTTPError:
                posts.append({'id': pid, 'message': f.get('name'), 'created_time': f.get('created_time'), 'permalink_url': f.get('link')})
        return posts
    posts = probar('pages_read_engagement', 'posts de Facebook', leer_posts, [])
    for p in posts:
        p['insights'] = probar('read_insights', 'alcance y clics de cada post de Facebook',
                               lambda p=p: metricas(f"{p['id']}/insights", {
                                   'alcance': ['post_total_media_view_unique', 'post_impressions_unique'],
                                   'clics': ['post_clicks']}), {})
        if p.get('comments', {}).get('summary', {}).get('total_count'):
            p['comentarios'] = probar('pages_read_user_content', 'texto de los comentarios de Facebook',
                                      lambda p=p: get(f"{p['id']}/comments", fields='message,created_time,from', limit=10).get('data', []), [])
    return dict(cuenta=cuenta, insights=ins, posts=posts)


def corto(t, n=70):
    t = (t or '').replace('\n', ' ').replace('|', '/').strip()
    return t if len(t) <= n else t[:n - 1] + '…'


def n(v):
    return '-' if v is None else str(v)


def main():
    hoy = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=7))
    ig, fb = instagram(), facebook()
    L = [f"# Cozy Paws en redes ({hoy:%d %b %Y}, {hoy:%H:%M} hora de Utah)", '',
         'Lo arma solo GitHub Actions todos los días (cozypaws/estadisticas.py). "Ayer" = últimas 24 horas. "-" = sin dato.', '']
    fila = {'fecha': hoy.date().isoformat()}
    if ig:
        c, i = ig['cuenta'], ig['insights']
        L += [f"## Instagram @{c.get('username', '?')}", '',
              f"1. Seguidores: {n(c.get('followers_count'))} · sigue a {n(c.get('follows_count'))} · posts: {n(c.get('media_count'))}",
              f"2. Ayer: alcance {n(i.get('reach'))}, visitas al perfil {n(i.get('profile_views'))}, cuentas que interactuaron {n(i.get('accounts_engaged'))}, "
              f"toques en el link {n(i.get('profile_links_taps') or i.get('website_clicks'))}", '',
              '| Fecha | Post | Likes | Coment. | Alcance | Guardados | Compartidos |', '|---|---|---|---|---|---|---|']
        for m in ig['media']:
            mi = m.get('insights', {})
            L.append(f"| {m['timestamp'][:10]} | [{corto(m.get('caption'), 50) or m['media_type']}]({m['permalink']}) | {n(m.get('like_count'))} | "
                     f"{n(m.get('comments_count'))} | {n(mi.get('reach'))} | {n(mi.get('saved'))} | {n(mi.get('shares'))} |")
        coms = [(m, c) for m in ig['media'] for c in m.get('comentarios', [])]
        if coms:
            L += ['', '### Comentarios recientes en Instagram (para responder)']
            L += [f"{k}. @{c.get('username', '?')} en [{corto(m.get('caption'), 30)}]({m['permalink']}): \"{corto(c.get('text'), 120)}\""
                  for k, (m, c) in enumerate(sorted(coms, key=lambda x: x[1].get('timestamp', ''), reverse=True)[:15], 1)]
        L.append('')
        fila.update(ig_seguidores=c.get('followers_count'), ig_posts=c.get('media_count'), ig_alcance_dia=i.get('reach'),
                    ig_visitas_perfil=i.get('profile_views'), ig_toques_link=i.get('profile_links_taps') or i.get('website_clicks'))
    if fb:
        c, i = fb['cuenta'], fb['insights']
        L += [f"## Facebook: {c.get('name', '?')}", '',
              f"1. Seguidores: {n(c.get('followers_count'))} · me gusta: {n(c.get('fan_count'))}",
              f"2. Ayer: alcance {n(i.get('alcance'))}, vistas {n(i.get('vistas'))}, interacciones {n(i.get('interacciones'))}, visitas a la página {n(i.get('visitas'))}", '',
              '| Fecha | Post | Reacciones | Coment. | Compartidos | Alcance | Clics |', '|---|---|---|---|---|---|---|']
        coms = []
        for p in fb['posts']:
            pi = p.get('insights', {})
            L.append(f"| {p['created_time'][:10]} | [{corto(p.get('message'), 50) or 'foto'}]({p.get('permalink_url', '')}) | "
                     f"{n(p.get('reactions', {}).get('summary', {}).get('total_count'))} | {n(p.get('comments', {}).get('summary', {}).get('total_count'))} | "
                     f"{n(p.get('shares', {}).get('count', 0))} | {n(pi.get('alcance'))} | {n(pi.get('clics'))} |")
            coms += [(p, cm) for cm in p.get('comentarios', [])]
        if coms:
            L += ['', '### Comentarios recientes en Facebook (para responder)']
            L += [f"{k}. {cm.get('from', {}).get('name', 'alguien')}: \"{corto(cm.get('message'), 120)}\" ([post]({p.get('permalink_url', '')}))"
                  for k, (p, cm) in enumerate(sorted(coms, key=lambda x: x[1].get('created_time', ''), reverse=True)[:15], 1)]
        L.append('')
        fila.update(fb_seguidores=c.get('followers_count'), fb_alcance_dia=i.get('alcance'))
    if not ig and not fb:
        L += ['Faltan los secrets FB_PAGE_TOKEN, FB_PAGE_ID o IG_USER_ID en GitHub.', '']
    if faltan:
        L += ['## Permisos que le faltan al token', '',
              'Para ver estos datos hay que generar el token de la página de nuevo (pasos A del plan de redes) sumando estos permisos:', '']
        L += [f"{k}. `{perm}`: {', '.join(sorted(q))}" for k, (perm, q) in enumerate(sorted(faltan.items()), 1)]
        L.append('')
    if notas:
        L += ['## Respuestas de Meta que no fueron datos (para revisar)', '']
        L += [f'{k}. {x}' for k, x in enumerate(dict.fromkeys(notas), 1)]
        L.append('')
    os.makedirs(OUT, exist_ok=True)
    open(os.path.join(OUT, 'redes.md'), 'w').write('\n'.join(L))
    hist = os.path.join(OUT, 'redes-historial.csv')
    cols = ['fecha', 'ig_seguidores', 'ig_posts', 'ig_alcance_dia', 'ig_visitas_perfil', 'ig_toques_link', 'fb_seguidores', 'fb_alcance_dia']
    filas = list(csv.DictReader(open(hist))) if os.path.exists(hist) else []
    filas = [f for f in filas if f['fecha'] != fila['fecha']] + [{k: fila.get(k, '') for k in cols}]
    w = csv.DictWriter(open(hist, 'w', newline=''), fieldnames=cols)
    w.writeheader(); w.writerows(filas)
    print('\n'.join(L))



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
    main()
