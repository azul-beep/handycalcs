#!/usr/bin/env python3
"""Claves por vencer: avisa a Azu antes de que una clave o permiso deje de andar. Sin Claude.

Corre los lunes en GitHub Actions (.github/workflows/claves.yml). El mismo archivo está en
azul-beep/crux-report y azul-beep/handycalcs: cada repo revisa los secretos que tiene.
Revisa lo que encuentre cargado:
1. PRINTIFY_TOKEN: que ande y cuándo vence (la clave trae la fecha adentro).
2. FB_PAGE_TOKEN: que ande y si tiene vencimiento (Meta lo dice con debug_token).
3. THREADS_TOKEN: que ande; vence 60 días después de la última renovación (la hace cozypaws-redes los lunes).
4. GH_SECRETS_PAT: cuándo vence (GitHub lo manda en un encabezado).
5. Permiso de Etsy (.github/etsy-token.enc): vence si pasan 90 días sin renovarse.
6. .github/claves.json (opcional): otras fechas cargadas a mano [{"nombre", "vence": "AAAA-MM-DD", "como"}].
Si algo vence en menos de AVISAR_DIAS días, está vencido o no anda, abre (o actualiza) un issue
"🔑 Claves por vencer" con la etiqueta "claves" y GitHub le manda el mail a Azu. Si todo está bien, lo cierra.
Nunca imprime las claves. Prueba sin tocar issues:  python3 tools/claves.py --dry-run
"""
import base64
import datetime as dt
import json
import os
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request

AVISAR_DIAS = 21
LABEL = "claves"
TITULO = "🔑 Claves por vencer"
DRY = "--dry-run" in sys.argv
REPO = os.environ.get("GITHUB_REPOSITORY", "")
OWNER = os.environ.get("GITHUB_REPOSITORY_OWNER", "")
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AHORA = dt.datetime.now(dt.timezone.utc)
env = lambda k: os.environ.get(k, "").strip()

# Cómo renovar cada una (el texto va al issue)
COMO = {
    "Printify": "Printify > My profile > Connections > Generate token (mismos permisos que la anterior). "
                "Pegarla en GitHub: crux-report > Settings > Secrets and variables > Actions > PRINTIFY_TOKEN > Update.",
    "Facebook/Instagram": "Generar un token de página nuevo (Graph API Explorer > token de usuario largo > /me/accounts) "
                          "y pegarlo en handycalcs > Settings > Secrets > FB_PAGE_TOKEN.",
    "Threads": "Correr a mano Actions > Cozy Paws (redes) > Run workflow con 'renovar'. Si falla, generar un token "
               "largo nuevo de Threads y pegarlo en handycalcs > Settings > Secrets > THREADS_TOKEN.",
    "GitHub (GH_SECRETS_PAT)": "github.com/settings/personal-access-tokens > el token > Regenerate (o crear uno nuevo con "
                               "Secrets: Read and write en handycalcs) y pegarlo en handycalcs > Settings > Secrets > GH_SECRETS_PAT.",
    "Etsy": "Correr a mano Actions > Imprimibles digitales a Etsy > Run workflow con modo 'plan' (renueva el permiso). "
            "Si Etsy lo rechazó, se abre solo el issue 'Autorizar Etsy' con el link para tocar Allow access.",
}


def pedir(url, headers=None):
    req = urllib.request.Request(url, headers={"User-Agent": "vigilante-claves", **(headers or {})})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode() or "null"), dict(r.headers)


def dias(fecha):
    return (fecha - AHORA).total_seconds() / 86400


def fmt(fecha):
    return fecha.strftime("%Y-%m-%d")


resultados = []  # (nombre, estado "ok"|"pronto"|"mal", detalle)


