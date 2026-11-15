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


DIARY_SEO = {
    'en': dict(
        title='Paw Diary: Free Pet Diary, Vet Reminders and Weight Tracker App for Dogs and Cats',
        desc='Free app for dog and cat owners: log walks, meals and meds, get vaccine and flea pill reminders, track weight with a chart and see how much to feed. Works offline, no sign up.',
        h1='Paw Diary: a free pet diary and reminder app',
        intro='Paw Diary keeps your dog or cat\'s daily life and health in one place. Log walks, meals, meds and moods with one tap, set reminders for vaccines, flea and tick pills, heartworm, grooming and vet visits, track weight with a chart and get a daily food plan. It is free, works in your browser and offline, and installs on your phone like a normal app.',
        feats=[('One tap daily log', 'Walk, meal, meds, potty, play, treat, grooming and vet buttons, with a walk counter for the day and the week.'),
               ('Pet diary', 'Notes with date, time, mood, tags, weight and a photo, grouped by day.'),
               ('Vet and care reminders', 'Vaccines, flea and tick, heartworm, deworming, grooming, nail trims, baths and checkups, repeating weekly, monthly, every 3 or 6 months or yearly. Add them to your phone calendar in one tap.'),
               ('Weight tracker', 'A weight chart plus the healthy weight range for 70 dog breeds and 10 cat breeds.'),
               ('Food calculator', 'Daily calories with the RER formula vets use, in cups or grams for your food, plus water and treat limits.'),
               ('Private backup', 'Everything stays on your device. Download a backup file and restore it on a new phone.')],
        faq=[('Is Paw Diary free?', 'Yes, completely free, with no sign up and no in-app purchases.'),
             ('Will it remind me when the app is closed?', 'The app shows what is due every time you open it, and can show an alert. To get a phone alert even when the app is closed, tap the calendar button and the reminder goes to your phone\'s calendar with an alarm.'),
             ('Where is my data saved?', 'Only on your device, in your browser. Nothing is sent to us. Use "Download a backup" from time to time, especially before changing phones.'),
             ('How do I install it on my phone?', 'On Android, tap "Install app" at the top (Chrome). On iPhone, open the page in Safari, tap Share and then "Add to Home Screen".'),
             ('Is the food calculator veterinary advice?', 'No. It is a starting point based on the standard RER formula. Ask your vet before changing your pet\'s diet.')],
        other_label='Español', in_lang='en-US'),
    'es': dict(
        title='Paw Diary: app gratis de diario, recordatorios del veterinario y peso para perros y gatos',
        desc='App gratis para dueños de perros y gatos: anota paseos, comidas y remedios, recibe recordatorios de vacunas y pastillas para pulgas, sigue el peso con un gráfico y mira cuánto darle de comer. Funciona sin internet y sin registrarte.',
        h1='Paw Diary: diario y recordatorios gratis para tu mascota',
        intro='Paw Diary junta el día a día y la salud de tu perro o gato en un solo lugar. Anota paseos, comidas, remedios y cómo está con un toque, pon recordatorios de vacunas, pulgas y garrapatas, pastilla del corazón, peluquería y veterinario, sigue su peso con un gráfico y mira cuánto darle de comer. Es gratis, funciona en el navegador y sin internet, y se instala en tu celular como una app normal.',
        feats=[('Anotar con un toque', 'Botones de paseo, comida, remedio, baño, juego, premio, aseo y veterinario, con contador de paseos del día y de la semana.'),
               ('Diario', 'Notas con fecha, hora, ánimo, etiquetas, peso y foto, ordenadas por día.'),
               ('Recordatorios', 'Vacunas, pulgas y garrapatas, pastilla del corazón, desparasitar, peluquería, uñas, baño y controles, cada semana, mes, 3 o 6 meses o año. Agrégalos al calendario de tu celular con un toque.'),
               ('Control de peso', 'Gráfico de peso y el rango sano para 70 razas de perro y 10 de gato.'),
               ('Calculadora de comida', 'Calorías diarias con la fórmula RER que usan los veterinarios, en tazas o gramos de su alimento, más agua y premios.'),
               ('Copia privada', 'Todo queda en tu equipo. Descarga una copia y restáurala en un celular nuevo.')],
        faq=[('¿Paw Diary es gratis?', 'Sí, totalmente gratis, sin registrarte y sin compras dentro de la app.'),
             ('¿Me avisa si la app está cerrada?', 'La app te muestra lo pendiente cada vez que la abres, y puede mostrar un aviso. Para que te avise el celular aunque esté cerrada, toca el botón de calendario y el recordatorio se guarda en el calendario de tu celular con alarma.'),
             ('¿Dónde se guardan mis datos?', 'Solo en tu equipo, en tu navegador. No nos llega nada. Usa "Descargar una copia" de vez en cuando, sobre todo antes de cambiar de celular.'),
             ('¿Cómo la instalo en el celular?', 'En Android, toca "Instalar app" arriba (Chrome). En iPhone, abre la página en Safari, toca Compartir y después "Agregar a inicio".'),
             ('¿La calculadora de comida es un consejo veterinario?', 'No. Es un punto de partida con la fórmula RER. Consulta a tu veterinario antes de cambiar su alimentación.')],
        other_label='English', in_lang='es-US'),
}

