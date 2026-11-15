"""Reloj de las rutinas: hace que las publicaciones salgan a horario, sin claves ni servicios de afuera.

GitHub atrasa los horarios programados (cron) 4 a 6 horas. Este programa corre adentro de GitHub Actions
(workflow .github/workflows/reloj.yml), mira la hora cada 30 segundos y, a la hora justa, dispara cada rutina
con "workflow_dispatch" usando la clave automática de GitHub (no hace falta ninguna clave de Azu).
Cada turno dura ~5 h 50 min; al terminar arranca el siguiente turno él solo. Si la cadena se corta,
el cron de respaldo (cada hora) lo vuelve a prender.
Repo público: los minutos de Actions son gratis. No gasta Claude.

Si una rutina llega dos veces (el reloj a horario + el cron atrasado de GitHub), el job "turno" de esa rutina
ve que ese turno ya salió y la segunda corrida termina en verde sin hacer nada.

Para sumar una rutina: una línea en TURNOS (hora UTC = Utah + 7 en invierno, + 6 en verano) y el input/job "turno" en su workflow.
Prueba sin disparar nada:  python3 tools/reloj.py --prueba
"""
import datetime as dt
import json
import os
import subprocess
import sys
import time

TURNOS = [
    # (hora UTC, workflow, turno = cron exacto del workflow, días 0=lunes..6=domingo o None)
    ("15:00", "imprimibles-diario.yml", "0 15 * * *", None),   # 8 AM Utah: juego del día y goteo
    ("16:20", "cozypaws-redes.yml",     "20 16 * * 1", [0]),   # lunes: renovar Threads
    ("17:00", "cozypaws-redes.yml",     "0 17 * * *", None),   # 10 AM: producto + historia
    ("19:00", "blue-instagram.yml",     "0 19 * * *", None),   # 12 PM: reel de Blue
    ("20:00", "cozypaws-redes.yml",     "0 20 * * *", None),   # 1 PM: tip o frase
    ("21:00", "cozypaws.yml",           "0 21 * * *", None),   # 2 PM: web y pines de Cozy Paws
    ("23:00", "handycalcs-redes.yml",   "0 23 * * *", None),   # 4 PM: guía a Facebook
    ("01:00", "cozypaws-redes.yml",     "0 1 * * *", None),    # 6 PM: producto
    ("02:00", "blue-instagram.yml",     "0 2 * * *", None),    # 7 PM: reel de Blue
]
VENTANA = dt.timedelta(minutes=20)      # si el reloj arranca un poco tarde, igual dispara lo de los últimos 20 min
DURACION = dt.timedelta(hours=5, minutes=50)
PRUEBA = '--prueba' in sys.argv
REPO = os.environ.get('GITHUB_REPOSITORY', 'azul-beep/handycalcs')


def gh(*args):
    return subprocess.run(['gh', *args], capture_output=True, text=True)


def otro_reloj_andando():
    """Si ya hay otro reloj corriendo, este se va (así nunca hay dos)."""
    yo = os.environ.get('GITHUB_RUN_ID', '0')
    r = gh('api', f'repos/{REPO}/actions/workflows/reloj.yml/runs?status=in_progress&per_page=20',
           '--jq', f'[.workflow_runs[] | select(.id != {yo})] | length')
    return r.returncode == 0 and r.stdout.strip() not in ('', '0')


def toca(ahora):
    for hora, wf, turno, dias in TURNOS:
        h, m = map(int, hora.split(':'))
        for delta in (0, -1):  # hoy, o ayer si el turno fue justo antes de medianoche UTC
            base = (ahora + dt.timedelta(days=delta)).replace(hour=h, minute=m, second=0, microsecond=0)
            if base <= ahora < base + VENTANA and (dias is None or base.weekday() in dias):
                yield base, wf, turno


def disparar(wf, turno):
    if PRUEBA:
        print(f'(prueba) dispararía {wf} turno "{turno}"')
        return
    for intento in range(3):
        r = gh('workflow', 'run', wf, '--repo', REPO, '--ref', 'main', '-f', f'turno={turno}')
        if r.returncode == 0:
            print(f'{dt.datetime.now(dt.timezone.utc):%H:%M} UTC  disparé {wf} ({turno})', flush=True)
            return
        time.sleep(20)
    print(f'::warning::No pude disparar {wf} ({turno}): {r.stderr.strip()[:200]}', flush=True)


def main():
    if PRUEBA:
        ahora = dt.datetime.now(dt.timezone.utc)
        for hora, wf, turno, dias in TURNOS:
            print(f'{hora} UTC  {wf}  turno "{turno}"' + (' (solo lunes)' if dias else ''))
        print('Toca ahora:', list(toca(ahora)) or 'nada')
        return
    for _ in range(4):  # en el relevo el reloj anterior tarda unos segundos en irse: esperarlo
        if not otro_reloj_andando():
            break
        time.sleep(60)
    else:
        print('Ya hay un reloj andando: este no hace falta.')
        return
    inicio = dt.datetime.now(dt.timezone.utc)
    hechos = set()
    print(f'Reloj andando desde {inicio:%H:%M} UTC hasta {(inicio + DURACION):%H:%M} UTC', flush=True)
    while dt.datetime.now(dt.timezone.utc) - inicio < DURACION:
        ahora = dt.datetime.now(dt.timezone.utc)
        for base, wf, turno in toca(ahora):
            if (base, turno) not in hechos:
                hechos.add((base, turno))
                disparar(wf, turno)
        time.sleep(30)
    # relevo: arranca el turno siguiente del reloj antes de irse
    r = gh('workflow', 'run', 'reloj.yml', '--repo', REPO, '--ref', 'main')
    print('Relevo pedido.' if r.returncode == 0 else f'::warning::No pude pedir el relevo ({r.stderr.strip()[:200]}); lo prende el cron.')


if __name__ == '__main__':
    main()
