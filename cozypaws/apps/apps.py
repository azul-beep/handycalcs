"""Apps web instalables (PWA) de Cozy Paws. Las arma build.py en cada publicación.

App 1: Paw Party (/fun/ en inglés, /fun/es/ en español): edad en años humanos, nombres, test de
personalidad, horóscopo y tarjetas con estampas de Cozy Paws. Todo corre en el navegador; lo que
guarda la persona queda en su equipo (localStorage "cozypaws-pets", compartido con la futura app del diario).

Archivos: fun.html (plantilla, textos de la app en EN/ES adentro), ../data/apps/ (estampas e íconos, los arma
make_assets.py). Anuncios: CONFIG['adsense_on'] en build.py (apagado hasta que AdSense apruebe el sitio).
"""
import hashlib, html, json, os, shutil
from urllib.parse import quote_plus

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, '..', 'data', 'apps')
E = html.escape

# estampa -> (skus de Etsy que la usan, búsqueda en la tienda si todavía no hay link directo)
STAMP_SHOP = {
    'dog-mom': (['a01', 'p01'], 'dog mom'), 'dog-dad': (['a02', 'a13'], 'dog dad'), 'cat-mom': (['a03', 'p02', 'p09'], 'cat mom'),
    'cat-dad': (['a04', 'p10', 'a12'], 'cat dad'), 'golden': (['p03', 'a05', 'a08'], 'golden retriever'), 'frenchie': (['p05', 'a06'], 'frenchie'),
    'doodle': (['p08', 'a07'], 'doodle'), 'labrador': (['p04'], 'labrador'), 'german-shepherd': (['p06'], 'german shepherd'),
    'dachshund': (['p07'], 'dachshund'), 'cozy-pup': (['w08'], 'cozy pup'), 'dog-mom-club': (['w06'], 'dog mom club'),
    'cat-mom-club': (['w07'], 'cat mom club'), 'comfy': (['a09'], 'my dog was comfy'), 'woofmas': (['p11'], 'woofmas'),
    'meowy': (['a10'], 'meowy christmas'), 'good-boy': (['p13'], 'good boy'),
}

