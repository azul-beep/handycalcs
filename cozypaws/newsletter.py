#!/usr/bin/env python3
"""Cozy Paws Club: newsletter mensual que se arma y se manda solo (gratis, sin Claude).

Qué hace (lo corre .github/workflows/cozypaws-newsletter.yml, días 1 a 10 de cada mes):
  1. Elige los productos que salieron desde el último newsletter (los mismos que alimentan feed.xml:
     data/productos.csv), los artículos nuevos del blog y una herramienta gratis del mes.
  2. Arma el mail en HTML con la marca (crema, ciruela, dorado) y el cupón del club (CLUB10).
  3. Lo guarda en cozypaws/newsletter/AAAA-MM.html (versión mail) y data/newsletter/AAAA-MM.html (versión web,
     build.py la publica en /news/AAAA-MM/).
  4. Si hay clave de MailerLite (secret MAILERLITE_TOKEN), crea la campaña para el grupo "Cozy Paws Club" y
     la manda (o la deja en borrador si la variable NEWSLETTER_MODO = borrador).

Sale el primer martes del mes (o la primera corrida después, si GitHub atrasó o salteó el cron).
Nunca manda dos veces el mismo mes: lo enviado queda en data/newsletter-enviado.json.

Probar a mano (no manda nada):  python3 cozypaws/newsletter.py --hoy 2026-12-01 --vista
"""
import argparse, datetime as dt, html, json, os, sys, urllib.error, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, 'apps'))
import build  # noqa: E402  (CONFIG, productos y herramientas de la web)
import articulos  # noqa: E402

CFG = build.CONFIG
URL = CFG['url']
E = html.escape
STATE = os.path.join(HERE, 'data', 'newsletter-enviado.json')
OUT_MAIL = os.path.join(HERE, 'newsletter')
OUT_WEB = os.path.join(HERE, 'data', 'newsletter')

NL = dict(
    group='Cozy Paws Club',                 # grupo de MailerLite (el del formulario de la web)
    from_name='Cozy Paws',
    from_email='support@skyesolutionsai.com',  # tiene que estar verificado en MailerLite (el dominio ya lo está)
    coupon='CLUB10',                        # cupón de Etsy del club (10%), lo crea el hilo de Chrome (paso D del LEEME)
    max_products=6,
    max_articles=3,
    min_new=2,                              # con menos productos nuevos se completa con los más recientes
    desde='2026-12',                        # primer número (antes de esto no arma nada)
)

# Saludo de cada mes: (asunto, texto de vista previa, título, párrafo). {n} = productos nuevos, {first} = el primero.
MONTHS = {
    1: ('New year, new cozy finds 🐾', 'Fresh designs for you and your pet', 'Hello, 2027 with paws',
        'A new year is the perfect excuse to treat the pet who got you through the last one. Here is what is new in the shop, plus a few reads for cold days.'),
    2: ('Love, but make it furry 💌', 'Valentine picks for pet people', 'Love comes with four paws',
        'February is for the ones who greet you at the door every single day. These are this month\'s picks for pet people and the pets themselves.'),
    3: ('Spring walks are coming 🌷', 'New designs and spring pet tips', 'Hello, spring',
        'Longer days mean longer walks. Here is what is new at Cozy Paws, plus some tips to get ready for the season.'),
    4: ('Fresh picks for spring 🐶', 'New in the shop this month', 'Spring cleaning, pet edition',
        'Out with the old toys, in with a little something new. These are the newest Cozy Paws designs.'),
    5: ('For the best pet moms 💐', 'Mother\'s Day picks for dog and cat moms', 'Happy Mother\'s Day to every pet mom',
        'Dog moms and cat moms count too. Here are this month\'s gifts for the pet mom in your life (or for you).'),
    6: ('Summer is for adventures 🌞', 'New designs and hot weather tips', 'Summer with your best friend',
        'Road trips, park days and lazy afternoons. Here is what is new, plus how to keep pets safe in the heat.'),
    7: ('Cozy picks for summer days 🐾', 'New in the shop this month', 'Mid summer hello',
        'Hope you and your pet are staying cool. Here is what is new at Cozy Paws this month.'),
    8: ('Back to routine, with paws 🐕', 'New designs for pet people', 'Back to routine',
        'New schedules can be hard on pets too. Here are this month\'s new designs and a few helpful reads.'),
    9: ('Sweater weather is here 🍂', 'Fall picks for you and your pet', 'Hello, fall',
        'Cooler mornings, cozier walks. Here is what is new at Cozy Paws for the season.'),
    10: ('Cozy fall finds 🎃', 'New designs and fall pet tips', 'Fall is for cozy',
         'Pumpkin season is better with a pet on the couch. These are the newest Cozy Paws designs.'),
    11: ('{n} new gifts for pet people 🎁', 'Start your holiday list early', 'The gift list starts here',
         'Holiday shopping for a pet person is easy when you know where to look. Here are the newest designs, made to order in the USA.'),
    12: ('{n} cozy gifts before Christmas 🎄', 'Order by Dec 10 for US Christmas delivery', 'Merry everything from Cozy Paws',
         'The most wonderful time of the year is even better with paws. Here are the newest gifts, made to order in the USA.'),
}

