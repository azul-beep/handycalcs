#!/usr/bin/env python3
"""Arma un reel vertical a partir de una receta, sin Claude: une clips, corta, pone voz, música, efectos de sonido,
subtítulos y saca la portada y una hoja de cuadros para revisar. Gratis (ffmpeg).

Uso:
  python3 tools/video/armar.py receta.json            arma el reel
  python3 tools/video/armar.py receta.json --hoja     además arma la hoja de cuadros (1 cuadro cada 0,5 s)
  python3 tools/video/armar.py --ejemplo              escribe una receta de ejemplo

Receta (rutas relativas a la carpeta de la receta):
{
  "salida": "reel.mp4",
  "clips": [ {"archivo": "c1.mp4", "desde": 0, "hasta": 3.2},          # desde/hasta en segundos (opcionales)
             {"archivo": "c2.mp4", "desde": 0.5, "sonido_clip": 0.6} ], # volumen del sonido propio del clip (1 = igual)
  "voz": "voz.mp3",                       # opcional; empieza en "voz_en" segundos (0 por defecto)
  "musica": "musica.mp3",                 # opcional; baja sola cuando habla la voz
  "volumen_musica": 0.25,
  "sonidos": [ {"archivo": "pop.mp3", "en": 2.4, "volumen": 0.8} ],    # efectos sincronizados con la acción
  "subtitulos": "subs.srt",               # opcional, quemados abajo del centro, letra grande con caja
  "portada_en": 1.0                       # segundo del que sale portada.jpg
}
Salida: H.264 yuv420p 1080x1920 30 fps, AAC, lista para Instagram/Facebook. Si un clip no es vertical, se recorta al
centro (no se deforma). La música de CapCut no se puede bajar: si se quiere un tema de CapCut, se arma acá sin música
y en CapCut solo se agrega el tema (un paso).
"""
import json
import os
import subprocess
import sys

ANCHO, ALTO, FPS = 1080, 1920, 30

EJEMPLO = {
    "salida": "reel.mp4",
    "clips": [{"archivo": "c1.mp4", "desde": 0, "hasta": 3.2}, {"archivo": "c2.mp4", "desde": 0.4}],
    "voz": "voz.mp3",
    "musica": "musica.mp3",
    "volumen_musica": 0.25,
    "sonidos": [{"archivo": "pop.mp3", "en": 2.4, "volumen": 0.8}],
    "subtitulos": "subs.srt",
    "portada_en": 1.0,
}


def duracion(ruta):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", ruta],
                       capture_output=True, text=True, check=True)
    return float(r.stdout.strip())


def tiene_audio(ruta):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries", "stream=index",
                        "-of", "csv=p=0", ruta], capture_output=True, text=True)
    return bool(r.stdout.strip())


