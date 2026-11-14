"""Cozy Paws: posts que no son de venta (tips, frases, Social Club, "¿perro o gato?") e historias, sin Claude.

BANCO es la lista de textos. social.py los publica en orden, uno por día, y cuando se terminan vuelve a empezar.
Para sumar textos, agregar entradas al final de BANCO (el id tiene que ser nuevo y no cambiar después).

render(site_dir, live_prods) arma las imágenes con plantillas (la llama build.py en cada corrida):
  site/img/social/<id>.jpg       post cuadrado 1080x1080
  site/img/social/<id>-story.jpg historia 1080x1920
  site/img/story/<sku>.jpg       historia "New in the shop" de cada producto a la venta
Las imágenes quedan guardadas en data/social/ para no rehacerlas en cada corrida.
"""
import hashlib, os, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, 'data')
CACHE = os.path.join(DATA, 'social')
V = '2'  # subir si cambia la plantilla, para rehacer todas las imágenes

PLUM, BLUE, CREAM, CREAM2, GOLD, SAND = (59, 36, 51), (78, 127, 134), (243, 233, 215), (250, 244, 232), (200, 150, 46), (230, 214, 184)

# tipo: tip (título + texto), frase, club, pregunta. "texto" va en la imagen; "caption" es el texto del post.
BANCO = [
    dict(id='t-agua-invierno', tipo='tip', titulo='Winter water check', texto='Pets drink less when it\'s cold. Refresh the bowl twice a day and keep it away from drafty doors.',
         caption='Little winter reminder: pets often drink less when it gets cold. Fresh water twice a day keeps them happy and hydrated. 💧', tags='dog cat'),
    dict(id='q-perro-o-gato', tipo='pregunta', texto='Dog person or cat person?', sub='(or proudly both)',
         caption='The eternal question. Tell us in the comments: 🐶 or 🐱 ... or both? 🐾', tags='dog cat'),
    dict(id='f-hogar', tipo='frase', texto='Home is wherever my dog is waiting at the door.',
         caption='Nothing beats that welcome. 🐾 Tag someone whose dog waits by the door.', tags='dog'),
    dict(id='c-bienvenida', tipo='club', titulo='Welcome to the Club', texto='The Cozy Paws Social Club is for people who plan their weekends around naps, walks and treats. Membership: one pet (or five).',
         caption='Welcome to the Cozy Paws Social Club ☕🐾 Original designs for dog and cat people, designed in Salt Lake City. Tell us your pet\'s name below so we can say hi!', tags='dog cat'),
    dict(id='t-chocolate', tipo='tip', titulo='Holiday treats to skip', texto='Chocolate, grapes, raisins, xylitol and onions are toxic for dogs. Keep the cookie plate up high.',
         caption='Holiday season = treats everywhere. Keep chocolate, grapes, raisins, onions and anything with xylitol out of reach. 🍫🚫 Save this for later!', tags='dog'),
    dict(id='f-gato-casa', tipo='frase', texto='My cat lets me live here. It\'s a good arrangement.',
         caption='Cat people know. 😼 Who\'s really in charge at your house?', tags='cat'),
    dict(id='q-nombre', tipo='pregunta', texto='What\'s your pet\'s name?', sub='We want to meet them',
         caption='Introduce us! Drop your pet\'s name (and a photo if you want) in the comments. 🐾', tags='dog cat'),
    dict(id='t-arbol', tipo='tip', titulo='Pet-safe Christmas tree', texto='Anchor the tree, skip tinsel, hang glass ornaments up high and keep the water bowl covered.',
         caption='Making the tree pet-proof: anchor it, skip the tinsel, hang the fragile ornaments high and cover the tree stand water. 🎄', tags='dog cat christmas'),
    dict(id='f-perro-terapia', tipo='frase', texto='Dogs don\'t fix everything. But they make everything better.',
         caption='Facts. 🐶❤️', tags='dog'),
    dict(id='c-domingos', tipo='club', titulo='Club rules', texto='1. Naps are sacred. 2. Treats are a love language. 3. The good spot on the couch is already taken.',
         caption='Official Cozy Paws Social Club rules 📜 Which one is the most true at your house?', tags='dog cat'),
    dict(id='t-patas-sal', tipo='tip', titulo='Paws vs. winter salt', texto='Wipe your dog\'s paws after winter walks. Road salt dries and cracks pads, and they lick it off.',
         caption='Winter walk tip: wipe those paws when you get home. Road salt and de-icers irritate pads, and pups lick them clean. 🐾❄️', tags='dog'),
    dict(id='q-duerme', tipo='pregunta', texto='Does your pet sleep in your bed?', sub='Be honest',
         caption='No judgment here. 😴 Does your dog or cat sleep in your bed? Yes / No / They own the bed', tags='dog cat'),
    dict(id='f-ronroneo', tipo='frase', texto='A purring cat on your lap is the best kind of therapy.',
         caption='Instant calm. 🐱💤', tags='cat'),
    dict(id='t-estres-fiestas', tipo='tip', titulo='Party season, calm pets', texto='Give your pet a quiet room with their bed and water when guests come over. Not every pet loves a crowd.',
         caption='Hosting this season? Set up a quiet room for your pet with their bed, water and a toy. Some pets love a party, many don\'t. 🎉', tags='dog cat'),
    dict(id='c-cafe', tipo='club', titulo='Morning ritual', texto='Coffee for you, breakfast for them, five minutes of cuddles for everyone.',
         caption='The only morning routine that matters ☕🐾 What does yours look like?', tags='dog cat'),
    dict(id='q-raza', tipo='pregunta', texto='What breed is your best friend?', sub='Mutts welcome',
         caption='Golden? Frenchie? Doodle? Proud mix? Tell us your dog\'s breed (or your cat\'s!) in the comments. 🐕🐈', tags='dog cat'),
    dict(id='f-mama', tipo='frase', texto='Not just a pet. Family.',
         caption='Say it louder for the people in the back. 🐾❤️', tags='dog cat'),
    dict(id='t-gatos-plantas', tipo='tip', titulo='Plants cats should avoid', texto='Lilies are very toxic to cats, and poinsettias and mistletoe upset tummies. Choose cat-safe flowers.',
         caption='Holiday flower alert 🌸 Lilies are extremely toxic to cats. Poinsettias and mistletoe can upset tummies too. Pick cat-safe bouquets this season.', tags='cat christmas'),
    dict(id='q-juguete', tipo='pregunta', texto='Favorite toy or the box it came in?', sub='We know the answer',
         caption='Every cat parent knows how this ends. 📦😹 What\'s your pet\'s favorite "toy" that isn\'t a toy?', tags='cat dog'),
    dict(id='f-paseo', tipo='frase', texto='The best conversations happen on long walks with your dog.',
         caption='Sunday walk energy. 🍂🐶', tags='dog'),
    dict(id='c-hecho', tipo='club', titulo='Designed in Salt Lake City', texto='Every Cozy Paws design is created by us and printed on demand in the USA by our production partners, so nothing goes to waste.',
         caption='A little about us: every Cozy Paws design is original, designed in Salt Lake City and printed on demand in the USA by our production partners. 🏔️🐾 Thank you for supporting a small shop!', tags='dog cat'),
    dict(id='t-viejitos', tipo='tip', titulo='Senior pets in the cold', texto='Older pets feel the cold more. A thick bed off the floor and a sweater for short-haired dogs help a lot.',
         caption='Senior pets feel the cold in their joints. A raised, cozy bed and a sweater for short-haired pups make winter so much easier. 🧣', tags='dog cat'),
    dict(id='q-navidad', tipo='pregunta', texto='Does your pet get a Christmas gift?', sub='Of course they do',
         caption='Asking for science 🎁 Does your pet get a gift (or a stocking) at Christmas?', tags='dog cat christmas'),
    dict(id='f-gato-ventana', tipo='frase', texto='Every window is a TV show if you\'re a cat.',
         caption='Today\'s episode: birds. 🐦🐱', tags='cat'),
    dict(id='t-identificacion', tipo='tip', titulo='Check the ID tag', texto='Doors open a lot during the holidays. Make sure your pet\'s tag and microchip info are up to date.',
         caption='Busy season, open doors. 🚪 Take one minute today to check your pet\'s ID tag and microchip details. Future you will thank you.', tags='dog cat'),
    dict(id='c-gracias', tipo='club', titulo='Thank you, Club', texto='Every order, like and share helps a tiny pet shop keep drawing. We see you and we\'re grateful.',
         caption='From all of us (and our very supervising pets): thank you for being here. 🧡🐾', tags='dog cat'),
]

