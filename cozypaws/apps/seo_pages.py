"""Páginas para buscadores que llevan a las apps (las arma build.py todos los días, gratis y sin Claude).

1. /breeds/<raza>/  : una por raza (70 perros + 10 gatos) con edad en años humanos, peso sano y cuánta comida darle.
2. /names/<lista>/  : listas de nombres por estilo para perros y gatos (salen de la lista de Paw Party).
Goteo (regla de Azu: de a poco): 1 raza y 1 lista por día desde START. Cada página nueva entra al feed.xml
con su pin 1000x1500, así Pinterest la publica sola. Las razas y los nombres se leen de diary.html y fun.html
(una sola fuente de datos: si se agrega una raza en la app, sale su página sola al final de la cola).
"""
import datetime as dt, html, json, os, re, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
E = html.escape
START = dt.date(2026, 11, 15)
# raza -> estampa de Cozy Paws que la tiene (para el link discreto a Etsy)
BREED_STAMP = {'Labrador Retriever': 'labrador', 'Golden Retriever': 'golden', 'German Shepherd': 'german-shepherd', 'French Bulldog': 'frenchie',
               'Dachshund': 'dachshund', 'Dachshund (Miniature)': 'dachshund', 'Labradoodle': 'doodle', 'Goldendoodle': 'doodle', 'Mini Goldendoodle': 'doodle'}
# orden de salida: las razas más buscadas primero
FIRST = ['Labrador Retriever', 'Golden Retriever', 'French Bulldog', 'German Shepherd', 'Domestic cat', 'Dachshund', 'Goldendoodle', 'Poodle (Standard)',
         'Beagle', 'Maine Coon', 'Bulldog', 'Rottweiler', 'Pembroke Welsh Corgi', 'Siberian Husky', 'Australian Shepherd', 'Ragdoll', 'Chihuahua',
         'Shih Tzu', 'Yorkshire Terrier', 'Pug', 'Border Collie', 'Siamese', 'Boxer', 'Cavalier King Charles Spaniel', 'Bernese Mountain Dog', 'Great Dane']
SIZE_F = {'small': 4, 'medium': 5, 'large': 6, 'giant': 7}
STYLE_EN = {'cute': 'Cute', 'classic': 'Classic', 'foodie': 'Food', 'tough': 'Tough', 'funny': 'Funny', 'holiday': 'Christmas', 'latino': 'Spanish',
            'nature': 'Nature', 'myth': 'Mythology'}


def slug(s):
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')


def js_array(src, name):
    m = re.search(r'var ' + name + r'=(\[\[.*?\]\]);', src, re.S)
    return json.loads(m.group(1).replace("'", '"'))


def load_breeds():
    src = open(os.path.join(HERE, 'diary.html'), encoding='utf-8').read()
    out = [dict(sp='dog', en=b[0], es=b[1], lo=b[2], hi=b[3]) for b in js_array(src, 'DOGS')]
    out += [dict(sp='cat', en=b[0], es=b[1], lo=b[2], hi=b[3]) for b in js_array(src, 'CATS')]
    for b in out:
        b['slug'] = slug(b['en'] if b['en'] != 'Domestic cat' else 'domestic-cat')
        mid = (b['lo'] + b['hi']) / 2
        b['size'] = None if b['sp'] == 'cat' else 'small' if mid < 9.1 else 'medium' if mid < 23 else 'large' if mid < 41 else 'giant'
    rank = {n: i for i, n in enumerate(FIRST)}
    out.sort(key=lambda b: (rank.get(b['en'], 999), b['sp'] != 'dog', b['en']))
    return out


def load_names():
    src = open(os.path.join(HERE, 'fun.html'), encoding='utf-8').read()
    block = src[src.index('var NAMES={'):src.index('function renderNames')]
    lists = []
    for style, d, c in re.findall(r"(\w+):\{d:'([^']*)',c:'([^']*)'\}", block):
        for sp, raw in (('dog', d), ('cat', c)):
            names = raw.split('|') if '|' in raw else raw.split()
            names = list(dict.fromkeys(n.strip() for n in names if n.strip()))
            lists.append(dict(style=style, sp=sp, names=names, slug=f'{slug(STYLE_EN[style])}-{sp}-names'))
    order = ['cute', 'holiday', 'funny', 'classic', 'tough', 'foodie', 'latino', 'nature', 'myth']
    lists.sort(key=lambda x: (order.index(x['style']), x['sp'] != 'dog'))
    return lists


