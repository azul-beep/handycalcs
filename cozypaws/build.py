#!/usr/bin/env python3
"""Cozy Paws: web de guías de regalos + herramientas para dueños de mascotas + RSS para Pinterest.

Objetivo: traer tráfico gratis a la tienda de Etsy (Google + Pinterest) sin depender de Claude.

  python3 cozypaws/build.py [--hoy 2026-11-20]   -> escribe cozypaws/site/

Goteo (regla de Azu: de a poco): cada producto aparece en la web y en el RSS el día DESPUÉS de su
fecha de carga en Etsy (columna dia de data/productos.csv), así el link de Etsy ya existe.
Cada guía aparece cuando tiene al menos 2 productos visibles. Las herramientas tienen fecha fija.
GitHub Actions corre esto todos los días (.github/workflows/cozypaws.yml) y publica solo.

Para cambiar algo, tocar CONFIG. Links directos de Etsy: data/etsy-links.txt ("<sku> <url>" por línea);
si un producto no tiene link directo, el botón lleva a la búsqueda dentro de la tienda.
"""
import argparse, csv, datetime as dt, html, json, os, re, shutil
from email.utils import format_datetime
from urllib.parse import quote_plus

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, 'data')
OUT = os.path.join(HERE, 'site')

ETSY_AUTH_HTML = """<!doctype html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow">
<meta name="referrer" content="no-referrer"><title>Cozy Paws · Etsy</title>
<style>body{font-family:system-ui,sans-serif;max-width:34rem;margin:3rem auto;padding:0 1rem;color:#22282A;line-height:1.5}
a.b{display:inline-block;background:#22282A;color:#fff;padding:.8rem 1.2rem;border-radius:.6rem;text-decoration:none;font-weight:600}</style>
</head><body><h1>Cozy Paws · Etsy</h1><p id="m">Un segundo...</p><p id="b"></p>
<script>
var q=new URLSearchParams(location.search),c=q.get('code'),m=document.getElementById('m');
if(c){var u='https://github.com/azul-beep/crux-report/issues/new?title=etsy-code&body='+encodeURIComponent('code: '+c);
m.textContent='Etsy dio el permiso. Ahora en GitHub tocá "Create" (o "Submit new issue") y listo.';
document.getElementById('b').innerHTML='<a class="b" href="'+u+'">Ir a GitHub</a>';
history.replaceState(null,'',location.pathname);location.replace(u);}
else{m.textContent='Etsy no dio el permiso'+(q.get('error')?' ('+q.get('error')+')':'')+'. Volvé a tocar el link del mail de GitHub.';}
</script></body></html>
"""

CONFIG = dict(
    name='Cozy Paws',
    url='https://cozypawsgifts.pages.dev',          # dirección de Cloudflare Pages (cambiar si se compra dominio)
    shop='https://www.etsy.com/shop/ShopCozyPaws',  # tienda de Etsy (shopcozypaws.etsy.com)
    pinterest='https://www.pinterest.com/cozypawsgifts/',          # https://www.pinterest.com/<usuario>/ cuando exista
    ga4='G-1RSXP3PFR4',                # G-XXXXXXX (GA4 de esta web)
    pixel='',              # ID del Pixel de Meta
    instagram='https://www.instagram.com/cozypawsgifts/',
    facebook='https://www.facebook.com/profile.php?id=61596427566616',
    maker='Azu',
    maker_photo_alt='Azu as a kid hugging her Doberman, Aaron',
    maker_photo_caption='Me as a kid with Aaron, my Doberman. Dogs have been family for as long as I can remember.',  # foto principal = la primera de data/autora/
    pinterest_verify='c84a6e3acb398fb108d0538381e88517',   # contenido de la etiqueta meta "p:domain_verify" para reclamar la web en Pinterest
    google_verify='snG6WI_Ay90gukuDRtPKQLCo42mUWLXTbusn-InyaTk',      # contenido de la meta "google-site-verification" (Search Console), si se usa
    contact='support@skyesolutionsai.com',
    company='Skye Solutions AI',
    christmas_cutoff=dt.date(2026, 12, 10),
    adsense='ca-pub-1174178180336933',   # AdSense de Azu (Skye Solutions AI)
    adsense_on=False,
    # MailerLite: URL "action" del formulario incrustado "Cozy Paws Club" (https://assets.mailerlite.com/jsonp/2793611/forms/<id>/subscribe).
    # Vacío = no se muestra el formulario. Al pegarla aparece la caja "Join the club" con el regalo (checklist PDF de data/gift/).
    mailerlite_action='https://assets.mailerlite.com/jsonp/2793611/forms/204177339414742657/subscribe',
    # Cuentas de las apps (Firebase, plan Spark gratis). Pegar acá el firebaseConfig de la consola (es público, no es secreto).
    # Vacío = apps sin cuenta (todo se guarda en el equipo). Ej: dict(apiKey='...', authDomain='cozy-paws-apps.firebaseapp.com', projectId='cozy-paws-apps', appId='...')
    firebase=dict(apiKey='AIzaSyBPa_WnI7oIRvY2_SCEmD9fc69c8xWO8Rk', authDomain='cozy-paws-apps.firebaseapp.com', projectId='cozy-paws-apps',
                  storageBucket='cozy-paws-apps.firebasestorage.app', messagingSenderId='446269425804', appId='1:446269425804:web:610e8167392f671bc093a9'),                    # True SOLO cuando AdSense apruebe cozypawsgifts.pages.dev: carga anuncios en las apps y publica ads.txt
)
E = html.escape
INDEXNOW_KEY = "92ad20c14927840aeb27fd01e77c8677"  # clave pública de IndexNow (Bing y otros); cozypaws/indexnow.py avisa las páginas nuevas

# ---------------------------------------------------------------- productos
KINDS = [  # (palabra en el título, tipo en inglés)
    ('printable', 'Printable (instant download)'), ('pajama', 'Pajama pants'), ('tank top', 'Pet tank top'),
    ('kids shirt', 'Kids T-shirt'), ('youth', 'Kids T-shirt'), ('wooden', 'Wooden ornament'), ('glass', 'Glass ornament'),
    ('ornament', 'Ceramic ornament'), ('accent mug', 'Accent mug'), ('latte mug', 'Latte mug'), ('enamel', 'Enamel camping mug'),
    ('tumbler', 'Insulated tumbler'), ('mug', 'Coffee mug'), ('bandana', 'Dog bandana'), ('dog sweater', 'Dog sweater'),
    ('dog hoodie', 'Dog hoodie'), ('pet blanket', 'Pet blanket'), ('dog blanket', 'Pet blanket'), ('blanket', 'Plush blanket'),
    ('socks', 'Socks'), ('beanie', 'Embroidered beanie'), ('hat', 'Embroidered hat'), ('cap', 'Embroidered cap'),
    ('tote', 'Tote bag'), ('hoodie', 'Sweatshirt'), ('sweatshirt', 'Sweatshirt'), ('shirt', 'T-shirt'), ('tee', 'T-shirt'),
    ('wrapping paper', 'Wrapping paper'), ('gift wrap', 'Wrapping paper'), ('sticker', 'Sticker sheet'), ('journal', 'Hardcover journal'),
    ('notebook', 'Spiral notebook'), ('calendar', '2027 wall calendar'), ('bowl', 'Pet bowl'), ('dish', 'Pet bowl'),
    ('coaster', 'Coaster set'), ('candle', 'Scented candle'), ('card', 'Greeting card'),
]


def kind_of(title):
    t = title.lower()
    for k, v in KINDS:
        if k in t:
            return v
    return 'Gift'


def short_title(title):
    return title.split(',')[0].strip()


def slug(s):
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')


def load_products(today):
    links = {}
    lp = os.path.join(DATA, 'etsy-links.txt')
    if os.path.exists(lp):
        for line in open(lp, encoding='utf-8'):
            m = re.match(r'\s*([\w-]+)\s+(https://\S+)', line)
            if m:
                links[m.group(1)] = m.group(2)
    out = []
    for r in csv.DictReader(open(os.path.join(DATA, 'productos.csv'), encoding='utf-8')):
        live = dt.date.fromisoformat(r['dia'])  # sale el mismo día que en Etsy (la web se arma a las 2 PM de Utah)
        st = short_title(r['titulo'])
        p = dict(r, live=live, short=st, kind=kind_of(r['titulo']), slug=slug(st) + '-' + slug(r['sku']),
                 tags=[t.strip() for t in r['etiquetas'].split(',') if t.strip()],
                 etsy=links.get(r['sku']) or f"{CONFIG['shop']}?search_query={quote_plus(st)}")
        p['hay'] = (r['titulo'] + ' ' + r['etiquetas']).lower()
        p['titulo_lower'] = r['titulo'].lower()
        if not p['texto']:
            p['texto'] = f"An original Cozy Paws design on a {p['kind'].lower()}. A cozy gift for people who love their pets like family, and an easy pick for Christmas, birthdays and new pet parents."
        out.append(p)
    visible = [p for p in out if p['live'] <= today]
    visible.sort(key=lambda p: (p['live'], p['sku']), reverse=True)
    return visible, out


