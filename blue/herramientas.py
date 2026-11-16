"""Rearma blue/web/_redirects (links cortos /ir/<id>) desde blue/web/herramientas.json.
Si una herramienta tiene link_afiliado, /ir/<id> lleva ahí; si no, a su web oficial.
Uso: python3 blue/herramientas.py   (lo corre solo la rutina 'Blue (web)')."""
import json, pathlib, sys
WEB = pathlib.Path(__file__).resolve().parent / "web"
datos = json.loads((WEB / "herramientas.json").read_text(encoding="utf-8"))
lineas = ["# Generado por blue/herramientas.py desde herramientas.json. No editar a mano."]
for h in datos["herramientas"]:
    destino = (h.get("link_afiliado") or h["web"]).strip()
    if not destino.startswith("https://"):
        sys.exit(f"{h['id']}: el link tiene que empezar con https://")
    lineas.append(f"/ir/{h['id']} {destino} 302")
    lineas.append(f"/ir/{h['id']}/ {destino} 302")
(WEB / "_redirects").write_text("\n".join(lineas) + "\n", encoding="utf-8")
print(f"_redirects con {len(datos['herramientas'])} herramientas")
