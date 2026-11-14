"""Avisa a Bing (y Yandex, Seznam, Naver) por IndexNow de las páginas nuevas o cambiadas de Cozy Paws.
Gratis y sin Claude. Lo corre .github/workflows/cozypaws-indexnow.yml todos los días después de la publicación diaria.
- Lee cozypaws/site/sitemap.xml y manda las URLs nuevas o con lastmod distinto al último aviso
  (la guía navideña principal cambia todos los días, así que se avisa cada día).
- Si la web o la clave todavía no están en línea, no hace nada (y no marca nada como avisado).
Uso: python3 cozypaws/indexnow.py <archivo-de-urls-avisadas>
"""
import json, os, re, sys, urllib.request, urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, "build.py"), encoding="utf-8").read()
KEY = re.search(r'INDEXNOW_KEY = "([0-9a-f]+)"', src).group(1)
SITE = re.search(r"url='([^']+)'", src).group(1).rstrip("/")
HOST = SITE.split("//", 1)[1]
sent_file = sys.argv[1] if len(sys.argv) > 1 else "cozy-indexnow-sent.txt"

try:
    req = urllib.request.Request("%s/%s.txt" % (SITE, KEY), headers={"User-Agent": "cozypaws-indexnow"})
    with urllib.request.urlopen(req, timeout=30) as r:
        if r.status != 200 or KEY not in r.read().decode("utf-8", "replace"):
            raise ValueError("clave no publicada")
except Exception as e:
    print("La web o la clave todavía no están en línea (%s). No se avisa nada hoy." % e)
    sys.exit(0)

sm = open(os.path.join(HERE, "site", "sitemap.xml"), encoding="utf-8").read()
entries = ["%s %s" % m for m in re.findall(r"<loc>([^<]+)</loc><lastmod>([^<]+)</lastmod>", sm)]
sent = set(open(sent_file).read().split("\n")) if os.path.exists(sent_file) else set()
new = [e for e in entries if e not in sent]
if not new:
    print("No hay páginas nuevas."); sys.exit(0)
urls = sorted({e.split(" ")[0] for e in new})
payload = json.dumps({"host": HOST, "key": KEY, "keyLocation": "%s/%s.txt" % (SITE, KEY), "urlList": urls[:10000]}).encode()
req = urllib.request.Request("https://api.indexnow.org/indexnow", data=payload,
                             headers={"Content-Type": "application/json; charset=utf-8"})
try:
    with urllib.request.urlopen(req, timeout=30) as r:
        print("IndexNow respondió", r.status, "por", len(urls), "páginas:", *urls, sep="\n  ")
except urllib.error.HTTPError as e:
    print("IndexNow respondió", e.code, e.read()[:300]); sys.exit(0 if e.code in (202, 429) else 1)
with open(sent_file, "w") as f:
    f.write("\n".join(sorted(sent | set(entries))) + "\n")
