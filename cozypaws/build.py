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

CONFIG = dict(
    name='Cozy Paws',
    url='https://cozypaws.pages.dev',          # dirección de Cloudflare Pages (cambiar si se compra dominio)
    shop='https://www.etsy.com/shop/ChalkPaperStudio',  # tienda de Etsy (el nombre viejo redirige solo al nuevo; poner el nuevo cuando esté: Cozy Paws)
    pinterest='',          # https://www.pinterest.com/<usuario>/ cuando exista
    ga4='',                # G-XXXXXXX (GA4 de esta web)
    pixel='',              # ID del Pixel de Meta
    pinterest_verify='',   # contenido de la etiqueta meta "p:domain_verify" para reclamar la web en Pinterest
    google_verify='',      # contenido de la meta "google-site-verification" (Search Console), si se usa
    contact='support@skyesolutionsai.com',
    company='Skye Solutions AI',
    christmas_cutoff=dt.date(2026, 12, 10),
)
E = html.escape

# ---------------------------------------------------------------- productos
KINDS = [  # (palabra en el título, tipo en inglés)
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
        live = dt.date.fromisoformat(r['dia']) + dt.timedelta(days=1)
        st = short_title(r['titulo'])
        p = dict(r, live=live, short=st, kind=kind_of(r['titulo']), slug=slug(st) + '-' + slug(r['sku']),
                 tags=[t.strip() for t in r['etiquetas'].split(',') if t.strip()],
                 etsy=links.get(r['sku']) or f"{CONFIG['shop']}?search_query={quote_plus(st)}")
        p['hay'] = (r['titulo'] + ' ' + r['etiquetas']).lower()
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
    dict(id='pet-lover-gifts-under-25', h1='Pet Lover Gifts Under $25', match=None, max_price=25,
         intro='Secret Santa, coworkers, teachers who love dogs: affordable gifts under $25 for pet people.',
         tips=['Stickers, cards and ornaments make great stocking stuffers.']),
    dict(id='pet-mugs', h1='Dog and Cat Mugs', match=r'mug|tumbler',
         intro='Coffee tastes better with a dog (or cat) on the mug. Classic white mugs, colored accent mugs, latte mugs, camping mugs and tumblers.',
         tips=['All ceramic mugs are dishwasher and microwave safe.']),
    dict(id='pet-stationery-and-gift-wrap', h1='Pet Stationery, Cards and Gift Wrap', match=r'wrapping|gift wrap|sticker|journal|notebook|calendar|card',
         intro='Paper goods for pet people: wrapping paper with paw prints, sticker sheets, journals, notebooks, a 2027 calendar and holiday cards.',
         tips=['The 2027 calendar is a great gift for planners.']),
]


def guide_products(g, prods):
    if g.get('max_price'):
        return [p for p in prods if float(p['precio'] or 0) < g['max_price']]
    rx = re.compile(g['match'])
    return [p for p in prods if rx.search(p['hay'])]


def guide_live_date(g, all_prods):
    ps = sorted(guide_products(g, all_prods), key=lambda p: p['live'])
    return ps[1]['live'] if len(ps) >= 2 else None


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