# ---------------------------------------------------------------- guías de regalos (SEO)
GUIDES = [
    dict(id='dog-mom-gifts', h1='Gifts for Dog Moms', match=r'dog mom|dog mama|fur mama',
         intro='The dog mom in your life already has a closet full of leashes. What she does not have is something that says "this is who I am" every morning: a mug for her coffee, an ornament with this year on it, a soft sweatshirt for the walk at 6 AM. These are original designs, printed on demand in the USA, so each one is made when you order it.',
         tips=['Mugs and ornaments are the safest pick when you do not know her size.', 'Sweatshirts come in light and dark colors: pick the one she wears most.', 'Order by Dec 10 for Christmas delivery in the US.']),
    dict(id='dog-dad-gifts', h1='Gifts for Dog Dads', match=r'dog dad',
         intro='Dog dads are easy to spot: dog hair on the jacket, treats in every pocket. Give him something he will actually use, like a camping mug for the trail, a beanie for winter walks or a tee for the weekend.',
         tips=['A camping enamel mug is a great pick for outdoorsy dog dads.', 'Embroidered beanies and caps are one size fits most.']),
    dict(id='cat-mom-gifts', h1='Gifts for Cat Moms', match=r'cat mom|cat mama|cat lady|kitty mom',
         intro='For the cat mom who plans her day around naps (the cat\'s, not hers). Cute, simple designs on mugs, ornaments, notebooks and cozy layers that feel like a warm windowsill.',
         tips=['A cat mom ornament is a sweet stocking stuffer under $20.', 'Spiral notebooks and journals work for planners and list makers.']),
    dict(id='cat-dad-gifts', h1='Gifts for Cat Dads', match=r'cat dad',
         intro='Cat dads deserve their own merch. These designs keep it simple and a little funny, on mugs, caps and tees he will wear without being asked twice.',
         tips=['Caps and tees run true to size; check the size chart on Etsy.']),
    dict(id='golden-retriever-gifts', h1='Golden Retriever Mom Gifts', match=r'golden retriever',
         intro='Golden Retriever people are a club of their own: sunny dogs, endless fur and a tennis ball in every room. These gifts are made for proud Golden moms and dads.',
         tips=['Pair a Golden mug with a paw print ornament for a full gift set.']),
    dict(id='labrador-gifts', h1='Labrador Mom Gifts', match=r'labrador|\blab\b',
         intro='Black, yellow or chocolate, a Lab is family. Simple, original gifts for Labrador moms who start every day with a happy tail.',
         tips=['Mugs ship in about a week inside the US.']),
    dict(id='frenchie-gifts', h1='French Bulldog Mom Gifts', match=r'frenchie|french bulldog',
         intro='Big ears, bigger personality. Gifts for Frenchie moms who would never trade the snoring for anything.',
         tips=['A Frenchie mug is an easy gift for coworkers and friends.']),
    dict(id='german-shepherd-gifts', h1='German Shepherd Mom Gifts', match=r'german shepherd',
         intro='Loyal, smart and always on duty. Gifts for German Shepherd moms who are proud of their best working partner.',
         tips=['Add a card from the dog for a funny touch.']),
    dict(id='dachshund-gifts', h1='Dachshund Mom Gifts', match=r'dachshund|doxie|wiener',
         intro='Long dog, short legs, huge heart. Original gifts for Dachshund moms and doxie lovers.',
         tips=['Doxie mugs make a fun office gift.']),
    dict(id='doodle-gifts', h1='Doodle Mom Gifts', match=r'doodle',
         intro='Goldendoodle, Labradoodle or Bernedoodle, every doodle mom knows the curls and the grooming bills. These gifts celebrate the fluff.',
         tips=['Doodle sweatshirts come in light and dark colors.']),
    dict(id='christmas-gifts-for-dog-lovers', h1='Christmas Gifts for Dog Lovers', match=r'(christmas|woofmas|holiday|santa|nice list|ornament).*(dog|puppy|paw)|(dog|puppy|paw).*(christmas|woofmas|holiday|santa|nice list|ornament)',
         intro='A holiday gift list for anyone whose dog gets their own stocking. Ornaments, mugs, cozy layers and even gifts for the dog itself, all printed on demand in the USA.',
         tips=['Order by Dec 10 for Christmas delivery in the US.', 'Gift wrap and cards are in the shop too.']),
    dict(id='christmas-gifts-for-cat-lovers', h1='Christmas Gifts for Cat Lovers', match=r'(christmas|meowy|holiday|ornament).*(cat|kitty)|(cat|kitty).*(christmas|meowy|holiday|ornament)',
         intro='Meowy Christmas! Cat-themed ornaments, mugs and cozy gifts for the cat person on your list.',
         tips=['Order by Dec 10 for Christmas delivery in the US.']),
    dict(id='pet-christmas-ornaments', h1='Pet Christmas Ornaments', match=r'ornament',
         intro='A pet ornament is the kind of gift that comes back every December. Ceramic keepsakes with paw prints, cats and this year\'s date.',
         tips=['Ornaments are light, so they are great to mail to family.']),
    dict(id='dog-clothes-and-accessories', h1='Dog Bandanas, Sweaters and Pet Accessories', match=r'bandana|dog sweater|dog hoodie|pet blanket|pet bowl|dog bowl|cat bowl|good boy|good dog|good kitty',
         intro='Gifts for the pet itself: holiday bandanas for the photo, cozy layers for winter walks and bowls with personality.',
         tips=['Measure your dog\'s neck and chest before choosing a size.']),
    dict(id='cozy-winter-gifts-pet-lovers', h1='Cozy Winter Gifts for Pet Lovers', match=r'blanket|socks|beanie|sweatshirt|hoodie|candle',
         intro='Couch, blanket, dog on the feet. Cozy gifts for the coldest months: plush throws, socks, beanies, sweatshirts and candles.',
         tips=['Plush blankets come in several background colors; pick the one that matches the couch.']),
    dict(id='matching-dog-and-owner-outfits', h1='Matching Dog and Owner Christmas Outfits', match=r'matching',
         intro='The family photo is better when the dog matches. Dog hoodies, kids tees and plaid pajamas designed to be worn together, so the whole pack shows up in the same holiday spirit.',
         tips=['Order the dog size from its chest measurement, and the people sizes from the Etsy size chart.', 'Plaid pajamas come in women\'s and men\'s cuts.']),
    dict(id='first-christmas-and-memorial-ornaments', h1="Puppy's First Christmas and Pet Memorial Ornaments", match=r'first christmas|memorial',
         intro="Two moments that deserve an ornament: the first Christmas with a new puppy or kitten, and the first one without a pet who crossed the rainbow bridge. Simple keepsakes to hang every year.",
         tips=['A memorial ornament is a kind sympathy gift for a friend who lost a pet.', 'Ornaments are light and easy to mail.']),
    dict(id='printable-pet-gifts', h1='Printable Pet Gifts and Gift Tags', match=r'printable|instant download',
         intro='Last minute? Printables download right after purchase: "from the dog" gift tags, a 2027 pet calendar and a pet health planner. Print at home tonight.',
         tips=['Printables are digital: nothing ships, so they work even on Christmas Eve.']),
    dict(id='pet-lover-gifts-under-25', h1='Pet Lover Gifts Under $25', match=None, max_price=25,
         intro='Secret Santa, coworkers, teachers who love dogs: affordable gifts under $25 for pet people.',
         tips=['Stickers, cards and ornaments make great stocking stuffers.']),
    dict(id='pet-mugs', h1='Dog and Cat Mugs', match=r'mug|tumbler',
         intro='Coffee tastes better with a dog (or cat) on the mug. Classic white mugs, colored accent mugs, latte mugs, camping mugs and tumblers.',
         tips=['All ceramic mugs are dishwasher and microwave safe.']),
    # guías por tipo de dueño de perro (14 nov): 'desde' las pone después de la última guía ya programada, así no corren ninguna fecha
    dict(id='new-puppy-owner-gifts', h1='Gifts for New Puppy Owners', match=r"puppy's first|new puppy|puppy gift|puppy clothes|good dog pet bowl", desde=dt.date(2026, 12, 2),
         intro="A new puppy changes everything: the sleep, the floors, the camera roll. Celebrate the first Christmas together with a dated keepsake ornament, a bowl with personality and something soft for the crate.",
         tips=["A Puppy's First Christmas ornament with the year on it becomes a keepsake they hang every December.", 'Pair a gift for the owner with a gift for the puppy: it always lands.']),
    dict(id='funny-dog-lover-gifts', h1='Funny Gifts for Dog Lovers', match=r"sorry i.m late|dog sibling|santa.s favorite|card from the dog|from the dog", desde=dt.date(2026, 12, 3),
         intro="For the friend who is always late because the dog was comfy. Funny, kind designs that make dog people laugh at themselves, from sweatshirts to cards signed by the dog.",
         tips=['Funny tees and sweatshirts are perfect for white elephant and Secret Santa swaps.', 'A card "from the dog" is the cheapest way to make someone cry happy tears.']),
    dict(id='outdoorsy-dog-owner-gifts', solo_titulo=True, h1='Gifts for Outdoorsy Dog Owners', match=r'(camping|enamel|beanie|embroidered hat|baseball cap|tumbler|socks).*(dog|paw)|(dog|paw).*(camping|enamel|beanie|embroidered hat|baseball cap|tumbler|socks)', desde=dt.date(2026, 12, 4),
         intro="For the dog owner who hikes in the snow, camps with the pup and never skips the morning walk. Camping mugs, warm beanies, caps and travel tumblers built for the trail and the trailhead.",
         tips=['An enamel camping mug is light, tough and ready for the campfire.', 'Embroidered beanies and caps are one size fits most.']),
    dict(id='dog-lover-stocking-stuffers', solo_titulo=True, h1='Stocking Stuffers for Dog Lovers', match=r'dog|puppy|paw|woofmas', max_dog_price=20, desde=dt.date(2026, 12, 5),
         intro="Small gifts with big dog energy, all $20 or less: ornaments, socks, cards, stickers, gift tags and printables that fit in a stocking (or under a paw).",
         tips=['Printables are digital: buy them on Christmas Eve and print at home.', 'Ornaments and socks are the classic stocking stuffers.']),
    dict(id='pet-stationery-and-gift-wrap', h1='Pet Stationery, Cards and Gift Wrap', match=r'wrapping|gift wrap|sticker|journal|notebook|calendar|card',
         intro='Paper goods for pet people: wrapping paper with paw prints, sticker sheets, journals, notebooks, a 2027 calendar and holiday cards.',
         tips=['The 2027 calendar is a great gift for planners.']),
]


def guide_products(g, prods):
    key = 'titulo_lower' if g.get('solo_titulo') else 'hay'  # solo_titulo: las etiquetas de gatos a veces dicen "dog lover"
    if g.get('max_dog_price'):
        rx = re.compile(g['match'])
        return [p for p in prods if float(p['precio'] or 0) <= g['max_dog_price'] and rx.search(p[key])]
    if g.get('max_price'):
        return [p for p in prods if float(p['precio'] or 0) < g['max_price']]
    rx = re.compile(g['match'])
    return [p for p in prods if rx.search(p[key])]


def guide_live_date(g, all_prods):
    ps = sorted(guide_products(g, all_prods), key=lambda p: p['live'])
    if len(ps) < 2:
        return None
    return max(ps[1]['live'], g.get('desde', dt.date.min))


# ---------------------------------------------------------------- guía navideña principal para dueños de perros
# Una sola página grande que junta todo lo de perros por tipo de dueño, raza y presupuesto. Se arma sola cada día
# con los productos que ya están en Etsy (los que todavía no salieron no aparecen). Cada sección aparece cuando tiene productos.
HUB = dict(
    id='christmas-gift-guide-dog-owners', live=dt.date(2026, 11, 14),
    h1='Christmas Gift Guide for Dog Owners',
    title='Christmas Gift Guide for Dog Owners {y}: Ideas by Owner and Breed',
    desc='The {y} Christmas gift guide for dog people: gifts for dog moms, dog dads, new puppy owners, breed lovers and the dog itself, from stocking stuffers to cozy blankets.',
    intro="Shopping for someone whose dog gets their own stocking? This guide sorts our holiday gifts by the kind of dog person you are shopping for: the proud dog mom, the outdoorsy dog dad, the brand new puppy parent, the breed superfan and the friend who just said goodbye to a good dog. Every design is original, designed in Salt Lake City and printed on demand in the USA by our production partners, and new gifts are added every day until Christmas.",
    dog=r'\bdogs?\b|puppy|paw|woofmas|good boy|doodle|frenchie|golden retriever|labrador|dachshund|german shepherd',
    sections=[
        dict(id='dog-mom', h2='For the dog mom', match=r'dog mom|dog mama|fur mama', guide='dog-mom-gifts',
             text="She talks about her dog the way other people talk about their kids. Mugs for the first coffee of the day, a dated ornament, a soft sweatshirt for the 6 AM walk and a blanket for the couch the dog took over."),
        dict(id='dog-dad', h2='For the dog dad', match=r'dog dad|gift for him|for him', guide='dog-dad-gifts',
             text="Dog dads are hard to shop for until you remember the only thing they never stop talking about. Tees, beanies, caps and a camping mug he will actually use."),
        dict(id='breeds', h2='By breed', match=r'golden retriever|labrador|frenchie|french bulldog|german shepherd|dachshund|doodle', breeds=True,
             text="Breed people are a club of their own. Golden, Lab, Frenchie, German Shepherd, Dachshund or Doodle: a gift with their breed on it says you pay attention."),
        dict(id='for-the-dog', h2='Gifts for the dog itself', match=r'bandana|dog hoodie|dog sweater|pet blanket|dog blanket|pet bowl|food bowl|tank top|puppy clothes', guide='dog-clothes-and-accessories',
             text="Yes, the dog gets a present too. A holiday bandana for the photo, a warm hoodie for winter walks, a bowl with personality or a blanket of their own."),
        dict(id='matching', h2='Matching outfits for the family photo', match=r'matching|dog sibling', guide='matching-dog-and-owner-outfits',
             text="The holiday card is better when the dog matches. Dog hoodies, kids tees, tank tops and plaid pajamas designed to be worn together."),
        dict(id='new-puppy', h2='For new puppy owners', match=r"puppy's first|new puppy|puppy gift|puppy clothes|good dog pet bowl", guide='new-puppy-owner-gifts',
             text="The first Christmas with a new puppy only happens once. A dated keepsake ornament and a few practical things for a house that just got a lot louder."),
        dict(id='memorial', h2='For someone who lost a dog this year', match=r'memorial|pet loss|sympathy', guide='first-christmas-and-memorial-ornaments',
             text="The first Christmas without a dog is hard. A memorial ornament is a gentle way to say you remember, and it gets a spot on the tree every year."),
        dict(id='outdoors', h2='For outdoorsy dog people', match=r'camping|enamel|beanie|embroidered hat|baseball cap|tumbler|socks', guide='outdoorsy-dog-owner-gifts',
             text="For the dog owner who hikes in the snow and never skips a walk: camping mugs, warm beanies, caps and travel tumblers."),
        dict(id='cozy', h2='Cozy gifts for nights on the couch', match=r'blanket|throw|slippers|candle|pajama|sweatshirt|crewneck', guide='cozy-winter-gifts-pet-lovers',
             text="Couch, blanket, dog on the feet. Plush throws, slippers, plaid pajamas and candles for the coldest weeks of the year."),
        dict(id='funny', h2='Funny gifts for dog lovers', match=r"sorry i.m late|dog sibling|santa.s favorite|from the dog|funny", guide='funny-dog-lover-gifts',
             text="For white elephant swaps and the friend who is always late because the dog was comfy."),
        dict(id='stocking', h2='Stocking stuffers under $20', max_price=20, guide='dog-lover-stocking-stuffers',
             text="Small gifts with big dog energy: ornaments, socks, stickers, cards and gift tags."),
        dict(id='last-minute', h2='Last-minute printables', match=r'printable|instant download', guide='printable-pet-gifts',
             text="Out of time? Printables download right after purchase, so they work even on Christmas Eve."),
    ],
    faq=[
        ("What is a good Christmas gift for a dog owner?", "Pick something tied to their dog: a mug or ornament with their breed, a sweatshirt that says dog mom or dog dad, or a gift for the dog itself like a holiday bandana or a pet blanket. Personal beats expensive."),
        ("What do you get a dog mom who has everything?", "A dated keepsake ornament, a cozy plush blanket or a funny sweatshirt. They are things she would not buy for herself, and the ornament comes back every December."),
        ("What is a good gift for someone with a new puppy?", "A Puppy's First Christmas ornament with the year on it, plus something practical for the puppy like a bowl or a warm hoodie."),
        ("What can I give a friend whose dog passed away?", "A memorial ornament is a gentle, lasting gift. Add a short handwritten note with a memory of their dog."),
        ("When should I order to get it before Christmas?", "Physical gifts are printed on demand in the USA: order by December 10 for Christmas delivery in the US. Printables download instantly, so they work up to Christmas Eve."),
        ("Where do I buy these gifts?", "Every gift is sold in the Cozy Paws shop on Etsy, with Etsy's secure checkout and purchase protection. The links on this page take you straight to each listing."),
    ],
)
BREED_GUIDES = ['golden-retriever-gifts', 'labrador-gifts', 'frenchie-gifts', 'german-shepherd-gifts', 'dachshund-gifts', 'doodle-gifts']


