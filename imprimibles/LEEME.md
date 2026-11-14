# Imprimibles automáticos (tanda 1)

Tres paquetes de imprimibles gratis que se generan solos con código (Python, SVG y PDF). No se usó IA para hacer imágenes: todo son figuras geométricas dibujadas por programa. Ganan plata con los anuncios (AdSense) y con los links de Amazon, y se mueven solos a Pinterest por RSS.

Regla de goteo (la tuya del 14 nov): nunca sale todo junto. Colorear y fichas publican 2 o 3 cosas nuevas por día con `goteo.py`; el juego del día sale de a uno por día.

## 1. Qué hay en esta carpeta

1. `colorear/`: un **sitio web propio y completo** de páginas para colorear, que va a Cloudflare Pages (no va dentro de Handy Calcs). Tiene inicio, 4 categorías (mandalas, animales, patrones geométricos, paisajes), una página por lámina, Acerca de, Privacidad, Cookies (con aviso de cookies), 404, `sitemap.xml`, `robots.txt`, `_headers`, `rss.xml` general (con goteo), un RSS por categoría (`rss-mandalas.xml`, `rss-animales.xml`, `rss-geometricos.xml`, `rss-paisajes.xml`) y `rss-completo.xml` (la cola entera). Primera tanda: 20 láminas, cada una en SVG, PDF carta y PNG 1000x1500 para Pinterest.
2. `juego-del-dia/`: va dentro de Handy Calcs. Cada día trae 3 sudokus (fácil, medio y difícil, todos con solución única comprobada) y una sopa de letras con tema en español. Se juega en pantalla (con botones de comprobar y ver solución) y también hay un PDF de 2 páginas: la 1 con los juegos y la 2 con las soluciones. Hay 31 días listos, del 17 nov al 17 dic de 2026, con archivo por mes, `rss.xml` y `sitemap.xml`.
3. `fichas-bilingues/`: va dentro de Handy Calcs. Son fichas español–inglés para chicos de 3 a 7 años: colores, números del 1 al 20 para repasar y contar, animales (con su sonido en los dos idiomas) y letras de la A a la Z con la Ñ. Primera tanda: 20 PDF con su vista previa. El catálogo base trae 76 fichas; cuando se terminan, sigue sola con fichas de repaso del tipo "une con flechas" (no se acaban nunca). Incluye `rss.xml` (con goteo), `rss-completo.xml` y `sitemap.xml`.
4. `index.html` (en la raíz): portada `/imprimibles/` de Handy Calcs, que junta el juego del día y las fichas.
5. `generar.py` y `motor/`: el programa que hace todo. `goteo.py` es una copia del de `ideas-tanda1/goteo/`.
6. `_datos/`: la lista de lo que ya se generó (no se sube a ningún sitio).
7. `config.json`: el único lugar donde se cambian el nombre y la URL del sitio de colorear, el dominio de Handy Calcs, los links de Amazon y el día 1 del goteo.
8. `.github/workflows/imprimibles-diario.yml`: el ejemplo de GitHub Actions que corre todo solo.
9. `requirements.txt`: lo que necesita Python (cairosvg, pypdf, pillow).

## 2. Cómo se enchufa en las webs

### Handy Calcs (Netlify)

1. Revisá en `config.json` que `base_url` sea la URL real (`https://handycalcs.com/imprimibles` lo puse por suposición). Si cambia, corré `python3 generar.py reconstruir`.
2. Subí al sitio, dentro de la carpeta `/imprimibles/`: `index.html`, `juego-del-dia/` y `fichas-bilingues/`. Sin `colorear/`, `_datos/` ni el código.
3. Reemplazá en todos los HTML los marcadores `<!-- GA4 -->` y `<!-- ADSENSE -->` por los códigos que ya usa Handy Calcs. Lo ideal es hacerlo en `motor/comun.py` (función `pagina_html`) para que lo nuevo también salga con los códigos.
4. Poné el link de afiliado de Amazon en `config.json` (`link_amazon_juegos` y `link_amazon_fichas`) y corré `python3 generar.py reconstruir`.
5. Sumá `juego-del-dia/sitemap.xml` y `fichas-bilingues/sitemap.xml` al sitemap de Handy Calcs, o cargalos aparte en Google Search Console.
6. Agregá un link a `/imprimibles/` en el menú de Handy Calcs.

