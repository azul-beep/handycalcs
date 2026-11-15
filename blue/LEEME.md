# Blue en Automático: los reels salen solos

Gratis y sin Claude: GitHub publica 2 reels por día (12 PM y 7 PM de Utah) en el Instagram de Blue, con la API oficial de Meta.
Claude solo hace los videos nuevos (eso es trabajo creativo); publicarlos no gasta nada.

## Cómo funciona

1. Los videos que esperan salir están en la rama `blue-videos` del repo handycalcs: `cola.json` (orden, texto y fecha de cada video) y los `.mp4`.
2. A cada hora, el workflow "Blue (Instagram)" toma el primer video cuya fecha ya llegó, lo sube a Instagram y lo borra de la rama (queda anotado en `publicado.json`). La rama se rehace en un solo commit, así el repo no engorda.
3. Si quedan menos de 4 videos, abre el issue "🎬 Blue: quedan N videos" (te llega por mail) para pedir otra tanda. Se cierra solo.
4. Cada texto lleva al final "🤖 Personaje y voz hechos con IA." (la API no deja tildar la etiqueta de IA de Instagram; el texto y la bio "AI-generated" cumplen la regla).
5. Con el despertador de Cloudflare instalado, sale a la hora justa; sin él, GitHub lo atrasa unas horas.

## Lo que hacés vos, una sola vez

1. Crear la cuenta de Instagram de Blue y pasarla a cuenta profesional (Creador).
2. Crear una página de Facebook "Blue en Automático" y conectarle el Instagram (Meta Business Suite > Configuración > Cuentas de Instagram). La página no muestra quién la administra.
3. Sacar el token de página que no vence, igual que con Cozy Paws (el hilo "Hacer los pasos en Chrome" te guía; permisos: instagram_basic, instagram_content_publish, pages_show_list, pages_read_engagement).
4. Pegar en GitHub > handycalcs > Settings > Secrets and variables > Actions:
   - `BLUE_IG_USER_ID`: el id de la cuenta de Instagram de Blue
   - `BLUE_FB_TOKEN`: el token de página
5. Probar: Actions > Blue (Instagram) > Run workflow > `revisar`. Tiene que decir "Clave OK: @tu-cuenta".

Hasta que estén los dos secretos, el workflow termina en verde sin publicar nada.

## Para sumar videos (lo hace el hilo de Blue)

1. Poner los `.mp4` (vertical 1080x1920, menos de 95 MB) en una carpeta con un `textos.json`:
   `{"v01.mp4": {"texto": "texto del reel con hashtags", "fecha": "2026-11-23"}}` (fecha opcional: sin fecha sale apenas le toca).
2. Desde un clon de handycalcs: `python3 blue/videos.py agregar CARPETA`. Empuja a la rama `blue-videos` (rama de datos: necesita permiso de Azu para que Claude empuje ahí).
3. Probar sin tocar nada: agregar `--prueba`.