# ---------------------------------------------------------------- herramientas (tráfico de Google todo el año)
TOOLS = [
    dict(id='dog-age-calculator', live=dt.date(2026, 11, 14), h1='Dog Age Calculator: Dog Years to Human Years',
         desc='Convert your dog\'s age to human years by size, with the classic vet chart and the newer DNA-based formula.', pet='dog'),
    dict(id='cat-age-calculator', live=dt.date(2026, 11, 18), h1='Cat Age Calculator: Cat Years to Human Years',
         desc='How old is your cat in human years? Instant answer plus your cat\'s life stage.', pet='cat'),
    dict(id='dog-food-calculator', live=dt.date(2026, 11, 20), h1='Dog Food Calculator: How Much to Feed Your Dog',
         desc='Daily calories and cups of food for your dog by weight and activity, using the standard RER formula vets use.', pet='dog'),
    dict(id='pet-name-generator', live=dt.date(2026, 11, 22), h1='Pet Name Generator: Dog and Cat Names',
         desc='Hundreds of dog and cat names by style: cute, classic, foodie, tough and Christmas names.', pet='both'),
]

TOOL_BODY = {
'dog-age-calculator': '''
<div class="calc"><label>Dog's age <input id="y" type="number" min="0" max="30" step="0.5" value="5"> years</label>
<label>Size <select id="s"><option value="4">Small (under 20 lb)</option><option value="5" selected>Medium (21-50 lb)</option><option value="6">Large (51-90 lb)</option><option value="7">Giant (over 90 lb)</option></select></label>
<div class="result" id="r"></div></div>
<script>
function calc(){var y=parseFloat(document.getElementById('y').value)||0,s=+document.getElementById('s').value,h;
if(y<=1)h=y*15;else if(y<=2)h=15+(y-1)*9;else h=24+(y-2)*s;
var d=y>0?16*Math.log(y)+31:0;
document.getElementById('r').innerHTML='<b>'+Math.round(h)+' human years</b> (vet chart by size)'+(y>=1?'<br><small>DNA-based formula (UC San Diego, 2019): about '+Math.round(d)+' human years</small>':'');}
document.querySelectorAll('.calc input,.calc select').forEach(function(e){e.addEventListener('input',calc)});calc();
</script>
<h2>How the dog age calculator works</h2>
<p>The old "multiply by 7" rule is a myth. Dogs grow up very fast in the first two years: a 1 year old dog is about 15 in human years and a 2 year old is about 24. After that, each dog year counts as 4 to 7 human years depending on size, because big dogs age faster than small ones.</p>
<p>We also show the DNA-based formula from a 2019 study at UC San Diego (human age = 16 × ln(dog age) + 31). It was built with Labrador Retrievers, so treat it as a fun second opinion.</p>
<h2>Dog years chart</h2>
<table><tr><th>Dog age</th><th>Small</th><th>Medium</th><th>Large</th><th>Giant</th></tr>
<tr><td>1</td><td>15</td><td>15</td><td>15</td><td>15</td></tr><tr><td>2</td><td>24</td><td>24</td><td>24</td><td>24</td></tr>
<tr><td>5</td><td>36</td><td>39</td><td>42</td><td>45</td></tr><tr><td>8</td><td>48</td><td>54</td><td>60</td><td>66</td></tr>
<tr><td>10</td><td>56</td><td>64</td><td>72</td><td>80</td></tr><tr><td>13</td><td>68</td><td>79</td><td>90</td><td>101</td></tr></table>
<p class="note">For fun and general information. Your vet knows your dog best.</p>''',
'cat-age-calculator': '''
<div class="calc"><label>Cat's age <input id="y" type="number" min="0" max="30" step="0.5" value="4"> years</label><div class="result" id="r"></div></div>
<script>
function stage(y){return y<1?'Kitten':y<3?'Young adult':y<7?'Mature adult':y<11?'Mature adult (7-10)':y<15?'Senior':'Super senior';}
function calc(){var y=parseFloat(document.getElementById('y').value)||0,h=y<=1?y*15:y<=2?15+(y-1)*9:24+(y-2)*4;
document.getElementById('r').innerHTML='<b>'+Math.round(h)+' human years</b><br><small>Life stage: '+stage(y)+'</small>';}
document.getElementById('y').addEventListener('input',calc);calc();
</script>
<h2>How cat years work</h2>
<p>Cats grow up fast: the first year equals about 15 human years and the second adds 9 more, so a 2 year old cat is about 24. After that, each cat year is about 4 human years. A 10 year old cat is roughly 56, and a 15 year old is about 76.</p>
<h2>Cat years chart</h2>
<table><tr><th>Cat age</th><th>Human years</th></tr><tr><td>1</td><td>15</td></tr><tr><td>2</td><td>24</td></tr><tr><td>4</td><td>32</td></tr><tr><td>6</td><td>40</td></tr><tr><td>8</td><td>48</td></tr><tr><td>10</td><td>56</td></tr><tr><td>12</td><td>64</td></tr><tr><td>15</td><td>76</td></tr><tr><td>18</td><td>88</td></tr></table>
<p class="note">For fun and general information. Senior cats do best with a vet check twice a year.</p>''',
'dog-food-calculator': '''
<div class="calc"><label>Weight <input id="w" type="number" min="1" max="250" value="40"> <select id="u"><option value="lb">lb</option><option value="kg">kg</option></select></label>
<label>Your dog is <select id="f"><option value="3">Puppy under 4 months</option><option value="2">Puppy 4-12 months</option><option value="1.6" selected>Adult, spayed or neutered</option><option value="1.8">Adult, not neutered</option><option value="1.4">Senior or not very active</option><option value="1.0">Adult that needs to lose weight</option><option value="2.5">Very active or working dog</option></select></label>
<label>Calories per cup of your food <input id="k" type="number" min="100" max="700" value="370"> kcal <small>(on the bag)</small></label>
<div class="result" id="r"></div></div>
<script>
function calc(){var w=parseFloat(document.getElementById('w').value)||0,kg=document.getElementById('u').value=='lb'?w/2.2046:w,
f=+document.getElementById('f').value,k=parseFloat(document.getElementById('k').value)||370,rer=70*Math.pow(kg,0.75),mer=rer*f;
document.getElementById('r').innerHTML='<b>About '+Math.round(mer)+' calories a day</b><br>That is about <b>'+(mer/k).toFixed(1)+' cups</b> a day of a food with '+k+' kcal per cup.<br><small>Resting energy (RER): '+Math.round(rer)+' kcal</small>';}
document.querySelectorAll('.calc input,.calc select').forEach(function(e){e.addEventListener('input',calc)});calc();
</script>
<h2>How we calculate it</h2>
<p>Vets start with the Resting Energy Requirement: RER = 70 × (weight in kg)<sup>0.75</sup>. Then they multiply it by a factor for life stage and activity, for example 1.6 for a typical neutered adult or 3 for a young puppy. The result is a starting point: weigh your dog every 2 to 4 weeks and adjust by 10% if they gain or lose weight.</p>
<p>Treats count too: keep them under 10% of daily calories.</p>
<p class="note">General information only, not veterinary advice. Ask your vet before changing your dog's diet, especially for puppies, seniors or dogs with health conditions.</p>''',
'pet-name-generator': '''
<div class="calc"><label>Pet <select id="p"><option value="dog">Dog</option><option value="cat">Cat</option></select></label>
<label>Style <select id="s"><option>Cute</option><option>Classic</option><option>Foodie</option><option>Tough</option><option>Christmas</option><option>Funny</option></select></label>
<button id="go" type="button">Give me names</button><div class="result" id="r"></div></div>
<script>
var N={Cute:'Biscuit Peanut Muffin Pebble Button Daisy Pickles Noodle Teddy Pumpkin Bean Mochi Sprout Clover Poppy Waffles Nugget Bubbles Honey Maple Pip Dot Tink Coco Lulu',
Classic:'Max Bella Charlie Lucy Cooper Daisy Buddy Molly Jack Sadie Rocky Maggie Duke Rosie Bear Stella Oscar Ruby Henry Lily Sam Grace Leo Penny Jake',
Foodie:'Nacho Pretzel Oreo Tofu Waffle Pepper Ginger Mango Kiwi Bagel Cookie Olive Churro Taco Sushi Brownie Nutmeg Cinnamon Dumpling Toast Biscotti Fig Pistachio Sesame Gnocchi',
Tough:'Tank Diesel Bruno Thor Rex Axel Blaze Titan Brutus Ranger Maverick Ace Rocco Zeus Gunner Hunter Bolt Storm Kodiak Atlas Viper Bandit Rambo Duke Moose',
Christmas:'Jingle Holly Noel Tinsel Rudy Ivy Comet Cocoa Snowball Merry Joy Gingerbread Frosty Twinkle Mistletoe Blitzen Cookie Candy Star Belle Nick Pinecone Sugarplum Winter Evergreen',
Funny:'Sir Barksalot|Chewbacca|Meowzart|Purrlock|Bark Twain|Catrick Swayze|Droolius Caesar|Mr. Pickles|Sherlock Bones|Kitty Purry|Fluffernutter|Captain Whiskers|Professor Paws|Notorious D.O.G.|Furrdinand|Count Pawcula|Hairy Pawter|Pupcake|Baron von Snuggles|Tater Tot'};
var C={Cute:'Whiskers Mittens Kitty Luna Smokey Pumpkin Mochi Bean Pixie Ziggy Cleo Willow Pebbles Socks Muffin Boots Nala Simba Fern Poppy Pearl Sugar Velvet Clover Tiny'};
function go(){var p=document.getElementById('p').value,s=document.getElementById('s').value,src=(p=='cat'&&C[s]?C[s]+' ':'')+N[s];
var a=s=='Funny'?N.Funny.split('|'):src.split(' '),o=[];while(o.length<10&&a.length){o.push(a.splice(Math.floor(Math.random()*a.length),1)[0]);}
document.getElementById('r').innerHTML='<ul class="names">'+o.map(function(n){return '<li>'+n+'</li>'}).join('')+'</ul><small>Tap the button again for more.</small>';}
document.getElementById('go').addEventListener('click',go);go();
</script>
<h2>Tips for picking a pet name</h2>
<ol><li>Short names (one or two syllables) are easier for pets to learn.</li><li>Avoid names that sound like commands, like "Kit" (sit) or "Bo" (no).</li><li>Say it out loud at the park: you will be yelling it for years.</li><li>Give it a few days. If the name does not fit, it is fine to change it while your pet is still learning.</li></ol>''',
}

FUN_TILE = ('<a class="tool" href="/fun/" style="background:var(--rose)"><b>Paw Party app 🎉</b><span>Free fun app for dogs and cats: human years, names, '
            'personality quiz, pet zodiac and birthday cards. Install it on your phone.</span></a>'
            '<a class="tool" href="/diary/" style="background:var(--plum)"><b>Paw Diary app 📔</b><span>Free pet diary and vet reminders: walks, meds, vaccines, '
            'weight chart and food plan for dogs and cats. Works offline.</span></a>')

# ---------------------------------------------------------------- html
PAW = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='120' height='120' viewBox='0 0 120 120'%3E%3Cg fill='%23e6d6b8' opacity='.55'%3E"
       "%3Cellipse cx='30' cy='36' rx='7' ry='6'/%3E%3Ccircle cx='22' cy='27' r='3'/%3E%3Ccircle cx='28' cy='23' r='3'/%3E%3Ccircle cx='34' cy='23' r='3'/%3E%3Ccircle cx='39' cy='28' r='3'/%3E"
       "%3Cellipse cx='88' cy='94' rx='7' ry='6'/%3E%3Ccircle cx='80' cy='85' r='3'/%3E%3Ccircle cx='86' cy='81' r='3'/%3E%3Ccircle cx='92' cy='81' r='3'/%3E%3Ccircle cx='97' cy='86' r='3'/%3E%3C/g%3E%3C/svg%3E")