# Herramienta o app gratis del mes (rota sola): (ruta, título, texto)
FEATURES = [
    ('/fun/', 'Paw Party, our free fun app', 'Find your pet\'s age in human years, take the personality quiz and make a birthday card with your pet\'s photo.'),
    ('/diary/', 'Paw Diary, a free pet diary', 'Log walks, meals and meds, and get reminders for vaccines and flea pills. Works offline, no sign up.'),
    ('/tools/dog-age-calculator/', 'How old is your dog in human years?', 'Our free calculator uses the vet chart by size and the newer DNA-based formula.'),
    ('/tools/dog-food-calculator/', 'How much should your dog eat?', 'Daily calories and cups by weight and activity, with the formula vets use.'),
    ('/tools/cat-age-calculator/', 'How old is your cat in human years?', 'Instant answer plus your cat\'s life stage.'),
    ('/tools/pet-name-generator/', 'Need a name for a new pet?', 'Hundreds of dog and cat names by style: cute, classic, foodie and more.'),
]


def utm(path, content):
    sep = '&' if '?' in path else '?'
    full = path if path.startswith('http') else URL + path
    return f'{full}{sep}utm_source=mailerlite&utm_medium=email&utm_campaign=newsletter&utm_content={content}'


def first_tuesday(year, month):
    d = dt.date(year, month, 1)
    return d + dt.timedelta(days=(1 - d.weekday()) % 7)


def load_state():
    if os.path.exists(STATE):
        return json.load(open(STATE, encoding='utf-8'))
    return {}


def pick(today, since):
    """Productos y artículos que salieron entre since (sin incluir) y today."""
    visible, _ = build.load_products(today)
    new = [p for p in visible if since < p['live'] <= today]
    # variedad: de a uno por tipo (taza, adorno, buzo...) en ronda, los más nuevos primero
    by_kind = {}
    for p in new:
        by_kind.setdefault(p['kind'], []).append(p)
    chosen = []
    while len(chosen) < NL['max_products'] and any(by_kind.values()):
        for k in list(by_kind):
            if by_kind[k] and len(chosen) < NL['max_products']:
                chosen.append(by_kind[k].pop(0))
    n_new = len(new)
    if len(chosen) < NL['max_products']:  # completar con los más recientes que no estén
        rest = [p for p in visible if p not in chosen]
        chosen += rest[:NL['max_products'] - len(chosen)]
    arts = [a for a in articulos.load() if since < a['live'] <= today]
    arts.sort(key=lambda a: a['live'], reverse=True)
    return chosen, n_new, arts[:NL['max_articles']]


# ---------------------------------------------------------------- HTML del mail (tablas e estilos en línea, 600 px)
C = dict(cream='#F3E9D7', cream2='#FAF4E8', plum='#3B2433', blue='#4E7F86', gold='#C8962E', rose='#B5525C', ink='#3a2f2a', line='#E2D3B8')
SERIF = "Georgia,'Times New Roman',serif"
SANS = "Helvetica,Arial,sans-serif"


