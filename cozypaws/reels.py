#!/usr/bin/env python3
"""Cozy Paws: aprender de los números de cada reel y juntar ideas de lo que funciona. Sin Claude (GitHub Actions).

1. Reels propios (todos los días): vistas, alcance, segundos promedio vistos, % del reel que se ve (segundos promedio
   / duración), guardados y compartidos. Arma lecciones simples comparando los mejores con los peores.
   Meta NO da por API el segundo exacto en que se va la gente (esa curva solo está en la app de Instagram).
2. Ideas (los domingos o con --ideas): los posts más populares de hashtags de mascotas en Instagram (API oficial
   de búsqueda de hashtags), con su formato y su primera línea.

Escribe cozypaws/estadisticas/reels.md, reels-historial.csv e ideas-instagram.md.
Usa FB_PAGE_TOKEN e IG_USER_ID (permisos instagram_basic e instagram_manage_insights).
"""
import csv
import datetime as dt
import os
import statistics
import subprocess
import sys
import tempfile
import urllib.request
from zoneinfo import ZoneInfo

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import estadisticas as es  # noqa: E402  (get, probar, valor_insight, permisos que faltan)

OUT = es.OUT
HIST = os.path.join(OUT, 'reels-historial.csv')
UTAH = ZoneInfo('America/Denver')
HASHTAGS = ['dachshund', 'funnydogs', 'dogsofinstagram', 'catsofinstagram', 'corgi', 'goldenretriever']
CAMPOS = ['id', 'fecha', 'hora', 'duracion_s', 'vistas', 'alcance', 'seg_promedio', 'pct_visto', 'guardados',
          'compartidos', 'likes', 'comentarios', 'texto', 'link']


def duracion(url):
    """Duración del video en segundos (ffprobe viene instalado en GitHub Actions)."""
    try:
        with tempfile.NamedTemporaryFile(suffix='.mp4') as t:
            with urllib.request.urlopen(url, timeout=120) as r:
                t.write(r.read())
            t.flush()
            s = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', t.name],
                               capture_output=True, text=True, timeout=60).stdout.strip()
            return round(float(s), 1)
    except Exception as e:  # noqa: BLE001
        print(f'sin duración: {e}')
        return None


def insights_reel(mid):
    for metricas in ('reach,views,saved,shares,total_interactions,ig_reels_avg_watch_time',
                     'reach,plays,saved,shares,total_interactions,ig_reels_avg_watch_time',
                     'reach,saved,shares,total_interactions'):
        d = es.probar('instagram_manage_insights', 'números de cada reel',
                      lambda: es.valor_insight(es.get(f'{mid}/insights', metric=metricas)), None)
        if d:
            return d
    return {}


def leer_hist():
    if not os.path.exists(HIST):
        return {}
    return {f['id']: f for f in csv.DictReader(open(HIST, encoding='utf-8'))}


def num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def reels():
    ig = es.env('IG_USER_ID')
    media = es.probar('instagram_basic', 'lista de reels', lambda: es.get(
        f'{ig}/media', fields='id,caption,media_type,media_product_type,timestamp,permalink,media_url,like_count,'
        'comments_count', limit=50).get('data', []), [])
    viejos = leer_hist()
    filas = dict(viejos)
    for m in media:
        if m.get('media_product_type') != 'REELS':
            continue
        ins = insights_reel(m['id'])
        if not ins and m['id'] in viejos:
            continue  # sin permiso hoy: se queda el dato anterior
        t = dt.datetime.fromisoformat(m['timestamp'].replace('+0000', '+00:00')).astimezone(UTAH)
        dur = num(viejos.get(m['id'], {}).get('duracion_s')) or (duracion(m['media_url']) if m.get('media_url') else None)
        prom = ins.get('ig_reels_avg_watch_time')
        prom = round(prom / 1000, 1) if prom else None  # Meta lo da en milisegundos
        filas[m['id']] = {
            'id': m['id'], 'fecha': t.date().isoformat(), 'hora': t.strftime('%H:%M'), 'duracion_s': dur or '',
            'vistas': ins.get('views', ins.get('plays', '')), 'alcance': ins.get('reach', ''),
            'seg_promedio': prom or '', 'pct_visto': round(100 * prom / dur) if prom and dur else '',
            'guardados': ins.get('saved', ''), 'compartidos': ins.get('shares', ''),
            'likes': m.get('like_count', ''), 'comentarios': m.get('comments_count', ''),
            'texto': (m.get('caption') or '').split('\n')[0][:80], 'link': m.get('permalink', '')}
    filas = sorted(filas.values(), key=lambda f: f['fecha'] + f['hora'], reverse=True)
    os.makedirs(OUT, exist_ok=True)
    with open(HIST, 'w', encoding='utf-8', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=CAMPOS)
        w.writeheader()
        w.writerows(filas)
    return filas