CSS = """@font-face{font-family:Yesteryear;src:url(/fonts/Yesteryear-Regular.woff2) format('woff2');font-display:swap}
@font-face{font-family:Abril;src:url(/fonts/AbrilFatface-Regular.woff2) format('woff2');font-display:swap}
@font-face{font-family:Lora;src:url(/fonts/Lora.woff2) format('woff2');font-weight:400 700;font-display:swap}
:root{--cream:#F3E9D7;--cream2:#FAF4E8;--plum:#3B2433;--blue:#4E7F86;--gold:#C8962E;--rose:#B5525C;--ink:#3a2f2a;--line:#E2D3B8}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}body{margin:0;font-family:Lora,Georgia,serif;background:var(--cream);background-image:url("PAWURL");color:var(--ink);line-height:1.65;font-size:17px}
a{color:var(--blue)}img{max-width:100%;height:auto}
.bar{background:var(--blue);color:var(--cream);text-align:center;font-size:14px;padding:8px 14px;letter-spacing:.3px}
header{background:var(--cream2);border-bottom:3px double var(--gold)}header .in{max-width:1120px;margin:0 auto;padding:10px 20px;display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap}
.brand{display:flex;align-items:center;gap:10px;text-decoration:none}.brand img{width:58px;height:58px}.brand span{font-family:Yesteryear,cursive;font-size:38px;color:var(--plum);line-height:1}
nav{display:flex;gap:6px;flex-wrap:wrap}nav a{font-family:Abril,Georgia,serif;color:var(--plum);text-decoration:none;font-size:16px;padding:8px 12px;border-radius:99px;letter-spacing:.3px}nav a:hover{background:var(--cream)}
nav a.shop{background:var(--plum);color:var(--cream)}
main{max-width:1120px;margin:0 auto;padding:6px 20px 50px}
h1,h2,h3{font-family:Abril,Georgia,serif;font-weight:400;color:var(--plum);line-height:1.15;letter-spacing:.2px}h1{font-size:44px;margin:26px 0 12px}h2{font-size:30px;margin:46px 0 16px;display:flex;align-items:center;gap:12px}
h2:after{content:"";flex:1;height:2px;background:linear-gradient(90deg,var(--gold),transparent)}
.script{font-family:Yesteryear,cursive;color:var(--plum)}
.lead{font-size:19px;max-width:740px;color:#5a4a44}
.hero{display:grid;grid-template-columns:1.25fr .9fr;gap:30px;align-items:center;background:var(--cream2);border:2px solid var(--line);border-radius:28px;padding:34px 40px;margin-top:22px;box-shadow:0 10px 30px rgba(59,36,51,.07)}
.hero .script{font-size:72px;line-height:1;display:block;margin-bottom:6px}.hero .tag{font-family:Abril,Georgia,serif;color:var(--blue);font-size:24px;line-height:1.3;margin:0 0 14px}
.hero p{margin:0 0 20px;color:#5a4a44}.hero img{width:100%;max-width:340px;justify-self:center}
.btn{display:inline-block;background:var(--plum);color:var(--cream)!important;padding:13px 24px;border-radius:99px;text-decoration:none;font-family:Abril,Georgia,serif;font-size:17px;letter-spacing:.4px;border:0;cursor:pointer;box-shadow:0 4px 0 #24151f}
.btn:hover{transform:translateY(1px);box-shadow:0 3px 0 #24151f}.btn.ghost{background:transparent;color:var(--plum)!important;border:2px solid var(--plum);box-shadow:none;margin-left:8px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:22px}
.card{background:var(--cream2);border:1px solid var(--line);border-radius:20px;overflow:hidden;text-decoration:none;color:inherit;display:flex;flex-direction:column;transition:transform .15s,box-shadow .15s;position:relative}
.card:hover{transform:translateY(-3px);box-shadow:0 12px 26px rgba(59,36,51,.12)}.card img{width:100%;height:auto;aspect-ratio:1;object-fit:cover;display:block}
.card .t{padding:12px 14px 2px;font-weight:600;font-size:16px;color:var(--plum);line-height:1.35}.card .m{padding:2px 14px 14px;font-size:14px;color:#7b6b62;display:flex;justify-content:space-between;align-items:center;gap:8px}
.card .price{font-family:Abril,Georgia,serif;color:var(--blue);font-size:18px}
.badge{position:absolute;top:12px;left:12px;background:var(--gold);color:#fff;font-family:Abril,Georgia,serif;font-size:13px;padding:4px 11px;border-radius:99px;letter-spacing:.4px}
.stamps{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:16px}
.stamp{display:flex;align-items:center;gap:14px;background:var(--cream2);border:2px dashed var(--blue);border-radius:18px;padding:12px;text-decoration:none;color:var(--plum)}
.stamp img{width:78px;height:78px;flex:none;border-radius:50%;object-fit:cover;border:3px solid var(--cream)}.stamp b{font-family:Abril,Georgia,serif;font-weight:400;font-size:18px;line-height:1.2}.stamp small{display:block;color:#7b6b62}
.pills a{display:inline-block;margin:5px 6px 5px 0;padding:8px 15px;border-radius:99px;background:var(--cream2);border:1.5px solid var(--blue);text-decoration:none;color:var(--blue);font-size:15px}
.prod{display:grid;grid-template-columns:1.05fr 1fr;gap:36px;align-items:start;margin-top:22px}.prod img{width:100%;border-radius:24px;border:1px solid var(--line)}
.prod h1{margin-top:6px}.bigprice{font-family:Abril,Georgia,serif;font-size:30px;color:var(--blue)}.kind{font-family:Abril,Georgia,serif;color:var(--gold);letter-spacing:1.5px;text-transform:uppercase;font-size:14px}
.perks{list-style:none;padding:0}.perks li{padding:6px 0 6px 30px;position:relative}.perks li:before{content:"✦";position:absolute;left:4px;color:var(--gold)}
.calc{background:var(--cream2);border:2px solid var(--line);border-radius:22px;padding:24px;max-width:640px}
.calc label{display:block;margin:0 0 14px;font-weight:600}.calc input,.calc select{font:inherit;font-size:17px;padding:9px 10px;border:1.5px solid var(--line);border-radius:12px;margin-left:6px;max-width:230px;background:#fff}
.calc button{font-family:Abril,Georgia,serif}.result{font-size:20px;background:#fff;border:2px dashed var(--gold);border-radius:16px;padding:16px;margin-top:10px}.names{columns:2;margin:0;padding-left:20px}
table{border-collapse:collapse;background:var(--cream2);border-radius:12px;overflow:hidden}td,th{border:1px solid var(--line);padding:7px 14px;text-align:center}th{background:var(--blue);color:var(--cream);font-weight:600}
.note{color:#7b6b62;font-size:14px}.tips li{margin:6px 0}
.about{display:grid;grid-template-columns:1fr 1fr;gap:34px;align-items:center;margin-top:20px}.about .ph img{width:100%;max-height:640px;object-fit:cover;object-position:50% 30%;border-radius:26px;border:6px solid var(--cream2);box-shadow:0 10px 30px rgba(59,36,51,.12)}
.gal{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:16px;margin:10px 0}.gal img{width:100%;aspect-ratio:1;object-fit:cover;border-radius:20px;border:5px solid var(--cream2)}
.vals{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:16px}.vals div{background:var(--cream2);border:1px solid var(--line);border-radius:20px;padding:18px 20px}.vals b{font-family:Abril,Georgia,serif;font-weight:400;font-size:20px;color:var(--plum);display:block;margin-bottom:4px}
.maker{display:grid;grid-template-columns:200px 1fr;gap:26px;align-items:center;background:var(--cream2);border:2px solid var(--line);border-radius:26px;padding:24px 30px;margin-top:46px}.maker img{width:200px;height:200px;object-fit:cover;object-position:50% 30%;border-radius:50%;border:5px solid var(--cream)}
.contact{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:16px}.contact a{display:block;background:var(--blue);color:var(--cream);border-radius:20px;padding:20px;text-decoration:none}.contact b{font-family:Abril,Georgia,serif;font-weight:400;font-size:21px;display:block}
footer .links a{margin-right:12px}
@media(max-width:760px){.about,.maker{grid-template-columns:1fr;text-align:center}.maker img{margin:0 auto;width:150px;height:150px}}
.post{max-width:760px}.post p,.post li{font-size:17.5px;line-height:1.7}.post table{margin:12px 0;font-size:16px}.post h2{margin-top:28px}
.toc{background:var(--cream2);border:2px dashed var(--gold);border-radius:20px;padding:16px 22px;margin:22px 0}.toc b{font-family:Abril,Georgia,serif;font-weight:400;color:var(--plum)}
.toc a{display:inline-block;margin:4px 6px 4px 0;padding:6px 13px;border-radius:99px;background:#fff;border:1.5px solid var(--line);text-decoration:none;color:var(--blue);font-size:15px}
.ship{background:var(--blue);color:var(--cream);border-radius:20px;padding:16px 22px;margin:18px 0}.ship b{font-family:Abril,Georgia,serif;font-weight:400}
.more{margin-top:14px}.faq details{background:var(--cream2);border:1px solid var(--line);border-radius:14px;padding:12px 18px;margin:10px 0}.faq summary{cursor:pointer;font-weight:600;color:var(--plum)}
.feature{display:grid;grid-template-columns:1fr 220px;gap:22px;align-items:center;background:var(--plum);color:var(--cream);border-radius:24px;padding:24px 30px;margin:24px 0;text-decoration:none}
.feature b{font-family:Abril,Georgia,serif;font-weight:400;font-size:28px;display:block;line-height:1.15;margin-bottom:6px}.feature img{border-radius:18px;width:100%}
@media(max-width:760px){.feature{grid-template-columns:1fr}.feature img{max-width:220px}}
.tools{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:18px}.tool{background:var(--blue);color:var(--cream);border-radius:22px;padding:22px;text-decoration:none}
.tool b{font-family:Abril,Georgia,serif;font-weight:400;font-size:22px;display:block;margin-bottom:6px;line-height:1.2}.tool span{font-size:15px;opacity:.92}.tool:hover{background:#436f75}
.club{display:grid;grid-template-columns:150px 1fr;gap:26px;align-items:center;background:var(--plum);color:var(--cream);border-radius:28px;padding:28px 34px;margin-top:50px}
.club .script{color:var(--cream);font-size:44px;line-height:1}.club p{margin:8px 0 0}.club img{width:150px}
footer{background:var(--plum);color:var(--cream);margin-top:50px;border-top:5px solid var(--gold)}footer .in{max-width:1120px;margin:0 auto;padding:26px 20px;display:flex;justify-content:space-between;align-items:center;gap:18px;flex-wrap:wrap;font-size:15px}
footer a{color:var(--cream);margin-right:16px}footer .fb{display:flex;align-items:center;gap:14px}footer img{width:64px}footer .script{color:var(--cream);font-size:30px}
#cc{position:fixed;bottom:12px;left:12px;right:12px;max-width:540px;background:var(--plum);color:var(--cream);padding:14px 16px;border-radius:16px;font-size:14px;display:none;z-index:9;box-shadow:0 10px 30px rgba(0,0,0,.25)}
#cc button{margin:8px 8px 0 0;padding:7px 16px;border-radius:99px;border:0;cursor:pointer;font:inherit}#cc .y{background:var(--gold);color:#fff}#cc a{color:#f3c9a0}
@media(max-width:760px){body{font-size:16px}h1{font-size:32px}h2{font-size:24px}.hero{grid-template-columns:1fr;padding:24px 20px;text-align:center}.hero img{max-width:190px;order:-1}.hero .script{font-size:56px}.hero .tag{font-size:20px}
.btn.ghost{margin:10px 0 0}.grid{grid-template-columns:repeat(2,1fr);gap:12px}.card .t{font-size:14px;padding:10px 10px 0}.card .m{padding:2px 10px 10px;font-size:12px}.card .price{font-size:16px}
.prod{grid-template-columns:1fr;gap:16px}.club{grid-template-columns:1fr;text-align:center;padding:24px}.club img{margin:0 auto;width:110px}
header .in{justify-content:center}.brand span{font-size:32px}.brand img{width:46px;height:46px}nav{justify-content:center}nav a{font-size:14px;padding:6px 10px}}
""".replace('PAWURL', PAW)


def analytics():
    ga, px = CONFIG['ga4'], CONFIG['pixel']
    js = "function wwLoad(){"
    if ga:
        js += (f"var s=document.createElement('script');s.async=1;s.src='https://www.googletagmanager.com/gtag/js?id={ga}';document.head.appendChild(s);"
               f"window.dataLayer=window.dataLayer||[];window.gtag=function(){{dataLayer.push(arguments)}};gtag('js',new Date());gtag('config','{ga}');")
    if px:
        js += ("!function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)};"
               "if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;t.src=v;s=b.getElementsByTagName(e)[0];"
               f"s.parentNode.insertBefore(t,s)}}(window,document,'script','https://connect.facebook.net/en_US/fbevents.js');fbq('init','{px}');fbq('track','PageView');")
    js += "}"
    js += """var c=localStorage.getItem('ww_cc');if(c==='y')wwLoad();else if(c!=='n'){document.addEventListener('DOMContentLoaded',function(){var b=document.getElementById('cc');b.style.display='block';
b.querySelector('.y').onclick=function(){localStorage.setItem('ww_cc','y');b.style.display='none';wwLoad()};b.querySelector('.n').onclick=function(){localStorage.setItem('ww_cc','n');b.style.display='none'}})}
document.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('a[data-etsy]');if(a&&window.gtag)gtag('event','etsy_click',{item_id:a.getAttribute('data-etsy')});if(a&&window.fbq)fbq('trackCustom','EtsyClick');});"""
    return f'<script>{js}</script>'


