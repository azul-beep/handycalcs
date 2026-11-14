# -*- coding: utf-8 -*-
"""Contenido de la guía "Herramientas gratis para emprender online".

Español neutro con "tú" (público hispano en EE.UU.).
- Links a herramientas: href="AFF_CLAVE" (se resuelven con afiliados.json).
- Links internos: href="PAG:slug" (si la página todavía no salió, el link se quita y queda el texto).
Datos de planes gratis consultados en noviembre de 2026 (ver "fuentes" en cada página).
"""

REVISADO = "noviembre de 2026"
AUTORA = "Azu, de Skye Solutions AI (Utah)"

F = {  # fuentes reutilizables
    "payhip_precios": ("Payhip: precios", "https://payhip.com/pricing"),
    "payhip_partner": ("Payhip: Partner Program", "https://payhip.com/partner-program"),
    "ml_free": ("GroupMail: límites del plan gratis de MailerLite 2026", "https://blog.groupmail.io/mailerlite-free-plan-limits/"),
    "ml_aff": ("MailerLite: programa de afiliados", "https://www.mailerlite.com/affiliate"),
    "canva_free": ("Style Factory: Canva Pro vs Free (act. 3 nov 2026)", "https://www.stylefactoryproductions.com/blog/canva-pro-vs-free"),
    "canva_aff": ("Canva: programa de afiliados", "https://www.canva.com/affiliates/"),
    "printify_precios": ("Printify: precios", "https://printify.com/pricing/"),
    "printify_aff": ("Printify: programa de afiliados", "https://printify.com/affiliate/"),
    "etsy_fees": ("Etsy: política de tarifas", "https://www.etsy.com/legal/fees/"),
    "etsy_aff": ("Etsy: programa de afiliados", "https://help.etsy.com/hc/en-us/articles/360000335987"),
    "pin_rss": ("Pinterest: publicar pines automáticamente desde tu RSS", "https://help.pinterest.com/en/business/article/auto-publish-pins-from-your-rss-feed"),
    "pin_biz": ("Pinterest: cuenta de empresa", "https://help.pinterest.com/en/business/article/get-a-business-account"),
    "ga4_ret": ("Google: retención de datos en Analytics", "https://support.google.com/analytics/answer/7667196?hl=en"),
    "netlify_precios": ("Netlify: precios", "https://www.netlify.com/pricing/"),
    "cf_limites": ("Cloudflare Pages: límites", "https://developers.cloudflare.com/pages/platform/limits/"),
    "gh_limites": ("GitHub Pages: límites", "https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits"),
    "kdp_regalias": ("Amazon KDP: regalías de eBook", "https://kdp.amazon.com/en_US/help/topic/G200644210"),
    "amz_politicas": ("Amazon Associates: políticas del programa", "https://affiliate-program.amazon.com/help/operating/policies"),
}

ORDEN_POR_DEFECTO = [
    "index", "mejores-herramientas-gratis-vender-productos-digitales-2027",
    "payhip-gratis", "mailerlite-gratis", "canva-gratis", "pinterest-gratis",
    "printify-gratis", "etsy-productos-digitales", "amazon-kdp-gratis",
    "hosting-gratis-cloudflare-netlify-github", "google-analytics-4-gratis",
]

PAGINAS = {}

# ---------------------------------------------------------------- HUB
PAGINAS["index"] = dict(
    titulo="Herramientas gratis para emprender online (guía en español)",
    meta="Guía en español de herramientas gratis para vender productos digitales desde EE.UU.: Payhip, MailerLite, Canva, Pinterest, Printify, Etsy, KDP y más.",
    h1="Herramientas gratis para emprender online",
    pin=("Herramientas", "GRATIS para", "emprender online", "Guía en español"),
    color=("#3f4a38", "#faf8f4"),
    resumen="La guía completa: qué herramienta usar para cada paso y qué te cobra cada una.",
    es_hub=True,
    intro="""<p>Si quieres vender productos digitales, plantillas, libros o productos impresos desde Estados Unidos, no necesitas pagar mensualidades para empezar. Esta guía junta las herramientas gratuitas que uso en mi propio negocio, con lo que <strong>sí</strong> te cobran (comisiones por venta, límites del plan gratis) y cuándo conviene pasar a un plan pago.</p>
<p>Cada guía explica cómo funciona la herramienta paso a paso, sus límites reales a {rev} y enlaces a las fuentes oficiales para que lo compruebes tú.</p>""",
    cuerpo="""<h2>Por dónde empezar según lo que quieres hacer</h2>
<ol>
<li><strong>Vender un PDF, una plantilla o un curso:</strong> tienda en Payhip + diseño en Canva + lista de correo en MailerLite.</li>
<li><strong>Vender camisetas, tazas o bolsas sin inventario:</strong> Printify conectado a Etsy u otra tienda.</li>
<li><strong>Publicar un libro, cuaderno o agenda:</strong> Amazon KDP.</li>
<li><strong>Conseguir visitas sin pagar anuncios:</strong> Pinterest con publicación automática desde tu web.</li>
<li><strong>Tener tu propia web gratis:</strong> Cloudflare Pages o Netlify, con el código guardado en GitHub.</li>
<li><strong>Saber qué funciona:</strong> Google Analytics 4.</li>
</ol>
<h2>Todas las guías</h2>
{{LISTA_GUIAS}}
<h2>Cómo elegimos estas herramientas</h2>
<p>Están aquí porque tienen un plan gratis que sirve de verdad para empezar (no una prueba de 7 días), funcionan en español o son fáciles de usar sin inglés avanzado, y aceptan cuentas de negocios en Estados Unidos. Revisamos los datos de cada plan una vez al mes; si algo cambia, lo actualizamos.</p>""",
    faq=[
        ("¿De verdad se puede emprender online sin pagar nada?",
         "Sí, para empezar. Payhip, MailerLite, Canva, Printify, Pinterest, Google Analytics, Cloudflare Pages y Amazon KDP tienen plan gratis o no cobran por abrir la cuenta. Lo que sí pagas son comisiones cuando vendes (por ejemplo, 5 % en el plan gratis de Payhip) y, en Etsy, USD 0.20 por cada producto publicado."),
        ("¿Necesito una LLC para usar estas herramientas?",
         "No. Todas permiten empezar como persona. Si ya tienes una LLC con EIN, puedes registrar las cuentas a nombre del negocio para separar tus finanzas; consulta con un contador cómo declarar los ingresos."),
        ("¿Por qué hay enlaces de afiliado en esta guía?",
         "Algunas herramientas nos pagan una comisión si te registras o pagas un plan desde nuestro enlace. A ti no te cuesta más. Las herramientas sin programa de afiliados también están en la guía, porque las usamos igual."),
        ("¿Cada cuánto se actualiza la información?",
         "Revisamos los enlaces y las páginas de precios de cada herramienta una vez al mes. Arriba de cada guía verás la fecha de la última revisión."),
    ],
    fuentes=[],
)