### Sitio de colorear (Cloudflare Pages)

1. Elegí el nombre y el dominio y cargalos en `config.json` (`SITE_NAME`, `SITE_URL`, `email_contacto`). Después corré `python3 generar.py reconstruir`. Hoy todo dice `SITE_NAME` y `https://SITE_URL` a propósito.
2. En Cloudflare Pages, creá un proyecto y publicá la carpeta `colorear/` como raíz del sitio. Los links son absolutos (`/archivos/...`), así que las imágenes solo se ven bien publicadas como raíz y no abriendo el archivo suelto.
3. Reemplazá los marcadores `<!-- GA4 -->`, `<!-- ADSENSE -->` y `<!-- META_PIXEL -->` (están en `motor/comun.py`).
4. Cargá el link de Amazon en `link_amazon_colorear`.
5. Cargá `SITE_URL/sitemap.xml` en Google Search Console.
6. AdSense pide un dominio propio, las páginas de Privacidad y Contacto (ya están) y algo de contenido. Conviene pedirlo cuando haya unas 30 o 40 láminas publicadas.

### 3 ideas de nombre para el sitio de colorear

1. **Pintamundo**: corto, fácil de recordar y sirve para chicos y grandes.
2. **Colorea Fácil**: dice exactamente lo que es y ayuda en Google ("colorear fácil").
3. **Láminas Libres**: suena a "gratis para imprimir" y deja lugar para sumar otras cosas más adelante.

Antes de elegir, fijate que el dominio .com esté libre.

## 3. Pinterest (por RSS)

1. En Pinterest Business, andá a Configuración, después a "Publicación masiva" y agregá un RSS por tablero:
2. El tablero "Páginas para colorear" usa `SITE_URL/rss.xml` (o un tablero por categoría con `rss-mandalas.xml`, `rss-animales.xml`, etc.).
3. El tablero "Sudoku y sopa de letras" usa `https://handycalcs.com/imprimibles/juego-del-dia/rss.xml`.
4. El tablero "Fichas bilingües para niños" usa `https://handycalcs.com/imprimibles/fichas-bilingues/rss.xml`.
5. Cada ítem trae la imagen de 1000x1500, el título y la descripción. Pinterest revisa el RSS una vez por día y publica solo lo nuevo.
6. No le pases a Pinterest los `rss-completo.xml`: son la cola entera y saldría todo junto.

## 4. Horarios y automatización

1. **Todos los días a las 8 de Utah** (15:00 UTC; el GitHub Action de ejemplo): `python3 generar.py diario`, que hace esto:
2. Arma los juegos que falten para tener siempre 30 días por delante y publica el del día.
3. Rellena la cola de colorear y de fichas para que siempre haya 7 días de material listo. En la práctica son unas 2 o 3 láminas y 2 o 3 fichas por día, o sea unas 17 por semana de cada una. Esto reemplaza el "5 a 10 por semana" del pedido original: con la regla del goteo (2 o 3 por día), si se generara una vez por semana la cola se vaciaría y después saldría todo de golpe.
4. Rehace los índices, el sitemap y los RSS. `goteo.py` arma el `rss.xml` público. Las páginas que todavía no salieron existen, pero no están enlazadas, no aparecen en el sitemap y llevan `noindex`.
5. El Action commitea los cambios y publica `colorear/` en Cloudflare Pages con `wrangler-action`. Para Handy Calcs, si Netlify está conectado al mismo repo, se publica solo con el commit.
6. Para que el Action funcione hay que crear un repo en GitHub y cargarle los secrets `CLOUDFLARE_API_TOKEN` y `CLOUDFLARE_ACCOUNT_ID` y la variable `CF_PAGES_PROJECT`. No subí ni activé nada.
7. `python3 generar.py semanal --cantidad 7`: es opcional y suma 7 más a la cola de cada paquete (sirve para adelantar).
8. `python3 generar.py descartar colorear 7`: si una lámina salió fea, la saca y no la vuelve a usar.
9. `--hoy AAAA-MM-DD`: sirve para simular una fecha (la carpeta que te dejo está armada como si hoy fuera el 17 nov: hay 2 láminas, 2 fichas y 1 juego publicados).
10. Correrlo dos veces el mismo día no duplica nada (lo probé).