def signup():
    act = CONFIG['mailerlite_action']
    if not act:
        return ''
    return f'''<section class="club" id="join"><img src="/img/sello-claro.png" alt="" width="120" height="120" loading="lazy"><div><span class="script">Join the club</span>
<p>Get our free printable <b>Pet Care Checklist</b> (daily, weekly, monthly and yearly, plus a pet info card for the fridge), new gift drops and the occasional member-only coupon. A few emails a month, unsubscribe anytime.</p>
<form action="{E(act)}" method="post" target="cp_nl" style="display:flex;gap:8px;flex-wrap:wrap;margin-top:10px" onsubmit="setTimeout(function(){{document.getElementById('cp-ok').hidden=false}},600);if(window.gtag)gtag('event','sign_up',{{method:'newsletter'}});if(window.fbq)fbq('track','Lead')">
<input type="email" name="fields[email]" required placeholder="Your email" aria-label="Your email" style="flex:1;min-width:200px;padding:12px;border:2px solid var(--gold);border-radius:10px;font:inherit">
<input type="hidden" name="fields[language]" value="en"><input type="hidden" name="ml-submit" value="1"><input type="hidden" name="anticsrf" value="true">
<button class="btn" type="submit" style="border:0;cursor:pointer;background:var(--gold);box-shadow:0 4px 0 #8f6a1f">Send me the checklist</button></form>
<p id="cp-ok" hidden><b>You're in!</b> Check your inbox in a minute: your checklist is on its way.</p>
<p style="font-size:13px;margin-top:6px">We use MailerLite to send emails. See our <a href="/privacy/" style="color:var(--cream)">privacy policy</a>.</p><iframe name="cp_nl" title="newsletter" hidden></iframe></div></section>'''


def page(path, title, desc, body, today, image=None, jsonld=None, canonical=True):
    url = CONFIG['url'] + path
    img = CONFIG['url'] + (image or '/img/og.jpg')
    days = (CONFIG['christmas_cutoff'] - today).days
    bar = (f'Order by Dec 10 for Christmas delivery in the US ({days} days left)' if 0 <= days <= 40
           else 'Original gifts for pet people, printed on demand in the USA')
    bar = '✦ ' + bar + ' ✦'
    metas = ''
    if CONFIG['pinterest_verify']:
        metas += f'<meta name="p:domain_verify" content="{E(CONFIG["pinterest_verify"])}">'
    if CONFIG['google_verify']:
        metas += f'<meta name="google-site-verification" content="{E(CONFIG["google_verify"])}">'
    ld = f'<script type="application/ld+json">{json.dumps(jsonld)}</script>' if jsonld else ''
    pin = f'<a href="{CONFIG["pinterest"]}" rel="me">Pinterest</a>' if CONFIG['pinterest'] else ''
    doc = f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)}</title><meta name="description" content="{E(desc)}">{'<link rel="canonical" href="' + url + '">' if canonical else ''}
