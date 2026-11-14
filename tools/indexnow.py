"""Avisa a Bing (y Yandex, Seznam, Naver) por IndexNow de las páginas nuevas de Handy Calcs.
Gratis y sin Claude. Lo corre .github/workflows/indexnow.yml todos los días.
- Lee site/sitemap.xml, compara con la lista de URLs ya avisadas (cache de Actions) y manda solo las nuevas.
- Si la web todavía no está en línea, no hace nada (y no marca nada como avisado).
Uso: python3 tools/indexnow.py <archivo-de-urls-avisadas>
"""
import json, os, re, sys, urllib.request, urllib.error

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
src = open(os.path.join(ROOT, "build.py"), encoding="utf-8").read()
KEY = re.search(r'INDEXNOW_KEY = "([0-9a-f]+)"', src).group(1)
SITE = re.search(r'site_url="([^"]+)"', src).group(1).rstrip("/")
HOST = SITE.split("//", 1)[1]
sent_file = sys.argv[1] if len(sys.argv) > 1 else "indexnow-sent.txt"

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "handycalcs-indexnow"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.status, r.read().decode("utf-8", "replace")

try:
    st, body = get("%s/%s.txt" % (SITE, KEY))
    if st != 200 or KEY not in body:
        raise ValueError("clave no publicada")
except Exception as e:
    print("La web o la clave todavía no están en línea (%s). No se avisa nada hoy." % e)
    sys.exit(0)

sm = open(os.path.join(ROOT, "site", "sitemap.xml"), encoding="utf-8").read()
urls = re.findall(r"<loc>([^<]+)</loc>", sm)
sent = set(open(sent_file).read().split()) if os.path.exists(sent_file) else set()
new = [u for u in urls if u not in sent]
if not new:
    print("No hay páginas nuevas."); sys.exit(0)
payload = json.dumps({"host": HOST, "key": KEY, "keyLocation": "%s/%s.txt" % (SITE, KEY), "urlList": new[:10000]}).encode()
req = urllib.request.Request("https://api.indexnow.org/indexnow", data=payload,
                             headers={"Content-Type": "application/json; charset=utf-8"})
try:
    with urllib.request.urlopen(req, timeout=30) as r:
        print("IndexNow respondió", r.status, "por", len(new), "páginas")
except urllib.error.HTTPError as e:
    print("IndexNow respondió", e.code, e.read()[:300]); sys.exit(0 if e.code in (202, 429) else 1)
with open(sent_file, "w") as f:
    f.write("\n".join(sorted(sent | set(new))) + "\n")