# ---------------------------------------------------------------- COMPARATIVA
PAGINAS["mejores-herramientas-gratis-vender-productos-digitales-2027"] = dict(
    titulo="Las mejores herramientas gratis para vender productos digitales en 2027",
    meta="Comparativa honesta de Payhip, Etsy, MailerLite, Canva, Printify, KDP y hosting gratis: qué cobra cada una, límites del plan gratis y cuándo pagar.",
    h1="Las mejores herramientas gratis para vender productos digitales en 2027",
    pin=("Las mejores", "herramientas gratis", "para vender", "productos digitales 2027"),
    color=("#5b3a29", "#fbf3ea"),
    resumen="Tabla comparativa: qué cobra cada herramienta y cuándo vale la pena pagar.",
    intro="""<p>Esta comparativa responde una pregunta concreta: <strong>¿con qué herramientas gratis puedo vender productos digitales (PDF, plantillas, planners, cursos) en 2027 y cuánto me cuesta cada venta?</strong> Los datos son de las páginas oficiales, revisados en {rev}.</p>""",
    cuerpo="""<h2>Resumen rápido</h2>
<div class="tabla-scroll"><table>
<thead><tr><th>Herramienta</th><th>Para qué sirve</th><th>Plan gratis</th><th>Qué te cobra</th></tr></thead>
<tbody>
<tr><td><a href="AFF_PAYHIP">Payhip</a></td><td>Tienda propia de productos digitales</td><td>Todas las funciones, productos ilimitados</td><td>5 % por venta + comisión de PayPal o Stripe</td></tr>
<tr><td><a href="AFF_ETSY">Etsy</a></td><td>Marketplace con compradores que ya buscan</td><td>No hay mensualidad</td><td>USD 0.20 por publicación + 6.5 % por venta + procesamiento de pago</td></tr>
<tr><td><a href="AFF_MAILERLITE">MailerLite</a></td><td>Lista de correo y automatizaciones</td><td>500 suscriptores, 12 000 correos al mes</td><td>Nada mientras estés dentro del límite</td></tr>
<tr><td><a href="AFF_CANVA">Canva</a></td><td>Diseñar productos, portadas y pines</td><td>5 GB y más de 1.6 millones de plantillas</td><td>Nada; Pro cuesta USD 18/mes o 144/año</td></tr>
<tr><td><a href="AFF_PRINTIFY">Printify</a></td><td>Productos impresos sin inventario</td><td>Hasta 5 tiendas, diseños ilimitados</td><td>El costo de producción de cada pedido</td></tr>
<tr><td><a href="AFF_KDP">Amazon KDP</a></td><td>Libros, cuadernos y agendas</td><td>Publicar no tiene costo</td><td>Amazon se queda con la parte que no es tu regalía</td></tr>
<tr><td><a href="AFF_PINTEREST">Pinterest</a></td><td>Visitas gratis a tu web</td><td>Cuenta de empresa gratis</td><td>Nada</td></tr>
<tr><td><a href="AFF_CLOUDFLARE">Cloudflare Pages</a></td><td>Alojar tu web</td><td>500 publicaciones al mes, 20 000 archivos</td><td>Nada</td></tr>
</tbody></table></div>
<h2>La combinación más barata para empezar</h2>
<ol>
<li><strong>Diseña</strong> tu producto y sus imágenes en Canva gratis.</li>
<li><strong>Véndelo</strong> en Payhip (sin mensualidad, pagas 5 % solo cuando vendes).</li>
<li><strong>Junta correos</strong> con un regalo gratis y MailerLite (gratis hasta 500 suscriptores).</li>
<li><strong>Trae visitas</strong> con Pinterest apuntando a tu página de Payhip o a tu web.</li>
<li><strong>Mide</strong> qué funciona con Google Analytics 4.</li>
</ol>
<p>Con esto tu costo fijo es cero. Lo que pagas depende de lo que vendes.</p>
<h2>Payhip o Etsy: ¿dónde vender tus descargables?</h2>
<p>No tienes que elegir uno solo. <strong>Etsy</strong> te da compradores que ya están buscando, pero cobra por publicar (USD 0.20 por producto, que se renueva cada cuatro meses o cuando se vende) y 6.5 % por venta, más el procesamiento de pago. Además, si una venta llega por los anuncios externos de Etsy, pagas 15 % extra (12 % si vendiste más de USD 10 000 en el último año), con un tope de USD 100 por pedido.</p>
<p><strong>Payhip</strong> no te trae compradores por sí solo, pero cobra 5 % en el plan gratis, te da tu propia tienda y te deja guardar los correos de tus clientes. Una estrategia común: usar Etsy para que te descubran y Payhip para tu tienda propia y tus clientes que vuelven.</p>
<p>Más detalles en <a href="PAG:payhip-gratis">la guía de Payhip</a> y <a href="PAG:etsy-productos-digitales">la guía de Etsy</a>.</p>
<h2>¿Cuándo conviene pasar a un plan pago?</h2>
<ol>
<li><strong>Payhip Plus (USD 29/mes, 2 % por venta):</strong> conviene cuando vendes más de unos USD 967 al mes, porque a partir de ahí el 3 % que ahorras paga la mensualidad (29 ÷ 0.03).</li>
<li><strong>Payhip Pro (USD 99/mes, 0 %):</strong> frente a Plus, conviene cuando vendes más de USD 3 500 al mes (70 ÷ 0.02).</li>
<li><strong>MailerLite pago:</strong> cuando pasas de 500 suscriptores o quieres quitar la marca de MailerLite de tus correos.</li>
<li><strong>Printify Premium (desde USD 24.99/mes al año):</strong> cuando el descuento de hasta 33 % en productos supera la mensualidad.</li>
<li><strong>Canva Pro:</strong> cuando quitar fondos o adaptar un diseño a muchos tamaños te ahorra horas cada semana.</li>
</ol>
<p>Puedes hacer estas cuentas con tus números en las calculadoras de Handy Calcs.</p>""",
    faq=[
        ("¿Cuál es la plataforma gratis que menos comisión cobra por vender descargables?",
         "Entre las de esta guía, Payhip en su plan gratis cobra 5 % por venta más la comisión de PayPal o Stripe, sin mensualidad ni costo por publicar. Etsy cobra USD 0.20 por publicación más 6.5 % por venta y el procesamiento de pago."),
        ("¿Puedo vender en Payhip y en Etsy al mismo tiempo?",
         "Sí. Muchas personas usan Etsy para que las descubran y Payhip como tienda propia. Revisa que tus precios y licencias sean coherentes en las dos."),
        ("¿Qué necesito para empezar con costo cero?",
         "Una cuenta gratis de Canva para diseñar, Payhip para vender, MailerLite para tu lista de correo y Pinterest para traer visitas. Todas tienen plan gratis sin tarjeta para empezar."),
        ("¿Estos precios pueden cambiar?",
         "Sí. Los revisamos cada mes y anotamos la fecha arriba de la página. Antes de decidir, confirma en la página oficial de precios de cada herramienta."),
    ],
    fuentes=["payhip_precios", "etsy_fees", "ml_free", "canva_free", "printify_precios", "kdp_regalias", "pin_biz", "cf_limites"],
)

