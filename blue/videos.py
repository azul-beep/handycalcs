"""Blue en Automático: publica sola los reels de Blue en Instagram (API oficial de Meta, gratis, sin Claude).

Dónde está cada cosa:
  - Este programa y el workflow (.github/workflows/blue-instagram.yml) viven en main.
  - Los videos que esperan salir viven en la rama "blue-videos" (un solo commit que se rehace cada vez,
    así el repo no engorda): cola.json + los .mp4 + publicado.json (historial).
  - Cuando un video sale, se borra de la rama y queda anotado en publicado.json.

Comandos:
  python3 blue/videos.py publicar            publica el próximo video de la cola (si su fecha ya llegó)
  python3 blue/videos.py revisar             prueba la clave y cuenta los videos en cola, sin publicar
  python3 blue/videos.py agregar CARPETA     suma a la cola todos los .mp4 de CARPETA con su texto
                                             (CARPETA/textos.json: {"v01.mp4": {"texto": "...", "fecha": "2026-11-23"}})
  --prueba                                   no publica ni empuja nada (muestra lo que haría)

Secretos (los pega Azu una vez en GitHub > Settings > Secrets > Actions):
  BLUE_IG_USER_ID   id de la cuenta de Instagram de Blue (cuenta profesional conectada a una página de Facebook)
  BLUE_FB_TOKEN     token de la página de Facebook de Blue (de los que no vencen, igual que Cozy Paws)
Sin secretos: termina en verde sin publicar.
"""
import datetime as dt
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request

FB = 'https://graph.facebook.com/v21.0'
RUPLOAD = 'https://rupload.facebook.com/ig-api-upload/v21.0'
RAMA = 'blue-videos'
AVISAR_SI_QUEDAN = 4  # menos de esto en cola -> issue "Blue: quedan pocos videos"
PIE_IA = '\n\n🤖 Personaje y voz hechos con IA.'
PRUEBA = '--prueba' in sys.argv


def call(url, params, method='POST'):
    data = urllib.parse.urlencode(params).encode()
    if method == 'GET':
        url, data = url + '?' + data.decode(), None
    req = urllib.request.Request(url, data=data, method=method)
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f'Meta respondió {e.code}: {e.read().decode()[:400]}') from None


def git(*args, cwd=None, check=True):
    return subprocess.run(['git', *args], cwd=cwd, check=check, capture_output=True, text=True).stdout.strip()


def abrir_rama():
    """Baja la rama de videos a una carpeta temporal. Devuelve (carpeta, sha) o (carpeta, None) si no existe."""
    d = tempfile.mkdtemp(prefix='blue-')
    remoto = git('remote', 'get-url', 'origin')
    git('init', '-q', cwd=d)
    git('remote', 'add', 'origin', remoto, cwd=d)
    for k in ('http.https://github.com/.extraheader',):  # credenciales del checkout de Actions
        v = git('config', '--get', k, check=False)
        if v:
            git('config', k, v, cwd=d)
    if git('ls-remote', 'origin', RAMA, cwd=d):
        git('fetch', '-q', '--depth=1', 'origin', RAMA, cwd=d)
        git('checkout', '-q', 'FETCH_HEAD', cwd=d)
        return d, git('rev-parse', 'HEAD', cwd=d)
    return d, None


def leer(d, nombre, defecto):
    p = os.path.join(d, nombre)
    return json.load(open(p, encoding='utf-8')) if os.path.exists(p) else defecto


def guardar_rama(d, sha_previo, mensaje):
    """Rehace la rama como un único commit nuevo (sin historia) y lo empuja solo si nadie la cambió mientras tanto."""
    git('config', 'user.name', 'publicacion-bot', cwd=d)
    git('config', 'user.email', 'publicacion-bot@users.noreply.github.com', cwd=d)
    git('checkout', '-q', '--orphan', 'nueva', cwd=d)
    git('add', '-A', cwd=d)
    git('commit', '-q', '-m', mensaje, cwd=d)
    if PRUEBA:
        print('(prueba) no empujo la rama')
        return True
    lease = f'--force-with-lease={RAMA}:{sha_previo or ""}'
    r = subprocess.run(['git', 'push', '-q', lease, 'origin', f'HEAD:refs/heads/{RAMA}'], cwd=d, capture_output=True, text=True)
    return r.returncode == 0