# ---------------------------------------------------------------- html
CSS = """*{box-sizing:border-box}body{margin:0;font-family:system-ui,-apple-system,'Segoe UI',sans-serif;background:#fbf6ef;color:#2b2622;line-height:1.6}
a{color:#a8333a}header{background:#2f4a40;color:#fbf6ef}header .in,footer .in{max-width:1100px;margin:0 auto;padding:14px 22px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px}
header a{color:#fbf6ef;text-decoration:none}.logo{font-family:Georgia,serif;font-size:25px;font-weight:bold}nav a{margin-left:16px;font-size:15px}
.bar{background:#a8333a;color:#fff;text-align:center;font-size:14px;padding:7px 12px}
main{max-width:1100px;margin:0 auto;padding:10px 22px 40px}h1,h2{font-family:Georgia,serif;line-height:1.2}h1{font-size:38px;margin:22px 0 10px}h2{font-size:26px;margin:34px 0 12px}
.lead{font-size:18px;max-width:760px;color:#4b433c}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:18px}
.card{background:#fff;border-radius:14px;overflow:hidden;text-decoration:none;color:inherit;box-shadow:0 1px 4px rgba(0,0,0,.07);display:flex;flex-direction:column}
.card img{width:100%;aspect-ratio:1;object-fit:cover;display:block}.card .t{padding:10px 12px 4px;font-weight:600;font-size:15px}.card .m{padding:0 12px 12px;color:#6b625a;font-size:14px}
.pills a{display:inline-block;margin:4px 6px 4px 0;padding:7px 13px;border-radius:99px;background:#fff;border:1px solid #e3d8ca;text-decoration:none;color:#2b2622;font-size:14px}
.btn{display:inline-block;background:#a8333a;color:#fff!important;padding:13px 22px;border-radius:10px;text-decoration:none;font-weight:700;border:0;font-size:16px;cursor:pointer}
.prod{display:grid;grid-template-columns:1fr 1fr;gap:30px;align-items:start}.prod img{width:100%;border-radius:14px}@media(max-width:720px){.prod{grid-template-columns:1fr}h1{font-size:30px}}
.price{font-size:22px;font-weight:700}.tips li{margin:4px 0}.calc{background:#fff;border-radius:14px;padding:20px;max-width:620px;box-shadow:0 1px 4px rgba(0,0,0,.07)}
.calc label{display:block;margin:0 0 14px}.calc input,.calc select{font-size:17px;padding:8px;border:1px solid #d9cdbd;border-radius:8px;margin-left:6px;max-width:220px}
.result{font-size:20px;background:#f2ebe1;border-radius:10px;padding:14px;margin-top:8px}.names{columns:2;margin:0;padding-left:20px}
table{border-collapse:collapse;background:#fff}td,th{border:1px solid #e3d8ca;padding:6px 12px;text-align:center}.note{color:#6b625a;font-size:14px}
footer{background:#efe6da;margin-top:40px;font-size:14px}footer a{margin-right:14px}
#cc{position:fixed;bottom:12px;left:12px;right:12px;max-width:560px;background:#2b2622;color:#fff;padding:14px 16px;border-radius:12px;font-size:14px;display:none;z-index:9}
#cc button{margin:8px 8px 0 0;padding:7px 14px;border-radius:8px;border:0;cursor:pointer}#cc a{color:#f6c9a8}"""


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


def page(path, title, desc, body, today, image=None, jsonld=None, canonical=True):
    url = CONFIG['url'] + path
    img = CONFIG['url'] + (image or '/img/og.jpg')
    days = (CONFIG['christmas_cutoff'] - today).days
    bar = (f'Order by Dec 10 for Christmas delivery in the US ({days} days left)' if 0 <= days <= 40
           else 'Original pet lover gifts, printed on demand in the USA')
    metas = ''
    if CONFIG['pinterest_verify']:
        metas += f'<meta name="p:domain_verify" content="{E(CONFIG["pinterest_verify"])}">'
    if CONFIG['google_verify']:
        metas += f'<meta name="google-site-verification" content="{E(CONFIG["google_verify"])}">'
    ld = f'<script type="application/ld+json">{json.dumps(jsonld)}</script>' if jsonld else ''
    pin = f' · <a href="{CONFIG["pinterest"]}" rel="me">Pinterest</a>' if CONFIG['pinterest'] else ''
    doc = f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)}</title><meta name="description" content="{E(desc)}">{'<link rel="canonical" href="' + url + '">' if canonical else ''}
