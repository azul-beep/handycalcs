"""Cozy Paws: carruseles para Instagram y Facebook (sin Claude, con plantillas de la marca).

CARRUSELES es la lista. Cada uno: portada (gancho), 3 a 6 diapositivas de contenido y cierre ("guardalo").
render(site_dir) arma las imágenes 1080x1350 en site/img/carrusel/<id>/<n>.jpg (la llama build.py).
social.py publica uno en el turno de contenido (1 PM Utah) los martes, jueves y sábados.
Para sumar carruseles: agregar entradas al final (id nuevo, que no cambie después).
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, 'data')
W, H = 1080, 1350
PLUM, BLUE, CREAM, CREAM2, GOLD, SAND = (59, 36, 51), (78, 127, 134), (243, 233, 215), (250, 244, 232), (200, 150, 46), (230, 214, 184)
INK = (80, 60, 70)
TERRA = (196, 112, 75)

CARRUSELES = [
    dict(id='k-gato-feliz', kicker='Cat language 101', titulo='6 signs your cat is happy with you',
         items=[('Slow blinks', 'A slow blink is a cat smile. It means they feel safe with you.'),
                ('Kneading', 'Making biscuits on your lap is a comfort habit from kittenhood.'),
                ('Tail up', 'A tail held high when they greet you is a happy hello.'),
                ('Headbutts', 'Bunting marks you with their scent. You belong to them now.'),
                ('Showing the belly', 'It is a sign of trust. Not always an invitation for belly rubs, though.'),
                ('Following you around', 'Room to room, door to door. They just like your company.')],
         cierre_titulo='Try this', cierre='Give your cat a slow blink from across the room. Many cats blink right back.',
         caption='How many of these does your cat do? 🐱💛 Comment the number below. (Bonus points if they headbutt you every morning.)',
         tags='#catmom #catlover #catsofinstagram #catbehavior #catlife'),
    dict(id='k-paseo-invierno', kicker='Cold weather care', titulo='Winter walk checklist for your dog',
         items=[('Shorter walks on cold days', 'Two short walks beat one long one when temperatures drop.'),
                ('Wipe the paws', 'Road salt and de-icers dry out pads, and dogs lick them off later.'),
                ('A coat for some pups', 'Small, senior and short-haired dogs get cold fast.'),
                ('Stay visible', 'It gets dark early. A reflective leash or a clip-on light helps.'),
                ('Check between the toes', 'Snow and ice balls get stuck there and hurt.')],
         cierre_titulo='Head home when', cierre='your dog lifts their paws, shivers or slows down. Warm up, then try again later.',
         caption='Cold weather is here ❄️🐾 Save this checklist for your next winter walk. Does your dog wear a coat or a sweater?',
         tags='#dogmom #doglover #dogsofinstagram #winterdog #dogwalk'),
    dict(id='k-solo-perros', kicker='Just dog people things', titulo='Things only dog people understand',
         items=[('Spelling W-A-L-K', 'And they still know. Every single time.'),
                ('Every snack is shared', 'Apparently. According to the face at your knee.'),
                ('Sorry, buddy', 'You step on their tail and apologize like you hurt a person. Because you did.'),
                ('Your camera roll', 'Ninety percent one face. Zero regrets.')],
         cierre_titulo='Tag a dog person', cierre='Send this to the friend who talks to their dog like a roommate.',
         caption='Which one is the most true at your house? 😂🐶 Tag a dog person who needs to see this.',
         tags='#dogmom #doglover #dogsofinstagram #doglife #dogpeople'),
    dict(id='k-comidas-toxicas', kicker='Save this before the holidays', titulo='5 holiday foods your dog should never eat',
         items=[('Chocolate', 'The darker it is, the more dangerous. Keep cookie plates and advent calendars up high.'),
                ('Grapes and raisins', 'Even a few can hurt a dog\'s kidneys. Watch out for fruitcake and trail mix.'),
                ('Xylitol', 'A sweetener in sugar-free gum, candy and some peanut butters. Read the label.'),
                ('Onions and garlic', 'Raw, cooked or powdered. Skip the stuffing and gravy scraps.'),
                ('Cooked bones', 'They splinter. Turkey and ham bones go straight in a closed trash can.')],
         cierre='If your dog eats something on this list, call your vet or the ASPCA Animal Poison Control line right away.',
         caption='Holiday kitchens are full of temptations. 🍫🍇 Save this list and share it with whoever is hosting this year. If your dog eats something on it, call your vet or the ASPCA Animal Poison Control line (888-426-4435) right away.',
         tags='#dogmom #doglover #dogsofinstagram #dogsafety #holidaytips #petparents'),
    dict(id='k-solo-gatos', kicker='Just cat people things', titulo='Things only cat people understand',
         items=[('The box wins', 'You bought the fancy bed. They chose the box it came in.'),
                ('3 AM zoomies', 'Not random. A scheduled event.'),
                ('Gravity tests', 'Anything on the table must be checked. From the floor.'),
                ('Reserved seating', 'Your lap is taken, especially when you need to get up.')],
         cierre_titulo='Tag a cat person', cierre='Send this to the friend whose cat runs the house.',
         caption='Cat people, you know. 😹 Which one happened at your house this week?',
         tags='#catmom #catlover #catsofinstagram #catlife #catpeople'),
    dict(id='k-arbol-seguro', kicker='Holiday prep', titulo='Make your Christmas tree pet-safe in 5 steps',
         items=[('Anchor it', 'Use a heavy base or tie it to the wall. Climbing cats and wagging tails happen.'),
                ('Skip the tinsel', 'Cats love it, and swallowed tinsel can cause serious tummy trouble.'),
                ('Fragile ornaments up high', 'Glass and salt-dough ornaments go on the top branches, out of reach.'),
                ('Cover the tree water', 'It can hold sap and preservatives. Keep curious pets from drinking it.'),
                ('Hide the cords', 'Use cord covers and unplug the lights when nobody is home.')],
         cierre_titulo='Merry and safe', cierre='A tree that stays standing is the best gift for everyone in the house, pets included.',
         caption='Tree season is here! 🎄 Five easy ways to keep it pet-proof. Save this for decorating day, and tell us: does your cat climb the tree? 😹',
         tags='#petchristmas #catsofinstagram #dogsofinstagram #christmastree #petparents'),
    dict(id='k-plantas-gatos', kicker='Before you buy flowers', titulo='Holiday plants and cats: what to know',
         items=[('Lilies', 'Very toxic to cats, even the pollen or the water in the vase. Keep them out of a cat home.'),
                ('Poinsettias', 'Mildly irritating. They can upset a cat\'s stomach if chewed.'),
                ('Mistletoe and holly', 'Can cause vomiting and tummy trouble. Hang and place them out of reach.'),
                ('Cat-friendly picks', 'Christmas cactus, orchids and roses are on the ASPCA non-toxic list.')],
         cierre_titulo='Not sure?', cierre='Check the ASPCA list of toxic and non-toxic plants before bringing a new plant home.',
         caption='Holiday flower season 🌸🐱 Save this before you buy a bouquet. Lilies are the big one to avoid with cats. If your cat chews a toxic plant, call your vet right away.',
         tags='#catmom #catsofinstagram #catsafety #petchristmas #catlover'),
    dict(id='k-invitados', kicker='Hosting this season?', titulo='5 ways to keep your pet calm with guests',
         items=[('A quiet room', 'Their bed, water and a toy in a room where guests do not go.'),
                ('Same routine', 'Meals and walks at the usual times, even on busy days.'),
                ('House rules for guests', 'No table scraps, no chasing, let the pet come to them.'),
                ('Watch the door', 'Doors open a lot. Make sure the ID tag is on and up to date.'),
                ('Something to do', 'A long-lasting chew or a puzzle toy keeps them busy and relaxed.')],
         cierre_titulo='Remember', cierre='Not every pet loves a party, and that is okay. A calm pet makes a happier host.',
         caption='Party season = lots of new faces 🎉 Save these tips for your next get-together. Is your pet the host or the one hiding under the bed?',
         tags='#dogmom #catmom #petparents #holidaytips #dogsofinstagram'),
    dict(id='k-club-reglas', kicker='Cozy Paws Social Club', titulo='The official club rules',
         items=[('Naps are sacred', 'Do not disturb a sleeping pet. Or a sleeping human with a pet on top.'),
                ('Treats are a love language', 'Fluent speakers only.'),
                ('The good spot is taken', 'The warm corner of the couch has an owner. It is not you.'),
                ('Every walk is an adventure', 'Same street, new smells, every day.'),
                ('Pets are family', 'No exceptions. This one is not up for a vote.')],
         cierre_titulo='Welcome to the Club', cierre='If you nodded at all five, you are already a member. Tell us your pet\'s name below.',
         caption='Official Cozy Paws Social Club rules 📜🐾 Which one does your pet follow best? Introduce us to them in the comments!',
         tags='#cozypawsclub #dogmom #catmom #petlover #petsofinstagram'),
    dict(id='k-mimos-gratis', kicker='No shopping required', titulo='5 free ways to spoil your pet this Christmas',
         items=[('A new walking route', 'New smells are like a new book for a dog.'),
                ('A snuffle hunt', 'Hide their kibble around the house and let them find it.'),
                ('Ten minutes of brushing', 'Most pets love it, and it is great bonding time.'),
                ('A tree photo session', 'Treats in hand, phone ready, patience on.'),
                ('An extra-long cuddle', 'On the couch, with a blanket and a movie. Simple and perfect.')],
         cierre_titulo='The best gift', cierre='is time with you. Everything else is a bonus.',
         caption='The best things for our pets are often free 🎁🐾 Which one will you do this week? Save this for the holidays.',
         tags='#dogmom #catmom #petsofinstagram #petchristmas #petparents'),
]


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


def _fit(d, text, kind, width, max_h, start, minimum=30, spacing=1.2):
    size = start
    while size > minimum:
        f = _font(kind, size)
        lines = _wrap(d, text, f, width)
        if len(lines) * size * spacing <= max_h:
            return f, lines, size
        size -= 4
    f = _font(kind, minimum)
    return f, _wrap(d, text, f, width), minimum


def _paw(d, x, y, s, color):
    d.ellipse((x, y + 0.55 * s, x + s, y + 1.4 * s), fill=color)
    for dx, dy in ((-0.38, 0), (0.08, -0.38), (0.62, -0.38), (1.08, 0)):
        d.ellipse((x + dx * s, y + dy * s, x + (dx + 0.42) * s, y + (dy + 0.5) * s), fill=color)


def _base(bg=CREAM, pat=SAND):
    from PIL import Image, ImageDraw
    im = Image.new('RGB', (W, H), bg)
    d = ImageDraw.Draw(im)
    for i, (x, y) in enumerate(((70, 90), (930, 160), (110, 1150), (900, 1180), (980, 640), (40, 620))):
        _paw(d, x, y, 34 if i % 2 else 26, pat)
    return im, d


def _pie(im, d, n, total, claro=False):
    from PIL import Image
    col = CREAM if claro else PLUM
    logo = Image.open(os.path.join(DATA, 'brand', 'logo-160.png')).convert('RGBA').resize((72, 72))
    sf = _font('script', 50)
    x0 = 70
    im.paste(logo, (x0, H - 125), logo)
    d.text((x0 + 88, H - 118), 'Cozy Paws', font=sf, fill=col)
    # puntitos de avance
    r, gap = 9, 30
    x = W - 70 - (total - 1) * gap
    for i in range(total):
        c = (GOLD if i == n else ((120, 95, 110) if claro else SAND))
        d.ellipse((x + i * gap - r, H - 89 - r, x + i * gap + r, H - 89 + r), fill=c)


def _centered(d, lines, font, size, top, color, spacing=1.2):
    y = top
    for ln in lines:
        d.text(((W - d.textlength(ln, font=font)) / 2, y), ln, font=font, fill=color)
        y += size * spacing
    return y


def portada(c, total):
    im, d = _base(PLUM, (85, 58, 76))
    d.rounded_rectangle((70, 70, W - 70, H - 170), 40, outline=GOLD, width=5)
    kf = _font('script', 64)
    _centered(d, [c['kicker']], kf, 64, 190, GOLD)
    tf, tl, ts = _fit(d, c['titulo'], 'title', W - 260, 640, 118, 60, 1.12)
    y = 330 + max(0, (640 - len(tl) * ts * 1.12) / 2)
    _centered(d, tl, tf, ts, y, CREAM, 1.12)
    sw = _font('title', 40)
    t = 'Swipe'
    tw = d.textlength(t, font=sw)
    d.rounded_rectangle(((W - 320) / 2, 1030, (W + 320) / 2, 1110), 40, fill=GOLD)
    x = (W - tw - 60) / 2
    d.text((x, 1046), t, font=sw, fill=PLUM)
    ax = x + tw + 22
    d.line((ax, 1072, ax + 38, 1072), fill=PLUM, width=5)
    d.polygon([(ax + 40, 1072), (ax + 24, 1060), (ax + 24, 1084)], fill=PLUM)
    _pie(im, d, 0, total, claro=True)
    return im


def item(c, i, total):
    nombre, texto = c['items'][i]
    im, d = _base()
    d.rounded_rectangle((70, 70, W - 70, H - 170), 40, fill=CREAM2, outline=GOLD, width=5)
    color = [BLUE, TERRA, PLUM][i % 3]
    top, bottom = 140, H - 250
    tf, tl, ts = _fit(d, nombre, 'title', W - 280, 260, 100, 56, 1.12)
    bf, bl, bs = _fit(d, texto, 'body', W - 280, 420, 58, 34, 1.4)
    r = 100
    block = 2 * r + 60 + len(tl) * ts * 1.12 + 70 + len(bl) * bs * 1.4 + 110
    y = top + max(0, (bottom - top - block) / 2)
    cx, cy = W / 2, y + r
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=color)
    nf = _font('title', 120)
    s = str(i + 1)
    bb = d.textbbox((0, 0), s, font=nf)
    d.text((cx - (bb[2] - bb[0]) / 2 - bb[0], cy - (bb[3] - bb[1]) / 2 - bb[1]), s, font=nf, fill=CREAM)
    y = _centered(d, tl, tf, ts, y + 2 * r + 60, PLUM, 1.12)
    d.line(((W - 120) / 2, y + 28, (W + 120) / 2, y + 28), fill=GOLD, width=5)
    y = _centered(d, bl, bf, bs, y + 70, INK, 1.4)
    for k in range(3):
        _paw(d, W / 2 - 80 + k * 70, y + 50, 22, color if k == 1 else SAND)
    _pie(im, d, i + 1, total)
    return im


def cierre(c, total):
    im, d = _base(BLUE, (98, 146, 152))
    d.rounded_rectangle((70, 70, W - 70, H - 170), 40, outline=CREAM, width=5)
    sf = _font('script', 96)
    _centered(d, [c.get('cierre_titulo', 'Good to know')], sf, 96, 210, GOLD)
    bf, bl, bs = _fit(d, c['cierre'], 'body', W - 300, 380, 50, 32, 1.4)
    y = _centered(d, bl, bf, bs, 380, CREAM, 1.4)
    tf = _font('title', 64)
    y = max(y + 90, 860)
    _centered(d, ['Save it  ·  Share it'], tf, 64, y, CREAM)
    uf = _font('body', 40)
    _centered(d, ['@cozypawsgifts'], uf, 40, y + 110, GOLD)
    _pie(im, d, total - 1, total, claro=True)
    return im


def slides(c):
    total = len(c['items']) + 2
    return [portada(c, total)] + [item(c, i, total) for i in range(len(c['items']))] + [cierre(c, total)]


def caption_de(c):
    return f"{c['caption']}\n\n{c['tags']} #cozypaws #cozypawssocialclub"


V = '1'  # subir si cambia la plantilla, para rehacer todas las imágenes


def render(site_dir):
    """Arma las diapositivas en site/img/carrusel/<id>/<n>.jpg. Guarda copia en data/carrusel/ para no rehacerlas."""
    import hashlib, json, shutil
    for c in CARRUSELES:
        clave = hashlib.md5((V + json.dumps(c, sort_keys=True)).encode()).hexdigest()[:10]
        cache = os.path.join(DATA, 'carrusel', f"{c['id']}-{clave}")
        if not os.path.isdir(cache):
            os.makedirs(cache)
            for n, im in enumerate(slides(c), 1):
                im.save(os.path.join(cache, f'{n}.jpg'), quality=88)
        out = os.path.join(site_dir, 'img', 'carrusel', c['id'])
        shutil.rmtree(out, ignore_errors=True)
        shutil.copytree(cache, out)


def fotos(c):
    """Cantidad de diapositivas de un carrusel."""
    return len(c['items']) + 2


if __name__ == '__main__':
    import sys
    render(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'site'))
