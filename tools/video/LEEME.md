# Armar reels sin Claude (ni CapCut para el montaje)

`armar.py` arma el reel a partir de una receta: une los clips, los corta, pone voz, música (que baja sola cuando
habla la voz), efectos de sonido en el segundo exacto y subtítulos, y saca la portada y una hoja de cuadros.
Gratis (ffmpeg). Sirve para Cozy y para Blue. Lo corre cualquier hilo en la nube o la PC con ffmpeg.

1. `python3 tools/video/armar.py --ejemplo` escribe una receta de ejemplo (explicada dentro de `armar.py`).
2. Poner en una carpeta los clips, la voz, la música, los sonidos y `subs.srt`, y completar la receta.
3. `python3 tools/video/armar.py receta.json --hoja` → `reel.mp4` (1080x1920, H.264 yuv420p, listo para IG),
   `portada.jpg` y `hoja-cuadros.jpg` (un cuadro cada 0,5 s con la hora: para el control de jurado cuadro por cuadro
   sin mirar el video entero).
4. Para corregir algo se cambia solo la receta y se vuelve a correr: no se rehace nada de lo aprobado.

Música: la de CapCut no se puede bajar. Si va un tema de CapCut, armar acá sin `musica` y en CapCut solo agregar
el tema (un paso). Con música propia o libre, se pone en la receta y CapCut no hace falta.
