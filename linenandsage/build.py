#!/usr/bin/env python3
"""Linen & Sage mini website: one page per product + RSS feed so Pinterest auto-publishes every product.

Run:   python3 linenandsage/build.py   -> writes linenandsage/site/ (MAKE_ZIP=1 also writes a zip for manual upload)
Source of truth: fuente/ (Payhip texts and images, copied from the project's kdp-linen-sage/).
To add a product link: add a line "<folder id> <payhip link>" to linenandsage/payhip-links.md and push.
The GitHub workflow linenandsage.yml rebuilds site/ and commits it; Cloudflare Pages (project connected
to this repo, output folder linenandsage/site) publishes it; Pinterest reads feed.xml and pins on its own.
"""
import html, json, os, re, shutil, zipfile, datetime
from email.utils import format_datetime

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'fuente')
OUT = os.path.join(HERE, 'site')
CONFIG = dict(
    name='Linen & Sage', url='https://linenandsage.pages.dev', store='https://payhip.com/LinenAndSage',
    ga4='', pixel='',            # paste the GA4 Measurement ID and Meta Pixel ID when they exist
    pinterest='https://www.pinterest.com/linenandsageprints/', contact='support@skyesolutionsai.com', company='Skye Solutions AI',
    pinterest_verify='f47f5db8d0594f46be0ed346e8db3e61',         # Pinterest "claim website" meta tag content, if Pinterest asks for one
)
PAYHIP = {}   # filled from payhip-links.md ("<folder id> <payhip link>" per line)
_pl = os.path.join(HERE, 'payhip-links.md')
if os.path.exists(_pl):
    for _l in open(_pl, encoding='utf-8'):
        _m = re.match(r'\s*([a-z0-9-]+)\s+(https://payhip\.com/\S+)', _l)
        if _m:
            PAYHIP[_m.group(1)] = _m.group(2)
KDP = {}      # e.g. "little-moments-en": "https://www.amazon.com/dp/XXXXXXXXXX?tag=cruxreport-20"
FOLDERS = {
    'imprimibles/payhip-y-pinterest.md': ['agenda-2027-es', 'pequenos-momentos-es', 'little-moments-en', 'brain-dump-daily-en', 'questions-for-me-en', 'caregiver-journal-en'],
    'digitales/payhip-digitales.md': ['agenda-digital-2027-en', 'agenda-digital-2027-es', 'botanical-calm', 'gentle-words-en', 'palabras-amables-es',
                                      'notion-budget-en', 'notion-budget-es', 'notion-meal-en', 'notion-meal-es', 'canva-kit-en', 'canva-kit-es'],
}
E = html.escape
TODAY = datetime.date.today().isoformat()


def parse_products():
    out = []
    for md, folders in FOLDERS.items():
        text = open(os.path.join(SRC, md), encoding='utf-8').read()
        secs = re.split(r'\n### (\d+)\. ', text)[1:]
        for num, body in zip(secs[0::2], secs[1::2]):
            i = int(num) - 1
            if i >= len(folders):
                continue
            head = body.split('\n', 1)[0]
            price = re.search(r'·\s*([\d,]+)\s*USD', head).group(1).replace(',', '.')
            title = re.search(r'^- (?:Título|Title): (.+)$', body, re.M).group(1).strip()
            desc_block = re.split(r'^- (?:Descripción|Description):\s*$', body, flags=re.M)[1]
            lines = []
            for l in desc_block.split('\n')[1:]:
                if l.startswith('- ') or l.startswith('#') or (l and not l.startswith('  ')):
                    break
                lines.append(l.strip())
            desc = [l for l in lines if l]
            sub = os.path.dirname(md)
            lang = 'es' if folders[i].endswith('-es') or re.search(r'español', head) else 'en'
            out.append(dict(id=folders[i], dir=os.path.join(SRC, sub, folders[i]), title=title, name=re.sub(r'\s*\((inglés|español)\)', '', head.split('·')[0]).strip(),
                            price=price, desc=desc, lang=lang, kind='Printable' if sub == 'imprimibles' else 'Digital'))
    return out