def lecciones(filas):
    out = []
    con_pct = [f for f in filas if num(f['pct_visto']) is not None]
    if len(con_pct) >= 4:
        orden = sorted(con_pct, key=lambda f: -num(f['pct_visto']))
        n = max(2, len(orden) // 3)
        top, bajo = orden[:n], orden[-n:]
        dt_top = statistics.mean(num(f['duracion_s']) for f in top)
        dt_bajo = statistics.mean(num(f['duracion_s']) for f in bajo)
        out.append(f"Los reels que más se miran hasta el final duran en promedio **{dt_top:.0f} s** "
                   f"(se ve el {statistics.mean(num(f['pct_visto']) for f in top):.0f}%); los que la gente abandona, "
                   f"{dt_bajo:.0f} s (se ve el {statistics.mean(num(f['pct_visto']) for f in bajo):.0f}%). "
                   f"Apuntar a ~{dt_top:.0f} s.")
        out.append("Arranques que retienen (copiar el estilo del primer segundo): "
                   + "; ".join(f"«{f['texto'][:50]}»" for f in top[:3]))
    con_v = [f for f in filas if num(f['vistas']) is not None]
    if len(con_v) >= 6:
        por_hora = {}
        for f in con_v:
            franja = 'mañana' if f['hora'] < '12:00' else 'tarde' if f['hora'] < '18:00' else 'noche'
            por_hora.setdefault(franja, []).append(num(f['vistas']))
        mejor = max(por_hora, key=lambda k: statistics.mean(por_hora[k]))
        out.append(f"La franja con más vistas promedio es la **{mejor}** ("
                   + ", ".join(f"{k}: {statistics.mean(v):.0f}" for k, v in por_hora.items()) + ").")
    utiles = [f for f in filas if num(f['alcance'])]
    if utiles:
        def valor(f):
            return ((num(f['compartidos']) or 0) + (num(f['guardados']) or 0)) / num(f['alcance'])
        mejor = max(utiles, key=valor)
        if valor(mejor) > 0:
            out.append(f"El que más se guarda y comparte por cada persona que lo ve: [{mejor['texto'][:50]}]({mejor['link']}) "
                       f"({valor(mejor) * 100:.1f}%). Ese tema o formato merece una segunda parte.")
    if not out:
        out.append("Todavía hay pocos reels con datos: las lecciones aparecen solas a partir de 4 reels medidos.")
    return out


def escribir_reels(filas):
    lineas = [f"# Reels de Cozy Paws: qué funciona ({dt.datetime.now(UTAH):%d %b %Y})", "",
              "Lo arma GitHub solo todos los días (cozypaws/reels.py). Leer ANTES de escribir el próximo guion.", "",
              "## Lecciones", ""] + [f"{i}. {l}" for i, l in enumerate(lecciones(filas), 1)] + [
              "", "## Cada reel", "",
              "| Fecha | Reel | Dura | Vistas | Se ve (seg prom.) | % visto | Guardados | Compartidos |",
              "|---|---|---|---|---|---|---|---|"]
    for f in filas[:30]:
        lineas.append(f"| {f['fecha']} {f['hora']} | [{f['texto'][:40] or 'reel'}]({f['link']}) | {f['duracion_s'] or '-'} s | "
                      f"{f['vistas'] or '-'} | {f['seg_promedio'] or '-'} | {f['pct_visto'] or '-'}% | "
                      f"{f['guardados'] or '-'} | {f['compartidos'] or '-'} |")
    lineas += ["", "Meta no entrega por API el segundo exacto en que se va la gente: esa curva se mira en la app "
               "(reel > Ver estadísticas). El % visto de arriba sale de los segundos promedio sobre la duración."]
    if es.faltan:
        lineas += ["", "## Permisos que le faltan al token", ""] + [f"{i}. `{p}`" for i, p in enumerate(sorted(es.faltan), 1)]
    open(os.path.join(OUT, 'reels.md'), 'w', encoding='utf-8').write("\n".join(lineas) + "\n")


def ideas():
    ig = es.env('IG_USER_ID')
    posts = []
    for tag in HASHTAGS:
        r = es.probar('instagram_basic', 'búsqueda de hashtags',
                      lambda: es.get('ig_hashtag_search', user_id=ig, q=tag).get('data', []), [])
        if not r:
            continue
        top = es.probar('instagram_basic', 'posts populares de un hashtag', lambda: es.get(
            f"{r[0]['id']}/top_media", user_id=ig, fields='caption,media_type,media_product_type,like_count,'
            'comments_count,permalink', limit=25).get('data', []), [])
        for p in top:
            p['tag'] = tag
        posts += top
    posts.sort(key=lambda p: -(p.get('like_count') or 0))
    formatos = {}
    for p in posts:
        k = 'reel' if p.get('media_product_type') == 'REELS' else {'CAROUSEL_ALBUM': 'carrusel'}.get(p.get('media_type'), 'foto')
        formatos[k] = formatos.get(k, 0) + 1
    lineas = [f"# Ideas de Instagram: lo más popular en hashtags de mascotas ({dt.datetime.now(UTAH):%d %b %Y})", "",
              "Lo arma GitHub los domingos. Copiar la IDEA (situación, remate, formato) y contarla con India en el mundo "
              "ilustrado de Cozy; nunca copiar el video ni usar fotos reales de India.", ""]
    if not posts:
        lineas.append("Esta semana no se pudo leer (el token de Meta no tiene permiso o venció).")
    else:
        lineas += ["Formatos entre los más populares: " + ", ".join(f"{k} {v}" for k, v in sorted(formatos.items(), key=lambda x: -x[1])), "",
                   "| # | Hashtag | Formato | Likes | Coment. | Primera línea |", "|---|---|---|---|---|---|"]
        for i, p in enumerate(posts[:20], 1):
            k = 'reel' if p.get('media_product_type') == 'REELS' else p.get('media_type', '').lower()
            txt = (p.get('caption') or '').split('\n')[0][:70].replace('|', '/')
            lineas.append(f"| {i} | #{p['tag']} | [{k}]({p.get('permalink', '')}) | {p.get('like_count', '-')} | "
                          f"{p.get('comments_count', '-')} | {txt} |")
    open(os.path.join(OUT, 'ideas-instagram.md'), 'w', encoding='utf-8').write("\n".join(lineas) + "\n")


if __name__ == '__main__':
    es.asegurar_token_de_pagina()
    if not es.env('IG_USER_ID') or not es.env('FB_PAGE_TOKEN'):
        sys.exit('Faltan IG_USER_ID / FB_PAGE_TOKEN')
    escribir_reels(reels())
    if '--ideas' in sys.argv or dt.datetime.now(UTAH).weekday() == 6:
        ideas()