SEO = {
    'en': dict(
        title='Paw Party: Free Fun App for Dogs and Cats (Human Years, Names, Quiz, Cards)',
        desc='Free pet app: dog and cat age in human years, a pet name generator, a personality quiz, pet zodiac and birthday cards with cute stamps. Use it on the web or install it on your phone.',
        h1='Paw Party: a free fun app for dogs and cats',
        intro='Paw Party is a free app for pet people. Find out your dog or cat\'s age in human years, get name ideas, take the personality quiz, read their zodiac sign and make a birthday or gotcha day card to share. No sign up and nothing to download: it works right here in your browser, and you can install it on your phone in one tap.',
        feats=[('Human years calculator', 'Dog age by size (small, medium, large, giant) and cat age, with life stage and the DNA-based formula from UC San Diego.'),
               ('Pet name generator', 'Hundreds of dog and cat names by style: cute, classic, foodie, tough, funny, Christmas, Spanish, nature and legends. Filter by first letter and save favorites.'),
               ('Pet personality quiz', 'Eight quick questions to find out if your pet is a Couch Potato, an Explorer, a Class Clown, a Velcro Buddy, a Diva or a Little Genius.'),
               ('Pet zodiac', 'Enter the birthday or adoption day to see your pet\'s star sign and what it says about them.'),
               ('Card maker', 'Birthday, gotcha day, Christmas and best friend cards with original Cozy Paws stamps and your pet\'s photo. Download or share in one tap.')],
        faq=[('Is Paw Party free?', 'Yes. Every tool is free, with no sign up and no in-app purchases.'),
             ('How do I install the app on my phone?', 'On Android, tap "Install app" at the top (Chrome). On iPhone, open this page in Safari, tap Share and then "Add to Home Screen". It opens like a normal app and works offline.'),
             ('Where are my pet\'s name and photo saved?', 'Only on your device, in your browser. We do not upload them. If you clear your browser data, they are deleted.'),
             ('How do you calculate dog years?', 'We use the vet chart by size: the first year equals about 15 human years, the second about 9 more, and after that 4 to 7 years each depending on size. Cats add about 4 years per year after age 2.'),
             ('Can I print the cards?', 'Yes. Download the card as a PNG image (1080 x 1350) and print it at home or share it on Instagram, WhatsApp or Facebook.')],
        other_label='Español', in_lang='en-US'),
    'es': dict(
        title='Paw Party: app gratis para perros y gatos (edad humana, nombres, test y tarjetas)',
        desc='App gratis para mascotas: edad de tu perro o gato en años humanos, generador de nombres, test de personalidad, horóscopo y tarjetas de cumpleaños con estampas. Úsala en la web o instálala en tu celular.',
        h1='Paw Party: app gratis y divertida para perros y gatos',
        intro='Paw Party es una app gratis para los que aman a sus mascotas. Calcula la edad de tu perro o gato en años humanos, busca ideas de nombres, haz el test de personalidad, mira su horóscopo y crea una tarjeta de cumpleaños o de adopción para compartir. Sin registrarte y sin descargar nada: funciona aquí en el navegador, y la puedes instalar en tu celular con un toque.',
        feats=[('Calculadora de años humanos', 'Edad del perro por tamaño (chico, mediano, grande, gigante) y del gato, con su etapa de vida y la fórmula del ADN de UC San Diego.'),
               ('Generador de nombres', 'Cientos de nombres para perros y gatos por estilo: tiernos, clásicos, de comida, fuertes, graciosos, navideños, en español, de la naturaleza y leyendas. Filtra por letra y guarda tus favoritos.'),
               ('Test de personalidad', 'Ocho preguntas rápidas para saber si tu mascota es el rey del sillón, el explorador, el payasito, el inseparable, la diva o el pequeño genio.'),
               ('Horóscopo de mascotas', 'Pon el cumpleaños o el día de adopción y mira su signo y lo que dice de su forma de ser.'),
               ('Tarjetas', 'Tarjetas de cumpleaños, de adopción, de Navidad y de mejor amigo con estampas originales de Cozy Paws y la foto de tu mascota. Descárgalas o compártelas con un toque.')],
        faq=[('¿Paw Party es gratis?', 'Sí. Todas las herramientas son gratis, sin registrarte y sin compras dentro de la app.'),
             ('¿Cómo instalo la app en el celular?', 'En Android, toca "Instalar app" arriba (Chrome). En iPhone, abre esta página en Safari, toca Compartir y después "Agregar a inicio". Se abre como una app normal y funciona sin internet.'),
             ('¿Dónde se guardan el nombre y la foto de mi mascota?', 'Solo en tu equipo, en tu navegador. No los subimos a ningún lado. Si borras los datos del navegador, se borran.'),
             ('¿Cómo se calculan los años de perro?', 'Usamos la tabla veterinaria por tamaño: el primer año equivale a unos 15 años humanos, el segundo suma unos 9, y después cada año suma de 4 a 7 según el tamaño. En gatos, después de los 2 años cada año suma unos 4.'),
             ('¿Puedo imprimir las tarjetas?', 'Sí. Descarga la tarjeta como imagen PNG (1080 x 1350) e imprímela en casa, o compártela en Instagram, WhatsApp o Facebook.')],
        other_label='English', in_lang='es-US'),
}


def stamp_links(config, all_prods, today):
    by = {p['sku']: p for p in all_prods}
    out = []
    for sid, (skus, q) in STAMP_SHOP.items():
        url = None
        for s in skus:  # primer producto ya publicado en Etsy con esa estampa
            p = by.get(s)
            if p and p['live'] <= today and '/listing/' in p['etsy']:
                url = p['etsy']; break
        out.append({'id': sid, 'url': url or f"{config['shop']}?search_query={quote_plus(q)}"})
    return out


def analytics_js(config):
    """Solo define wwLoad(); el aviso de cookies lo maneja la app (misma clave ww_cc que el resto del sitio)."""
    ga, ads = config.get('ga4'), config.get('adsense') if config.get('adsense_on') else ''
    js = 'function wwLoad(){'
    if ga:
        js += (f"var s=document.createElement('script');s.async=1;s.src='https://www.googletagmanager.com/gtag/js?id={ga}';document.head.appendChild(s);"
               f"window.dataLayer=window.dataLayer||[];window.gtag=function(){{dataLayer.push(arguments)}};gtag('js',new Date());gtag('config','{ga}');")
    if ads:
        js += (f"var a=document.createElement('script');a.async=1;a.crossOrigin='anonymous';a.src='https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ads}';"
               "a.onload=function(){document.querySelectorAll('ins.adsbygoogle').forEach(function(){try{(window.adsbygoogle=window.adsbygoogle||[]).push({})}catch(e){}})};document.head.appendChild(a);")
    return f'<script>{js}}}</script>'


