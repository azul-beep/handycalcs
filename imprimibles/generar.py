#!/usr/bin/env python3
"""Generador de imprimibles automaticos (todo por codigo, sin IA).

Subcomandos:
  python3 generar.py inicial                 primera tanda: 20 para colorear, 20 fichas, juegos 30 dias
  python3 generar.py diario                  lo que corre todos los dias (GitHub Actions):
                                             juego del dia + rellenar cola de colorear y fichas
                                             + rehacer indices, sitemap y rss (goteo 2-3 por dia)
  python3 generar.py semanal [--cantidad 7]  agrega N paginas para colorear y N fichas a la cola
  python3 generar.py colorear [--agregar N]  solo el sitio de colorear
  python3 generar.py fichas [--agregar N]    solo las fichas bilingues
  python3 generar.py juego [--dias 30]       solo el juego del dia
  python3 generar.py reconstruir             rehace HTML, sitemap y RSS sin generar nada nuevo
  python3 generar.py descartar colorear 7    saca el item numero 7 (si salio feo) y no lo vuelve a usar

Opcion global: --hoy AAAA-MM-DD para simular otra fecha.
Todo es idempotente: correrlo dos veces el mismo dia no duplica nada.
"""
import argparse
import os
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--hoy", help="fecha a simular (AAAA-MM-DD)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("inicial")
    d = sub.add_parser("diario")
    d.add_argument("--buffer", type=int, default=7, help="dias de cola a mantener listos (default 7)")
    s = sub.add_parser("semanal")
    s.add_argument("--cantidad", type=int, default=7)
    c = sub.add_parser("colorear")
    c.add_argument("--agregar", type=int, default=0)
    f = sub.add_parser("fichas")
    f.add_argument("--agregar", type=int, default=0)
    j = sub.add_parser("juego")
    j.add_argument("--dias", type=int, default=30)
    sub.add_parser("reconstruir")
    x = sub.add_parser("descartar")
    x.add_argument("paquete", choices=["colorear", "fichas"])
    x.add_argument("numero", type=int)
    a = ap.parse_args()
    if a.hoy:
        os.environ["IMPRIMIBLES_HOY"] = a.hoy

    from motor import colorear, fichas, juego, portada
    from motor.comun import hoy

    print(f"Fecha: {hoy().isoformat()}")
    if a.cmd == "inicial":
        colorear.agregar(cantidad=max(0, 20 - len(_items("colorear"))))
        fichas.agregar(cantidad=max(0, 20 - len(_items("fichas-bilingues"))))
        juego.construir(30)
    elif a.cmd == "diario":
        juego.construir(30)
        colorear.agregar(dias_buffer=a.buffer)
        fichas.agregar(dias_buffer=a.buffer)
    elif a.cmd == "semanal":
        colorear.agregar(cantidad=a.cantidad)
        fichas.agregar(cantidad=a.cantidad)
    elif a.cmd == "colorear" and a.agregar:
        colorear.agregar(cantidad=a.agregar)
    elif a.cmd == "fichas" and a.agregar:
        fichas.agregar(cantidad=a.agregar)
    elif a.cmd == "juego":
        juego.construir(a.dias)
    elif a.cmd == "descartar":
        _descartar(a.paquete, a.numero)

    # siempre se rehacen indices, sitemap y rss (es barato e idempotente)
    if a.cmd in ("inicial", "diario", "semanal", "colorear", "reconstruir", "descartar"):
        colorear.construir_sitio()
    if a.cmd in ("inicial", "diario", "semanal", "fichas", "reconstruir", "descartar"):
        fichas.construir()
    if a.cmd == "reconstruir":
        juego.construir(0)
    portada.construir()
    print("Listo.")


def _items(paq):
    from motor.comun import cargar
    return cargar(paq)["items"]


def _descartar(paquete, n):
    from motor.comun import RAIZ, cargar, guardar
    paq = "colorear" if paquete == "colorear" else "fichas-bilingues"
    datos = cargar(paq)
    it = next((x for x in datos["items"] if x["n"] == n), None)
    datos.setdefault("descartados", [])
    if n not in datos["descartados"]:
        datos["descartados"].append(n)
    if it:
        datos["items"].remove(it)
        for p in (RAIZ / paq).rglob("*"):
            if p.is_file() and p.stem in (it["slug"], it["slug"] + "-mini"):
                p.unlink()
        print(f"Descartado {paq} n.º {n} ({it['slug']}).")
    guardar(paq, datos)


if __name__ == "__main__":
    main()