# ---------------------------------------------------------------- PAYHIP
PAGINAS["payhip-gratis"] = dict(
    titulo="Cómo uso Payhip gratis para vender productos digitales",
    meta="Guía de Payhip en español: plan gratis (5 % por venta), cómo crear tu tienda, cobrar con PayPal o Stripe y cuándo conviene el plan Plus o Pro.",
    h1="Cómo uso Payhip gratis para vender productos digitales",
    pin=("Cómo vender", "productos digitales", "con Payhip", "GRATIS"),
    color=("#1f4e5f", "#eef6f8"),
    resumen="Tienda propia sin mensualidad: 5 % por venta en el plan gratis.",
    intro="""<p>Payhip es una plataforma para vender productos digitales (PDF, plantillas, planners, audios, cursos y membresías) desde tu propia tienda. Lo que la hace útil para empezar es que su plan <strong>Free Forever</strong> no tiene mensualidad: pagas solo cuando vendes.</p>""",
    cuerpo="""<h2>Qué incluye el plan gratis y qué cobra</h2>
<div class="tabla-scroll"><table>
<thead><tr><th>Plan</th><th>Mensualidad</th><th>Comisión de Payhip por venta</th></tr></thead>
<tbody>
<tr><td>Free Forever</td><td>USD 0</td><td>5 %</td></tr>
<tr><td>Plus</td><td>USD 29</td><td>2 %</td></tr>
<tr><td>Pro</td><td>USD 99</td><td>0 %</td></tr>
</tbody></table></div>
<p>Según su página de precios, los tres planes tienen todas las funciones, productos ilimitados e ingresos ilimitados. Encima de la comisión de Payhip, PayPal y Stripe cobran su propia tarifa de procesamiento en cada venta, en cualquier plan.</p>
<h2>Cómo armo una tienda en Payhip paso a paso</h2>
<ol>
<li>Crea tu cuenta gratis en <a href="AFF_PAYHIP">Payhip</a>.</li>
<li>Conecta PayPal, Stripe o ambos para cobrar. El dinero de cada venta llega a esas cuentas.</li>
<li>Sube tu primer producto: el archivo, un título claro, una descripción que diga exactamente qué recibe la persona y una imagen de portada (la puedes hacer en <a href="PAG:canva-gratis">Canva gratis</a>).</li>
<li>Pon un precio. Si dudas, empieza con un producto gratis o de "paga lo que quieras" para juntar tus primeros clientes.</li>
<li>Personaliza tu tienda con tu logo y colores, y escribe una página "Sobre mí".</li>
<li>Comparte el enlace del producto en Pinterest, en tu web y en tus redes.</li>
</ol>
<h2>Funciones que más uso del plan gratis</h2>
<ol>
<li><strong>Cupones y descuentos</strong> para lanzamientos o fechas especiales.</li>
<li><strong>Paquetes (bundles)</strong> para vender varios productos juntos.</li>
<li><strong>Afiliados propios:</strong> puedes dejar que otras personas recomienden tus productos a cambio de una comisión que tú defines.</li>
<li><strong>Lista de clientes:</strong> guardas los correos de quienes compran (con su permiso) y puedes conectarla con <a href="PAG:mailerlite-gratis">MailerLite</a>.</li>
</ol>
<h2>¿Cuándo pasar a Plus o Pro?</h2>
<p>Haz la cuenta con tus ventas mensuales. Plus te ahorra 3 % de comisión a cambio de USD 29 al mes, así que se paga solo a partir de unos <strong>USD 967 en ventas al mes</strong>. Pro frente a Plus ahorra otro 2 % a cambio de USD 70 más, y conviene a partir de <strong>USD 3 500 al mes</strong>. Por debajo de eso, el plan gratis te sale más barato.</p>
<h2>Lo que no me gusta</h2>
<ol>
<li>Payhip no te trae compradores: el tráfico lo tienes que conseguir tú (Pinterest, correo, redes).</li>
<li>Pagas dos comisiones por venta: la de Payhip y la de PayPal o Stripe.</li>
</ol>
<h2>Si recomiendas Payhip, también puedes ganar</h2>
<p>Payhip tiene un programa de socios gratis: según su página, pagan 50 % de lo que Payhip gana de las tiendas que refieres (comisiones y planes), cada mes y de por vida, por PayPal, con un mínimo de USD 50. No necesitas ser cliente para unirte.</p>""",
    faq=[
        ("¿Payhip es gratis de verdad?",
         "Sí, el plan Free Forever no tiene mensualidad. Payhip cobra 5 % de cada venta y PayPal o Stripe cobran su tarifa de procesamiento."),
        ("¿Qué puedo vender en Payhip?",
         "Productos digitales (PDF, plantillas, audio, video, software), cursos online, membresías, servicios y productos físicos."),
        ("¿Cómo me pagan las ventas en Payhip?",
         "El dinero llega directo a tu cuenta de PayPal o Stripe, según lo que conectes."),
        ("¿Cuándo me conviene pagar el plan Plus?",
         "Cuando vendes más de unos USD 967 al mes: a partir de ahí, el 3 % de comisión que ahorras cubre los USD 29 de la mensualidad."),
    ],
    fuentes=["payhip_precios", "payhip_partner"],
)