<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:image" content="{img}"><meta property="og:url" content="{url}"><meta property="og:type" content="website">
<meta name="twitter:card" content="summary_large_image">{metas}
<link rel="alternate" type="application/rss+xml" title="{CONFIG['name']}" href="/feed.xml"><link rel="icon" href="/img/icon.png"><style>{CSS}</style>{ld}{analytics()}</head><body>
<div class="bar">{bar}</div>
<header><div class="in"><a class="logo" href="/">Cozy Paws</a><nav><a href="/gifts/">Gift guides</a><a href="/tools/">Pet tools</a><a href="{CONFIG['shop']}" data-etsy="shop">Etsy shop</a></nav></div></header>
<main>{body}</main>
<footer><div class="in"><div>© {today.year} Cozy Paws · Original pet lover gifts designed in Salt Lake City, Utah{pin}</div>
<div><a href="/privacy/">Privacy</a><a href="/feed.xml">RSS</a><a href="mailto:{CONFIG['contact']}">Contact</a></div></div></footer>
<div id="cc">We use cookies for anonymous stats (Google Analytics) and ads measurement (Meta). <a href="/privacy/">Privacy</a><br><button class="y">OK</button><button class="n">No thanks</button></div>
</body></html>"""
    if path.endswith('.html'):
        f = os.path.join(OUT, path.strip('/'))
    else:
        d = os.path.join(OUT, path.strip('/'))
        os.makedirs(d, exist_ok=True)
        f = os.path.join(d, 'index.html')
    open(f, 'w', encoding='utf-8').write(doc)


def card(p):
    return (f'<a class="card" href="/p/{p["slug"]}/"><img src="/img/p/{p["sku"]}.jpg" alt="{E(p["short"])}" loading="lazy" width="450" height="450">'
            f'<div class="t">{E(p["short"])}</div><div class="m">{E(p["kind"])} · from ${E(p["precio"])}</div></a>')


def grid(ps):
    return '<div class="grid">' + ''.join(card(p) for p in ps) + '</div>'


# ---------------------------------------------------------------- imágenes
def make_images(all_prods, guides_live, tools_live):
    from PIL import Image, ImageDraw, ImageFont
    os.makedirs(os.path.join(OUT, 'img', 'p'), exist_ok=True)
    os.makedirs(os.path.join(OUT, 'img', 'pin'), exist_ok=True)
    pins_cache = os.path.join(DATA, 'pins')
    os.makedirs(pins_cache, exist_ok=True)

    def font(bold, size):
        for f in (['/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf'] if bold else ['/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']):
            if os.path.exists(f):
                return ImageFont.truetype(f, size)
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

    def pin(dst, head, sub, imgs):
        if os.path.exists(dst):
            return
        W, H = 1000, 1500
        c = Image.new('RGB', (W, H), (251, 246, 239))
        if len(imgs) == 1:
            im = Image.open(imgs[0]).convert('RGB'); im = im.resize((900, 900))
            c.paste(im, (50, 50))
        elif imgs:
            for i, f in enumerate(imgs[:4]):
                im = Image.open(f).convert('RGB').resize((445, 445))
                c.paste(im, (50 + (i % 2) * 455, 50 + (i // 2) * 455))
        else:
            d0 = ImageDraw.Draw(c)
            d0.rectangle([50, 50, 950, 950], fill=(47, 74, 64))
            for i in range(4):  # huellitas simples
                x, y = 300 + (i % 2) * 380, 300 + (i // 2) * 360
                d0.ellipse([x - 70, y - 50, x + 70, y + 70], fill=(168, 51, 58))
                for dx, dy in ((-75, -95), (-25, -125), (25, -125), (75, -95)):
                    d0.ellipse([x + dx - 24, y + dy - 30, x + dx + 24, y + dy + 30], fill=(168, 51, 58))
        d = ImageDraw.Draw(c)
        f1 = font(True, 64)
        lines = wrap(d, head, f1, 880)
        if len(lines) > 3:
            f1 = font(True, 52); lines = wrap(d, head, f1, 880)[:4]
        f2 = font(False, 34)
        sub_lines = wrap(d, sub, f2, 860)[:2]
        block = len(lines) * (f1.size + 14) + 10 + len(sub_lines) * 46
        y = 960 + max(0, (H - 90 - 960 - block) // 2)
        for ln in lines:
            w = d.textlength(ln, font=f1); d.text(((W - w) / 2, y), ln, font=f1, fill=(43, 38, 34)); y += f1.size + 14
        for ln in sub_lines:
            w = d.textlength(ln, font=f2); d.text(((W - w) / 2, y + 10), ln, font=f2, fill=(107, 98, 90)); y += 46
        d.rectangle([0, H - 90, W, H], fill=(47, 74, 64))
        f3 = font(True, 36); t = 'Cozy Paws'
        d.text(((W - d.textlength(t, font=f3)) / 2, H - 70), t, font=f3, fill=(251, 246, 239))
        c.save(dst, 'JPEG', quality=84, optimize=True, progressive=True)

    for p in all_prods:
        src = os.path.join(DATA, 'img', p['imagen'])
        shutil.copy(src, os.path.join(OUT, 'img', 'p', p['sku'] + '.jpg'))
        pin(os.path.join(pins_cache, p['sku'] + '.jpg'), p['short'], f"{p['kind']} · Shop on Etsy", [src])
    for g, ps in guides_live:
        pin(os.path.join(pins_cache, 'g-' + g['id'] + '.jpg'), g['h1'], 'Original gift ideas, printed in the USA',
            [os.path.join(DATA, 'img', p['imagen']) for p in ps[:4]])
    for t in TOOLS:
        pin(os.path.join(pins_cache, 't-' + t['id'] + '.jpg'), t['h1'].split(':')[0], 'Free and instant at cozypaws.pages.dev', [])
    for f in os.listdir(pins_cache):
        shutil.copy(os.path.join(pins_cache, f), os.path.join(OUT, 'img', 'pin', f))
    # imagen para compartir e ícono
    first = [os.path.join(DATA, 'img', p['imagen']) for p in all_prods[:4]]
    og = Image.new('RGB', (1200, 630), (251, 246, 239))
    for i, f in enumerate(first):
        og.paste(Image.open(f).convert('RGB').resize((290, 290)), (20 + i * 295, 20))
    d = ImageDraw.Draw(og)
    f1 = font(True, 70); t = 'Cozy Paws'
    d.text(((1200 - d.textlength(t, font=f1)) / 2, 380), t, font=f1, fill=(47, 74, 64))
    f2 = font(False, 34); t = 'Gifts for dog moms, cat lovers and their pets'
    d.text(((1200 - d.textlength(t, font=f2)) / 2, 485), t, font=f2, fill=(107, 98, 90))
    og.save(os.path.join(OUT, 'img', 'og.jpg'), 'JPEG', quality=84)
    ic = Image.new('RGB', (192, 192), (47, 74, 64)); d = ImageDraw.Draw(ic)
    d.ellipse([56, 86, 136, 156], fill=(251, 246, 239))
    for x, y in ((50, 62), (80, 40), (112, 40), (142, 62)):
        d.ellipse([x - 15, y - 18, x + 15, y + 18], fill=(251, 246, 239))
    ic.save(os.path.join(OUT, 'img', 'icon.png'))


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
    make_images(prods, guides_live, tools_live)
    urls = []

    # inicio
    pills = '<div class="pills">' + ''.join(f'<a href="/gifts/{g["id"]}/">{E(g["h1"])}</a>' for g, _ in guides_live) + '</div>'
    tl = ''.join(f'<li><a href="/tools/{t["id"]}/">{E(t["h1"].split(":")[0])}</a>: {E(t["desc"])}</li>' for t in tools_live)
    body = ('<h1>Gifts for dog moms, cat lovers and their furry best friends</h1>'
            '<p class="lead">Original designs on mugs, ornaments, cozy clothes and pet accessories, drawn in Salt Lake City and printed on demand in the USA. '
            'Every product is sold through our Etsy shop.</p>'
            f'<p><a class="btn" href="{CONFIG["shop"]}" data-etsy="shop">Visit the Etsy shop</a></p>'
            + (f'<h2>Gift guides</h2>{pills}' if guides_live else '')
            + (f'<h2>New in the shop</h2>{grid(prods[:12])}' if prods else '<h2>New designs start dropping on November 17</h2><p>Three new gifts a day until Christmas. Check back soon, or try our free pet tools below.</p>')
            + (f'<h2>Free pet tools</h2><ul>{tl}</ul>' if tl else ''))
    page('/', 'Cozy Paws: Dog Mom and Cat Lover Gifts, Pet Christmas Gifts',
         'Original gifts for dog moms, cat lovers and their pets: mugs, ornaments, sweatshirts, blankets and pet accessories. Gift guides and free pet tools.',
         body, today, jsonld={'@context': 'https://schema.org', '@type': 'Organization', 'name': 'Cozy Paws', 'url': CONFIG['url'],
                              'sameAs': [x for x in (CONFIG['shop'], CONFIG['pinterest']) if x]})
    urls.append(('/', today))

    # guías
    gl = ''.join(f'<a class="card" href="/gifts/{g["id"]}/"><img src="/img/p/{ps[0]["sku"]}.jpg" alt="" loading="lazy"><div class="t">{E(g["h1"])}</div><div class="m">{len(ps)} gift ideas</div></a>' for g, ps in guides_live)
    page('/gifts/', 'Gift Guides for Pet Lovers | Cozy Paws', 'Gift ideas for dog moms, dog dads, cat lovers and every breed fan.',
         f'<h1>Gift guides for pet lovers</h1><div class="grid">{gl}</div>' if gl else '<h1>Gift guides</h1><p>Coming soon.</p>', today)
    urls.append(('/gifts/', today))
    for g, ps in guides_live:
        others = ''.join(f'<a href="/gifts/{o["id"]}/">{E(o["h1"])}</a>' for o, _ in guides_live if o is not g)
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
                f'<h1>{E(p["short"])}</h1><p class="price">From ${E(p["precio"])}</p><p>{E(p["texto"])}</p>'
                f'<ul><li>{E(p["kind"])} with an original Cozy Paws design</li><li>Printed on demand in the USA</li><li>Ships from our production partner (Printify)</li>'
                + (f'<li>Order by Dec 10 for Christmas delivery in the US</li>' if today <= CONFIG['christmas_cutoff'] else '')
                + f'</ul><p><a class="btn" href="{E(p["etsy"])}" data-etsy="{E(p["sku"])}" rel="nofollow">See it on Etsy</a></p>'
                + (f'<p>Part of: <span class="pills">{in_guides}</span></p>' if in_guides else '') + '</div></div>'
                + (f'<h2>You may also like</h2>{grid(related)}' if related else ''))
        ld = {'@context': 'https://schema.org', '@type': 'Product', 'name': p['short'], 'description': p['texto'], 'image': f'{CONFIG["url"]}/img/p/{p["sku"]}.jpg',
              'brand': {'@type': 'Brand', 'name': 'Cozy Paws'}, 'sku': p['sku'],
              'offers': {'@type': 'Offer', 'price': p['precio'], 'priceCurrency': 'USD', 'availability': 'https://schema.org/InStock', 'url': p['etsy']}}
        page(f'/p/{p["slug"]}/', f'{p["short"]} | Cozy Paws', p['titulo'][:155], body, today, image=f'/img/pin/{p["sku"]}.jpg', jsonld=ld)
        urls.append((f'/p/{p["slug"]}/', p['live']))

    # herramientas
    tli = ''.join(f'<a class="card" href="/tools/{t["id"]}/"><img src="/img/pin/t-{t["id"]}.jpg" alt="" loading="lazy" style="aspect-ratio:2/3"><div class="t">{E(t["h1"].split(":")[0])}</div><div class="m">{E(t["desc"])}</div></a>' for t in tools_live)
    page('/tools/', 'Free Pet Tools: Dog Age, Cat Age, Dog Food Calculator | Cozy Paws', 'Free calculators and generators for dog and cat owners.',
         f'<h1>Free pet tools</h1><div class="grid">{tli}</div>' if tli else '<h1>Free pet tools</h1><p>Coming soon.</p>', today)
    urls.append(('/tools/', today))
    for t in tools_live:
        pet_ps = [p for p in prods if t['pet'] == 'both' or t['pet'] in p['hay']][:4]
        body = (f'<h1>{E(t["h1"])}</h1><p class="lead">{E(t["desc"])}</p>{TOOL_BODY[t["id"]]}'
                + (f'<h2>Gifts for {"dog" if t["pet"] == "dog" else "cat" if t["pet"] == "cat" else "pet"} lovers</h2>{grid(pet_ps)}' if pet_ps else ''))
        ld = {'@context': 'https://schema.org', '@type': 'WebApplication', 'name': t['h1'].split(':')[0], 'applicationCategory': 'UtilitiesApplication',
              'operatingSystem': 'Any', 'offers': {'@type': 'Offer', 'price': '0', 'priceCurrency': 'USD'}, 'url': f'{CONFIG["url"]}/tools/{t["id"]}/'}
        page(f'/tools/{t["id"]}/', f'{t["h1"]} | Cozy Paws', t['desc'], body, today, image=f'/img/pin/t-{t["id"]}.jpg', jsonld=ld)
        urls.append((f'/tools/{t["id"]}/', t['live']))

    # privacidad y 404
    page('/privacy/', 'Privacy Policy | Cozy Paws', 'How Cozy Paws uses cookies and data.', f"""<h1>Privacy policy</h1>
