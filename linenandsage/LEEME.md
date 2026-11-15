# Linen & Sage: web automática (https://linenandsage.pages.dev)

1. `payhip-links.md`: una línea por producto publicado en Payhip: `<carpeta> <link>`. Es lo único que se toca al publicar un producto nuevo.
2. Al hacer push, el workflow `.github/workflows/linenandsage.yml` corre `build.py`, rearma `site/` y lo sube. Solo aparecen en la web los productos que ya tienen link de Payhip.
3. Cloudflare Pages publica `site/` sola (proyecto conectado a este repo). Pinterest (linenandsageprints) lee `site/feed.xml` y crea los pines solo.
4. `fuente/`: textos de Payhip e imágenes (copiados de la carpeta del proyecto `kdp-linen-sage/`). Producto nuevo de otra carpeta: copiar su `imagenes/` y `pinterest/pin-1.jpg` acá y sumar su carpeta en `FOLDERS` de `build.py`.
5. Meta de verificación de Pinterest ya incluida (`pinterest_verify` en `build.py`).

## Paso único en Cloudflare (lo hace el hilo de Chrome)
1. dash.cloudflare.com > Workers & Pages. Si ya existe un proyecto `linenandsage` subido a mano (Direct Upload), no se puede conectar a GitHub: borrarlo (Settings > Delete project) para liberar el nombre.
2. Create > Pages > Connect to Git > repo `azul-beep/handycalcs`.
3. Project name: `linenandsage`. Production branch: `main`. Framework: None. Build command: vacío. Build output directory: `linenandsage/site`.
4. Settings > Builds > Build watch paths: incluir solo `linenandsage/*` (así no se republica con cada cambio de las otras webs).
5. Save and Deploy. Probar https://linenandsage.pages.dev.