## 5. Diez textos de pin por paquete

Los pines están en español neutro (igual que las webs) para llegar a más gente.

### Páginas para colorear

1. Mandalas para colorear gratis: imprime el PDF y relájate un rato 🧘
2. Dibujos de animales para colorear para niños: líneas gruesas, PDF gratis.
3. Patrones geométricos antiestrés para colorear. Descarga gratis en PDF.
4. Paisaje de montaña para colorear: pinos, lago y sol. Imprimible gratis.
5. ¿Tarde de lluvia? Páginas para colorear gratis para toda la familia.
6. Mandala nuevo cada semana, gratis para imprimir en tamaño carta.
7. Gato para colorear con su nombre en letras grandes: ideal para preescolar.
8. Láminas para colorear para adultos: mosaicos y ondas para desconectar.
9. Actividad para el aula: dibujos para colorear gratis, listos para imprimir.
10. Guarda este pin: cientos de páginas para colorear gratis en PDF.

### Juego del día (sudoku y sopa de letras)

1. Sudoku del día gratis: fácil, medio y difícil, con soluciones en PDF.
2. Sopa de letras en español para imprimir: un tema nuevo cada día.
3. Ejercita la mente: sudoku y sopa de letras diarios, gratis.
4. Juegos de palabras para adultos mayores: imprime la sopa de letras del día.
5. Sudoku para principiantes: empieza por el fácil y anímate al difícil.
6. Sopa de letras de Navidad gratis para imprimir 🎄
7. Juego del día para el café de la mañana: sudoku + sopa de letras.
8. Actividad para la clase de español: sopa de letras temática gratis.
9. Sudoku online o en papel: juégalo en el celular o imprímelo con soluciones.
10. Un juego nuevo cada día, gratis. Guarda el pin y vuelve mañana.

### Fichas bilingües español–inglés

1. Fichas bilingües para niños: aprende los colores en español e inglés.
2. Números del 1 al 20 para repasar: uno / one, dos / two… PDF gratis.
3. Letras para repasar de la A a la Z (¡con la Ñ!) en español e inglés.
4. Animales en inglés para niños: colorea, repasa y aprende el sonido.
5. Hojas de trabajo gratis para preescolar bilingüe (3 a 7 años).
6. Homeschool bilingüe: fichas imprimibles gratis de español e inglés.
7. Une cada animal con su nombre en inglés: ficha de repaso gratis.
8. Material para maestras de dual language: fichas gratis en PDF.
9. Aprender inglés jugando: colorear y repasar palabras, gratis.
10. Free Spanish–English worksheets for kids: colors, numbers, animals.

## 6. Lo que no salió del todo bien o hay que revisar

1. Los mandalas con 8 pétalos de afuera tienen pétalos un poco "gorditos", con forma de escudo. Se ven bien para colorear, pero son menos finos que un mandala hecho a mano.
2. Los paisajes son lindos pero bastante parecidos entre sí: siempre hay montañas, sol, nubes y pinos, y lo único que cambia es si hay lago o pradera.
3. Los animales son simples, para chicos. No sirven para adultos que buscan dibujos detallados.
4. Las letras para repasar son letras con contorno punteado (se repasa el borde). No son las letras de "una sola línea" de los cuadernos escolares, porque no hay una fuente así instalada.
5. Algunas fichas de letras no traen dibujo (por ejemplo V de vaca, K de koala, X de xilófono) porque ese objeto no está dibujado. En esas el espacio queda vacío.
6. La dificultad del sudoku se mide de forma aproximada: el fácil y el medio se resuelven sin adivinar y el difícil necesita más técnica. No es una escala profesional.
7. `goteo.py` reescribe el XML, así que la descripción del RSS pierde el `CDATA` (queda escapada). Sigue siendo válido y Pinterest toma la imagen de `enclosure` y de `media:content`.
8. El dominio de Handy Calcs y el nombre del sitio de colorear son suposiciones o marcadores: revisalos en `config.json` antes de publicar.
9. Los textos públicos de las webs están en español neutro ("Descarga", "Imprime") para llegar a más gente. Las palabras de las sopas de letras también se pasaron a neutro (fresa, piña, autobús).
