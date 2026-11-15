# Linen & Sage: productos digitales para Payhip (agenda digital, Notion, Canva y fondos)

Son 11 productos nuevos para la misma tienda de Payhip de Linen & Sage (ver `../imprimibles/payhip-y-pinterest.md` para abrir la tienda).
Cada carpeta tiene: el archivo que se vende, `imagenes/` (3 fotos para Payhip, 1600x1600) y `pinterest/` (2 pines, 1000x1500).
Vista rápida de los 22 pines: `los-22-pines.jpg`. Código para regenerar todo: `fuente/`.

Nada se publica sin el OK de Azu. Todo lo de cuentas (Notion, Canva, Payhip, Pinterest) se hace desde el Chrome de Azu.

---

## Parte A: Qué está listo y qué falta

1. **Listos para subir a Payhip ya** (no necesitan nada más): las 2 agendas digitales y los 3 packs de fondos de pantalla.
2. **Necesitan un paso en Notion antes** (Parte B): las 4 plantillas de Notion. Hay que armarlas en el Notion de Azu con los CSV de `para-armar/`, publicarlas y pegar el link en el PDF de acceso.
3. **Necesitan un paso en Canva antes** (Parte C): los 2 kits de Canva. Hay que importar el PDF en el Canva de Azu y sacar el "link de plantilla".
4. Los PDF de acceso hoy dicen **LINK PENDIENTE**. Cuando estén los links, se regeneran con:
   `python3 fuente/access.py <carpeta> budget-en=<link> budget-es=<link> meal-en=<link> meal-es=<link> canva-en=<link> canva-es=<link>`
5. Las imágenes de Notion muestran una vista de cómo queda la plantilla terminada. Cuando esté armada en Notion, conviene reemplazar `2-por-dentro.jpg` por una captura real.

---

## Parte B: Armar las plantillas de Notion (cuenta gratis de Notion sirve)

Se repite para cada una: `notion-budget-en`, `notion-budget-es`, `notion-meal-en`, `notion-meal-es`. Los nombres van en el idioma de cada una.

### B1. Pasos comunes
1. En Notion, crear una página nueva con el título de la plantilla (por ejemplo "Presupuesto mensual"), ícono 🌿 (presupuesto) o 🥗 (comidas), y de portada subir `para-armar/portada-notion.png`.
2. Debajo del título, escribir la frase de bienvenida (está en la descripción de cada producto, Parte D).
3. Descomprimir el .zip de `para-armar/`. Para cada CSV: menú lateral > **Import** > **CSV** > elegir el archivo. Notion crea una base de datos por archivo.
4. Mover cada base importada adentro de la página de la plantilla (los tres puntos de la base > **Move to** > la página).
5. Revisar los tipos de cada columna (clic en el nombre de la columna > **Edit property** > **Type**). Lo que va en cada una está en B2 y B3.
6. Revisar que las filas de ejemplo se vean bien y dejar la primera fila con la nota "borrala / delete me".
7. Publicar: **Share** > **Publish** > activar **Allow duplicate as template** (Permitir duplicar como plantilla) > copiar el link.
8. Pasar el link para regenerar el PDF de acceso (Parte A, punto 4). Probarlo desde una ventana de incógnito: tiene que aparecer el botón "Duplicate".

### B2. Presupuesto (Budget Planner / Presupuesto mensual)
1. **Transactions / Movimientos**: Date/Fecha = Date. Amount/Monto = Number, formato US Dollar. Type/Tipo, Account/Cuenta = Select. Category/Categoría = **Relation** con la base Categories/Categorías, con **Show on Categories** activado para que la relación vaya en los dos sentidos (si las filas de ejemplo no se vinculan solas, elegir la categoría en cada una).
2. Vistas de Movimientos:
   1. "This month / Este mes": tabla con filtro Date **is within** **this month**, y en el pie de Amount elegir **Sum**.
   2. "By category / Por categoría": tabla agrupada por Category.
   3. "Calendar / Calendario": vista de calendario por Date.
