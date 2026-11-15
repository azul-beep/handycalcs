#!/usr/bin/env python3
"""Handy Calcs en redes: cada guía nueva (src/articles/, 1 por día desde el 16 nov 2026) sale sola en Facebook. Sin Claude.

Qué ya estaba cubierto y NO hace este archivo:
- Pinterest: tools/pines_calculadoras.py le arma un pin a cada guía el mismo día que sale y lo pone en
  /pines/calculadoras/rss-en.xml (tablero "Free Calculators", auto-publish de Pinterest).

Qué hace este archivo (lo corre .github/workflows/handycalcs-redes.yml todas las tardes):
1. Busca guías que ya estén en la web (de los últimos DIAS_VENTANA días) y que todavía no salieron en Facebook.
2. Confirma que la página de la guía ya responde (el build diario a veces corre tarde); si no, espera al día siguiente.
3. Publica la más vieja (máximo POR_CORRIDA por corrida) en la página de Facebook de Handy Calcs: foto del pin + texto + link.
4. Anota lo publicado en redes/handycalcs-publicado.json para no repetir.

Necesita los secrets HC_FB_PAGE_ID y HC_FB_PAGE_TOKEN (token de la página de Handy Calcs que no vence).
Mientras no estén cargados, avisa "todavía no hay página de Facebook" y termina sin error.

Uso:  python3 tools/redes_guias.py publicar     (lo normal)
      python3 tools/redes_guias.py revisar      (prueba el token y muestra qué saldría, sin publicar)
      python3 tools/redes_guias.py probar       (igual que revisar pero sin internet; útil en local)
Fecha de prueba: HC_TODAY=2026-11-18 python3 tools/redes_guias.py probar
"""
import datetime as dt
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://gethandycalcs.pages.dev"            # igual que CONFIG["site_url"] de build.py
ARTICLES_START = dt.date(2026, 11, 16)              # igual que build.py
ESTADO = os.path.join(ROOT, "redes", "handycalcs-publicado.json")
FB = "https://graph.facebook.com/v21.0"
DIAS_VENTANA = 7     # una guía más vieja que esto ya no se publica (si la página se creó tarde, no se llena de golpe)
POR_CORRIDA = 1      # una por día: el ritmo de las guías
UTM = "?utm_source=facebook&utm_medium=social&utm_campaign=guide"
HASHTAGS = {
    "tip": "#tipping", "split": "#splitthebill", "tipout": "#restaurantlife", "discount": "#shoppingtips",
    "salestax": "#salestax", "scaler": "#cooking", "cooking": "#recipes", "hourly": "#salary", "overtime": "#overtime",
    "rule503020": "#budgeting", "budget": "#familybudget", "ccpayoff": "#debtfree", "compound": "#investing",
    "savings": "#savingmoney", "foodcost": "#restaurantowner", "menuprice": "#smallbusiness",
}
env = lambda k: os.environ.get(k, "").strip()


def hoy():
    return dt.date.fromisoformat(env("HC_TODAY")) if env("HC_TODAY") else dt.date.today()


def guias():
    d = os.path.join(ROOT, "src", "articles"); out = []
    for f in sorted(os.listdir(d)):
        m = re.match(r"(\d+)-([a-z0-9-]+)\.html$", f)
        if not m: continue
        head = open(os.path.join(d, f), encoding="utf-8").read().split("\n---\n", 1)[0]
        a = dict(line.split(": ", 1) for line in head.strip().splitlines() if ": " in line)
        a.update(n=int(m.group(1)), slug=m.group(2))
        a["live"] = ARTICLES_START + dt.timedelta(days=a["n"] - 1)
        a["calcs"] = [x.strip() for x in a.get("calcs", "").split(",") if x.strip()]
        out.append(a)
    return out


def leer_estado():
    return json.load(open(ESTADO, encoding="utf-8")) if os.path.exists(ESTADO) else {"facebook": {}}