<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:image" content="{img}"><meta property="og:url" content="{url}"><meta property="og:type" content="website">
<meta name="twitter:card" content="summary_large_image">{metas}
<link rel="alternate" type="application/rss+xml" title="{CONFIG['name']}" href="/feed.xml"><link rel="icon" href="/img/icon.png"><link rel="apple-touch-icon" href="/img/apple-touch-icon.png">
<link rel="preload" href="/fonts/Yesteryear-Regular.woff2" as="font" type="font/woff2" crossorigin><link rel="preload" href="/fonts/AbrilFatface-Regular.woff2" as="font" type="font/woff2" crossorigin>
<meta name="theme-color" content="#4E7F86"><style>{CSS}</style>{ld}{analytics()}</head><body>
<div class="bar">{bar}</div>
<header><div class="in"><a class="brand" href="/"><img src="/img/logo-160.png" alt="" width="58" height="58"><span>Cozy Paws</span></a>
<nav><a href="/gifts/">Gift guides</a><a href="/tools/">Pet tools</a><a href="/blog/">Pet tips</a><a href="/fun/">Fun app</a><a href="/diary/">Pet diary</a><a href="/about/">About</a><a class="shop" href="{CONFIG['shop']}" data-etsy="shop">Shop on Etsy</a></nav></div></header>
<main>{body}{signup() if path not in ('/', '/privacy/', '/terms/') else ''}</main>
<footer><div class="in"><div class="fb"><img src="/img/sello-claro.png" alt="" width="64" height="64" loading="lazy"><div><span class="script">Cozy Paws</span><br>Vintage club gifts for dogs, cats &amp; the people who love them. Designed in Salt Lake City, Utah.</div></div>
<div class="links"><a href="{CONFIG['shop']}" data-etsy="footer">Etsy shop</a>{pin}<a href="{CONFIG['instagram']}" rel="me">Instagram</a><a href="{CONFIG['facebook']}" rel="me">Facebook</a><br>
<a href="/about/">About</a><a href="/shipping-returns/">Shipping &amp; returns</a><a href="/faq/">FAQ</a><a href="/contact/">Contact</a><a href="/privacy/">Privacy</a><a href="/terms/">Terms</a><br><small>© {today.year} Cozy Paws</small></div></div></footer>
<div id="cc">We use cookies for anonymous stats (Google Analytics) and ads measurement (Meta). <a href="/privacy/">Privacy</a><br><button class="y">OK</button><button class="n">No thanks</button></div>
</body></html>"""
    if path.endswith('.html'):
        f = os.path.join(OUT, path.strip('/'))
    else:
        d = os.path.join(OUT, path.strip('/'))
        os.makedirs(d, exist_ok=True)
        f = os.path.join(d, 'index.html')
    open(f, 'w', encoding='utf-8').write(doc)


def card(p, soon=None):
    inner = (f'<img src="/img/p/{p["sku"]}.jpg" alt="{E(p["short"])}" loading="lazy" width="450" height="450">'
             + (f'<span class="badge">{E(soon)}</span>' if soon else '')
             + f'<div class="t">{E(p["short"])}</div><div class="m"><span>{E(p["kind"])}</span><span class="price">${E(p["precio"])}</span></div>')
    if soon:
        return f'<div class="card">{inner}</div>'
    return f'<a class="card" href="/p/{p["slug"]}/">{inner}</a>'


def grid(ps):
    return '<div class="grid">' + ''.join(card(p) for p in ps) + '</div>'


def hub_sections(prods):
    """Secciones de la guía principal con los productos de perro ya publicados (vacías no se muestran)."""
    dog, cat = re.compile(HUB['dog']), re.compile(r'\bcats?\b|kitty|kitten|meow')
    # solo el título (las etiquetas de productos de gatos a veces dicen "dog lover")
    dps = [dict(p, hay=p['titulo'].lower()) for p in prods if dog.search(p['titulo'].lower())
           and not (cat.search(p['titulo'].lower()) and 'dog' not in p['titulo'].lower())]
    out = []
    for sec in HUB['sections']:
        if sec.get('max_price'):
            ps = [p for p in dps if float(p['precio'] or 0) <= sec['max_price']]
        else:
            rx = re.compile(sec['match'])
            ps = [p for p in dps if rx.search(p['hay'])]
        if ps:
            out.append((sec, ps))
    return dps, out


def hub_page(prods, guides_live, today):
    dps, secs = hub_sections(prods)
    if len(dps) < 2:
        return None
    live_ids = {g['id'] for g, _ in guides_live}
    y = today.year
    toc = ''.join(f'<a href="#{s["id"]}">{E(s["h2"])}</a>' for s, _ in secs)
    days = (CONFIG['christmas_cutoff'] - today).days
    ship = (f'<div class="ship"><b>Shipping:</b> order physical gifts by December 10 for Christmas delivery in the US'
            + (f' ({days} days left)' if days >= 0 else '') + '. Printables download instantly, even on Christmas Eve.</div>'
            if today <= dt.date(today.year, 12, 24) else '')
    body = (f'<p class="note"><a href="/">Home</a> › <a href="/gifts/">Gift guides</a> › Christmas gift guide for dog owners</p>'
            f'<h1>{E(HUB["h1"])} ({y})</h1><p class="lead">{E(HUB["intro"])}</p>{ship}'
            f'<nav class="toc" aria-label="Jump to"><b>Jump to:</b><br>{toc}<a href="#faq">Questions</a></nav>')
    for sec, ps in secs:
        body += f'<h2 id="{sec["id"]}">{E(sec["h2"])}</h2><p>{E(sec["text"])}</p>{grid(ps[:8])}'
        if sec.get('breeds'):
            bl = ''.join(f'<a href="/gifts/{g["id"]}/">{E(g["h1"])}</a>' for g, _ in guides_live if g['id'] in BREED_GUIDES)
            if bl:
                body += f'<p class="more pills">{bl}</p>'
        elif sec.get('guide') in live_ids:
            g = next(g for g, _ in guides_live if g['id'] == sec['guide'])
            body += f'<p class="more pills"><a href="/gifts/{g["id"]}/">See all: {E(g["h1"])} →</a></p>'
    faq = ''.join(f'<details><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q, a in HUB['faq'])
    others = ''.join(f'<a href="/gifts/{g["id"]}/">{E(g["h1"])}</a>' for g, _ in guides_live)
    body += (f'<p style="margin-top:34px"><a class="btn" href="{CONFIG["shop"]}" data-etsy="hub">See every gift on Etsy</a></p>'
             f'<h2 id="faq">Questions dog people ask</h2><div class="faq">{faq}</div>'
             + (f'<h2>More gift guides</h2><div class="pills">{others}</div>' if others else ''))
    url = f'{CONFIG["url"]}/gifts/{HUB["id"]}/'
    seen, items = set(), []
    for _, ps in secs:
        for p in ps:
            if p['sku'] not in seen:
                seen.add(p['sku']); items.append(p)
    ld = {'@context': 'https://schema.org', '@graph': [
        {'@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': CONFIG['url'] + '/'},
            {'@type': 'ListItem', 'position': 2, 'name': 'Gift guides', 'item': CONFIG['url'] + '/gifts/'},
            {'@type': 'ListItem', 'position': 3, 'name': HUB['h1'], 'item': url}]},
        {'@type': 'ItemList', 'name': f'{HUB["h1"]} {y}', 'url': url, 'numberOfItems': len(items),
         'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'url': f'{CONFIG["url"]}/p/{p["slug"]}/', 'name': p['short']} for i, p in enumerate(items)]},
        {'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in HUB['faq']]},
    ]}
    page(f'/gifts/{HUB["id"]}/', HUB['title'].format(y=y) + ' | Cozy Paws', HUB['desc'].format(y=y)[:158], body, today,
         image=f'/img/pin/g-{HUB["id"]}.jpg', jsonld=ld)
    return dps


# ---------------------------------------------------------------- páginas de confianza (about, envíos, preguntas, contacto)
PAGES_UPDATED = dt.date(2026, 11, 14)
AUTORA = os.path.join(DATA, 'autora')  # fotos de Azu con perros (jpg/png). Si no hay, se usa el logo ilustrado.


def author_photos():
    """Copia y achica las fotos de la autora a site/img/autora/. Devuelve las rutas web (la primera es la principal)."""
    if not os.path.isdir(AUTORA):
        return []
    from PIL import Image, ImageOps
    out = os.path.join(OUT, 'img', 'autora')
    os.makedirs(out, exist_ok=True)
    res = []
    for f in sorted(os.listdir(AUTORA)):
        if not re.search(r'\.(jpe?g|png|webp)$', f, re.I):
            continue
        name = re.sub(r'\.\w+$', '.jpg', slug(f.rsplit('.', 1)[0]) + '.x')
        dst = os.path.join(out, name)
        im = ImageOps.exif_transpose(Image.open(os.path.join(AUTORA, f))).convert('RGB')
        im.thumbnail((1200, 1200))
        im.save(dst, 'JPEG', quality=84, optimize=True, progressive=True)
        res.append('/img/autora/' + name)
    return res


def maker_block():
    ph = author_photos()
    img = ph[0] if ph else '/img/logo-ilustrado.png'
    return (f'<section class="maker"><img src="{img}" alt="{E(CONFIG["maker_photo_alt"] if ph else CONFIG["maker"])}" loading="lazy" width="200" height="200">'
            f'<div><span class="script" style="font-size:44px">Meet the maker</span><p>Hi, I\'m {E(CONFIG["maker"])}. I design every Cozy Paws gift in Salt Lake City, '
            'surrounded by mountains, trail dogs and very spoiled couch potatoes. This is a one-person shop: each gift is made to order and I answer every message myself.</p>'
            '<p><a href="/about/">Read our story →</a></p></div></section>')


SHOP_FAQ = [
    ('Where do I buy Cozy Paws gifts?', 'All our gifts are sold in the Cozy Paws shop on Etsy, so you check out with Etsy\'s secure payments and Etsy Purchase Protection. This website is our gift guide and catalog.'),
    ('How long does shipping take?', 'Every item is printed when you order it. Production takes about 2 to 5 business days, and US shipping usually takes 3 to 7 business days more. Each Etsy listing shows the estimated delivery date for your address.'),
    ('When should I order for Christmas?', 'Order physical gifts by December 10 for Christmas delivery in the US. Printables are instant downloads, so you can buy them up to Christmas Eve.'),
    ('Do you ship outside the US?', 'International shipping depends on the product. Etsy shows the shipping options and costs for your country at checkout.'),
    ('What if my order arrives damaged or with a print error?', 'If your item arrives misprinted, damaged or with a manufacturing defect, message us through Etsy within 30 days of delivery with a clear photo (or video) of the problem. We send a free replacement or a refund, and you do not need to send the item back.'),
    ('Can I return an item if I change my mind?', 'Because every piece is made to order just for you, we cannot accept returns or exchanges if you change your mind or order the wrong size or color. Please check the size chart in each listing before ordering.'),
    ('How do printables work?', 'After paying on Etsy you get a download link right away. Print at home or at any print shop. Since they are digital files, printables cannot be refunded, but if a file does not open, write to us and we will fix it.'),
    ('Can I personalize a gift with my pet\'s name?', 'Some listings have a personalization box on Etsy. If you want something different, send us a message on Etsy and we will tell you what we can do.'),
    ('How do I care for my mug, sweatshirt or blanket?', 'Ceramic mugs are dishwasher and microwave safe. Wash sweatshirts, tees and blankets inside out in cold water and tumble dry on low so the print lasts.'),
    ('Who makes Cozy Paws?', 'Cozy Paws is a small independent brand designed in Salt Lake City, Utah, and run by ' + CONFIG['maker'] + ' under Skye Solutions AI. Our products are printed on demand by trusted US production partners.'),
]


def faq_ld(faq):
    return {'@context': 'https://schema.org', '@type': 'FAQPage',
            'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in faq]}


def faq_html(faq):
    return '<div class="faq">' + ''.join(f'<details><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q, a in faq) + '</div>'


def trust_pages(today, prods):
    ph = author_photos()
    main_img = ph[0] if ph else '/img/logo-ilustrado.png'
    gal = (f'<h2>Life with dogs</h2><div class="gal">' + ''.join(f'<img src="{p}" alt="{E(CONFIG["maker"])} with a dog" loading="lazy" width="300" height="300">' for p in ph[1:]) + '</div>') if len(ph) > 1 else ''
    vals = ('<div class="vals"><div><b>Original designs</b>Every design is created for Cozy Paws by the maker. Nothing is copied from other shops.</div>'
            '<div><b>Made to order</b>Nothing sits in a warehouse. Each piece is printed when you order it, which means less waste.</div>'
            '<div><b>Printed in the USA</b>Our production partners print and ship from the US, so gifts arrive in days, not weeks.</div>'
            '<div><b>A real person</b>Cozy Paws is a one-person shop. When you write to us, the maker answers.</div></div>')
    news = grid(prods[:4]) if prods else ''
    body = (f'<p class="note"><a href="/">Home</a> › About</p><div class="about"><div><h1>Hi, I\'m {E(CONFIG["maker"])}</h1>'
            '<p class="lead">I started Cozy Paws for people like me: the ones who plan weekends around the dog, take more photos of the cat than of themselves, and think a pet is family, full stop.</p>'
            '<p>I live in Salt Lake City, Utah, where the mountains are ten minutes away and every trailhead is full of happy dogs. '
            'Cozy Paws mixes two things I love: the charm of old social clubs and vintage naturalist guides, and the very real, very silly life we share with our pets. '
            'That is where designs like the Dog Mom Club and Merry Woofmas come from.</p>'
            '<p>Every design is made for this shop and printed on demand in the USA, so nothing is mass produced and nothing goes to waste. '
            'I pick every product, check every mockup and answer every message myself.</p>'
            f'<p><a class="btn" href="{CONFIG["shop"]}" data-etsy="about">Visit the shop</a><a class="btn ghost" href="/contact/">Say hi</a></p></div>'
            f'<div class="ph"><img src="{main_img}" alt="{E(CONFIG["maker_photo_alt"] if ph else CONFIG["maker"])}" width="520" height="520">'
            + (f'<p class="note" style="text-align:center">{E(CONFIG["maker_photo_caption"])}</p>' if ph else '') + '</div></div>'
            + gal + '<h2>What we care about</h2>' + vals
            + (f'<h2>New in the shop</h2>{news}' if news else '')
            + '<p class="note" style="margin-top:30px">Cozy Paws is a brand of Skye Solutions AI, a sole proprietorship based in Salt Lake City, Utah.</p>')
    ld = {'@context': 'https://schema.org', '@type': 'AboutPage', 'name': 'About Cozy Paws', 'url': CONFIG['url'] + '/about/',
          'mainEntity': {'@type': 'Person', 'name': CONFIG['maker'], 'image': CONFIG['url'] + main_img, 'jobTitle': 'Designer and founder',
                         'worksFor': {'@type': 'Organization', 'name': 'Cozy Paws', 'url': CONFIG['url']}, 'homeLocation': 'Salt Lake City, Utah'}}
    page('/about/', 'About Cozy Paws: Pet Gifts Designed in Salt Lake City', f'Meet {CONFIG["maker"]}, the maker behind Cozy Paws: original gifts for dog and cat people, designed in Salt Lake City and printed on demand in the USA.',
         body, today, image=main_img if ph else None, jsonld=ld)

    ship_faq = SHOP_FAQ[1:7]
    body = ('<p class="note"><a href="/">Home</a> › Shipping &amp; returns</p><h1>Shipping &amp; returns</h1>'
            '<p class="lead">All orders are placed and protected on Etsy. Here is what to expect after you order.</p>'
            '<h2>Shipping</h2><table><tr><th>Step</th><th>Time</th></tr><tr><td>Production (made to order)</td><td>2 to 5 business days</td></tr>'
            '<tr><td>Shipping inside the US</td><td>3 to 7 business days</td></tr><tr><td>Printables (instant download)</td><td>Right after payment</td></tr></table>'
            '<p>Each Etsy listing shows the exact estimated delivery date for your address. You get a tracking number by email when your order ships.</p>'
            '<div class="ship"><b>Christmas:</b> order physical gifts by December 10 for delivery in the US before Christmas.</div>'
            '<h2>Damaged, misprinted or defective items</h2><p>If your item arrives misprinted, damaged or with a manufacturing defect, message us on Etsy within 30 days of delivery with a clear photo (or video) that shows the problem. If several items have the same issue, please include one photo with all of them. We send a free replacement or a refund, whichever you prefer. You do not need to send the item back.</p>'
            '<h2>Lost packages</h2><p>If your order has not arrived 30 days after it shipped (45 days for international orders), message us on Etsy and we will check the tracking with our production partner and find a solution. Packages marked as delivered and orders sent to an address with a typo are not covered, so please double check your shipping address at checkout.</p>'
            '<h2>Returns and exchanges</h2><p>Every piece is printed just for you, so we cannot accept returns or exchanges if you change your mind or order the wrong size or color. Please check the size chart in each listing before ordering. Your order is also covered by Etsy Purchase Protection.</p>'
            '<h2>Printables</h2><p>Digital files cannot be returned. If a file does not open or print correctly, write to us and we will help right away.</p>'
            f'<h2>Common questions</h2>{faq_html(ship_faq)}<p>More answers on the <a href="/faq/">FAQ page</a>, or <a href="/contact/">contact us</a>.</p>')
    page('/shipping-returns/', 'Shipping and Returns | Cozy Paws', 'Cozy Paws shipping times, Christmas order deadline, damaged item replacements and return policy. All orders are protected by Etsy.',
         body, today, jsonld=faq_ld(ship_faq))

    body = (f'<p class="note"><a href="/">Home</a> › FAQ</p><h1>Frequently asked questions</h1><p class="lead">Everything about ordering, shipping and caring for your Cozy Paws gifts.</p>{faq_html(SHOP_FAQ)}'
            '<p style="margin-top:24px">Still have a question? <a href="/contact/">Write to us</a>, we answer within one business day.</p>')
    page('/faq/', 'FAQ: Orders, Shipping and Gifts | Cozy Paws', 'Answers about Cozy Paws orders on Etsy, shipping times, Christmas deadlines, returns, printables and product care.',
         body, today, jsonld=faq_ld(SHOP_FAQ))

    body = ('<p class="note"><a href="/">Home</a> › Contact</p><h1>Contact us</h1><p class="lead">A real person answers, usually within one business day (Monday to Friday, Mountain Time).</p>'
            '<div class="contact">'
            f'<a href="{CONFIG["shop"]}" data-etsy="contact"><b>Etsy messages</b>Best for questions about an order. Open the shop and tap "Message".</a>'
            f'<a href="mailto:{CONFIG["contact"]}"><b>Email</b>{E(CONFIG["contact"])}</a>'
            f'<a href="{CONFIG["instagram"]}" rel="me"><b>Instagram</b>@cozypawsgifts</a>'
            f'<a href="{CONFIG["facebook"]}" rel="me"><b>Facebook</b>Cozy Paws</a>'
            + (f'<a href="{CONFIG["pinterest"]}" rel="me"><b>Pinterest</b>Gift ideas and pins</a>' if CONFIG['pinterest'] else '')
            + '</div><h2>Before you write</h2><p>Many answers are already in the <a href="/faq/">FAQ</a> and on the <a href="/shipping-returns/">shipping &amp; returns</a> page. '
            'For an order, please include your Etsy order number.</p>'
            '<p class="note">Cozy Paws, a brand of Skye Solutions AI. Salt Lake City, Utah, USA.</p>')
    ld = {'@context': 'https://schema.org', '@type': 'ContactPage', 'name': 'Contact Cozy Paws', 'url': CONFIG['url'] + '/contact/',
          'mainEntity': {'@type': 'Organization', 'name': 'Cozy Paws', 'email': CONFIG['contact'],
                         'contactPoint': {'@type': 'ContactPoint', 'contactType': 'customer support', 'email': CONFIG['contact'], 'availableLanguage': ['English', 'Spanish']}}}
    page('/contact/', 'Contact Cozy Paws', 'Questions about a gift or an order? Contact Cozy Paws by Etsy message, email, Instagram or Facebook.', body, today, jsonld=ld)



# ---------------------------------------------------------------- imágenes
def make_images(all_prods, guides_live, tools_live):
    from PIL import Image, ImageDraw, ImageFont
    for sub in ('img/p', 'img/pin', 'fonts'):
        os.makedirs(os.path.join(OUT, sub), exist_ok=True)
    pins_cache = os.path.join(DATA, 'pins')
    os.makedirs(pins_cache, exist_ok=True)
    for f in os.listdir(os.path.join(DATA, 'fonts')):
        if f.endswith('.woff2'):
            shutil.copy(os.path.join(DATA, 'fonts', f), os.path.join(OUT, 'fonts', f))
    for f in os.listdir(os.path.join(DATA, 'brand')):
        shutil.copy(os.path.join(DATA, 'brand', f), os.path.join(OUT, 'img', f))
    if os.path.isdir(os.path.join(DATA, 'gift')):  # regalo del club de mails (cozypaws/regalo.py)
        shutil.copytree(os.path.join(DATA, 'gift'), os.path.join(OUT, 'gift'), dirs_exist_ok=True)
    PLUM, BLUE, CREAM, GOLD = (59, 36, 51), (78, 127, 134), (243, 233, 215), (200, 150, 46)

    def font(kind, size):
        f = {'script': 'Yesteryear-Regular.ttf', 'title': 'AbrilFatface-Regular.ttf'}.get(kind)
        path = os.path.join(DATA, 'fonts', f) if f else '/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf'
        try:
            return ImageFont.truetype(path, size)
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

    def pin(dst, head, sub, imgs):
        if os.path.exists(dst):
            return
        W, H = 1000, 1500
        c = Image.new('RGB', (W, H), CREAM)
        d = ImageDraw.Draw(c)
        d.rounded_rectangle([30, 30, W - 30, H - 30], 36, outline=GOLD, width=4)
        if len(imgs) == 1:
            im = Image.open(imgs[0]).convert('RGB').resize((860, 860))
            m = Image.new('L', im.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, 859, 859], 30, fill=255)
            c.paste(im, (70, 70), m)
        elif imgs:
            for i, f in enumerate(imgs[:4]):
                im = Image.open(f).convert('RGB').resize((420, 420))
                m = Image.new('L', im.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, 419, 419], 24, fill=255)
                c.paste(im, (70 + (i % 2) * 440, 70 + (i // 2) * 440), m)
        else:
            lg = logo.copy(); lg.thumbnail((700, 700))
            c.paste(lg, ((W - lg.width) // 2, 90), lg)
        f1 = font('title', 70)
        lines = wrap(d, head, f1, 840)
        if len(lines) > 2:
            f1 = font('title', 56); lines = wrap(d, head, f1, 860)[:3]
        f2 = font(None, 34)
        sub_lines = wrap(d, sub, f2, 840)[:2]
        block = len(lines) * (f1.size + 12) + 16 + len(sub_lines) * 46
        y = 960 + max(0, (H - 200 - 960 - block) // 2)
        for ln in lines:
            w = d.textlength(ln, font=f1); d.text(((W - w) / 2, y), ln, font=f1, fill=PLUM); y += f1.size + 12
        y += 16
        for ln in sub_lines:
            w = d.textlength(ln, font=f2); d.text(((W - w) / 2, y), ln, font=f2, fill=BLUE); y += 46
        d.rounded_rectangle([30, H - 170, W - 30, H - 30], 36, fill=BLUE)
        d.rectangle([30, H - 170, W - 30, H - 120], fill=BLUE)
        f3 = font('script', 78); t = 'Cozy Paws'
        d.text(((W - d.textlength(t, font=f3)) / 2, H - 160), t, font=f3, fill=CREAM)
        c.save(dst, 'JPEG', quality=86, optimize=True, progressive=True)

    for p in all_prods:
        src = os.path.join(DATA, 'img', p['imagen'])
        shutil.copy(src, os.path.join(OUT, 'img', 'p', p['sku'] + '.jpg'))
        pin(os.path.join(pins_cache, p['sku'] + '.jpg'), p['short'], f"{p['kind']} · Shop on Etsy", [src])
    for g, ps in guides_live:
        pin(os.path.join(pins_cache, 'g-' + g['id'] + '.jpg'), g['h1'], 'Original gift ideas, printed in the USA',
            [os.path.join(DATA, 'img', p['imagen']) for p in ps[:4]])
    dps = hub_sections([p for p in all_prods if p['live'] <= HUB['live'] + dt.timedelta(days=1)])[0]
    pin(os.path.join(pins_cache, 'g-' + HUB['id'] + '.jpg'), HUB['h1'], 'Gifts for dog moms, dog dads, new puppies and every breed',
        [os.path.join(DATA, 'img', p['imagen']) for p in dps[:4]])
    for t in TOOLS:
        pin(os.path.join(pins_cache, 't-' + t['id'] + '.jpg'), t['h1'].split(':')[0], 'Free and instant at ' + CONFIG['url'].split('//')[1], [])
    pin(os.path.join(pins_cache, 'app-diary.jpg'), 'Paw Diary: free pet diary & vet reminders', 'Walks, meds, vaccines, weight and food for dogs and cats', [])
    pin(os.path.join(pins_cache, 'app-fun.jpg'), 'Paw Party: free fun app for dogs & cats', 'Human years, names, personality quiz, pet zodiac and cards', [])
    for f in os.listdir(pins_cache):
        shutil.copy(os.path.join(pins_cache, f), os.path.join(OUT, 'img', 'pin', f))
    # imagen para compartir (1200x630)
    og = Image.new('RGB', (1200, 630), CREAM)
    d = ImageDraw.Draw(og)
    lg = logo.copy(); lg.thumbnail((470, 470)); og.paste(lg, (70, 80), lg)
    d.text((590, 150), 'Cozy Paws', font=font('script', 150), fill=PLUM)
    f2 = font('title', 40)
    d.text((600, 360), 'Vintage club gifts for dogs, cats', font=f2, fill=BLUE)
    d.text((600, 412), '& the people who love them', font=f2, fill=BLUE)
    d.rectangle([0, 600, 1200, 608], fill=GOLD); d.rectangle([0, 608, 1200, 630], fill=BLUE)
    og.save(os.path.join(OUT, 'img', 'og.jpg'), 'JPEG', quality=86)


# ---------------------------------------------------------------- armado
def build(today):
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    prods, all_prods = load_products(today)
    # cada guía sale cuando tiene 2 productos, pero como mucho una guía nueva por día (goteo)
    sched, used = {}, set()
    for g in sorted(GUIDES, key=lambda g: (guide_live_date(g, all_prods) or dt.date.max, GUIDES.index(g))):
        d = guide_live_date(g, all_prods)
        if d is None:
            continue
        while d in used:
            d += dt.timedelta(days=1)
        used.add(d); sched[g['id']] = d
    for g in GUIDES:
        g['live'] = sched.get(g['id'])
    guides_live = [(g, guide_products(g, prods)) for g in GUIDES if g['live'] and g['live'] <= today]
    tools_live = [t for t in TOOLS if t['live'] <= today]
    make_images(all_prods, guides_live, tools_live)
    import contenido  # posts que no son de venta e historias para redes (cozypaws/contenido.py)
    contenido.render(OUT, prods)
    urls = []

    # inicio
    stamps = ''.join(f'<a class="stamp" href="/gifts/{g["id"]}/"><img src="/img/p/{ps[0]["sku"]}.jpg" alt="" loading="lazy" width="78" height="78"><span><b>{E(g["h1"])}</b><small>{len(ps)} gift ideas</small></span></a>' for g, ps in guides_live)
    tl = FUN_TILE + ''.join(f'<a class="tool" href="/tools/{t["id"]}/"><b>{E(t["h1"].split(":")[0])}</b><span>{E(t["desc"])}</span></a>' for t in tools_live)
    upcoming = [p for p in sorted(all_prods, key=lambda p: (p['live'], p['sku'])) if p['live'] > today][:8]
    if prods:
        shop = f'<h2>New in the shop</h2>{grid(prods[:12])}'
    else:
        shop = ''
    if upcoming and len(prods) < 8:
        first = upcoming[0]['live']
        shop += (f'<h2>Sneak peek: dropping soon</h2><p>Five new gifts a day, starting {first.strftime("%B")} {first.day}.</p>'
                 '<div class="grid">' + ''.join(card(p, soon=f'{p["live"].strftime("%b")} {p["live"].day}') for p in upcoming) + '</div>')
    body = ('<section class="hero"><div><span class="script">Cozy Paws</span>'
            '<p class="tag">Vintage club gifts for dogs, cats &amp; the people who love them</p>'
            '<p>Mugs, ornaments, cozy sweatshirts, blankets and goodies for the pets themselves. Original designs from Salt Lake City, printed on demand in the USA by our production partners.</p>'
            f'<a class="btn" href="{CONFIG["shop"]}" data-etsy="hero">Shop on Etsy</a><a class="btn ghost" href="/gifts/">Gift guides</a></div>'
            '<img src="/img/logo-ilustrado.png" alt="Cozy Paws Social Club logo: a sleeping dog and cat" width="340" height="340"></section>'
            + shop
            + (f'<h2>Gift guides</h2><div class="stamps">{stamps}</div>' if guides_live else '')
            + (f'<h2>Free pet tools</h2><div class="tools">{tl}</div>' if tl else '')
            + maker_block()
            + (signup() or '<section class="club"><img src="/img/sello-claro.png" alt="" width="150" height="150" loading="lazy"><div><span class="script">Join the club</span>'
            '<p>Every design is made for people who let the dog on the couch and the cat on the keyboard. New gifts drop all season long.</p>'
            f'<p style="margin-top:14px"><a class="btn" style="background:var(--gold);box-shadow:0 4px 0 #8f6a1f" href="{CONFIG["shop"]}" data-etsy="club">Visit the shop</a></p></div></section>'))
    page('/', 'Cozy Paws: Dog Mom and Cat Lover Gifts, Pet Christmas Gifts',
         'Original gifts for dog moms, cat lovers and their pets: mugs, ornaments, sweatshirts, blankets and pet accessories. Gift guides and free pet tools.',
         body, today, jsonld={'@context': 'https://schema.org', '@type': 'Organization', 'name': 'Cozy Paws', 'url': CONFIG['url'],
                              'logo': CONFIG['url'] + '/img/logo-ilustrado.png', 'email': CONFIG['contact'],
                              'founder': {'@type': 'Person', 'name': CONFIG['maker']},
                              'sameAs': [x for x in (CONFIG['shop'], CONFIG['pinterest'], CONFIG['instagram'], CONFIG['facebook']) if x]})
    urls.append(('/', today))

    # guías
    gl = ''.join(f'<a class="card" href="/gifts/{g["id"]}/"><img src="/img/p/{ps[0]["sku"]}.jpg" alt="" loading="lazy" width="450" height="450"><div class="t">{E(g["h1"])}</div><div class="m"><span>{len(ps)} gift ideas</span><span class="price">→</span></div></a>' for g, ps in guides_live)
    hub_dps = hub_sections(prods)[0] if HUB['live'] <= today else []
    feat = (f'<a class="feature" href="/gifts/{HUB["id"]}/"><div><b>{E(HUB["h1"])} ({today.year})</b>'
            'Ideas for dog moms, dog dads, new puppy owners, breed fans and the dog itself, sorted by owner and budget. →</div>'
            f'<img src="/img/pin/g-{HUB["id"]}.jpg" alt="" loading="lazy" width="220" height="330"></a>') if len(hub_dps) >= 2 else ''
    page('/gifts/', 'Gift Guides for Pet Lovers | Cozy Paws', 'Gift ideas for dog moms, dog dads, cat lovers and every breed fan.',
         f'<h1>Gift guides for pet lovers</h1><p class="lead">Ideas for every dog mom, cat dad and breed fan on your list.</p>{feat}<div class="grid">{gl}</div>' if gl else '<h1>Gift guides</h1><p class="lead">The first guides open on November 17, with five new gifts a day. Meanwhile, try our <a href="/tools/">free pet tools</a>.</p>', today)
    urls.append(('/gifts/', today))
    if feat and hub_page(prods, guides_live, today):
        urls.append((f'/gifts/{HUB["id"]}/', today))
    for g, ps in guides_live:
        others = ''.join(f'<a href="/gifts/{o["id"]}/">{E(o["h1"])}</a>' for o, _ in guides_live if o is not g)
        if feat and re.search(HUB['dog'], g['h1'].lower() + ' ' + (g['match'] or '')):
            others = f'<a href="/gifts/{HUB["id"]}/"><b>{E(HUB["h1"])}</b></a>' + others
        tips = ''.join(f'<li>{E(t)}</li>' for t in g['tips'])
        body = (f'<h1>{E(g["h1"])}</h1><p class="lead">{E(g["intro"])}</p>{grid(ps)}<h2>Tips</h2><ul class="tips">{tips}</ul>'
                f'<p><a class="btn" href="{CONFIG["shop"]}" data-etsy="guide-{g["id"]}">See everything on Etsy</a></p><h2>More gift guides</h2><div class="pills">{others}</div>')
        ld = {'@context': 'https://schema.org', '@type': 'ItemList', 'name': g['h1'],
              'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'url': f'{CONFIG["url"]}/p/{p["slug"]}/'} for i, p in enumerate(ps)]}
        page(f'/gifts/{g["id"]}/', f'{g["h1"]} ({today.year}) | Cozy Paws', g['intro'][:155], body, today,
             image=f'/img/pin/g-{g["id"]}.jpg', jsonld=ld)
        urls.append((f'/gifts/{g["id"]}/', max(p['live'] for p in ps)))

    # productos
    for p in prods:
        related = [o for o in prods if o is not p and set(o['tags'][:4]) & set(p['tags'][:4])][:4] or [o for o in prods if o is not p][:4]
        in_guides = ''.join(f'<a href="/gifts/{g["id"]}/">{E(g["h1"])}</a>' for g, ps in guides_live if p in ps)
        body = (f'<div class="prod"><img src="/img/p/{p["sku"]}.jpg" alt="{E(p["short"])}" width="900" height="900"><div>'
                f'<div class="kind">{E(p["kind"])}</div><h1>{E(p["short"])}</h1><p class="bigprice">${E(p["precio"])}</p><p>{E(p["texto"])}</p>'
                + (f'<ul class="perks"><li>Printable PDF with an original Cozy Paws design</li><li>Instant download after purchase on Etsy</li><li>Print at home or at any print shop, as many times as you need</li>'
                   if p['kind'].startswith('Printable') else
                   f'<ul class="perks"><li>{E(p["kind"])} with an original Cozy Paws design</li><li>Printed on demand in the USA</li><li>Ships from our production partner (Printify)</li>'
                   + (f'<li>Order by Dec 10 for Christmas delivery in the US</li>' if today <= CONFIG['christmas_cutoff'] else ''))
                + f'</ul><p><a class="btn" href="{E(p["etsy"])}" data-etsy="{E(p["sku"])}" rel="nofollow">See it on Etsy</a></p>'
                + (f'<p>Part of: <span class="pills">{in_guides}</span></p>' if in_guides else '') + '</div></div>'
                + (f'<h2>You may also like</h2>{grid(related)}' if related else ''))
        ld = {'@context': 'https://schema.org', '@type': 'Product', 'name': p['short'], 'description': p['texto'], 'image': f'{CONFIG["url"]}/img/p/{p["sku"]}.jpg',
              'brand': {'@type': 'Brand', 'name': 'Cozy Paws'}, 'sku': p['sku'],
              'offers': {'@type': 'Offer', 'price': p['precio'], 'priceCurrency': 'USD', 'availability': 'https://schema.org/InStock', 'url': p['etsy']}}
        page(f'/p/{p["slug"]}/', f'{p["short"]} | Cozy Paws', p['titulo'][:155], body, today, image=f'/img/pin/{p["sku"]}.jpg', jsonld=ld)
        urls.append((f'/p/{p["slug"]}/', p['live']))

    # herramientas
    tli = FUN_TILE + ''.join(f'<a class="tool" href="/tools/{t["id"]}/"><b>{E(t["h1"].split(":")[0])}</b><span>{E(t["desc"])}</span></a>' for t in tools_live)
    page('/tools/', 'Free Pet Tools: Dog Age, Cat Age, Dog Food Calculator | Cozy Paws', 'Free calculators and generators for dog and cat owners.',
         f'<h1>Free pet tools</h1><p class="lead">Quick, free calculators for dog and cat people. Nothing to sign up for.</p><div class="tools">{tli}</div>'
         '<p class="pills" style="margin-top:18px"><a href="/breeds/">Breed guides: weight, age and food</a><a href="/names/">Pet name lists</a></p>' if tli else '<h1>Free pet tools</h1><p>Coming soon.</p>', today)
    urls.append(('/tools/', today))
    for t in tools_live:
        pet_ps = [p for p in prods if t['pet'] == 'both' or t['pet'] in p['hay']][:4]
        body = (f'<h1>{E(t["h1"])}</h1><p class="lead">{E(t["desc"])}</p>{TOOL_BODY[t["id"]]}'
                + (f'<h2>Gifts for {"dog" if t["pet"] == "dog" else "cat" if t["pet"] == "cat" else "pet"} lovers</h2>{grid(pet_ps)}' if pet_ps else ''))
        ld = {'@context': 'https://schema.org', '@type': 'WebApplication', 'name': t['h1'].split(':')[0], 'applicationCategory': 'UtilitiesApplication',
              'operatingSystem': 'Any', 'offers': {'@type': 'Offer', 'price': '0', 'priceCurrency': 'USD'}, 'url': f'{CONFIG["url"]}/tools/{t["id"]}/'}
        page(f'/tools/{t["id"]}/', f'{t["h1"]} | Cozy Paws', t['desc'], body, today, image=f'/img/pin/t-{t["id"]}.jpg', jsonld=ld)
        urls.append((f'/tools/{t["id"]}/', t['live']))

    # páginas de confianza: about, envíos y devoluciones, preguntas, contacto
    trust_pages(today, prods)
    urls += [(u, PAGES_UPDATED) for u in ('/about/', '/shipping-returns/', '/faq/', '/contact/')]

    # apps (PWA): Paw Party en /fun/ y /fun/es/ (cozypaws/apps/)
    import apps.apps as cpapps
    urls += cpapps.build_fun(OUT, CONFIG, all_prods, today)
    urls += cpapps.build_diary(OUT, CONFIG, all_prods, today)
    # páginas por raza y listas de nombres (goteo 1+1 por día; cada una con pin en el feed): cozypaws/apps/seo_pages.py
    from apps import seo_pages
    seo_urls, seo_items, nb, nn, tb, tn = seo_pages.build_seo(page, CONFIG, OUT, DATA, today, cpapps.stamp_links(CONFIG, all_prods, today))
    urls += seo_urls
    print(f'razas {nb}/{tb}, listas de nombres {nn}/{tn}')
    # artículos (goteo 1 por día desde el 16 nov; textos ya escritos en cozypaws/articulos/; cada uno con pin en el feed): cozypaws/apps/articulos.py
    from apps import articulos
    blog_urls, blog_items, na = articulos.build_blog(page, CONFIG, OUT, DATA, today, seo_pages.pin_maker)
    urls += blog_urls
    print(f'artículos {na}/{len(articulos.load())}')
    # cada artículo también sale como post e historia en Instagram y Facebook (imágenes acá; publica social.py)
    contenido.render_articulos(OUT, [a for a in articulos.load() if a['live'] <= today])
    items_apps = [(dt.date(2026, 11, 15), 'Paw Party: free fun app for dogs and cats', '/fun/', '/img/pin/app-fun.jpg',
                   'Dog and cat age in human years, pet name ideas, a personality quiz, pet zodiac and birthday cards. Free, no sign up, install it on your phone.', 'app-fun'),
                  (dt.date(2026, 11, 16), 'Paw Diary: free pet diary and vet reminder app', '/diary/', '/img/pin/app-diary.jpg',
                   'Log walks, meals and meds, get vaccine and flea pill reminders, track weight and see how much to feed your dog or cat. Free, works offline.', 'app-diary')]
    if CONFIG['adsense_on']:
        open(os.path.join(OUT, 'ads.txt'), 'w').write(f"google.com, {CONFIG['adsense'].replace('ca-', '')}, DIRECT, f08c47fec0942fa0\n")

    # privacidad, términos y 404
    page('/privacy/', 'Privacy Policy | Cozy Paws', 'How Cozy Paws uses cookies and data.', f"""<h1>Privacy policy</h1>