def parse_favorites():
    text = open(os.path.join(SRC, 'imprimibles/payhip-y-pinterest.md'), encoding='utf-8').read()
    part = text.split('### Lista de pines', 1)[1]
    favs = []
    for m in re.finditer(r'\d+\. `([^`]+)` · Tablero: \*\*([^*]+)\*\*\n\s+- Título: (.+)\n\s+- Descripción: (.+)\n\s+- Link: (\S+)', part):
        img, board, title, desc, link = m.groups()
        desc = desc.replace(' #ad As an Amazon Associate I earn from qualifying purchases.', '').strip()
        favs.append(dict(id=img.rsplit('.', 1)[0], img=img, board=board, title=title.strip(), desc=desc, link=link))
    return favs


CSS = """*{box-sizing:border-box}body{margin:0;font-family:Georgia,'Times New Roman',serif;background:#f6f3ee;color:#2f3b33;line-height:1.6}
a{color:#4f6b55}header,footer{padding:18px 24px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px}
header .logo{font-size:26px;text-decoration:none;color:#2f3b33;letter-spacing:.5px}nav a{margin-left:16px;font-family:system-ui,sans-serif;font-size:15px}
main{max-width:1080px;margin:0 auto;padding:12px 24px 40px}h1{font-weight:normal;font-size:40px;line-height:1.15;margin:18px 0 10px}h2{font-weight:normal;font-size:28px;margin:34px 0 12px}
.lead{font-size:19px;color:#56645a;max-width:720px}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:20px}
.card{background:#fff;border-radius:14px;overflow:hidden;text-decoration:none;color:inherit;box-shadow:0 1px 3px rgba(0,0,0,.06)}.card img{width:100%;aspect-ratio:3/2;object-fit:cover;display:block}
.card div{padding:12px 14px;font-family:system-ui,sans-serif;font-size:15px}.card b{display:block;font-family:Georgia,serif;font-size:17px;font-weight:normal;margin-bottom:4px}
.prod{display:grid;grid-template-columns:1.1fr 1fr;gap:32px;align-items:start}.prod img{width:100%;border-radius:14px;margin-bottom:12px}
@media(max-width:760px){.prod{grid-template-columns:1fr}h1{font-size:32px}}
.btn{display:inline-block;background:#4f6b55;color:#fff;padding:13px 22px;border-radius:30px;text-decoration:none;font-family:system-ui,sans-serif;font-weight:600}
.small{font-size:14px;color:#6b776e;font-family:system-ui,sans-serif}.tag{font-family:system-ui,sans-serif;font-size:13px;background:#e4ebe2;padding:3px 10px;border-radius:20px}
footer{border-top:1px solid #e2ddd3;font-family:system-ui,sans-serif;font-size:14px;color:#6b776e}
#ck{position:fixed;left:16px;right:16px;bottom:16px;max-width:520px;background:#fff;padding:16px;border-radius:12px;box-shadow:0 4px 20px rgba(0,0,0,.15);font-family:system-ui,sans-serif;font-size:14px}
#ck button{margin:8px 8px 0 0;padding:8px 14px;border-radius:20px;border:1px solid #4f6b55;background:#fff;cursor:pointer}#ck .y{background:#4f6b55;color:#fff}"""

TRACK = """<script>(function(){var C=%s;function load(){if(C.ga4){var s=document.createElement('script');s.async=1;s.src='https://www.googletagmanager.com/gtag/js?id='+C.ga4;document.head.appendChild(s);
window.dataLayer=window.dataLayer||[];window.gtag=function(){dataLayer.push(arguments)};gtag('js',new Date());gtag('config',C.ga4);}
if(C.pixel){!function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}(window,document,'script','https://connect.facebook.net/en_US/fbevents.js');fbq('init',C.pixel);fbq('track','PageView');}}
var c=localStorage.getItem('ls_consent');if(c==='yes')load();
document.addEventListener('DOMContentLoaded',function(){var b=document.getElementById('ck');if(!c&&b)b.hidden=false;
b&&b.addEventListener('click',function(e){if(e.target.tagName!=='BUTTON')return;var y=e.target.className==='y';localStorage.setItem('ls_consent',y?'yes':'no');b.hidden=true;if(y)load();});
var r=document.getElementById('rc');r&&r.addEventListener('click',function(e){e.preventDefault();localStorage.removeItem('ls_consent');location.reload();});});})();</script>"""


