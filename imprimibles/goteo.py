#!/usr/bin/env python3
"""Publicación en goteo (regla de Azu, 14 nov 2026): 2 o 3 cosas por día, nunca todo junto.

Toma un RSS "completo" (todos los items) y escribe el RSS público solo con los items
que ya les tocó salir. Corre una vez por día (tarea programada o GitHub Actions).

Uso:
  python3 goteo.py rss-completo.xml rss.xml --inicio 2026-11-17 [--hoy 2026-11-20]

Reparto: día 1 = 2 items, día 2 = 3, día 3 = 2, ... (alterna 2 y 3).
El orden es el del RSS completo. Cada item sale con pubDate = su día de salida.
Si se agregan items nuevos al final del RSS completo, entran a la cola solos.
"""
import argparse, datetime as dt, xml.etree.ElementTree as ET
from email.utils import format_datetime

def dia_de_salida(i, inicio):
    # i = posición 0..n ; bloques de 5 items cada 2 días (2 + 3)
    bloque, resto = divmod(i, 5)
    return inicio + dt.timedelta(days=bloque * 2 + (0 if resto < 2 else 1))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("completo"); ap.add_argument("salida")
    ap.add_argument("--inicio", required=True)
    ap.add_argument("--hoy", default=dt.date.today().isoformat())
    a = ap.parse_args()
    inicio = dt.date.fromisoformat(a.inicio); hoy = dt.date.fromisoformat(a.hoy)
    tree = ET.parse(a.completo); canal = tree.getroot().find("channel")
    items = canal.findall("item")
    publicados = 0
    for i, it in enumerate(items):
        d = dia_de_salida(i, inicio)
        if d > hoy:
            canal.remove(it); continue
        pd = it.find("pubDate")
        if pd is None: pd = ET.SubElement(it, "pubDate")
        pd.text = format_datetime(dt.datetime(d.year, d.month, d.day, 15, 0, tzinfo=dt.timezone.utc))
        publicados += 1
    tree.write(a.salida, encoding="utf-8", xml_declaration=True)
    falta = len(items) - publicados
    ultimo = dia_de_salida(len(items) - 1, inicio) if items else inicio
    print(f"Publicados {publicados} de {len(items)}; faltan {falta}; el último sale el {ultimo}")

if __name__ == "__main__":
    main()
