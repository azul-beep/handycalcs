# Permiso de Meta: una sola vez, para que GitHub publique y lea números solo (Cozy y Blue)

Con esto, Claude deja de manejar el Chrome de Azu para programar posts y leer estadísticas (lo que más uso gasta).
Los tokens se pegan SOLO en GitHub (Settings > Secrets). Nunca en el chat, en un archivo ni en un issue.

## Lo único de Azu
Entrar con su Facebook en https://developers.facebook.com/apps/1109634448361462/dashboard/ (si pide "Confirmar cuenta",
confirmarla). Con eso abierto, el Agente Cozy hace todo lo demás en su Chrome.

## Lo que hace el Agente Cozy en el Chrome de Azu (unos 10 minutos)
1. Abrir https://developers.facebook.com/tools/explorer/ . Meta App: **Cozy Paws Poster**. User or Page: **User Token**.
2. Permisos: `pages_show_list`, `pages_read_engagement`, `pages_manage_posts`, `instagram_basic`,
   `instagram_content_publish`, `instagram_manage_insights`, `read_insights`, `business_management`.
3. **Generate Access Token**. En la ventana de Meta elegir las DOS páginas (**Cozy Paws** y **Blue en Automático**) y las
   DOS cuentas de Instagram (**@cozypawsgifts** y **@blue.automatica**).
4. Alargar el token: https://developers.facebook.com/tools/debug/accesstoken/ > pegar > **Debug** > **Extend Access Token**.
5. En el Explorer, con el token largo, pedir `me/accounts?fields=id,name,access_token,instagram_business_account`.
6. De la respuesta salen 5 datos. Cargarlos en https://github.com/azul-beep/handycalcs/settings/secrets/actions
   (**New repository secret**, o **Update** si ya existe):
   1. Cozy Paws: `access_token` → `FB_PAGE_TOKEN` · `id` → `FB_PAGE_ID` · `instagram_business_account.id` → `IG_USER_ID`
   2. Blue en Automático: `access_token` → `BLUE_FB_TOKEN` · `instagram_business_account.id` → `BLUE_IG_USER_ID`
7. Opcional: el Debugger con cada token de página tiene que decir **Expires: Never**.
8. Cerrar las pestañas de Meta y de GitHub (la PC de Azu tiene poca memoria).

## Probar sin publicar nada (lo hace cualquier hilo, sin Chrome)
1. Actions > **Blue (Instagram)** > Run workflow > `revisar` → "Clave OK: @blue.automatica".
2. Actions > **Cozy Paws (reels a Instagram)** > Run workflow > `revisar` → "Clave OK: @cozypawsgifts".
3. Actions > **Cozy Paws (estadísticas de redes)** > Run workflow → `cozypaws/estadisticas/redes.md` sin "Permisos que faltan".

## Qué queda andando solo después
1. Reels aprobados de Blue y de Cozy: se suben a su cola (rama `blue-videos` / `cozy-videos`) y salen solos a su hora.
2. Estadísticas diarias de Cozy y Blue, y el informe "qué anduvo mejor" cada lunes (issue + `informes/`).
3. Si un token deja de andar (por ejemplo, cambio de contraseña de Facebook), los workflows avisan y se repiten
   los pasos 1-6. Cambiar la contraseña de Facebook invalida los tokens: avisar antes.