APPS = {
    'fun': dict(tpl='fun.html', seo=SEO, name='Paw Party by Cozy Paws', short='Paw Party', cat='EntertainmentApplication', cats=['entertainment', 'lifestyle'],
                theme='#4E7F86', pin='/img/pin/app-fun.jpg', cache='pawparty',
                shortcuts={'en': [('Cards', '#card'), ('Human years', '#age')], 'es': [('Tarjetas', '#card'), ('Años humanos', '#age')]}),
    'diary': dict(tpl='diary.html', seo=DIARY_SEO, name='Paw Diary by Cozy Paws', short='Paw Diary', cat='LifestyleApplication', cats=['lifestyle', 'health', 'productivity'],
                  theme='#3B2433', pin='/img/pin/app-diary.jpg', cache='pawdiary',
                  shortcuts={'en': [('Reminders', '#rem'), ('Diary', '#log')], 'es': [('Recordatorios', '#rem'), ('Diario', '#log')]}),
}


def manifest(slug, lang):
    a, es = APPS[slug], lang == 'es'
    base = f'/{slug}/' + ('es/' if es else '')
    return {
        'id': base, 'name': a['name'], 'short_name': a['short'], 'description': a['seo'][lang]['desc'], 'lang': lang,
        'start_url': base + '?source=pwa', 'scope': f'/{slug}/', 'display': 'standalone',
        'background_color': '#F3E9D7', 'theme_color': a['theme'], 'orientation': 'portrait', 'categories': a['cats'],
        'icons': [{'src': f'/{slug}/icons/icon-192.png', 'sizes': '192x192', 'type': 'image/png'},
                  {'src': f'/{slug}/icons/icon-512.png', 'sizes': '512x512', 'type': 'image/png'},
                  {'src': f'/{slug}/icons/icon-maskable-512.png', 'sizes': '512x512', 'type': 'image/png', 'purpose': 'maskable'}],
        'shortcuts': [{'name': n, 'url': base + h} for n, h in a['shortcuts'][lang]],
    }


def shared_style():
    s = open(os.path.join(HERE, 'fun.html'), encoding='utf-8').read()
    return s[s.index('<style>'):s.index('</style>') + 8]


