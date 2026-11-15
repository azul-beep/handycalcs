# -*- coding: utf-8 -*-
"""Online tools (QR, images, text, random pickers, password, timer) for Handy Calcs.
English pages live at /tools/<slug>/ and Spanish pages at /es/herramientas/<slug>/.
"n" is the release order: build.py publishes tools 1-2 on TOOLS_START and then one more tool per day (EN + ES),
so the section grows by itself every morning with the daily GitHub Action, without Claude.
The widgets run 100% in the visitor's browser (src/tools.js): no text, image or name ever leaves the device."""
import html
E = html.escape

def t(lang, en, es):
    return en if lang == "en" else es

# ------------------------------------------------------------------ widget markup per engine
def _qr(mode, lang):
    if mode == "wifi":
        fields = f"""<div class="row"><div><label>{t(lang,'Network name (SSID)','Nombre de la red (SSID)')}</label><input data-k="ssid" value="" placeholder="MyHomeWiFi" autocomplete="off"></div>
<div><label>{t(lang,'Password','Contraseña')}</label><input data-k="pass" value="" autocomplete="off"></div>
<div><label>{t(lang,'Security','Seguridad')}</label><select data-k="sec"><option value="WPA">WPA / WPA2 / WPA3</option><option value="WEP">WEP</option><option value="nopass">{t(lang,'None (open)','Ninguna (abierta)')}</option></select></div></div>
<label class="chk"><input type="checkbox" data-k="hidden"> {t(lang,'Hidden network','Red oculta')}</label>"""
    elif mode == "whatsapp":
        fields = f"""<div class="row"><div><label>{t(lang,'Phone with country code','Teléfono con código de país')}</label><input data-k="phone" inputmode="tel" placeholder="{t(lang,'1 801 555 0123','52 55 1234 5678')}"></div></div>
<label>{t(lang,'Message that appears ready to send (optional)','Mensaje que aparece listo para enviar (opcional)')}</label><textarea data-k="msg" rows="3" style="min-height:80px">{t(lang,'Hi! I saw your QR code and I have a question.','¡Hola! Vi tu código QR y tengo una consulta.')}</textarea>"""
    else:
        fields = f"""<label>{t(lang,'Link or text','Enlace o texto')}</label><textarea data-k="text" rows="3" style="min-height:80px">https://</textarea>"""
    return f"""{fields}
<div class="row"><div><label>{t(lang,'Size','Tamaño')}</label><select data-k="size"><option value="200">200 px</option><option value="300" selected>300 px</option><option value="600">600 px</option><option value="1000">1000 px ({t(lang,'print','imprimir')})</option></select></div>
<div><label>{t(lang,'Color','Color')}</label><input type="color" data-k="fg" value="#000000"></div><div><label>{t(lang,'Background','Fondo')}</label><input type="color" data-k="bg" value="#ffffff"></div></div>
<div class="qr-out" aria-live="polite"></div>
<div class="acts"><button type="button" class="btn" data-act="png">{t(lang,'Download PNG','Descargar PNG')}</button><button type="button" class="btn-ghost" data-act="svg">{t(lang,'Download SVG (vector)','Descargar SVG (vector)')}</button></div>"""

def _words(mode, lang):
    return f"""<div class="two"><div><label for="wc-in">{t(lang,'Type or paste your text','Escribe o pega tu texto')}</label><textarea id="wc-in" rows="12"></textarea></div>
<div><div class="stats" aria-live="polite"></div><div class="kw"></div></div></div>"""

def _textx(mode, lang):
    opts = ""
    if mode == "case":
        b = [("upper", "UPPERCASE", "MAYÚSCULAS"), ("lower", "lowercase", "minúsculas"), ("title", "Title Case", "Tipo Título"),
             ("sentence", "Sentence case", "Tipo oración"), ("alt", "aLtErNaTiNg", "aLtErNaDo"), ("invert", "iNVERT", "iNVERTIR")]
        opts = '<div class="chips" role="group">%s</div>' % "".join('<button type="button" class="chip%s" data-case="%s">%s</button>' % (" on" if i == 0 else "", k, t(lang, en, es)) for i, (k, en, es) in enumerate(b))
    if mode == "accents":
        opts = f'<label class="chk"><input type="checkbox" data-k="keepn" checked> {t(lang,"Keep ñ and Ñ","Mantener la ñ y la Ñ")}</label>'
    if mode == "breaks":
        opts = f"""<div class="row"><div><label>{t(lang,'What to do','Qué hacer')}</label><select data-k="how"><option value="all">{t(lang,'Remove all line breaks (one line)','Quitar todos los saltos (una sola línea)')}</option>
<option value="para">{t(lang,'Keep paragraphs, join the lines inside them','Mantener párrafos y unir las líneas de adentro')}</option><option value="empty">{t(lang,'Only remove empty lines','Solo quitar líneas vacías')}</option></select></div></div>
<label class="chk"><input type="checkbox" data-k="spaces" checked> {t(lang,'Also remove double spaces','Quitar también los espacios dobles')}</label>"""
    return f"""{opts}<div class="two"><div><label>{t(lang,'Your text','Tu texto')}</label><textarea data-k="in" rows="10"></textarea></div>
<div><label>{t(lang,'Result','Resultado')}</label><textarea data-k="out" rows="10" readonly></textarea></div></div>
<div class="acts"><button type="button" class="btn" data-act="copy">{t(lang,'Copy result','Copiar resultado')}</button></div>"""

def _lorem(mode, lang):
    return f"""<div class="row"><div><label>{t(lang,'How many','Cuántos')}</label><input type="number" data-k="n" value="3" min="1" max="50"></div>
<div><label>{t(lang,'Of what','De qué')}</label><select data-k="unit"><option value="paragraphs">{t(lang,'Paragraphs','Párrafos')}</option><option value="sentences">{t(lang,'Sentences','Oraciones')}</option><option value="words">{t(lang,'Words (x10)','Palabras (x10)')}</option></select></div>
<div><label>{t(lang,'Language','Idioma')}</label><select data-k="lang"><option value="latin">Lorem ipsum ({t(lang,'Latin','latín')})</option><option value="es"{'' if lang == 'en' else ' selected'}>{t(lang,'Spanish placeholder','Español')}</option></select></div></div>
<label class="chk"><input type="checkbox" data-k="start" checked> {t(lang,'Start with "Lorem ipsum dolor sit amet"','Empezar con "Lorem ipsum dolor sit amet"')}</label>
<div class="acts"><button type="button" class="btn" data-act="gen">{t(lang,'Generate again','Generar otro')}</button><button type="button" class="btn-ghost" data-act="copy">{t(lang,'Copy','Copiar')}</button></div>
<textarea data-k="out" rows="10" readonly></textarea>"""

def _img(mode, lang):
    fmt = f"""<div><label>{t(lang,'Save as','Guardar como')}</label><select data-k="format">{'<option value="keep">' + t(lang,'Same format','Mismo formato') + '</option>' if mode != 'convert' else ''}<option value="image/jpeg"{' selected' if mode == 'convert' else ''}>JPG</option><option value="image/png">PNG</option><option value="image/webp">WebP</option></select></div>"""
    if mode == "compress":
        ctl = f"""<div class="row"><div><label>{t(lang,'Quality','Calidad')}: <span class="qv">75%</span></label><input type="range" data-k="quality" min="10" max="95" value="75"></div>
<div><label>{t(lang,'Max size in KB (optional)','Peso máximo en KB (opcional)')}</label><input type="number" data-k="target" min="10" placeholder="{t(lang,'e.g. 100','ej. 100')}"></div>
<div><label>{t(lang,'Max width (px, optional)','Ancho máximo (px, opcional)')}</label><input type="number" data-k="maxw" min="50" placeholder="1920"></div>{fmt}</div>"""
    elif mode == "resize":
        sizes = [("1080x1080", "Instagram post"), ("1080x1350", "Instagram 4:5"), ("1080x1920", t(lang, "Story / Reel / TikTok", "Historia / Reel / TikTok")),
                 ("1200x630", t(lang, "Facebook / link preview", "Facebook / vista de enlace")), ("820x312", t(lang, "Facebook cover", "Portada de Facebook")),
                 ("1280x720", t(lang, "YouTube thumbnail", "Miniatura de YouTube")), ("1000x1500", "Pinterest pin"), ("1500x500", t(lang, "X / Twitter header", "Portada de X / Twitter"))]
        ctl = f"""<div class="chips" role="group">{''.join('<button type="button" class="chip" data-size="%s">%s · %s</button>' % (s, E(n), s.replace('x', '×')) for s, n in sizes)}</div>
<div class="row"><div><label>{t(lang,'Width (px)','Ancho (px)')}</label><input type="number" data-k="w" min="1" placeholder="{t(lang,'auto','auto')}"></div>
<div><label>{t(lang,'Height (px)','Alto (px)')}</label><input type="number" data-k="h" min="1" placeholder="{t(lang,'auto','auto')}"></div>
<div><label>{t(lang,'Or scale (%)','O escala (%)')}</label><input type="number" data-k="pct" min="1" max="400" placeholder="50"></div>
<div><label>{t(lang,'If both are set','Si pones los dos')}</label><select data-k="fit"><option value="cover">{t(lang,'Crop to fill','Recortar para llenar')}</option><option value="contain">{t(lang,'Fit inside (add margins)','Encajar (con márgenes)')}</option><option value="stretch">{t(lang,'Stretch','Estirar')}</option></select></div>{fmt}</div>
<input type="hidden" data-k="quality" value="92"><span class="qv" hidden></span>"""
    else:
        ctl = f"""<div class="row">{fmt}<div><label>{t(lang,'Quality (JPG/WebP)','Calidad (JPG/WebP)')}: <span class="qv">90%</span></label><input type="range" data-k="quality" min="10" max="100" value="90"></div></div>"""
    return f"""{ctl}
<label class="drop">{t(lang,'Choose images or drop them here','Elige imágenes o suéltalas aquí')}<br><span class="small">JPG · PNG · WebP · GIF · {t(lang,'up to 30 at a time','hasta 30 a la vez')}</span><input type="file" accept="image/*" multiple></label>
<div class="acts"><button type="button" class="btn-ghost" data-act="redo">{t(lang,'Apply new settings','Aplicar los cambios')}</button></div>
<div class="img-list" aria-live="polite"></div>"""

def _wheel(mode, lang):
    names = t(lang, "Emma\nLiam\nOlivia\nNoah\nAva\nLucas\nMia\nEthan", "Sofía\nMateo\nValentina\nSantiago\nIsabella\nSebastián\nCamila\nDiego")
    return f"""<div class="wheel-wrap"><div><label for="wh-in">{t(lang,'Names (one per line)','Nombres (uno por línea)')}</label><textarea id="wh-in" rows="10">{names}</textarea>
<label class="chk"><input type="checkbox" data-k="remove"> {t(lang,'Remove the winner after each spin','Quitar al ganador después de cada giro')}</label>
<div class="acts"><button type="button" class="btn" data-act="spin">{t(lang,'Spin the wheel','Girar la ruleta')}</button><button type="button" class="btn-ghost" data-act="shuffle">{t(lang,'Shuffle','Mezclar')}</button></div></div>
<div><canvas width="600" height="600" aria-label="{t(lang,'Name wheel','Ruleta de nombres')}"></canvas><div class="wheel-res" aria-live="polite"></div></div></div>"""

def _teams(mode, lang):
    names = t(lang, "Emma\nLiam\nOlivia\nNoah\nAva\nLucas\nMia\nEthan\nChloe\nJames", "Sofía\nMateo\nValentina\nSantiago\nIsabella\nSebastián\nCamila\nDiego\nLucía\nNicolás")
    return f"""<div class="two"><div><label for="tm-in">{t(lang,'Names (one per line)','Nombres (uno por línea)')}</label><textarea id="tm-in" rows="10">{names}</textarea></div>
<div><div class="row"><div><label>{t(lang,'Split by','Dividir por')}</label><select data-k="by"><option value="teams">{t(lang,'Number of teams','Cantidad de equipos')}</option><option value="size">{t(lang,'People per team','Personas por equipo')}</option></select></div>
<div><label>{t(lang,'How many','Cuántos')}</label><input type="number" data-k="n" value="2" min="1"></div></div>
<div class="acts"><button type="button" class="btn" data-act="go">{t(lang,'Make teams','Armar equipos')}</button><button type="button" class="btn-ghost" data-act="copy">{t(lang,'Copy teams','Copiar equipos')}</button></div></div></div>
<div class="teams-out" aria-live="polite"></div>"""

