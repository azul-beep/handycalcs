#!/usr/bin/env python3
"""Informe semanal "qué anduvo mejor" de Cozy Paws y de Blue, por separado. Sin Claude (GitHub Actions, lunes).

Lee los números de cada reel que GitHub ya junta todos los días:
  Cozy: cozypaws/estadisticas/reels-historial.csv     Blue: blue/estadisticas/reels-historial.csv
y escribe informes/semana-AAAA-MM-DD.md con, para cada cuenta: los 3 reels con más vistas de los últimos 7 días,
el que peor anduvo, el promedio de la semana contra la anterior y "hacé más de esto". Los agentes leen este archivo
en vez de analizar los números con Claude. El workflow además lo manda por mail (issue).
Si no hay datos, lo dice: casi siempre falta el permiso de Meta (ver blue/LEEME.md y meta/LEEME.md).
"""
import csv
import datetime as dt
import os
import statistics
from zoneinfo import ZoneInfo

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CUENTAS = [("Cozy Paws (@cozypawsgifts)", "cozypaws/estadisticas/reels-historial.csv"),
           ("Blue en Automático (@blue.automatica)", "blue/estadisticas/reels-historial.csv")]
HOY = dt.datetime.now(ZoneInfo("America/Denver")).date()


def num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def leer(rel):
    ruta = os.path.join(RAIZ, rel)
    if not os.path.exists(ruta):
        return []
    return list(csv.DictReader(open(ruta, encoding="utf-8")))


def entre(filas, desde, hasta):
    return [f for f in filas if f.get("fecha") and desde <= dt.date.fromisoformat(f["fecha"]) < hasta]


def promedio(filas, campo):
    v = [num(f.get(campo)) for f in filas if num(f.get(campo)) is not None]
    return round(statistics.mean(v)) if v else None


def linea(f):
    partes = [f"{int(num(f['vistas']) or 0)} vistas"]
    if num(f.get("pct_visto")):
        partes.append(f"se ve el {int(num(f['pct_visto']))}%")
    if num(f.get("compartidos")):
        partes.append(f"{int(num(f['compartidos']))} compartidos")
    if num(f.get("guardados")):
        partes.append(f"{int(num(f['guardados']))} guardados")
    return f"[{f.get('texto') or 'sin texto'}]({f.get('link', '')}) ({f['fecha']}): " + ", ".join(partes)


def seccion(nombre, rel):
    filas = [f for f in leer(rel) if num(f.get("vistas")) is not None]
    semana = entre(filas, HOY - dt.timedelta(days=7), HOY + dt.timedelta(days=1))
    antes = entre(filas, HOY - dt.timedelta(days=14), HOY - dt.timedelta(days=7))
    L = [f"## {nombre}", ""]
    if not semana:
        L += ["Sin datos de reels esta semana. Si hubo reels publicados, falta el permiso de Meta: "
              "pasos en `meta/LEEME.md`.", ""]
        return L
    top = sorted(semana, key=lambda f: num(f["vistas"]), reverse=True)
    L += ["**Los que mejor anduvieron:**", ""] + [f"{i}. {linea(f)}" for i, f in enumerate(top[:3], 1)] + [""]
    if len(top) > 3:
        L += [f"**El más flojo:** {linea(top[-1])}", ""]
    p1, p0 = promedio(semana, "vistas"), promedio(antes, "vistas")
    comp = f" (semana anterior: {p0})" if p0 is not None else ""
    L += [f"Promedio: {p1} vistas por reel en {len(semana)} reels{comp}.", ""]
    compartido = max(semana, key=lambda f: num(f.get("compartidos")) or 0)
    L += [f"**Hacé más de esto:** el tema y el gancho de «{top[0].get('texto') or 'el primero'}»."]
    if (num(compartido.get("compartidos")) or 0) > 0 and compartido is not top[0]:
        L += [f"El más compartido fue «{compartido.get('texto')}»: los compartidos son lo que más alcance trae."]
    L.append("")
    return L


def main():
    L = [f"# Informe semanal de redes: semana al {HOY:%d %b %Y}", "",
         "Lo arma GitHub solo cada lunes (tools/informe_semanal.py). Cozy y Blue van separados.", ""]
    for nombre, rel in CUENTAS:
        L += seccion(nombre, rel)
    texto = "\n".join(L)
    os.makedirs(os.path.join(RAIZ, "informes"), exist_ok=True)
    ruta = os.path.join(RAIZ, "informes", f"semana-{HOY:%Y-%m-%d}.md")
    open(ruta, "w", encoding="utf-8").write(texto)
    print(texto)


if __name__ == "__main__":
    main()