# ---------------------------------------------------------------- MAILERLITE
PAGINAS["mailerlite-gratis"] = dict(
    titulo="Cómo uso MailerLite gratis para crear mi lista de correo",
    meta="MailerLite gratis en 2026: 500 suscriptores y 12 000 correos al mes. Cómo armar tu lista, un regalo de bienvenida y una automatización paso a paso.",
    h1="Cómo uso MailerLite gratis para crear mi lista de correo",
    pin=("Tu lista de correo", "GRATIS", "con MailerLite", "paso a paso"),
    color=("#0f5132", "#eef8f1"),
    resumen="Lista de correo gratis hasta 500 suscriptores, con automatizaciones.",
    intro="""<p>Las redes cambian sus reglas y tu alcance baja de un día para otro. Tu lista de correo, en cambio, es tuya. MailerLite es una de las pocas herramientas de email marketing con plan gratis que incluye formularios, páginas de aterrizaje y automatizaciones.</p>""",
    cuerpo="""<h2>Límites del plan gratis en 2026</h2>
<ol>
<li><strong>500 suscriptores activos</strong> (los dados de baja o rebotados no cuentan). El límite bajó de 1 000 a 500 el 23 de septiembre de 2025.</li>
<li><strong>12 000 correos al mes</strong>, sin límite diario.</li>
<li>1 usuario, 1 sitio web, 10 páginas de aterrizaje y 1 producto digital.</li>
<li>Tus correos llevan la marca de MailerLite al pie.</li>
<li>No incluye plantillas de correo, editor HTML, reenvío a quienes no abrieron ni el asistente de IA.</li>
<li>Soporte: solo la base de ayuda después de los primeros 14 días.</li>
</ol>
<h2>Cómo armo mi lista paso a paso</h2>
<ol>
<li>Crea tu cuenta en <a href="AFF_MAILERLITE">MailerLite</a>. Te van a pedir datos de tu negocio y revisar la cuenta antes de dejarte enviar: es normal.</li>
<li>Verifica tu dominio de correo si tienes uno (por ejemplo hola@tunegocio.com). Mejora la entrega y evita el spam.</li>
<li>Crea un <strong>grupo</strong> (por ejemplo "Regalo planner").</li>
<li>Prepara un <strong>regalo</strong> que la gente quiera: una plantilla, un checklist o un mini calendario hecho en <a href="PAG:canva-gratis">Canva</a>.</li>
<li>Crea un <strong>formulario</strong> o una <strong>página de aterrizaje</strong> que ofrezca el regalo a cambio del correo.</li>
<li>Crea una <strong>automatización</strong>: cuando alguien entra al grupo, recibe el correo con el enlace de descarga.</li>
<li>Agrega 2 o 3 correos más en la automatización (días 2 y 5, por ejemplo) contando quién eres y mostrando tu producto pago en <a href="PAG:payhip-gratis">Payhip</a>.</li>
<li>Pon el enlace de la página en tu bio, en tus pines de <a href="PAG:pinterest-gratis">Pinterest</a> y en tu web.</li>
</ol>
<h2>Consejos para no pasarte del límite</h2>
<ol>
<li>Cada tres meses, elimina a quienes no abrieron ningún correo en ese tiempo. Te mantiene debajo de 500 y mejora la entrega.</li>
<li>Usa el doble opt-in (confirmación por correo) para evitar correos falsos.</li>
<li>Con 12 000 correos al mes y 500 suscriptores puedes enviar unas 24 campañas al mes: más que suficiente.</li>
</ol>
<h2>Reglas legales básicas en EE.UU.</h2>
<p>La ley CAN-SPAM pide que cada correo comercial tenga una forma clara de darse de baja y una dirección postal física. MailerLite agrega el enlace de baja; la dirección la pones tú (puede ser un apartado postal).</p>
<h2>Programa de afiliados de MailerLite</h2>
<p>MailerLite paga 30 % de cada pago de las personas que refieres, mientras sigan siendo clientes, con una cookie de 45 días. No necesitas ser cliente para unirte. Pagan por PayPal, depósito directo o transferencia (a través de Tipalti) cuando acumulas USD 100 de al menos 2 referidos distintos.</p>""",
    faq=[
        ("¿Cuántos suscriptores permite MailerLite gratis?",
         "Desde el 23 de septiembre de 2025, el plan gratis permite 500 suscriptores activos y 12 000 correos al mes."),
        ("¿El plan gratis de MailerLite tiene automatizaciones?",
         "Sí, puedes crear automatizaciones (por ejemplo, un correo de bienvenida con un regalo), aunque algunas opciones avanzadas como varios disparadores son de pago."),
        ("¿Puedo quitar el logo de MailerLite de mis correos gratis?",
         "No. Quitar la marca requiere un plan pago, que según la fuente consultada empieza en USD 10 al mes."),
        ("¿Qué pasa si llego a 500 suscriptores?",
         "Tienes que limpiar tu lista o pasar a un plan pago. Conviene eliminar cada tanto a quienes no abren tus correos."),
    ],
    fuentes=["ml_free", "ml_aff"],
)

# ---------------------------------------------------------------- CANVA
PAGINAS["canva-gratis"] = dict(
    titulo="Cómo uso Canva gratis para diseñar productos y pines",
    meta="Canva gratis en 2026: 5 GB, más de 1.6 millones de plantillas. Qué puedes hacer sin pagar, qué es solo de Pro y cuidado con la licencia al vender.",
    h1="Cómo uso Canva gratis para diseñar productos y pines",
    pin=("Canva GRATIS", "para diseñar", "productos y pines", "qué incluye"),
    color=("#4b2a7a", "#f4effb"),
    resumen="Diseña productos, portadas y pines sin pagar: qué incluye y qué no.",
    intro="""<p>Canva es la herramienta de diseño que uso para casi todo: portadas de productos, imágenes de Pinterest, páginas de planners y publicaciones. El plan gratis alcanza para empezar; la mayoría de las personas no necesita Pro el primer mes.</p>""",
    cuerpo="""<h2>Qué incluye Canva gratis (2026)</h2>
<ol>
<li>5 GB de almacenamiento.</li>
<li>Más de 1.6 millones de plantillas (Pro tiene más de 3.6 millones).</li>
<li>Un kit de marca con hasta 3 colores.</li>
<li>Descargas en PNG, JPG y PDF.</li>
</ol>
<h2>Qué es solo de Canva Pro</h2>
<ol>
<li>Quitar el fondo de fotos y videos.</li>
<li>Magic Resize: adaptar un diseño a muchos tamaños con un clic.</li>
<li>Traducir diseños a otros idiomas.</li>
<li>Hasta 5 kits de marca y 100 GB de almacenamiento.</li>
</ol>
<p>Canva Pro cuesta USD 18 al mes o USD 144 al año en EE.UU., según la fuente consultada.</p>
<h2>Cómo diseño un pin de Pinterest gratis</h2>
<ol>
<li>Crea un diseño de <strong>1000 × 1500 píxeles</strong> (proporción 2:3, la que recomienda Pinterest).</li>
<li>Elige una plantilla gratis (las de pago tienen una corona) o empieza en blanco.</li>
<li>Escribe un título grande que diga el beneficio ("Calendario 2027 gratis para imprimir").</li>
<li>Usa máximo dos tipografías y tres colores.</li>
<li>Agrega tu web chiquita abajo.</li>
<li>Descarga en PNG y súbelo a <a href="PAG:pinterest-gratis">Pinterest</a>.</li>
</ol>
<h2>Cómo diseño un producto para vender</h2>
<ol>
<li>Crea el diseño en tamaño Carta (8.5 × 11 in), que es el estándar de impresión en EE.UU.; si vendes también fuera, ofrece A4.</li>
<li>Usa elementos gratis o tus propias fotos y dibujos.</li>
<li>Descarga en "PDF para imprimir".</li>
<li>Sube el PDF a <a href="PAG:payhip-gratis">Payhip</a> o a <a href="PAG:etsy-productos-digitales">Etsy</a>.</li>
</ol>
<h2>Importante: la licencia al vender</h2>
<p>Canva permite usar sus elementos en productos que vendes, pero no revender los elementos o plantillas tal cual, sin cambios. Antes de vender, lee el acuerdo de licencia de contenido de Canva y agrega tu propio trabajo (texto, estructura, ilustraciones propias). Si quieres vender <strong>plantillas editables de Canva</strong>, compártelas como enlace de plantilla, no como archivo con elementos sueltos.</p>
<h2>Programa de afiliados de Canva</h2>
<p>Según su página, Canva paga hasta USD 36 por cada suscriptor nuevo de Canva Pro que llegue por tu enlace, con una cookie de 30 días, y paga por PayPal o transferencia. Ojo: dan prioridad a influencers y educadores de diseño y a sitios de diseño con más de 1 millón de visitas al mes, así que no es fácil que aprueben una web pequeña.</p>""",
    faq=[
        ("¿Canva gratis sirve para vender productos?",
         "Sí, puedes diseñar productos con Canva gratis y venderlos, siempre que agregues tu propio trabajo y no revendas los elementos o plantillas de Canva tal cual. Revisa la licencia de contenido de Canva."),
        ("¿Cuánto almacenamiento tiene Canva gratis?",
         "5 GB. Canva Pro tiene 100 GB."),
        ("¿Se puede quitar el fondo de una foto en Canva gratis?",
         "No, el removedor de fondo es una función de Canva Pro."),
        ("¿Qué tamaño uso para un pin de Pinterest en Canva?",
         "1000 × 1500 píxeles, proporción 2:3."),
    ],
    fuentes=["canva_free", "canva_aff"],
)