TAGS = {'dog': '#doglover #dogmom', 'cat': '#catlover #catmom', 'christmas': '#petchristmas'}


def caption_de(item):
    tags = []
    for t in item.get('tags', '').split():
        tags += TAGS.get(t, '').split()
    tags = list(dict.fromkeys(tags)) + ['#cozypaws', '#cozypawssocialclub']
    return f"{item['caption']}\n\n{' '.join(tags)}"


def _font(kind, size):
    from PIL import ImageFont
    f = {'script': 'Yesteryear-Regular.ttf', 'title': 'AbrilFatface-Regular.ttf', 'body': 'Lora.ttf'}[kind]
    return ImageFont.truetype(os.path.join(DATA, 'fonts', f), size)


def _wrap(d, text, font, width):
    words, lines, cur = text.split(), [], ''
    for w in words:
        t = (cur + ' ' + w).strip()
        if d.textlength(t, font=font) <= width:
            cur = t
        else:
            lines.append(cur); cur = w
    if cur:
        lines.append(cur)
    return lines


def _fit(d, text, kind, width, max_h, start, minimum=30, spacing=1.25):
    size = start
    while size > minimum:
        f = _font(kind, size)
        lines = _wrap(d, text, f, width)
        if len(lines) * size * spacing <= max_h:
            return f, lines, size
        size -= 4
    f = _font(kind, minimum)
    return f, _wrap(d, text, f, width), minimum


