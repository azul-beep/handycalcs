# Handy Calcs: plan de anuncios y crecimiento

## Redes de anuncios (por etapas)
1. **Ahora: Google AdSense** (Auto ads). Ya está el lugar en la web; solo falta el ID ca-pub.
2. **A las 10.000 sesiones/mes: Mediavine Journey** (paga bastante más que AdSense). Se pide desde mediavine.com con los datos de Google Analytics.
3. **Alternativa si Mediavine tarda: Newor Media** (comparte 70-75% con sitios chicos).
4. **No por ahora:** Ezoic (pide 250.000) y Raptive (pide 100.000 páginas vistas).
El monitor de ingresos revisa las sesiones en GA4 y avisa cuando se pasa 10.000.

## Lo que ya está en la web
1. Página "Advertise with us / Publicidad" (/advertise/ y /es/advertise/). Solo se aceptan patrocinios si los ofrecen; siempre marcados "Sponsored" + rel="sponsored".
2. Cuadro de newsletter en todas las calculadoras y en la portada. Se prende solo al cargar el formulario de MailerLite (`mailerlite_action` en build.py).
3. Afiliados: cuadros listos para Publer, SocialBee, Typefully y Amazon (se muestran cuando hay link).

## Extensión de Chrome
Carpeta `extension/` y zip `handycalcs-extension-chrome.zip`: calculadora de propinas en la barra del navegador, en inglés y español, con links a la web. No junta datos.
Publicarla cuesta 5 USD una sola vez (cuenta de desarrollador de Chrome Web Store). Pendiente del OK de Azu.

## Newsletter (MailerLite, gratis hasta 1.000 suscriptores)
1. En MailerLite: Forms > Embedded form "Handy Calcs", campo email + campo oculto "language". Grupo "Handy Calcs EN" / "ES".
2. Pasar la URL "action" del formulario (https://assets.mailerlite.com/jsonp/.../subscribe).
3. Automatización semanal: Claude escribe los correos; MailerLite los manda solo.
