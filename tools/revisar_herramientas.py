"""Vigila la sección de herramientas online de Handy Calcs (/tools/ y /es/herramientas/). Gratis y sin Claude.
Lo corre .github/workflows/herramientas-salud.yml todos los días, después de la publicación diaria.
Revisa en la web EN LÍNEA:
  1. que estén publicadas todas las herramientas que ya tendrían que haber salido según el goteo (TOOLS_START en build.py),
  2. que cada página responda 200 y traiga su herramienta (data-tool=),
  3. que respondan tools.js, tools.css y vendor/qrcode.js,
  4. pines de Pinterest: que cada herramienta tenga sus 2 pines (EN y ES) en la cola pines/calculadoras/cola.json,
     que ninguno salga antes que su página y que la imagen de los pines que ya salieron esté en línea.
Si algo falla, escribe el detalle en problemas.txt y sale con código 1 (el workflow abre un aviso en GitHub, que llega por mail).
"""
import datetime, json, os, re, sys, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
import tools as TL

src = open(os.path.join(ROOT, "build.py"), encoding="utf-8").read()
SITE = os.environ.get("HC_SITE") or re.search(r'site_url="([^"]+)"', src).group(1).rstrip("/")
y, m, d = map(int, re.search(r"TOOLS_START = datetime.date\((\d+), (\d+), (\d+)\)", src).groups())
START = datetime.date(y, m, d)
# La publicación diaria corre a las 15:00 UTC pero GitHub la puede atrasar horas: se toma como "hoy" lo que debía salir ayer.
HOY = datetime.date.fromisoformat(os.environ["HC_HOY"]) if os.environ.get("HC_HOY") else datetime.date.today() - datetime.timedelta(days=1)

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "handycalcs-monitor"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, ""
    except Exception as e:
        return 0, str(e)

problemas = []
deben = [x for x in TL.TOOLS if START + datetime.timedelta(days=max(0, x["n"] - 2)) <= HOY]
if not deben:
    print("Todavía no salió ninguna herramienta (empiezan el %s)." % START); sys.exit(0)

for f in ("/tools.js", "/tools.css", "/vendor/qrcode.js", "/tools/", "/es/herramientas/"):
    st, _ = get(SITE + f)
    if st != 200: problemas.append("%s responde %s" % (f, st))
for x in deben:
    for path in ("/tools/%s/" % x["en"]["slug"], "/es/herramientas/%s/" % x["es"]["slug"]):
        st, body = get(SITE + path)
        if st != 200: problemas.append("%s responde %s (tenía que estar publicada)" % (path, st))
        elif 'data-tool="%s"' % x["engine"] not in body: problemas.append("%s no muestra la herramienta" % path)

# 4) Pines de las herramientas (los publica tools/pines_calculadoras.py en los feeds rss-en.xml y rss-es.xml)
cola = json.load(open(os.path.join(ROOT, "pines", "calculadoras", "cola.json"), encoding="utf-8"))["items"]
fecha_pin = {i["id"]: datetime.date.fromisoformat(i["fecha"]) for i in cola}
salidos = 0
for x in TL.TOOLS:
    live = START + datetime.timedelta(days=max(0, x["n"] - 2))
    for lang in ("en", "es"):
        pid = "tool-%s-%s" % (x["id"], lang)
        if pid not in fecha_pin: problemas.append("La herramienta %s no tiene pin %s en la cola de Pinterest" % (x["id"], lang.upper())); continue
        if fecha_pin[pid] < live: problemas.append("El pin %s sale el %s, antes que su página (%s)" % (pid, fecha_pin[pid], live))
        if fecha_pin[pid] <= HOY:
            salidos += 1
            st, _ = get(SITE + "/pines/calculadoras/img/%s.jpg" % pid)
            if st != 200: problemas.append("La imagen del pin %s responde %s" % (pid, st))
print("Pines de herramientas que ya salieron: %d de %d" % (salidos, 2 * len(TL.TOOLS)))

print("Herramientas que ya tendrían que estar en línea: %d de %d" % (len(deben), len(TL.TOOLS)))
if problemas:
    open("problemas.txt", "w", encoding="utf-8").write("\n".join("- " + p for p in problemas) + "\n")
    print("\n".join(problemas)); sys.exit(1)
print("Todo bien.")
