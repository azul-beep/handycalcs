"""Paquete juego-del-dia/: sudoku (3 niveles) + sopa de letras en español, uno por dia."""
import json
import random
import unicodedata
from datetime import date, timedelta

from .comun import (RAIZ, a_pdf, a_png, carta_svg, cfg, esc, escribir, hoy, miniatura,
                    pagina_html, preview_pin, rss)

PAQ = "juego-del-dia"
DIR = RAIZ / PAQ

DIAS = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre",
         "octubre", "noviembre", "diciembre"]


def fecha_larga(d):
    return f"{DIAS[d.weekday()]} {d.day} de {MESES[d.month - 1]} de {d.year}"


# ===========================================================================
# SUDOKU
# ===========================================================================
TODOS = 0x3FE  # bits 1..9


def _bits(m):
    while m:
        b = m & -m
        yield b.bit_length() - 1
        m ^= b


def _candidatos(g):
    filas = [0] * 9
    cols = [0] * 9
    cajas = [0] * 9
    for i, v in enumerate(g):
        if v:
            r, c = divmod(i, 9)
            b = 1 << v
            filas[r] |= b
            cols[c] |= b
            cajas[(r // 3) * 3 + c // 3] |= b
    return filas, cols, cajas


def contar_soluciones(g, limite=2):
    g = list(g)
    filas, cols, cajas = _candidatos(g)
    vacias = [i for i, v in enumerate(g) if v == 0]
    cuenta = 0

    def rec():
        nonlocal cuenta
        mejor = None
        mejor_m = 0
        mejor_n = 10
        for i in vacias:
            if g[i]:
                continue
            r, c = divmod(i, 9)
            m = TODOS & ~(filas[r] | cols[c] | cajas[(r // 3) * 3 + c // 3])
            n = bin(m).count("1")
            if n == 0:
                return
            if n < mejor_n:
                mejor, mejor_m, mejor_n = i, m, n
                if n == 1:
                    break
        if mejor is None:
            cuenta += 1
            return
        r, c = divmod(mejor, 9)
        k = (r // 3) * 3 + c // 3
        for v in _bits(mejor_m):
            b = 1 << v
            g[mejor] = v
            filas[r] |= b
            cols[c] |= b
            cajas[k] |= b
            rec()
            filas[r] ^= b
            cols[c] ^= b
            cajas[k] ^= b
            g[mejor] = 0
            if cuenta >= limite:
                return

    rec()
    return cuenta


def _llena(rng):
    g = [0] * 81

    def rec(i):
        if i == 81:
            return True
        r, c = divmod(i, 9)
        usados = set(g[r * 9:(r + 1) * 9]) | {g[k * 9 + c] for k in range(9)}
        br, bc = (r // 3) * 3, (c // 3) * 3
        usados |= {g[(br + a) * 9 + bc + b] for a in range(3) for b in range(3)}
        vals = [v for v in range(1, 10) if v not in usados]
        rng.shuffle(vals)
        for v in vals:
            g[i] = v
            if rec(i + 1):
                return True
        g[i] = 0
        return False

    rec(0)
    return g


def resolver_simple(g):
    """Solo singles desnudos y ocultos. Devuelve True si alcanza para resolverlo."""
    g = list(g)
    unidades = ([[r * 9 + c for c in range(9)] for r in range(9)] +
                [[r * 9 + c for r in range(9)] for c in range(9)] +
                [[(br + a) * 9 + bc + b for a in range(3) for b in range(3)] for br in (0, 3, 6) for bc in (0, 3, 6)])
    while True:
        filas, cols, cajas = _candidatos(g)
        cand = {}
        for i in range(81):
            if not g[i]:
                r, c = divmod(i, 9)
                cand[i] = TODOS & ~(filas[r] | cols[c] | cajas[(r // 3) * 3 + c // 3])
        if not cand:
            return True
        avance = False
        for i, m in cand.items():
            if m and m & (m - 1) == 0:
                g[i] = m.bit_length() - 1
                avance = True
        if not avance:
            for u in unidades:
                for v in range(1, 10):
                    b = 1 << v
                    lugares = [i for i in u if i in cand and cand[i] & b]
                    if len(lugares) == 1 and not g[lugares[0]]:
                        g[lugares[0]] = v
                        avance = True
        if not avance:
            return False


NIVELES = {"facil": ("Fácil", 38), "medio": ("Medio", 30), "dificil": ("Difícil", 24)}


def sudoku(rng, nivel):
    objetivo = NIVELES[nivel][1]
    for _ in range(40):
        sol = _llena(rng)
        g = list(sol)
        celdas = list(range(41))  # pares simetricos (i, 80-i)
        rng.shuffle(celdas)
        pistas = 81
        for i in celdas:
            if pistas <= objetivo:
                break
            j = 80 - i
            a, b = g[i], g[j]
            g[i] = g[j] = 0
            quitadas = 1 if i == j else 2
            ok = contar_soluciones(g) == 1
            if ok and nivel != "dificil":
                ok = resolver_simple(g)
            if ok:
                pistas -= quitadas
            else:
                g[i], g[j] = a, b
        if nivel == "dificil":
            if pistas <= objetivo + 4 and not resolver_simple(g):
                return g, sol
        elif pistas <= objetivo + 2:
            return g, sol
    return g, sol


# ===========================================================================
# SOPA DE LETRAS
# ===========================================================================
TEMAS = {
    "Animales de la granja": "VACA CABALLO OVEJA CERDO GALLINA PATO CABRA CONEJO BURRO GALLO PAVO TERNERO POLLITO GANSO",
    "Frutas": "MANZANA BANANA NARANJA PERA UVA FRESA KIWI MANGO SANDIA MELON DURAZNO CEREZA LIMON PIÑA CIRUELA",
    "Verduras": "ZANAHORIA PAPA TOMATE LECHUGA CEBOLLA CALABAZA PEPINO ESPINACA ACELGA REPOLLO BROCOLI MAIZ AJO APIO",
    "Colores": "ROJO AZUL VERDE AMARILLO NARANJA VIOLETA ROSA BLANCO NEGRO GRIS MARRON CELESTE TURQUESA DORADO",
    "Países de América": "ARGENTINA URUGUAY CHILE PERU MEXICO BRASIL BOLIVIA PARAGUAY COLOMBIA ECUADOR CUBA PANAMA HONDURAS CANADA",
    "Profesiones": "MEDICO MAESTRA BOMBERO PANADERO CARPINTERO ENFERMERA PILOTO CHEF ABOGADA DENTISTA PINTOR CARTERO JUEZ",
    "Deportes": "FUTBOL TENIS BEISBOL RUGBY NATACION BOXEO HOCKEY VOLEY BASQUET GOLF CICLISMO KARATE ATLETISMO REMO",
    "En la cocina": "OLLA SARTEN CUCHARA TENEDOR CUCHILLO PLATO VASO TAZA HORNO BATIDORA LICUADORA JARRA MANTEL BATIDOR",
    "Naturaleza": "ARBOL RIO MONTAÑA LAGO BOSQUE FLOR HOJA PIEDRA NUBE LLUVIA VOLCAN CASCADA PRADERA ARENA",
    "La escuela": "LAPIZ GOMA REGLA CUADERNO MOCHILA PIZARRA TIZA LIBRO RECREO MAESTRA AULA TIJERA CARTUCHERA",
    "Transportes": "AUTO TREN AVION BARCO BICICLETA MOTO AUTOBUS CAMION METRO HELICOPTERO VELERO TAXI TRANVIA",
    "Instrumentos": "GUITARRA PIANO BATERIA VIOLIN FLAUTA TROMPETA ARPA BOMBO UKELELE ACORDEON SAXO MARACAS CELLO",
    "El cuerpo": "CABEZA MANO PIE BRAZO PIERNA RODILLA CODO OREJA NARIZ BOCA OJO HOMBRO ESPALDA DEDO",
    "La ropa": "CAMISA PANTALON VESTIDO FALDA CALCETINES ZAPATO BUFANDA GORRO CHAQUETA CAMISETA GUANTES BOTAS SACO",
    "El clima": "SOL LLUVIA VIENTO NIEVE NUBE TORMENTA RAYO NIEBLA GRANIZO CALOR FRIO HUMEDAD ARCOIRIS HELADA",
    "En la casa": "COCINA BAÑO SALA DORMITORIO PATIO PUERTA VENTANA TECHO ESCALERA BALCON GARAJE PASILLO JARDIN",
    "El mar": "OLA PLAYA ARENA BALLENA DELFIN PULPO CANGREJO TIBURON ESTRELLA ALGA CORAL CARACOL MEDUSA FARO",
    "El espacio": "PLANETA ESTRELLA LUNA SOL COMETA COHETE GALAXIA MARTE JUPITER SATURNO ORBITA ASTRONAUTA METEORO",
    "Emociones": "ALEGRIA TRISTEZA MIEDO ENOJO CALMA SORPRESA AMOR VERGUENZA ORGULLO TERNURA NERVIOS PAZ ILUSION",
    "Animales salvajes": "LEON TIGRE JIRAFA CEBRA ELEFANTE MONO OSO LOBO ZORRO PUMA HIPOPOTAMO CANGURO JAGUAR KOALA",
    "Postres": "FLAN HELADO TORTA ALFAJOR BUDIN MOUSSE BROWNIE CHURRO TARTA GELATINA PANQUEQUE GALLETAS VOLCAN",
    "Juegos de mesa": "AJEDREZ DAMAS DOMINO MEMORIA NAIPES DADOS LOTERIA BINGO MONOPOLY UNO CARTAS PUZZLE TABLERO",
    "Herramientas": "MARTILLO SERRUCHO TALADRO PINZA TORNILLO CLAVO LIJA LLAVE METRO NIVEL DESTORNILLADOR PALA",
    "Pájaros": "PERICO COLIBRI LORO AGUILA BUHO PALOMA GORRION CONDOR PINGUINO TUCAN CARDENAL GAVIOTA PATO",
    "Flores": "ROSA MARGARITA GIRASOL TULIPAN JAZMIN CLAVEL LIRIO ORQUIDEA LAVANDA AMAPOLA AZUCENA VIOLETA DALIA",
}
ESPECIALES = {
    (11, 26): ("Acción de Gracias", "PAVO FAMILIA GRACIAS CENA MAIZ CALABAZA OTOÑO MESA PASTEL HOJAS ABRAZO AMIGOS"),
    (12, 8): ("Arbolito de Navidad", "ARBOL ESTRELLA GUIRNALDA ADORNO LUCES REGALO PESEBRE ANGEL CAMPANA BOTA MOÑO"),
    (12, 24): ("Nochebuena", "NAVIDAD REGALO BRINDIS FAMILIA ESTRELLA DUENDE RENO TRINEO TURRON SIDRA PESEBRE"),
    (12, 31): ("Año Nuevo", "BRINDIS DESEOS FUEGOS CUENTA ABRAZO FIESTA RELOJ SIDRA CALENDARIO METAS FAMILIA"),
}
DIRECCIONES = [(0, 1), (1, 0), (1, 1), (-1, 1), (0, -1), (-1, 0), (1, -1), (-1, -1)]
RELLENO = "AAAAAEEEEEOOOOIIIUUSSSRRRNNNLLLDDTTCCMMPPBGVYQHFZJÑX"


def _sin_tildes(p):
    p = p.replace("Ñ", "\0")
    p = "".join(ch for ch in unicodedata.normalize("NFD", p) if unicodedata.category(ch) != "Mn")
    return p.replace("\0", "Ñ")


def sopa(rng, d, n=12, cantidad=10):
    if (d.month, d.day) in ESPECIALES:
        tema, palabras = ESPECIALES[(d.month, d.day)]
    elif d.month == 12 and d.day < 24 and d.weekday() == 4:
        tema, palabras = ("Navidad", "NAVIDAD REGALO ESTRELLA PESEBRE RENO TRINEO CAMPANA VELA ARBOLITO "
                          "DUENDE LUCES ADORNO CORONA")
    else:
        temas = sorted(TEMAS)
        tema = temas[(d.toordinal() * 7) % len(temas)]
        palabras = TEMAS[tema]
    lista = [_sin_tildes(p) for p in palabras.split() if len(p) <= n]
    for _ in range(200):
        rng.shuffle(lista)
        elegidas = sorted(lista[:cantidad], key=len, reverse=True)
        g = [[""] * n for _ in range(n)]
        pos = {}
        ok = True
        for p in elegidas:
            colocada = False
            intentos = [(r, c, dr, dc) for r in range(n) for c in range(n) for dr, dc in DIRECCIONES]
            rng.shuffle(intentos)
            for r, c, dr, dc in intentos:
                er, ec = r + dr * (len(p) - 1), c + dc * (len(p) - 1)
                if not (0 <= er < n and 0 <= ec < n):
                    continue
                if all(g[r + dr * k][c + dc * k] in ("", p[k]) for k in range(len(p))):
                    for k in range(len(p)):
                        g[r + dr * k][c + dc * k] = p[k]
                    pos[p] = (r, c, er, ec)
                    colocada = True
                    break
            if not colocada:
                ok = False
                break
        if ok:
            for r in range(n):
                for c in range(n):
                    if not g[r][c]:
                        g[r][c] = rng.choice(RELLENO)
            orden = sorted(elegidas)
            return {"tema": tema, "grilla": ["".join(f) for f in g], "palabras": orden,
                    "pos": {p: pos[p] for p in orden}}
    raise RuntimeError("no se pudo armar la sopa")


# ===========================================================================
# Generar un dia
# ===========================================================================
def datos_dia(d):
    rng = random.Random(d.toordinal() * 31 + 7)
    out = {"fecha": d.isoformat(), "sudokus": {}}
    for nivel in NIVELES:
        p, s = sudoku(rng, nivel)
        out["sudokus"][nivel] = {"p": "".join(map(str, p)), "s": "".join(map(str, s))}
    out["sopa"] = sopa(rng, d)
    return out


def _svg_sudoku(x, y, cel, p, s=None):
    o = [f'<rect x="{x}" y="{y}" width="{cel * 9}" height="{cel * 9}" fill="#fff" stroke="#000" stroke-width="3"/>']
    for k in range(1, 9):
        w = 2.4 if k % 3 == 0 else 0.9
        o.append(f'<line x1="{x + k * cel}" y1="{y}" x2="{x + k * cel}" y2="{y + 9 * cel}" stroke="#000" stroke-width="{w}"/>')
        o.append(f'<line x1="{x}" y1="{y + k * cel}" x2="{x + 9 * cel}" y2="{y + k * cel}" stroke="#000" stroke-width="{w}"/>')
    for i in range(81):
        r, c = divmod(i, 9)
        v = p[i]
        col = "#000"
        if v == "0":
            if not s:
                continue
            v = s[i]
            col = "#6a8fb0"
        o.append(f'<text x="{x + c * cel + cel / 2:.1f}" y="{y + r * cel + cel * 0.72:.1f}" text-anchor="middle" '
                 f'font-family="Inter" font-weight="{600 if col == "#000" else 500}" font-size="{cel * 0.62:.1f}" fill="{col}">{v}</text>')
    return "\n".join(o)


def _svg_sopa(x, y, cel, sp, soluciones=False):
    n = len(sp["grilla"])
    o = [f'<rect x="{x}" y="{y}" width="{cel * n}" height="{cel * n}" rx="8" fill="#fff" stroke="#000" stroke-width="2.4"/>']
    if soluciones:
        for p, (r, c, er, ec) in sp["pos"].items():
            o.append(f'<line x1="{x + c * cel + cel / 2:.1f}" y1="{y + r * cel + cel / 2:.1f}" x2="{x + ec * cel + cel / 2:.1f}" '
                     f'y2="{y + er * cel + cel / 2:.1f}" stroke="#f4c542" stroke-opacity="0.75" stroke-width="{cel * 0.78:.1f}" stroke-linecap="round"/>')
    for r, fila in enumerate(sp["grilla"]):
        for c, ch in enumerate(fila):
            o.append(f'<text x="{x + c * cel + cel / 2:.1f}" y="{y + r * cel + cel * 0.7:.1f}" text-anchor="middle" '
                     f'font-family="DejaVu Sans Mono" font-weight="bold" font-size="{cel * 0.6:.1f}">{ch}</text>')
    return "\n".join(o)


def _pagina_pdf(dd, soluciones):
    c = cfg()
    d = date.fromisoformat(dd["fecha"])
    cel = 38
    o = [f'<text x="50" y="72" font-family="Inter" font-weight="800" font-size="30">Juego del día</text>',
         f'<text x="50" y="104" font-family="Inter" font-size="19" fill="#444">{esc(fecha_larga(d).capitalize())}'
         f'{" · SOLUCIONES" if soluciones else ""}</text>',
         f'<text x="800" y="72" text-anchor="end" font-family="Inter" font-weight="600" font-size="15" fill="#666">{esc(c["sitio"])}</text>',
         '<line x1="50" y1="120" x2="800" y2="120" stroke="#000" stroke-width="1.5"/>']
    pos = {"facil": (50, 170), "medio": (458, 170), "dificil": (50, 590)}
    for nivel, (x, y) in pos.items():
        o.append(f'<text x="{x}" y="{y - 14}" font-family="Inter" font-weight="700" font-size="19">Sudoku · {NIVELES[nivel][0]}</text>')
        sd = dd["sudokus"][nivel]
        o.append(_svg_sudoku(x, y, cel, sd["p"], sd["s"] if soluciones else None))
    sp = dd["sopa"]
    o.append(f'<text x="458" y="576" font-family="Inter" font-weight="700" font-size="19">Sopa de letras: {esc(sp["tema"])}</text>')
    o.append(_svg_sopa(458, 590, 28.5, sp, soluciones))
    for k, p in enumerate(sp["palabras"]):
        cx = 458 + (k % 2) * 175
        cy = 960 + (k // 2) * 24
        o.append(f'<rect x="{cx}" y="{cy - 13}" width="13" height="13" fill="none" stroke="#000" stroke-width="1.2"/>')
        o.append(f'<text x="{cx + 20}" y="{cy}" font-family="Inter" font-size="16">{p}</text>')
    if not soluciones:
        o.append('<text x="50" y="975" font-family="Inter" font-weight="700" font-size="15">Cómo se juega</text>')
        txt = ["Sudoku: completa cada fila, columna y cuadro de 3×3",
               "con los números del 1 al 9, sin repetir.",
               "Sopa de letras: busca las palabras en todas las",
               "direcciones (también al revés y en diagonal).",
               "Soluciones en la página 2."]
        for k, t in enumerate(txt):
            o.append(f'<text x="50" y="{1000 + k * 20}" font-family="Inter" font-size="14" fill="#333">{esc(t)}</text>')
    o.append(f'<text x="425" y="1075" text-anchor="middle" font-family="Inter" font-size="12" fill="#888">'
             f'{esc(c["base_url"])}/juego-del-dia/ · gratis para uso personal</text>')
    return "\n".join(o)


def generar_dia(d, forzar=False):
    DIR.mkdir(parents=True, exist_ok=True)
    jp = DIR / "datos" / f"{d.isoformat()}.json"
    if jp.exists() and not forzar:
        return json.loads(jp.read_text(encoding="utf-8"))
    dd = datos_dia(d)
    escribir(jp, json.dumps(dd, ensure_ascii=False))
    p1 = _pagina_pdf(dd, False)
    p2 = _pagina_pdf(dd, True)
    (DIR / "pdf").mkdir(exist_ok=True)
    a_pdf([carta_svg(p1), carta_svg(p2)], DIR / "pdf" / f"juego-del-dia-{d.isoformat()}.pdf")
    (DIR / "img").mkdir(exist_ok=True)
    pv = preview_pin(p1, "Sudoku y sopa de letras", f"{d.day} de {MESES[d.month - 1]} · con soluciones",
                     "#eef3f8", "#24476b")
    a_png(pv, DIR / "img" / f"juego-del-dia-{d.isoformat()}.png", 1000, 1500)
    miniatura(DIR / "img" / f"juego-del-dia-{d.isoformat()}.png", DIR / "img" / f"juego-del-dia-{d.isoformat()}-mini.jpg")
    print(f"  juego-del-dia: {d.isoformat()}")
    return dd


# ===========================================================================
# HTML
# ===========================================================================
JS = r"""
<script>
const D = __DATOS__;
function armarSudoku(id){
  const sd = D.sudokus[id], t = document.getElementById('sd-'+id);
  for(let i=0;i<81;i++){
    const inp=document.createElement('input');
    inp.inputMode='numeric'; inp.maxLength=1; inp.setAttribute('aria-label','Fila '+(Math.floor(i/9)+1)+' columna '+(i%9+1));
    const r=Math.floor(i/9), c=i%9;
    if(c%3==2&&c<8) inp.classList.add('bd'); if(r%3==2&&r<8) inp.classList.add('bb');
    if(sd.p[i]!=='0'){inp.value=sd.p[i]; inp.readOnly=true; inp.classList.add('dado');}
    inp.addEventListener('input',()=>{inp.value=inp.value.replace(/[^1-9]/g,''); inp.classList.remove('mal');});
    t.appendChild(inp);
  }
}
function comprobar(id){
  const sd=D.sudokus[id], ins=document.querySelectorAll('#sd-'+id+' input'); let vacias=0, mal=0;
  ins.forEach((inp,i)=>{ if(!inp.value){vacias++;return;} if(inp.value!==sd.s[i]){inp.classList.add('mal');mal++;} });
  document.getElementById('msg-'+id).textContent = mal? ('Hay '+mal+' casilla(s) para revisar.') : (vacias? 'Vas bien. Faltan '+vacias+'.' : '¡Resuelto! Felicitaciones.');
}
function solucion(id){ const sd=D.sudokus[id]; document.querySelectorAll('#sd-'+id+' input').forEach((inp,i)=>{inp.value=sd.s[i];inp.classList.remove('mal');}); }
// sopa de letras
let ini=null;
function armarSopa(){
  const g=D.sopa.grilla, n=g.length, t=document.getElementById('sopa');
  t.style.gridTemplateColumns='repeat('+n+',1fr)';
  for(let r=0;r<n;r++) for(let c=0;c<n;c++){
    const b=document.createElement('button'); b.textContent=g[r][c]; b.dataset.r=r; b.dataset.c=c;
    b.addEventListener('click',()=>tocar(b)); t.appendChild(b);
  }
}
function celda(r,c){return document.querySelector('#sopa button[data-r="'+r+'"][data-c="'+c+'"]');}
function tocar(b){
  const r=+b.dataset.r, c=+b.dataset.c;
  if(!ini){ini={r,c,b}; b.classList.add('sel'); return;}
  ini.b.classList.remove('sel');
  const dr=Math.sign(r-ini.r), dc=Math.sign(c-ini.c), largo=Math.max(Math.abs(r-ini.r),Math.abs(c-ini.c))+1;
  const recto = (ini.r===r||ini.c===c||Math.abs(r-ini.r)===Math.abs(c-ini.c));
  if(recto && largo>1){
    let w=''; const cs=[];
    for(let k=0;k<largo;k++){const x=celda(ini.r+dr*k, ini.c+dc*k); w+=x.textContent; cs.push(x);}
    const rev=w.split('').reverse().join('');
    for(const p of D.sopa.palabras){
      if(p===w||p===rev){ cs.forEach(x=>x.classList.add('ok')); const li=document.getElementById('p-'+p); if(li&&!li.classList.contains('hecha')){li.classList.add('hecha');}
        if(document.querySelectorAll('#lista .hecha').length===D.sopa.palabras.length) document.getElementById('msg-sopa').textContent='¡Encontraste todas!';
      }
    }
  }
  ini=null;
}
function verSopa(){ for(const p in D.sopa.pos){ const [r,c,er,ec]=D.sopa.pos[p]; const dr=Math.sign(er-r), dc=Math.sign(ec-c);
  for(let k=0;k<p.length;k++) celda(r+dr*k,c+dc*k).classList.add('ok'); document.getElementById('p-'+p).classList.add('hecha'); } }
['facil','medio','dificil'].forEach(armarSudoku); armarSopa();
</script>
"""

CSS_JUEGO = """<style>
.sudoku{display:grid;grid-template-columns:repeat(9,1fr);max-width:400px;border:3px solid #1f2a33;margin:.5rem 0}
.sudoku input{width:100%;aspect-ratio:1;text-align:center;font-size:1.25rem;border:1px solid #c5cdd3;padding:0;font-family:inherit;color:#2f6f8f;background:#fff}
.sudoku input.dado{color:#1f2a33;font-weight:700;background:#f2f4f6}.sudoku input.mal{background:#ffd9d6}
.sudoku input.bd{border-right:2px solid #1f2a33}.sudoku input.bb{border-bottom:2px solid #1f2a33}
.sopa{display:grid;max-width:480px;gap:2px;margin:.5rem 0}
.sopa button{aspect-ratio:1;border:1px solid #d6dbe0;background:#fff;font:700 1rem ui-monospace,monospace;padding:0;cursor:pointer;border-radius:4px}
.sopa button.sel{background:#ffe08a}.sopa button.ok{background:#bfe6c9}
#lista{columns:2;padding-left:1.2rem}#lista .hecha{text-decoration:line-through;color:#6b8f73}
.niveles{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:1.5rem}
.msg{font-weight:600;color:#2e6b45;min-height:1.4em}
.navdias{display:flex;justify-content:space-between;margin:1rem 0}
</style>
"""


def html_dia(dd, anterior, siguiente):
    c = cfg()
    B = c["base_url"]
    d = date.fromisoformat(dd["fecha"])
    fl = fecha_larga(d)
    sp = dd["sopa"]
    tit = f"Sudoku y sopa de letras del día – {d.day} de {MESES[d.month - 1]} de {d.year}"
    desc = (f"Juego del día del {fl}: sudoku fácil, medio y difícil, y sopa de letras de {sp['tema'].lower()}. "
            "Juega en pantalla o imprime el PDF gratis con soluciones.")
    slug = d.isoformat()
    datos_js = json.dumps({"sudokus": dd["sudokus"], "sopa": sp}, ensure_ascii=False)
    niveles = "".join(
        f'<section><h2>Sudoku {NIVELES[n][0].lower()}</h2><div class="sudoku" id="sd-{n}"></div>'
        f'<button class="boton sec" onclick="comprobar(\'{n}\')">Comprobar</button>'
        f'<button class="boton sec" onclick="solucion(\'{n}\')">Ver solución</button><p class="msg" id="msg-{n}"></p></section>'
        for n in NIVELES)
    lista = "".join(f'<li id="p-{p}">{p}</li>' for p in sp["palabras"])
    nav = '<nav class="navdias no-imprimir">'
    nav += f'<a href="{anterior}.html">&larr; Juego anterior</a>' if anterior else "<span></span>"
    nav += f'<a href="{siguiente}.html">Juego siguiente &rarr;</a>' if siguiente else "<span></span>"
    nav += "</nav>"
    cuerpo = f"""
<p>{esc(fl.capitalize())}. Tres sudokus (fácil, medio y difícil) y una sopa de letras con el tema <strong>{esc(sp['tema'])}</strong>.
Puedes jugar aquí mismo o descargar el PDF para imprimir: las soluciones están en la página 2.</p>
<p><a class="boton" href="pdf/juego-del-dia-{slug}.pdf" download>Descargar PDF para imprimir</a>
<a class="boton sec" href="./">Juego de hoy y archivo</a></p>
<div class="niveles">{niveles}</div>
<div class="anuncio"><!-- ADSENSE --></div>
<section><h2>Sopa de letras: {esc(sp['tema'])}</h2>
<p>Toca la primera y la última letra de cada palabra. Hay palabras al derecho, al revés y en diagonal.</p>
<div class="sopa" id="sopa"></div><p class="msg" id="msg-sopa"></p>
<ul id="lista">{lista}</ul>
<button class="boton sec" onclick="verSopa()">Ver solución</button></section>
<p><img src="img/juego-del-dia-{slug}-mini.jpg" width="400" height="600" loading="lazy" alt="Vista previa del PDF del juego del día: sudoku y sopa de letras de {esc(sp['tema'].lower())} del {esc(fl)}"></p>
{nav}
""" + JS.replace("__DATOS__", datos_js)
    return pagina_html(titulo=tit, descripcion=desc, h1=f"Juego del día: {d.day} de {MESES[d.month - 1]} de {d.year}",
                       canonical=f"{B}/juego-del-dia/{slug}.html", cuerpo=cuerpo,
                       imagen=f"{B}/juego-del-dia/img/juego-del-dia-{slug}.png",
                       migas=[("Imprimibles", f"{B}/"), ("Juego del día", f"{B}/juego-del-dia/"), (fl, None)],
                       extra_head=CSS_JUEGO, amazon=c["link_amazon_juegos"],
                       texto_amazon="Libros de sudoku y sopas de letras en letra grande",
                       jsonld={"@context": "https://schema.org", "@type": "Game", "name": tit, "description": desc,
                               "inLanguage": "es", "datePublished": slug})


def construir(dias_adelante=30, desde=None):
    """Genera los dias que falten (hasta hoy + dias_adelante) y reconstruye paginas, indice y RSS."""
    h = hoy()
    desde = desde or date(2026, 11, 17)
    existentes = sorted(date.fromisoformat(p.stem) for p in (DIR / "datos").glob("*.json")) if (DIR / "datos").exists() else []
    primero = min([desde] + existentes)
    d = primero
    while d <= max(h, desde) + timedelta(days=dias_adelante):
        generar_dia(d)
        d += timedelta(days=1)
    todos = sorted(date.fromisoformat(p.stem) for p in (DIR / "datos").glob("*.json"))
    publicados = [x for x in todos if x <= h]
    c = cfg()
    B = c["base_url"]
    # paginas de cada dia (todas existen; solo se enlazan las publicadas)
    for i, x in enumerate(todos):
        dd = json.loads((DIR / "datos" / f"{x.isoformat()}.json").read_text(encoding="utf-8"))
        ant = todos[i - 1].isoformat() if i > 0 else None
        sig = todos[i + 1].isoformat() if i + 1 < len(todos) and todos[i + 1] <= h else None
        html = html_dia(dd, ant, sig)
        if x > h:
            html = html.replace("<head>", '<head>\n<meta name="robots" content="noindex">', 1)
        escribir(DIR / f"{x.isoformat()}.html", html)
    # indice
    destacado = publicados[-1] if publicados else (todos[0] if todos else None)
    cuerpo = ""
    if destacado:
        dd = json.loads((DIR / "datos" / f"{destacado.isoformat()}.json").read_text(encoding="utf-8"))
        cuerpo += (f'<div class="ficha"><div><a href="{destacado.isoformat()}.html"><img src="img/juego-del-dia-{destacado.isoformat()}.png" '
                   f'width="1000" height="1500" alt="Sudoku y sopa de letras del {esc(fecha_larga(destacado))}"></a></div><div>'
                   f'<h2>{"Hoy" if destacado == h else "Próximo juego"}: {esc(fecha_larga(destacado))}</h2>'
                   f'<p>Tres sudokus (fácil, medio y difícil) y una sopa de letras de <strong>{esc(dd["sopa"]["tema"])}</strong>. '
                   f'Juégalo en pantalla o imprímelo con las soluciones en la página 2.</p>'
                   f'<p><a class="boton" href="{destacado.isoformat()}.html">Jugar ahora</a>'
                   f'<a class="boton sec" href="pdf/juego-del-dia-{destacado.isoformat()}.pdf" download>PDF para imprimir</a></p>'
                   f'<p>Todos los días hay un juego nuevo. Síguenos por <a href="rss.xml">RSS</a> o en Pinterest.</p></div></div>')
    if publicados:
        cuerpo += "<h2>Archivo de juegos</h2>"
        meses = {}
        for x in reversed(publicados):
            meses.setdefault((x.year, x.month), []).append(x)
        for (a, m), xs in meses.items():
            cuerpo += f"<h3>{MESES[m - 1].capitalize()} {a}</h3><ol>"
            cuerpo += "".join(f'<li><a href="{x.isoformat()}.html">{esc(fecha_larga(x).capitalize())}</a></li>' for x in xs)
            cuerpo += "</ol>"
    html = pagina_html(titulo="Sudoku y sopa de letras del día gratis para imprimir (con soluciones)",
                       descripcion="Un sudoku fácil, medio y difícil y una sopa de letras nueva todos los días. Juega online o imprime el PDF gratis con soluciones.",
                       h1="Juego del día: sudoku y sopa de letras", canonical=f"{B}/juego-del-dia/", cuerpo=cuerpo,
                       imagen=f"{B}/juego-del-dia/img/juego-del-dia-{destacado.isoformat()}.png" if destacado else None,
                       migas=[("Imprimibles", f"{B}/"), ("Juego del día", None)], amazon=c["link_amazon_juegos"],
                       texto_amazon="Libros de sudoku y sopas de letras en letra grande")
    escribir(DIR / "index.html", html)
    items = []
    for x in reversed(publicados[-50:]):
        dd = json.loads((DIR / "datos" / f"{x.isoformat()}.json").read_text(encoding="utf-8"))
        items.append({"titulo": f"Sudoku y sopa de letras del día – {x.day} de {MESES[x.month - 1]} (PDF gratis)",
                      "link": f"{B}/juego-del-dia/{x.isoformat()}.html",
                      "descripcion": f"Sudoku fácil, medio y difícil + sopa de letras de {dd['sopa']['tema'].lower()}. Para jugar online o imprimir, con soluciones.",
                      "imagen": f"{B}/juego-del-dia/img/juego-del-dia-{x.isoformat()}.png", "fecha": x,
                      "guid": f"juego-del-dia-{x.isoformat()}"})
    rss(titulo="Juego del día – sudoku y sopa de letras", link=f"{B}/juego-del-dia/",
        descripcion="Un sudoku y una sopa de letras nuevos cada día, gratis para imprimir.", items=items,
        destino=DIR / "rss.xml", self_url=f"{B}/juego-del-dia/rss.xml")
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
          f"<url><loc>{esc(B)}/juego-del-dia/</loc><lastmod>{publicados[-1].isoformat() if publicados else h.isoformat()}</lastmod></url>"]
    sm += [f"<url><loc>{esc(B)}/juego-del-dia/{x.isoformat()}.html</loc><lastmod>{x.isoformat()}</lastmod></url>" for x in publicados]
    sm.append("</urlset>\n")
    escribir(DIR / "sitemap.xml", "\n".join(sm))
    print(f"  juego-del-dia: {len(todos)} días generados, {len(publicados)} publicados")