def btn(href, label, color=None):
    color = color or C['gold']
    return (f'<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="margin:0 auto"><tr><td style="background:{color};border-radius:10px">'
            f'<a href="{E(href)}" style="display:inline-block;padding:13px 26px;font:bold 16px {SANS};color:#ffffff;text-decoration:none">{E(label)}</a></td></tr></table>')


def product_cell(p, i):
    return (f'<td width="50%" valign="top" style="padding:8px">'
            f'<a href="{E(utm(p["etsy"], "producto-" + p["sku"]))}" style="text-decoration:none;color:{C["ink"]}">'
            f'<img src="{URL}/img/p/{E(p["sku"])}.jpg" width="264" alt="{E(p["short"])}" style="display:block;width:100%;max-width:264px;height:auto;border-radius:12px;border:1px solid {C["line"]}">'
            f'<p style="margin:10px 0 2px;font:bold 15px/1.3 {SANS};color:{C["plum"]}">{E(p["short"])}</p>'
            f'<p style="margin:0;font:14px/1.4 {SANS};color:{C["ink"]}">{E(p["kind"])} · from ${E(str(p["precio"]))}</p></a></td>')


def render(today, prods, n_new, arts, feature, for_email=True):
    m = today.month
    subj, pre, title, intro = MONTHS[m]
    n_show = n_new if n_new >= NL['min_new'] else len(prods)
    subj = subj.format(n=n_show, first=prods[0]['short'] if prods else '')
    month_name = today.strftime('%B %Y')
    rows = ''
    for i in range(0, len(prods), 2):
        pair = prods[i:i + 2]
        rows += '<tr>' + ''.join(product_cell(p, i + j) for j, p in enumerate(pair)) + ('<td width="50%"></td>' if len(pair) == 1 else '') + '</tr>'
    prod_head = 'New in the shop' if n_new >= NL['min_new'] else 'Member favorites'
    art_html = ''
    if arts:
        lis = ''.join(f'<tr><td style="padding:8px 0;border-bottom:1px solid {C["line"]}"><a href="{E(utm("/blog/" + a["slug"] + "/", "articulo-" + a["slug"]))}" '
                      f'style="font:bold 16px/1.4 {SANS};color:{C["blue"]};text-decoration:none">{E(a.get("h1") or a["title"])}</a>'
                      f'<p style="margin:4px 0 0;font:14px/1.5 {SANS};color:{C["ink"]}">{E(a.get("description", ""))}</p></td></tr>' for a in arts)
        art_html = (f'<tr><td style="padding:26px 30px 6px"><h2 style="margin:0 0 6px;font:normal 26px {SERIF};color:{C["plum"]}">Fresh on the blog</h2>'
                    f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">{lis}</table></td></tr>')
    fpath, ftitle, ftext = feature
    xmas = (f'<p style="margin:14px 0 0;font:bold 14px {SANS};color:{C["rose"]}">Order by December 10 for Christmas delivery in the US.</p>'
            if m == 12 and today <= CFG['christmas_cutoff'] else '')
    if for_email:
        foot_links = (f'<a href="{{$unsubscribe}}" style="color:{C["plum"]}">Unsubscribe</a> · '
                      f'<a href="{URL}/news/{today:%Y-%m}/" style="color:{C["plum"]}">View in browser</a>')
    else:
        foot_links = f'<a href="{URL}/#join" style="color:{C["plum"]}">Join the club</a> to get this in your inbox every month.'
    body = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(subj)}</title>{'' if for_email else f'<link rel="canonical" href="{URL}/news/{today:%Y-%m}/"><meta name="description" content="{E(pre)}">'}</head>