# ---------------------------------------------------------------- PINTEREST
PAGINAS["pinterest-gratis"] = dict(
    titulo="Cómo uso Pinterest gratis para llevar visitas a mi web",
    meta="Pinterest para emprendedores: cuenta de empresa gratis, reclamar tu web y publicar pines automáticamente desde tu RSS (hasta 200 por día).",
    h1="Cómo uso Pinterest gratis para llevar visitas a mi web",
    pin=("Pinterest GRATIS", "para llevar visitas", "a tu web", "pines automáticos"),
    color=("#9b1c2c", "#fdf0f1"),
    resumen="Visitas gratis desde Pinterest, con pines que se publican solos desde tu web.",
    intro="""<p>Pinterest funciona más como un buscador que como una red social: la gente busca ideas ("planner semanal para imprimir", "calendario 2027") y un pin bueno puede seguir trayendo visitas durante meses. Para un negocio de productos digitales es de las fuentes de tráfico gratis más útiles.</p>""",
    cuerpo="""<h2>Paso 1: cuenta de empresa gratis</h2>
<p>La cuenta de empresa de Pinterest es gratis y te da acceso a Pinterest Analytics para ver cómo les va a tus pines. Si ya tienes una cuenta personal, puedes convertirla.</p>
<h2>Paso 2: reclamar tu web</h2>
<p>"Reclamar" tu sitio le demuestra a Pinterest que la web es tuya. Se hace agregando una etiqueta en el &lt;head&gt; de tu página o un archivo en tu sitio. Es obligatorio para el paso 3.</p>
<h2>Paso 3: publicación automática desde tu RSS</h2>
<p>Esta es la parte que más tiempo me ahorra. Pinterest puede leer el <strong>feed RSS</strong> de tu web y crear un pin por cada entrada nueva, sin que tengas que subirlos a mano:</p>
<ol>
<li>Tienes que tener tu web reclamada; cada entrada del feed debe enlazar a ese dominio.</li>
<li>El feed debe ser RSS 2.x o RSS 1.x (Atom no sirve).</li>
<li>Pinterest toma la imagen de las etiquetas &lt;image&gt;, &lt;enclosure&gt; o &lt;media:content&gt; de cada entrada, y el título y la descripción de &lt;title&gt; y &lt;description&gt;.</li>
<li>Revisa el feed y publica lo nuevo dentro de 24 horas, empezando por lo más antiguo.</li>
<li>Publica hasta 200 pines por día por esta vía.</li>
</ol>
<p>En la configuración de tu cuenta de empresa, busca "Publicación automática" (Auto-publish), pega la URL de tu feed y elige el tablero.</p>
<h2>Cómo hacer pines que funcionen</h2>
<ol>
<li>Formato vertical 2:3 (1000 × 1500 px). Te explico cómo en <a href="PAG:canva-gratis">la guía de Canva</a>.</li>
<li>Título con las palabras que la gente busca, en el pin y en el título del pin.</li>
<li>Descripción de 1 o 2 frases que explique qué va a encontrar al hacer clic.</li>
<li>Un enlace que lleve justo a lo que promete el pin, no a tu página de inicio.</li>
<li>Constancia: mejor 2 o 3 pines por día que 50 un día y nada el resto del mes.</li>
</ol>
<h2>¿Pinterest tiene programa de afiliados?</h2>
<p>No encontramos un programa de afiliados de Pinterest. Lo usamos porque trae visitas gratis, no por comisión.</p>""",
    faq=[
        ("¿La cuenta de empresa de Pinterest es gratis?",
         "Sí. Es gratis y te da acceso a Pinterest Analytics. Los anuncios son opcionales."),
        ("¿Cómo publico pines automáticamente desde mi web?",
         "Reclama tu web en Pinterest y agrega la URL de tu feed RSS en la opción de publicación automática. Pinterest crea los pines nuevos dentro de 24 horas, hasta 200 por día."),
        ("¿Qué tamaño de imagen uso para Pinterest?",
         "Vertical, proporción 2:3; por ejemplo 1000 × 1500 píxeles."),
        ("¿Sirve Pinterest para vender productos digitales?",
         "Sí: la gente busca planners, plantillas y descargables en Pinterest, y cada pin puede enlazar a tu producto en Payhip, Etsy o tu web."),
    ],
    fuentes=["pin_biz", "pin_rss"],
)