<p>This website is run by {CONFIG['company']} (Cozy Paws brand). We do not sell products on this site: purchases happen on Etsy, under Etsy's own privacy policy.</p>
<p><b>Cookies and stats.</b> Only if you click OK in the cookie notice, we load Google Analytics (anonymous visit statistics) and the Meta Pixel (to measure ads and visits). If you click "No thanks", nothing is loaded. You can change your choice by clearing this site's data in your browser.</p>
<p><b>Calculators.</b> The pet tools run in your browser. We do not store what you type.</p>
<p><b>Contact.</b> <a href="mailto:{CONFIG['contact']}">{CONFIG['contact']}</a></p><p class="note">Last updated: November 14, 2026.</p>""", today)
    page('/404.html', 'Page not found | Cozy Paws', 'Page not found.', '<h1>Oops, this page ran off to chase a squirrel</h1><p><a href="/">Go to the home page</a> or <a href="/gifts/">see the gift guides</a>.</p>', today, canonical=False)

    # sitemap, robots, feed
    sm = ''.join(f'<url><loc>{CONFIG["url"]}{u}</loc><lastmod>{d.isoformat()}</lastmod></url>' for u, d in urls)
    open(os.path.join(OUT, 'sitemap.xml'), 'w').write(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{sm}</urlset>')
    open(os.path.join(OUT, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\nSitemap: {CONFIG["url"]}/sitemap.xml\n')
    open(os.path.join(OUT, '_headers'), 'w').write('/img/*\n  Cache-Control: public, max-age=604800\n')

    items = []
    for p in prods:
        items.append((p['live'], f'{p["short"]}', f'/p/{p["slug"]}/', f'/img/pin/{p["sku"]}.jpg',
                      f'{p["texto"]} {p["kind"]} from ${p["precio"]}. Shop Cozy Paws on Etsy.', p['sku']))
    for g, ps in guides_live:
        items.append((g['live'], f'{g["h1"]}: {len(ps)} gift ideas', f'/gifts/{g["id"]}/', f'/img/pin/g-{g["id"]}.jpg', g['intro'][:300], 'g-' + g['id']))
    for t in tools_live:
        items.append((t['live'], t['h1'], f'/tools/{t["id"]}/', f'/img/pin/t-{t["id"]}.jpg', t['desc'], 't-' + t['id']))
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