def _giveaway(mode, lang):
    ex = t(lang, "@maria_bakes love this! @ana @luis\n@joe.climbs count me in @sam\n@maria_bakes again! @pat\n@lucy_k 😍 @tom @kim",
           "@maria_reposteria ¡me encanta! @ana @luis\n@joe.escala yo participo @sam\n@maria_reposteria otra vez @pat\n@lucia_k 😍 @tomas @kim")
    return f"""<label for="gv-in">{t(lang,'Paste the comments or names (one per line)','Pega los comentarios o nombres (uno por línea)')}</label><textarea id="gv-in" data-k="entries" rows="9">{E(ex)}</textarea>
<div class="row"><div><label>{t(lang,'Winners','Ganadores')}</label><input type="number" data-k="winners" value="1" min="1"></div>
<div><label>{t(lang,'Alternates','Suplentes')}</label><input type="number" data-k="alts" value="1" min="0"></div>
<div><label>{t(lang,'Minimum tagged friends','Mínimo de amigos etiquetados')}</label><input type="number" data-k="tags" value="0" min="0"></div>
<div><label>{t(lang,'Exclude (one per line)','Excluir (uno por línea)')}</label><textarea data-k="exclude" rows="2" style="min-height:44px" placeholder="@yourshop"></textarea></div></div>
<label class="chk"><input type="checkbox" data-k="unique" checked> {t(lang,'One entry per person (remove duplicates)','Una participación por persona (quitar repetidos)')}</label>
<div class="acts"><button type="button" class="btn" data-act="go">{t(lang,'Pick the winner','Elegir ganador')}</button></div>
<div class="give-out" aria-live="polite"></div>"""

def _randnum(mode, lang):
    return f"""<div class="row"><div><label>{t(lang,'Minimum','Mínimo')}</label><input type="number" data-k="min" value="1"></div><div><label>{t(lang,'Maximum','Máximo')}</label><input type="number" data-k="max" value="100"></div>
<div><label>{t(lang,'How many numbers','Cuántos números')}</label><input type="number" data-k="n" value="1" min="1" max="1000"></div></div>
<label class="chk"><input type="checkbox" data-k="unique" checked> {t(lang,'No repeats','Sin repetir')}</label><label class="chk"><input type="checkbox" data-k="sort"> {t(lang,'Sort from low to high','Ordenar de menor a mayor')}</label>
<div class="acts"><button type="button" class="btn" data-act="go">{t(lang,'Generate','Generar')}</button></div><div class="rn-out" aria-live="polite"></div>"""

def _coin(mode, lang):
    return f"""<div class="coin" aria-hidden="true">$</div><div class="coin-res" aria-live="polite"></div>
<div class="acts" style="justify-content:center"><button type="button" class="btn" data-act="go">{t(lang,'Flip the coin','Lanzar la moneda')}</button></div><p class="coin-hist"></p>"""

def _dice(mode, lang):
    return f"""<div class="row"><div><label>{t(lang,'Number of dice','Cantidad de dados')}</label><input type="number" data-k="n" value="2" min="1" max="10"></div>
<div><label>{t(lang,'Sides','Caras')}</label><select data-k="sides"><option value="4">d4</option><option value="6" selected>d6</option><option value="8">d8</option><option value="10">d10</option><option value="12">d12</option><option value="20">d20</option><option value="100">d100</option></select></div></div>
<div class="acts"><button type="button" class="btn" data-act="go">{t(lang,'Roll','Lanzar')}</button></div><div class="dice-out" aria-live="polite"></div><p class="dice-total"></p>"""

def _password(mode, lang):
    return f"""<div class="row"><div><label>{t(lang,'Length','Largo')}: <span class="lv">16</span></label><input type="range" data-k="len" min="6" max="64" value="16"></div>
<div><label>{t(lang,'How many','Cuántas')}</label><input type="number" data-k="count" value="3" min="1" max="10"></div></div>
<label class="chk"><input type="checkbox" data-k="lower" checked> abc</label><label class="chk"><input type="checkbox" data-k="upper" checked> ABC</label>
<label class="chk"><input type="checkbox" data-k="digits" checked> 123</label><label class="chk"><input type="checkbox" data-k="symbols" checked> !@#$</label>
<label class="chk"><input type="checkbox" data-k="ambig"> {t(lang,'Avoid look-alike characters (I, l, 1, O, 0)','Evitar caracteres parecidos (I, l, 1, O, 0)')}</label>
<div class="acts"><button type="button" class="btn" data-act="go">{t(lang,'New passwords','Nuevas contraseñas')}</button></div><div class="pw-out" aria-live="polite"></div>"""

def _timer(mode, lang):
    return f"""<div class="chips" role="group"><button type="button" class="chip on" data-mode-btn="down">{t(lang,'Timer','Temporizador')}</button><button type="button" class="chip" data-mode-btn="up">{t(lang,'Stopwatch','Cronómetro')}</button></div>
<div class="t-set"><div class="row"><div><label>{t(lang,'Hours','Horas')}</label><input type="number" data-k="h" value="0" min="0"></div><div><label>{t(lang,'Minutes','Minutos')}</label><input type="number" data-k="m" value="5" min="0"></div><div><label>{t(lang,'Seconds','Segundos')}</label><input type="number" data-k="s" value="0" min="0" max="59"></div></div>
<div class="chips" role="group">{''.join('<button type="button" class="chip" data-min="%d">%d min</button>' % (m, m) for m in (1, 2, 3, 5, 10, 15, 20, 25, 30, 45, 60))}</div></div>
<div class="t-box"><div class="t-disp" aria-live="off">05:00</div></div>
<div class="acts"><button type="button" class="btn" data-act="start">{t(lang,'Start','Iniciar')}</button><button type="button" class="btn-ghost" data-act="pause">{t(lang,'Pause','Pausar')}</button><button type="button" class="btn-ghost" data-act="reset">{t(lang,'Reset','Reiniciar')}</button><button type="button" class="btn-ghost" data-act="full">{t(lang,'Full screen','Pantalla completa')}</button></div>"""

def _units(mode, lang):
    cats = [("length", "Length", "Longitud"), ("weight", "Weight", "Peso"), ("volume", "Volume", "Volumen"), ("temp", "Temperature", "Temperatura"),
            ("area", "Area", "Superficie"), ("speed", "Speed", "Velocidad"), ("data", "Data size", "Tamaño de archivos")]
    return f"""<div class="row"><div><label>{t(lang,'What to convert','Qué convertir')}</label><select data-k="cat">{''.join('<option value="%s">%s</option>' % (k, t(lang, en, es)) for k, en, es in cats)}</select></div>
<div><label>{t(lang,'Value','Valor')}</label><input type="number" step="any" data-k="v" value="1"></div></div>
<div class="row"><div><label>{t(lang,'From','De')}</label><select data-k="from"></select></div><div><label>{t(lang,'To','A')}</label><select data-k="to"></select></div></div>
<div class="acts"><button type="button" class="btn-ghost" data-act="swap">⇄ {t(lang,'Swap','Invertir')}</button></div>
<div class="u-out" aria-live="polite"></div><div class="u-all"></div>"""

def _tz(mode, lang):
    return f"""<div class="row"><div><label>{t(lang,'Time in','Hora en')}</label><select data-k="from"></select></div>
<div><label>{t(lang,'Date and time','Fecha y hora')}</label><input type="datetime-local" data-k="dt"></div></div>
<div class="acts"><button type="button" class="btn-ghost" data-act="now">{t(lang,'Now','Ahora')}</button><select data-k="add" style="max-width:280px" aria-label="{t(lang,'Add a city','Agregar ciudad')}"></select></div>
<div class="tz-list" aria-live="polite"></div>"""

def _palette(mode, lang):
    sch = [("random", "Surprise me", "Sorpresa"), ("analog", "Analogous (calm)", "Análogos (tranquila)"), ("comp", "Complementary (contrast)", "Complementarios (contraste)"),
           ("triad", "Triadic (lively)", "Tríada (alegre)"), ("mono", "Monochrome", "Monocromática"), ("pastel", "Pastel", "Pastel")]
    return f"""<div class="row"><div><label>{t(lang,'Style','Estilo')}</label><select data-k="scheme">{''.join('<option value="%s">%s</option>' % (k, t(lang, en, es)) for k, en, es in sch)}</select></div>
<div><label>{t(lang,'Start from my color','Partir de mi color')}</label><input type="color" data-k="base" value="#0f766e"></div></div>
<div class="acts"><button type="button" class="btn" data-act="gen">{t(lang,'New palette (space bar)','Nueva paleta (barra espaciadora)')}</button><button type="button" class="btn-ghost" data-act="base">{t(lang,'Palette from my color','Paleta con mi color')}</button><button type="button" class="btn-ghost" data-act="css">{t(lang,'Copy as CSS','Copiar como CSS')}</button></div>
<div class="pal" aria-live="polite"></div><p class="small">{t(lang,'Tap a color code to copy it. Tap the lock to keep a color while you generate new ones.','Toca un código para copiarlo. Toca el candado para dejar fijo un color mientras generas otros.')}</p>"""

def _names(mode, lang):
    kinds = [("dog", "Dog names", "Nombres para perros"), ("cat", "Cat names", "Nombres para gatos"), ("babyf", "Baby girl names", "Nombres de niña"),
             ("babym", "Baby boy names", "Nombres de niño"), ("biz", "Business names", "Nombres para negocios")]
    return f"""<div class="row"><div><label>{t(lang,'Names for','Nombres para')}</label><select data-k="kind">{''.join('<option value="%s">%s</option>' % (k, t(lang, en, es)) for k, en, es in kinds)}</select></div>
<div><label>{t(lang,'Starts with (optional)','Empieza con (opcional)')}</label><input data-k="letter" maxlength="3" placeholder="M"></div>
<div class="biz-only"><label>{t(lang,'A word about your business (optional)','Una palabra de tu negocio (opcional)')}</label><input data-k="word" placeholder="{t(lang,'bakery','dulce')}"></div></div>
<div class="acts"><button type="button" class="btn" data-act="go">{t(lang,'More names','Más nombres')}</button></div>
<div class="nm-out" aria-live="polite"></div><p class="small">{t(lang,'Your favorites (tap a name):','Tus favoritos (toca un nombre):')}</p><p class="nm-fav"></p>"""

def _petage(mode, lang):
    return f"""<div class="two"><div><div class="row"><div><label>{t(lang,'Pet','Mascota')}</label><select data-k="pet"><option value="dog">{t(lang,'Dog','Perro')}</option><option value="cat">{t(lang,'Cat','Gato')}</option></select></div>
<div class="dog-only"><label>{t(lang,'Size when adult','Tamaño de adulto')}</label><select data-k="size"><option value="4">{t(lang,'Small (under 20 lb)','Chico (menos de 9 kg)')}</option><option value="5" selected>{t(lang,'Medium (21-50 lb)','Mediano (9 a 23 kg)')}</option><option value="6">{t(lang,'Large (51-100 lb)','Grande (23 a 45 kg)')}</option><option value="7">{t(lang,'Giant (over 100 lb)','Gigante (más de 45 kg)')}</option></select></div></div>
<div class="row"><div><label>{t(lang,'Years','Años')}</label><input type="number" data-k="y" value="5" min="0" max="30"></div><div><label>{t(lang,'Months','Meses')}</label><input type="number" data-k="m" value="0" min="0" max="11"></div></div></div>
<div class="stats pa-out" aria-live="polite"></div></div>"""

def _invoice(mode, lang):
    curs = ["USD", "MXN", "EUR", "CAD", "COP", "ARS", "CLP", "PEN", "GBP"]
    return f"""<div class="inv-form"><div class="row"><div><label>{t(lang,'From (you or your business)','De (tú o tu negocio)')}</label><textarea data-k="from" rows="3" style="min-height:80px">{t(lang,'Your Name or Business&#10;your@email.com&#10;City, State','Tu nombre o negocio&#10;tu@correo.com&#10;Ciudad, Estado')}</textarea></div>
<div><label>{t(lang,'Bill to (client)','Facturar a (cliente)')}</label><textarea data-k="to" rows="3" style="min-height:80px">{t(lang,'Client Name&#10;client@email.com','Nombre del cliente&#10;cliente@correo.com')}</textarea></div></div>
<div class="row"><div><label>{t(lang,'Invoice number','Número de factura')}</label><input data-k="num"></div><div><label>{t(lang,'Date','Fecha')}</label><input type="date" data-k="date"></div>
<div><label>{t(lang,'Due date','Vencimiento')}</label><input type="date" data-k="due"></div><div><label>{t(lang,'Currency','Moneda')}</label><select data-k="cur">{''.join('<option>%s</option>' % c for c in curs)}</select></div></div>
<label>{t(lang,'Items: description, quantity, price','Ítems: descripción, cantidad, precio')}</label><div class="inv-rows"></div>
<div class="acts"><button type="button" class="btn-ghost" data-act="add">+ {t(lang,'Add line','Agregar línea')}</button></div>
<div class="row"><div><label>{t(lang,'Discount (%)','Descuento (%)')}</label><input type="number" data-k="disc" value="0" min="0" max="100" step="any"></div><div><label>{t(lang,'Tax (%)','Impuesto (%)')}</label><input type="number" data-k="tax" value="0" min="0" step="any"></div></div>
<label>{t(lang,'Notes or payment details','Notas o datos de pago')}</label><textarea data-k="notes" rows="2" style="min-height:60px">{t(lang,'Thank you for your business! Payment by bank transfer or Zelle.','¡Gracias por tu compra! Pago por transferencia o Zelle.')}</textarea></div>
<div class="acts"><button type="button" class="btn" data-act="print">{t(lang,'Download PDF / Print','Descargar PDF / Imprimir')}</button></div>
<div class="inv-preview" aria-live="polite"></div>"""