<p>This website and its apps (including Paw Party) are run by {CONFIG['company']}, a sole proprietorship based in Utah, USA, under the Cozy Paws brand. We do not sell products on this site: purchases happen on Etsy, under Etsy's own privacy policy.</p>
<p><b>Cookies and stats.</b> Only if you click OK in the cookie notice, we load Google Analytics (anonymous visit statistics) and the Meta Pixel (to measure ads and visits). If you click "No thanks", nothing is loaded. You can change your choice by clearing this site's data in your browser.</p>
<p><b>Ads.</b> In the future we may show ads from Google AdSense. If we do, they load only after you click OK, and Google may use cookies to show and measure them. See <a href="https://policies.google.com/technologies/ads" rel="noopener">how Google uses data in ads</a>.</p>
<p><b>Calculators and apps.</b> The pet tools and the Paw Party and Paw Diary apps run in your browser. What you enter (your pet's name, birthday, breed, weight, photos, diary notes, reminders, saved names) is stored only on your own device (browser storage) and is never sent to us. You can delete it at any time by deleting it in the app (Paw Diary has "Delete all my data") or clearing this site's data in your browser. We do not ask for your name, email or location in the tools.</p>
""" + ("""<p><b>Email club.</b> If you join our email club, we store your email address (and the language of the form) with MailerLite, our email provider, to send you the free checklist, new gift drops and offers. Every email has an unsubscribe link. We never sell or share your email. To be removed, unsubscribe or write to us.</p>""" if CONFIG.get('mailerlite_action') else '') + (f"""<p><b>Optional accounts.</b> In Paw Party and Paw Diary you can choose to sign in (with Google or with a link sent to your email) to keep your data on all your devices. If you do, we store your email address and a copy of your app data (pets, small pet photo, diary notes, reminders and saved names) in Google Firebase (Firestore), in the United States. Diary photos are not uploaded. Only you can read your data. You can delete your account and the cloud copy at any time from the Account button in the app, or by writing to us.</p>""" if CONFIG.get('firebase') else '') + f"""<p><b>Children.</b> The site is meant for a general audience and is not directed to children under 13. We do not knowingly collect personal information from children.</p>
<p><b>Your rights.</b> Because we do not keep personal data from the apps, there is nothing for us to access or delete. For questions about analytics data, write to us.</p>
<p><b>Contact.</b> <a href="mailto:{CONFIG['contact']}">{CONFIG['contact']}</a></p><p class="note">Last updated: November 14, 2026.</p>""", today)
    urls.append(('/privacy/', dt.date(2026, 11, 14)))
    page('/terms/', 'Terms of Use | Cozy Paws', 'Terms of use for the Cozy Paws website and the Paw Party and Paw Diary apps.', f"""<h1>Terms of use</h1>
<p>This website and the Paw Party and Paw Diary apps are provided by {CONFIG['company']} (a sole proprietorship, Cozy Paws brand). By using them you agree to these terms.</p>
<p><b>Free, for fun and general information.</b> The calculators, quiz, zodiac, diary, reminders, food calculator and other tools are free and for entertainment and general information only. They are not veterinary advice. Always ask your vet about your pet's health, food and weight.</p>
<p><b>Your content.</b> Photos and text you add stay on your device. You are responsible for having the right to use the photos you add. Cards you make are yours to download, print and share for personal, non-commercial use. The Cozy Paws stamps and logo remain our property and may not be resold.</p>
<p><b>Products.</b> Cozy Paws designs are created by Azu in Salt Lake City and printed on demand by our production partners. Purchases happen on Etsy under Etsy's terms.</p>
<p><b>No warranty.</b> The site and apps are provided "as is", without warranties. Reminders depend on your device and calendar; we cannot guarantee they will fire, so do not rely only on them for medication. We are not liable for lost data stored on your device or for decisions made based on the tools. Back up anything important (Paw Diary has a backup button).</p>
<p><b>Changes.</b> We may update these terms; the date below shows the latest version. Contact: <a href="mailto:{CONFIG['contact']}">{CONFIG['contact']}</a>.</p>
<p class="note">Last updated: November 14, 2026. Governed by the laws of the State of Utah, USA.</p>""", today)
    urls.append(('/terms/', dt.date(2026, 11, 14)))
    page('/404.html', 'Page not found | Cozy Paws', 'Page not found.', '<h1>Oops, this page ran off to chase a squirrel</h1><p><a href="/">Go to the home page</a> or <a href="/gifts/">see the gift guides</a>.</p>', today, canonical=False)

    # página de vuelta de la autorización de Etsy (app "Cozy Paws Shop Tools"): lleva el código a un issue
    # "etsy-code" de crux-report, donde un workflow lo guarda (tools/etsy_digital). No va al sitemap.
    os.makedirs(os.path.join(OUT, 'etsy-auth'), exist_ok=True)
    open(os.path.join(OUT, 'etsy-auth', 'index.html'), 'w', encoding='utf-8').write(ETSY_AUTH_HTML)

    # sitemap, robots, feed
    sm = ''.join(f'<url><loc>{CONFIG["url"]}{u}</loc><lastmod>{d.isoformat()}</lastmod></url>' for u, d in urls)
    open(os.path.join(OUT, 'sitemap.xml'), 'w').write(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{sm}</urlset>')
    open(os.path.join(OUT, INDEXNOW_KEY + '.txt'), 'w').write(INDEXNOW_KEY)
    open(os.path.join(OUT, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\nSitemap: {CONFIG["url"]}/sitemap.xml\n')
    open(os.path.join(OUT, '_headers'), 'w').write('/img/*\n  Cache-Control: public, max-age=604800\n/fun/sw.js\n  Cache-Control: no-cache\n/diary/sw.js\n  Cache-Control: no-cache\n/*.webmanifest\n  Content-Type: application/manifest+json\n')

    items = []
    for p in prods:
        items.append((p['live'], f'{p["short"]}', f'/p/{p["slug"]}/', f'/img/pin/{p["sku"]}.jpg',
                      f'{p["texto"]} {p["kind"]} from ${p["precio"]}. Shop Cozy Paws on Etsy.', p['sku']))
    for g, ps in guides_live:
        items.append((g['live'], f'{g["h1"]}: {len(ps)} gift ideas', f'/gifts/{g["id"]}/', f'/img/pin/g-{g["id"]}.jpg', g['intro'][:300], 'g-' + g['id']))
    if feat:
        items.append((HUB['live'], f'{HUB["h1"]} {today.year}', f'/gifts/{HUB["id"]}/', f'/img/pin/g-{HUB["id"]}.jpg', HUB['intro'][:300], 'g-' + HUB['id']))
    for t in tools_live:
        items.append((t['live'], t['h1'], f'/tools/{t["id"]}/', f'/img/pin/t-{t["id"]}.jpg', t['desc'], 't-' + t['id']))
    items += [x for x in items_apps if x[0] <= today] + seo_items + blog_items
    items.sort(key=lambda x: x[0], reverse=True)
    xi = ''
    for d, title, path, img, desc, gid in items[:60]:
        pub = format_datetime(dt.datetime(d.year, d.month, d.day, 15, 30, tzinfo=dt.timezone.utc))
        xi += (f'<item><title>{E(title)}</title><link>{CONFIG["url"]}{path}</link><guid isPermaLink="false">ww-{gid}</guid><pubDate>{pub}</pubDate>'
               f'<description>{E(desc)}</description><enclosure url="{CONFIG["url"]}{img}" type="image/jpeg" length="0"/>'
               f'<media:content url="{CONFIG["url"]}{img}" medium="image" type="image/jpeg"/></item>')
    open(os.path.join(OUT, 'feed.xml'), 'w', encoding='utf-8').write(
        f'<?xml version="1.0" encoding="UTF-8"?><rss version="2.0" xmlns:media="http://search.yahoo.com/mrss/" xmlns:atom="http://www.w3.org/2005/Atom"><channel>'
        f'<title>Cozy Paws: gifts for pet lovers</title><link>{CONFIG["url"]}/</link><description>New gifts for dog moms, cat lovers and their pets, plus free pet tools.</description>'
        f'<atom:link href="{CONFIG["url"]}/feed.xml" rel="self" type="application/rss+xml"/><language>en-us</language>{xi}</channel></rss>')
    print(f'{today}: {len(prods)} productos visibles de {len(all_prods)}, {len(guides_live)} guías, {len(tools_live)} herramientas, {len(items)} items en el RSS')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--hoy', default=None)
    a = ap.parse_args()
    # fecha de Utah (America/Denver ~ UTC-7) para que el día cambie a la mañana de Azu
    hoy = dt.date.fromisoformat(a.hoy) if a.hoy else (dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=7)).date()
    build(hoy)
