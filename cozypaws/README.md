# Cozy Paws: web para traer tráfico a la tienda de Etsy

Web estática (inglés, público de EE. UU.) que vive en https://cozypawsgifts.pages.dev y empuja visitas a Etsy desde Google y Pinterest.

- **Guías de regalos** (`/gifts/...`): dog mom, cat mom, razas, Navidad, menos de 25 USD, tazas, invierno, papelería. Cada una aparece cuando tiene 2 productos, como mucho una guía nueva por día.
- **Guía navideña principal** (`/gifts/christmas-gift-guide-dog-owners/`): junta todo lo de perros por tipo de dueño (dog mom, dog dad, cachorro nuevo, duelo, aire libre, el perro mismo, fotos combinadas), por raza y por presupuesto, con preguntas frecuentes. Schema BreadcrumbList + ItemList + FAQPage. Se rearma sola cada día con los productos ya publicados; cada sección aparece cuando tiene productos. Está destacada arriba en `/gifts/` y enlazada desde las guías de perros. Se edita en `HUB` de build.py.
- **Guías por tipo de dueño** (salen solas, una por día, después de las existentes): cachorro nuevo (2 dic), regalos graciosos (3 dic), dueños que salen al aire libre (4 dic), stocking stuffers de 20 USD o menos (5 dic). La clave `desde` evita que corran las fechas de las guías anteriores.
- **Páginas de confianza**: `/about/` (Azu, historia de la marca, valores, galería "Life with dogs"), `/shipping-returns/`, `/faq/`, `/contact/`, `/terms/` y `/privacy/`, con schema AboutPage, FAQPage y ContactPage. Bloque "Meet the maker" en el inicio. Las fotos de Azu van en `cozypaws/data/autora/` (ver el LEEME de esa carpeta); sin fotos se usa el logo.
- **Productos** (`/p/...`): uno por publicación de Etsy, el mismo día de su fecha en el calendario (la web se arma a las 2 PM de Utah, cuando la tanda ya está cargada). Botón "See it on Etsy".
- **Herramientas gratis** (`/tools/...`): edad del perro, edad del gato, cuánta comida darle al perro, generador de nombres. Traen búsquedas de Google todo el año, no solo en Navidad.
- **feed.xml**: RSS con imagen de pin 1000x1500 por item. Pinterest lo lee y publica solo.
- GA4 + Pixel de Meta con aviso de cookies (se cargan solo si la persona acepta), política de privacidad, sitemap, robots.

## Cómo corre solo
`.github/workflows/cozypaws.yml` corre todos los días a las 21:00 UTC (2 PM de Utah): `python3 cozypaws/build.py` y commit de `cozypaws/site`. Cloudflare Pages publica cada commit.

## Aviso a buscadores (IndexNow)
`.github/workflows/cozypaws-indexnow.yml` corre a las 21:30 UTC (después de la publicación) y `cozypaws/indexnow.py` avisa a Bing y otros de las páginas nuevas o cambiadas del sitemap. La clave está en `INDEXNOW_KEY` de build.py y se publica como `/<clave>.txt`. Google lee el sitemap solo.

## Configuración (arriba de build.py, en CONFIG)
`url`, `shop` (hoy apunta al nombre viejo de Etsy, que redirige solo), `pinterest`, `ga4`, `pixel`, `pinterest_verify`, `google_verify`.

## Productos nuevos
1. Los hilos de diseño agregan filas en `/mnt/project-files/navidad-mascotas-maestros/listados-*.csv` y las estampas en `estampas/`.
2. Correr `python3 cozypaws/sync.py` (desde un hilo de Claude con la carpeta del proyecto): copia filas y vistas previas a `cozypaws/data/`.
3. Commit a main. El workflow hace el resto.

Links directos de Etsy (opcional): `cozypaws/data/etsy-links.txt`, una línea por producto: `p01 https://www.etsy.com/listing/123456789`. Sin link directo, el botón abre la búsqueda dentro de la tienda.

## Redes (Instagram y Facebook, Threads si tiene token)
`.github/workflows/cozypaws-redes.yml` + `social.py`, con las APIs oficiales de Meta (gratis, sin Claude). Por día, en hora de Utah:
1. 10 AM: producto nuevo en el feed + una historia (el producto nuevo con "New in the shop", o una tarjeta del banco si no hay productos nuevos).
2. 1 PM: un post que no es de venta: tip de cuidado, frase, Social Club o pregunta para la comunidad.
3. 6 PM: otro producto nuevo.

Los textos de los posts que no son de venta están en `BANCO` de `contenido.py` y rotan en orden. Para sumar, agregar entradas al final con un id nuevo. Las imágenes se arman con plantillas en cada build (`site/img/social/`, `site/img/story/`). Lo publicado queda en `data/redes-publicado.json`.