# ---------------------------------------------------------------- PRINTIFY
PAGINAS["printify-gratis"] = dict(
    titulo="Cómo uso Printify gratis para vender productos impresos",
    meta="Printify gratis: hasta 5 tiendas y diseños ilimitados, sin inventario. Cómo funciona la impresión bajo demanda, costos reales y cuándo vale Premium.",
    h1="Cómo uso Printify gratis para vender productos impresos sin inventario",
    pin=("Vende camisetas", "y tazas SIN", "inventario con", "Printify gratis"),
    color=("#1d5c3a", "#f0f7f2"),
    resumen="Camisetas, tazas y más sin inventario: impresión bajo demanda.",
    intro="""<p>Printify es un servicio de <strong>impresión bajo demanda</strong>: subes tu diseño, eliges el producto (camiseta, taza, bolsa, póster) y lo publicas en tu tienda. Cuando alguien compra, una imprenta asociada lo fabrica y lo envía. Tú no compras inventario.</p>""",
    cuerpo="""<h2>Plan gratis y plan Premium</h2>
<div class="tabla-scroll"><table>
<thead><tr><th></th><th>Free</th><th>Premium</th></tr></thead>
<tbody>
<tr><td>Precio</td><td>USD 0</td><td>Desde USD 39/mes, o desde USD 24.99/mes pagando el año</td></tr>
<tr><td>Tiendas</td><td>Hasta 5 por cuenta</td><td>Más tiendas</td></tr>
<tr><td>Diseños</td><td>Ilimitados</td><td>Ilimitados</td></tr>
<tr><td>Descuento en productos</td><td>No</td><td>Hasta 33 %</td></tr>
</tbody></table></div>
<h2>Cómo funciona una venta</h2>
<ol>
<li>Un cliente compra tu camiseta en tu tienda (por ejemplo en Etsy) a USD 25.</li>
<li>El pedido pasa a Printify.</li>
<li>Printify te cobra el costo del producto y del envío.</li>
<li>Tu ganancia es lo que queda después del costo de Printify y las comisiones de la tienda donde vendiste.</li>
</ol>
<p>Por eso es clave calcular bien el precio: suma costo de producción, envío, comisiones de la plataforma y lo que quieres ganar.</p>
<h2>Cómo empiezo paso a paso</h2>
<ol>
<li>Crea tu cuenta gratis en <a href="AFF_PRINTIFY">Printify</a>.</li>
<li>Conecta tu tienda (Printify se integra con Etsy, Shopify y otras).</li>
<li>Elige un producto del catálogo y compara proveedores: cambian el precio, la calidad y el tiempo de envío.</li>
<li>Sube tu diseño (hazlo en <a href="PAG:canva-gratis">Canva</a> con fondo transparente si tienes Pro, o en otra herramienta).</li>
<li>Revisa las vistas previas y pide una muestra para ti antes de vender.</li>
<li>Publica el producto en tu tienda con fotos y descripción claras.</li>
</ol>
<h2>Lo que hay que saber antes</h2>
<ol>
<li>El margen es más chico que en productos digitales: cada venta tiene costo de fabricación.</li>
<li>No uses marcas, personajes o frases registradas de otros: las plataformas bajan esos productos.</li>
<li>Premium conviene cuando el descuento en productos supera lo que pagas por mes.</li>
</ol>
<h2>Programas de Printify</h2>
<ol>
<li><strong>Afiliados:</strong> 5 % de las ventas de tus referidos durante 12 meses, cookie de 90 días, pago mensual por PayPal. Inscripción gratis por PartnerStack.</li>
<li><strong>Referidos (para quienes ya venden con Printify):</strong> USD 20 por cada usuario nuevo que se registre con tu enlace y haga al menos tres pedidos.</li>
</ol>""",
    faq=[
        ("¿Printify es gratis?",
         "Sí, el plan Free cuesta USD 0, permite hasta 5 tiendas y diseños ilimitados. Pagas el costo de cada producto cuando se vende."),
        ("¿Necesito comprar inventario?",
         "No. Printify fabrica y envía cada producto solo cuando alguien lo compra."),
        ("¿Puedo usar Printify con Etsy?",
         "Sí, Printify se conecta con Etsy y otras tiendas para recibir los pedidos automáticamente."),
        ("¿Cuándo conviene Printify Premium?",
         "Cuando vendes lo suficiente para que el descuento de hasta 33 % en productos supere la mensualidad (desde USD 24.99 al mes pagando el año)."),
    ],
    fuentes=["printify_precios", "printify_aff"],
)

# ---------------------------------------------------------------- ETSY
PAGINAS["etsy-productos-digitales"] = dict(
    titulo="Etsy para vender productos digitales: lo que cuesta de verdad",
    meta="Cuánto cobra Etsy en 2026: USD 0.20 por publicación, 6.5 % por venta, procesamiento de pago y anuncios externos de 12 a 15 %. Cómo empezar con descargables.",
    h1="Etsy para vender productos digitales: lo que cuesta de verdad",
    pin=("Vender en Etsy:", "lo que cuesta", "de verdad", "tarifas 2026"),
    color=("#a3471b", "#fdf3ec"),
    resumen="Las tarifas reales de Etsy y cómo empezar con descargables.",
    intro="""<p>Etsy no es gratis, pero es barato para empezar: no hay mensualidad y tiene millones de compradores buscando justo productos como los tuyos. Aquí van las tarifas reales y cómo armo una tienda de descargables.</p>""",
    cuerpo="""<h2>Las tarifas de Etsy (vendedores de EE.UU.)</h2>
<ol>
<li><strong>Publicación:</strong> USD 0.20 por producto. Se cobra aunque no se venda y la publicación vence a los cuatro meses (se renueva con otro cargo).</li>
<li><strong>Transacción:</strong> 6.5 % del precio que muestras, más el envío y el envoltorio de regalo si los hay. Para vendedores de EE.UU. no incluye el impuesto de venta.</li>
<li><strong>Procesamiento de pago:</strong> varía según el país de tu cuenta bancaria; está en la política de Etsy Payments.</li>
<li><strong>Anuncios externos (Offsite Ads):</strong> si una venta llega por un anuncio de Etsy fuera de Etsy, pagas 15 % (12 % si vendiste más de USD 10 000 en los últimos 365 días), con un tope de USD 100 por pedido.</li>
</ol>
<h2>Ejemplo con números</h2>
<p>Vendes un planner digital a USD 8. Pagas USD 0.20 de publicación y 6.5 % de transacción (USD 0.52), más el procesamiento de pago. Si la venta vino por un anuncio externo, se suman USD 1.20 (15 %). Usa nuestras calculadoras para hacer la cuenta con tus precios.</p>
<h2>Cómo publico un producto digital en Etsy</h2>
<ol>
<li>Abre tu tienda en <a href="AFF_ETSY">Etsy</a> y configura tu forma de cobro.</li>
<li>Al crear el producto, elige "Digital" como tipo: el comprador descarga el archivo al pagar.</li>
<li>Sube tus archivos (si son muchos, júntalos en un ZIP o en un PDF con enlaces de descarga).</li>
<li>Usa las 13 etiquetas con frases que la gente busca ("planner semanal imprimible", "calendario 2027").</li>
<li>Haz fotos de muestra (mockups) en <a href="PAG:canva-gratis">Canva</a>: muestra el producto impreso o en una tablet.</li>
<li>Escribe en la descripción qué recibe exactamente, en qué tamaño y que no se envía nada físico.</li>
</ol>
<h2>Etsy y Payhip juntos</h2>
<p>Etsy te ayuda a que te descubran; <a href="PAG:payhip-gratis">Payhip</a> cobra menos y te deja tener tu propia lista de clientes. Lo comparo en detalle en <a href="PAG:mejores-herramientas-gratis-vender-productos-digitales-2027">la comparativa</a>.</p>
<h2>Programa de afiliados de Etsy</h2>
<p>Etsy tiene un programa de afiliados gestionado por Rakuten, pensado para blogs y medios (cookie de 30 días), y un "Creator Collective" para creadores en redes con al menos 500 seguidores (cookie de 7 días). Pagan por depósito directo, PayPal o cheque, después de que vence el plazo de devolución del pedido.</p>""",
    faq=[
        ("¿Cuánto cobra Etsy por publicar un producto?",
         "USD 0.20 por publicación. La publicación dura cuatro meses o hasta que se vende."),
        ("¿Cuánto cobra Etsy por venta?",
         "6.5 % de transacción sobre el precio más el envío, más la tarifa de procesamiento de pago. Si la venta vino de un anuncio externo de Etsy, se suma 12 % o 15 % con tope de USD 100."),
        ("¿Se pueden vender productos digitales en Etsy?",
         "Sí. Al crear el producto eliges el tipo digital y el comprador descarga los archivos al pagar."),
        ("¿Me conviene más Etsy o Payhip?",
         "Etsy trae compradores pero cobra más; Payhip cobra 5 % en el plan gratis pero el tráfico lo traes tú. Muchas personas usan los dos."),
    ],
    fuentes=["etsy_fees", "etsy_aff"],
)