def hoy_utah():
    return (dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=7)).date().isoformat()


def proximo(cola):
    hoy = hoy_utah()
    for it in cola:
        if not it.get('fecha') or it['fecha'] <= hoy:
            return it
    return None


def subir_reel(ruta, texto, ig_user, token):
    """Subida reanudable: Meta no necesita que el video esté en una web pública."""
    c = call(f'{FB}/{ig_user}/media', {'media_type': 'REELS', 'upload_type': 'resumable', 'caption': texto,
                                         'share_to_feed': 'true', 'access_token': token})
    cid = c['id']
    datos = open(ruta, 'rb').read()
    req = urllib.request.Request(f'{RUPLOAD}/{cid}', data=datos, method='POST', headers={
        'Authorization': f'OAuth {token}', 'offset': '0', 'file_size': str(len(datos))})
    try:
        with urllib.request.urlopen(req, timeout=600) as r:
            r.read()
    except urllib.error.HTTPError as e:
        raise RuntimeError(f'Meta no aceptó el video: {e.code} {e.read().decode()[:400]}') from None
    for _ in range(40):  # hasta ~10 minutos procesando
        time.sleep(15)
        st = call(f'{FB}/{cid}', {'fields': 'status_code,status', 'access_token': token}, 'GET')
        if st.get('status_code') == 'FINISHED':
            break
        if st.get('status_code') in ('ERROR', 'EXPIRED'):
            raise RuntimeError(f'Meta no pudo procesar el video: {st}')
    else:
        raise RuntimeError('Meta tardó más de 10 minutos en procesar el video')
    return call(f'{FB}/{ig_user}/media_publish', {'creation_id': cid, 'access_token': token})['id']


def avisar_pocos(quedan):
    if PRUEBA or quedan >= AVISAR_SI_QUEDAN or not os.environ.get('GH_TOKEN'):
        return
    abiertos = subprocess.run(['gh', 'issue', 'list', '--label', 'blue', '--state', 'open', '--json', 'number', '--jq', 'length'],
                              capture_output=True, text=True).stdout.strip()
    if abiertos and abiertos != '0':
        return
    subprocess.run(['gh', 'label', 'create', 'blue', '--color', '1d76db', '--force'], capture_output=True)
    subprocess.run(['gh', 'issue', 'create', '--label', 'blue', '--title', f'🎬 Blue: quedan {quedan} videos en la cola',
                    '--body', 'La cuenta de Blue publica 2 videos por día. Hace falta una tanda nueva '
                              '(pedirla en el hilo de Blue). Este aviso se cierra solo cuando la cola vuelve a tener videos.'])


def cerrar_aviso():
    if PRUEBA or not os.environ.get('GH_TOKEN'):
        return
    nums = subprocess.run(['gh', 'issue', 'list', '--label', 'blue', '--state', 'open', '--json', 'number', '--jq', '.[].number'],
                          capture_output=True, text=True).stdout.split()
    for n in nums:
        subprocess.run(['gh', 'issue', 'close', n, '--comment', 'La cola volvió a tener videos.'], capture_output=True)


