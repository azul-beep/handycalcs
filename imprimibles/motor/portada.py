"""Pagina /imprimibles/ de Handy Calcs que junta juego del dia y fichas bilingues."""
from .comun import RAIZ, cfg, escribir, pagina_html


def construir():
    c = cfg()
    B = c["base_url"]
    cuerpo = f"""
<p>Imprimibles gratis para toda la familia: un juego nuevo cada día y fichas bilingües para los más chicos.</p>
<ul class="grilla">
<li><a href="{B}/juego-del-dia/"><img src="{B}/juego-del-dia/portada.jpg" width="400" height="600" alt="Sudoku y sopa de letras del día para imprimir"><span>Juego del día: sudoku y sopa de letras</span></a></li>
<li><a href="{B}/fichas-bilingues/"><img src="{B}/fichas-bilingues/portada.jpg" width="400" height="600" alt="Fichas bilingües español-inglés para niños"><span>Fichas bilingües español–inglés</span></a></li>
</ul>
<p>Suscríbete por RSS: <a href="{B}/juego-del-dia/rss.xml">juego del día</a> · <a href="{B}/fichas-bilingues/rss.xml">fichas bilingües</a>.</p>
"""
    escribir(RAIZ / "index.html", pagina_html(
        titulo="Imprimibles gratis: sudoku del día y fichas bilingües para niños",
        descripcion="Imprimibles gratis en PDF: sudoku y sopa de letras nuevos cada día y fichas bilingües español-inglés para niños de 3 a 7 años.",
        h1="Imprimibles gratis", canonical=f"{B}/", cuerpo=cuerpo))
    # portadas: copia de la miniatura mas reciente publicada
    import shutil
    from datetime import date
    from .comun import cargar, hoy, liberados
    j = sorted((RAIZ / "juego-del-dia" / "img").glob("*-mini.jpg"))
    pub = [p for p in j if date.fromisoformat(p.name[14:24]) <= hoy()] or j
    if pub:
        shutil.copy(pub[-1], RAIZ / "juego-del-dia" / "portada.jpg")
    fl = liberados(cargar("fichas-bilingues")["items"], "fichas-bilingues") or cargar("fichas-bilingues")["items"]
    if fl:
        shutil.copy(RAIZ / "fichas-bilingues" / "archivos" / f"{fl[-1]['slug']}-mini.jpg",
                    RAIZ / "fichas-bilingues" / "portada.jpg")