def human(sp, y, size):
    if y <= 1:
        return y * 15
    if y <= 2:
        return 15 + (y - 1) * 9
    return 24 + (y - 2) * (4 if sp == 'cat' else SIZE_F[size])


def kcal(kg, f):
    return round(70 * kg ** 0.75 * f)


def lb(kg):
    return round(kg * 2.20462)


def pin_maker(DATA):
    from PIL import Image, ImageDraw, ImageFont
    PLUM, BLUE, CREAM, GOLD = (59, 36, 51), (78, 127, 134), (243, 233, 215), (200, 150, 46)

    def font(kind, size):
        f = {'script': 'Yesteryear-Regular.ttf', 'title': 'AbrilFatface-Regular.ttf', 'body': 'Lora.ttf'}[kind]
        try:
            return ImageFont.truetype(os.path.join(DATA, 'fonts', f), size)
        except OSError:
            return ImageFont.load_default()

    def wrap(d, text, f, maxw):
        lines, cur = [], ''
        for w in text.split():
            t = (cur + ' ' + w).strip()
            if d.textlength(t, font=f) <= maxw:
                cur = t
            else:
                lines.append(cur); cur = w
        lines.append(cur)
        return lines

    logo = Image.open(os.path.join(DATA, 'brand', 'logo-ilustrado.png')).convert('RGBA')

    def pin(dst, kicker, head, sub, stamp=None, big=None):
        if os.path.exists(dst):
            return
        W, H = 1000, 1500
        c = Image.new('RGB', (W, H), CREAM)
        d = ImageDraw.Draw(c)
        d.rounded_rectangle([30, 30, W - 30, H - 30], 36, outline=GOLD, width=4)
        art = Image.open(stamp).convert('RGBA') if stamp else logo.copy()
        art.thumbnail((760, 600))
        c.paste(art, ((W - art.width) // 2, 80 + (600 - art.height) // 2), art)
        fk, f1, f2 = font('body', 40), font('title', 92), font('body', 42)
        lines = wrap(d, head, f1, 880)
        if len(lines) > 3:
            f1 = font('title', 72); lines = wrap(d, head, f1, 880)[:4]
        subs = wrap(d, sub, f2, 860)[:2]
        block = 60 + len(lines) * (f1.size + 14) + 20 + len(subs) * 56
        y = 700 + max(0, (H - 190 - 700 - block) // 2)
        w = d.textlength(kicker.upper(), font=fk); d.text(((W - w) / 2, y), kicker.upper(), font=fk, fill=GOLD); y += 60
        for ln in lines:
            w = d.textlength(ln, font=f1); d.text(((W - w) / 2, y), ln, font=f1, fill=PLUM); y += f1.size + 14
        y += 20
        for ln in subs:
            w = d.textlength(ln, font=f2); d.text(((W - w) / 2, y), ln, font=f2, fill=BLUE); y += 56
        d.rounded_rectangle([30, H - 170, W - 30, H - 30], 36, fill=BLUE)
        d.rectangle([30, H - 170, W - 30, H - 120], fill=BLUE)
        f3 = font('script', 78); t = 'Cozy Paws'
        d.text(((W - d.textlength(t, font=f3)) / 2, H - 160), t, font=f3, fill=CREAM)
        c.save(dst, 'JPEG', quality=86, optimize=True, progressive=True)
    return pin


def build_seo(page, config, OUT, DATA, today, stamps):
    """Escribe las páginas que ya tocan por el goteo. Devuelve (urls para el sitemap, items para el feed)."""
    urls, items = [], []
    shop = {s['id']: s['url'] for s in stamps}
    pins_cache = os.path.join(DATA, 'pins')
    os.makedirs(pins_cache, exist_ok=True)
    os.makedirs(os.path.join(OUT, 'img', 'pin'), exist_ok=True)
    pin = pin_maker(DATA)
    stamp_png = lambda sid: os.path.join(DATA, 'apps', 'stamps', sid + '.png')
    breeds, names = load_breeds(), load_names()
    app_links = ('<div class="tools" style="margin-top:20px"><a class="tool" href="/diary/" style="background:var(--plum)"><b>Paw Diary app 📔</b><span>Track weight with a chart, '
                 'get vaccine and flea pill reminders and a daily food plan. Free, works offline.</span></a><a class="tool" href="/fun/" style="background:var(--rose)">'
                 '<b>Paw Party app 🎉</b><span>Human years, name ideas, a personality quiz and birthday cards with cute stamps.</span></a></div>')

    def shop_box(sid):
        if not sid or sid not in shop:
            return ''
        return (f'<a class="feature" href="{E(shop[sid])}" data-etsy="breed-{sid}" rel="nofollow" style="grid-template-columns:1fr 160px;background:var(--cream2);color:var(--ink);border:2px dashed var(--gold)">'
                '<div><b style="color:var(--plum)">A little something for the fan</b>Original Cozy Paws design on mugs, sweatshirts and ornaments, '
                'designed in Salt Lake City and printed on demand by our production partners. See it on Etsy →</div>'
                f'<img src="/fun/stamps/{sid}.png" alt="" loading="lazy" width="160" height="160" style="background:#fff;padding:8px"></a>')

    # ---------------------------------------------------------------- 1. razas
    live_b = []
    for i, b in enumerate(breeds):
        b['live'] = START + dt.timedelta(days=i)
        if b['live'] <= today:
            live_b.append(b)
    for b in live_b:
        cat, n, sid = b['sp'] == 'cat', b['en'].replace('Domestic cat', 'Domestic Cat'), BREED_STAMP.get(b['en'])
        pet = 'cat' if cat else 'dog'
        lo, hi = b['lo'], b['hi']
        mid = (lo + hi) / 2
        h1 = f'{n}{"" if cat else ""}: Age in Human Years, Healthy Weight and How Much to Feed'
        if n == 'Domestic cat':
            h1 = 'Domestic Cat: Age in Human Years, Healthy Weight and How Much to Feed'
        desc = (f'{n} facts for owners: healthy adult weight {lb(lo)}-{lb(hi)} lb ({lo:g}-{hi:g} kg), age in human years chart and daily calories. '
                'Free calculator and pet diary app.')
        ages = [1, 2, 3, 5, 7, 10, 12, 15]
        rows = ''.join(f'<tr><td>{a}</td><td>{round(human(b["sp"], a, b["size"]))}</td></tr>' for a in ages)
        size_txt = ('' if cat else f' That makes it a <b>{b["size"]}</b> breed, so after age 2 each year counts as about {SIZE_F[b["size"]]} human years.')
        if cat:
            fac = [('Adult, spayed or neutered', 1.2), ('Adult, not neutered', 1.4), ('Less active or senior', 1.0), ('Needs to lose weight', 0.8)]
        else:
            fac = [('Adult, spayed or neutered', 1.6), ('Adult, not neutered', 1.8), ('Senior or not very active', 1.4), ('Needs to lose weight', 1.0), ('Very active', 2.0)]
        cup = 400 if cat else 370
        food = ''.join(f'<tr><td>{E(lbl)}</td><td>{kcal(lo, f)} to {kcal(hi, f)}</td><td>{kcal(lo, f) / cup:.1f} to {kcal(hi, f) / cup:.1f}</td></tr>' for lbl, f in fac)
        water = f'{lb(lo)} to {lb(hi)} oz ({round(lo * 60)} to {round(hi * 60)} ml)'
        faq = [(f'How much should a {n} weigh?', f'A healthy adult {n} usually weighs {lb(lo)} to {lb(hi)} lb ({lo:g} to {hi:g} kg). Males are often at the top of the range and females at the bottom. Check the body too: you should feel the ribs easily and see a waist from above.'),
               (f'How old is a 5 year old {n} in human years?', f'About {round(human(b["sp"], 5, b["size"]))} human years. A 10 year old {n} is about {round(human(b["sp"], 10, b["size"]))}.'),
               (f'How many calories does a {n} need a day?', f'A typical spayed or neutered adult {n} needs about {kcal(mid, fac[0][1])} calories a day ({kcal(lo, fac[0][1])} to {kcal(hi, fac[0][1])} depending on size). That is roughly {kcal(mid, fac[0][1]) / cup:.1f} cups of a food with {cup} kcal per cup. Ask your vet for your {pet}\'s exact needs.')]
        body = (f'<h1>{E(h1)}</h1><p class="lead">Everything in one place for {E(n)} owners: how old your {pet} is in human years, the healthy weight range and how much to feed every day. '
                f'For your own {pet}\'s numbers, use our free <a href="/diary/">Paw Diary app</a>.</p>'
                f'<h2>Healthy weight</h2><p>A healthy adult <b>{E(n)}</b> usually weighs <b>{lb(lo)} to {lb(hi)} lb</b> ({lo:g} to {hi:g} kg).{size_txt}</p>'
                '<p>Breed ranges are a guide. The best check is the body: you should feel the ribs with light pressure, see a waist from above and a tummy tuck from the side. '
                'Weigh every 2 to 4 weeks and track it in <a href="/diary/">Paw Diary</a>, which shows a chart and tells you if the weight is in the healthy range for the breed.</p>'
                f'<h2>{E(n)} age in human years</h2><table><tr><th>{"Cat" if cat else "Dog"} age</th><th>Human years</th></tr>{rows}</table>'
                f'<p>Want a quick answer or a birthday card for your {pet}? Try <a href="/fun/">Paw Party</a>.</p>'
                f'<h2>How much to feed a {E(n)}</h2><p>Daily calories for an adult {E(n)} between {lb(lo)} and {lb(hi)} lb, using the RER formula vets use (70 × kg<sup>0.75</sup> × a factor). '
                f'Cups assume a food with {cup} kcal per cup: check your bag.</p>'
                f'<table><tr><th>Your {pet}</th><th>Calories a day</th><th>Cups a day</th></tr>{food}</table>'
                f'<p>Water: about {water} a day. Treats: under 10% of daily calories. {"Puppies" if not cat else "Kittens"} need 2 to 3 times more per pound.</p>'
                '<p class="note">General information only, not veterinary advice. Ask your vet before changing your pet\'s diet.</p>'
                + shop_box(sid) + app_links
                + '<h2>Questions</h2><div class="faq">' + ''.join(f'<details><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q, a in faq) + '</div>'
                + '<h2>More breeds</h2><div class="pills">' + ''.join(f'<a href="/breeds/{o["slug"]}/">{E(o["en"])}</a>' for o in [o for o in live_b if o is not b][-30:]) + '</div>')
        ld = [{'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in faq]},
              {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
                  {'@type': 'ListItem', 'position': 1, 'name': 'Breeds', 'item': config['url'] + '/breeds/'},
                  {'@type': 'ListItem', 'position': 2, 'name': n, 'item': config['url'] + f'/breeds/{b["slug"]}/'}]}]
        img = f'b-{b["slug"]}.jpg'
        pin(os.path.join(pins_cache, img), f'{n} owners', f'{n}: human years, healthy weight & food', f'Healthy weight {lb(lo)}-{lb(hi)} lb · free calculator', stamp_png(sid) if sid else None)
        page(f'/breeds/{b["slug"]}/', f'{n} Age in Human Years, Weight and Feeding Chart | Cozy Paws', desc[:158], body, today, image=f'/img/pin/{img}', jsonld=ld)
        urls.append((f'/breeds/{b["slug"]}/', b['live']))
        items.append((b['live'], f'{n}: age in human years, healthy weight and how much to feed', f'/breeds/{b["slug"]}/', f'/img/pin/{img}', desc, 'b-' + b['slug']))
    if live_b:
        dogs = ''.join(f'<a href="/breeds/{b["slug"]}/">{E(b["en"])}</a>' for b in sorted(live_b, key=lambda x: x['en']) if b['sp'] == 'dog')
        cats = ''.join(f'<a href="/breeds/{b["slug"]}/">{E(b["en"])}</a>' for b in sorted(live_b, key=lambda x: x['en']) if b['sp'] == 'cat')
        page('/breeds/', 'Dog and Cat Breeds: Human Years, Healthy Weight and Feeding | Cozy Paws', 'Healthy weight, age in human years and feeding charts for popular dog and cat breeds.',
             '<h1>Breed guides</h1><p class="lead">Healthy weight, age in human years and how much to feed, breed by breed. New breeds every day.</p>'
             + (f'<h2>Dogs</h2><div class="pills">{dogs}</div>' if dogs else '') + (f'<h2>Cats</h2><div class="pills">{cats}</div>' if cats else '') + app_links, today)
        urls.append(('/breeds/', today))

    # ---------------------------------------------------------------- 2. nombres
    live_n = []
    for i, x in enumerate(names):
        x['live'] = START + dt.timedelta(days=i)
        if x['live'] <= today:
            live_n.append(x)
    for x in live_n:
        sty, pet = STYLE_EN[x['style']], x['sp']
        title = f'{len(x["names"])} {sty} {"Dog" if pet == "dog" else "Cat"} Names'
        if x['style'] == 'latino':
            title = f'{len(x["names"])} Spanish {"Dog" if pet == "dog" else "Cat"} Names (Nombres en español)'
        desc = f'{title} with ideas you will not find everywhere. Tap for more in our free pet name generator app.'
        lis = ''.join(f'<li>{E(nm)}</li>' for nm in x['names'])
        others = ''.join(f'<a href="/names/{o["slug"]}/">{E(STYLE_EN[o["style"]])} {o["sp"]} names</a>' for o in live_n if o is not x)
        body = (f'<h1>{E(title)}</h1><p class="lead">Looking for the perfect name for your new {pet}? Here are {len(x["names"])} {sty.lower()} {pet} names. '
                f'Want more? Our free <a href="/fun/#names">Paw Party name generator</a> has hundreds more in 9 styles, lets you filter by first letter and save your favorites.</p>'
                f'<ul class="names" style="columns:3;font-size:18px">{lis}</ul>'
                '<h2>Tips for picking a name</h2><ol class="tips"><li>Short names (one or two syllables) are easier to learn.</li>'
                '<li>Avoid names that sound like commands, like "Kit" (sit) or "Bo" (no).</li><li>Say it out loud a few times: you will be calling it for years.</li>'
                '<li>Give it a few days. Changing the name early is fine.</li></ol>'
                + shop_box('dog-mom-club' if pet == 'dog' else 'cat-mom-club') + app_links
                + (f'<h2>More name lists</h2><div class="pills">{others}</div>' if others else ''))
        ld = {'@context': 'https://schema.org', '@type': 'ItemList', 'name': title, 'numberOfItems': len(x['names']),
              'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'name': nm} for i, nm in enumerate(x['names'][:50])]}
        img = f'n-{x["slug"]}.jpg'
        pin(os.path.join(pins_cache, img), 'Name ideas', title, ', '.join(x['names'][:6]) + '...', stamp_png('cozy-pup' if pet == 'dog' else 'cat-mom'))
        page(f'/names/{x["slug"]}/', f'{title} | Cozy Paws', desc[:158], body, today, image=f'/img/pin/{img}', jsonld=ld)
        urls.append((f'/names/{x["slug"]}/', x['live']))
        items.append((x['live'], title, f'/names/{x["slug"]}/', f'/img/pin/{img}', desc, 'n-' + x['slug']))
    if live_n:
        page('/names/', 'Dog and Cat Name Ideas | Cozy Paws', 'Lists of dog and cat names by style: cute, Christmas, funny, classic, tough, food, Spanish, nature and mythology.',
             '<h1>Pet name ideas</h1><p class="lead">Name lists by style, plus a free <a href="/fun/#names">name generator</a>.</p><div class="pills">'
             + ''.join(f'<a href="/names/{o["slug"]}/">{E(STYLE_EN[o["style"]])} {o["sp"]} names</a>' for o in live_n) + '</div>' + app_links, today)
        urls.append(('/names/', today))
    for f in os.listdir(pins_cache):
        if f.startswith(('b-', 'n-')):
            shutil.copy(os.path.join(pins_cache, f), os.path.join(OUT, 'img', 'pin', f))
    return urls, items, len(live_b), len(live_n), len(breeds), len(names)