ENGINES = dict(qr=_qr, words=_words, textx=_textx, lorem=_lorem, img=_img, wheel=_wheel, teams=_teams, giveaway=_giveaway,
               randnum=_randnum, coin=_coin, dice=_dice, password=_password, timer=_timer,
               units=_units, tz=_tz, palette=_palette, names=_names, petage=_petage, invoice=_invoice)

def widget(tool, lang):
    inner = ENGINES[tool["engine"]](tool.get("mode", ""), lang)
    return '<section class="card tool" data-tool="%s" data-mode="%s">%s</section>' % (tool["engine"], tool.get("mode", ""), inner)

CATS = {
    "qr": ("QR codes", "Códigos QR"),
    "image": ("Images", "Imágenes"),
    "text": ("Text", "Texto"),
    "random": ("Random pickers and games", "Sorteos y juegos al azar"),
    "everyday": ("Everyday tools", "Herramientas para todos los días"),
    "work": ("Work and design", "Trabajo y diseño"),
}

# ------------------------------------------------------------------ the tools, in release order
TOOLS = [
dict(id="qr", n=1, cat="qr", engine="qr", mode="text", related=["qrwifi", "qrwa", "resize"],
 en=dict(slug="qr-code-generator", title="Free QR Code Generator (No Sign-Up, Never Expires)", h1="QR Code Generator",
  desc="Make a QR code for any link or text in one second. Free, no sign-up, no watermark, and it never expires. Download as PNG or SVG.",
  intro="Paste a link or text and your QR code appears right away. Download it as PNG or SVG and print it anywhere.",
  steps=["Paste your link (for example your menu, website, Google review page or Instagram) or any text.", "Pick the size and colors. Keep the code dark on a light background so every phone can read it.", "Download PNG for screens and documents, or SVG for print. Test it with your phone camera before printing."],
  body="""<h2>Free forever, and it never stops working</h2><p>Many QR sites give you a "dynamic" code that points to their own server and stops working when the free trial ends. This tool makes a <strong>static</strong> QR code: your link is written inside the code itself, so it works forever and nobody can switch it off. The only catch: if the link changes, you make a new code (it takes one second).</p>
<h2>Ideas for small businesses</h2><ul><li>Restaurant menu on every table.</li><li>"Leave us a review" sign at the register (paste your Google review link).</li><li>Instagram or TikTok profile on flyers and business cards.</li><li>Payment link (Venmo, PayPal, Cash App) next to the tip jar.</li></ul>""",
  faq=[("Do these QR codes expire?", "No. They are static codes with your link written inside, so they keep working as long as the link works."),
       ("Can I use the QR code commercially?", "Yes. The codes you make are yours to use on menus, flyers, packaging and ads, with no attribution needed."),
       ("Why won't my QR code scan?", "Usually low contrast (light code on light background), a code printed too small (keep it at least 2 cm or 0.8 in wide) or a very long link. Use dark on light and shorten long links.")]),
 es=dict(slug="generador-codigo-qr", title="Generador de códigos QR gratis (sin registro y no vence)", h1="Generador de códigos QR",
  desc="Crea un código QR para cualquier enlace o texto en un segundo. Gratis, sin registro, sin marca de agua y no vence nunca. Descárgalo en PNG o SVG.",
  intro="Pega un enlace o un texto y tu código QR aparece al instante. Descárgalo en PNG o SVG e imprímelo donde quieras.",
  steps=["Pega tu enlace (por ejemplo tu menú, tu web, tu página de reseñas de Google o tu Instagram) o cualquier texto.", "Elige el tamaño y los colores. Deja el código oscuro sobre fondo claro para que lo lea cualquier celular.", "Descarga PNG para pantallas y documentos, o SVG para imprenta. Pruébalo con la cámara del celular antes de imprimir."],
  body="""<h2>Gratis para siempre y no deja de funcionar</h2><p>Muchas páginas de QR te dan un código "dinámico" que pasa por su servidor y deja de funcionar cuando termina la prueba gratis. Esta herramienta crea un código QR <strong>estático</strong>: tu enlace queda escrito dentro del código, así que funciona para siempre y nadie lo puede apagar. Lo único: si cambia el enlace, haces un código nuevo (tarda un segundo).</p>
<h2>Ideas para negocios</h2><ul><li>El menú del restaurante en cada mesa.</li><li>Cartel de "déjanos tu reseña" en la caja (pega tu enlace de reseñas de Google).</li><li>Tu Instagram o TikTok en volantes y tarjetas.</li><li>Enlace de pago (Zelle, PayPal, Mercado Pago) junto al frasco de propinas.</li></ul>""",
  faq=[("¿Los códigos QR vencen?", "No. Son códigos estáticos con tu enlace escrito adentro, así que funcionan mientras el enlace funcione."),
       ("¿Puedo usar el código QR para mi negocio?", "Sí. Los códigos que creas son tuyos para menús, volantes, empaques y publicidad, sin necesidad de mencionarnos."),
       ("¿Por qué no se escanea mi código QR?", "Casi siempre es poco contraste (código claro sobre fondo claro), un código impreso muy chico (mínimo 2 cm de ancho) o un enlace muy largo. Usa oscuro sobre claro y acorta los enlaces largos.")])),

dict(id="compress", n=2, cat="image", engine="img", mode="compress", related=["resize", "convert", "qr"],
 en=dict(slug="compress-image", title="Compress Image to 100KB, 50KB or Any Size (Free, Private)", h1="Compress Image",
  desc="Make JPG, PNG and WebP photos smaller in seconds. Set a target like 100KB or 50KB. Free, no upload: your photos never leave your device.",
  intro="Shrink photos for email, job applications, government forms and websites. Set a size limit like 100 KB and the tool does the rest.",
  steps=["Choose a quality (75% looks the same to the eye and is much lighter) or type a maximum size in KB.", "Optional: set a maximum width. 1920 px is plenty for screens; 1200 px for websites.", "Choose or drop your images. Each one shows the new size and a Download button."],
  body="""<h2>Your photos stay on your device</h2><p>Most compressors upload your photos to a server. This one works inside your browser: the images are never sent anywhere, which matters for ID cards, documents and family photos.</p>
<h2>Compress to an exact size (100 KB, 50 KB, 20 KB)</h2><p>Forms for visas, school portals and job sites often say "maximum 100 KB" or "under 50 KB". Type that number in <em>Max size in KB</em> and the tool tries different quality levels until the photo fits, and makes it a little smaller if it still does not fit.</p>""",
  faq=[("Is it safe to compress private photos here?", "Yes. Nothing is uploaded. The compression runs on your phone or computer, and the result is saved straight to your downloads."),
       ("Why is my PNG still big?", "PNG is a lossless format, so quality does not apply. Choose 'Save as JPG' or WebP to make photos much smaller. Keep PNG only for logos and images with transparency."),
       ("Does compressing reduce quality?", "A little, but at 70-80% the difference is very hard to see while the file is often 60-80% smaller.")]),
 es=dict(slug="comprimir-imagen", title="Comprimir imagen a 100 KB, 50 KB o el peso que quieras (gratis y privado)", h1="Comprimir imagen",
  desc="Reduce el peso de fotos JPG, PNG y WebP en segundos. Pon un límite como 100 KB o 50 KB. Gratis y sin subir nada: tus fotos no salen de tu dispositivo.",
  intro="Achica fotos para correos, solicitudes de empleo, trámites y páginas web. Pon un límite como 100 KB y la herramienta hace el resto.",
  steps=["Elige una calidad (75% se ve igual a simple vista y pesa mucho menos) o escribe un peso máximo en KB.", "Opcional: pon un ancho máximo. 1920 px alcanza para pantallas; 1200 px para páginas web.", "Elige o suelta tus imágenes. Cada una muestra su nuevo peso y un botón para descargar."],
  body="""<h2>Tus fotos se quedan en tu dispositivo</h2><p>La mayoría de los compresores suben tus fotos a un servidor. Este funciona dentro de tu navegador: las imágenes no se envían a ningún lado, algo importante para identificaciones, documentos y fotos familiares.</p>
<h2>Comprimir a un peso exacto (100 KB, 50 KB, 20 KB)</h2><p>Los formularios de visas, escuelas y bolsas de trabajo suelen pedir "máximo 100 KB" o "menos de 50 KB". Escribe ese número en <em>Peso máximo en KB</em> y la herramienta prueba distintas calidades hasta que la foto entre, y la achica un poco si todavía no entra.</p>""",
  faq=[("¿Es seguro comprimir fotos privadas aquí?", "Sí. No se sube nada. La compresión se hace en tu celular o computadora y el resultado se guarda directo en tus descargas."),
       ("¿Por qué mi PNG sigue pesando mucho?", "PNG es un formato sin pérdida, así que la calidad no cambia nada. Elige 'Guardar como JPG' o WebP para que las fotos pesen mucho menos. Usa PNG solo para logos e imágenes con transparencia."),
       ("¿Comprimir baja la calidad?", "Un poco, pero entre 70% y 80% la diferencia casi no se nota y el archivo suele pesar entre 60% y 80% menos.")])),

dict(id="words", n=3, cat="text", engine="words", related=["case", "breaks", "accents"],
 en=dict(slug="word-counter", title="Word Counter and Character Counter (Free, Live)", h1="Word Counter",
  desc="Count words, characters (with and without spaces), sentences and paragraphs as you type, plus reading time and most used words. Free.",
  intro="Paste your essay, post or cover letter and see the word and character count update as you type.",
  steps=["Type or paste your text in the box.", "Words, characters, sentences, paragraphs and reading time update instantly.", "Check the most used words to avoid repeating yourself."],
  body="""<h2>Common limits to keep in mind</h2><table><tr><th>Where</th><th>Limit</th></tr><tr><td>X (Twitter) post</td><td>280 characters</td></tr><tr><td>Instagram caption</td><td>2,200 characters</td></tr><tr><td>Meta description (Google)</td><td>about 155 characters</td></tr><tr><td>College essay (Common App)</td><td>650 words</td></tr><tr><td>Cover letter</td><td>250-400 words</td></tr></table>
<p>Your text is not saved or sent anywhere: the count happens in your browser.</p>""",
  faq=[("How is reading time calculated?", "We use 230 words per minute, the average adult silent reading speed, and 140 words per minute for speaking out loud."),
       ("Do numbers and hyphenated words count?", "Yes. Numbers count as words, and a hyphenated word like 'well-known' counts as one word, the same way Microsoft Word and Google Docs count it."),
       ("Is my text saved?", "No. Nothing is stored or sent. If you reload the page, the box is empty again.")]),
 es=dict(slug="contador-de-palabras", title="Contador de palabras y caracteres en línea (gratis)", h1="Contador de palabras",
  desc="Cuenta palabras, caracteres (con y sin espacios), oraciones y párrafos mientras escribes, más el tiempo de lectura y las palabras más usadas. Gratis.",
  intro="Pega tu ensayo, publicación o carta de presentación y mira cómo se actualizan las palabras y los caracteres mientras escribes.",
  steps=["Escribe o pega tu texto en el recuadro.", "Las palabras, caracteres, oraciones, párrafos y el tiempo de lectura se actualizan al instante.", "Revisa las palabras más usadas para no repetirte."],
  body="""<h2>Límites comunes</h2><table><tr><th>Dónde</th><th>Límite</th></tr><tr><td>Publicación en X (Twitter)</td><td>280 caracteres</td></tr><tr><td>Texto de Instagram</td><td>2.200 caracteres</td></tr><tr><td>Meta descripción (Google)</td><td>unos 155 caracteres</td></tr><tr><td>Biografía de Instagram</td><td>150 caracteres</td></tr><tr><td>Carta de presentación</td><td>250 a 400 palabras</td></tr></table>
<p>Tu texto no se guarda ni se envía a ningún lado: el conteo se hace en tu navegador.</p>""",
  faq=[("¿Cómo se calcula el tiempo de lectura?", "Usamos 230 palabras por minuto, la velocidad promedio de lectura en silencio de un adulto, y 140 palabras por minuto para leer en voz alta."),
       ("¿Los números cuentan como palabras?", "Sí. Los números cuentan como palabras, igual que en Word y Google Docs."),
       ("¿Se guarda mi texto?", "No. No se guarda ni se envía nada. Si recargas la página, el recuadro queda vacío.")])),

dict(id="wheel", n=4, cat="random", engine="wheel", related=["teams", "giveaway", "randnum"],
 en=dict(slug="random-name-picker-wheel", title="Random Name Picker Wheel: Spin to Choose (Free)", h1="Random Name Picker Wheel",
  desc="Type names, spin the wheel and get a fair random winner. Great for classrooms, raffles, giveaways and deciding who goes first. Free.",
  intro="Write one name per line and spin. The result is truly random and fair, and you can remove each winner after the spin.",
  steps=["Type or paste the names, one per line (up to 200).", "Tap Spin the wheel, or tap the wheel itself.", "Turn on 'Remove the winner' to pick several people in a row without repeats."],
  body="""<h2>Is it really random?</h2><p>Yes. The winner is chosen with your browser's cryptographic random generator (the same kind used for passwords) before the wheel starts turning; the animation just shows the result. Every name has exactly the same chance.</p>
<h2>Ideas</h2><ul><li>Teachers: pick a student to answer, a helper of the day or the order of presentations.</li><li>Raffles and giveaways at events or live streams.</li><li>Family: who washes the dishes, which movie to watch, where to eat.</li></ul>""",
  faq=[("How many names can I add?", "Up to 200. With many names the labels get small, but the pick is still fair."),
       ("Are the names saved?", "No. They stay only on your screen."),
       ("Can I use it in class on a projector?", "Yes. It works in any browser, on a phone, tablet or classroom computer.")]),
 es=dict(slug="ruleta-de-nombres", title="Ruleta de nombres: gira y elige al azar (gratis)", h1="Ruleta de nombres",
  desc="Escribe nombres, gira la ruleta y obtén un ganador al azar y justo. Ideal para clases, rifas, sorteos y decidir quién empieza. Gratis.",
  intro="Escribe un nombre por línea y gira. El resultado es realmente al azar y justo, y puedes quitar a cada ganador después del giro.",
  steps=["Escribe o pega los nombres, uno por línea (hasta 200).", "Toca Girar la ruleta, o toca la ruleta misma.", "Activa 'Quitar al ganador' para elegir a varias personas seguidas sin repetir."],
  body="""<h2>¿Es realmente al azar?</h2><p>Sí. El ganador se elige con el generador aleatorio criptográfico de tu navegador (el mismo tipo que se usa para contraseñas) antes de que la ruleta empiece a girar; la animación solo muestra el resultado. Todos los nombres tienen exactamente la misma probabilidad.</p>
<h2>Ideas</h2><ul><li>Maestros: elegir quién responde, el ayudante del día o el orden de las exposiciones.</li><li>Rifas y sorteos en eventos o transmisiones en vivo.</li><li>En familia: quién lava los platos, qué película ver o dónde comer.</li></ul>""",
  faq=[("¿Cuántos nombres puedo poner?", "Hasta 200. Con muchos nombres las letras se achican, pero el sorteo sigue siendo justo."),
       ("¿Se guardan los nombres?", "No. Quedan solo en tu pantalla."),
       ("¿La puedo usar en clase con el proyector?", "Sí. Funciona en cualquier navegador, en celular, tableta o la computadora del aula.")])),

dict(id="password", n=5, cat="everyday", engine="password", related=["randnum", "qrwifi", "words"],
 en=dict(slug="password-generator", title="Strong Password Generator (Random, Free, Private)", h1="Password Generator",
  desc="Create strong random passwords with letters, numbers and symbols. Choose the length, avoid look-alike characters and see the strength. Nothing is sent or saved.",
  intro="Get strong, random passwords in one tap. They are created on your device and never sent or stored.",
  steps=["Choose the length. 16 characters or more is a good default.", "Choose the types of characters. Some sites do not accept symbols; untick them if needed.", "Copy the password and save it in your password manager."],
  body="""<h2>What makes a password strong</h2><p>Length matters more than anything. A random 16-character password with letters, numbers and symbols has more than 100 bits of entropy: it would take far longer than a lifetime to guess. Never reuse a password on two sites; a password manager remembers them for you.</p>
<p>The passwords are generated with <code>crypto.getRandomValues</code>, the secure random generator built into your browser, and every password includes at least one of each type you choose.</p>""",
  faq=[("Is it safe to create passwords on a website?", "This page creates them inside your browser and never sends them anywhere. You can even load the page, turn off your Wi-Fi and it still works."),
       ("How long should my password be?", "At least 12 characters, and 16 or more for email, banking and your password manager."),
       ("What does 'avoid look-alike characters' do?", "It removes I, l, 1, O, 0 and o, so the password is easier to read and type by hand, for example a Wi-Fi password.")]),
 es=dict(slug="generador-de-contrasenas", title="Generador de contraseñas seguras (al azar, gratis y privado)", h1="Generador de contraseñas",
  desc="Crea contraseñas seguras al azar con letras, números y símbolos. Elige el largo, evita caracteres parecidos y mira qué tan segura es. No se envía ni se guarda nada.",
  intro="Obtén contraseñas fuertes y al azar con un toque. Se crean en tu dispositivo y nunca se envían ni se guardan.",
  steps=["Elige el largo. 16 caracteres o más es un buen punto de partida.", "Elige los tipos de caracteres. Algunos sitios no aceptan símbolos; desmárcalos si hace falta.", "Copia la contraseña y guárdala en tu administrador de contraseñas."],
  body="""<h2>Qué hace fuerte a una contraseña</h2><p>El largo importa más que nada. Una contraseña al azar de 16 caracteres con letras, números y símbolos tiene más de 100 bits de entropía: adivinarla llevaría muchísimo más que una vida. Nunca repitas una contraseña en dos sitios; un administrador de contraseñas las recuerda por ti.</p>
<p>Las contraseñas se generan con <code>crypto.getRandomValues</code>, el generador aleatorio seguro de tu navegador, y cada una incluye al menos un carácter de cada tipo que elijas.</p>""",
  faq=[("¿Es seguro crear contraseñas en una página web?", "Esta página las crea dentro de tu navegador y nunca las envía a ningún lado. Incluso puedes cargar la página, apagar el wifi y sigue funcionando."),
       ("¿Qué largo debería tener mi contraseña?", "Al menos 12 caracteres, y 16 o más para el correo, el banco y tu administrador de contraseñas."),
       ("¿Para qué sirve 'evitar caracteres parecidos'?", "Quita I, l, 1, O, 0 y o, para que la contraseña sea más fácil de leer y escribir a mano, por ejemplo la del wifi.")])),

dict(id="giveaway", n=6, cat="random", engine="giveaway", related=["wheel", "randnum", "teams"],
 en=dict(slug="instagram-giveaway-picker", title="Instagram Giveaway Comment Picker (Free, No Login)", h1="Giveaway Comment Picker",
  desc="Pick a fair random winner from Instagram, TikTok or Facebook comments. Paste the comments, remove duplicates, require tagged friends. No login needed.",
  intro="Copy the comments from your post, paste them here and pick one or more winners. No need to connect your Instagram account.",
  steps=["Open your post on a computer, select all the comments and copy them (or export them with any tool). Paste them here, one comment per line.", "Set the rules: number of winners, alternates, minimum tagged friends and accounts to exclude (like your own).", "Tap Pick the winner. Take a screenshot of the result, with the date and time, to share in your stories."],
  body="""<h2>A fair draw your followers can trust</h2><p>The tool removes duplicate entries from the same account (if you turn that on), checks the tagged friends rule and chooses the winners with your browser's cryptographic random generator. The date and time are shown with the result so you can post proof.</p>
<p>We never ask for your Instagram password and nothing is sent anywhere. The usernames stay on your screen.</p>""",
  faq=[("How does it read the username?", "If a line has an @username, the first one is taken as the person who commented. If not, the first word of the line is used."),
       ("Can someone win twice?", "Not when 'One entry per person' is on. Turn it off if your rules give one entry per comment."),
       ("Does it work for TikTok and Facebook?", "Yes. It works with any list of names or comments, from any app or even a spreadsheet.")]),
 es=dict(slug="sorteo-instagram", title="Sorteo de Instagram por comentarios (gratis y sin iniciar sesión)", h1="Sorteo por comentarios",
  desc="Elige un ganador al azar y justo entre los comentarios de Instagram, TikTok o Facebook. Pega los comentarios, quita repetidos y pide amigos etiquetados. Sin iniciar sesión.",
  intro="Copia los comentarios de tu publicación, pégalos aquí y elige uno o más ganadores. No hace falta conectar tu cuenta de Instagram.",
  steps=["Abre tu publicación en la computadora, selecciona todos los comentarios y cópialos. Pégalos aquí, un comentario por línea.", "Pon las reglas: cantidad de ganadores, suplentes, mínimo de amigos etiquetados y cuentas para excluir (como la tuya).", "Toca Elegir ganador. Haz una captura del resultado, con fecha y hora, para compartirla en tus historias."],
  body="""<h2>Un sorteo justo en el que tus seguidores pueden confiar</h2><p>La herramienta quita las participaciones repetidas de la misma cuenta (si lo activas), revisa la regla de amigos etiquetados y elige a los ganadores con el generador aleatorio criptográfico de tu navegador. Junto al resultado aparecen la fecha y la hora para que puedas mostrar la prueba.</p>
<p>Nunca te pedimos la contraseña de Instagram y no se envía nada. Los nombres de usuario quedan en tu pantalla.</p>""",
  faq=[("¿Cómo sabe quién comentó?", "Si una línea tiene un @usuario, toma el primero como la persona que comentó. Si no, usa la primera palabra de la línea."),
       ("¿Alguien puede ganar dos veces?", "No, si está activada 'Una participación por persona'. Desactívala si tus reglas dan una participación por comentario."),
       ("¿Sirve para TikTok y Facebook?", "Sí. Funciona con cualquier lista de nombres o comentarios, de cualquier aplicación o incluso de una planilla.")])),

dict(id="resize", n=7, cat="image", engine="img", mode="resize", related=["compress", "convert", "qr"],
 en=dict(slug="resize-image", title="Resize Image for Instagram, Facebook, YouTube and More (Free)", h1="Resize Image",
  desc="Resize photos to exact pixels or by percentage, with one-tap sizes for Instagram, Stories, Facebook, YouTube and Pinterest. Free, no upload.",
  intro="Change the size of your photos in pixels or by percentage, or tap a social media size and the photo is cropped to fit.",
  steps=["Tap a size (for example Instagram post 1080×1080) or type the width and height you need.", "If you type only the width or only the height, the other one is calculated to keep the proportions.", "Choose or drop your photos and download the resized copies."],
  body="""<h2>Social media sizes</h2><table><tr><th>Where</th><th>Size (px)</th></tr><tr><td>Instagram post</td><td>1080×1080 or 1080×1350</td></tr><tr><td>Stories, Reels, TikTok</td><td>1080×1920</td></tr><tr><td>Facebook shared link</td><td>1200×630</td></tr><tr><td>YouTube thumbnail</td><td>1280×720</td></tr><tr><td>Pinterest pin</td><td>1000×1500</td></tr></table>
<p>Everything happens in your browser: your photos are never uploaded.</p>""",
  faq=[("What does 'Crop to fill' do?", "It fills the whole size without stretching, cutting the edges that do not fit. 'Fit inside' keeps the whole photo and adds margins."),
       ("Can I make a photo bigger?", "Yes, up to 400%, but enlarging cannot add detail, so very large enlargements look soft."),
       ("Can I resize many photos at once?", "Yes, up to 30 at a time with the same settings.")]),
 es=dict(slug="redimensionar-imagen", title="Cambiar tamaño de imagen para Instagram, Facebook, YouTube y más (gratis)", h1="Cambiar tamaño de imagen",
  desc="Cambia el tamaño de tus fotos en píxeles o por porcentaje, con tamaños de un toque para Instagram, historias, Facebook, YouTube y Pinterest. Gratis y sin subir nada.",
  intro="Cambia el tamaño de tus fotos en píxeles o por porcentaje, o toca un tamaño de redes sociales y la foto se recorta para que entre.",
  steps=["Toca un tamaño (por ejemplo publicación de Instagram 1080×1080) o escribe el ancho y el alto que necesitas.", "Si escribes solo el ancho o solo el alto, el otro se calcula para mantener la proporción.", "Elige o suelta tus fotos y descarga las copias con el nuevo tamaño."],
  body="""<h2>Tamaños para redes sociales</h2><table><tr><th>Dónde</th><th>Tamaño (px)</th></tr><tr><td>Publicación de Instagram</td><td>1080×1080 o 1080×1350</td></tr><tr><td>Historias, Reels, TikTok</td><td>1080×1920</td></tr><tr><td>Enlace compartido en Facebook</td><td>1200×630</td></tr><tr><td>Miniatura de YouTube</td><td>1280×720</td></tr><tr><td>Pin de Pinterest</td><td>1000×1500</td></tr></table>
<p>Todo se hace en tu navegador: tus fotos nunca se suben.</p>""",
  faq=[("¿Qué hace 'Recortar para llenar'?", "Llena todo el tamaño sin estirar, recortando los bordes que no entran. 'Encajar' deja la foto entera y agrega márgenes."),
       ("¿Puedo agrandar una foto?", "Sí, hasta 400%, pero al agrandar no se agrega detalle, así que una foto muy agrandada se ve borrosa."),
       ("¿Puedo cambiar el tamaño de muchas fotos a la vez?", "Sí, hasta 30 a la vez con la misma configuración.")])),

dict(id="qrwifi", n=8, cat="qr", engine="qr", mode="wifi", related=["qr", "qrwa", "password"],
 en=dict(slug="wifi-qr-code-generator", title="WiFi QR Code Generator: Share Your WiFi Without the Password", h1="WiFi QR Code Generator",
  desc="Make a QR code that connects guests to your WiFi with one scan. Perfect for homes, Airbnbs, cafés and offices. Free, private, printable.",
  intro="Guests point their camera at the code and join your WiFi without typing the password.",
  steps=["Type the network name exactly as it appears (upper and lower case matter) and the password.", "Choose the security type. Almost all home routers use WPA/WPA2/WPA3.", "Download and print it: on the fridge, at the front desk or in a frame on each café table."],
  body="""<h2>Works with iPhone and Android</h2><p>The iPhone camera (iOS 11 and later) and Android phones (Android 10 and later, or with Google Lens) recognize WiFi QR codes and show a "Join network" button.</p>
<h2>Your password stays private</h2><p>The code is created in your browser. Your network name and password are not sent to us or to anyone. Remember that anyone who scans the code can join the network, so for businesses use a separate guest network.</p>""",
  faq=[("Why does the phone say it cannot join?", "Check that the network name and password are exactly right, including capital letters and spaces, and that the security type matches your router."),
       ("Do I need a new code if I change the password?", "Yes. The password is written inside the code, so make and print a new one."),
       ("Does it work with 5 GHz networks?", "Yes. Use the exact name of the network you want guests to join.")]),
 es=dict(slug="codigo-qr-wifi", title="Código QR para wifi: comparte tu wifi sin dar la contraseña", h1="Código QR para wifi",
  desc="Crea un código QR que conecta a tus invitados a tu wifi con solo escanearlo. Ideal para casas, Airbnb, cafeterías y oficinas. Gratis, privado e imprimible.",
  intro="Tus invitados apuntan la cámara al código y se conectan a tu wifi sin escribir la contraseña.",
  steps=["Escribe el nombre de la red tal como aparece (mayúsculas y minúsculas importan) y la contraseña.", "Elige el tipo de seguridad. Casi todos los routers de casa usan WPA/WPA2/WPA3.", "Descárgalo e imprímelo: en la heladera, en la recepción o en un portarretratos en cada mesa."],
  body="""<h2>Funciona con iPhone y Android</h2><p>La cámara del iPhone (iOS 11 o más nuevo) y los celulares Android (Android 10 o más nuevo, o con Google Lens) reconocen los códigos QR de wifi y muestran un botón para conectarse.</p>
<h2>Tu contraseña queda privada</h2><p>El código se crea en tu navegador. El nombre de tu red y tu contraseña no se nos envían ni a nadie. Recuerda que cualquiera que escanee el código puede entrar a la red, así que en un negocio usa una red de invitados aparte.</p>""",
  faq=[("¿Por qué el celular dice que no se puede conectar?", "Revisa que el nombre de la red y la contraseña estén exactos, con mayúsculas y espacios, y que el tipo de seguridad sea el de tu router."),
       ("¿Necesito un código nuevo si cambio la contraseña?", "Sí. La contraseña va escrita dentro del código, así que crea e imprime uno nuevo."),
       ("¿Sirve para redes de 5 GHz?", "Sí. Usa el nombre exacto de la red a la que quieres que se conecten.")])),

dict(id="case", n=9, cat="text", engine="textx", mode="case", related=["words", "accents", "breaks"],
 en=dict(slug="case-converter", title="Case Converter: UPPERCASE, lowercase, Title Case (Free)", h1="Case Converter",
  desc="Change text to UPPERCASE, lowercase, Title Case, Sentence case or aLtErNaTiNg in one click. Fix text typed with Caps Lock on. Free.",
  intro="Paste text and switch it between upper case, lower case, title case and sentence case in one click.",
  steps=["Paste your text in the left box.", "Tap the style you want. The result appears on the right.", "Tap Copy result and paste it wherever you need."],
  body="""<h2>When it helps</h2><ul><li>Text typed with Caps Lock on by mistake.</li><li>Headlines and titles in Title Case (small words like "and", "of" and "the" stay lower case).</li><li>Spreadsheets with names in all capitals.</li><li>Sentence case for emails and descriptions.</li></ul><p>Accented letters such as á, é, ñ and ü are converted correctly.</p>""",
  faq=[("What is Title Case?", "Each important word starts with a capital letter: 'The Best Tacos in Salt Lake City'."),
       ("What is Sentence case?", "Only the first letter of each sentence is a capital, like normal writing. Names will need a manual capital."),
       ("Is my text saved?", "No. Everything happens in your browser.")]),
 es=dict(slug="convertir-mayusculas-minusculas", title="Convertir mayúsculas a minúsculas y viceversa (gratis)", h1="Convertir mayúsculas y minúsculas",
  desc="Pasa un texto a MAYÚSCULAS, minúsculas, Tipo Título, tipo oración o aLtErNaDo con un clic. Arregla textos escritos con Bloq Mayús. Gratis.",
  intro="Pega un texto y cámbialo entre mayúsculas, minúsculas, tipo título y tipo oración con un clic.",
  steps=["Pega tu texto en el recuadro de la izquierda.", "Toca el estilo que quieras. El resultado aparece a la derecha.", "Toca Copiar resultado y pégalo donde lo necesites."],
  body="""<h2>Cuándo sirve</h2><ul><li>Textos escritos con Bloq Mayús activado sin querer.</li><li>Títulos con cada palabra importante en mayúscula (las palabras chicas como "de", "la" o "y" quedan en minúscula).</li><li>Planillas con nombres todos en mayúsculas.</li><li>Tipo oración para correos y descripciones.</li></ul><p>Las letras con tilde y la ñ se convierten bien.</p>""",
  faq=[("¿Qué es Tipo Título?", "Cada palabra importante empieza con mayúscula: 'Los Mejores Tacos de la Ciudad'. En español lo correcto en títulos suele ser tipo oración, pero en marcas y redes se usa mucho."),
       ("¿Qué es tipo oración?", "Solo va en mayúscula la primera letra de cada oración, como se escribe normalmente. Los nombres propios hay que corregirlos a mano."),
       ("¿Se guarda mi texto?", "No. Todo pasa en tu navegador.")])),

dict(id="teams", n=10, cat="random", engine="teams", related=["wheel", "giveaway", "randnum"],
 en=dict(slug="random-team-generator", title="Random Team Generator: Split a List Into Groups (Free)", h1="Random Team Generator",
  desc="Split a list of names into random, balanced teams or groups. Choose the number of teams or people per team. Great for classes, sports and work.",
  intro="Paste the names, choose how many teams or how many people per team, and get fair random groups.",
  steps=["Write one name per line.", "Choose 'Number of teams' (for example 4 teams) or 'People per team' (for example groups of 3).", "Tap Make teams. Tap again for a new random mix, then copy the teams."],
  body="""<p>Teams are balanced: sizes differ by one person at most. The order is shuffled with your browser's secure random generator, so nobody can say the teams were picked on purpose.</p><p>Ideas: pickup soccer and basketball, classroom group projects, breakout rooms, trivia night and work training.</p>""",
  faq=[("What if the names do not divide evenly?", "Some teams get one extra person. For example 10 names in 3 teams gives teams of 4, 3 and 3."),
       ("Can I keep two people apart?", "Not automatically. Make teams again until you like the mix, or move one name by hand."),
       ("Are the names saved?", "No. They stay on your screen only.")]),
 es=dict(slug="generador-de-equipos", title="Generador de equipos al azar: divide una lista en grupos (gratis)", h1="Generador de equipos al azar",
  desc="Divide una lista de nombres en equipos o grupos al azar y parejos. Elige la cantidad de equipos o de personas por equipo. Ideal para clases, deportes y trabajo.",
  intro="Pega los nombres, elige cuántos equipos o cuántas personas por equipo y obtén grupos al azar y justos.",
  steps=["Escribe un nombre por línea.", "Elige 'Cantidad de equipos' (por ejemplo 4 equipos) o 'Personas por equipo' (por ejemplo grupos de 3).", "Toca Armar equipos. Tócalo otra vez para otra mezcla y después copia los equipos."],
  body="""<p>Los equipos quedan parejos: como mucho hay una persona de diferencia. El orden se mezcla con el generador aleatorio seguro de tu navegador, así nadie puede decir que los equipos se armaron a propósito.</p><p>Ideas: fútbol y básquet con amigos, trabajos en grupo en clase, salas de reuniones, noches de trivia y capacitaciones.</p>""",
  faq=[("¿Qué pasa si no se dividen justo?", "Algunos equipos quedan con una persona más. Por ejemplo, 10 nombres en 3 equipos da equipos de 4, 3 y 3."),
       ("¿Puedo separar a dos personas?", "No de forma automática. Vuelve a armar los equipos hasta que te guste la mezcla, o mueve un nombre a mano."),
       ("¿Se guardan los nombres?", "No. Quedan solo en tu pantalla.")])),

dict(id="convert", n=11, cat="image", engine="img", mode="convert", related=["compress", "resize", "qr"],
 en=dict(slug="image-converter", title="Image Converter: PNG to JPG, JPG to PNG, WebP to JPG (Free)", h1="Image Converter",
  desc="Convert images between JPG, PNG and WebP in your browser: PNG to JPG, WebP to PNG, JPG to WebP and more. Free, private, many files at once.",
  intro="Turn WebP images into JPG or PNG, make PNGs lighter as JPG, or create WebP for your website. No upload needed.",
  steps=["Choose the format you want: JPG, PNG or WebP.", "Choose or drop the images (up to 30).", "Download each converted file."],
  body="""<h2>Which format should I use?</h2><ul><li><strong>JPG</strong>: photos. Light and accepted everywhere.</li><li><strong>PNG</strong>: logos, screenshots and images with a transparent background.</li><li><strong>WebP</strong>: websites. Usually 25-35% lighter than JPG with the same look.</li></ul><p>When you convert a transparent PNG to JPG, the transparent parts become white, because JPG has no transparency.</p>""",
  faq=[("How do I open a WebP image I downloaded?", "Convert it here to JPG or PNG and it opens in any program."),
       ("Can I convert HEIC photos from my iPhone?", "Only if your browser can open HEIC (Safari on Mac and iPhone can). On other browsers, change the iPhone camera to 'Most Compatible' in Settings > Camera > Formats."),
       ("Are my images uploaded?", "No. The conversion happens on your device.")]),
 es=dict(slug="convertir-imagen", title="Convertir imagen: PNG a JPG, JPG a PNG, WebP a JPG (gratis)", h1="Convertir imagen",
  desc="Convierte imágenes entre JPG, PNG y WebP en tu navegador: PNG a JPG, WebP a PNG, JPG a WebP y más. Gratis, privado y con muchos archivos a la vez.",
  intro="Pasa imágenes WebP a JPG o PNG, aliviana PNG convirtiéndolos a JPG o crea WebP para tu web. Sin subir nada.",
  steps=["Elige el formato que quieres: JPG, PNG o WebP.", "Elige o suelta las imágenes (hasta 30).", "Descarga cada archivo convertido."],
  body="""<h2>¿Qué formato me conviene?</h2><ul><li><strong>JPG</strong>: fotos. Livianas y aceptadas en todos lados.</li><li><strong>PNG</strong>: logos, capturas de pantalla e imágenes con fondo transparente.</li><li><strong>WebP</strong>: páginas web. Suele pesar entre 25% y 35% menos que JPG y se ve igual.</li></ul><p>Si conviertes un PNG transparente a JPG, lo transparente queda blanco, porque JPG no tiene transparencia.</p>""",
  faq=[("¿Cómo abro una imagen WebP que descargué?", "Conviértela aquí a JPG o PNG y se abre con cualquier programa."),
       ("¿Puedo convertir fotos HEIC del iPhone?", "Solo si tu navegador abre HEIC (Safari en Mac y iPhone sí). En otros navegadores, cambia la cámara del iPhone a 'Más compatible' en Ajustes > Cámara > Formatos."),
       ("¿Se suben mis imágenes?", "No. La conversión se hace en tu dispositivo.")])),

dict(id="randnum", n=12, cat="random", engine="randnum", related=["wheel", "dice", "coin"],
 en=dict(slug="random-number-generator", title="Random Number Generator (1-100, No Repeats, Free)", h1="Random Number Generator",
  desc="Pick random numbers between any minimum and maximum, one or many at once, with or without repeats. Great for raffles, lotteries and games.",
  intro="Choose a range, how many numbers you need and whether they can repeat. Perfect for raffles with numbered tickets.",
  steps=["Set the minimum and maximum (for example 1 and 100).", "Choose how many numbers you need and tick 'No repeats' for raffles.", "Tap Generate."],
  body="""<p>The numbers come from your browser's cryptographic random generator, so every number in the range has the same chance. For a raffle with numbered tickets, set the range to the first and last ticket, choose the number of prizes and keep 'No repeats' on.</p>""",
  faq=[("Can I generate negative numbers?", "Yes. Use a negative minimum, for example -50 to 50."),
       ("What is the maximum amount of numbers?", "Up to 1,000 at once."),
       ("Is it truly random?", "It uses crypto.getRandomValues, the same secure generator used for passwords and encryption.")]),
 es=dict(slug="numero-aleatorio", title="Generador de números aleatorios (1 a 100, sin repetir, gratis)", h1="Generador de números aleatorios",
  desc="Elige números al azar entre un mínimo y un máximo, uno o muchos a la vez, con o sin repetir. Ideal para rifas, loterías y juegos.",
  intro="Elige el rango, cuántos números necesitas y si se pueden repetir. Perfecto para rifas con números.",
  steps=["Pon el mínimo y el máximo (por ejemplo 1 y 100).", "Elige cuántos números necesitas y marca 'Sin repetir' para rifas.", "Toca Generar."],
  body="""<p>Los números salen del generador aleatorio criptográfico de tu navegador, así que todos los números del rango tienen la misma probabilidad. Para una rifa con boletos numerados, pon el rango del primer al último boleto, elige la cantidad de premios y deja marcado 'Sin repetir'.</p>""",
  faq=[("¿Puedo generar números negativos?", "Sí. Usa un mínimo negativo, por ejemplo de -50 a 50."),
       ("¿Cuántos números puedo generar?", "Hasta 1.000 a la vez."),
       ("¿Es realmente al azar?", "Usa crypto.getRandomValues, el mismo generador seguro que se usa para contraseñas y cifrado.")])),

dict(id="accents", n=13, cat="text", engine="textx", mode="accents", related=["case", "breaks", "words"],
 en=dict(slug="remove-accents", title="Remove Accents From Text (é → e, ñ → n) Free Online", h1="Remove Accents From Text",
  desc="Strip accents and diacritics from any text: á é í ó ú ü ç ñ become plain letters. Useful for file names, URLs, usernames and old systems.",
  intro="Paste text with accents and get the same text with plain letters, ready for file names, links, usernames and old software.",
  steps=["Paste your text.", "Choose whether to keep ñ (useful for Spanish) or turn it into n.", "Copy the result."],
  body="""<p>Some forms, payment systems and older programs reject letters like é, ü or ñ, and file names with accents can break links. This tool removes the accent marks (diacritics) but keeps the letters, spaces, numbers and punctuation.</p>""",
  faq=[("Which characters are changed?", "Letters with accents and marks from Spanish, French, Portuguese, German and other languages: á→a, ç→c, ü→u, ã→a and so on."),
       ("Does it change upper case?", "No. Capital letters stay capital: É becomes E."),
       ("Is my text saved?", "No. It is processed in your browser.")]),
 es=dict(slug="quitar-acentos", title="Quitar tildes y acentos de un texto (gratis en línea)", h1="Quitar tildes y acentos",
  desc="Quita tildes y acentos de cualquier texto: á é í ó ú ü quedan como letras simples, con opción de mantener la ñ. Útil para nombres de archivo, enlaces y sistemas viejos.",
  intro="Pega un texto con tildes y obtén el mismo texto sin acentos, listo para nombres de archivo, enlaces, usuarios y programas viejos.",
  steps=["Pega tu texto.", "Elige si mantienes la ñ o la pasas a n.", "Copia el resultado."],
  body="""<p>Algunos formularios, sistemas de pago y programas viejos rechazan letras como é, ü o ñ, y los nombres de archivo con tilde pueden romper enlaces. Esta herramienta quita las tildes y diéresis pero deja las letras, los espacios, los números y la puntuación.</p>""",
  faq=[("¿Qué caracteres cambia?", "Las letras con tilde y marcas del español, francés, portugués, alemán y otros idiomas: á→a, ç→c, ü→u, ã→a, etc."),
       ("¿Cambia las mayúsculas?", "No. Las mayúsculas siguen siendo mayúsculas: É queda E."),
       ("¿Se guarda mi texto?", "No. Se procesa en tu navegador.")])),

dict(id="timer", n=14, cat="everyday", engine="timer", related=["coin", "dice", "randnum"],
 en=dict(slug="online-timer", title="Online Timer and Stopwatch With Alarm (Full Screen)", h1="Online Timer and Stopwatch",
  desc="Free countdown timer with alarm and stopwatch. One-tap 1, 5, 10, 25 and 60 minute timers, full screen for classrooms and meetings.",
  intro="Set a countdown with an alarm, or use the stopwatch. Tap full screen to show it on a projector or TV.",
  steps=["Tap a preset (5 min, 25 min…) to start right away, or type hours, minutes and seconds and tap Start.", "When time is up the screen blinks and an alarm sounds three times.", "Switch to Stopwatch to measure time instead."],
  body="""<h2>Ideas</h2><ul><li>Classroom activities and tests, on the projector in full screen.</li><li>Pomodoro: 25 minutes of focus, 5 minutes of break.</li><li>Cooking, workouts and rest between climbing attempts.</li><li>Meetings and presentations with a time limit.</li></ul><p>Keep this tab open. Some phones pause timers in background tabs to save battery.</p>""",
  faq=[("Why did I not hear the alarm?", "Check the volume and that the phone is not on silent. Browsers only allow sound after you tap the page once, which happens when you press Start."),
       ("Does it keep counting if I switch tabs?", "Yes, it uses the clock time, so it stays exact. The alarm sounds when you come back if the browser paused the tab."),
       ("Can I use it on a TV or projector?", "Yes. Tap Full screen.")]),
 es=dict(slug="temporizador-online", title="Temporizador y cronómetro online con alarma (pantalla completa)", h1="Temporizador y cronómetro online",
  desc="Temporizador gratis con alarma y cronómetro. Temporizadores de 1, 5, 10, 25 y 60 minutos con un toque y pantalla completa para clases y reuniones.",
  intro="Pon una cuenta regresiva con alarma o usa el cronómetro. Toca pantalla completa para mostrarlo en un proyector o televisor.",
  steps=["Toca un tiempo listo (5 min, 25 min…) para empezar ya, o escribe horas, minutos y segundos y toca Iniciar.", "Cuando se acaba el tiempo la pantalla parpadea y suena una alarma tres veces.", "Cambia a Cronómetro para medir tiempo."],
  body="""<h2>Ideas</h2><ul><li>Actividades y exámenes en clase, en el proyector a pantalla completa.</li><li>Pomodoro: 25 minutos de concentración y 5 de descanso.</li><li>Cocina, ejercicio y descanso entre series.</li><li>Reuniones y exposiciones con tiempo límite.</li></ul><p>Deja esta pestaña abierta. Algunos celulares pausan las pestañas de fondo para ahorrar batería.</p>""",
  faq=[("¿Por qué no escuché la alarma?", "Revisa el volumen y que el celular no esté en silencio. Los navegadores solo permiten sonido después de que tocas la página una vez, y eso pasa al apretar Iniciar."),
       ("¿Sigue contando si cambio de pestaña?", "Sí, usa la hora del reloj, así que queda exacto. Si el navegador pausó la pestaña, la alarma suena cuando vuelves."),
       ("¿Lo puedo usar en un televisor o proyector?", "Sí. Toca Pantalla completa.")])),

dict(id="qrwa", n=15, cat="qr", engine="qr", mode="whatsapp", related=["qr", "qrwifi", "giveaway"],
 en=dict(slug="whatsapp-qr-code-generator", title="WhatsApp QR Code Generator With Pre-Filled Message (Free)", h1="WhatsApp QR Code Generator",
  desc="Create a QR code that opens a WhatsApp chat with your number and a ready-to-send message. Ideal for shops, flyers and business cards. Free.",
  intro="Customers scan the code and a WhatsApp chat with you opens, with a message already written. They just tap send.",
  steps=["Type your phone number with the country code (1 for the US, 52 for Mexico) and no plus sign or spaces needed.", "Write the message that will appear ready to send, for example 'Hi, I want to order…'.", "Download the code and put it on your flyers, menu, packaging or shop window."],
  body="""<p>The code opens a standard <code>wa.me</code> link, the official click-to-chat link from WhatsApp. It works with regular WhatsApp and WhatsApp Business, on iPhone and Android.</p><p>Tip: add a short line next to the code, like "Scan to order on WhatsApp", so people know what it does.</p>""",
  faq=[("Do I need WhatsApp Business?", "No. It works with any WhatsApp number, but WhatsApp Business lets you add automatic greetings and a catalog."),
       ("Why does it say the number is invalid?", "Include the country code and remove leading zeros. A US number looks like 1 801 555 0123."),
       ("Can I change the message later?", "The message is part of the code, so you make a new code. It takes one second.")]),
 es=dict(slug="codigo-qr-whatsapp", title="Código QR de WhatsApp con mensaje listo para enviar (gratis)", h1="Código QR de WhatsApp",
  desc="Crea un código QR que abre un chat de WhatsApp con tu número y un mensaje ya escrito. Ideal para negocios, volantes y tarjetas. Gratis.",
  intro="Tus clientes escanean el código y se abre un chat de WhatsApp contigo, con el mensaje ya escrito. Solo tienen que tocar enviar.",
  steps=["Escribe tu número con el código de país (1 para EE. UU., 52 para México, 54 9 para Argentina), sin el signo + ni espacios.", "Escribe el mensaje que aparecerá listo para enviar, por ejemplo 'Hola, quiero hacer un pedido…'.", "Descarga el código y ponlo en tus volantes, menú, empaques o vidriera."],
  body="""<p>El código abre un enlace <code>wa.me</code>, el enlace oficial de WhatsApp para iniciar un chat. Funciona con WhatsApp normal y WhatsApp Business, en iPhone y Android.</p><p>Consejo: pon una frase corta al lado del código, como "Escanea y pide por WhatsApp", para que la gente sepa qué hace.</p>""",
  faq=[("¿Necesito WhatsApp Business?", "No. Funciona con cualquier número de WhatsApp, pero WhatsApp Business te deja poner saludos automáticos y un catálogo."),
       ("¿Por qué dice que el número no es válido?", "Incluye el código de país y quita el 0 o el 15 del principio. Un número de México se ve así: 52 55 1234 5678."),
       ("¿Puedo cambiar el mensaje después?", "El mensaje va dentro del código, así que haces un código nuevo. Tarda un segundo.")])),

dict(id="coin", n=16, cat="random", engine="coin", related=["dice", "randnum", "wheel"],
 en=dict(slug="flip-a-coin", title="Flip a Coin Online: Heads or Tails (Free, Fair)", h1="Flip a Coin",
  desc="Flip a virtual coin and get heads or tails with a fair 50/50 result. Keeps a count of heads and tails. Free, no ads in the way.",
  intro="Tap the button for a fair heads-or-tails result, with a running count of each side.",
  steps=["Tap Flip the coin.", "Wait one second for the result.", "Flip as many times as you want; the count of heads and tails appears below."],
  body="""<p>Each flip uses your browser's secure random generator, so heads and tails have exactly a 50% chance. Use it to decide who kicks off, who pays, or as a tie-breaker. For more than two options, try the <a href="../random-name-picker-wheel/">name picker wheel</a>.</p>""",
  faq=[("Is a virtual coin fair?", "Yes. It is exactly 50/50, even fairer than a real coin, which is slightly more likely to land on the side it started on."),
       ("Can I flip several coins at once?", "Use the dice roller with 2-sided... or simply flip several times; the count keeps track."),
       ("Does it work offline?", "Yes, once the page is loaded.")]),
 es=dict(slug="cara-o-cruz", title="Cara o cruz online: lanza una moneda (gratis y justo)", h1="Cara o cruz",
  desc="Lanza una moneda virtual y obtén cara o cruz con un resultado justo 50/50. Lleva la cuenta de caras y cruces. Gratis.",
  intro="Toca el botón para un resultado justo de cara o cruz, con la cuenta de cada lado.",
  steps=["Toca Lanzar la moneda.", "Espera un segundo el resultado.", "Lanza todas las veces que quieras; la cuenta de caras y cruces aparece abajo."],
  body="""<p>Cada lanzamiento usa el generador aleatorio seguro de tu navegador, así que cara y cruz tienen exactamente 50% de probabilidad cada una. Úsalo para decidir quién saca, quién paga o para desempatar. Si tienes más de dos opciones, prueba la <a href="../ruleta-de-nombres/">ruleta de nombres</a>.</p>""",
  faq=[("¿Una moneda virtual es justa?", "Sí. Es exactamente 50/50, incluso más justa que una moneda real, que tiene un poquito más de chance de caer del lado en que empezó."),
       ("¿También se dice águila o sol?", "Sí. En México se dice águila o sol y en otros países cara o sello: es lo mismo."),
       ("¿Funciona sin internet?", "Sí, una vez que la página cargó.")])),

dict(id="dice", n=17, cat="random", engine="dice", related=["coin", "randnum", "teams"],
 en=dict(slug="dice-roller", title="Online Dice Roller: Roll 1 to 10 Dice (d6, d20 and More)", h1="Dice Roller",
  desc="Roll virtual dice online: 1 to 10 dice with 4, 6, 8, 10, 12, 20 or 100 sides, with the total. For board games, D&D and classrooms.",
  intro="Lost the dice? Roll up to 10 dice of any type and see the total instantly.",
  steps=["Choose how many dice (1 to 10).", "Choose the type: d6 for most board games, d20 for role-playing games.", "Tap Roll."],
  body="""<p>Each die is fair: every face has the same chance, using your browser's secure random generator. Classic six-sided dice show dots; other dice show the number and type. Teachers use it for math games with sums and probabilities.</p>""",
  faq=[("Which dice are available?", "d4, d6, d8, d10, d12, d20 and d100."),
       ("Does it show the total?", "Yes, when you roll more than one die."),
       ("Can I use it for Dungeons & Dragons?", "Yes. Choose d20 for attacks and checks, and the right die for damage.")]),
 es=dict(slug="lanzar-dados", title="Lanzar dados online: de 1 a 10 dados (d6, d20 y más)", h1="Lanzar dados",
  desc="Lanza dados virtuales: de 1 a 10 dados de 4, 6, 8, 10, 12, 20 o 100 caras, con el total. Para juegos de mesa, rol y clases.",
  intro="¿Perdiste los dados? Lanza hasta 10 dados de cualquier tipo y mira el total al instante.",
  steps=["Elige cuántos dados (de 1 a 10).", "Elige el tipo: d6 para la mayoría de los juegos de mesa, d20 para juegos de rol.", "Toca Lanzar."],
  body="""<p>Cada dado es justo: todas las caras tienen la misma probabilidad, con el generador aleatorio seguro de tu navegador. Los dados de seis caras muestran puntos; los demás muestran el número y el tipo. Los maestros lo usan para juegos de sumas y probabilidad.</p>""",
  faq=[("¿Qué dados hay?", "d4, d6, d8, d10, d12, d20 y d100."),
       ("¿Muestra el total?", "Sí, cuando lanzas más de un dado."),
       ("¿Sirve para Calabozos y Dragones?", "Sí. Elige d20 para ataques y pruebas, y el dado que corresponda para el daño.")])),

dict(id="breaks", n=18, cat="text", engine="textx", mode="breaks", related=["case", "words", "accents"],
 en=dict(slug="remove-line-breaks", title="Remove Line Breaks From Text (Fix PDF Copy-Paste)", h1="Remove Line Breaks",
  desc="Remove line breaks and extra spaces from text copied from PDFs, emails or websites. Keep paragraphs or make one line. Free and instant.",
  intro="Text copied from a PDF comes with a break at the end of every line. Paste it here to join the lines back together.",
  steps=["Paste the text.", "Choose: everything in one line, keep paragraphs, or only remove empty lines.", "Copy the clean result."],
  body="""<p>"Keep paragraphs" is the best choice for text copied from PDFs: it joins the lines inside each paragraph and keeps the blank line between paragraphs. "One line" is handy for spreadsheets, code and form fields.</p>""",
  faq=[("Why does text from a PDF have so many line breaks?", "PDFs store each line separately, so copying adds a break at the end of every line."),
       ("Can I remove double spaces too?", "Yes, keep 'Also remove double spaces' ticked."),
       ("Is my text saved?", "No. It is processed in your browser.")]),
 es=dict(slug="quitar-saltos-de-linea", title="Quitar saltos de línea de un texto (arreglar texto copiado de PDF)", h1="Quitar saltos de línea",
  desc="Quita los saltos de línea y espacios de más de textos copiados de PDF, correos o páginas web. Mantén los párrafos o deja una sola línea. Gratis.",
  intro="El texto copiado de un PDF trae un salto al final de cada línea. Pégalo aquí para volver a unir las líneas.",
  steps=["Pega el texto.", "Elige: todo en una línea, mantener párrafos o solo quitar líneas vacías.", "Copia el resultado limpio."],
  body="""<p>"Mantener párrafos" es la mejor opción para texto copiado de PDF: une las líneas de cada párrafo y deja la línea en blanco entre párrafos. "Una sola línea" sirve para planillas, código y campos de formularios.</p>""",
  faq=[("¿Por qué el texto de un PDF tiene tantos saltos de línea?", "Los PDF guardan cada línea por separado, así que al copiar se agrega un salto al final de cada una."),
       ("¿También puedo quitar los espacios dobles?", "Sí, deja marcado 'Quitar también los espacios dobles'."),
       ("¿Se guarda mi texto?", "No. Se procesa en tu navegador.")])),

dict(id="lorem", n=19, cat="text", engine="lorem", related=["words", "case", "breaks"],
 en=dict(slug="lorem-ipsum-generator", title="Lorem Ipsum Generator (Paragraphs, Sentences, Words)", h1="Lorem Ipsum Generator",
  desc="Generate lorem ipsum placeholder text by paragraphs, sentences or words, in Latin or Spanish. Copy with one click. Free for designers and developers.",
  intro="Fill your design with placeholder text: choose how many paragraphs, sentences or words and copy.",
  steps=["Choose how many and of what (paragraphs, sentences or words).", "Choose classic Latin lorem ipsum or Spanish placeholder text.", "Copy and paste into your design, website or template."],
  body="""<p>Lorem ipsum is scrambled Latin from a text by Cicero, used by printers since the 1500s so that readers look at the layout instead of the words. Use Spanish placeholder text when you design for a Spanish-speaking audience, because Spanish words are longer and change how the text fits.</p>""",
  faq=[("What does lorem ipsum mean?", "Nothing exactly. It comes from 'dolorem ipsum' ('pain itself') in Cicero's De finibus, cut and mixed so it reads as nonsense."),
       ("Can I use it commercially?", "Yes. Placeholder text is free to use anywhere."),
       ("Why use Spanish placeholder text?", "Spanish text is about 20-25% longer than English, so it shows the real space you will need.")]),
 es=dict(slug="generador-texto-de-relleno", title="Generador de texto de relleno y lorem ipsum en español", h1="Generador de texto de relleno",
  desc="Genera texto de relleno en español o lorem ipsum en latín, por párrafos, oraciones o palabras. Cópialo con un clic. Gratis para diseñadores.",
  intro="Llena tu diseño con texto de prueba: elige cuántos párrafos, oraciones o palabras y cópialo.",
  steps=["Elige cuántos y de qué (párrafos, oraciones o palabras).", "Elige texto de relleno en español o el clásico lorem ipsum en latín.", "Cópialo y pégalo en tu diseño, página web o plantilla."],
  body="""<p>El lorem ipsum es latín desordenado de un texto de Cicerón que usan las imprentas desde el siglo XVI para que el lector mire el diseño y no las palabras. Para diseños en español conviene texto de relleno en español, porque las palabras son más largas y cambian cómo entra el texto.</p>""",
  faq=[("¿Qué significa lorem ipsum?", "Nada en concreto. Viene de 'dolorem ipsum' ('el dolor mismo') en De finibus de Cicerón, cortado y mezclado para que no se entienda."),
       ("¿Lo puedo usar en trabajos comerciales?", "Sí. El texto de relleno se puede usar libremente."),
       ("¿Por qué usar texto de relleno en español?", "Un texto en español es entre 20% y 25% más largo que en inglés, así que muestra el espacio real que vas a necesitar.")])),
dict(id="units", n=20, cat="everyday", engine="units", related=["tz", "timer", "randnum"],
 en=dict(slug="unit-converter", title="Unit Converter: Length, Weight, Volume, Temperature and More", h1="Unit Converter",
  desc="Convert feet to meters, pounds to kg, cups to mL, °F to °C, acres, mph and file sizes. Instant results with every unit at once. Free.",
  intro="Convert between US and metric units in one place: length, weight, volume, temperature, area, speed and data size.",
  steps=["Choose what you want to convert (length, weight, temperature…).", "Type the value and pick the units. Tap Swap to turn the conversion around.", "Below the result you see the same value in every other unit."],
  body="""<h2>Quick reference</h2><table><tr><th>US</th><th>Metric</th></tr><tr><td>1 inch</td><td>2.54 cm</td></tr><tr><td>1 foot</td><td>30.48 cm</td></tr><tr><td>1 mile</td><td>1.609 km</td></tr><tr><td>1 pound</td><td>453.6 g</td></tr><tr><td>1 US cup</td><td>236.6 mL</td></tr><tr><td>1 US gallon</td><td>3.785 L</td></tr><tr><td>32 °F</td><td>0 °C</td></tr></table>
<p>For cooking conversions by ingredient (cups of flour to grams), use the <a href="/cooking-measurement-converter/">cooking measurement converter</a>.</p>""",
  faq=[("How do I convert °F to °C?", "Subtract 32 and multiply by 5/9. For example 68 °F − 32 = 36, × 5/9 = 20 °C."),
       ("Is a US gallon the same as a UK gallon?", "No. A US gallon is 3.785 liters and a UK (imperial) gallon is 4.546 liters. Both are in the list."),
       ("Why does my 1 TB drive show less space?", "Drive makers use 1 TB = 1,000,000,000,000 bytes, while computers often count in binary (TiB). Compare TB and GiB in the 'Data size' section.")]),
 es=dict(slug="convertidor-de-unidades", title="Convertidor de unidades: longitud, peso, volumen, temperatura y más", h1="Convertidor de unidades",
  desc="Convierte pies a metros, libras a kilos, tazas a mL, °F a °C, acres, millas por hora y tamaños de archivo. Resultado al instante en todas las unidades. Gratis.",
  intro="Convierte entre unidades de EE. UU. y del sistema métrico en un solo lugar: longitud, peso, volumen, temperatura, superficie, velocidad y archivos.",
  steps=["Elige qué quieres convertir (longitud, peso, temperatura…).", "Escribe el valor y elige las unidades. Toca Invertir para dar vuelta la conversión.", "Debajo del resultado ves el mismo valor en todas las demás unidades."],
  body="""<h2>Equivalencias rápidas</h2><table><tr><th>EE. UU.</th><th>Métrico</th></tr><tr><td>1 pulgada</td><td>2,54 cm</td></tr><tr><td>1 pie</td><td>30,48 cm</td></tr><tr><td>1 milla</td><td>1,609 km</td></tr><tr><td>1 libra</td><td>453,6 g</td></tr><tr><td>1 taza (EE. UU.)</td><td>236,6 mL</td></tr><tr><td>1 galón (EE. UU.)</td><td>3,785 L</td></tr><tr><td>32 °F</td><td>0 °C</td></tr></table>
<p>Para convertir ingredientes de cocina (tazas de harina a gramos), usa el <a href="/es/conversor-medidas-de-cocina/">convertidor de medidas de cocina</a>.</p>""",
  faq=[("¿Cómo paso de °F a °C?", "Resta 32 y multiplica por 5/9. Por ejemplo 68 °F − 32 = 36, × 5/9 = 20 °C."),
       ("¿El galón de EE. UU. es igual al del Reino Unido?", "No. El galón de EE. UU. tiene 3,785 litros y el británico 4,546 litros. Los dos están en la lista."),
       ("¿Por qué mi disco de 1 TB muestra menos espacio?", "Los fabricantes usan 1 TB = 1.000.000.000.000 bytes y las computadoras suelen contar en binario (TiB). Compara TB y GiB en 'Tamaño de archivos'.")])),

dict(id="tz", n=21, cat="everyday", engine="tz", related=["units", "timer", "invoice"],
 en=dict(slug="time-zone-converter", title="Time Zone Converter: What Time Is It There? (Free)", h1="Time Zone Converter",
  desc="Convert a time between time zones and cities: Mountain, Pacific, Eastern, Mexico, Colombia, Argentina, Spain, London, Tokyo and more. Daylight saving included.",
  intro="Pick a date and time in one city and see what time it is everywhere else, with daylight saving time handled for you.",
  steps=["Choose the city of the time you know. It starts with your own time zone.", "Change the date and time, or tap Now.", "Add cities from the list. Each one shows the time and the difference in hours."],
  body="""<p>Scheduling a call with family abroad, a client in another state or a live stream? Daylight saving time changes on different dates in the US, Mexico and Europe, and Arizona and most of Latin America do not change at all. This converter uses your browser's official time zone database, so the difference is right on any date.</p>""",
  faq=[("Is Utah on Mountain Time?", "Yes. Salt Lake City uses Mountain Time (MST in winter, MDT in summer), the same as Denver. Arizona stays on MST all year."),
       ("Does it handle daylight saving time?", "Yes. It checks the rules of each city for the exact date you choose."),
       ("Can I add any city?", "You can add the main cities of the Americas, Europe, Asia and Oceania from the list.")]),
 es=dict(slug="convertidor-de-zonas-horarias", title="Convertidor de zonas horarias: ¿qué hora es allá? (gratis)", h1="Convertidor de zonas horarias",
  desc="Convierte una hora entre zonas horarias y ciudades: México, Colombia, Argentina, España, Nueva York, Los Ángeles, Utah y más. Con horario de verano incluido.",
  intro="Elige una fecha y hora en una ciudad y mira qué hora es en las demás, con el horario de verano ya calculado.",
  steps=["Elige la ciudad de la hora que conoces. Empieza con tu propia zona horaria.", "Cambia la fecha y la hora, o toca Ahora.", "Agrega ciudades de la lista. Cada una muestra la hora y la diferencia en horas."],
  body="""<p>¿Vas a llamar a tu familia en otro país, a un cliente en otro estado o hacer un en vivo? El horario de verano cambia en fechas distintas en EE. UU. y Europa, y México, Arizona y casi toda Latinoamérica no lo cambian. Este convertidor usa la base oficial de zonas horarias de tu navegador, así que la diferencia es correcta en cualquier fecha.</p>""",
  faq=[("¿Qué diferencia hay entre Utah y México?", "Depende de la época del año: Utah cambia al horario de verano y la Ciudad de México ya no. Elige la fecha y el convertidor te da la diferencia exacta."),
       ("¿Tiene en cuenta el horario de verano?", "Sí. Revisa las reglas de cada ciudad para la fecha exacta que elijas."),
       ("¿Puedo agregar cualquier ciudad?", "Puedes agregar las principales ciudades de América, Europa, Asia y Oceanía desde la lista.")])),

dict(id="palette", n=22, cat="work", engine="palette", related=["qr", "resize", "invoice"],
 en=dict(slug="color-palette-generator", title="Color Palette Generator: Beautiful Color Schemes With HEX Codes", h1="Color Palette Generator",
  desc="Generate color palettes in one tap: analogous, complementary, triadic, monochrome or pastel. Lock the colors you like, copy HEX, RGB, HSL or CSS. Free.",
  intro="Tap for a new 5-color palette, lock the colors you like and copy the codes for your brand, Canva design or website.",
  steps=["Pick a style or start from your own color (for example your logo color).", "Tap New palette, or press the space bar, until you like it. Lock any color to keep it.", "Tap a HEX code to copy it, or copy the whole palette as CSS."],
  body="""<h2>Which style to choose</h2><ul><li><strong>Analogous</strong>: neighbor colors, calm and natural. Great for wellness, food and home brands.</li><li><strong>Complementary</strong>: opposite colors with strong contrast for buttons and calls to action.</li><li><strong>Triadic</strong>: three evenly spaced colors, playful and lively.</li><li><strong>Monochrome</strong>: one color in light and dark shades, elegant and simple.</li></ul><p>Tip: use the darkest color for text, one bright color for buttons and the lightest for backgrounds.</p>""",
  faq=[("Can I use the colors for my brand?", "Yes. Colors cannot be owned, so the palettes are free to use anywhere."),
       ("How do I use the codes in Canva?", "In Canva, tap a color, then the '+' (new color) and paste the HEX code, for example #0F766E."),
       ("What do HEX, RGB and HSL mean?", "They are three ways to write the same color. HEX is used on the web and in Canva, RGB in many apps, and HSL is handy to make a color lighter or darker.")]),
 es=dict(slug="generador-de-paletas-de-colores", title="Generador de paletas de colores con códigos HEX (gratis)", h1="Generador de paletas de colores",
  desc="Crea paletas de colores con un toque: análogos, complementarios, tríada, monocromática o pastel. Fija los colores que te gustan y copia HEX, RGB, HSL o CSS. Gratis.",
  intro="Toca para una paleta nueva de 5 colores, fija los que te gustan y copia los códigos para tu marca, tu diseño de Canva o tu web.",
  steps=["Elige un estilo o parte de tu propio color (por ejemplo el de tu logo).", "Toca Nueva paleta, o la barra espaciadora, hasta que te guste. Fija con el candado los colores que quieras mantener.", "Toca un código HEX para copiarlo, o copia toda la paleta como CSS."],
  body="""<h2>Qué estilo elegir</h2><ul><li><strong>Análogos</strong>: colores vecinos, tranquilos y naturales. Ideales para marcas de bienestar, comida y hogar.</li><li><strong>Complementarios</strong>: colores opuestos con mucho contraste, para botones y llamadas a la acción.</li><li><strong>Tríada</strong>: tres colores repartidos, alegres y llamativos.</li><li><strong>Monocromática</strong>: un color en tonos claros y oscuros, elegante y simple.</li></ul><p>Consejo: usa el color más oscuro para textos, uno vivo para botones y el más claro para fondos.</p>""",
  faq=[("¿Puedo usar los colores para mi marca?", "Sí. Los colores no tienen dueño, así que puedes usar las paletas donde quieras."),
       ("¿Cómo uso los códigos en Canva?", "En Canva toca un color, luego el '+' (color nuevo) y pega el código HEX, por ejemplo #0F766E."),
       ("¿Qué son HEX, RGB y HSL?", "Son tres formas de escribir el mismo color. HEX se usa en la web y en Canva, RGB en muchas aplicaciones y HSL sirve para aclarar u oscurecer un color.")])),

dict(id="names", n=23, cat="random", engine="names", mode="dog", related=["petage", "wheel", "palette"],
 en=dict(slug="name-generator", title="Name Generator: Dog, Cat, Baby and Business Names", h1="Name Generator",
  desc="Find the perfect name: cute dog and cat names, popular baby names in English and Spanish, and business name ideas. Filter by first letter and save favorites.",
  intro="Looking for a name for your new puppy, kitten, baby or small business? Get 12 ideas at a time and keep your favorites.",
  steps=["Choose what the name is for: dog, cat, baby girl, baby boy or business.", "Optional: type the first letter, or for businesses a word about what you sell.", "Tap a name to add it to your favorites, and tap More names for new ideas."],
  body="""<h2>Tips for pet names</h2><p>Dogs respond best to names with one or two syllables that end in a vowel sound ("Luna", "Toby", "Mochi"). Avoid names that sound like commands, such as "Kit" (sit) or "Bo" (no).</p><h2>Tips for business names</h2><p>Keep it short, easy to spell and say out loud. Before you decide, search the name on Google, Instagram and your state's business registry to make sure it is free. Want gifts for your new pet? Visit <a href="https://cozypawsgifts.pages.dev/" rel="noopener">Cozy Paws</a>.</p>""",
  faq=[("Are the baby names popular in the US?", "Yes. The lists mix the most popular names in the US and in Spanish-speaking families, like Sofía, Mateo, Olivia and Liam."),
       ("Can I use a generated business name?", "You can, but check that no one else uses it in your state and that the domain and social handles are free."),
       ("Are my favorites saved?", "Only while the page is open. Write them down or take a screenshot.")]),
 es=dict(slug="generador-de-nombres", title="Generador de nombres: para perros, gatos, bebés y negocios", h1="Generador de nombres",
  desc="Encuentra el nombre ideal: nombres lindos para perros y gatos, nombres de bebé populares en español e inglés e ideas de nombres para negocios. Filtra por letra y guarda favoritos.",
  intro="¿Buscas nombre para tu cachorro, tu gatito, tu bebé o tu emprendimiento? Recibe 12 ideas a la vez y guarda tus favoritos.",
  steps=["Elige para qué es el nombre: perro, gato, niña, niño o negocio.", "Opcional: escribe la primera letra, o para negocios una palabra de lo que vendes.", "Toca un nombre para sumarlo a tus favoritos y toca Más nombres para nuevas ideas."],
  body="""<h2>Consejos para nombres de mascotas</h2><p>Los perros responden mejor a nombres de una o dos sílabas que terminan en vocal ("Luna", "Toby", "Canela"). Evita nombres que suenen a órdenes, como "Ven" o "No".</p><h2>Consejos para nombres de negocios</h2><p>Que sea corto, fácil de escribir y de decir. Antes de decidir, búscalo en Google, Instagram y en el registro de negocios de tu estado para asegurarte de que esté libre. ¿Quieres regalos para tu nueva mascota? Visita <a href="https://cozypawsgifts.pages.dev/" rel="noopener">Cozy Paws</a>.</p>""",
  faq=[("¿Los nombres de bebé son populares?", "Sí. Las listas mezclan los nombres más populares entre familias hispanas y en EE. UU., como Sofía, Mateo, Valentina y Liam."),
       ("¿Puedo usar un nombre de negocio generado?", "Sí, pero revisa que nadie lo use en tu estado y que el dominio y las redes estén libres."),
       ("¿Se guardan mis favoritos?", "Solo mientras la página está abierta. Anótalos o haz una captura.")])),

dict(id="petage", n=24, cat="everyday", engine="petage", mode="dog", related=["names", "units", "timer"],
 en=dict(slug="dog-cat-age-in-human-years", title="Dog and Cat Age in Human Years Calculator", h1="Dog and Cat Age in Human Years",
  desc="How old is your dog or cat in human years? Instant answer by size, with the vet chart and the DNA-based formula, plus your pet's life stage.",
  intro="Enter your pet's age and see it in human years, with its life stage. For dogs, size matters: big dogs age faster.",
  steps=["Choose dog or cat. For dogs, choose the adult size.", "Type the age in years and months.", "See the age in human years and the life stage."],
  body="""<p>The "multiply by 7" rule is a myth. The first year of a dog or cat equals about 15 human years and the second adds about 9. After that, a cat adds about 4 years per year, and a dog 4 to 7 depending on size. For dogs we also show the 2019 UC San Diego DNA formula (16 × ln(age) + 31) as a second opinion.</p>
<p>More pet tools, guides and gifts at <a href="https://cozypawsgifts.pages.dev/" rel="noopener">Cozy Paws</a>.</p>""",
  faq=[("How old is a 10 year old dog in human years?", "About 56 for a small dog, 64 for a medium dog and 72 for a large dog."),
       ("How old is a 15 year old cat?", "About 76 in human years."),
       ("When is a pet a senior?", "Small dogs around 10, large dogs around 7, and cats from about 11.")]),
 es=dict(slug="edad-de-perro-y-gato-en-anos-humanos", title="Edad de tu perro o gato en años humanos (calculadora)", h1="Edad de perro y gato en años humanos",
  desc="¿Cuántos años humanos tiene tu perro o tu gato? Respuesta al instante según el tamaño, con la tabla veterinaria y la fórmula de ADN, más la etapa de vida.",
  intro="Escribe la edad de tu mascota y mírala en años humanos, con su etapa de vida. En perros importa el tamaño: los grandes envejecen más rápido.",
  steps=["Elige perro o gato. Para perros, elige el tamaño de adulto.", "Escribe la edad en años y meses.", "Mira la edad en años humanos y la etapa de vida."],
  body="""<p>La regla de "multiplicar por 7" es un mito. El primer año de un perro o un gato equivale a unos 15 años humanos y el segundo suma unos 9. Después, un gato suma unos 4 años por año, y un perro entre 4 y 7 según el tamaño. Para perros también mostramos la fórmula de ADN de UC San Diego de 2019 (16 × ln(edad) + 31) como segunda opinión.</p>
<p>Más herramientas, guías y regalos para mascotas en <a href="https://cozypawsgifts.pages.dev/" rel="noopener">Cozy Paws</a> (en inglés).</p>""",
  faq=[("¿Cuántos años humanos tiene un perro de 10 años?", "Unos 56 si es chico, 64 si es mediano y 72 si es grande."),
       ("¿Y un gato de 15 años?", "Unos 76 años humanos."),
       ("¿Cuándo una mascota es mayor?", "Los perros chicos alrededor de los 10 años, los grandes alrededor de los 7, y los gatos desde los 11 más o menos.")])),

dict(id="invoice", n=25, cat="work", engine="invoice", related=["palette", "tz", "units"],
 en=dict(slug="invoice-generator", title="Free Invoice Generator: Make a PDF Invoice in 1 Minute", h1="Free Invoice Generator",
  desc="Create a simple, professional invoice and save it as PDF. Add items, tax and discount, choose the currency. Free, no sign-up, your data stays on your device.",
  intro="Fill in your details, your client and the items, and save a clean invoice as PDF. No account and no watermark.",
  steps=["Write your details and your client's details.", "Add the items with quantity and price. Add discount and tax if needed.", "Tap Download PDF / Print and choose 'Save as PDF' as the printer."],
  body="""<h2>What a basic invoice should include</h2><ul><li>Your name or business name and contact.</li><li>The client's name.</li><li>An invoice number (one that never repeats) and the date.</li><li>What you did or sold, quantity and price.</li><li>Total, due date and how to pay.</li></ul><p>Your details are not saved or sent anywhere. Keep a copy of every PDF for your taxes. This tool makes simple invoices and is not tax advice.</p>""",
  faq=[("How do I save it as PDF on my phone?", "Tap Download PDF / Print. On iPhone, pinch out on the preview or use Share > Save to Files. On Android, choose 'Save as PDF' as the printer."),
       ("Do I need to charge sales tax?", "It depends on your state and what you sell. Services are often exempt and products usually are not. Check your state's tax website."),
       ("Is my information saved?", "No. Everything stays in your browser and disappears when you close the page.")]),
 es=dict(slug="generador-de-facturas", title="Generador de facturas gratis: crea una factura en PDF en 1 minuto", h1="Generador de facturas gratis",
  desc="Crea una factura simple y profesional y guárdala en PDF. Agrega ítems, impuesto y descuento, y elige la moneda. Gratis, sin registro y tus datos quedan en tu dispositivo.",
  intro="Completa tus datos, los de tu cliente y los ítems, y guarda una factura prolija en PDF. Sin cuenta y sin marca de agua.",
  steps=["Escribe tus datos y los de tu cliente.", "Agrega los ítems con cantidad y precio. Suma descuento e impuesto si hace falta.", "Toca Descargar PDF / Imprimir y elige 'Guardar como PDF' como impresora."],
  body="""<h2>Qué debe tener una factura básica</h2><ul><li>Tu nombre o el de tu negocio y un contacto.</li><li>El nombre del cliente.</li><li>Un número de factura (que nunca se repita) y la fecha.</li><li>Qué hiciste o vendiste, cantidad y precio.</li><li>Total, vencimiento y forma de pago.</li></ul><p>Tus datos no se guardan ni se envían. Guarda una copia de cada PDF para tus impuestos. Esta herramienta hace facturas simples (recibos o "invoices"); no reemplaza la factura electrónica oficial que piden algunos países, como el CFDI en México.</p>""",
  faq=[("¿Cómo la guardo en PDF desde el celular?", "Toca Descargar PDF / Imprimir. En iPhone usa Compartir > Guardar en Archivos. En Android elige 'Guardar como PDF' como impresora."),
       ("¿Sirve como factura fiscal en México, Argentina o Colombia?", "No. En esos países la factura oficial es electrónica y la emite el sistema de impuestos. Esta sirve como invoice en EE. UU. y como presupuesto o recibo."),
       ("¿Se guardan mis datos?", "No. Todo queda en tu navegador y se borra al cerrar la página.")])),
]

BY_ID = {x["id"]: x for x in TOOLS}