# ---------------------------------------------------------------- KDP
PAGINAS["amazon-kdp-gratis"] = dict(
    titulo="Cómo uso Amazon KDP gratis para publicar libros y cuadernos",
    meta="Amazon KDP en español: publicar no cuesta nada. Regalías de 35 % y 70 % en eBook, cómo funcionan los libros de tapa blanda y cómo empezar.",
    h1="Cómo uso Amazon KDP gratis para publicar libros y cuadernos",
    pin=("Publica tu libro", "en Amazon", "GRATIS con KDP", "guía en español"),
    color=("#232f3e", "#fff6e5"),
    resumen="Publica libros, cuadernos y agendas en Amazon sin pagar por publicar.",
    intro="""<p>Kindle Direct Publishing (KDP) es la plataforma de Amazon para publicar libros electrónicos (Kindle) y libros impresos bajo demanda. Abrir la cuenta y publicar no tiene costo: Amazon imprime cada ejemplar cuando alguien lo compra y te paga una regalía.</p>""",
    cuerpo="""<h2>Cómo te pagan: las regalías</h2>
<h3>Libros electrónicos</h3>
<ol>
<li><strong>Opción 35 %:</strong> recibes 35 % del precio de lista sin IVA.</li>
<li><strong>Opción 70 %:</strong> recibes 70 % del precio de lista sin IVA, menos un costo de entrega por el tamaño del archivo (en promedio unos USD 0.06 por copia), en los países que entran en esa opción. Las ventas fuera de esos países pagan 35 %.</li>
<li>Los libros que son principalmente de dominio público solo pueden usar la opción de 35 %.</li>
</ol>
<h3>Libros impresos (tapa blanda)</h3>
<p>En tapa blanda, la regalía se calcula sobre el precio de lista menos el costo de impresión de cada ejemplar. KDP lo explica en su artículo de regalías de tapa blanda; la calculadora de KDP te muestra el número exacto antes de publicar.</p>
<h2>Qué se puede publicar</h2>
<ol>
<li>Libros escritos por ti (novelas, guías, recetarios, libros infantiles).</li>
<li>Cuadernos, agendas y diarios con interior propio ("low content"). Para que se diferencien, diseña un interior útil y original, no una página repetida.</li>
<li>Libros bilingües, de actividades o para colorear con tus propias ilustraciones.</li>
</ol>
<h2>Cómo publico paso a paso</h2>
<ol>
<li>Crea tu cuenta en <a href="AFF_KDP">KDP</a> con tu cuenta de Amazon.</li>
<li>Completa la entrevista de impuestos y los datos de cobro.</li>
<li>Prepara el interior en PDF con el tamaño exacto que elijas (por ejemplo 6 × 9 in) y márgenes de KDP.</li>
<li>Diseña la portada (KDP tiene un creador de portadas, o la haces en <a href="PAG:canva-gratis">Canva</a> con la plantilla de medidas de KDP).</li>
<li>Escribe título, descripción y palabras clave pensando en lo que la gente busca.</li>
<li>Pide una copia de prueba antes de publicar.</li>
</ol>
<h2>Llevar visitas a tu libro</h2>
<p>Amazon trae compradores, pero ayuda que tú también muevas tu libro: pines en <a href="PAG:pinterest-gratis">Pinterest</a>, una página en tu web y tu <a href="PAG:mailerlite-gratis">lista de correo</a>. Si te unes a Amazon Associates, puedes ganar una comisión por las compras que hagan otras personas desde tus enlaces (las compras propias no cuentan). Ojo: Amazon cierra la cuenta de Associates si no generas al menos tres ventas que califiquen en los primeros 180 días.</p>""",
    faq=[
        ("¿Cuesta dinero publicar en Amazon KDP?",
         "No. Abrir la cuenta y publicar es gratis. Amazon se queda con su parte de cada venta y, en libros impresos, descuenta el costo de impresión de tu regalía."),
        ("¿Cuánto paga KDP por un eBook?",
         "35 % del precio de lista sin IVA, o 70 % menos un pequeño costo de entrega en los países que califican para esa opción."),
        ("¿Puedo publicar cuadernos y agendas en KDP?",
         "Sí. Para destacarte, diseña interiores útiles y originales, no páginas repetidas."),
        ("¿Puedo ganar comisión enlazando mi propio libro?",
         "Con Amazon Associates ganas comisión por compras de otras personas que lleguen desde tus enlaces; tus compras propias no cuentan. Necesitas tres ventas que califiquen en los primeros 180 días para mantener la cuenta."),
    ],
    fuentes=["kdp_regalias", "amz_politicas"],
)

