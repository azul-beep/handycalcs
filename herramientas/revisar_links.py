#!/usr/bin/env python3
"""Revisión mensual de la guía de herramientas.

1. Todos los links que salen de las páginas (y los de afiliados.json): ¿siguen andando?
2. Las páginas oficiales de donde salen los datos (hechos.json): ¿cambió el texto?
   ¿siguen apareciendo las frases clave (precios, límites, comisiones)?

Uso:
  python3 revisar_links.py                       # revisa sitio/ y vista-previa/
  python3 revisar_links.py --html otra/carpeta   # otra carpeta de páginas
  python3 revisar_links.py --no-falla            # no termina con error aunque haya problemas

Guarda el estado en estado_links.json (hash de cada página) y el informe en
informes/revision-AAAA-MM-DD.md. Sale con código 1 si hay links rotos o datos a revisar
(así GitHub Actions avisa por mail). Solo usa la librería estándar de Python.
"""
import argparse, concurrent.futures as cf, datetime as dt, glob, hashlib, html, json, os, re, sys
import urllib.request, urllib.error

AQUI = os.path.dirname(os.path.abspath(__file__))
UA = "Mozilla/5.0 (compatible; revisor-de-enlaces/1.0)"


def links_de_html(carpetas):
    urls = {}
    for c in carpetas:
        for f in glob.glob(os.path.join(c, "**", "*.html"), recursive=True):
            txt = open(f, encoding="utf-8").read()
            for u in re.findall(r'href="(https?://[^"]+)"', txt):
                u = html.unescape(u)
                if "handycalcs.pages.dev" in u and ("rss.xml" in u or u.endswith((".html", "/"))) and "/herramientas-gratis/" in u:
                    continue  # links propios (canonical, rss): se publican de a poco
                urls.setdefault(u, set()).add(os.path.basename(f))
    return urls


def texto_normal(cuerpo):
    t = re.sub(r"(?is)<(script|style|noscript|svg)[^>]*>.*?</\1>", " ", cuerpo)
    t = re.sub(r"<[^>]+>", " ", t)
    t = html.unescape(t)
    return re.sub(r"\s+", " ", t).strip()


def bajar(url, timeout):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "en-US,en;q=0.8,es;q=0.6"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            data = r.read(3_000_000)
            enc = r.headers.get_content_charset() or "utf-8"
            return {"estado": r.status, "final": r.geturl(), "texto": texto_normal(data.decode(enc, "replace"))}
    except urllib.error.HTTPError as e:
        return {"estado": e.code, "final": url, "texto": ""}
    except Exception as e:  # DNS, timeout, SSL...
        return {"estado": 0, "final": url, "texto": "", "error": f"{type(e).__name__}: {e}"}


def clasificar(estado):
    if 200 <= estado < 400:
        return "ok"
    if estado in (401, 403, 429, 503):
        return "bloqueado"  # muchos sitios frenan robots: revisar a mano en el navegador
    return "roto"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--html", nargs="*", default=[os.path.join(AQUI, "sitio"), os.path.join(AQUI, "vista-previa")])
    ap.add_argument("--hechos", default=os.path.join(AQUI, "hechos.json"))
    ap.add_argument("--afiliados", default=os.path.join(AQUI, "afiliados.json"))
    ap.add_argument("--estado", default=os.path.join(AQUI, "estado_links.json"))
    ap.add_argument("--informes", default=os.path.join(AQUI, "informes"))
    ap.add_argument("--timeout", type=int, default=25)
    ap.add_argument("--no-falla", action="store_true")
    a = ap.parse_args()

    links = links_de_html(a.html)
    afi = json.load(open(a.afiliados, encoding="utf-8"))
    for k, v in afi.items():
        if k.startswith("AFF_"):
            for campo in ("url_afiliado", "url_oficial"):
                if v.get(campo):
                    links.setdefault(v[campo], set()).add(f"afiliados.json:{k}")
    hechos = json.load(open(a.hechos, encoding="utf-8"))["paginas"]
    for h in hechos:
        links.setdefault(h["url"], set()).add(f"hechos.json:{h['id']}")

    previo = json.load(open(a.estado, encoding="utf-8")) if os.path.exists(a.estado) else {}
    resultados = {}
    with cf.ThreadPoolExecutor(max_workers=6) as ex:
        futuros = {ex.submit(bajar, u, a.timeout): u for u in links}
        for f in cf.as_completed(futuros):
            resultados[futuros[f]] = f.result()

    hoy = dt.date.today().isoformat()
    nuevo, rotos, bloqueados, redirs, cambios, frases_faltan = {}, [], [], [], [], []
    por_url_hecho = {h["url"]: h for h in hechos}
    for u in sorted(links):
        r = resultados[u]
        clase = clasificar(r["estado"])
        hsh = hashlib.sha256(r["texto"].encode()).hexdigest() if r["texto"] else ""
        nuevo[u] = {"estado": r["estado"], "hash": hsh or previo.get(u, {}).get("hash", ""), "revisado": hoy}
        donde = ", ".join(sorted(links[u]))
        if clase == "roto":
            rotos.append(f"{u} → {r['estado'] or r.get('error')} (en: {donde})")
        elif clase == "bloqueado":
            bloqueados.append(f"{u} → {r['estado']} (en: {donde})")
        if r["final"].rstrip("/") != u.rstrip("/") and clase == "ok":
            redirs.append(f"{u} → {r['final']}")
        if u in por_url_hecho and hsh:
            h = por_url_hecho[u]
            ant = previo.get(u, {}).get("hash")
            if ant and ant != hsh:
                cambios.append(f"{h['id']}: {u} (lo usan: {', '.join(h['usa'])})")
            low = r["texto"].lower()
            falta = [fr for fr in h["frases"] if fr.lower() not in low]
            if falta:
                frases_faltan.append(f"{h['id']}: ya no aparece {falta} en {u} (lo usan: {', '.join(h['usa'])})")

    json.dump(nuevo, open(a.estado, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    os.makedirs(a.informes, exist_ok=True)
    def lista(xs):
        return "\n".join(f"{i}. {x}" for i, x in enumerate(xs, 1)) if xs else "1. Nada."
    informe = f"""# Revisión de links y datos — {hoy}

Links revisados: {len(links)}. Rotos: {len(rotos)}. Bloqueados por el sitio: {len(bloqueados)}. Datos a revisar: {len(frases_faltan)}. Páginas de datos que cambiaron: {len(cambios)}.

## 1. Links rotos (arreglar)
{lista(rotos)}

## 2. Datos que pueden haber cambiado (revisar la página y corregir contenido.py)
{lista(frases_faltan)}

## 3. Páginas de datos con texto distinto al mes pasado (mirar si cambió algo importante)
{lista(cambios)}

## 4. Sitios que no dejan entrar al robot (abrir a mano en el navegador)
{lista(bloqueados)}

## 5. Redirecciones (andan, pero conviene actualizar el link)
{lista(redirs)}
"""
    ruta = os.path.join(a.informes, f"revision-{hoy}.md")
    open(ruta, "w", encoding="utf-8").write(informe)
    print(informe)
    print(f"Informe: {ruta}")
    if (rotos or frases_faltan) and not a.no_falla:
        sys.exit(1)


if __name__ == "__main__":
    main()