3. Resumen arriba de todo: agregar una vista enlazada (escribir `/linked view`) de Movimientos, filtrada a este mes, **agrupada por Tipo**, con Sum en Monto. Así se ven "Ingresos del mes" y "Gastos del mes".
4. **Categories / Categorías**: Monthly budget/Presupuesto mensual = Number (US Dollar), Group/Grupo = Select. Agregar una propiedad **Formula** llamada "Spent this month / Gastado este mes":
   `prop("Transactions").filter(formatDate(current.prop("Date"), "YYYY-MM") == formatDate(now(), "YYYY-MM")).map(current.prop("Amount")).sum()`
   (en la versión en español, cambiar los nombres: `prop("Movimientos")`, `prop("Fecha")`, `prop("Monto")`).
   Y otra fórmula "Left / Disponible": `prop("Monthly budget") - prop("Spent this month")` (en español: `prop("Presupuesto mensual") - prop("Gastado este mes")`).
5. **Bills / Cuentas a pagar**: Due day = Number, Amount = Number (US Dollar), Autopay y Paid this month = **Checkbox** (revisar que "Yes/Sí" quede tildado y "No" sin tildar). Ordenar por Due day.
6. **Savings goals / Metas de ahorro**: Goal y Saved = Number (US Dollar), Target date = Date. Fórmula "Progress / Avance": `prop("Saved") / prop("Goal")`, formato **Percent** y **Show as: Bar**.

### B3. Comidas (Meal Planner / Planificador de comidas)
1. **Recipes / Recetas**: Meal/Comida = Select. Time y Servings = Number. Tags/Etiquetas = **Multi-select** (Notion separa por coma). Link = URL.
2. Vistas de Recetas: "By meal / Por comida" (Board agrupado por Comida), "All recipes / Todas" (tabla) y "Gallery / Galería".
3. **Weekly plan / Menú semanal**: Breakfast, Lunch, Dinner, Snack (Desayuno, Almuerzo, Cena, Colación) = **Relation** con Recetas. Si no se vinculan solas, elegir la receta en cada celda de ejemplo.
4. **Grocery list / Lista del súper**: Aisle/Sección = Select, Bought/Comprado = Checkbox. Vista "To buy / Para comprar": Board agrupado por Sección con filtro Comprado sin tildar.

---

## Parte C: Armar los kits de Canva (cuenta gratis de Canva sirve)

1. Entrar a canva.com > **Create a design** > **Import file** y subir el PDF del kit (`canva-kit-en/Budget-and-Meal-Planner-Kit.pdf` o `canva-kit-es/Kit-Presupuesto-y-Comidas.pdf`). Canva lo convierte en un diseño editable de 7 páginas.
2. Revisar que las letras sean DM Serif Display, Lora y Josefin Sans (están en Canva gratis). Si alguna cambió, elegirla de nuevo.
3. Ponerle nombre al diseño: "Linen & Sage · Budget & Meal Planner Kit" o "Linen & Sage · Kit de presupuesto y comidas".
4. **Share** > **See all** > **Template link** (Enlace de plantilla) > copiar el link.
5. Probar el link en una ventana de incógnito: tiene que decir "Use template".
6. Pasar el link para regenerar el PDF de acceso (Parte A, punto 4).
7. En Payhip se suben DOS archivos por kit: el PDF de acceso y el PDF del kit (listo para imprimir).

---

## Parte D: Textos de cada producto en Payhip

### 1. 2027 Digital Planner (inglés) · 7,99 USD
- Archivo: `agenda-digital-2027-en/Digital-Planner-2027.pdf`
- Title: 2027 Digital Planner for GoodNotes and Notability | Hyperlinked iPad Planner | Monday Start
- Description:
  Your whole 2027 on your tablet, calm and simple. Tap a tab, land on the right page.
  What's included:
  1. 101 hyperlinked pages with more than 2,000 links.
  2. Year at a glance, yearly goals and a welcome page with an index.
  3. 12 monthly calendars: tap any day to jump to that week.
  4. 53 weekly pages (Monday start) with a priorities list.
  5. 12 monthly habit trackers and 20 note pages (lined and dot grid).
  6. Landscape layout for iPad and Android tablets.
  Works with GoodNotes, Notability, Noteshelf, Xodo and any PDF app that supports links. This is a digital download: nothing will be shipped.