def _paws(im, color=SAND):
    from PIL import ImageDraw
    d = ImageDraw.Draw(im)
    for y in range(40, im.height, 170):
        for x in range(40 + (85 if (y // 170) % 2 else 0), im.width, 170):
            d.ellipse((x, y + 14, x + 26, y + 36), fill=color)
            for dx, dy in ((-10, 0), (2, -10), (16, -10), (28, 0)):
                d.ellipse((x + dx, y + dy, x + dx + 11, y + dy + 13), fill=color)


def _centered(d, lines, font, size, top, W, color, spacing=1.25):
    y = top
    for ln in lines:
        d.text(((W - d.textlength(ln, font=font)) / 2, y), ln, font=font, fill=color)
        y += size * spacing
    return y


def _card(item, W, H):
    from PIL import Image, ImageDraw
    im = Image.new('RGB', (W, H), CREAM)
    _paws(im)
    d = ImageDraw.Draw(im)
    m = 60
    d.rounded_rectangle((m, m, W - m, H - m), 36, fill=CREAM2, outline=GOLD, width=6)
    d.rounded_rectangle((m + 16, m + 16, W - m - 16, H - m - 16), 28, outline=(226, 205, 160), width=2)
    label = {'tip': 'Pet care tip', 'frase': 'Cozy thought', 'club': 'Cozy Paws Social Club', 'pregunta': 'Tell us'}[item['tipo']]
    k = 1.0 if H == W else 1.3  # en historias (9:16) todo un poco más grande
    lf = _font('title', int(34 * k))
    top = m + 90 if H == W else m + 230
    lw = d.textlength(label.upper(), font=lf)
    d.text(((W - lw) / 2, top), label.upper(), font=lf, fill=BLUE)
    d.line(((W - 120) / 2, top + 62 * k, (W + 120) / 2, top + 62 * k), fill=GOLD, width=4)
    inner_w = W - 2 * m - 140
    bottom = H - m - (230 if H == W else 470)
    y0 = top + 110 * k
    if item['tipo'] in ('tip', 'club'):
        tf, tl, ts = _fit(d, item['titulo'], 'title', inner_w, 230 * k, int(88 * k), 48, 1.15)
        th = len(tl) * ts * 1.15 + 36
        bf, bl, bs = _fit(d, item['texto'], 'body', inner_w, bottom - y0 - th, int(50 * k), 30, 1.4)
        block = th + len(bl) * bs * 1.4
        y = y0 + max(0, (bottom - y0 - block) / 2)
        y = _centered(d, tl, tf, ts, y, W, PLUM, 1.15) + 36
        _centered(d, bl, bf, bs, y, W, (80, 60, 70), 1.4)
    else:
        sub_h = 110 if item.get('sub') else 0
        f, lines, s = _fit(d, item['texto'], 'title', inner_w, bottom - y0 - sub_h, int(104 * k), 52, 1.18)
        block = len(lines) * s * 1.18 + sub_h
        y = y0 + max(0, (bottom - y0 - block) / 2)
        y = _centered(d, lines, f, s, y, W, PLUM, 1.18)
        if item.get('sub'):
            sf = _font('script', int(64 * k))
            sw = d.textlength(item['sub'], font=sf)
            d.text(((W - sw) / 2, y + 20), item['sub'], font=sf, fill=BLUE)
    # pie: logo + marca
    logo = Image.open(os.path.join(DATA, 'brand', 'logo-160.png')).convert('RGBA').resize((110, 110))
    fy = H - m - (170 if H == W else 380)
    sf = _font('script', 72)
    brand = 'Cozy Paws'
    bw = d.textlength(brand, font=sf)
    x0 = (W - (110 + 24 + bw)) / 2
    im.paste(logo, (int(x0), int(fy)), logo)
    d.text((x0 + 134, fy + 8), brand, font=sf, fill=PLUM)
    if H != W:
        uf = _font('body', 38)
        u = 'cozypawsgifts.pages.dev'
        d.text(((W - d.textlength(u, font=uf)) / 2, fy + 150), u, font=uf, fill=BLUE)
    return im


def _story_producto(p, img_path):
    from PIL import Image, ImageDraw
    W, H = 1080, 1920
    im = Image.new('RGB', (W, H), CREAM)
    _paws(im)
    d = ImageDraw.Draw(im)
    sf = _font('script', 120)
    t = 'New in the shop'
    d.text(((W - d.textlength(t, font=sf)) / 2, 170), t, font=sf, fill=PLUM)
    d.line(((W - 160) / 2, 345, (W + 160) / 2, 345), fill=GOLD, width=5)
    prod = Image.open(img_path).convert('RGB').resize((860, 860))
    mask = Image.new('L', prod.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, 859, 859), 40, fill=255)
    d.rounded_rectangle((104, 404, 976, 1276), 48, fill=GOLD)
    im.paste(prod, (110, 410), mask)
    tf, tl, ts = _fit(d, p['short'], 'title', 880, 200, 76, 44, 1.15)
    y = _centered(d, tl, tf, ts, 1340, W, PLUM, 1.15)
    pf = _font('body', 50)
    pr = f"${p['precio']}" if p.get('precio') else ''
    if pr:
        d.text(((W - d.textlength(pr, font=pf)) / 2, y + 10), pr, font=pf, fill=BLUE)
    d.rectangle((0, H - 280, W, H), fill=BLUE)
    bf = _font('title', 52)
    for i, line in enumerate(('Link in bio', 'ShopCozyPaws on Etsy')):
        f = bf if i == 0 else _font('body', 42)
        d.text(((W - d.textlength(line, font=f)) / 2, H - 230 + i * 90), line, font=f, fill=CREAM2)
    return im


def _cached(key, out, make):
    os.makedirs(CACHE, exist_ok=True)
    h = hashlib.sha1((V + key).encode()).hexdigest()[:10]
    src = os.path.join(CACHE, f'{os.path.basename(out)[:-4]}-{h}.jpg')
    if not os.path.exists(src):
        for old in os.listdir(CACHE):  # borra versiones viejas de la misma imagen
            if old.startswith(os.path.basename(out)[:-4] + '-') and len(old) == len(os.path.basename(src)):
                os.remove(os.path.join(CACHE, old))
        make().save(src, quality=88, optimize=True)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    shutil.copy(src, out)


def render(site_dir, live_prods):
    for it in BANCO:
        key = repr(sorted(it.items()))
        _cached(key, os.path.join(site_dir, 'img', 'social', it['id'] + '.jpg'), lambda it=it: _card(it, 1080, 1080))
        _cached(key, os.path.join(site_dir, 'img', 'social', it['id'] + '-story.jpg'), lambda it=it: _card(it, 1080, 1920))
    for p in live_prods:
        src = os.path.join(DATA, 'img', p['sku'] + '.jpg')
        if os.path.exists(src):
            key = p['short'] + p.get('precio', '') + str(os.path.getsize(src))
            _cached(key, os.path.join(site_dir, 'img', 'story', p['sku'] + '.jpg'), lambda p=p, src=src: _story_producto(p, src))