<body style="margin:0;padding:0;background:{C["cream"]}">
<div style="display:none;max-height:0;overflow:hidden;opacity:0">{E(pre)}</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:{C["cream"]}"><tr><td align="center" style="padding:20px 10px">
<table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0" style="width:100%;max-width:600px;background:{C["cream2"]};border-radius:16px;overflow:hidden;border:1px solid {C["line"]}">
<tr><td align="center" style="background:{C["plum"]};padding:22px 20px 18px">
<a href="{E(utm("/", "logo"))}"><img src="{URL}/img/logo-160.png" width="90" height="91" alt="Cozy Paws" style="display:block;border:0"></a>
<p style="margin:10px 0 0;font:bold 12px {SANS};letter-spacing:2px;text-transform:uppercase;color:{C["gold"]}">Cozy Paws Social Club · {E(month_name)}</p></td></tr>
<tr><td style="padding:30px 30px 8px"><h1 style="margin:0 0 12px;font:normal 32px/1.2 {SERIF};color:{C["plum"]}">{E(title)}</h1>
<p style="margin:0;font:16px/1.6 {SANS};color:{C["ink"]}">{E(intro)}</p>{xmas}</td></tr>
<tr><td style="padding:22px 22px 0"><h2 style="margin:0 8px 4px;font:normal 26px {SERIF};color:{C["plum"]}">{prod_head}</h2>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">{rows}</table></td></tr>
<tr><td style="padding:18px 30px 6px">{btn(utm(CFG["shop"], "tienda"), "See everything on Etsy")}</td></tr>
<tr><td style="padding:22px 30px 0"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:{C["plum"]};border-radius:14px">
<tr><td align="center" style="padding:22px 20px"><p style="margin:0;font:bold 12px {SANS};letter-spacing:2px;text-transform:uppercase;color:{C["gold"]}">Members only</p>
<p style="margin:8px 0 4px;font:normal 24px {SERIF};color:#ffffff">10% off with code <b style="color:{C["gold"]}">{E(NL["coupon"])}</b></p>
<p style="margin:0;font:14px {SANS};color:{C["cream"]}">Type it at checkout in our Etsy shop.</p></td></tr></table></td></tr>
{art_html}
<tr><td style="padding:24px 30px 6px"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="border:2px dashed {C["gold"]};border-radius:14px">
<tr><td style="padding:18px 20px"><p style="margin:0 0 4px;font:bold 12px {SANS};letter-spacing:2px;text-transform:uppercase;color:{C["blue"]}">Free this month</p>
<p style="margin:0 0 6px;font:normal 22px {SERIF};color:{C["plum"]}">{E(ftitle)}</p><p style="margin:0 0 12px;font:15px/1.5 {SANS};color:{C["ink"]}">{E(ftext)}</p>
<a href="{E(utm(fpath, "gratis"))}" style="font:bold 15px {SANS};color:{C["blue"]}">Try it free →</a></td></tr></table></td></tr>
<tr><td style="padding:24px 30px 10px"><p style="margin:0;font:16px/1.6 {SANS};color:{C["ink"]}">Thanks for being part of the club. Hit reply and tell us about your pet, we read every email.</p>
<p style="margin:10px 0 0;font:italic 18px {SERIF};color:{C["plum"]}">Azu and the Cozy Paws crew</p></td></tr>
<tr><td align="center" style="padding:20px 30px 26px;border-top:1px solid {C["line"]}">
<p style="margin:0 0 8px;font:13px {SANS}"><a href="{E(utm(CFG["instagram"], "instagram"))}" style="color:{C["blue"]}">Instagram</a> · <a href="{E(utm(CFG["pinterest"], "pinterest"))}" style="color:{C["blue"]}">Pinterest</a> · <a href="{E(utm(CFG["facebook"], "facebook"))}" style="color:{C["blue"]}">Facebook</a></p>
<p style="margin:0;font:12px/1.6 {SANS};color:#7a6d63">Cozy Paws by {E(CFG["company"])} · Designed in Salt Lake City, Utah<br>
You get this because you joined the Cozy Paws Club at cozypawsgifts.pages.dev.<br>{foot_links}</p></td></tr>
</table></td></tr></table></body></html>'''
    return subj, pre, body


# ---------------------------------------------------------------- MailerLite (API nueva, connect.mailerlite.com)
def ml(method, path, token, data=None):
    req = urllib.request.Request('https://connect.mailerlite.com/api' + path, method=method,
                                 data=json.dumps(data).encode() if data is not None else None,
                                 headers={'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json', 'Accept': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            txt = r.read().decode()
            return json.loads(txt) if txt else {}
    except urllib.error.HTTPError as e:
        raise SystemExit(f'MailerLite respondió {e.code} en {method} {path}: {e.read().decode()[:800]}')


def group_id(token):
    gid = os.environ.get('MAILERLITE_GROUP_ID', '').strip()
    if gid:
        return gid
    res = ml('GET', '/groups?limit=100&filter[name]=' + urllib.request.quote(NL['group']), token)
    for g in res.get('data', []):
        if g['name'].strip().lower() == NL['group'].lower():
            print(f'Grupo "{g["name"]}": {g.get("active_count", "?")} suscriptores activos')
            return g['id']
    raise SystemExit(f'No encontré el grupo "{NL["group"]}" en MailerLite. Crealo (paso A del LEEME) o poné MAILERLITE_GROUP_ID.')


def send(today, subj, body, token, modo):
    gid = group_id(token)
    camp = ml('POST', '/campaigns', token, {
        'name': f'Cozy Paws Club · {today:%B %Y}', 'type': 'regular', 'groups': [gid],
        'emails': [{'subject': subj, 'from_name': NL['from_name'], 'from': NL['from_email'], 'reply_to': NL['from_email'], 'content': body}],
    })['data']
    print(f'Campaña creada: {camp["id"]} ({camp.get("status")})')
    if modo == 'enviar':
        ml('POST', f'/campaigns/{camp["id"]}/schedule', token, {'delivery': 'instant'})
        print('Enviada (delivery instant).')
    else:
        print('Quedó en BORRADOR en MailerLite > Campaigns (NEWSLETTER_MODO=borrador).')
    return camp['id']


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--hoy', help='AAAA-MM-DD (por defecto, hoy en Utah)')
    ap.add_argument('--vista', action='store_true', help='solo arma los HTML, no manda ni guarda estado')
    ap.add_argument('--forzar', action='store_true', help='armar aunque no sea el primer martes')
    a = ap.parse_args()
    today = dt.date.fromisoformat(a.hoy) if a.hoy else (dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=7)).date()
    key = f'{today:%Y-%m}'
    state = load_state()
    if key < NL['desde'] and not a.vista:
        print(f'El newsletter arranca en {NL["desde"]}.')
        return
    if key in state and not a.vista:
        print(f'El newsletter de {key} ya salió ({state[key]["fecha"]}). Nada que hacer.')
        return
    if today < first_tuesday(today.year, today.month) and not (a.forzar or a.vista):
        print(f'Todavía no: sale el primer martes ({first_tuesday(today.year, today.month)}).')
        return
    prev = [dt.date.fromisoformat(v['fecha']) for v in state.values()]
    since = max(prev) if prev else today - dt.timedelta(days=31)
    prods, n_new, arts = pick(today, since)
    if not prods:
        print('No hay productos publicados: no se arma newsletter.')
        return
    feature = FEATURES[(today.year * 12 + today.month) % len(FEATURES)]
    subj, pre, body = render(today, prods, n_new, arts, feature, for_email=True)
    _, _, web = render(today, prods, n_new, arts, feature, for_email=False)
    os.makedirs(OUT_MAIL, exist_ok=True); os.makedirs(OUT_WEB, exist_ok=True)
    open(os.path.join(OUT_MAIL, key + '.html'), 'w', encoding='utf-8').write(body)
    open(os.path.join(OUT_WEB, key + '.html'), 'w', encoding='utf-8').write(web)
    print(f'{key}: "{subj}" · {n_new} productos nuevos desde {since}, {len(prods)} en el mail, {len(arts)} artículos, gratis: {feature[0]}')
    if a.vista:
        return
    token = os.environ.get('MAILERLITE_TOKEN', '').strip()
    modo = (os.environ.get('NEWSLETTER_MODO') or 'enviar').strip().lower()
    if not token:
        # sin clave: queda listo y publicado en la web, pero no se marca como enviado (se prueba de nuevo mañana)
        print('Falta el secret MAILERLITE_TOKEN: el mail quedó armado en cozypaws/newsletter/ pero no se mandó.')
        if today.day >= 8:
            print('::warning::Newsletter de Cozy Paws listo pero sin mandar: falta MAILERLITE_TOKEN en GitHub (ver cozypaws/newsletter/LEEME.md).')
        return
    cid = send(today, subj, body, token, modo)
    state[key] = dict(fecha=today.isoformat(), asunto=subj, campaign_id=cid, modo=modo, productos=[p['sku'] for p in prods])
    json.dump(state, open(STATE, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main()