### 2. Agenda digital 2027 en español · 6,99 USD
- Archivo: `agenda-digital-2027-es/Agenda-Digital-2027.pdf`
- Título: Agenda digital 2027 en español para GoodNotes | Con links | Semana de lunes a domingo
- Descripción:
  Tu 2027 en la tablet, en orden y con calma. Tocás una pestaña y llegás a la página justa.
  Qué incluye:
  1. 101 páginas con más de 2.000 links.
  2. Año de un vistazo, metas del año y un índice de bienvenida.
  3. 12 calendarios mensuales: tocás un día y vas directo a esa semana.
  4. 53 páginas semanales, de lunes a domingo, con prioridades.
  5. 12 páginas de hábitos y 20 páginas de notas (renglones y puntos).
  6. Formato horizontal para iPad y tablets Android.
  Funciona en GoodNotes, Notability, Noteshelf, Xodo y cualquier app de PDF con links. Es un producto digital: no se envía nada por correo.

### 3. Botanical Calm: Phone Wallpapers (inglés) · 3,99 USD
- Archivo: `botanical-calm/Botanical-Calm-Wallpapers.zip`
- Title: Boho Botanical Phone Wallpapers | 20 Minimalist iPhone and Android Backgrounds
- Description:
  Soft colors for a calmer phone. 20 boho botanical wallpapers with arches, rainbows, hills and leaves.
  What's included:
  1. 20 wallpapers in 6 soft palettes.
  2. No text, with a clean top area for your clock.
  3. High resolution PNG, 1290 x 2796 px.
  4. Works on iPhone and Android.
  Instant download for personal use.

### 4. Gentle Words: Affirmation Wallpapers (inglés) · 3,99 USD
- Archivo: `gentle-words-en/Gentle-Words-Wallpapers.zip`
- Title: Affirmation Phone Wallpapers | 20 Boho Positive Quote Backgrounds for iPhone and Android
- Description:
  A kind reminder every time you unlock your phone. 20 gentle affirmations on soft botanical designs.
  What's included:
  1. 20 affirmation wallpapers ("I am allowed to rest", "Small steps still count" and more).
  2. Boho botanical designs in soft colors.
  3. High resolution PNG, 1290 x 2796 px.
  4. Works on iPhone and Android.
  Instant download for personal use.

### 5. Palabras amables: fondos con frases (español) · 2,99 USD
- Archivo: `palabras-amables-es/Palabras-Amables-Fondos.zip`
- Título: Fondos de pantalla con frases en español | 20 afirmaciones para iPhone y Android
- Descripción:
  Un recordatorio amable cada vez que mirás el celular. 20 afirmaciones en español con diseños boho.
  Qué incluye:
  1. 20 fondos con frases ("Me permito descansar", "Un día a la vez" y más).
  2. Diseños botánicos en colores suaves.
  3. PNG en alta resolución, 1290 x 2796 px.
  4. Para iPhone y Android.
  Descarga inmediata, uso personal.

### 6. Notion Budget Planner (inglés) · 6,99 USD
- Archivo: `notion-budget-en/Notion-Budget-Planner-Access.pdf` (con el link ya cargado)
- Title: Notion Budget Planner Template | Monthly Budget, Bill Tracker and Savings Goals
- Description:
  See where your money goes, calmly. A simple budget planner for Notion that works on the free plan.
  What's included:
  1. Transactions with monthly totals and a calendar view.
  2. Categories with budget vs. spent this month.
  3. Bill tracker with due dates and autopay.
  4. Savings goals with progress bars.
  5. Example rows so you can see how it works.
  You get a PDF with the link to duplicate the template into your Notion. Requires a Notion account (free).

### 7. Presupuesto mensual en Notion (español) · 5,99 USD
- Archivo: `notion-budget-es/Notion-Presupuesto-Acceso.pdf` (con el link ya cargado)
- Título: Plantilla de presupuesto en Notion en español | Gastos, cuentas a pagar y ahorro
- Descripción:
  Mirá a dónde va tu plata, con calma. Un presupuesto simple para Notion que funciona con la cuenta gratis.
  Qué incluye:
  1. Movimientos con totales del mes y vista de calendario.
  2. Categorías: previsto contra gastado este mes.
  3. Cuentas a pagar con vencimientos y débito automático.
  4. Metas de ahorro con barra de avance.
  5. Filas de ejemplo para ver cómo se usa.
  Recibís un PDF con el link para duplicar la plantilla en tu Notion. Necesitás una cuenta de Notion (gratis).