def anotar(nombre, vence=None, error=None, nota=""):
    if error:
        resultados.append((nombre, "mal", f"no anda: {error}"))
    elif vence is None:
        resultados.append((nombre, "ok", "anda y no vence" + (f" ({nota})" if nota else "")))
    else:
        d = dias(vence)
        estado = "mal" if d < 0 else "pronto" if d <= AVISAR_DIAS else "ok"
        if d < 0:
            txt = f"vencida el {fmt(vence)}"
        elif d < 2:
            txt = f"vence el {vence.strftime('%Y-%m-%d %H:%M')} UTC (en {max(int(d * 24), 0)} horas)"
        else:
            txt = f"vence el {fmt(vence)} (en {int(d)} días)"
        resultados.append((nombre, estado, txt + (f" ({nota})" if nota else "")))


def jwt_exp(token):
    try:
        cuerpo = token.split(".")[1]
        datos = json.loads(base64.urlsafe_b64decode(cuerpo + "=" * (-len(cuerpo) % 4)))
        return dt.datetime.fromtimestamp(datos["exp"], dt.timezone.utc) if datos.get("exp") else None
    except Exception:
        return None


def revisar_printify():
    t = env("PRINTIFY_TOKEN")
    if not t:
        return
    try:
        pedir("https://api.printify.com/v1/shops.json", {"Authorization": f"Bearer {t}"})
    except urllib.error.HTTPError as e:
        if e.code in (401, 403):
            return anotar("Printify", error=f"Printify contestó {e.code}")
    except Exception as e:
        print("Printify no respondió (no aviso por esto):", type(e).__name__)
    anotar("Printify", jwt_exp(t))


def revisar_meta():
    t = env("FB_PAGE_TOKEN")
    if not t:
        return
    try:
        d, _ = pedir("https://graph.facebook.com/v21.0/debug_token?" + urllib.parse.urlencode(
            {"input_token": t, "access_token": t}))
        d = d.get("data", {})
    except urllib.error.HTTPError as e:
        return anotar("Facebook/Instagram", error=f"Meta contestó {e.code}")
    except Exception as e:
        return print("Meta no respondió (no aviso por esto):", type(e).__name__)
    if not d.get("is_valid"):
        return anotar("Facebook/Instagram", error="Meta dice que el token no es válido")
    exp = d.get("expires_at") or 0
    anotar("Facebook/Instagram", dt.datetime.fromtimestamp(exp, dt.timezone.utc) if exp else None)
    acc = d.get("data_access_expires_at") or 0
    if acc:
        # Meta renueva este permiso solo mientras se use la página; avisar si se acerca igual
        anotar("Facebook/Instagram (acceso a datos)", dt.datetime.fromtimestamp(acc, dt.timezone.utc),
               nota="se renueva solo al usar la app; si vence, generar token nuevo")


def fecha_secreto(nombre):
    """updated_at del secreto en este repo (necesita GH_SECRETS_PAT con permiso de secretos)."""
    pat = env("GH_SECRETS_PAT")
    if not (pat and REPO):
        return None
    try:
        d, _ = pedir(f"https://api.github.com/repos/{REPO}/actions/secrets/{nombre}",
                     {"Authorization": f"Bearer {pat}", "Accept": "application/vnd.github+json"})
        return dt.datetime.fromisoformat(d["updated_at"].replace("Z", "+00:00"))
    except Exception:
        return None


def revisar_threads():
    t = env("THREADS_TOKEN")
    if not t:
        return
    try:
        pedir("https://graph.threads.net/v1.0/me?" + urllib.parse.urlencode({"fields": "username", "access_token": t}))
    except urllib.error.HTTPError as e:
        return anotar("Threads", error=f"Threads contestó {e.code}")
    except Exception as e:
        return print("Threads no respondió (no aviso por esto):", type(e).__name__)
    f = fecha_secreto("THREADS_TOKEN")
    if f:
        anotar("Threads", f + dt.timedelta(days=60), nota=f"última renovación {fmt(f)}")
    else:
        resultados.append(("Threads", "ok", "anda (no pude leer la fecha de la última renovación)"))