# ---------------------------------------------------------------- HOSTING
PAGINAS["hosting-gratis-cloudflare-netlify-github"] = dict(
    titulo="Hosting gratis: Cloudflare Pages, Netlify y GitHub comparados",
    meta="Cómo publicar tu web gratis en 2026: límites reales de Cloudflare Pages, Netlify (300 créditos) y GitHub Pages, y cuál conviene para un negocio.",
    h1="Cómo publico mi web gratis con Cloudflare Pages, Netlify y GitHub",
    pin=("Tu web GRATIS:", "Cloudflare,", "Netlify o GitHub", "cuál conviene"),
    color=("#7a3e00", "#fff4e6"),
    resumen="Publica tu web sin pagar hosting: límites reales de cada opción.",
    intro="""<p>Si tu web es estática (páginas HTML, imágenes y PDFs, sin base de datos), puedes publicarla gratis. Esta misma web está en Cloudflare Pages. Estas son las tres opciones que conozco y sus límites reales.</p>""",
    cuerpo="""<h2>Comparación rápida</h2>
<div class="tabla-scroll"><table>
<thead><tr><th></th><th>Cloudflare Pages</th><th>Netlify (Free)</th><th>GitHub Pages</th></tr></thead>
<tbody>
<tr><td>Costo</td><td>Gratis</td><td>Gratis</td><td>Gratis</td></tr>
<tr><td>Publicaciones</td><td>500 por mes, de a una</td><td>Cuentan dentro de 300 créditos al mes</td><td>Límite suave de 10 por hora (no aplica con GitHub Actions)</td></tr>
<tr><td>Tráfico</td><td>No publica un límite de ancho de banda</td><td>20 créditos por GB, del mismo pozo de 300</td><td>Límite suave de 100 GB al mes</td></tr>
<tr><td>Tamaño</td><td>20 000 archivos; 25 MiB por archivo</td><td>Según créditos</td><td>Sitio de hasta 1 GB</td></tr>
<tr><td>Si te pasas</td><td>—</td><td>El sitio se pausa hasta el mes siguiente (no te cobran)</td><td>Pueden limitar el sitio</td></tr>
<tr><td>Uso comercial</td><td>Sí</td><td>Sí</td><td>No para negocios o tiendas</td></tr>
</tbody></table></div>
<h2>Mi elección: GitHub para guardar, Cloudflare para publicar</h2>
<ol>
<li>Guardo el código de la web en un repositorio de <a href="AFF_GITHUB">GitHub</a> (gratis): queda un historial de cada cambio.</li>
<li>Conecto ese repositorio a <a href="AFF_CLOUDFLARE">Cloudflare Pages</a>: cada vez que subo un cambio, la web se publica sola.</li>
<li>Uso un dominio propio o el subdominio gratis .pages.dev.</li>
</ol>
<p>GitHub Pages es excelente para proyectos personales, pero sus reglas no permiten alojar un negocio, una tienda o un SaaS comercial, así que para una web con anuncios o ventas prefiero Cloudflare Pages o Netlify.</p>
<h2>Cuándo uso Netlify</h2>
<p><a href="AFF_NETLIFY">Netlify</a> es muy fácil (puedes arrastrar una carpeta para publicar) y trae formularios. Desde su cambio a créditos, el plan gratis tiene 300 créditos al mes para publicaciones, tráfico, formularios y funciones. Si el sitio llega al límite, se pausa hasta el siguiente ciclo; te avisan al 50 %, 75 % y 100 %. Para sitios con mucho tráfico, eso lo vuelve menos práctico que Cloudflare.</p>
<h2>Automatizaciones gratis que se pueden sumar</h2>
<ol>
<li>GitHub Actions puede correr tareas programadas (por ejemplo, revisar que los enlaces sigan funcionando cada mes).</li>
<li>Un feed RSS generado por tu web puede alimentar <a href="PAG:pinterest-gratis">Pinterest</a> sin trabajo manual.</li>
<li>Con <a href="PAG:google-analytics-4-gratis">Google Analytics 4</a> mides qué páginas traen visitas.</li>
</ol>
<h2>Programas de afiliados</h2>
<p>Netlify tiene un programa de socios en PartnerStack: según su ficha, los socios del nivel inicial ganan 20 % durante 12 meses por clientes nuevos de autoservicio, y la aceptación es a criterio de Netlify. No encontramos programas de afiliados de Cloudflare ni de GitHub.</p>""",
    faq=[
        ("¿Cuál es el mejor hosting gratis para una web de negocio?",
         "Para una web estática con anuncios o ventas, Cloudflare Pages o Netlify. GitHub Pages no permite alojar negocios ni tiendas."),
        ("¿Cuánto tráfico permite Cloudflare Pages gratis?",
         "Su página de límites no publica un tope de ancho de banda para el plan gratis. Sí limita 500 publicaciones al mes, 20 000 archivos y 25 MiB por archivo."),
        ("¿Qué pasa si me paso del plan gratis de Netlify?",
         "El plan gratis tiene límites fijos: no te cobran, pero el sitio se pausa hasta el siguiente ciclo mensual."),
        ("¿Necesito saber programar?",
         "No para publicar una web hecha con un generador o una plantilla HTML. Para cambios avanzados ayuda saber algo de HTML."),
    ],
    fuentes=["cf_limites", "netlify_precios", "gh_limites"],
)

# ---------------------------------------------------------------- GA4
PAGINAS["google-analytics-4-gratis"] = dict(
    titulo="Cómo uso Google Analytics 4 gratis para saber qué funciona",
    meta="Google Analytics 4 en español: instalarlo en tu web, cambiar la retención a 14 meses, ver de dónde vienen tus visitas y qué páginas venden.",
    h1="Cómo uso Google Analytics 4 gratis para saber qué funciona",
    pin=("Google Analytics 4", "GRATIS", "para saber", "qué funciona"),
    color=("#a15c00", "#fff8ec"),
    resumen="Mide de dónde vienen tus visitas y qué páginas funcionan.",
    intro="""<p>Sin datos, todo es adivinar. Google Analytics 4 (GA4) es gratis y te dice cuánta gente entra a tu web, de dónde viene (Google, Pinterest, correo) y qué hace. Así sabes en qué vale la pena poner tu tiempo.</p>""",
    cuerpo="""<h2>Cómo lo instalo</h2>
<ol>
<li>Entra a <a href="AFF_GA4">Google Analytics</a> con tu cuenta de Google y crea una propiedad para tu web.</li>
<li>Crea un "flujo de datos web" con la dirección de tu sitio.</li>
<li>Copia la etiqueta de Google (empieza con G-) y pégala en el &lt;head&gt; de todas tus páginas.</li>
<li>Abre tu web y revisa en "Tiempo real" que aparezca tu visita.</li>
</ol>
<h2>Primer ajuste: retención de 14 meses</h2>
<p>Por defecto, GA4 guarda los datos detallados (los que usan las exploraciones y embudos) solo 2 meses. En las propiedades gratis puedes subirlo a <strong>14 meses</strong>: Administrar → Configuración de datos → Retención de datos. Los informes estándar no se ven afectados, pero para comparar temporadas (como enero contra enero) necesitas los 14 meses. Si lo subes, se aplica también a los datos que ya tienes.</p>
<h2>Los 4 informes que miro</h2>
<ol>
<li><strong>Adquisición de tráfico:</strong> de dónde llegan las visitas (búsqueda orgánica, Pinterest, correo, directo).</li>
<li><strong>Páginas y pantallas:</strong> qué páginas tienen más visitas y cuánto tiempo se quedan.</li>
<li><strong>Eventos:</strong> clics en botones de descarga o en enlaces a tu tienda.</li>
<li><strong>Tiempo real:</strong> para comprobar que un pin o un correo nuevo está trayendo gente.</li>
</ol>
<h2>Etiqueta tus enlaces</h2>
<p>Agrega parámetros UTM a los enlaces que pones en Pinterest, en tus correos de <a href="PAG:mailerlite-gratis">MailerLite</a> o en tus redes (por ejemplo ?utm_source=pinterest&amp;utm_medium=social). Así GA4 te muestra qué canal trae cada visita.</p>
<h2>Privacidad</h2>
<p>Si usas GA4 o anuncios, tu web necesita una política de privacidad que lo explique. Si recibes visitas de Europa o de estados con leyes de privacidad propias (como California), revisa si necesitas un aviso de cookies.</p>
<h2>¿Tiene programa de afiliados?</h2>
<p>No. Google Analytics es gratis y no tiene programa de afiliados; está en esta guía porque es la herramienta que usamos para medir.</p>""",
    faq=[
        ("¿Google Analytics 4 es gratis?",
         "Sí. La versión estándar es gratis. La versión de pago (Analytics 360) es para empresas grandes."),
        ("¿Cuánto tiempo guarda los datos GA4?",
         "En la versión gratis puedes elegir 2 o 14 meses para los datos detallados. Te conviene cambiarlo a 14 meses."),
        ("¿Cómo sé si mis visitas vienen de Pinterest?",
         "En el informe de Adquisición de tráfico. Para más precisión, agrega parámetros UTM a tus enlaces."),
        ("¿Necesito avisar que uso Google Analytics?",
         "Sí, tu política de privacidad debe explicarlo. Según de dónde vengan tus visitas, también puedes necesitar un aviso de cookies."),
    ],
    fuentes=["ga4_ret"],
)