def manifest(config, lang):
    es = lang == 'es'
    return {
        'id': '/fun/' + ('es/' if es else ''), 'name': 'Paw Party by Cozy Paws', 'short_name': 'Paw Party',
        'description': SEO[lang]['desc'], 'lang': 'es' if es else 'en',
        'start_url': '/fun/' + ('es/' if es else '') + '?source=pwa', 'scope': '/fun/', 'display': 'standalone',
        'background_color': '#F3E9D7', 'theme_color': '#4E7F86', 'orientation': 'portrait',
        'categories': ['entertainment', 'lifestyle'],
        'icons': [{'src': '/fun/icons/icon-192.png', 'sizes': '192x192', 'type': 'image/png'},
                  {'src': '/fun/icons/icon-512.png', 'sizes': '512x512', 'type': 'image/png'},
                  {'src': '/fun/icons/icon-maskable-512.png', 'sizes': '512x512', 'type': 'image/png', 'purpose': 'maskable'}],
        'shortcuts': [{'name': 'Cards' if not es else 'Tarjetas', 'url': '/fun/' + ('es/' if es else '') + '#card'},
                      {'name': 'Human years' if not es else 'Años humanos', 'url': '/fun/' + ('es/' if es else '') + '#age'}],
    }


def build_fun(out, config, all_prods, today):
    """Escribe /fun/ y /fun/es/. Devuelve [(ruta, fecha)] para el sitemap."""
    d = os.path.join(out, 'fun')
    for sub in ('icons', 'stamps', 'es'):
        os.makedirs(os.path.join(d, sub), exist_ok=True)
    for f in os.listdir(ASSETS):
        if f.endswith('.png'):
            shutil.copy(os.path.join(ASSETS, f), os.path.join(d, 'icons', f))
    for f in os.listdir(os.path.join(ASSETS, 'stamps')):
        shutil.copy(os.path.join(ASSETS, 'stamps', f), os.path.join(d, 'stamps', f))
    tpl = open(os.path.join(HERE, 'fun.html'), encoding='utf-8').read()
    url = config['url']
    stamps = stamp_links(config, all_prods, today)
    host = url.split('//')[1]
    pages = {}
    for lang in ('en', 'es'):
        s = SEO[lang]
        path = '/fun/' + ('es/' if lang == 'es' else '')
        other = '/fun/es/' if lang == 'en' else '/fun/'
        ld = [{'@context': 'https://schema.org', '@type': 'WebApplication', 'name': 'Paw Party', 'url': url + path, 'inLanguage': s['in_lang'],
               'applicationCategory': 'EntertainmentApplication', 'operatingSystem': 'Any (web, Android, iPhone)', 'description': s['desc'],
               'offers': {'@type': 'Offer', 'price': '0', 'priceCurrency': 'USD'}, 'image': url + '/fun/icons/icon-512.png',
               'publisher': {'@type': 'Organization', 'name': 'Cozy Paws', 'url': url}},
              {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
                  {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in s['faq']]}]
        head = (f'<title>{E(s["title"])}</title><meta name="description" content="{E(s["desc"])}">'
                f'<link rel="canonical" href="{url}{path}"><link rel="alternate" hreflang="en" href="{url}/fun/">'
                f'<link rel="alternate" hreflang="es" href="{url}/fun/es/"><link rel="alternate" hreflang="x-default" href="{url}/fun/">'
                f'<link rel="manifest" href="{path}manifest.webmanifest">'
                f'<meta property="og:title" content="{E(s["title"])}"><meta property="og:description" content="{E(s["desc"])}">'
                f'<meta property="og:image" content="{url}/img/pin/app-fun.jpg"><meta property="og:url" content="{url}{path}"><meta property="og:type" content="website">'
                f'<meta name="twitter:card" content="summary_large_image">'
                + (f'<meta name="google-site-verification" content="{E(config["google_verify"])}">' if config.get('google_verify') else '')
                + (f'<meta name="p:domain_verify" content="{E(config["pinterest_verify"])}">' if config.get('pinterest_verify') else '')
                + ''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ld))
        feats = ''.join(f'<li><b>{E(a)}.</b> {E(b)}</li>' for a, b in s['feats'])
        faq = ''.join(f'<details><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q, a in s['faq'])
        more = ('More free tools' if lang == 'en' else 'Más herramientas gratis')
        seo = (f'<section class="seo"><h1>{E(s["h1"])}</h1><p>{E(s["intro"])}</p><h2>{"What you can do" if lang == "en" else "Qué puedes hacer"}</h2><ul>{feats}</ul>'
               f'<h2>{"Questions" if lang == "en" else "Preguntas frecuentes"}</h2>{faq}'
               f'<p>{more}: <a href="/tools/">{"Pet tools" if lang == "en" else "Calculadoras (en inglés)"}</a> · <a href="/gifts/">{"Gift guides" if lang == "en" else "Guías de regalos (en inglés)"}</a> · '
               f'<a href="{config["shop"]}" data-etsy="fun-seo" rel="noopener">Cozy Paws Etsy shop</a></p></section>')
        cfg = {'lang': lang, 'stamps': stamps, 'host': host, 'company': config['company'],
               'ads': config['adsense'] if config.get('adsense_on') else ''}
        doc = (tpl.replace('__LANG__', lang).replace('<!--HEAD-->', head).replace('<!--SEO-->', seo)
               .replace('<!--ANALYTICS-->', analytics_js(config)).replace('/*CFG*/', 'var CFG=' + json.dumps(cfg, ensure_ascii=False) + ';')
               .replace('__OTHER_URL__', other).replace('__OTHER_LABEL__', s['other_label']))
        pages[lang] = doc
        open(os.path.join(out, path.strip('/'), 'index.html'), 'w', encoding='utf-8').write(doc)
        open(os.path.join(out, path.strip('/'), 'manifest.webmanifest'), 'w', encoding='utf-8').write(json.dumps(manifest(config, lang), ensure_ascii=False, indent=1))

    # service worker: la versión cambia solo si cambia el código de la app o las imágenes (no todos los días)
    h = hashlib.sha1(tpl.encode())
    for f in sorted(os.listdir(os.path.join(ASSETS, 'stamps'))):
        h.update(f.encode())
    ver = h.hexdigest()[:10]
    pre = ['/fun/', '/fun/es/', '/fun/manifest.webmanifest', '/fun/es/manifest.webmanifest', '/img/logo-160.png', '/img/logo-ilustrado.png', '/img/icon.png',
           '/fonts/Yesteryear-Regular.woff2', '/fonts/AbrilFatface-Regular.woff2', '/fonts/Lora.woff2',
           '/fun/icons/icon-192.png', '/fun/icons/icon-512.png'] + [f'/fun/stamps/{x["id"]}.png' for x in stamps]
    sw = f"""// Paw Party (Cozy Paws): funciona sin internet. Versión {ver} (cambia sola cuando cambia la app).
const C='pawparty-{ver}',PRE={json.dumps(pre)};
self.addEventListener('install',e=>{{e.waitUntil(caches.open(C).then(c=>c.addAll(PRE)).then(()=>self.skipWaiting()))}});
self.addEventListener('activate',e=>{{e.waitUntil(caches.keys().then(k=>Promise.all(k.filter(x=>x.startsWith('pawparty-')&&x!==C).map(x=>caches.delete(x)))).then(()=>self.clients.claim()))}});
self.addEventListener('fetch',e=>{{const r=e.request,u=new URL(r.url);if(r.method!=='GET'||u.origin!==location.origin)return;
 if(r.mode==='navigate'){{e.respondWith(fetch(r).then(x=>{{const y=x.clone();caches.open(C).then(c=>c.put(u.pathname,y));return x}}).catch(()=>caches.match(u.pathname).then(m=>m||caches.match('/fun/'))));return}}
 e.respondWith(caches.match(r).then(m=>{{const f=fetch(r).then(x=>{{if(x.ok){{const y=x.clone();caches.open(C).then(c=>c.put(r,y))}}return x}}).catch(()=>m);return m||f}}));}});
"""
    open(os.path.join(d, 'sw.js'), 'w', encoding='utf-8').write(sw)
    return [('/fun/', today), ('/fun/es/', today)]