def revisar_pat():
    pat = env("GH_SECRETS_PAT")
    if not pat:
        return
    try:
        _, h = pedir("https://api.github.com/user", {"Authorization": f"Bearer {pat}"})
    except urllib.error.HTTPError as e:
        return anotar("GitHub (GH_SECRETS_PAT)", error=f"GitHub contestó {e.code}")
    except Exception as e:
        return print("GitHub no respondió:", type(e).__name__)
    h = {k.lower(): v for k, v in h.items()}
    exp = h.get("github-authentication-token-expiration")
    vence = None
    if exp:
        try:
            vence = dt.datetime.strptime(exp.replace(" UTC", "").strip()[:19], "%Y-%m-%d %H:%M:%S").replace(tzinfo=dt.timezone.utc)
        except ValueError:
            pass
    anotar("GitHub (GH_SECRETS_PAT)", vence)


def revisar_etsy():
    archivo = os.path.join(RAIZ, ".github", "etsy-token.enc")
    if not (env("ETSY_KEYSTRING") and os.path.exists(archivo)):
        return  # sin permiso guardado: el workflow de Etsy ya pide la autorización por issue
    try:
        out = subprocess.run(["gh", "api", f"repos/{REPO}/commits?path=.github/etsy-token.enc&per_page=1",
                              "--jq", ".[0].commit.committer.date"], capture_output=True, text=True, check=True).stdout.strip()
        ultima = dt.datetime.fromisoformat(out.replace("Z", "+00:00"))
    except Exception:
        return print("no pude leer la fecha del permiso de Etsy")
    anotar("Etsy", ultima + dt.timedelta(days=90), nota=f"última renovación {fmt(ultima)}; se renueva solo los días 1 y 15")


def revisar_manuales():
    archivo = os.path.join(RAIZ, ".github", "claves.json")
    if not os.path.exists(archivo):
        return
    for c in json.load(open(archivo, encoding="utf-8")):
        vence = dt.datetime.fromisoformat(c["vence"]).replace(tzinfo=dt.timezone.utc)
        COMO.setdefault(c["nombre"], c.get("como", ""))
        anotar(c["nombre"], vence)


def gh(*a):
    return subprocess.run(["gh", *a], check=True, capture_output=True, text=True).stdout


def main():
    for f in (revisar_printify, revisar_meta, revisar_threads, revisar_pat, revisar_etsy, revisar_manuales):
        f()
    for n, e, d in resultados:
        print(f"{'✅' if e == 'ok' else '⚠️' if e == 'pronto' else '❌'} {n}: {d}")
    problemas = [r for r in resultados if r[1] != "ok"]
    if DRY or not REPO:
        return
    abiertos = json.loads(gh("issue", "list", "--label", LABEL, "--state", "open", "--json", "number,body"))
    if not problemas:
        for i in abiertos:
            gh("issue", "close", str(i["number"]), "--comment", "Todas las claves andan y ninguna vence pronto. Cierro solo.")
        return
    lineas = []
    for k, (n, e, d) in enumerate(problemas, 1):
        base = n.split(" (")[0]
        lineas.append(f"{k}. {'❌' if e == 'mal' else '⚠️'} **{n}**: {d}.\n   Cómo renovar: {COMO.get(base, COMO.get(n, ''))}")
    cuerpo = ("Hay claves que vencen pronto o dejaron de andar. Cuando se arreglan, este aviso se cierra solo "
              "(se revisa los lunes; para revisar ya: Actions > Claves por vencer > Run workflow).\n\n"
              + "\n".join(lineas) + "\n\nNo pegues claves en este issue: van solo en Settings > Secrets.")
    if abiertos:
        i = abiertos[0]
        if (i["body"] or "").strip() != cuerpo.strip():
            gh("issue", "edit", str(i["number"]), "--body", cuerpo)
            gh("issue", "comment", str(i["number"]), "--body", "Actualicé la lista:\n\n" + "\n".join(lineas))
        return
    subprocess.run(["gh", "label", "create", LABEL, "--color", "D93F0B", "--description", "Claves por vencer"],
                   capture_output=True)
    a = ["issue", "create", "--title", TITULO, "--label", LABEL, "--body", cuerpo]
    if OWNER:
        a += ["--assignee", OWNER]
    gh(*a)


if __name__ == "__main__":
    main()