### 8. Notion Meal Planner (inglés) · 5,99 USD
- Archivo: `notion-meal-en/Notion-Meal-Planner-Access.pdf` (con el link ya cargado)
- Title: Notion Meal Planner and Recipe Organizer | Weekly Menu and Grocery List Template
- Description:
  Plan the week in 10 minutes. Save your recipes, build your menu and never forget the grocery list.
  What's included:
  1. Recipe database with 13 starter recipes.
  2. Weekly menu, from breakfast to snack.
  3. Grocery list sorted by aisle.
  4. Views by meal, gallery and this week.
  You get a PDF with the link to duplicate the template into your Notion. Requires a Notion account (free).

### 9. Planificador de comidas en Notion (español) · 4,99 USD
- Archivo: `notion-meal-es/Notion-Planificador-Comidas-Acceso.pdf` (con el link ya cargado)
- Título: Planificador de comidas en Notion en español | Recetario, menú semanal y lista del súper
- Descripción:
  Armá el menú de la semana en 10 minutos. Guardá tus recetas y tené la lista del súper a mano.
  Qué incluye:
  1. Recetario con 13 recetas para empezar.
  2. Menú semanal, del desayuno a la colación.
  3. Lista del súper por sección.
  4. Vistas por comida, galería y semana.
  Recibís un PDF con el link para duplicar la plantilla en tu Notion. Necesitás una cuenta de Notion (gratis).

### 10. Budget & Meal Planner Kit for Canva (inglés) · 5,99 USD
- Archivos: `canva-kit-en/Canva-Kit-Access.pdf` (con el link) y `canva-kit-en/Budget-and-Meal-Planner-Kit.pdf`
- Title: Editable Budget and Meal Planner Canva Template | Printable Bill Tracker, Grocery List | US Letter
- Description:
  Change colors and text in minutes, then print. 7 matching pages to organize money and meals.
  What's included:
  1. Monthly budget with summary.
  2. Bill tracker and expense log.
  3. 100-step savings tracker.
  4. Weekly meal planner, grocery list and recipe page.
  5. Canva template link plus a ready-to-print PDF (US Letter).
  Edit with a free Canva account. Digital download for personal use.

### 11. Kit de presupuesto y comidas para Canva (español) · 4,99 USD
- Archivos: `canva-kit-es/Canva-Kit-Acceso.pdf` (con el link) y `canva-kit-es/Kit-Presupuesto-y-Comidas.pdf`
- Título: Plantilla de presupuesto y menú semanal editable en Canva | Lista del súper imprimible
- Descripción:
  Cambiá colores y textos en minutos, y después imprimí. 7 páginas que combinan para ordenar la plata y las comidas.
  Qué incluye:
  1. Presupuesto mensual con resumen.
  2. Control de pagos y registro de gastos.
  3. Seguimiento de ahorro de 100 pasos.
  4. Menú semanal, lista del súper y página de receta.
  5. Link a la plantilla de Canva y PDF listo para imprimir (tamaño Carta).
  Se edita con la cuenta gratis de Canva. Producto digital para uso personal.

### Combos sugeridos (Products > Add product > Bundle)
1. Wallpaper Bundle (Botanical + Gentle Words): 5,99 USD.
2. Notion Home Bundle (Budget + Meal Planner): 9,99 USD.
3. Combo Notion en español (Presupuesto + Comidas): 8,99 USD.

---

## Parte E: Pines de Pinterest (cuenta de Linen & Sage)

Tableros nuevos para sumar a los 4 que ya están: 5. Digital Planners, 6. Phone Wallpapers, 7. Notion Templates, 8. Budget and Meal Planning. Los pines en español van a "Agendas y diarios en español".
Igual que antes: 2 o 3 pines por día, programados con "Publish later", cada uno con el link a su producto en Payhip.