def page(title, desc, path, body, img=None, ld=None, lang='en'):
    url = CONFIG['url'] + path
    img = img or CONFIG['url'] + '/og-image.jpg'
    pv = '<meta name="p:domain_verify" content="%s">' % CONFIG['pinterest_verify'] if CONFIG['pinterest_verify'] else ''
    lds = ''.join('<script type="application/ld+json">%s</script>' % json.dumps(x, ensure_ascii=False) for x in (ld or []))
    return f"""<!DOCTYPE html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)}</title><meta name="description" content="{E(desc)}"><link rel="canonical" href="{url}">
<meta property="og:type" content="website"><meta property="og:site_name" content="{CONFIG['name']}"><meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{img}"><meta name="twitter:card" content="summary_large_image">
<link rel="alternate" type="application/rss+xml" title="{CONFIG['name']}" href="/feed.xml">{pv}<style>{CSS}</style>{TRACK % json.dumps({'ga4': CONFIG['ga4'], 'pixel': CONFIG['pixel']})}{lds}</head><body>
<header><a class="logo" href="/">Linen &amp; Sage</a><nav><a href="/#printables">Printables</a><a href="/#digital">Digital</a><a href="/favorites/">Favorites</a></nav></header>
<main>{body}</main>
<footer><span>© {datetime.date.today().year} {CONFIG['name']} · {CONFIG['company']}</span><span><a href="/privacy/">Privacy &amp; cookies</a> · <a href="#" id="rc">Cookie settings</a> · <a href="{CONFIG['pinterest']}">Pinterest</a> · <a href="/feed.xml">RSS</a> · <a href="mailto:{CONFIG['contact']}">Contact</a></span></footer>
<div id="ck" hidden>We use cookies for statistics (Google Analytics) and to measure visits from ads (Meta Pixel), only if you accept. <a href="/privacy/">Privacy</a><br><button class="y">Accept</button><button class="n">Only necessary</button></div>
</body></html>
"""


def write(path, s):
    f = os.path.join(OUT, path.strip('/'), 'index.html') if path.endswith('/') else os.path.join(OUT, path.lstrip('/'))
    os.makedirs(os.path.dirname(f), exist_ok=True)
    open(f, 'w', encoding='utf-8').write(s)


def img_copy(src, dst, width):
    from PIL import Image
    im = Image.open(src).convert('RGB')
    if im.width > width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    im.save(dst, quality=85, optimize=True)


