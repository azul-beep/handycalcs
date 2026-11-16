# Blue en Automático: página del link del perfil (https://blueautomatica.pages.dev)

Página única con las plantillas, prompts y pasos que nombran los videos de @blue.automatica ("está en el link de mi perfil"). Cada sección se abre sola con un ancla: `#instagram`, `#pinterest`, `#herramientas`, `#etsy`, `#prompt`, `#planilla`, `#respuestas`, `#libro`, `#empezar`.

GA4 y Píxel de Meta: cambiar `GA4_ID` y `PIXEL_ID` arriba de `index.html` cuando existan (solo se cargan si la persona acepta cookies).

## Paso único en Cloudflare (5 minutos)
1. dash.cloudflare.com > Workers & Pages > Create > Pages > Connect to Git > repo `azul-beep/handycalcs`.
2. Project name: `blueautomatica`. Production branch: `main`. Framework: None. Build command: vacío. Build output directory: `blue/web`.
3. Settings > Builds > Build watch paths: incluir solo `blue/web/*`.
4. Save and Deploy. Probar https://blueautomatica.pages.dev y pegar ese link en el perfil de Instagram.

## Herramientas que uso (afiliados)
- Sección `#uso` arriba de todo. Se arma sola desde `herramientas.json` (solo las que tienen `"mostrar": true`).
- Links cortos `/ir/<id>`: los escribe `blue/herramientas.py` en `_redirects`; la rutina "Blue (herramientas)" lo corre sola cuando cambia `herramientas.json` en main. Para poner un link de afiliada: pegarlo en `link_afiliado` y unir a main.
- Cada clic en "Ver" manda el evento `clic_afiliado` (parámetro `herramienta`) a GA4 y `ClicHerramienta` al Píxel, solo con cookies aceptadas.
- Paquete completo (fichas de alta, avisos, respuesta guardada, líneas para videos): /mnt/project-files/cuenta-ia/afiliados-tecnologia/paquete-afiliados-blue.md