def armar(receta_ruta, hoja=False):
    base = os.path.dirname(os.path.abspath(receta_ruta))
    R = json.load(open(receta_ruta, encoding="utf-8"))
    p = lambda x: os.path.join(base, x)  # noqa: E731
    entradas, filtros, vs, as_ = [], [], [], []
    total = 0.0
    for i, c in enumerate(R["clips"]):
        f = p(c["archivo"])
        d0 = float(c.get("desde", 0))
        d1 = float(c.get("hasta", duracion(f)))
        largo = d1 - d0
        entradas += ["-ss", f"{d0}", "-t", f"{largo}", "-i", f]
        filtros.append(f"[{i}:v]scale={ANCHO}:{ALTO}:force_original_aspect_ratio=increase,crop={ANCHO}:{ALTO},"
                       f"fps={FPS},setsar=1,format=yuv420p[v{i}]")
        if tiene_audio(f):
            filtros.append(f"[{i}:a]aformat=sample_rates=48000:channel_layouts=stereo,"
                           f"volume={c.get('sonido_clip', 1)}[a{i}]")
        else:
            filtros.append(f"anullsrc=r=48000:cl=stereo,atrim=0:{largo}[a{i}]")
        vs.append(f"[v{i}][a{i}]")
        total += largo
    n = len(R["clips"])
    filtros.append("".join(vs) + f"concat=n={n}:v=1:a=1[vcat][acat]")
    video = "[vcat]"
    if R.get("subtitulos"):
        srt = p(R["subtitulos"]).replace("\\", "/").replace(":", "\\:").replace("'", "\\'")
        estilo = ("FontName=DejaVu Sans,FontSize=13,Bold=1,PrimaryColour=&H00FFFFFF,BackColour=&H99000000,"
                  "BorderStyle=3,Outline=6,Shadow=0,Alignment=2,MarginV=110")
        filtros.append(f"{video}subtitles='{srt}':force_style='{estilo}'[vsub]")
        video = "[vsub]"
    mezcla = ["[acat]"]
    k = n
    voz = None
    if R.get("voz"):
        entradas += ["-i", p(R["voz"])]
        demora = int(float(R.get("voz_en", 0)) * 1000)
        filtros.append(f"[{k}:a]aformat=sample_rates=48000:channel_layouts=stereo,adelay={demora}|{demora},"
                       f"asplit=2[voz][vozlado]")
        voz = "[voz]"
        mezcla.append(voz)
        k += 1
    if R.get("musica"):
        entradas += ["-stream_loop", "-1", "-i", p(R["musica"])]
        vol = R.get("volumen_musica", 0.25)
        filtros.append(f"[{k}:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:{total},"
                       f"volume={vol},afade=t=in:d=0.5,afade=t=out:st={max(total - 1, 0)}:d=1[mus]")
        if voz:
            filtros.append("[mus][vozlado]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=400[musb]")
            mezcla.append("[musb]")
        else:
            mezcla.append("[mus]")
        k += 1
    elif voz:
        filtros.append("[vozlado]anullsink")
    for s in R.get("sonidos", []):
        entradas += ["-i", p(s["archivo"])]
        dm = int(float(s["en"]) * 1000)
        filtros.append(f"[{k}:a]aformat=sample_rates=48000:channel_layouts=stereo,volume={s.get('volumen', 1)},"
                       f"adelay={dm}|{dm}[s{k}]")
        mezcla.append(f"[s{k}]")
        k += 1
    filtros.append("".join(mezcla) + f"amix=inputs={len(mezcla)}:normalize=0:duration=first,"
                   f"alimiter=limit=0.95[aout]")
    salida = p(R.get("salida", "reel.mp4"))
    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", *entradas, "-filter_complex", ";".join(filtros),
           "-map", video, "-map", "[aout]", "-t", f"{total}", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
           "-pix_fmt", "yuv420p", "-r", str(FPS), "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", salida]
    subprocess.run(cmd, check=True)
    portada = os.path.join(os.path.dirname(salida), "portada.jpg")
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-ss", str(R.get("portada_en", 1.0)),
                    "-i", salida, "-frames:v", "1", "-q:v", "2", portada], check=True)
    print(f"Listo: {salida} ({total:.1f} s) y {portada}")
    if hoja:
        hoja_ruta = os.path.join(os.path.dirname(salida), "hoja-cuadros.jpg")
        filas = max(1, int(total * 2 / 8) + 1)
        subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", salida, "-vf",
                        f"fps=2,scale=216:-1,drawtext=text='%{{pts\\:hms}}':x=6:y=6:fontsize=18:fontcolor=white:"
                        f"box=1:boxcolor=black@0.6,tile=8x{filas}", "-frames:v", "1", hoja_ruta], check=True)
        print(f"Hoja de cuadros para revisar: {hoja_ruta}")


if __name__ == "__main__":
    if "--ejemplo" in sys.argv:
        json.dump(EJEMPLO, open("receta-ejemplo.json", "w"), indent=2, ensure_ascii=False)
        print("Escribí receta-ejemplo.json")
    elif len(sys.argv) > 1:
        armar(sys.argv[1], hoja="--hoja" in sys.argv)
    else:
        print(__doc__)
