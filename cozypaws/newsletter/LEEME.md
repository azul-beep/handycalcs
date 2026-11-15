# Newsletter mensual de Cozy Paws Club

Un mail por mes al grupo "Cozy Paws Club" de MailerLite con los productos nuevos, el cupón del club, artículos nuevos del blog y una herramienta gratis. Se arma y se manda solo con GitHub Actions. Gratis y sin Claude.

## Qué corre solo

1. `.github/workflows/cozypaws-newsletter.yml` corre los días 1 a 10 de cada mes a las 9 AM de Utah.
2. `cozypaws/newsletter.py` espera al primer martes del mes. Ese día:
   1. Toma los productos que salieron en la web desde el newsletter anterior (los mismos de `feed.xml`, leídos de `data/productos.csv`). Elige 6 variados (uno por tipo: taza, adorno, buzo...). Si hubo menos de 2 nuevos, completa con los más recientes y el título dice "Member favorites".
   2. Suma hasta 3 artículos nuevos del blog y una herramienta o app gratis que rota cada mes.
   3. Asunto y saludo según el mes (diciembre con la fecha límite de envío de Navidad). Los textos están en `MONTHS` de `newsletter.py`.
   4. Guarda la versión mail en `cozypaws/newsletter/AAAA-MM.html` y la versión web en `data/newsletter/AAAA-MM.html`. La web la publica en `/news/AAAA-MM/` (archivo en `/news/`) en el build diario.
   5. Si existe el secret `MAILERLITE_TOKEN`, crea la campaña en MailerLite y la manda. Queda anotada en `data/newsletter-enviado.json` y no se manda dos veces.
3. Si GitHub atrasa o saltea el cron, sale en la corrida siguiente (hasta el día 10).
4. El primer número es diciembre 2026 (martes 1 de diciembre). Antes de eso no hace nada.
5. Links con UTM (`utm_campaign=newsletter`, `utm_content=` producto, tienda, cupón...) para ver en GA4 qué vende.

## Qué hace Azu una vez (cuando MailerLite apruebe la cuenta)

1. MailerLite > Integrations > MailerLite API > Generate new token. Nombre `GitHub newsletter`. Copiarla.
2. GitHub > repo handycalcs > Settings > Secrets and variables > Actions > New repository secret. Nombre `MAILERLITE_TOKEN`, pegar la clave. (La pega Azu; Claude no pega claves.)
3. Opcional, solo el primer mes: en la pestaña Variables crear `NEWSLETTER_MODO` = `borrador`. Así el de diciembre queda como borrador en MailerLite > Campaigns para mirarlo y tocar Send. Después borrar la variable (o poner `enviar`) y los siguientes salen solos.
4. Opcional: Actions > "Cozy Paws - newsletter mensual" > Run workflow para probar ya.

Sin la clave no se rompe nada: el mail queda armado en el repo y publicado en la web, y desde el día 8 el workflow muestra un aviso amarillo.

## Qué vigila el monitor

1. Si el envío falla, el workflow falla y abre un issue "Newsletter de Cozy Paws: no salió" con lo que hay que revisar. GitHub le manda el mail a Azu.
2. El vigilante (Apps Script) ya lee los mails de mailerlite.com con "limit", "paused", "suspend" o "error".
3. Límite del plan gratis: 2.500 mails por mes y 250 suscriptores. Un newsletter por mes más la bienvenida entra de sobra.

## Plan B si el plan gratis no deja mandar el HTML por la API

La documentación de MailerLite dice que el contenido HTML por API "no está disponible en todos los planes" y no dice cuáles. Lo sabremos en la primera corrida con la clave (el issue lo dice). Si pasa:

1. El mail igual queda armado en `cozypaws/newsletter/AAAA-MM.html` y publicado en `https://cozypawsgifts.pages.dev/news/AAAA-MM/`.
2. Opción gratis con un paso de 2 minutos por mes: en MailerLite duplicar la campaña del mes anterior (editor Drag & drop con logo, una imagen y el botón "See this month's picks" que lleva a `/news/AAAA-MM/`), cambiar el link y mandar.
3. Opción sin pasos: plan pago de MailerLite cuando el club tenga ventas que lo justifiquen.

## Cambiar algo

1. Textos de cada mes: `MONTHS` en `newsletter.py`.
2. Cupón, remitente, cantidad de productos, grupo: `NL` en `newsletter.py`.
3. Herramientas que rotan: `FEATURES`.
4. Probar sin mandar: `python3 cozypaws/newsletter.py --hoy 2026-12-01 --vista` (escribe los HTML; borrarlos si era solo una prueba).