def build_app(slug, out, config, all_prods, today):
    """Escribe /<slug>/ y /<slug>/es/. Devuelve [(ruta, fecha)] para el sitemap."""
    a = APPS[slug]
    d = os.path.join(out, slug)
    for sub in ('icons', 'stamps', 'es'):
        os.makedirs(os.path.join(d, sub), exist_ok=True)
    for f in os.listdir(ASSETS):
        if f.endswith('.png'):
            shutil.copy(os.path.join(ASSETS, f), os.path.join(d, 'icons', f))
    stamps = stamp_links(config, all_prods, today)
    if slug == 'fun':
        for f in os.listdir(os.path.join(ASSETS, 'stamps')):
            shutil.copy(os.path.join(ASSETS, 'stamps', f), os.path.join(d, 'stamps', f))
    else:
        os.rmdir(os.path.join(d, 'stamps'))
    tpl = open(os.path.join(HERE, a['tpl']), encoding='utf-8').read().replace('<!--SHARED_STYLE-->', shared_style())
    url, host = config['url'], config['url'].split('//')[1]
    for lang in ('en', 'es'):
        s = a['seo'][lang]
        path = f'/{slug}/' + ('es/' if lang == 'es' else '')
        other = f'/{slug}/es/' if lang == 'en' else f'/{slug}/'
        ld = [{'@context': 'https://schema.org', '@type': 'WebApplication', 'name': a['short'], 'url': url + path, 'inLanguage': s['in_lang'],
               'applicationCategory': a['cat'], 'operatingSystem': 'Any (web, Android, iPhone)', 'description': s['desc'],
               'offers': {'@type': 'Offer', 'price': '0', 'priceCurrency': 'USD'}, 'image': url + f'/{slug}/icons/icon-512.png',
               'publisher': {'@type': 'Organization', 'name': 'Cozy Paws', 'url': url}},
              {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
                  {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': ans}} for q, ans in s['faq']]}]
        head = (f'<title>{E(s["title"])}</title><meta name="description" content="{E(s["desc"])}">'
                f'<link rel="canonical" href="{url}{path}"><link rel="alternate" hreflang="en" href="{url}/{slug}/">'
                f'<link rel="alternate" hreflang="es" href="{url}/{slug}/es/"><link rel="alternate" hreflang="x-default" href="{url}/{slug}/">'
                f'<link rel="manifest" href="{path}manifest.webmanifest">'
                f'<meta property="og:title" content="{E(s["title"])}"><meta property="og:description" content="{E(s["desc"])}">'
                f'<meta property="og:image" content="{url}{a["pin"]}"><meta property="og:url" content="{url}{path}"><meta property="og:type" content="website">'
                f'<meta name="twitter:card" content="summary_large_image">'
                + (f'<meta name="google-site-verification" content="{E(config["google_verify"])}">' if config.get('google_verify') else '')
                + (f'<meta name="p:domain_verify" content="{E(config["pinterest_verify"])}">' if config.get('pinterest_verify') else '')
                + ''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ld))
        feats = ''.join(f'<li><b>{E(x)}.</b> {E(y)}</li>' for x, y in s['feats'])
        faq = ''.join(f'<details><summary>{E(q)}</summary><p>{E(ans)}</p></details>' for q, ans in s['faq'])
        en = lang == 'en'
        sib = 'diary' if slug == 'fun' else 'fun'
        sib_txt = (('Paw Diary: diary, reminders and weight' if en else 'Paw Diary: diario, recordatorios y peso') if sib == 'diary'
                   else ('Paw Party: human years, names, quiz and cards' if en else 'Paw Party: edad humana, nombres, test y tarjetas'))
        seo = (f'<section class="seo"><h1>{E(s["h1"])}</h1><p>{E(s["intro"])}</p><h2>{"What you can do" if en else "Qué puedes hacer"}</h2><ul>{feats}</ul>'
               f'<h2>{"Questions" if en else "Preguntas frecuentes"}</h2>{faq}'
               f'<p>{"More free apps and tools" if en else "Más apps y herramientas gratis"}: <a href="/{sib}/{"" if en else "es/"}">{E(sib_txt)}</a> · '
               f'<a href="/tools/">{"Pet tools" if en else "Calculadoras (en inglés)"}</a> · <a href="/gifts/">{"Gift guides" if en else "Guías de regalos (en inglés)"}</a> · '
               f'<a href="{config["shop"]}" data-etsy="{slug}-seo" rel="noopener">Cozy Paws Etsy shop</a></p></section>')
        cfg = {'lang': lang, 'stamps': stamps, 'host': host, 'company': config['company'], 'shop': config['shop'],
               'ads': config['adsense'] if config.get('adsense_on') else '', 'firebase': config.get('firebase') or None}
        doc = (tpl.replace('__LANG__', lang).replace('<!--HEAD-->', head).replace('<!--SEO-->', seo)
               .replace('<!--ANALYTICS-->', analytics_js(config)).replace('/*CFG*/', 'var CFG=' + json.dumps(cfg, ensure_ascii=False) + ';')
               .replace('__OTHER_URL__', other).replace('__OTHER_LABEL__', s['other_label']))
        if config.get('firebase'):  # cuentas (apps/cuenta.js): solo si hay proyecto Firebase cargado en build.py
            doc = doc.replace('</body>', '<script>' + open(os.path.join(HERE, 'cuenta.js'), encoding='utf-8').read() + '</script>\n</body>')
        open(os.path.join(out, path.strip('/'), 'index.html'), 'w', encoding='utf-8').write(doc)
        open(os.path.join(out, path.strip('/'), 'manifest.webmanifest'), 'w', encoding='utf-8').write(json.dumps(manifest(slug, lang), ensure_ascii=False, indent=1))

    # service worker: la versión cambia solo si cambia el código de la app o las imágenes (no todos los días)
    h = hashlib.sha1(tpl.encode() + json.dumps(config.get('firebase')).encode() + open(os.path.join(HERE, 'cuenta.js'), 'rb').read())
    if slug == 'fun':
        for f in sorted(os.listdir(os.path.join(ASSETS, 'stamps'))):
            h.update(f.encode())
    ver, c = h.hexdigest()[:10], a['cache']
    pre = [f'/{slug}/', f'/{slug}/es/', f'/{slug}/manifest.webmanifest', f'/{slug}/es/manifest.webmanifest', '/img/logo-160.png', '/img/logo-ilustrado.png', '/img/icon.png',
           '/fonts/Yesteryear-Regular.woff2', '/fonts/AbrilFatface-Regular.woff2', '/fonts/Lora.woff2',
           f'/{slug}/icons/icon-192.png', f'/{slug}/icons/icon-512.png'] + ([f'/fun/stamps/{x["id"]}.png' for x in stamps] if slug == 'fun' else [])
    sw = f"""// {a['short']} (Cozy Paws): funciona sin internet. Versión {ver} (cambia sola cuando cambia la app).
const C='{c}-{ver}',PRE={json.dumps(pre)};
self.addEventListener('install',e=>{{e.waitUntil(caches.open(C).then(c=>c.addAll(PRE)).then(()=>self.skipWaiting()))}});
self.addEventListener('activate',e=>{{e.waitUntil(caches.keys().then(k=>Promise.all(k.filter(x=>x.startsWith('{c}-')&&x!==C).map(x=>caches.delete(x)))).then(()=>self.clients.claim()))}});
self.addEventListener('notificationclick',e=>{{e.notification.close();e.waitUntil(clients.openWindow('/{slug}/#rem'))}});
self.addEventListener('fetch',e=>{{const r=e.request,u=new URL(r.url);if(r.method!=='GET'||u.origin!==location.origin)return;
 if(r.mode==='navigate'){{e.respondWith(fetch(r).then(x=>{{const y=x.clone();caches.open(C).then(c=>c.put(u.pathname,y));return x}}).catch(()=>caches.match(u.pathname).then(m=>m||caches.match('/{slug}/'))));return}}
 e.respondWith(caches.match(r).then(m=>{{const f=fetch(r).then(x=>{{if(x.ok){{const y=x.clone();caches.open(C).then(c=>c.put(r,y))}}return x}}).catch(()=>m);return m||f}}));}});
"""
    open(os.path.join(d, 'sw.js'), 'w', encoding='utf-8').write(sw)
    return [(f'/{slug}/', today), (f'/{slug}/es/', today)]


def build_fun(out, config, all_prods, today):
    return build_app('fun', out, config, all_prods, today)


def build_diary(out, config, all_prods, today):
    return build_app('diary', out, config, all_prods, today)