def main():
    shutil.rmtree(OUT, ignore_errors=True)
    prods, favs = parse_products(), parse_favorites()
    # Only products already for sale on Payhip go on the site (and into the Pinterest feed).
    prods = [p for p in prods if p['id'] in PAYHIP]
    items = []   # feed entries
    for p in prods:
        imgs = sorted(f for f in os.listdir(os.path.join(p['dir'], 'imagenes')) if f.endswith('.jpg'))
        for f in imgs:
            img_copy(os.path.join(p['dir'], 'imagenes', f), os.path.join(OUT, 'img', p['id'], f), 1000)
        img_copy(os.path.join(p['dir'], 'pinterest', 'pin-1.jpg'), os.path.join(OUT, 'pins', p['id'] + '.jpg'), 1000)
        p['img'] = f"/img/{p['id']}/{imgs[0]}"
        buy = PAYHIP.get(p['id'], CONFIG['store'])
        es = p['lang'] == 'es'
        amz = KDP.get(p['id'])
        desc_html = ''.join(('<p>%s</p>' % E(l)) if not re.match(r'^\d+\.', l) else '<li>%s</li>' % E(re.sub(r'^\d+\.\s*', '', l)) for l in p['desc'])
        desc_html = re.sub(r'((?:<li>.*?</li>)+)', r'<ol>\1</ol>', desc_html)
        meta = ' '.join(p['desc'][:2])[:155]
        path = f"/p/{p['id']}/"
        ld = [{'@context': 'https://schema.org', '@type': 'Product', 'name': p['title'], 'image': [CONFIG['url'] + p['img']], 'description': meta,
               'brand': {'@type': 'Brand', 'name': CONFIG['name']},
               'offers': {'@type': 'Offer', 'price': p['price'], 'priceCurrency': 'USD', 'availability': 'https://schema.org/InStock', 'url': buy}}]
        body = (f'<div class="prod"><div>' + ''.join(f'<img src="/img/{p["id"]}/{f}" alt="{E(p["name"])}" loading="lazy">' for f in imgs) +
                f'</div><div><span class="tag">{"Imprimible" if es and p["kind"] == "Printable" else p["kind"]}</span><h1>{E(p["name"])}</h1>'
                f'<p class="lead">${p["price"]} · {"Descarga digital" if es else "Instant digital download"}</p>'
                f'<p><a class="btn" href="{buy}" rel="noopener">{"Comprar en Payhip" if es else "Get it on Payhip"} →</a></p>'
                + (f'<p><a href="{amz}" rel="sponsored noopener">{"También en tapa blanda en Amazon" if es else "Also as a paperback on Amazon"} →</a></p>' if amz else '') +
                f'{desc_html}</div></div>')
        write(path, page(f"{p['title']} | {CONFIG['name']}", meta, path, body, CONFIG['url'] + f"/pins/{p['id']}.jpg", ld, p['lang']))
        items.append((p['title'], meta, path, f"/pins/{p['id']}.jpg"))
    # favorites (Amazon affiliate)
    fav_cards = ''
    for f in favs:
        img_copy(os.path.join(SRC, 'imprimibles', 'pines-afiliados-amazon', f['img']), os.path.join(OUT, 'pins', 'fav-' + f['id'] + '.jpg'), 1000)
        path = f"/favorites/{f['id']}/"
        body = (f'<div class="prod"><div><img src="/pins/fav-{f["id"]}.jpg" alt="{E(f["title"])}"></div><div><span class="tag">{E(f["board"])}</span>'
                f'<h1>{E(f["title"].split(" | ")[-1])}</h1><p class="lead">{E(f["desc"])}</p>'
                f'<p><a class="btn" href="{f["link"]}" rel="sponsored noopener">See it on Amazon →</a></p>'
                f'<p class="small">As an Amazon Associate we earn from qualifying purchases, at no extra cost to you.</p>'
                f'<p><a href="/favorites/">← All journaling favorites</a></p></div></div>')
        write(path, page(f"{f['title']} | {CONFIG['name']}", f['desc'][:155], path, body, CONFIG['url'] + f"/pins/fav-{f['id']}.jpg"))
        items.append((f['title'], f['desc'][:155], path, f"/pins/fav-{f['id']}.jpg"))
        fav_cards += f'<a class="card" href="{path}"><img src="/pins/fav-{f["id"]}.jpg" alt="" loading="lazy" style="aspect-ratio:2/3"><div><b>{E(f["title"].split(" | ")[-1])}</b>{E(f["board"])}</div></a>'
    write('/favorites/', page(f"Journaling supplies we love | {CONFIG['name']}", 'Pens, notebooks and cozy things for a calm journaling and planning routine.', '/favorites/',
                              '<h1>Journaling favorites</h1><p class="lead">Pens, notebooks and cozy things for a calm journaling routine.</p>'
                              '<p class="small">Affiliate links: as an Amazon Associate we earn from qualifying purchases.</p>'
                              f'<div class="grid">{fav_cards}</div>'))
    card = lambda p: f'<a class="card" href="/p/{p["id"]}/"><img src="{p["img"]}" alt="" loading="lazy"><div><b>{E(p["name"])}</b>${p["price"]}</div></a>'
    home = ('<h1>Calm, simple journals and planners</h1><p class="lead">Printable journals, digital planners and templates in English and Spanish, '
            'made to take five quiet minutes a day.</p>'
            f'<h2 id="printables">Printable journals</h2><div class="grid">{"".join(card(p) for p in prods if p["kind"] == "Printable")}</div>'
            f'<h2 id="digital">Digital planners &amp; templates</h2><div class="grid">{"".join(card(p) for p in prods if p["kind"] == "Digital")}</div>'
            '<h2>Journaling favorites</h2><p><a href="/favorites/">Pens, notebooks and cozy things we love →</a></p>')
    write('/', page(f"{CONFIG['name']}: printable journals and digital planners", 'Printable gratitude journals, ADHD planners, digital planners and Notion and Canva templates in English and Spanish.', '/', home,
                    ld=[{'@context': 'https://schema.org', '@type': 'WebSite', 'name': CONFIG['name'], 'url': CONFIG['url'] + '/'}]))
    write('/privacy/', page(f"Privacy & cookies | {CONFIG['name']}", 'How Linen & Sage uses cookies and affiliate links.', '/privacy/',
        f'<h1>Privacy &amp; cookies</h1><p>{CONFIG["name"]} is run by {CONFIG["company"]} (Utah, USA). Contact: <a href="mailto:{CONFIG["contact"]}">{CONFIG["contact"]}</a>.</p>'
        '<p>We do not ask for your name or email on this site. If you accept cookies, Google Analytics (visit statistics) and Meta Pixel (measuring visits from ads) load and collect usage data such as pages viewed, device and approximate location. If you choose "Only necessary", neither loads. Change your choice with "Cookie settings" at the bottom of every page.</p>'
        '<p>Purchases happen on Payhip or Amazon, under their own privacy policies. Some links are affiliate links: as an Amazon Associate we earn from qualifying purchases.</p>'
        '<p>Depending on where you live you may ask to access or delete your data, or opt out of sale or sharing: write to us. We do not sell personal information.</p>'))
    # share image
    shutil.copy(os.path.join(OUT, 'pins', prods[min(2, len(prods) - 1)]['id'] + '.jpg'), os.path.join(OUT, 'og-image.jpg'))
    # feed (keeps first-seen dates so Pinterest only pins new items)
    feed = os.path.join(HERE, 'feed-dates.json')
    seen = json.load(open(feed)) if os.path.exists(feed) else {}
    now = format_datetime(datetime.datetime.now(datetime.timezone.utc))
    for _, _, path, _ in items:
        seen.setdefault(path, now)
    json.dump(seen, open(feed, 'w'), indent=1)
    rss = ''.join(f"<item><title>{E(t)}</title><link>{CONFIG['url']}{p}</link><guid>{CONFIG['url']}{p}</guid><pubDate>{seen[p]}</pubDate>"
                  f"<description>{E(d)}</description><enclosure url=\"{CONFIG['url']}{im}\" type=\"image/jpeg\" length=\"0\"/>"
                  f"<media:content url=\"{CONFIG['url']}{im}\" medium=\"image\"/></item>" for t, d, p, im in items)
    write('/feed.xml', f'<?xml version="1.0" encoding="UTF-8"?><rss version="2.0" xmlns:media="http://search.yahoo.com/mrss/"><channel><title>{E(CONFIG["name"])}</title>'
                       f'<link>{CONFIG["url"]}/</link><description>Printable journals, digital planners and journaling favorites.</description>{rss}</channel></rss>\n')
    urls = ['/', '/favorites/'] + [p for _, _, p, _ in items]
    write('/sitemap.xml', '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' +
          ''.join(f'<url><loc>{CONFIG["url"]}{u}</loc><lastmod>{TODAY}</lastmod></url>' for u in urls) + '</urlset>\n')
    write('/robots.txt', f'User-agent: *\nAllow: /\nSitemap: {CONFIG["url"]}/sitemap.xml\n')
    write('/404.html', page('Not found', 'Page not found', '/404', '<h1>Page not found</h1><p><a href="/">Back to Linen &amp; Sage</a></p>'))
    if not os.environ.get('MAKE_ZIP'):
        print(f'{len(prods)} products, {len(favs)} favorites, {len(urls)} URLs ->', OUT)
        return
    z = os.path.join(HERE, 'linen-and-sage-sitio-para-subir.zip')
    with zipfile.ZipFile(z, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, _, files in os.walk(OUT):
            for f in files:
                full = os.path.join(root, f); zf.write(full, os.path.relpath(full, OUT))
    print(f'{len(prods)} products, {len(favs)} favorites, {len(urls)} URLs ->', OUT)


if __name__ == '__main__':
    main()