def guardar_estado(e):
    os.makedirs(os.path.dirname(ESTADO), exist_ok=True)
    e["_nota"] = "Guías de Handy Calcs ya publicadas en redes. Lo escribe tools/redes_guias.py; no hace falta editarlo."
    with open(ESTADO, "w", encoding="utf-8") as f:
        json.dump(e, f, ensure_ascii=False, indent=1, sort_keys=True); f.write("\n")


def responde(url):
    try:
        req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "handycalcs-redes"})
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status == 200
    except Exception:
        return False


def call(url, data=None):
    body = urllib.parse.urlencode(data).encode() if data is not None else None
    try:
        with urllib.request.urlopen(urllib.request.Request(url, data=body), timeout=60) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        msg = e.read().decode(errors="replace")
        raise SystemExit("Facebook contestó %s: %s" % (e.code, msg[:400]))


def texto(a):
    tags = " ".join(dict.fromkeys(" ".join(HASHTAGS.get(c, "") for c in a["calcs"]).split()))
    link = SITE + "/guides/%s/" % a["slug"] + UTM
    return ("%s\n\n%s\n\nRead the free guide (with a calculator, no sign-up): %s\n\n#moneytips #freecalculator %s"
            % (a.get("h1", a.get("title", "")).rstrip("."), a.get("description", ""), link, tags)).strip()


def pendientes(estado, today):
    hechas = estado.get("facebook", {})
    return [a for a in guias() if a["live"] <= today and (today - a["live"]).days <= DIAS_VENTANA and a["slug"] not in hechas]


def main(accion):
    today = hoy()
    estado = leer_estado()
    page, token = env("HC_FB_PAGE_ID"), env("HC_FB_PAGE_TOKEN")
    cola = pendientes(estado, today)
    print("Guías listas para Facebook (%s): %s" % (today, ", ".join(a["slug"] for a in cola) or "ninguna"))
    if accion == "probar":
        for a in cola[:POR_CORRIDA]: print("---\n" + texto(a))
        return 0
    if not (page and token):
        print("Todavía no hay página de Facebook de Handy Calcs (faltan HC_FB_PAGE_ID y HC_FB_PAGE_TOKEN). No se publica nada.")
        return 0
    if not estado.get("facebook") and len(cola) > 1:   # primera vez (página nueva): arranca por la guía de hoy, sin ponerse al día
        for a in cola[:-1]: estado.setdefault("facebook", {})[a["slug"]] = {"fecha": today.isoformat(), "id": "omitida"}
        cola = cola[-1:]
    yo = call(FB + "/%s?" % page + urllib.parse.urlencode({"fields": "name", "access_token": token}))
    print("Token OK: página %s" % yo.get("name"))
    if accion == "revisar":
        for a in cola[:POR_CORRIDA]: print("---\n" + texto(a))
        return 0
    # Guías vencidas que nunca aparecieron en la web: eso es un problema del build diario -> corrida en rojo, mail de GitHub.
    ayer = today - dt.timedelta(days=1)
    caidas = [a for a in guias() if a["live"] == ayer and not responde(SITE + "/guides/%s/" % a["slug"])]
    publicadas = 0
    for a in cola:
        if publicadas >= POR_CORRIDA: break
        pagina = SITE + "/guides/%s/" % a["slug"]
        if not responde(pagina):
            print("%s todavía no está en la web; sale en la próxima corrida." % a["slug"]); continue
        img = SITE + "/pines/calculadoras/img/guide-%s.jpg" % a["slug"]
        if responde(img):
            r = call(FB + "/%s/photos" % page, {"url": img, "caption": texto(a), "access_token": token})
        else:   # sin imagen: post con link (Facebook arma la vista previa)
            r = call(FB + "/%s/feed" % page, {"message": texto(a), "link": pagina + UTM, "access_token": token})
        estado.setdefault("facebook", {})[a["slug"]] = {"fecha": today.isoformat(), "id": r.get("post_id") or r.get("id")}
        guardar_estado(estado); publicadas += 1
        print("Publicada en Facebook: %s" % a["slug"])
    if caidas:
        print("PROBLEMA: la guía de ayer no está en la web: %s. Revisá 'Publicación diaria (imprimibles y goteo)'."
              % ", ".join(a["slug"] for a in caidas))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "publicar"))