def publicar():
    ig_user, token = os.environ.get('BLUE_IG_USER_ID'), os.environ.get('BLUE_FB_TOKEN')
    if not (ig_user and token):
        print('Blue todavía no tiene cuenta conectada (faltan BLUE_IG_USER_ID y BLUE_FB_TOKEN): no publico nada.')
        return
    media_id = None
    hecho = None  # video ya publicado en un intento anterior (solo falta guardarlo)
    for intento in range(3):
        d, sha = abrir_rama()
        cola = leer(d, 'cola.json', [])
        it = next((x for x in cola if x['video'] == hecho), None) if hecho else proximo(cola)
        if hecho and not it:
            print(f'{hecho} ya no está en la cola: nada que guardar.')
            return
        if not it:
            print(f'Nada para hoy ({len(cola)} en cola con fecha más adelante o cola vacía).')
            avisar_pocos(len(cola))
            return
        ruta = os.path.join(d, it['video'])
        if PRUEBA:
            print(f"(prueba) publicaría {it['video']}: {it['texto'][:80]}...")
            return
        if not hecho:
            media_id = subir_reel(ruta, it['texto'] + PIE_IA, ig_user, token)
            hecho = it['video']
            print(f"Publicado {it['video']} (media {media_id})")
        hechos = leer(d, 'publicado.json', [])
        hechos.append({'video': it['video'], 'texto': it['texto'][:120], 'media_id': media_id,
                       'cuando': dt.datetime.now(dt.timezone.utc).isoformat(timespec='minutes')})
        cola = [x for x in cola if x['video'] != it['video']]
        if os.path.exists(ruta):
            os.remove(ruta)
        json.dump(cola, open(os.path.join(d, 'cola.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
        json.dump(hechos, open(os.path.join(d, 'publicado.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
        if guardar_rama(d, sha, f"Blue: publicado {it['video']}"):
            avisar_pocos(len(cola))
            return
        print('La rama cambió mientras publicaba (llegaron videos nuevos): vuelvo a intentar guardar.')
        shutil.rmtree(d, ignore_errors=True)
        # en el reintento no se vuelve a publicar: se reaplica solo el borrado
    raise RuntimeError('Publiqué pero no pude actualizar la cola: revisar la rama blue-videos a mano')


def revisar():
    d, sha = abrir_rama()
    cola = leer(d, 'cola.json', [])
    print(f'Rama {RAMA}: {"no existe todavía" if not sha else sha[:7]}; {len(cola)} videos en cola; próximo: '
          f'{(proximo(cola) or {}).get("video", "ninguno para hoy")}')
    faltan = [x['video'] for x in cola if not os.path.exists(os.path.join(d, x['video']))]
    if faltan:
        raise RuntimeError(f'En cola.json pero sin archivo: {faltan}')
    ig_user, token = os.environ.get('BLUE_IG_USER_ID'), os.environ.get('BLUE_FB_TOKEN')
    if ig_user and token:
        r = call(f'{FB}/{ig_user}', {'fields': 'username,media_count', 'access_token': token}, 'GET')
        print(f"Clave OK: @{r.get('username')} ({r.get('media_count')} publicaciones)")
    else:
        print('Sin secretos de Instagram todavía.')
    if cola:
        cerrar_aviso()


def agregar(carpeta):
    textos = json.load(open(os.path.join(carpeta, 'textos.json'), encoding='utf-8'))
    for intento in range(3):
        d, sha = abrir_rama()
        cola = leer(d, 'cola.json', [])
        ya = {x['video'] for x in cola} | {x['video'] for x in leer(d, 'publicado.json', [])}
        nuevos = 0
        for nombre, info in sorted(textos.items()):
            if nombre in ya:
                print(f'{nombre}: ya estaba, lo salteo')
                continue
            if os.path.getsize(os.path.join(carpeta, nombre)) > 95 * 1024 * 1024:
                raise RuntimeError(f'{nombre} pesa más de 95 MB (GitHub no lo acepta)')
            shutil.copy(os.path.join(carpeta, nombre), os.path.join(d, nombre))
            cola.append({'video': nombre, 'texto': info['texto'], **({'fecha': info['fecha']} if info.get('fecha') else {})})
            nuevos += 1
        json.dump(cola, open(os.path.join(d, 'cola.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
        if not os.path.exists(os.path.join(d, 'publicado.json')):
            json.dump([], open(os.path.join(d, 'publicado.json'), 'w'))
        if guardar_rama(d, sha, f'Blue: {nuevos} videos nuevos en cola'):
            print(f'Listo: {nuevos} videos nuevos, {len(cola)} en cola.')
            return
        shutil.rmtree(d, ignore_errors=True)
    raise RuntimeError('No pude empujar la rama blue-videos')


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    cmd = args[0] if args else 'publicar'
    {'publicar': publicar, 'revisar': revisar}.get(cmd, lambda: agregar(args[1]))()
