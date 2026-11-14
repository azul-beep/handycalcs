# Cozy Paws: web para traer tráfico a la tienda de Etsy

Web estática (inglés, público de EE. UU.) que vive en https://cozypawsgifts.pages.dev y empuja visitas a Etsy desde Google y Pinterest.

- **Guías de regalos** (`/gifts/...`): dog mom, cat mom, razas, Navidad, menos de 25 USD, tazas, invierno, papelería. Cada una aparece cuando tiene 2 productos, como mucho una guía nueva por día.
- **Productos** (`/p/...`): uno por publicación de Etsy, el mismo día de su fecha en el calendario (la web se arma a las 2 PM de Utah, cuando la tanda ya está cargada). Botón "See it on Etsy".
- **Herramientas gratis** (`/tools/...`): edad del perro, edad del gato, cuánta comida darle al perro, generador de nombres. Traen búsquedas de Google todo el año, no solo en Navidad.
- **feed.xml**: RSS con imagen de pin 1000x1500 por item. Pinterest lo lee y publica solo.
- GA4 + Pixel de Meta con aviso de cookies (se cargan solo si la persona acepta), política de privacidad, sitemap, robots.

## Cómo corre solo
`.github/workflows/cozypaws.yml` corre todos los días a las 21:00 UTC (2 PM de Utah): `python3 cozypaws/build.py` y commit de `cozypaws/site`. Cloudflare Pages publica cada commit.

## Configuración (arriba de build.py, en CONFIG)
`url`, `shop` (hoy apunta al nombre viejo de Etsy, que redirige solo), `pinterest`, `ga4`, `pixel`, `pinterest_verify`, `google_verify`.

## Productos nuevos
1. Los hilos de diseño agregan filas en `/mnt/project-files/navidad-mascotas-maestros/listados-*.csv` y las estampas en `estampas/`.
2. Correr `python3 cozypaws/sync.py` (desde un hilo de Claude con la carpeta del proyecto): copia filas y vistas previas a `cozypaws/data/`.
3. Commit a main. El workflow hace el resto.

Links directos de Etsy (opcional): `cozypaws/data/etsy-links.txt`, una línea por producto: `p01 https://www.etsy.com/listing/123456789`. Sin link directo, el botón abre la búsqueda dentro de la tienda.
