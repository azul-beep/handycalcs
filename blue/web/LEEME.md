# Blue en Automático: página del link del perfil (https://blueautomatica.pages.dev)

Página única con las plantillas, prompts y pasos que nombran los videos de @blue.automatica ("está en el link de mi perfil"). Cada sección se abre sola con un ancla: `#instagram`, `#pinterest`, `#herramientas`, `#etsy`, `#prompt`, `#planilla`, `#respuestas`, `#libro`, `#empezar`.

GA4 y Píxel de Meta: cambiar `GA4_ID` y `PIXEL_ID` arriba de `index.html` cuando existan (solo se cargan si la persona acepta cookies).

## Paso único en Cloudflare (5 minutos)
1. dash.cloudflare.com > Workers & Pages > Create > Pages > Connect to Git > repo `azul-beep/handycalcs`.
2. Project name: `blueautomatica`. Production branch: `main`. Framework: None. Build command: vacío. Build output directory: `blue/web`.
3. Settings > Builds > Build watch paths: incluir solo `blue/web/*`.
4. Save and Deploy. Probar https://blueautomatica.pages.dev y pegar ese link en el perfil de Instagram.