1. agenda-digital-2027-en/pin-1 · "2027 Digital Planner for GoodNotes" · "A calm, hyperlinked 2027 planner for iPad and Android tablets: monthly, weekly, goals and habits. Instant download." · Digital Planners
2. agenda-digital-2027-en/pin-2 · "Tap any day to jump to that week" · "101 pages and 2,000+ links. Works in GoodNotes, Notability and Noteshelf. Monday start." · Digital Planners
3. agenda-digital-2027-es/pin-1 · "Agenda digital 2027 en español para GoodNotes" · "Agenda 2027 con links para iPad y tablets: meses, semanas, metas y hábitos. Descarga inmediata." · Agendas y diarios en español
4. agenda-digital-2027-es/pin-2 · "Tocá un día y vas directo a esa semana" · "101 páginas y más de 2.000 links. Para GoodNotes, Notability y Noteshelf." · Agendas y diarios en español
5. botanical-calm/pin-1 · "Boho Botanical Phone Wallpapers" · "20 minimalist wallpapers in soft sage, blush and terracotta. iPhone and Android, high resolution." · Phone Wallpapers
6. botanical-calm/pin-2 · "Soft colors for a calmer phone" · "Arches, rainbows, hills and leaves. A clean lock screen with room for your clock." · Phone Wallpapers
7. gentle-words-en/pin-1 · "Affirmation Wallpapers for Your Phone" · "20 boho wallpapers with gentle affirmations like 'I am allowed to rest'. iPhone and Android." · Phone Wallpapers
8. gentle-words-en/pin-2 · "A kind reminder every time you unlock" · "Positive quote wallpapers in soft botanical colors. Instant download." · Phone Wallpapers
9. palabras-amables-es/pin-1 · "Fondos de pantalla con frases en español" · "20 fondos boho con afirmaciones como 'Me permito descansar'. Para iPhone y Android." · Agendas y diarios en español
10. palabras-amables-es/pin-2 · "Un recordatorio amable cada vez que mirás el celu" · "Frases lindas en español sobre diseños botánicos en colores suaves. Descarga inmediata." · Agendas y diarios en español
11. notion-budget-en/pin-1 · "Simple Notion Budget Planner Template" · "Track spending, bills and savings goals in Notion. Works on the free plan." · Notion Templates
12. notion-budget-en/pin-2 · "See where your money goes, calmly" · "A clean Notion budget with monthly totals, budget vs. spent and savings progress bars." · Budget and Meal Planning
13. notion-budget-es/pin-1 · "Plantilla de presupuesto en Notion en español" · "Gastos, cuentas a pagar y metas de ahorro en Notion. Funciona con la cuenta gratis." · Agendas y diarios en español
14. notion-budget-es/pin-2 · "Mirá a dónde va tu plata, con calma" · "Un presupuesto mensual simple en Notion, con totales del mes y barras de ahorro." · Agendas y diarios en español
15. notion-meal-en/pin-1 · "Notion Meal Planner and Recipe Organizer" · "Weekly menu, recipe database and grocery list by aisle in one Notion template." · Notion Templates
16. notion-meal-en/pin-2 · "Plan the week in 10 minutes" · "Save recipes, plan breakfast to dinner and tick off your grocery list. Free Notion plan." · Budget and Meal Planning
17. notion-meal-es/pin-1 · "Planificador de comidas en Notion en español" · "Recetario, menú semanal y lista del súper por sección en una sola plantilla de Notion." · Agendas y diarios en español
18. notion-meal-es/pin-2 · "Armá el menú de la semana en 10 minutos" · "Guardá tus recetas y tené la lista del súper siempre a mano. Funciona con Notion gratis." · Agendas y diarios en español
19. canva-kit-en/pin-1 · "Editable Budget and Meal Planner in Canva" · "7 matching printable pages: budget, bills, savings, meal plan and grocery list. Edit in free Canva." · Budget and Meal Planning
20. canva-kit-en/pin-2 · "Change colors and text in minutes" · "A Canva template kit plus a ready-to-print PDF. US Letter." · Budget and Meal Planning
21. canva-kit-es/pin-1 · "Presupuesto y menú semanal editables en Canva" · "7 páginas para imprimir: presupuesto, pagos, ahorro, menú semanal y lista del súper." · Agendas y diarios en español
22. canva-kit-es/pin-2 · "Cambiá colores y textos en minutos" · "Plantilla de Canva más un PDF listo para imprimir. Tamaño Carta." · Agendas y diarios en español
