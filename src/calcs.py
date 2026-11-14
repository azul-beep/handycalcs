# -*- coding: utf-8 -*-
"""Calculator definitions: inputs, outputs and bilingual SEO content."""

def N(key, en, es, default, step="any", unit="", minv="0"):
    return dict(kind="num", key=key, en=en, es=es, default=default, step=step, unit=unit, min=minv)

def S(key, en, es, options, default):
    return dict(kind="select", key=key, en=en, es=es, options=options, default=default)

def TA(key, en, es, default_en, default_es, rows=6):
    return dict(kind="textarea", key=key, en=en, es=es, default_en=default_en, default_es=default_es, rows=rows)

def TX(key, en, es, default):
    return dict(kind="text", key=key, en=en, es=es, default=default)

def D(key, en, es, default):
    """Date input (YYYY-MM-DD). default="today" uses the visitor's date."""
    return dict(kind="date", key=key, en=en, es=es, default=default)

def TR(key, en, es, start="", end="", brk=""):
    """Time-card row: start time, end time, unpaid break in minutes."""
    return dict(kind="timerow", key=key, en=en, es=es, default=(start, end, brk))

def O(key, en, es, big=False, pre=False):
    return dict(key=key, en=en, es=es, big=big, pre=pre)

YESNO = [("yes", "Yes", "Sí"), ("no", "No", "No")]

CATS = {
    "restaurant": ("Restaurant & tips", "Restaurante y propinas"),
    "kitchen": ("Kitchen & recipes", "Cocina y recetas"),
    "work": ("Work & pay", "Trabajo y sueldo"),
    "money": ("Budget & money", "Presupuesto y dinero"),
    "everyday": ("Everyday math", "Cuentas de todos los días"),
    "health": ("Health & fitness", "Salud y ejercicio"),
    "school": ("School & grades", "Escuela y notas"),
}

CALCS = [
# ---------------------------------------------------------------- TIP
dict(id="tip", cat="restaurant", aff="restaurant",
 inputs=[N("bill","Bill amount","Total de la cuenta",60,"0.01","$"),
         N("tip","Tip percentage","Porcentaje de propina",20,"0.5","%"),
         N("people","Number of people","Cantidad de personas",1,"1","","1")],
 presets=("tip",[15,18,20,22,25]),
 outputs=[O("tipAmt","Tip","Propina"),O("total","Total with tip","Total con propina",True),
          O("perPerson","Each person pays","Paga cada uno"),O("tipPerPerson","Tip per person","Propina por persona")],
 related=["split","tipout","salestax"],
 en=dict(slug="tip-calculator", title="Tip Calculator: How Much to Tip (15%, 18%, 20%)",
  h1="Tip Calculator", desc="Free tip calculator. Enter the bill, pick 15%, 18%, 20% or any tip and split it between people. Instant, no sign-up.",
  intro="Work out the tip and the total in one second, and split it between everyone at the table.",
  body="""<h2>How to calculate a tip</h2>
<p>Multiply the bill by the tip percentage and divide by 100. For a $60 bill and a 20% tip: 60 × 20 ÷ 100 = <strong>$12</strong>, so the total is $72. If four people split it, each pays $18.</p>
<h2>Quick mental math</h2>
<ul><li><strong>10%</strong>: move the decimal point one place to the left ($60 → $6).</li>
<li><strong>20%</strong>: double the 10% ($6 × 2 = $12).</li>
<li><strong>15%</strong>: 10% plus half of it ($6 + $3 = $9).</li>
<li><strong>18%</strong>: 20% minus 2% ($12 − $1.20 = $10.80).</li></ul>
<h2>How much should you tip in the US?</h2>
<p>For table service at a sit-down restaurant, 18% to 20% is standard today, and 15% is the usual minimum for acceptable service. Servers in many states earn a lower "tipped minimum wage", so tips are a big part of their pay. For counter service, coffee or takeout, tipping is optional; $1 or 10% is common. Delivery drivers usually get 15% to 20% or at least $3–5.</p>
<h2>Should I tip on the total before or after tax?</h2>
<p>Etiquette guides say tipping on the pre-tax amount is fine. Many people tip on the total because it is easier. The difference is small: on a $60 bill with 7% tax it is under $1.</p>""",
  faq=[("What is a good tip percentage?","For good table service in the US, 18% to 20%. Use 15% as a minimum and 25% or more for excellent service."),
       ("How do I split the tip between friends?","Enter the number of people and the calculator divides both the tip and the total. For uneven bills use the split-the-bill calculator."),
       ("Is the tip included in the bill?","Check for a 'service charge' or 'gratuity' line, common for groups of 6 or more. If it is there, you do not need to tip again.")]),
 es=dict(slug="calculadora-de-propinas", title="Calculadora de propinas: cuánto dejar (15%, 18%, 20%)",
  h1="Calculadora de propinas", desc="Calculadora de propinas gratis. Pon el total, elige 15%, 18%, 20% o el porcentaje que quieras y divídelo entre varias personas.",
  intro="Saca la propina y el total en un segundo, y divídelo entre todos los de la mesa.",
  body="""<h2>Cómo calcular la propina</h2>
<p>Multiplica la cuenta por el porcentaje y divide por 100. Para una cuenta de $60 con 20%: 60 × 20 ÷ 100 = <strong>$12</strong>, así que el total es $72. Si son cuatro, paga $18 cada uno.</p>
<h2>Trucos para calcular de cabeza</h2>
<ul><li><strong>10%</strong>: corre la coma un lugar a la izquierda ($60 → $6).</li>
<li><strong>20%</strong>: el doble del 10% ($6 × 2 = $12).</li>
<li><strong>15%</strong>: el 10% más la mitad ($6 + $3 = $9).</li>
<li><strong>18%</strong>: el 20% menos un 2% ($12 − $1,20 = $10,80).</li></ul>
<h2>¿Cuánta propina se deja en Estados Unidos?</h2>
<p>En restaurantes con servicio de mesa lo normal hoy es entre 18% y 20%, y 15% es el mínimo para un buen servicio. En muchos estados los meseros cobran un salario mínimo reducido ("tipped minimum wage"), así que la propina es gran parte de su sueldo. En mostrador, café o comida para llevar es opcional: se suele dejar $1 o un 10%. A los repartidores se les deja entre 15% y 20%, o al menos $3 a $5.</p>
<h2>¿La propina va sobre el total con o sin impuesto?</h2>
<p>Lo correcto es calcularla sobre el monto antes del impuesto, pero mucha gente la calcula sobre el total porque es más fácil. La diferencia es chica: en una cuenta de $60 con 7% de impuesto es menos de $1.</p>""",
  faq=[("¿Qué porcentaje de propina es bueno?","En Estados Unidos, entre 18% y 20% para un buen servicio de mesa. 15% como mínimo y 25% o más si el servicio fue excelente."),
       ("¿Cómo divido la propina entre amigos?","Pon la cantidad de personas y la calculadora divide la propina y el total. Si cada uno consumió distinto, usa la calculadora para dividir la cuenta."),
       ("¿La propina ya viene incluida?","Fíjate si la cuenta tiene una línea de 'service charge' o 'gratuity', algo común en grupos de 6 o más. Si está, no hace falta dejar otra.")])),

# ---------------------------------------------------------------- SPLIT
dict(id="split", cat="restaurant", aff="restaurant",
 inputs=[N("subtotal","Subtotal (before tax)","Subtotal (sin impuesto)",120,"0.01","$"),
         N("tax","Sales tax on the bill","Impuesto de la cuenta",8.4,"0.01","$"),
         N("tip","Tip percentage","Porcentaje de propina",20,"0.5","%"),
         S("pretax","Tip on the pre-tax amount?","¿Propina sobre el monto sin impuesto?",YESNO,"yes"),
         N("people","Number of people","Cantidad de personas",4,"1","","1")],
 outputs=[O("each","Each person pays","Paga cada uno",True),O("total","Total","Total"),O("tipAmt","Tip","Propina"),
          O("rounded","Rounded up per person","Redondeado por persona")],
 related=["tip","tipout","percent"],
 en=dict(slug="split-the-bill-calculator", title="Split the Bill Calculator with Tax and Tip",
  h1="Split the Bill Calculator", desc="Split a restaurant bill evenly with tax and tip included. Shows what each person pays, rounded up so nobody comes up short.",
  intro="Divide a restaurant check fairly, with tax and tip, and see a rounded amount that makes paying in cash easy.",
  body="""<h2>How the split works</h2>
<p>The calculator adds the tax and the tip to the subtotal and divides the total by the number of people. Tip is calculated on the pre-tax subtotal by default, which is what most etiquette guides recommend. Switch it to "No" to tip on the total including tax.</p>
<h2>Example</h2>
<p>Four friends, a $120 subtotal, $8.40 of tax and a 20% tip. The tip is $24, the total is $152.40, and each person pays <strong>$38.10</strong>. Rounded up, each pays $39 and the server gets an extra $3.60.</p>
<h2>When an even split is not fair</h2>
<p>If someone only had a salad and someone else had steak and two drinks, it is fairer to pay for what each person ordered and add the same tip percentage to each. Ask the server for separate checks before ordering when the group is big; many restaurants cannot split after the bill is printed.</p>""",
  faq=[("How do you split a bill with tax and tip?","Add tax and tip to the subtotal, then divide by the number of people. This calculator does it in one step."),
       ("Should tip be calculated before tax?","Most etiquette experts say yes. The default here tips on the pre-tax subtotal; you can change it."),
       ("What if someone pays in cash?","Use the rounded-up amount so the total covers the bill. The leftover goes to the tip.")]),
 es=dict(slug="calculadora-dividir-la-cuenta", title="Calculadora para dividir la cuenta con impuesto y propina",
  h1="Dividir la cuenta", desc="Divide la cuenta del restaurante en partes iguales con impuesto y propina. Muestra cuánto paga cada uno, redondeado para pagar en efectivo.",
  intro="Divide la cuenta del restaurante en partes iguales, con impuesto y propina, y mira un monto redondeado para pagar en efectivo sin vueltas.",
  body="""<h2>Cómo se divide</h2>
<p>La calculadora suma el impuesto y la propina al subtotal y divide por la cantidad de personas. Por defecto la propina se calcula sobre el subtotal sin impuesto, que es lo que recomiendan las guías de etiqueta. Cámbialo a "No" si quieres calcularla sobre el total con impuesto.</p>
<h2>Ejemplo</h2>
<p>Cuatro amigos, subtotal de $120, impuesto de $8,40 y propina del 20%. La propina es $24, el total $152,40 y cada uno paga <strong>$38,10</strong>. Redondeando, paga $39 cada uno y el mesero se lleva $3,60 más.</p>
<h2>Cuándo no conviene dividir en partes iguales</h2>
<p>Si alguien comió solo una ensalada y otro un bistec con dos tragos, es más justo que cada uno pague lo suyo más el mismo porcentaje de propina. Si son muchos, pide cuentas separadas antes de ordenar: muchos restaurantes no pueden dividir una vez impresa la cuenta.</p>""",
  faq=[("¿Cómo se divide una cuenta con impuesto y propina?","Se suma el impuesto y la propina al subtotal y se divide por la cantidad de personas. Esta calculadora lo hace en un paso."),
       ("¿La propina se calcula antes del impuesto?","La mayoría de los expertos en etiqueta dice que sí. Aquí viene así por defecto, pero lo puedes cambiar."),
       ("¿Y si alguien paga en efectivo?","Usa el monto redondeado para que alcance. Lo que sobra queda como propina.")])),

# ---------------------------------------------------------------- TIP OUT
dict(id="tipout", cat="restaurant", aff="restaurant",
 inputs=[N("pool","Total tips to share","Total de propinas",850,"0.01","$"),
         N("share","Percent of tips that go to the pool","Porcentaje que va al pozo",100,"1","%"),
         TX("hours","Hours worked by each person (comma separated)","Horas de cada persona (separadas por coma)","8, 6.5, 5, 4")],
 outputs=[O("rate","Tips per hour","Propina por hora",True),O("shared","Amount shared","Monto repartido"),
          O("kept","Amount not in the pool","Monto fuera del pozo"),O("shares","Each person's share","Lo que le toca a cada uno",pre=True)],
 related=["tip","hourly","overtime"],
 en=dict(slug="tip-pool-calculator", title="Tip Pool Calculator: Split Tips by Hours Worked",
  h1="Tip Pool Calculator (by hours)", desc="Split pooled tips between restaurant staff by hours worked. Enter the total tips and each person's hours to get every share.",
  intro="Split a tip pool fairly between servers, bartenders, bussers and runners based on the hours each person worked.",
  body="""<h2>How a tip pool by hours works</h2>
<p>All the tips for the shift go into one pool. The pool is divided by the total hours worked to get a tip rate per hour, and each person gets that rate times their own hours. Someone who worked 8 hours gets twice what someone who worked 4 hours gets.</p>
<h2>Example</h2>
<p>$850 in tips and four people who worked 8, 6.5, 5 and 4 hours (23.5 hours total). The rate is $850 ÷ 23.5 = <strong>$36.17 per hour</strong>. The 8-hour shift takes $289.36 and the 4-hour shift takes $144.68.</p>
<h2>Tip-out percentage</h2>
<p>Some restaurants only pool part of the tips, for example servers tip out 20% to the support staff. Put that percent in "Percent of tips that go to the pool" and enter the hours of the support staff only.</p>
<h2>Rules to keep in mind</h2>
<p>Under the US Fair Labor Standards Act, managers and supervisors cannot keep employees' tips, and a pool that includes back-of-house staff has extra rules when the employer takes a tip credit. State laws vary, so check your state's labor department before setting up a policy.</p>""",
  faq=[("What is a fair way to split tips?","Splitting by hours worked is the most common and easiest to explain. Some teams also use points by role (for example server 1.0, busser 0.5)."),
       ("Can managers be part of the tip pool?","Under federal law, managers and supervisors cannot keep any part of employees' tips. Check your state rules too."),
       ("Does this store my staff data?","No. Everything is calculated in your browser and nothing is sent or saved.")]),
 es=dict(slug="calculadora-pozo-de-propinas", title="Calculadora de pozo de propinas: repartir por horas trabajadas",
  h1="Repartir propinas por horas", desc="Reparte el pozo de propinas entre el personal del restaurante según las horas trabajadas. Pon el total y las horas de cada uno.",
  intro="Reparte el pozo de propinas de forma justa entre meseros, barra, ayudantes y runners según las horas que trabajó cada uno.",
  body="""<h2>Cómo funciona el reparto por horas</h2>
<p>Todas las propinas del turno van a un pozo. El pozo se divide por el total de horas trabajadas para sacar cuánto toca por hora, y cada persona se lleva eso multiplicado por sus horas. Quien trabajó 8 horas cobra el doble que quien trabajó 4.</p>
<h2>Ejemplo</h2>
<p>$850 de propinas y cuatro personas que trabajaron 8; 6,5; 5 y 4 horas (23,5 horas en total). Por hora tocan $850 ÷ 23,5 = <strong>$36,17</strong>. El turno de 8 horas se lleva $289,36 y el de 4 horas, $144,68.</p>
<h2>Porcentaje para el personal de apoyo</h2>
<p>En algunos lugares solo una parte va al pozo, por ejemplo los meseros le pasan un 20% al personal de apoyo. Pon ese porcentaje en "Porcentaje que va al pozo" y carga solo las horas del personal de apoyo.</p>
<h2>Reglas a tener en cuenta</h2>
<p>Según la ley federal de Estados Unidos (FLSA), gerentes y supervisores no pueden quedarse con propinas de los empleados, y si el pozo incluye a la cocina hay reglas extra cuando el empleador usa el "tip credit". Cada estado tiene sus propias leyes: consulta el departamento de trabajo de tu estado.</p>""",
  faq=[("¿Cuál es la forma justa de repartir propinas?","Por horas trabajadas es lo más común y fácil de explicar. Algunos equipos usan puntos por puesto (por ejemplo mesero 1, ayudante 0,5)."),
       ("¿Los gerentes pueden entrar en el pozo?","Por ley federal, gerentes y supervisores no pueden quedarse con ninguna parte de las propinas de los empleados. Revisa también la ley de tu estado."),
       ("¿Se guardan los datos de mi equipo?","No. Todo se calcula en tu navegador y no se envía ni se guarda nada.")])),

# ---------------------------------------------------------------- MENU PRICE
dict(id="menuprice", cat="restaurant", aff="restaurant",
 inputs=[N("cost","Cost of the plate (ingredients)","Costo del plato (ingredientes)",4.2,"0.01","$"),
         N("target","Target food cost percentage","Costo de comida objetivo",30,"0.5","%")],
 presets=("target",[25,28,30,32,35]),
 outputs=[O("price","Menu price","Precio de menú",True),O("rounded","Price ending in .99","Precio terminado en ,99"),
          O("profit","Gross profit per plate","Ganancia bruta por plato"),O("markup","Markup","Margen sobre costo")],
 related=["foodcost","scaler","percent"],
 en=dict(slug="menu-price-calculator", title="Menu Price Calculator: Price a Dish from Food Cost",
  h1="Menu Price Calculator", desc="Price any dish from its plate cost and your target food cost percentage. Shows menu price, .99 price, gross profit and markup.",
  intro="Set the right price for a dish from what its ingredients cost and the food cost percentage you want.",
  body="""<h2>The menu pricing formula</h2>
<p><strong>Menu price = plate cost ÷ target food cost %</strong>. A plate that costs $4.20 in ingredients with a 30% target sells for $4.20 ÷ 0.30 = <strong>$14.00</strong>. Your gross profit on that plate is $9.80 before labor and rent.</p>
<h2>How to get the plate cost</h2>
<p>List every ingredient in the recipe with the amount used and its purchase price, and add them up. Include small things (oil, garnish, sauce, bread) and divide batch recipes by the number of portions. Update it when suppliers change prices.</p>
<h2>What food cost percentage to use</h2>
<ul><li><strong>25%–28%</strong>: pizza, pasta, breakfast and other cheap-ingredient dishes.</li>
<li><strong>28%–32%</strong>: typical full-service restaurant target.</li>
<li><strong>32%–40%</strong>: steaks and seafood, where a higher cost is accepted for a higher dollar profit.</li></ul>
<p>Look at the whole menu: a low-cost appetizer can balance a premium main course.</p>""",
  faq=[("What is a good food cost percentage?","Most restaurants aim for 28% to 35% overall. Fast casual is often lower, fine dining with expensive proteins can be higher."),
       ("What is the difference between markup and food cost?","Food cost is cost divided by price (30%). Markup is how much you add on top of cost (233% in the same example)."),
       ("Should prices end in .99?","Charm pricing (.99 or .95) is common in casual places. Upscale menus often use whole numbers without the dollar sign.")]),
 es=dict(slug="calculadora-precio-de-menu", title="Calculadora de precio de menú según el costo del plato",
  h1="Calculadora de precio de menú", desc="Calcula el precio de venta de un plato a partir del costo de ingredientes y el porcentaje de costo que quieres. Precio, ganancia y margen.",
  intro="Pon el precio justo a un plato según lo que cuestan sus ingredientes y el porcentaje de costo que buscas.",
  body="""<h2>La fórmula del precio de menú</h2>
<p><strong>Precio = costo del plato ÷ % de costo objetivo</strong>. Un plato que cuesta $4,20 en ingredientes con un objetivo del 30% se vende a $4,20 ÷ 0,30 = <strong>$14,00</strong>. La ganancia bruta del plato es $9,80, antes de sueldos y alquiler.</p>
<h2>Cómo sacar el costo del plato</h2>
<p>Anota cada ingrediente de la receta con la cantidad que usas y su precio de compra, y súmalos. Incluye lo chico (aceite, guarnición, salsa, pan) y en preparaciones por tanda divide por la cantidad de porciones. Actualízalo cuando los proveedores cambian precios.</p>
<h2>Qué porcentaje de costo usar</h2>
<ul><li><strong>25%–28%</strong>: pizza, pastas, desayunos y platos con ingredientes baratos.</li>
<li><strong>28%–32%</strong>: objetivo típico de un restaurante con servicio de mesa.</li>
<li><strong>32%–40%</strong>: carnes y mariscos, donde se acepta un costo más alto a cambio de más ganancia en dólares.</li></ul>
<p>Mira el menú completo: una entrada de bajo costo compensa un plato principal caro.</p>""",
  faq=[("¿Cuál es un buen porcentaje de costo de comida?","La mayoría de los restaurantes apunta a 28%–35% en total. La comida rápida suele estar más abajo y la alta cocina con proteínas caras, más arriba."),
       ("¿Qué diferencia hay entre margen y costo?","El costo es costo ÷ precio (30%). El margen sobre costo (markup) es cuánto le sumas al costo (233% en el mismo ejemplo)."),
       ("¿Conviene que el precio termine en ,99?","En lugares informales es común. Los menús más elegantes suelen usar números redondos sin el signo $.")])),

# ---------------------------------------------------------------- FOOD COST %
dict(id="foodcost", cat="restaurant", aff="restaurant",
 inputs=[N("begin","Beginning inventory","Inventario inicial",8000,"0.01","$"),
         N("purchases","Purchases during the period","Compras del período",12500,"0.01","$"),
         N("end","Ending inventory","Inventario final",7200,"0.01","$"),
         N("sales","Food sales in the period","Ventas de comida del período",43000,"0.01","$")],
 outputs=[O("pctOut","Food cost percentage","Porcentaje de costo de comida",True),O("cogs","Cost of goods sold","Costo de lo vendido"),
          O("verdict","What it means","Qué significa")],
 related=["menuprice","scaler","percent"],
 en=dict(slug="food-cost-percentage-calculator", title="Food Cost Percentage Calculator for Restaurants",
  h1="Food Cost Percentage Calculator", desc="Calculate your restaurant's food cost percentage from inventory, purchases and sales. See your cost of goods sold and if it is healthy.",
  intro="Measure your real food cost for a week or a month with the standard inventory formula.",
  body="""<h2>The food cost formula</h2>
<p><strong>Food cost % = (beginning inventory + purchases − ending inventory) ÷ food sales × 100</strong>. The part in parentheses is the cost of goods sold (COGS): what you actually used.</p>
<h2>Example</h2>
<p>You start the month with $8,000 of inventory, buy $12,500 and end with $7,200. You used $13,300. With $43,000 in food sales, the food cost is 13,300 ÷ 43,000 = <strong>30.9%</strong>.</p>
<h2>How to lower your food cost</h2>
<ol><li>Count inventory on the same day and time every period.</li>
<li>Standardize recipes and portion sizes, and train the line on them.</li>
<li>Track waste: spoiled food, mistakes and staff meals.</li>
<li>Compare supplier prices every quarter.</li>
<li>Re-price dishes whose plate cost went up (use the menu price calculator).</li></ol>""",
  faq=[("How often should I calculate food cost?","Weekly is best for catching problems early; monthly is the minimum."),
       ("Should beverages be included?","Track beverage and alcohol cost separately; they have very different targets (often 18%–24% for alcohol)."),
       ("What is prime cost?","Food and beverage cost plus total labor cost. A common target is 60% of sales or less.")]),
 es=dict(slug="calculadora-costo-de-comida", title="Calculadora del porcentaje de costo de comida para restaurantes",
  h1="Porcentaje de costo de comida", desc="Calcula el porcentaje de costo de comida de tu restaurante con inventario, compras y ventas. Mira el costo de lo vendido y si es sano.",
  intro="Mide el costo real de comida de una semana o un mes con la fórmula de inventario que usa la industria.",
  body="""<h2>La fórmula</h2>
<p><strong>% de costo = (inventario inicial + compras − inventario final) ÷ ventas de comida × 100</strong>. Lo que está entre paréntesis es el costo de lo vendido: lo que realmente usaste.</p>
<h2>Ejemplo</h2>
<p>Empiezas el mes con $8.000 de inventario, compras $12.500 y terminas con $7.200. Usaste $13.300. Con $43.000 de ventas de comida, el costo es 13.300 ÷ 43.000 = <strong>30,9%</strong>.</p>
<h2>Cómo bajar el costo de comida</h2>
<ol><li>Cuenta el inventario siempre el mismo día y a la misma hora.</li>
<li>Estandariza recetas y porciones, y capacita a la cocina.</li>
<li>Registra el desperdicio: lo que se vence, los errores y la comida del personal.</li>
<li>Compara precios de proveedores cada tres meses.</li>
<li>Actualiza el precio de los platos cuyo costo subió (usa la calculadora de precio de menú).</li></ol>""",
  faq=[("¿Cada cuánto conviene calcularlo?","Semanal es lo ideal para detectar problemas a tiempo; mensual es lo mínimo."),
       ("¿Incluyo las bebidas?","Lleva el costo de bebidas y alcohol por separado; tienen objetivos muy distintos (el alcohol suele ir entre 18% y 24%)."),
       ("¿Qué es el prime cost?","Costo de comida y bebida más el costo total de personal. Un objetivo común es 60% de las ventas o menos.")])),

# ---------------------------------------------------------------- RECIPE SCALER
dict(id="scaler", cat="kitchen", aff="kitchen",
 inputs=[N("from","Original servings","Porciones de la receta",4,"1","","1"),
         N("to","Servings you want","Porciones que quieres",10,"1","","1"),
         TA("list","Ingredients (one per line, amount first)","Ingredientes (uno por línea, cantidad primero)",
            "2 cups flour\n1 1/2 tsp baking powder\n3/4 cup milk\n2 eggs\n1/2 cup sugar",
            "2 tazas de harina\n1 1/2 cdta de polvo de hornear\n3/4 taza de leche\n2 huevos\n1/2 taza de azúcar")],
 outputs=[O("factor","Multiply everything by","Multiplica todo por",True),O("list","Scaled ingredients","Ingredientes ajustados",pre=True)],
 copy="list",
 related=["cooking","oven","menuprice"],
 en=dict(slug="recipe-scaler", title="Recipe Scaler: Double, Halve or Resize Any Recipe",
  h1="Recipe Scaler", desc="Resize any recipe to the servings you need. Paste the ingredient list and get every amount scaled, with kitchen-friendly fractions.",
  intro="Paste your ingredient list, set the servings and get every amount converted, with fractions you can actually measure.",
  body="""<h2>How to scale a recipe</h2>
<p>Divide the servings you want by the servings in the recipe. That number is the scaling factor. Going from 4 to 10 servings is a factor of 2.5, so 2 cups of flour become 5 cups and 3/4 cup of milk becomes 1 7/8 cups.</p>
<h2>Tips for good results</h2>
<ul><li><strong>Baking</strong>: weigh flour and sugar when you scale more than 2×; cups get less accurate.</li>
<li><strong>Eggs</strong>: round to the nearest whole egg, or beat one and use part of it.</li>
<li><strong>Salt and spices</strong>: start with a little less than the scaled amount and adjust to taste.</li>
<li><strong>Pans and time</strong>: a bigger batch may need a bigger pan or two pans, and the baking time changes.</li></ul>
<h2>Supported formats</h2>
<p>Whole numbers (2), decimals (1.5), fractions (3/4), mixed numbers (1 1/2) and symbols (½). Lines without a number at the start stay as they are.</p>""",
  faq=[("How do I halve a recipe?","Set the servings you want to half the original (for example 4 → 2). The factor will be 0.5."),
       ("Can I convert cups to grams too?","Yes, use the cooking measurement converter for each ingredient."),
       ("Does baking time change when I double a recipe?","Usually yes. Check for doneness earlier and later than the recipe says, or bake in two pans.")]),
 es=dict(slug="ajustar-porciones-receta", title="Ajustar porciones de una receta: duplicar o reducir",
  h1="Ajustar porciones de una receta", desc="Ajusta cualquier receta a las porciones que necesitas. Pega la lista de ingredientes y obtén todas las cantidades con fracciones fáciles.",
  intro="Pega tu lista de ingredientes, elige las porciones y obtén todas las cantidades convertidas, con fracciones que se pueden medir.",
  body="""<h2>Cómo ajustar una receta</h2>
<p>Divide las porciones que quieres por las porciones de la receta. Ese número es el factor. Pasar de 4 a 10 porciones es un factor de 2,5: 2 tazas de harina pasan a ser 5 y 3/4 taza de leche pasa a 1 7/8 tazas.</p>
<h2>Consejos para que salga bien</h2>
<ul><li><strong>Pastelería</strong>: pesa la harina y el azúcar cuando multiplicas más de 2 veces; las tazas pierden precisión.</li>
<li><strong>Huevos</strong>: redondea al huevo entero más cercano, o bate uno y usa una parte.</li>
<li><strong>Sal y especias</strong>: pon un poco menos de lo calculado y ajusta a gusto.</li>
<li><strong>Moldes y tiempo</strong>: una tanda más grande puede necesitar un molde más grande o dos, y cambia el tiempo de horno.</li></ul>
<h2>Formatos que entiende</h2>
<p>Enteros (2), decimales (1,5), fracciones (3/4), mixtos (1 1/2) y símbolos (½). Las líneas que no empiezan con un número quedan igual.</p>""",
  faq=[("¿Cómo hago media receta?","Pon como porciones deseadas la mitad de las originales (por ejemplo 4 → 2). El factor va a ser 0,5."),
       ("¿Puedo pasar tazas a gramos?","Sí, usa el conversor de medidas de cocina para cada ingrediente."),
       ("¿Cambia el tiempo de horno si duplico?","En general sí. Revisa antes y después del tiempo de la receta, o haz dos moldes.")])),

# ---------------------------------------------------------------- COOKING CONVERTER
dict(id="cooking", cat="kitchen", aff="kitchen",
 inputs=[N("amount","Amount","Cantidad",1,"any"),
         S("from","From","De",[("cup","cups","tazas"),("tbsp","tablespoons","cucharadas"),("tsp","teaspoons","cucharaditas"),("floz","fluid ounces","onzas líquidas"),("ml","milliliters","mililitros"),("l","liters","litros"),("pint","pints","pintas"),("quart","quarts","cuartos de galón"),("gallon","gallons","galones"),("g","grams","gramos"),("kg","kilograms","kilos"),("oz","ounces (weight)","onzas (peso)"),("lb","pounds","libras")],"cup"),
         S("to","To","A",[("g","grams","gramos"),("ml","milliliters","mililitros"),("cup","cups","tazas"),("tbsp","tablespoons","cucharadas"),("tsp","teaspoons","cucharaditas"),("floz","fluid ounces","onzas líquidas"),("l","liters","litros"),("kg","kilograms","kilos"),("oz","ounces (weight)","onzas (peso)"),("lb","pounds","libras")],"g"),
         S("ingredient","Ingredient (for cups ↔ grams)","Ingrediente (para tazas ↔ gramos)",[("flour","All-purpose flour","Harina común"),("sugar","Granulated sugar","Azúcar"),("brownsugar","Brown sugar (packed)","Azúcar negra (apretada)"),("powdered","Powdered sugar","Azúcar glas"),("butter","Butter","Mantequilla"),("water","Water","Agua"),("milk","Milk","Leche"),("oil","Vegetable oil","Aceite"),("honey","Honey","Miel"),("rice","Rice (uncooked)","Arroz (crudo)"),("oats","Rolled oats","Avena"),("cocoa","Cocoa powder","Cacao en polvo"),("salt","Table salt","Sal fina")],"flour")],
 outputs=[O("result","Result","Resultado",True),O("note","Note","Nota")],
 related=["scaler","oven","menuprice"],
 en=dict(slug="cooking-measurement-converter", title="Cooking Converter: Cups to Grams, Tbsp, Ml and Ounces",
  h1="Cooking Measurement Converter", desc="Convert cups to grams, tablespoons, teaspoons, ml, ounces and pounds for flour, sugar, butter and more. Accurate kitchen conversions.",
  intro="Convert between US cups, spoons, ml, grams, ounces and pounds, with real densities for common ingredients.",
  body="""<h2>Why cups to grams depends on the ingredient</h2>
<p>A cup measures volume, a gram measures weight. A cup of flour weighs about 125 g, while a cup of sugar weighs about 200 g and a cup of honey about 340 g. That is why you need to choose the ingredient when converting between volume and weight.</p>
<h2>Handy equivalents (US)</h2>
<table><tr><th>Measure</th><th>Equals</th></tr>
<tr><td>1 cup</td><td>16 tbsp = 48 tsp = 8 fl oz ≈ 237 ml</td></tr>
<tr><td>1 tablespoon</td><td>3 teaspoons ≈ 14.8 ml</td></tr>
<tr><td>1 stick of butter</td><td>1/2 cup = 113 g</td></tr>
<tr><td>1 pound</td><td>16 oz = 453.6 g</td></tr></table>
<h2>Tips</h2>
<p>Spoon flour into the cup and level it; scooping straight from the bag packs it and can add 20% more. For baking, a cheap kitchen scale is the single best upgrade for consistent results.</p>""",
  faq=[("How many grams is 1 cup of flour?","About 120–125 g for all-purpose flour spooned and leveled."),
       ("How many tablespoons are in a cup?","16 tablespoons, or 48 teaspoons."),
       ("Is a US cup the same as a metric cup?","No. A US cup is about 237 ml; a metric cup (Australia, Canada recipes) is 250 ml.")]),
 es=dict(slug="conversor-medidas-de-cocina", title="Conversor de medidas de cocina: tazas a gramos, cucharadas y ml",
  h1="Conversor de medidas de cocina", desc="Pasa tazas a gramos, cucharadas, cucharaditas, ml, onzas y libras para harina, azúcar, mantequilla y más. Conversiones de cocina precisas.",
  intro="Convierte entre tazas, cucharadas, ml, gramos, onzas y libras, con la densidad real de los ingredientes más usados.",
  body="""<h2>Por qué tazas a gramos depende del ingrediente</h2>
<p>La taza mide volumen y el gramo mide peso. Una taza de harina pesa unos 125 g, una de azúcar unos 200 g y una de miel unos 340 g. Por eso hay que elegir el ingrediente al pasar de volumen a peso.</p>
<h2>Equivalencias útiles (medidas de EE. UU.)</h2>
<table><tr><th>Medida</th><th>Equivale a</th></tr>
<tr><td>1 taza</td><td>16 cucharadas = 48 cucharaditas = 8 oz líquidas ≈ 237 ml</td></tr>
<tr><td>1 cucharada</td><td>3 cucharaditas ≈ 14,8 ml</td></tr>
<tr><td>1 barra de mantequilla (stick)</td><td>1/2 taza = 113 g</td></tr>
<tr><td>1 libra</td><td>16 oz = 453,6 g</td></tr></table>
<h2>Consejos</h2>
<p>Pon la harina en la taza con una cuchara y enrasa; si la sacas directo de la bolsa se compacta y puede tener 20% más. Para pastelería, una balanza de cocina barata es lo que más mejora los resultados.</p>""",
  faq=[("¿Cuántos gramos tiene una taza de harina?","Entre 120 y 125 g de harina común, puesta con cuchara y enrasada."),
       ("¿Cuántas cucharadas tiene una taza?","16 cucharadas, o 48 cucharaditas."),
       ("¿La taza de EE. UU. es igual a la taza métrica?","No. La de EE. UU. tiene unos 237 ml; la métrica tiene 250 ml.")])),

# ---------------------------------------------------------------- OVEN
dict(id="oven", cat="kitchen", aff="kitchen",
 inputs=[N("temp","Temperature","Temperatura",350,"1","","-100"),
         S("dir","Convert","Convertir",[("f2c","°F → °C","°F → °C"),("c2f","°C → °F","°C → °F")],"f2c")],
 presets=("temp",[325,350,375,400,425]),
 outputs=[O("c","Celsius","Celsius",True),O("f","Fahrenheit","Fahrenheit"),O("fan","Fan / convection oven (°C)","Horno con ventilador (°C)"),O("gas","Gas mark","Gas mark (marca de gas)")],
 related=["cooking","scaler","percent"],
 en=dict(slug="oven-temperature-converter", title="Oven Temperature Converter: Fahrenheit to Celsius",
  h1="Oven Temperature Converter", desc="Convert oven temperatures between Fahrenheit and Celsius, with fan oven and gas mark equivalents. 350°F, 375°F, 400°F and more.",
  intro="Convert oven temperatures from °F to °C and back, with the fan-oven and gas-mark equivalents.",
  body="""<h2>The formula</h2>
<p><strong>°C = (°F − 32) × 5 ÷ 9</strong> and <strong>°F = °C × 9 ÷ 5 + 32</strong>. So 350 °F is 177 °C, which most recipes round to 175 or 180 °C.</p>
<h2>Common oven temperatures</h2>
<table><tr><th>°F</th><th>°C</th><th>Fan °C</th><th>Use</th></tr>
<tr><td>325</td><td>163</td><td>145</td><td>Slow baking, cheesecake</td></tr>
<tr><td>350</td><td>177</td><td>160</td><td>Cakes, cookies</td></tr>
<tr><td>375</td><td>191</td><td>170</td><td>Muffins, pies</td></tr>
<tr><td>400</td><td>204</td><td>185</td><td>Roasting vegetables</td></tr>
<tr><td>425</td><td>218</td><td>200</td><td>Pizza, crispy potatoes</td></tr></table>
<h2>Fan (convection) ovens</h2>
<p>A fan oven cooks faster, so lower the temperature by about 20 °C (25 °F) or check for doneness earlier.</p>""",
  faq=[("What is 350°F in Celsius?","About 177 °C. Most recipes use 180 °C, or 160 °C in a fan oven."),
       ("What is 200°C in Fahrenheit?","392 °F, usually rounded to 400 °F."),
       ("Do I lower the temperature for a convection oven?","Yes, by about 25 °F (20 °C), or keep the temperature and shorten the time.")]),
 es=dict(slug="conversor-temperatura-horno", title="Conversor de temperatura del horno: Fahrenheit a Celsius",
  h1="Temperatura del horno: °F a °C", desc="Pasa temperaturas de horno de Fahrenheit a Celsius y al revés, con equivalencias para horno con ventilador y gas mark.",
  intro="Convierte la temperatura del horno de °F a °C y al revés, con la equivalencia para horno con ventilador.",
  body="""<h2>La fórmula</h2>
<p><strong>°C = (°F − 32) × 5 ÷ 9</strong> y <strong>°F = °C × 9 ÷ 5 + 32</strong>. O sea que 350 °F son 177 °C, que la mayoría de las recetas redondea a 175 o 180 °C.</p>
<h2>Temperaturas de horno más comunes</h2>
<table><tr><th>°F</th><th>°C</th><th>Ventilador °C</th><th>Para</th></tr>
<tr><td>325</td><td>163</td><td>145</td><td>Horno suave, cheesecake</td></tr>
<tr><td>350</td><td>177</td><td>160</td><td>Pasteles, galletas</td></tr>
<tr><td>375</td><td>191</td><td>170</td><td>Muffins, tartas</td></tr>
<tr><td>400</td><td>204</td><td>185</td><td>Verduras asadas</td></tr>
<tr><td>425</td><td>218</td><td>200</td><td>Pizza, papas crocantes</td></tr></table>
<h2>Horno con ventilador (convección)</h2>
<p>Cocina más rápido: baja unos 20 °C o revisa antes de tiempo.</p>""",
  faq=[("¿Cuánto es 350 °F en Celsius?","Unos 177 °C. La mayoría de las recetas usa 180 °C, o 160 °C con ventilador."),
       ("¿Cuánto es 180 °C en Fahrenheit?","356 °F, que se redondea a 350 °F."),
       ("¿Bajo la temperatura si el horno tiene ventilador?","Sí, unos 20 °C, o deja la temperatura y acorta el tiempo.")])),

# ---------------------------------------------------------------- HOURLY TO SALARY
dict(id="hourly", cat="work", aff="work",
 inputs=[N("wage","Hourly wage","Pago por hora",18,"0.01","$"),
         N("hours","Hours per week","Horas por semana",40,"0.5"),
         N("weeks","Weeks worked per year","Semanas trabajadas por año",52,"1")],
 outputs=[O("yearly","Yearly salary","Sueldo anual",True),O("monthly","Monthly","Mensual"),O("biweekly","Every two weeks","Cada dos semanas"),O("weekly","Weekly","Semanal")],
 related=["salary","overtime","budget"],
 en=dict(slug="hourly-to-salary-calculator", title="Hourly to Salary Calculator: What Is My Hourly Wage per Year?",
  h1="Hourly to Salary Calculator", desc="Convert an hourly wage to yearly, monthly, biweekly and weekly pay. See what $15, $20 or $25 an hour is per year before taxes.",
  intro="See what your hourly wage adds up to per week, every two weeks, per month and per year (before taxes).",
  body="""<h2>The formula</h2>
<p><strong>Yearly pay = hourly wage × hours per week × weeks per year</strong>. Full time is usually 40 hours × 52 weeks = 2,080 hours. At $18 an hour that is <strong>$37,440 a year</strong>, $3,120 a month and $1,440 every two weeks.</p>
<h2>Quick reference (40 h/week, 52 weeks)</h2>
<table><tr><th>Hourly</th><th>Yearly</th><th>Monthly</th></tr>
<tr><td>$15</td><td>$31,200</td><td>$2,600</td></tr>
<tr><td>$20</td><td>$41,600</td><td>$3,467</td></tr>
<tr><td>$25</td><td>$52,000</td><td>$4,333</td></tr>
<tr><td>$30</td><td>$62,400</td><td>$5,200</td></tr></table>
<h2>Unpaid time off</h2>
<p>If you do not get paid vacation, lower the weeks per year. Two unpaid weeks means 50 weeks. Tipped workers can add their average tips per hour to the wage to see their real income.</p>""",
  faq=[("How much is $20 an hour per year?","$41,600 before taxes at 40 hours a week for 52 weeks."),
       ("Is this before or after taxes?","Before taxes (gross pay). Take-home pay depends on federal, state and payroll taxes."),
       ("How many work hours are in a year?","2,080 for a 40-hour week with 52 weeks.")]),
 es=dict(slug="sueldo-por-hora-a-anual", title="Calculadora de sueldo por hora a anual y mensual",
  h1="Sueldo por hora a anual", desc="Pasa tu pago por hora a sueldo anual, mensual, quincenal y semanal. Mira cuánto son $15, $20 o $25 la hora por año, antes de impuestos.",
  intro="Mira cuánto suma tu pago por hora por semana, cada dos semanas, por mes y por año (antes de impuestos).",
  body="""<h2>La fórmula</h2>
<p><strong>Sueldo anual = pago por hora × horas por semana × semanas por año</strong>. Tiempo completo suele ser 40 horas × 52 semanas = 2.080 horas. A $18 la hora son <strong>$37.440 al año</strong>, $3.120 por mes y $1.440 cada dos semanas.</p>
<h2>Tabla rápida (40 h por semana, 52 semanas)</h2>
<table><tr><th>Por hora</th><th>Por año</th><th>Por mes</th></tr>
<tr><td>$15</td><td>$31.200</td><td>$2.600</td></tr>
<tr><td>$20</td><td>$41.600</td><td>$3.467</td></tr>
<tr><td>$25</td><td>$52.000</td><td>$4.333</td></tr>
<tr><td>$30</td><td>$62.400</td><td>$5.200</td></tr></table>
<h2>Vacaciones sin goce de sueldo</h2>
<p>Si no tienes vacaciones pagas, baja las semanas por año: dos semanas sin pago son 50 semanas. Si cobras propinas, suma tu promedio de propinas por hora al pago para ver tu ingreso real.</p>""",
  faq=[("¿Cuánto son $20 la hora por año?","$41.600 antes de impuestos, con 40 horas por semana durante 52 semanas."),
       ("¿Es antes o después de impuestos?","Antes (bruto). Lo que cobras en mano depende de los impuestos federales, estatales y de nómina."),
       ("¿Cuántas horas de trabajo tiene un año?","2.080 con 40 horas por semana y 52 semanas.")])),

# ---------------------------------------------------------------- SALARY TO HOURLY
dict(id="salary", cat="work", aff="work",
 inputs=[N("salary","Yearly salary","Sueldo anual",50000,"100","$"),
         N("hours","Hours per week","Horas por semana",40,"0.5"),
         N("weeks","Weeks worked per year","Semanas trabajadas por año",52,"1")],
 outputs=[O("hourly","Hourly rate","Pago por hora",True),O("daily","Per day (5-day week)","Por día (5 días)"),O("weekly","Weekly","Semanal"),O("monthly","Monthly","Mensual")],
 related=["hourly","overtime","rule503020"],
 en=dict(slug="salary-to-hourly-calculator", title="Salary to Hourly Calculator: Convert Annual Pay to Hourly",
  h1="Salary to Hourly Calculator", desc="Convert an annual salary to an hourly rate, plus daily, weekly and monthly pay. Compare a salaried job offer with an hourly one.",
  intro="Turn a yearly salary into an hourly rate so you can compare job offers fairly.",
  body="""<h2>The formula</h2>
<p><strong>Hourly rate = yearly salary ÷ (hours per week × weeks per year)</strong>. A $50,000 salary at 40 hours a week is $50,000 ÷ 2,080 = <strong>$24.04 per hour</strong>.</p>
<h2>Compare offers with real hours</h2>
<p>Salaried jobs often mean more than 40 hours. If a $55,000 job really takes 50 hours a week, it pays $21.15 an hour, less than a $23 hourly job at 40 hours with overtime pay. Put the real hours in the calculator to see it.</p>
<h2>Do not forget benefits</h2>
<p>Health insurance, retirement match and paid time off can be worth thousands of dollars a year. Add their value to the salary when comparing.</p>""",
  faq=[("How much is $50,000 a year per hour?","About $24.04 an hour at 40 hours a week for 52 weeks."),
       ("How much is $60,000 a year per hour?","About $28.85 an hour full time."),
       ("Do salaried employees get overtime?","Only non-exempt employees. Many salaried roles are exempt and do not earn overtime.")]),
 es=dict(slug="sueldo-anual-a-por-hora", title="Calculadora de sueldo anual a pago por hora",
  h1="Sueldo anual a pago por hora", desc="Convierte un sueldo anual a pago por hora, por día, por semana y por mes. Compara una oferta con sueldo fijo contra una por hora.",
  intro="Pasa un sueldo anual a pago por hora para comparar ofertas de trabajo de igual a igual.",
  body="""<h2>La fórmula</h2>
<p><strong>Pago por hora = sueldo anual ÷ (horas por semana × semanas por año)</strong>. Un sueldo de $50.000 con 40 horas semanales da $50.000 ÷ 2.080 = <strong>$24,04 la hora</strong>.</p>
<h2>Compara ofertas con las horas reales</h2>
<p>Los trabajos con sueldo fijo muchas veces piden más de 40 horas. Si un trabajo de $55.000 en realidad lleva 50 horas por semana, paga $21,15 la hora: menos que uno de $23 la hora con 40 horas y horas extra pagas. Pon las horas reales para verlo.</p>
<h2>No te olvides de los beneficios</h2>
<p>El seguro médico, el aporte para la jubilación y las vacaciones pagas pueden valer miles de dólares por año. Súmalos al comparar.</p>""",
  faq=[("¿Cuánto son $50.000 al año por hora?","Unos $24,04 la hora con 40 horas semanales durante 52 semanas."),
       ("¿Cuánto son $60.000 al año por hora?","Unos $28,85 la hora a tiempo completo."),
       ("¿Los empleados con sueldo fijo cobran horas extra?","Solo los 'no exentos'. Muchos puestos con sueldo fijo son exentos y no cobran horas extra.")])),

# ---------------------------------------------------------------- OVERTIME
dict(id="overtime", cat="work", aff="work",
 inputs=[N("rate","Regular hourly rate","Pago por hora normal",18,"0.01","$"),
         N("reg","Regular hours","Horas normales",40,"0.25"),
         N("ot","Overtime hours","Horas extra",6,"0.25"),
         S("mult","Overtime rate","Recargo de horas extra",[("1.5","Time and a half (1.5×)","Tiempo y medio (1,5×)"),("2","Double time (2×)","Doble (2×)")],"1.5")],
 outputs=[O("total","Total pay","Pago total",True),O("otRate","Overtime hourly rate","Pago por hora extra"),O("regPay","Regular pay","Pago normal"),O("otPay","Overtime pay","Pago de horas extra")],
 related=["hourly","salary","tipout"],
 en=dict(slug="overtime-pay-calculator", title="Overtime Pay Calculator: Time and a Half and Double Time",
  h1="Overtime Pay Calculator", desc="Calculate overtime pay at time and a half or double time. Enter your hourly rate and hours to see regular, overtime and total pay.",
  intro="Check your paycheck: regular pay, overtime at time and a half or double time, and the total.",
  body="""<h2>How overtime is calculated</h2>
<p>Under the federal Fair Labor Standards Act, non-exempt employees earn at least <strong>1.5 times their regular rate</strong> for every hour over 40 in a workweek. At $18 an hour, overtime is $27 an hour. With 40 regular hours and 6 overtime hours the week pays $720 + $162 = <strong>$882</strong>.</p>
<h2>Daily overtime and double time</h2>
<p>A few states, like California, also require overtime after 8 hours in a day and double time after 12 hours. Most states, including Utah and Texas, follow only the federal 40-hour weekly rule.</p>
<h2>Tipped employees</h2>
<p>For tipped workers, overtime is based on the full minimum wage, not the reduced tipped wage. Check your pay stub if the overtime rate looks low.</p>""",
  faq=[("What is time and a half for $20 an hour?","$30 an hour."),
       ("Is overtime calculated per day or per week?","Federal law uses the workweek (over 40 hours). Some states add daily overtime."),
       ("Do part-time workers get overtime?","Yes, if they work more than 40 hours in a week and are non-exempt.")]),
 es=dict(slug="calculadora-horas-extra", title="Calculadora de horas extra: tiempo y medio y doble",
  h1="Calculadora de horas extra", desc="Calcula el pago de horas extra a tiempo y medio o doble. Pon tu pago por hora y tus horas para ver el pago normal, el extra y el total.",
  intro="Controla tu cheque: pago normal, horas extra a tiempo y medio o doble, y el total.",
  body="""<h2>Cómo se calculan las horas extra</h2>
<p>Según la ley federal (FLSA), los empleados no exentos cobran al menos <strong>1,5 veces su pago normal</strong> por cada hora arriba de 40 en la semana. A $18 la hora, la hora extra vale $27. Con 40 horas normales y 6 extra, la semana paga $720 + $162 = <strong>$882</strong>.</p>
<h2>Horas extra por día y doble</h2>
<p>Algunos estados, como California, también pagan extra después de 8 horas en un día y doble después de 12. La mayoría, incluidos Utah y Texas, solo aplica la regla federal de 40 horas semanales.</p>
<h2>Empleados con propina</h2>
<p>Para quienes cobran propina, la hora extra se calcula sobre el salario mínimo completo, no sobre el reducido. Revisa tu recibo si el pago te parece bajo.</p>""",
  faq=[("¿Cuánto es tiempo y medio de $20 la hora?","$30 la hora."),
       ("¿Las horas extra se cuentan por día o por semana?","La ley federal usa la semana (más de 40 horas). Algunos estados suman horas extra por día."),
       ("¿Los de medio tiempo cobran horas extra?","Sí, si trabajan más de 40 horas en una semana y no son exentos.")])),

# ---------------------------------------------------------------- 50/30/20
dict(id="rule503020", cat="money", aff="money",
 inputs=[N("income","Monthly take-home pay","Ingreso mensual neto",4000,"10","$")],
 outputs=[O("needs","Needs (50%)","Necesidades (50%)",True),O("wants","Wants (30%)","Gustos (30%)"),O("savings","Savings and debt (20%)","Ahorro y deudas (20%)"),O("yearly","Saved in a year","Ahorro en un año")],
 related=["budget","savings","hourly"],
 en=dict(slug="50-30-20-budget-calculator", title="50/30/20 Budget Calculator: Split Your Income",
  h1="50/30/20 Budget Calculator", desc="Split your take-home pay with the 50/30/20 rule: 50% needs, 30% wants, 20% savings. See your monthly amounts instantly.",
  intro="The simplest budget there is: half for needs, 30% for wants and 20% for your future.",
  body="""<h2>What is the 50/30/20 rule?</h2>
<ul><li><strong>50% needs</strong>: rent or mortgage, utilities, groceries, insurance, transportation, minimum debt payments.</li>
<li><strong>30% wants</strong>: eating out, streaming, travel, hobbies, shopping.</li>
<li><strong>20% savings</strong>: emergency fund, retirement, extra debt payments.</li></ul>
<p>With $4,000 a month of take-home pay, that is $2,000 for needs, $1,200 for wants and <strong>$800 for savings</strong>, or $9,600 a year.</p>
<h2>When it does not fit</h2>
<p>In expensive cities, needs can take 60% or more. That is fine: start with what you can save, even 5%, and raise it each time your income goes up. If you want a detailed plan by category, use the family budget calculator.</p>""",
  faq=[("Is the 50/30/20 rule based on gross or net income?","Net income: what lands in your bank account after taxes."),
       ("Where do debt payments go?","Minimum payments are needs; anything extra you pay goes to the 20%."),
       ("What if I have irregular income?","Use your lowest typical month as the income to stay safe.")]),
 es=dict(slug="presupuesto-50-30-20", title="Calculadora de presupuesto 50/30/20",
  h1="Presupuesto 50/30/20", desc="Divide tu ingreso con la regla 50/30/20: 50% necesidades, 30% gustos y 20% ahorro. Mira tus montos mensuales al instante.",
  intro="El presupuesto más simple que existe: la mitad para lo necesario, 30% para gustos y 20% para tu futuro.",
  body="""<h2>¿Qué es la regla 50/30/20?</h2>
<ul><li><strong>50% necesidades</strong>: alquiler o hipoteca, servicios, supermercado, seguros, transporte, pagos mínimos de deudas.</li>
<li><strong>30% gustos</strong>: salidas a comer, streaming, viajes, hobbies, compras.</li>
<li><strong>20% ahorro</strong>: fondo de emergencia, jubilación, pagos extra de deudas.</li></ul>
<p>Con $4.000 netos por mes son $2.000 para necesidades, $1.200 para gustos y <strong>$800 de ahorro</strong>, o $9.600 por año.</p>
<h2>Cuando no alcanza</h2>
<p>En ciudades caras las necesidades pueden llevarse 60% o más. No pasa nada: empieza con lo que puedas ahorrar, aunque sea 5%, y súbelo cada vez que aumente tu ingreso. Si quieres un plan detallado por categoría, usa la calculadora de presupuesto familiar.</p>""",
  faq=[("¿Se usa el ingreso bruto o el neto?","El neto: lo que te llega a la cuenta después de impuestos."),
       ("¿Dónde van los pagos de deudas?","El pago mínimo es necesidad; lo que pagues de más va al 20%."),
       ("¿Y si mi ingreso varía?","Usa tu mes más bajo habitual como ingreso, para ir a lo seguro.")])),

# ---------------------------------------------------------------- FAMILY BUDGET
dict(id="budget", cat="money", aff="money",
 inputs=[N("income","Monthly take-home income","Ingreso mensual neto",5200,"10","$"),
         N("housing","Rent or mortgage","Alquiler o hipoteca",1600,"10","$"),
         N("utilities","Utilities, phone, internet","Servicios, teléfono, internet",320,"10","$"),
         N("groceries","Groceries","Supermercado",750,"10","$"),
         N("transport","Car, gas, transit","Auto, gasolina, transporte",450,"10","$"),
         N("insurance","Insurance and health","Seguros y salud",380,"10","$"),
         N("debt","Debt payments","Pagos de deudas",250,"10","$"),
         N("childcare","Childcare and school","Cuidado de niños y escuela",400,"10","$"),
         N("other","Everything else","Todo lo demás",500,"10","$")],
 outputs=[O("left","Left over each month","Te queda por mes",True),O("spent","Total expenses","Gastos totales"),O("spentPct","Share of income spent","Porcentaje del ingreso gastado"),O("housingPct","Housing share","Porcentaje en vivienda")],
 related=["rule503020","savings","loan"],
 en=dict(slug="family-budget-calculator", title="Family Budget Calculator: Monthly Household Budget",
  h1="Family Budget Calculator", desc="Plan your monthly household budget. Enter income and expenses by category and see what is left, how much you spend and your housing share.",
  intro="Put your income and your monthly expenses side by side and see exactly what is left.",
  body="""<h2>How to make a family budget in 4 steps</h2>
<ol><li><strong>Income</strong>: add every take-home paycheck in the house for a month.</li>
<li><strong>Fixed expenses</strong>: rent, insurance, car payment, phone. Look at last month's bank statement.</li>
<li><strong>Variable expenses</strong>: groceries, gas, eating out. Average the last three months.</li>
<li><strong>Compare</strong>: if the leftover is negative, cut wants first; if it is positive, give it a job (emergency fund, debt, savings goal).</li></ol>
<h2>Healthy guidelines</h2>
<ul><li>Housing at or under <strong>30%</strong> of take-home income.</li>
<li>Emergency fund of <strong>3 to 6 months</strong> of expenses.</li>
<li>Total debt payments (excluding mortgage) under <strong>15%</strong>.</li></ul>
<h2>Do not forget irregular costs</h2>
<p>Car registration, birthdays, holidays and back-to-school show up every year. Divide their yearly total by 12 and add it to "Everything else".</p>""",
  faq=[("How much should a family spend on groceries?","It depends on size and location; a family of four in the US often spends $900–$1,300 a month on a moderate plan."),
       ("What percentage of income should go to rent?","A common guideline is 30% of take-home pay or less."),
       ("Is my data saved?","No. The numbers stay in your browser and disappear when you close the page.")]),
 es=dict(slug="presupuesto-familiar", title="Calculadora de presupuesto familiar mensual",
  h1="Presupuesto familiar", desc="Arma el presupuesto mensual de tu casa. Pon ingresos y gastos por categoría y mira cuánto te queda, cuánto gastas y cuánto va a vivienda.",
  intro="Pon tus ingresos y tus gastos del mes uno al lado del otro y mira exactamente cuánto te queda.",
  body="""<h2>Cómo armar un presupuesto familiar en 4 pasos</h2>
<ol><li><strong>Ingresos</strong>: suma todos los sueldos netos de la casa en un mes.</li>
<li><strong>Gastos fijos</strong>: alquiler, seguros, cuota del auto, teléfono. Mira el resumen del banco del mes pasado.</li>
<li><strong>Gastos variables</strong>: supermercado, gasolina, salidas. Promedia los últimos tres meses.</li>
<li><strong>Compara</strong>: si lo que queda es negativo, recorta primero los gustos; si es positivo, dale un destino (fondo de emergencia, deudas, una meta de ahorro).</li></ol>
<h2>Referencias sanas</h2>
<ul><li>Vivienda en <strong>30%</strong> o menos del ingreso neto.</li>
<li>Fondo de emergencia de <strong>3 a 6 meses</strong> de gastos.</li>
<li>Pagos de deudas (sin hipoteca) por debajo del <strong>15%</strong>.</li></ul>
<h2>No te olvides de los gastos irregulares</h2>
<p>La registro del auto, cumpleaños, fiestas y la vuelta a clases aparecen todos los años. Divide el total anual por 12 y súmalo a "Todo lo demás".</p>""",
  faq=[("¿Cuánto gasta una familia en supermercado?","Depende del tamaño y la ciudad; una familia de cuatro en EE. UU. suele gastar entre $900 y $1.300 por mes con un plan moderado."),
       ("¿Qué porcentaje del ingreso debería ir al alquiler?","Una referencia común es 30% del ingreso neto o menos."),
       ("¿Se guardan mis datos?","No. Los números quedan en tu navegador y se borran al cerrar la página.")])),

# ---------------------------------------------------------------- SAVINGS GOAL
dict(id="savings", cat="money", aff="money",
 inputs=[N("goal","Savings goal","Meta de ahorro",10000,"10","$"),
         N("current","Saved so far","Ahorrado hasta ahora",1500,"10","$"),
         N("monthly","Monthly deposit","Depósito mensual",400,"10","$"),
         N("rate","Annual interest (savings account)","Interés anual (cuenta de ahorro)",4,"0.1","%")],
 outputs=[O("months","Months to reach it","Meses para llegar",True),O("date","Goal reached in","Llegas en"),O("contrib","Total you deposit","Total que depositas")],
 related=["budget","rule503020","loan"],
 en=dict(slug="savings-goal-calculator", title="Savings Goal Calculator: How Long to Save for It",
  h1="Savings Goal Calculator", desc="Find out how many months it takes to reach a savings goal with monthly deposits and interest. Plan an emergency fund, a trip or a down payment.",
  intro="Find out when you will reach your goal: an emergency fund, a car, a trip or a down payment.",
  body="""<h2>How it works</h2>
<p>Each month the calculator adds your deposit and the interest earned on the balance, until the balance reaches the goal. With $1,500 saved, $400 a month and 4% interest, a $10,000 goal takes about <strong>21 months</strong>.</p>
<h2>Ways to get there faster</h2>
<ol><li>Automate the deposit on payday so it happens before you spend.</li>
<li>Use a high-yield savings account; online banks often pay several times more than big banks.</li>
<li>Send raises, tax refunds and side income straight to the goal.</li></ol>
<h2>How big should an emergency fund be?</h2>
<p>Three to six months of essential expenses. Use the family budget calculator to know that number.</p>""",
  faq=[("How much should I save each month?","A common target is 20% of take-home pay (see the 50/30/20 calculator), but any automatic amount is a good start."),
       ("Is the interest guaranteed?","No. Savings account rates change. The result is an estimate."),
       ("Does it include taxes on interest?","No. Interest is taxable income in the US, but the effect on the timeline is small.")]),
 es=dict(slug="calculadora-meta-de-ahorro", title="Calculadora de meta de ahorro: cuánto tardo en juntar",
  h1="Meta de ahorro", desc="Calcula cuántos meses tardas en llegar a tu meta de ahorro con depósitos mensuales e interés. Fondo de emergencia, viaje o enganche de casa.",
  intro="Descubre cuándo vas a llegar a tu meta: fondo de emergencia, auto, viaje o enganche de una casa.",
  body="""<h2>Cómo funciona</h2>
<p>Cada mes la calculadora suma tu depósito y el interés que genera el saldo, hasta llegar a la meta. Con $1.500 ahorrados, $400 por mes y 4% de interés, una meta de $10.000 lleva unos <strong>21 meses</strong>.</p>
<h2>Cómo llegar más rápido</h2>
<ol><li>Programa el depósito automático el día que cobras, antes de gastar.</li>
<li>Usa una cuenta de ahorro de alto rendimiento: los bancos online suelen pagar varias veces más que los grandes.</li>
<li>Manda aumentos, devoluciones de impuestos e ingresos extra directo a la meta.</li></ol>
<h2>¿De cuánto tiene que ser el fondo de emergencia?</h2>
<p>De tres a seis meses de gastos esenciales. Usa la calculadora de presupuesto familiar para saber ese número.</p>""",
  faq=[("¿Cuánto debería ahorrar por mes?","Una referencia común es el 20% del ingreso neto (mira la calculadora 50/30/20), pero cualquier monto automático es un buen comienzo."),
       ("¿El interés está garantizado?","No. Las tasas cambian. El resultado es una estimación."),
       ("¿Incluye impuestos sobre el interés?","No. En EE. UU. el interés paga impuesto, pero el efecto en el plazo es chico.")])),

# ---------------------------------------------------------------- LOAN
dict(id="loan", cat="money", aff="money",
 inputs=[N("amount","Loan amount","Monto del préstamo",20000,"100","$"),
         N("apr","Interest rate (APR)","Tasa de interés anual (APR)",7.5,"0.05","%"),
         N("years","Term in years","Plazo en años",5,"0.5")],
 outputs=[O("monthly","Monthly payment","Cuota mensual",True),O("interest","Total interest","Interés total"),O("total","Total paid","Total pagado")],
 related=["savings","budget","percent"],
 en=dict(slug="loan-payment-calculator", title="Loan Payment Calculator: Monthly Payment and Total Interest",
  h1="Loan Payment Calculator", desc="Calculate the monthly payment and total interest for a car loan, personal loan or any fixed-rate loan. Enter amount, APR and years.",
  intro="See the monthly payment and the real cost in interest of a car loan, personal loan or any fixed-rate loan.",
  body="""<h2>The loan payment formula</h2>
<p><strong>Payment = P × r ÷ (1 − (1 + r)<sup>−n</sup>)</strong>, where P is the loan amount, r the monthly rate (APR ÷ 12) and n the number of months. A $20,000 loan at 7.5% for 5 years costs <strong>$400.76 a month</strong> and $4,046 in interest.</p>
<h2>Shorter term or lower payment?</h2>
<p>A longer term lowers the monthly payment but raises the total interest. The same $20,000 at 7.5% over 7 years is $307 a month, but the interest grows to about $5,770. If the budget allows it, the shorter term saves money.</p>
<h2>Before you sign</h2>
<ul><li>Compare the APR, not just the payment.</li><li>Ask about prepayment penalties.</li><li>Check that the payment fits your family budget with room to spare.</li></ul>""",
  faq=[("Does this work for mortgages?","For principal and interest only. A mortgage payment also includes taxes, insurance and sometimes PMI."),
       ("What is APR?","The annual percentage rate: the yearly cost of the loan including some fees."),
       ("Can I pay a loan off early?","Usually yes, and it saves interest. Check your contract for prepayment penalties.")]),
 es=dict(slug="calculadora-cuota-prestamo", title="Calculadora de cuota de préstamo e interés total",
  h1="Cuota de préstamo", desc="Calcula la cuota mensual y el interés total de un préstamo para auto, personal o cualquiera con tasa fija. Pon monto, tasa anual y años.",
  intro="Mira la cuota mensual y el costo real en intereses de un préstamo para auto, personal o cualquiera con tasa fija.",
  body="""<h2>La fórmula de la cuota</h2>
<p><strong>Cuota = P × r ÷ (1 − (1 + r)<sup>−n</sup>)</strong>, donde P es el monto, r la tasa mensual (tasa anual ÷ 12) y n la cantidad de meses. Un préstamo de $20.000 al 7,5% a 5 años da una cuota de <strong>$400,76</strong> y $4.046 de interés.</p>
<h2>¿Menos plazo o cuota más baja?</h2>
<p>Un plazo más largo baja la cuota pero sube el interés total. Los mismos $20.000 al 7,5% a 7 años son $307 por mes, pero el interés sube a unos $5.770. Si el presupuesto te da, el plazo corto te ahorra dinero.</p>
<h2>Antes de firmar</h2>
<ul><li>Compara la tasa anual (APR), no solo la cuota.</li><li>Pregunta si hay penalidad por cancelar antes.</li><li>Fíjate que la cuota entre en tu presupuesto familiar con margen.</li></ul>""",
  faq=[("¿Sirve para hipotecas?","Solo para capital e interés. La cuota de una hipoteca también incluye impuestos, seguro y a veces PMI."),
       ("¿Qué es el APR?","La tasa anual: el costo por año del préstamo, incluyendo algunos cargos."),
       ("¿Puedo cancelar antes?","En general sí, y ahorras intereses. Revisa si el contrato tiene penalidad.")])),

# ---------------------------------------------------------------- PERCENT
dict(id="percent", cat="everyday", aff="money",
 inputs=[S("mode","What do you want to know?","¿Qué quieres saber?",[("of","What is A% of B?","¿Cuánto es A% de B?"),("is","A is what % of B?","¿Qué % de B es A?"),("chg","% change from A to B","Variación % de A a B")],"of"),
         N("a","A","A",15,"any","","-1e12"),N("b","B","B",80,"any","","-1e12")],
 outputs=[O("result","Result","Resultado",True)],
 related=["discount","salestax","tip"],
 en=dict(slug="percentage-calculator", title="Percentage Calculator: % of a Number, % Change",
  h1="Percentage Calculator", desc="Free percentage calculator: find X% of a number, what percent one number is of another, and the percentage increase or decrease.",
  intro="The three percentage questions everyone asks, in one place.",
  body="""<h2>The three formulas</h2>
<ul><li><strong>A% of B</strong> = A ÷ 100 × B. Example: 15% of 80 = 12.</li>
<li><strong>A is what % of B</strong> = A ÷ B × 100. Example: 12 is 15% of 80.</li>
<li><strong>% change from A to B</strong> = (B − A) ÷ A × 100. Example: from 80 to 92 is a 15% increase.</li></ul>
<h2>Percentage points vs. percent</h2>
<p>If an interest rate goes from 4% to 5%, it rose 1 percentage point, but 25 percent. Use the change mode with A = 4 and B = 5 to see it.</p>
<h2>A common mistake</h2>
<p>A 50% drop followed by a 50% rise does not get you back to the start: 100 → 50 → 75. Percent changes always apply to the current value.</p>""",
  faq=[("How do I calculate 20% of a number?","Multiply the number by 0.2. For 80, that is 16."),
       ("How do I find the percentage increase?","Subtract the old value from the new one, divide by the old value and multiply by 100."),
       ("Can A or B be negative?","Yes, for percent of and percent change. Results with a negative starting value can be confusing, so double-check them.")]),
 es=dict(slug="calculadora-de-porcentajes", title="Calculadora de porcentajes: % de un número y variación",
  h1="Calculadora de porcentajes", desc="Calculadora de porcentajes gratis: saca el X% de un número, qué porcentaje es un número de otro y el aumento o la baja en porcentaje.",
  intro="Las tres preguntas de porcentaje que todos hacemos, en un solo lugar.",
  body="""<h2>Las tres fórmulas</h2>
<ul><li><strong>A% de B</strong> = A ÷ 100 × B. Ejemplo: el 15% de 80 es 12.</li>
<li><strong>Qué % de B es A</strong> = A ÷ B × 100. Ejemplo: 12 es el 15% de 80.</li>
<li><strong>Variación % de A a B</strong> = (B − A) ÷ A × 100. Ejemplo: de 80 a 92 es un aumento del 15%.</li></ul>
<h2>Puntos porcentuales y porcentaje</h2>
<p>Si una tasa pasa del 4% al 5%, subió 1 punto porcentual, pero un 25 por ciento. Usa el modo variación con A = 4 y B = 5 para verlo.</p>
<h2>Un error común</h2>
<p>Una baja del 50% seguida de una suba del 50% no te devuelve al principio: 100 → 50 → 75. Los porcentajes siempre se aplican sobre el valor actual.</p>""",
  faq=[("¿Cómo saco el 20% de un número?","Multiplica el número por 0,2. Para 80 da 16."),
       ("¿Cómo calculo el aumento en porcentaje?","Resta el valor viejo al nuevo, divide por el viejo y multiplica por 100."),
       ("¿A o B pueden ser negativos?","Sí. Pero si el valor inicial es negativo, revisa el resultado con cuidado.")])),

# ---------------------------------------------------------------- DISCOUNT
dict(id="discount", cat="everyday", aff="money",
 inputs=[N("price","Original price","Precio original",80,"0.01","$"),
         N("off","Discount","Descuento",25,"1","%"),
         N("tax","Sales tax (optional)","Impuesto (opcional)",0,"0.01","%")],
 presets=("off",[10,20,25,30,50]),
 outputs=[O("total","You pay","Pagas",True),O("save","You save","Ahorras"),O("after","Price after discount","Precio con descuento"),O("tax","Sales tax","Impuesto")],
 related=["salestax","percent","tip"],
 en=dict(slug="discount-calculator", title="Discount Calculator: Sale Price and How Much You Save",
  h1="Discount Calculator", desc="Find the sale price after a discount and how much you save. Works for 10%, 20%, 25%, 30%, 50% off and more, with optional sales tax.",
  intro="Know the real price of a sale before you get to the register, sales tax included.",
  body="""<h2>How to calculate a discount</h2>
<p><strong>Sale price = original price × (1 − discount ÷ 100)</strong>. 25% off $80 is $80 × 0.75 = <strong>$60</strong>, so you save $20.</p>
<h2>Stacked discounts</h2>
<p>"20% off plus an extra 10%" is not 30% off. The second discount applies to the already reduced price: $100 → $80 → $72, which is 28% off. Run the calculator twice to check.</p>
<h2>Add the sales tax</h2>
<p>In the US the tax is added at the register on the discounted price. Enter your local rate to see the final amount.</p>""",
  faq=[("How much is 30% off $50?","$35, you save $15."),
       ("Is the tax calculated before or after the discount?","After. You pay tax on the discounted price in most states."),
       ("How do I find the original price from the sale price?","Divide the sale price by (1 − discount). $60 at 25% off came from $60 ÷ 0.75 = $80.")]),
 es=dict(slug="calculadora-de-descuentos", title="Calculadora de descuentos: precio final y cuánto ahorras",
  h1="Calculadora de descuentos", desc="Calcula el precio con descuento y cuánto ahorras. Sirve para 10%, 20%, 25%, 30%, 50% y más, con impuesto opcional.",
  intro="Conoce el precio real de una oferta antes de llegar a la caja, con impuesto incluido.",
  body="""<h2>Cómo calcular un descuento</h2>
<p><strong>Precio final = precio original × (1 − descuento ÷ 100)</strong>. Un 25% de descuento sobre $80 es $80 × 0,75 = <strong>$60</strong>: ahorras $20.</p>
<h2>Descuentos acumulados</h2>
<p>"20% más un 10% extra" no es 30%. El segundo descuento se aplica sobre el precio ya rebajado: $100 → $80 → $72, o sea 28%. Usa la calculadora dos veces para comprobarlo.</p>
<h2>Suma el impuesto</h2>
<p>En EE. UU. el impuesto se suma en la caja sobre el precio con descuento. Pon la tasa de tu zona para ver el total.</p>""",
  faq=[("¿Cuánto es 30% de descuento sobre $50?","$35; ahorras $15."),
       ("¿El impuesto va antes o después del descuento?","Después. En la mayoría de los estados pagas impuesto sobre el precio rebajado."),
       ("¿Cómo saco el precio original?","Divide el precio con descuento por (1 − descuento). $60 con 25% viene de $60 ÷ 0,75 = $80.")])),

# ---------------------------------------------------------------- SALES TAX
dict(id="salestax", cat="everyday", aff="money",
 inputs=[S("mode","Mode","Modo",[("add","Add tax to a price","Sumar impuesto a un precio"),("remove","Remove tax from a total","Sacar el impuesto de un total")],"add"),
         N("amount","Amount","Monto",100,"0.01","$"),
         N("rate","Sales tax rate","Tasa de impuesto",7.25,"0.01","%")],
 outputs=[O("total","Total with tax","Total con impuesto",True),O("tax","Tax","Impuesto"),O("pre","Price before tax","Precio sin impuesto")],
 related=["discount","percent","tip"],
 en=dict(slug="sales-tax-calculator", title="Sales Tax Calculator: Add or Remove Sales Tax",
  h1="Sales Tax Calculator", desc="Add sales tax to a price or remove it from a total (reverse sales tax). Enter your state and local rate to get the tax and the final price.",
  intro="Add sales tax to a price, or work backwards from a receipt total to the price before tax.",
  body="""<h2>Formulas</h2>
<ul><li><strong>Add tax</strong>: total = price × (1 + rate ÷ 100). $100 at 7.25% = $107.25.</li>
<li><strong>Remove tax</strong>: price = total ÷ (1 + rate ÷ 100). $107.25 at 7.25% = $100.</li></ul>
<h2>Sales tax in the US</h2>
<p>There is no national sales tax. Each state sets a base rate and many counties and cities add their own, so the combined rate can go from 0% (Oregon, Montana, New Hampshire, Delaware) to more than 10% in some cities. Groceries are taxed at a lower rate or not at all in many states. Check your receipt or your state's revenue department for the exact rate.</p>""",
  faq=[("How do I calculate sales tax backwards?","Divide the total by 1 plus the rate as a decimal. With 8%: total ÷ 1.08."),
       ("Which states have no sales tax?","Alaska (state level), Delaware, Montana, New Hampshire and Oregon."),
       ("Is sales tax charged on tips?","Generally no, a voluntary tip is not taxed; mandatory service charges often are.")]),
 es=dict(slug="calculadora-impuesto-de-venta", title="Calculadora de impuesto de venta (sales tax): sumar o sacar",
  h1="Calculadora de sales tax", desc="Suma el impuesto de venta a un precio o sácalo de un total. Pon la tasa de tu estado y ciudad para ver el impuesto y el precio final.",
  intro="Suma el impuesto de venta a un precio, o calcula al revés el precio sin impuesto desde el total del ticket.",
  body="""<h2>Fórmulas</h2>
<ul><li><strong>Sumar impuesto</strong>: total = precio × (1 + tasa ÷ 100). $100 al 7,25% = $107,25.</li>
<li><strong>Sacar impuesto</strong>: precio = total ÷ (1 + tasa ÷ 100). $107,25 al 7,25% = $100.</li></ul>
<h2>El sales tax en Estados Unidos</h2>
<p>No hay un impuesto nacional. Cada estado fija una tasa base y muchos condados y ciudades suman la suya, así que la tasa combinada va del 0% (Oregon, Montana, New Hampshire, Delaware) a más del 10% en algunas ciudades. En muchos estados la comida del supermercado paga menos o nada. Fíjate la tasa exacta en tu ticket o en el sitio de impuestos de tu estado.</p>""",
  faq=[("¿Cómo saco el impuesto de un total?","Divide el total por 1 más la tasa en decimal. Con 8%: total ÷ 1,08."),
       ("¿Qué estados no tienen sales tax?","Alaska (a nivel estatal), Delaware, Montana, New Hampshire y Oregon."),
       ("¿La propina paga impuesto?","En general no, si es voluntaria; los cargos de servicio obligatorios muchas veces sí.")])),

# ---------------------------------------------------------------- GAS TRIP
dict(id="gas", cat="everyday", aff="money",
 inputs=[N("distance","Distance (miles, one way)","Distancia (millas, ida)",240,"1"),
         S("round","Round trip?","¿Ida y vuelta?",YESNO,"yes"),
         N("mpg","Fuel economy (MPG)","Rendimiento (millas por galón)",28,"0.5"),
         N("price","Gas price per gallon","Precio del galón",3.29,"0.01","$"),
         N("people","People sharing the cost","Personas que comparten",1,"1","","1")],
 outputs=[O("cost","Trip fuel cost","Costo de gasolina del viaje",True),O("each","Cost per person","Costo por persona"),O("gallons","Gas needed","Gasolina necesaria")],
 related=["budget","split","percent"],
 en=dict(slug="gas-trip-cost-calculator", title="Gas Cost Calculator: How Much Will My Road Trip Cost?",
  h1="Gas Trip Cost Calculator", desc="Estimate the fuel cost of a road trip from distance, MPG and gas price. Split it between passengers. Round trip option included.",
  intro="Estimate how much gas your trip will cost and how much each passenger should chip in.",
  body="""<h2>The formula</h2>
<p><strong>Fuel cost = miles ÷ MPG × price per gallon</strong>. A 240-mile trip each way (480 miles) in a car that gets 28 MPG uses about 17.1 gallons. At $3.29 a gallon that is <strong>$56.40</strong>, or $14.10 each for four people.</p>
<h2>Tips to spend less on gas</h2>
<ul><li>Keep tires properly inflated; low pressure can cost 1–3% in fuel economy.</li>
<li>Drive at 60–65 mph instead of 75–80 on the highway.</li>
<li>Remove roof racks you are not using.</li>
<li>Compare gas prices along the route with a gas price app.</li></ul>""",
  faq=[("How do I find my car's MPG?","Check the window sticker or fueleconomy.gov, or divide the miles driven by the gallons used at your next fill-up."),
       ("Does this include tolls and parking?","No, only fuel. Add tolls and parking separately."),
       ("Can I use kilometers?","Convert kilometers to miles first: 1 km = 0.621 miles.")]),
 es=dict(slug="calculadora-costo-gasolina-viaje", title="Calculadora de costo de gasolina para un viaje en auto",
  h1="Costo de gasolina del viaje", desc="Calcula cuánto vas a gastar de gasolina en un viaje según la distancia, el rendimiento y el precio del galón. Divídelo entre los pasajeros.",
  intro="Calcula cuánto te va a costar la gasolina del viaje y cuánto tiene que poner cada pasajero.",
  body="""<h2>La fórmula</h2>
<p><strong>Costo = millas ÷ millas por galón × precio del galón</strong>. Un viaje de 240 millas de ida (480 ida y vuelta) en un auto que hace 28 millas por galón usa unos 17,1 galones. A $3,29 el galón son <strong>$56,40</strong>, o $14,10 cada uno si son cuatro.</p>
<h2>Consejos para gastar menos gasolina</h2>
<ul><li>Mantén las llantas bien infladas: con poca presión se pierde entre 1% y 3% de rendimiento.</li>
<li>Maneja a 60–65 mph en la ruta en vez de 75–80.</li>
<li>Saca el portaequipaje del techo si no lo usas.</li>
<li>Compara precios en el camino con una app de precios de gasolina.</li></ul>""",
  faq=[("¿Cómo sé cuántas millas por galón hace mi auto?","Mira la etiqueta del auto o fueleconomy.gov, o divide las millas recorridas por los galones que cargas la próxima vez."),
       ("¿Incluye peajes y estacionamiento?","No, solo gasolina. Suma peajes y estacionamiento aparte."),
       ("¿Puedo usar kilómetros?","Pasa los kilómetros a millas primero: 1 km = 0,621 millas.")])),
# ================================================================ ADDED NOV 2026 (high US search volume)
# ---------------------------------------------------------------- MORTGAGE
dict(id="mortgage", cat="money", aff="money",
 inputs=[N("price","Home price","Precio de la casa",400000,"1000","$"),
         N("down","Down payment","Enganche (pago inicial)",20,"1","%"),
         N("rate","Interest rate","Tasa de interés",6.5,"0.01","%"),
         S("years","Loan term","Plazo",[("30","30 years","30 años"),("20","20 years","20 años"),("15","15 years","15 años"),("10","10 years","10 años")],"30"),
         N("taxrate","Property tax per year","Impuesto a la propiedad por año",1.1,"0.01","%"),
         N("insurance","Home insurance per year","Seguro de la casa por año",1800,"10","$"),
         N("pmi","PMI if down payment is under 20%","PMI si el enganche es menos del 20%",0.7,"0.05","%"),
         N("hoa","HOA fees per month","Cuota de HOA por mes",0,"5","$")],
 presets=("down",[3.5,5,10,20]),
 outputs=[O("monthly","Monthly payment","Pago mensual",True),O("pi","Principal and interest","Capital e interés"),
          O("taxes","Property tax / insurance per month","Impuesto / seguro por mes"),O("pmiOut","PMI per month","PMI por mes"),
          O("loanAmt","Loan amount","Monto del préstamo"),O("interest","Total interest over the loan","Interés total del préstamo")],
 related=["loan","budget","rule503020"],
 en=dict(slug="mortgage-calculator", title="Mortgage Calculator with Taxes, Insurance and PMI",
  h1="Mortgage Calculator", desc="Free mortgage calculator: monthly payment with principal, interest, property tax, home insurance, PMI and HOA. 30, 20, 15 or 10 years.",
  intro="See the real monthly cost of a home, not just principal and interest: taxes, insurance, PMI and HOA included.",
  body="""<h2>How the monthly payment is calculated</h2>
<p>The loan part uses the standard amortization formula: <strong>M = P × r ÷ (1 − (1 + r)<sup>−n</sup>)</strong>, where P is the loan amount, r the monthly rate (annual rate ÷ 12) and n the number of payments. Then the calculator adds one twelfth of the yearly property tax and insurance, PMI when the down payment is under 20%, and HOA fees. That full number is often called PITI.</p>
<h2>Example</h2>
<p>A $400,000 home with 20% down is a $320,000 loan. At 6.5% for 30 years, principal and interest are about <strong>$2,023 a month</strong>. Add $367 of property tax (1.1% a year) and $150 of insurance and the payment is about $2,540.</p>
<h2>What is PMI?</h2>
<p>Private mortgage insurance protects the lender on conventional loans with less than 20% down. It usually costs 0.3% to 1.5% of the loan per year. You can ask to cancel it when you reach 20% equity, and it ends automatically at 22% equity (78% of the original value). FHA loans have their own mortgage insurance (MIP) with different rules.</p>
<h2>How much house can I afford?</h2>
<p>A common rule is to keep the full housing payment under 28% of your gross monthly income and all debts under 36%. Lenders may approve more, but a payment that fits your budget leaves room for repairs and savings. Try the family budget calculator to check.</p>
<h2>15 or 30 years?</h2>
<p>A 15-year loan has a higher payment but usually a lower rate and much less total interest. Switch the term above and compare the "Total interest" line.</p>""",
  faq=[("Does this mortgage calculator include taxes and insurance?","Yes. Enter your yearly property tax rate and insurance premium and they are added to the monthly payment, along with PMI and HOA."),
       ("What is a typical property tax rate?","The US average is around 1% of the home value per year, but it goes from about 0.3% to over 2% depending on the state and county. Check your county assessor's site."),
       ("How can I avoid PMI?","Put 20% down, use a piggyback loan, or look at loan programs without PMI (such as VA loans). PMI can be removed later once you have 20% equity.")]),
 es=dict(slug="calculadora-de-hipoteca", title="Calculadora de hipoteca con impuestos, seguro y PMI",
  h1="Calculadora de hipoteca", desc="Calculadora de hipoteca gratis: pago mensual con capital, interés, impuesto a la propiedad, seguro, PMI y HOA. A 30, 20, 15 o 10 años.",
  intro="Mira el costo mensual real de una casa, no solo capital e interés: impuestos, seguro, PMI y HOA incluidos.",
  body="""<h2>Cómo se calcula el pago mensual</h2>
<p>La parte del préstamo usa la fórmula de amortización: <strong>M = P × r ÷ (1 − (1 + r)<sup>−n</sup>)</strong>, donde P es el monto del préstamo, r la tasa mensual (tasa anual ÷ 12) y n la cantidad de pagos. Después la calculadora suma la doceava parte del impuesto a la propiedad y del seguro, el PMI si el enganche es menor al 20% y la cuota de HOA. A ese total se le suele llamar PITI.</p>
<h2>Ejemplo</h2>
<p>Una casa de $400.000 con 20% de enganche es un préstamo de $320.000. Al 6,5% a 30 años, capital e interés dan unos <strong>$2.023 por mes</strong>. Con $367 de impuesto (1,1% anual) y $150 de seguro, el pago queda en unos $2.540.</p>
<h2>¿Qué es el PMI?</h2>
<p>Es un seguro hipotecario privado que protege al banco en los préstamos convencionales con menos del 20% de enganche. Suele costar entre 0,3% y 1,5% del préstamo por año. Puedes pedir que lo quiten cuando llegas al 20% de capital propio, y se cancela solo al 22% (78% del valor original). Los préstamos FHA tienen su propio seguro (MIP) con otras reglas.</p>
<h2>¿Cuánta casa me puedo permitir?</h2>
<p>Una regla común es que el pago total de la vivienda no pase del 28% del ingreso bruto mensual y todas las deudas juntas no pasen del 36%. El banco puede aprobarte más, pero un pago que entra en tu presupuesto deja margen para arreglos y ahorro. Pruébalo con la calculadora de presupuesto familiar.</p>
<h2>¿15 o 30 años?</h2>
<p>A 15 años el pago es más alto, pero la tasa suele ser menor y el interés total mucho más bajo. Cambia el plazo arriba y compara la línea "Interés total".</p>""",
  faq=[("¿La calculadora incluye impuestos y seguro?","Sí. Pon la tasa anual del impuesto a la propiedad y el costo del seguro y se suman al pago mensual, junto con el PMI y el HOA."),
       ("¿Cuánto es el impuesto a la propiedad?","El promedio en EE. UU. ronda el 1% del valor de la casa por año, pero va de 0,3% a más de 2% según el estado y el condado. Fíjate en el sitio del tasador de tu condado."),
       ("¿Cómo evito el PMI?","Dando 20% de enganche, con un segundo préstamo (piggyback) o con programas sin PMI, como los préstamos VA. También se puede quitar después, al llegar al 20% de capital propio.")])),

# ---------------------------------------------------------------- COMPOUND INTEREST
dict(id="compound", cat="money", aff="money",
 inputs=[N("initial","Initial deposit","Depósito inicial",5000,"100","$"),
         N("monthly","Monthly contribution","Aporte mensual",200,"10","$"),
         N("rate","Annual interest rate","Tasa de interés anual",7,"0.1","%"),
         N("years","Years","Años",20,"1"),
         S("freq","Compounding","Capitalización",[("12","Monthly","Mensual"),("365","Daily","Diaria"),("4","Quarterly","Trimestral"),("1","Yearly","Anual")],"12")],
 outputs=[O("fv","Future value","Valor final",True),O("contrib","Total you put in","Total que aportaste"),
          O("earned","Interest earned","Intereses ganados"),O("doubling","Years to double (rule of 72)","Años para duplicar (regla del 72)")],
 related=["savings","rule503020","percent"],
 en=dict(slug="compound-interest-calculator", title="Compound Interest Calculator with Monthly Contributions",
  h1="Compound Interest Calculator", desc="Free compound interest calculator. See how your savings or investments grow with monthly contributions and daily, monthly, quarterly or yearly compounding.",
  intro="See how money grows when interest earns interest, with a starting amount and a monthly contribution.",
  body="""<h2>The compound interest formula</h2>
<p>For a single deposit: <strong>A = P × (1 + r/n)<sup>n×t</sup></strong>, where P is the deposit, r the annual rate, n how many times a year interest is added and t the years. With monthly contributions each deposit grows for the months left, and the calculator adds them all up month by month.</p>
<h2>Example</h2>
<p>$5,000 to start plus $200 a month at 7% for 20 years. You put in $53,000 in total and end with about <strong>$124,000</strong>: more than half of it is interest.</p>
<h2>The rule of 72</h2>
<p>Divide 72 by the yearly rate to estimate how many years it takes to double your money. At 6% it takes about 12 years; at 9%, about 8.</p>
<h2>Where can you get compound interest?</h2>
<ul><li><strong>High-yield savings accounts</strong> and CDs: low risk, FDIC insured up to the limit.</li>
<li><strong>Index funds</strong> in a 401(k) or IRA: higher long-term returns but the value goes up and down; past returns do not guarantee future ones.</li>
<li><strong>Credit cards work the other way</strong>: compound interest makes debt grow fast. See the credit card payoff calculator.</li></ul>""",
  faq=[("What is the difference between simple and compound interest?","Simple interest is paid only on the original amount. Compound interest is also paid on the interest already earned, so growth speeds up over time."),
       ("Does daily compounding make a big difference?","Not much compared with monthly. At 5%, monthly compounding gives an effective 5.12% a year and daily 5.13%."),
       ("What rate should I use for the stock market?","Many people use 5% to 7% after inflation for a diversified stock index fund over long periods. It is an estimate, not a promise.")]),
 es=dict(slug="calculadora-interes-compuesto", title="Calculadora de interés compuesto con aportes mensuales",
  h1="Calculadora de interés compuesto", desc="Calculadora de interés compuesto gratis. Mira cuánto crecen tus ahorros o inversiones con aportes mensuales y capitalización diaria, mensual o anual.",
  intro="Mira cuánto crece tu dinero cuando los intereses generan más intereses, con un monto inicial y un aporte por mes.",
  body="""<h2>La fórmula del interés compuesto</h2>
<p>Para un solo depósito: <strong>A = P × (1 + r/n)<sup>n×t</sup></strong>, donde P es el depósito, r la tasa anual, n cuántas veces por año se suman los intereses y t los años. Con aportes mensuales cada depósito crece por los meses que le quedan, y la calculadora los suma mes a mes.</p>
<h2>Ejemplo</h2>
<p>$5.000 para empezar más $200 por mes al 7% durante 20 años. Pones $53.000 en total y terminas con unos <strong>$124.000</strong>: más de la mitad son intereses.</p>
<h2>La regla del 72</h2>
<p>Divide 72 por la tasa anual para saber más o menos en cuántos años se duplica tu dinero. Al 6% tarda unos 12 años; al 9%, unos 8.</p>
<h2>¿Dónde se gana interés compuesto?</h2>
<ul><li><strong>Cuentas de ahorro de alto rendimiento</strong> y CDs: poco riesgo, aseguradas por la FDIC hasta el límite.</li>
<li><strong>Fondos indexados</strong> en un 401(k) o IRA: más rendimiento a largo plazo, pero el valor sube y baja; lo pasado no garantiza lo que viene.</li>
<li><strong>Las tarjetas de crédito funcionan al revés</strong>: el interés compuesto hace crecer la deuda rápido. Mira la calculadora para pagar la tarjeta.</li></ul>""",
  faq=[("¿Qué diferencia hay entre interés simple y compuesto?","El simple se paga solo sobre el monto original. El compuesto también se paga sobre los intereses ya ganados, así que el crecimiento se acelera con el tiempo."),
       ("¿La capitalización diaria cambia mucho?","Poco comparada con la mensual. Al 5%, la mensual da un 5,12% efectivo por año y la diaria un 5,13%."),
       ("¿Qué tasa uso para la bolsa?","Mucha gente usa entre 5% y 7% por encima de la inflación para un fondo indexado diversificado a largo plazo. Es una estimación, no una promesa.")])),

# ---------------------------------------------------------------- AUTO LOAN
dict(id="autoloan", cat="money", aff="money",
 inputs=[N("price","Vehicle price","Precio del auto",32000,"100","$"),
         N("down","Down payment","Pago inicial",4000,"100","$"),
         N("trade","Trade-in value","Valor del auto que entregas",0,"100","$"),
         S("tradetax","Does your state tax only the difference after trade-in?","¿Tu estado cobra impuesto solo sobre la diferencia?",YESNO,"yes"),
         N("tax","Sales tax","Impuesto de venta",7,"0.01","%"),
         N("fees","Title, registration and dealer fees","Título, registro y cargos del concesionario",800,"10","$"),
         N("apr","Interest rate (APR)","Tasa de interés (APR)",7.5,"0.01","%"),
         S("months","Loan term","Plazo",[("36","36 months","36 meses"),("48","48 months","48 meses"),("60","60 months","60 meses"),("72","72 months","72 meses"),("84","84 months","84 meses")],"60")],
 outputs=[O("monthly","Monthly payment","Pago mensual",True),O("loanAmt","Amount financed","Monto financiado"),O("salesTax","Sales tax","Impuesto de venta"),
          O("interest","Total interest","Interés total"),O("total","Total cost of the car","Costo total del auto")],
 related=["loan","budget","gas"],
 en=dict(slug="auto-loan-calculator", title="Auto Loan Calculator: Car Payment with Tax, Trade-In and Fees",
  h1="Auto Loan Calculator", desc="Free car payment calculator with sales tax, trade-in, down payment and fees. Compare 36, 48, 60, 72 and 84-month auto loans and the total interest.",
  intro="Find your monthly car payment with everything the dealer adds: sales tax, fees, trade-in and down payment.",
  body="""<h2>How the car payment is calculated</h2>
<p>Amount financed = price + sales tax + fees − down payment − trade-in. The monthly payment then uses the standard loan formula with your APR and term. In most states sales tax is charged only on the price minus the trade-in; a few (such as California, Michigan and Virginia) tax the full price, so switch that option to "No".</p>
<h2>Example</h2>
<p>A $32,000 car with $4,000 down, 7% tax and $800 in fees. You finance $31,040. At 7.5% for 60 months the payment is about <strong>$622</strong> and you pay about $6,280 in interest.</p>
<h2>Longer is not cheaper</h2>
<p>A 72 or 84-month loan lowers the payment but adds a lot of interest, and you can owe more than the car is worth for years (being "upside down"). A popular guideline is 20/4/10: at least 20% down, no more than 4 years, and total car costs under 10% of your income.</p>
<h2>Get pre-approved first</h2>
<p>Ask your bank or a credit union for a pre-approval before visiting the dealer. Then you can compare their APR with the dealer's offer and negotiate the price of the car separately from the financing.</p>""",
  faq=[("What is a good APR for a car loan?","It depends on your credit score and whether the car is new or used. Borrowers with excellent credit get the lowest rates; used cars and lower scores pay more. Compare at least two offers."),
       ("Should I include sales tax in the loan?","You can pay it upfront to borrow less, or roll it into the loan. Rolling it in is common but you pay interest on it."),
       ("Is it better to pay cash or finance?","If the loan APR is higher than what your savings earn, paying cash (or a larger down payment) saves money. Keep an emergency fund first.")]),
 es=dict(slug="calculadora-prestamo-de-auto", title="Calculadora de préstamo de auto: cuota con impuesto, entrega y cargos",
  h1="Calculadora de préstamo de auto", desc="Calcula la cuota mensual del auto con impuesto de venta, auto en parte de pago, pago inicial y cargos. Compara plazos de 36 a 84 meses.",
  intro="Calcula la cuota mensual del auto con todo lo que suma el concesionario: impuesto, cargos, auto en parte de pago y pago inicial.",
  body="""<h2>Cómo se calcula la cuota</h2>
<p>Monto financiado = precio + impuesto + cargos − pago inicial − auto que entregas. La cuota usa la fórmula de préstamos con tu APR y el plazo. En la mayoría de los estados el impuesto se cobra solo sobre el precio menos el auto que entregas; algunos (como California, Michigan y Virginia) lo cobran sobre el precio completo: en ese caso elige "No".</p>
<h2>Ejemplo</h2>
<p>Un auto de $32.000 con $4.000 de pago inicial, 7% de impuesto y $800 de cargos. Financias $31.040. Al 7,5% a 60 meses la cuota es de unos <strong>$622</strong> y pagas unos $6.280 de interés.</p>
<h2>Más largo no es más barato</h2>
<p>Un préstamo a 72 u 84 meses baja la cuota pero suma mucho interés, y puedes deber más de lo que vale el auto durante años. Una guía conocida es 20/4/10: al menos 20% de pago inicial, no más de 4 años y que todos los gastos del auto no pasen del 10% de tu ingreso.</p>
<h2>Pide una preaprobación antes</h2>
<p>Pide una preaprobación en tu banco o en una credit union antes de ir al concesionario. Así comparas su APR con la oferta del concesionario y negocias el precio del auto aparte del financiamiento.</p>""",
  faq=[("¿Qué APR es bueno para un auto?","Depende de tu puntaje de crédito y de si el auto es nuevo o usado. Con crédito excelente se consiguen las tasas más bajas; los usados y los puntajes bajos pagan más. Compara al menos dos ofertas."),
       ("¿Conviene meter el impuesto en el préstamo?","Puedes pagarlo al contado para pedir menos, o sumarlo al préstamo. Sumarlo es común, pero pagas interés sobre él."),
       ("¿Es mejor pagar al contado o financiar?","Si el APR del préstamo es más alto que lo que te rinden los ahorros, pagar al contado (o dar más de inicial) te ahorra plata. Primero guarda un fondo de emergencia.")])),

# ---------------------------------------------------------------- CREDIT CARD PAYOFF
dict(id="ccpayoff", cat="money", aff="money",
 inputs=[N("balance","Credit card balance","Saldo de la tarjeta",5000,"10","$"),
         N("apr","Interest rate (APR)","Tasa de interés (APR)",22.9,"0.1","%"),
         N("payment","Monthly payment","Pago mensual",200,"5","$"),
         N("target","Months you want to be debt-free in","En cuántos meses quieres terminar",24,"1","","1")],
 outputs=[O("months","Time to pay it off","Tiempo para pagarla",True),O("interest","Total interest you will pay","Interés total que pagarás"),
          O("needed","Payment to finish in your target months","Pago para terminar en tus meses")],
 related=["budget","compound","loan"],
 en=dict(slug="credit-card-payoff-calculator", title="Credit Card Payoff Calculator: How Long to Pay Off Debt",
  h1="Credit Card Payoff Calculator", desc="Find out how many months it takes to pay off a credit card, how much interest you will pay, and the monthly payment to be debt-free by your goal date.",
  intro="See when your credit card will be paid off and how much a bigger payment saves you in interest.",
  body="""<h2>How it works</h2>
<p>Each month the card adds interest (APR ÷ 12 on the balance) and your payment is subtracted. The calculator repeats this until the balance is zero, so you see the exact number of months and the total interest. It assumes you stop using the card while you pay it off.</p>
<h2>Example</h2>
<p>A $5,000 balance at 22.9% APR with $200 a month takes about <strong>35 months</strong> and costs around $1,860 in interest. Paying $300 a month cuts it to 21 months and about $1,080 of interest.</p>
<h2>Why the minimum payment is a trap</h2>
<p>Minimum payments are usually 1% to 3% of the balance plus interest, so they shrink as the balance shrinks. Paying only the minimum can take more than 10 years. Your statement shows how long it would take; a fixed payment is always faster.</p>
<h2>Ways to pay it off faster</h2>
<ul><li><strong>Avalanche</strong>: pay extra on the card with the highest APR first. It saves the most money.</li>
<li><strong>Snowball</strong>: pay off the smallest balance first for quick wins and motivation.</li>
<li><strong>0% balance transfer</strong>: moving the debt to a 0% intro card stops the interest for a while; watch the transfer fee (often 3%–5%).</li>
<li>Call your card issuer and ask for a lower rate; it works more often than people think.</li></ul>""",
  faq=[("How is credit card interest calculated?","Most cards use the average daily balance and a daily rate (APR ÷ 365). Using APR ÷ 12 per month, as this calculator does, gives a very close estimate."),
       ("What if my payment is too low?","If the payment is not more than the monthly interest, the balance never goes down. The calculator will warn you."),
       ("Should I pay off debt or save first?","Most planners suggest a small emergency fund first (for example $1,000), then attacking high-interest debt, because 20%+ APR is more than savings can earn.")]),
 es=dict(slug="calculadora-pagar-tarjeta-de-credito", title="Calculadora para pagar la tarjeta de crédito: en cuánto tiempo",
  h1="Calculadora para pagar la tarjeta", desc="Calcula en cuántos meses terminas de pagar la tarjeta de crédito, cuánto interés pagas y qué cuota necesitas para quedar sin deuda en la fecha que quieras.",
  intro="Mira cuándo terminas de pagar la tarjeta y cuánto interés te ahorras con un pago más grande.",
  body="""<h2>Cómo funciona</h2>
<p>Cada mes la tarjeta suma interés (APR ÷ 12 sobre el saldo) y se resta tu pago. La calculadora repite esto hasta llegar a cero, así ves la cantidad exacta de meses y el interés total. Supone que no usas la tarjeta mientras la pagas.</p>
<h2>Ejemplo</h2>
<p>Un saldo de $5.000 al 22,9% de APR pagando $200 por mes tarda unos <strong>35 meses</strong> y cuesta alrededor de $1.860 de interés. Pagando $300 por mes baja a 21 meses y unos $1.080 de interés.</p>
<h2>Por qué el pago mínimo es una trampa</h2>
<p>El pago mínimo suele ser del 1% al 3% del saldo más los intereses, así que baja a medida que baja el saldo. Pagando solo el mínimo puedes tardar más de 10 años. Tu resumen lo muestra; un pago fijo siempre es más rápido.</p>
<h2>Formas de pagarla más rápido</h2>
<ul><li><strong>Avalancha</strong>: pon lo extra en la tarjeta con el APR más alto. Es lo que más ahorra.</li>
<li><strong>Bola de nieve</strong>: paga primero el saldo más chico, para ver avances rápido y no aflojar.</li>
<li><strong>Transferencia al 0%</strong>: pasar la deuda a una tarjeta con 0% inicial frena el interés un tiempo; ojo con el cargo por transferir (suele ser 3%–5%).</li>
<li>Llama al banco y pide una tasa más baja: funciona más seguido de lo que parece.</li></ul>""",
  faq=[("¿Cómo se calcula el interés de la tarjeta?","La mayoría usa el saldo diario promedio y una tasa diaria (APR ÷ 365). Usar APR ÷ 12 por mes, como hace esta calculadora, da un resultado muy parecido."),
       ("¿Y si mi pago es muy bajo?","Si el pago no supera el interés del mes, el saldo nunca baja. La calculadora te avisa."),
       ("¿Pago la deuda o ahorro primero?","Muchos asesores sugieren primero un fondo de emergencia chico (por ejemplo $1.000) y después atacar la deuda cara, porque un APR de más del 20% es más de lo que rinde cualquier ahorro.")])),

# ---------------------------------------------------------------- TIME CARD
dict(id="timecard", cat="work", aff="work",
 inputs=[TR("d1","Monday","Lunes","09:00","17:30","30"),TR("d2","Tuesday","Martes","09:00","17:30","30"),
         TR("d3","Wednesday","Miércoles","09:00","17:30","30"),TR("d4","Thursday","Jueves","09:00","17:30","30"),
         TR("d5","Friday","Viernes","09:00","17:30","30"),TR("d6","Saturday","Sábado"),TR("d7","Sunday","Domingo"),
         N("rate","Hourly wage (optional)","Pago por hora (opcional)",18,"0.01","$")],
 outputs=[O("hours","Total hours this week","Total de horas de la semana",True),O("ot","Overtime (over 40 h)","Horas extra (más de 40)"),
          O("pay","Gross pay (overtime at 1.5×)","Pago bruto (extras a 1,5×)"),O("days","Hours per day","Horas por día",pre=True)],
 related=["overtime","hourly","tipout"],
 en=dict(slug="time-card-calculator", title="Time Card Calculator: Weekly Hours with Breaks and Overtime",
  h1="Time Card Calculator", desc="Free time card calculator. Enter start and end times for each day, subtract lunch breaks, and get total weekly hours, overtime and gross pay.",
  intro="Add up your hours for the week from clock-in and clock-out times, with unpaid breaks, overtime and pay.",
  body="""<h2>How to use it</h2>
<p>For each day, enter the time you started and the time you finished, and the minutes of unpaid break (for example a 30-minute lunch). Leave a day empty if you did not work. Shifts that end after midnight are handled automatically.</p>
<h2>Hours and minutes vs. decimal hours</h2>
<p>Payroll uses decimal hours: 7 hours 45 minutes is <strong>7.75 hours</strong>, not 7.45. To convert, divide the minutes by 60 (45 ÷ 60 = 0.75). The calculator shows both.</p>
<h2>Overtime</h2>
<p>Under federal law (FLSA), non-exempt employees get at least 1.5 times their regular rate for hours over 40 in a workweek. Some states, like California, also require overtime after 8 hours in a day. This calculator uses the weekly 40-hour rule; check the overtime calculator for other cases.</p>
<h2>Example</h2>
<p>Monday to Friday from 9:00 to 17:30 with a 30-minute lunch is 8 hours a day, 40 hours a week. At $18 an hour that is <strong>$720</strong> before taxes.</p>""",
  faq=[("Are breaks paid?","Under federal rules, short breaks of 5 to 20 minutes are paid, while meal breaks of 30 minutes or more where you are fully relieved can be unpaid. Enter only the unpaid minutes."),
       ("How do I calculate hours worked between two times?","Subtract the start time from the end time and then the unpaid break. 8:30 to 17:15 is 8 h 45 m; minus 30 minutes of lunch is 8 h 15 m, or 8.25 hours."),
       ("Does it work for night shifts?","Yes. If the end time is earlier than the start time, the calculator assumes the shift ended the next day.")]),
 es=dict(slug="calculadora-de-horas-trabajadas", title="Calculadora de horas trabajadas: horas de la semana con descansos y extras",
  h1="Calculadora de horas trabajadas", desc="Calculadora de horas trabajadas gratis: pon la hora de entrada y salida de cada día, resta el almuerzo y mira el total de horas, las horas extra y el pago.",
  intro="Suma tus horas de la semana con la hora de entrada y salida de cada día, con descansos sin pago, horas extra y sueldo.",
  body="""<h2>Cómo se usa</h2>
<p>Para cada día pon la hora de entrada, la de salida y los minutos de descanso que no se pagan (por ejemplo, 30 minutos de almuerzo). Deja vacío el día que no trabajaste. Los turnos que terminan después de medianoche se calculan solos.</p>
<h2>Horas y minutos o horas decimales</h2>
<p>La nómina usa horas decimales: 7 horas y 45 minutos son <strong>7,75 horas</strong>, no 7,45. Para pasar, divide los minutos por 60 (45 ÷ 60 = 0,75). La calculadora muestra las dos formas.</p>
<h2>Horas extra</h2>
<p>Según la ley federal (FLSA), los empleados no exentos cobran al menos 1,5 veces su tarifa por las horas que pasan de 40 en la semana. Algunos estados, como California, también pagan extra después de 8 horas en un día. Esta calculadora usa la regla de 40 horas semanales; para otros casos usa la calculadora de horas extra.</p>
<h2>Ejemplo</h2>
<p>De lunes a viernes de 9:00 a 17:30 con 30 minutos de almuerzo son 8 horas por día, 40 por semana. A $18 la hora son <strong>$720</strong> antes de impuestos.</p>""",
  faq=[("¿Los descansos se pagan?","Según las reglas federales, los descansos cortos de 5 a 20 minutos se pagan; las comidas de 30 minutos o más en las que no trabajas pueden no pagarse. Pon solo los minutos sin pago."),
       ("¿Cómo calculo las horas entre dos horarios?","Resta la hora de entrada a la de salida y después el descanso. De 8:30 a 17:15 son 8 h 45 m; menos 30 minutos de almuerzo quedan 8 h 15 m, o sea 8,25 horas."),
       ("¿Sirve para turnos de noche?","Sí. Si la salida es más temprano que la entrada, la calculadora entiende que saliste al día siguiente.")])),

# ---------------------------------------------------------------- AGE
dict(id="age", cat="everyday", aff="money",
 inputs=[D("birth","Date of birth","Fecha de nacimiento","1990-06-15"),
         D("asof","Age on this date","Edad a esta fecha","today")],
 outputs=[O("age","Age","Edad",True),O("total","In months","En meses"),O("days","In days","En días"),O("next","Next birthday","Próximo cumpleaños")],
 related=["datediff","percent","savings"],
 en=dict(slug="age-calculator", title="Age Calculator: How Old Am I in Years, Months and Days?",
  h1="Age Calculator", desc="Free age calculator. Enter a date of birth to get the exact age in years, months and days, the total days lived, and the days until the next birthday.",
  intro="Get an exact age in years, months and days, on today's date or any other date.",
  body="""<h2>How age is calculated</h2>
<p>The calculator counts full years since the date of birth, then full months, then the remaining days, the same way people say "34 years, 5 months and 2 days". It handles leap years and months with different numbers of days.</p>
<h2>Uses</h2>
<ul><li>Checking the exact age on a form, an application or a contract date.</li>
<li>Knowing how old a child will be on the first day of school or a sports cut-off date.</li>
<li>Counting days lived, or the days left to the next birthday.</li></ul>
<h2>Born on February 29?</h2>
<p>In non-leap years most people celebrate on February 28 or March 1. Legally, many US states consider that you turn a year older on March 1 in a non-leap year. This calculator counts the next birthday from February 28 of those years.</p>""",
  faq=[("How do I calculate my age in days?","Enter your date of birth and the calculator shows the total days lived, counting leap years."),
       ("Can I find someone's age on a past or future date?","Yes. Change the second date to any date, for example a school cut-off or a retirement date."),
       ("Is my birth date saved?","No. Everything is calculated on your device and nothing is sent anywhere.")]),
 es=dict(slug="calculadora-de-edad", title="Calculadora de edad: cuántos años, meses y días tengo",
  h1="Calculadora de edad", desc="Calculadora de edad gratis. Pon la fecha de nacimiento y mira la edad exacta en años, meses y días, los días vividos y cuánto falta para el cumpleaños.",
  intro="Saca la edad exacta en años, meses y días, a la fecha de hoy o a cualquier otra.",
  body="""<h2>Cómo se calcula la edad</h2>
<p>La calculadora cuenta los años completos desde la fecha de nacimiento, después los meses completos y después los días que sobran, igual que cuando decimos "34 años, 5 meses y 2 días". Tiene en cuenta los años bisiestos y los meses de distinta cantidad de días.</p>
<h2>Para qué sirve</h2>
<ul><li>Ver la edad exacta para un formulario, una solicitud o la fecha de un contrato.</li>
<li>Saber qué edad tendrá un chico el primer día de clases o en la fecha de corte de un deporte.</li>
<li>Contar los días vividos o los que faltan para el próximo cumpleaños.</li></ul>
<h2>¿Naciste un 29 de febrero?</h2>
<p>En los años no bisiestos la mayoría lo festeja el 28 de febrero o el 1 de marzo. En muchos estados de EE. UU., legalmente cumples años el 1 de marzo en los años no bisiestos. Esta calculadora cuenta el próximo cumpleaños desde el 28 de febrero en esos años.</p>""",
  faq=[("¿Cómo calculo mi edad en días?","Pon tu fecha de nacimiento y la calculadora muestra el total de días vividos, con los años bisiestos."),
       ("¿Puedo ver la edad en una fecha pasada o futura?","Sí. Cambia la segunda fecha por la que quieras, por ejemplo la fecha de corte de la escuela o la de tu jubilación."),
       ("¿Se guarda mi fecha de nacimiento?","No. Todo se calcula en tu dispositivo y no se envía nada.")])),

# ---------------------------------------------------------------- DAYS BETWEEN DATES
dict(id="datediff", cat="everyday", aff="money",
 inputs=[D("start","Start date","Fecha de inicio","today"),
         D("end","End date","Fecha de fin","2026-12-25"),
         S("incl","Count the end day too?","¿Contar también el último día?",[("no","No","No"),("yes","Yes","Sí")],"no")],
 outputs=[O("days","Days between the dates","Días entre las fechas",True),O("weeks","In weeks","En semanas"),O("months","In months and years","En meses y años"),O("work","Business days","Días hábiles")],
 related=["age","timecard","savings"],
 en=dict(slug="days-between-dates-calculator", title="Days Between Dates Calculator: Count Days, Weeks and Business Days",
  h1="Days Between Dates Calculator", desc="Count the days between two dates, including weeks, months and business days (Monday to Friday). Free day counter for deadlines, trips and countdowns.",
  intro="Count how many days, weeks and business days there are between two dates, for deadlines, trips or a countdown.",
  body="""<h2>How the days are counted</h2>
<p>By default the calculator counts the days from the start date up to the end date without counting the end day, the way you count nights in a hotel or days until an event. Choose "Yes" to include both the first and last day, for example when counting the days of a vacation or a contract.</p>
<h2>Business days</h2>
<p>Business days are Monday to Friday. Federal holidays such as Thanksgiving or Christmas are not subtracted, because they change by year and by employer, so take them out yourself if they fall in the range.</p>
<h2>Quick facts</h2>
<ul><li>A common year has 365 days (52 weeks and 1 day); a leap year has 366.</li>
<li>An average month has about 30.44 days.</li>
<li>"30 days from today" is not always "one month from today": it depends on the month.</li></ul>""",
  faq=[("How many days until Christmas?","Leave today as the start date and set the end date to December 25. The default example already does it."),
       ("Does it count weekends?","The main result counts every calendar day. The business days line counts only Monday to Friday."),
       ("Why is my result one day off?","Check the 'count the end day' option. Some rules count both the first and last day, others count only one of them.")]),
 es=dict(slug="calculadora-dias-entre-fechas", title="Calculadora de días entre fechas: días, semanas y días hábiles",
  h1="Días entre fechas", desc="Cuenta los días entre dos fechas, con semanas, meses y días hábiles (de lunes a viernes). Contador de días gratis para plazos, viajes y cuentas regresivas.",
  intro="Cuenta cuántos días, semanas y días hábiles hay entre dos fechas, para plazos, viajes o una cuenta regresiva.",
  body="""<h2>Cómo se cuentan los días</h2>
<p>Por defecto la calculadora cuenta los días desde la fecha de inicio hasta la de fin sin contar el último día, como se cuentan las noches de hotel o los días que faltan para un evento. Elige "Sí" para contar el primero y el último, por ejemplo para los días de unas vacaciones o de un contrato.</p>
<h2>Días hábiles</h2>
<p>Los días hábiles son de lunes a viernes. No se restan los feriados (como Thanksgiving o Navidad), porque cambian según el año y el empleador: réstalos tú si caen en el período.</p>
<h2>Datos útiles</h2>
<ul><li>Un año común tiene 365 días (52 semanas y 1 día); uno bisiesto, 366.</li>
<li>Un mes tiene en promedio unos 30,44 días.</li>
<li>"30 días desde hoy" no siempre es "un mes desde hoy": depende del mes.</li></ul>""",
  faq=[("¿Cuántos días faltan para Navidad?","Deja hoy como fecha de inicio y pon el 25 de diciembre como fecha de fin. El ejemplo ya viene así."),
       ("¿Cuenta los fines de semana?","El resultado principal cuenta todos los días del calendario. La línea de días hábiles cuenta solo de lunes a viernes."),
       ("¿Por qué me da un día de diferencia?","Revisa la opción de contar el último día. Algunas reglas cuentan el primero y el último, otras solo uno.")])),

# ---------------------------------------------------------------- SQUARE FOOTAGE
dict(id="sqft", cat="everyday", aff="money",
 inputs=[N("length","Length","Largo",12,"0.1"),
         N("width","Width","Ancho",10,"0.1"),
         S("unit","Unit","Unidad",[("ft","Feet","Pies"),("in","Inches","Pulgadas"),("yd","Yards","Yardas"),("m","Meters","Metros")],"ft"),
         N("count","Number of equal rooms or areas","Cantidad de ambientes iguales",1,"1","","1"),
         N("waste","Extra for cuts and waste","Extra por cortes y desperdicio",10,"1","%"),
         N("cost","Price per square foot (optional)","Precio por pie cuadrado (opcional)",0,"0.01","$")],
 outputs=[O("area","Area","Superficie",True),O("metric","In square meters and yards","En metros y yardas cuadradas"),
          O("buy","Material to buy (with extra)","Material a comprar (con extra)"),O("cost","Material cost","Costo del material")],
 related=["percent","discount","budget"],
 en=dict(slug="square-footage-calculator", title="Square Footage Calculator for Rooms, Flooring and Paint",
  h1="Square Footage Calculator", desc="Free square footage calculator. Enter length and width in feet, inches, yards or meters to get the area, the material to buy with waste and the total cost.",
  intro="Get the square feet of a room or area and how much flooring, tile or sod to buy, with extra for cuts.",
  body="""<h2>How to calculate square feet</h2>
<p><strong>Square feet = length × width</strong> (both in feet). A 12 × 10 ft room is 120 sq ft. If you measured in inches, the calculator divides by 144; in meters it multiplies by 10.764.</p>
<h2>L-shaped and odd rooms</h2>
<p>Split the room into rectangles, calculate each one and add them up. For a closet or a hallway that has the same size as another area, use the "number of equal areas" field.</p>
<h2>How much extra to buy</h2>
<ul><li><strong>Carpet, vinyl plank, laminate</strong>: 5% to 10% extra.</li>
<li><strong>Tile</strong>: 10%, or 15% for diagonal patterns.</li>
<li><strong>Hardwood</strong>: 7% to 10%.</li></ul>
<p>Leftover pieces are useful for repairs later, and boxes from a different batch can have a slightly different color.</p>
<h2>Paint</h2>
<p>For walls, multiply the perimeter of the room by the wall height. One gallon of paint covers about 350 to 400 sq ft per coat.</p>""",
  faq=[("How many square feet is a 12x12 room?","144 square feet."),
       ("How do I convert square meters to square feet?","Multiply by 10.764. For example, 20 m² is about 215 sq ft."),
       ("How much does flooring cost per square foot?","It varies a lot by material and region. Enter the price from your store to see the total material cost; installation is extra.")]),
 es=dict(slug="calculadora-de-pies-cuadrados", title="Calculadora de pies cuadrados para pisos, cuartos y pintura",
  h1="Calculadora de pies cuadrados", desc="Calculadora de pies cuadrados gratis. Pon el largo y el ancho en pies, pulgadas, yardas o metros y mira la superficie, el material a comprar y el costo.",
  intro="Saca los pies cuadrados de un cuarto o un terreno y cuánto piso, cerámica o pasto comprar, con extra por cortes.",
  body="""<h2>Cómo calcular pies cuadrados</h2>
<p><strong>Pies cuadrados = largo × ancho</strong> (los dos en pies). Un cuarto de 12 × 10 pies tiene 120 pies cuadrados. Si mediste en pulgadas, la calculadora divide por 144; en metros, multiplica por 10,764.</p>
<h2>Cuartos en L o irregulares</h2>
<p>Divide el cuarto en rectángulos, calcula cada uno y súmalos. Si hay varios ambientes del mismo tamaño, usa el campo "cantidad de ambientes iguales".</p>
<h2>Cuánto extra comprar</h2>
<ul><li><strong>Alfombra, vinílico, laminado</strong>: de 5% a 10% extra.</li>
<li><strong>Cerámica o porcelanato</strong>: 10%, o 15% si va en diagonal.</li>
<li><strong>Madera</strong>: de 7% a 10%.</li></ul>
<p>Lo que sobra sirve para arreglos más adelante, y las cajas de otra tanda pueden venir con un color un poco distinto.</p>
<h2>Pintura</h2>
<p>Para las paredes, multiplica el perímetro del cuarto por la altura. Un galón de pintura cubre unos 350 a 400 pies cuadrados por mano.</p>""",
  faq=[("¿Cuántos pies cuadrados tiene un cuarto de 12x12?","144 pies cuadrados."),
       ("¿Cómo paso metros cuadrados a pies cuadrados?","Multiplica por 10,764. Por ejemplo, 20 m² son unos 215 pies cuadrados."),
       ("¿Cuánto cuesta el piso por pie cuadrado?","Cambia mucho según el material y la zona. Pon el precio de tu tienda para ver el costo del material; la instalación va aparte.")])),

# ---------------------------------------------------------------- BMI
dict(id="bmi", cat="health", aff="money",
 inputs=[N("ft","Height (feet)","Altura (pies)",5,"1"),
         N("inch","Height (inches)","Altura (pulgadas)",7,"0.5"),
         N("lb","Weight (pounds)","Peso (libras)",160,"0.5")],
 outputs=[O("bmi","Your BMI","Tu IMC",True),O("cat","Category","Categoría"),O("range","Healthy weight for your height","Peso saludable para tu altura"),O("metric","In metric","En sistema métrico")],
 related=["calorie","age","percent"],
 en=dict(slug="bmi-calculator", title="BMI Calculator: Body Mass Index in Pounds and Feet",
  h1="BMI Calculator", desc="Free BMI calculator for adults. Enter your height in feet and inches and your weight in pounds to get your body mass index, category and healthy weight range.",
  intro="Find your body mass index (BMI) and the healthy weight range for your height, using feet, inches and pounds.",
  body="""<h2>The BMI formula</h2>
<p><strong>BMI = 703 × weight (lb) ÷ height (in)²</strong>. Someone 5 ft 7 in (67 inches) who weighs 160 lb has a BMI of 703 × 160 ÷ 4,489 = <strong>25.1</strong>.</p>
<h2>BMI categories for adults</h2>
<ul><li>Below 18.5: underweight</li><li>18.5 to 24.9: healthy weight</li><li>25 to 29.9: overweight</li><li>30 or more: obesity</li></ul>
<p>These are the categories used by the CDC and the World Health Organization for adults 20 and older. Children and teens use BMI-for-age percentiles instead.</p>
<h2>What BMI does not tell you</h2>
<p>BMI is a quick screening number, not a diagnosis. It does not separate muscle from fat, so athletes can show as "overweight", and it does not show where fat is stored. Waist size, blood pressure, blood tests and your doctor's advice give a fuller picture.</p>""",
  faq=[("What is a healthy BMI?","For adults, 18.5 to 24.9 is considered a healthy weight range."),
       ("Is BMI accurate for women, older adults and athletes?","It uses the same formula for everyone, but it can overestimate fat in muscular people and underestimate it in older adults who have lost muscle. Use it as a starting point."),
       ("Is this medical advice?","No. It is an informational tool. Talk to a doctor or a registered dietitian about your health and weight.")]),
 es=dict(slug="calculadora-imc", title="Calculadora de IMC (BMI): índice de masa corporal en libras y pies",
  h1="Calculadora de IMC", desc="Calculadora de IMC gratis para adultos. Pon tu altura en pies y pulgadas y tu peso en libras para ver tu índice de masa corporal, la categoría y el peso saludable.",
  intro="Calcula tu índice de masa corporal (IMC o BMI) y el rango de peso saludable para tu altura, en pies, pulgadas y libras.",
  body="""<h2>La fórmula del IMC</h2>
<p><strong>IMC = 703 × peso (lb) ÷ altura (pulgadas)²</strong>. Una persona de 5 pies 7 pulgadas (67 pulgadas) que pesa 160 libras tiene un IMC de 703 × 160 ÷ 4.489 = <strong>25,1</strong>. En el sistema métrico es peso (kg) ÷ altura (m)².</p>
<h2>Categorías de IMC en adultos</h2>
<ul><li>Menos de 18,5: bajo peso</li><li>De 18,5 a 24,9: peso saludable</li><li>De 25 a 29,9: sobrepeso</li><li>30 o más: obesidad</li></ul>
<p>Son las categorías que usan los CDC y la Organización Mundial de la Salud para mayores de 20 años. En chicos y adolescentes se usan percentiles según la edad.</p>
<h2>Lo que el IMC no dice</h2>
<p>El IMC es un número rápido de referencia, no un diagnóstico. No separa músculo de grasa (los deportistas pueden salir con "sobrepeso") y no muestra dónde se acumula la grasa. La medida de la cintura, la presión, los análisis y tu médico dan una idea más completa.</p>""",
  faq=[("¿Qué IMC es saludable?","En adultos, entre 18,5 y 24,9."),
       ("¿El IMC sirve para mujeres, mayores y deportistas?","Usa la misma fórmula para todos, pero puede marcar de más en personas musculosas y de menos en mayores que perdieron músculo. Úsalo como punto de partida."),
       ("¿Esto es consejo médico?","No. Es una herramienta informativa. Habla con un médico o un nutricionista sobre tu salud y tu peso.")])),

# ---------------------------------------------------------------- CALORIES
dict(id="calorie", cat="health", aff="money",
 inputs=[S("sex","Sex","Sexo",[("f","Female","Mujer"),("m","Male","Hombre")],"f"),
         N("age","Age","Edad",35,"1","","15"),
         N("ft","Height (feet)","Altura (pies)",5,"1"),
         N("inch","Height (inches)","Altura (pulgadas)",5,"0.5"),
         N("lb","Weight (pounds)","Peso (libras)",150,"0.5"),
         S("activity","Activity level","Nivel de actividad",[("1.2","Sedentary (little or no exercise)","Sedentario (poco o nada de ejercicio)"),
           ("1.375","Light (exercise 1–3 days a week)","Liviano (ejercicio 1 a 3 días por semana)"),("1.55","Moderate (exercise 3–5 days a week)","Moderado (ejercicio 3 a 5 días por semana)"),
           ("1.725","Active (hard exercise 6–7 days a week)","Activo (ejercicio fuerte 6 a 7 días)"),("1.9","Very active (physical job plus training)","Muy activo (trabajo físico y entrenamiento)")],"1.375")],
 outputs=[O("tdee","Calories to maintain your weight","Calorías para mantener el peso",True),O("lose05","Lose about 0.5 lb a week","Bajar unas 0,5 lb por semana"),
          O("lose1","Lose about 1 lb a week","Bajar unas 1 lb por semana"),O("gain","Gain about 0.5 lb a week","Subir unas 0,5 lb por semana"),O("bmr","Resting calories (BMR)","Calorías en reposo (metabolismo basal)")],
 related=["bmi","age","cooking"],
 en=dict(slug="calorie-calculator", title="Calorie Calculator: How Many Calories Do I Need a Day?",
  h1="Calorie Calculator", desc="Free calorie calculator (TDEE). Estimate the calories you need a day to maintain, lose or gain weight, based on age, sex, height, weight and activity.",
  intro="Estimate how many calories you burn a day and how many to eat to keep, lose or gain weight.",
  body="""<h2>How the calories are estimated</h2>
<p>First the calculator finds your basal metabolic rate (BMR), the energy your body uses at rest, with the <strong>Mifflin-St Jeor equation</strong>, one of the most accurate for most adults:</p>
<ul><li>Men: 10 × weight (kg) + 6.25 × height (cm) − 5 × age + 5</li>
<li>Women: 10 × weight (kg) + 6.25 × height (cm) − 5 × age − 161</li></ul>
<p>Then it multiplies the BMR by an activity factor (1.2 for sedentary up to 1.9 for very active) to get your total daily energy expenditure, or TDEE: the calories that keep your weight stable.</p>
<h2>Losing or gaining weight</h2>
<p>About 500 calories a day under your TDEE leads to roughly 1 pound a week of weight loss for many people; 250 calories gives about half a pound. Real results vary. The calculator never suggests going below 1,200 calories a day for women or 1,500 for men without medical supervision.</p>
<h2>Tips</h2>
<ul><li>Track for two or three weeks and adjust: if your weight does not move, change the number by 100–200 calories.</li>
<li>Protein, fiber and vegetables help you feel full on fewer calories.</li>
<li>Pregnant or breastfeeding? Your needs are different; ask your doctor.</li></ul>""",
  faq=[("What is TDEE?","Total daily energy expenditure: the calories you burn in a day including rest, digestion and activity."),
       ("How accurate is this calorie calculator?","Formulas like Mifflin-St Jeor are usually within about 10% for most people. Use the result as a starting point and adjust with real results."),
       ("Is this medical advice?","No. It is for information only. Talk to a doctor or registered dietitian before starting a diet, especially if you have a health condition.")]),
 es=dict(slug="calculadora-de-calorias", title="Calculadora de calorías: cuántas calorías necesito por día",
  h1="Calculadora de calorías", desc="Calculadora de calorías gratis. Estima las calorías que necesitas por día para mantener, bajar o subir de peso según tu edad, sexo, altura, peso y actividad.",
  intro="Estima cuántas calorías gastas por día y cuántas comer para mantener, bajar o subir de peso.",
  body="""<h2>Cómo se calculan las calorías</h2>
<p>Primero la calculadora saca tu metabolismo basal (BMR), la energía que usa el cuerpo en reposo, con la <strong>ecuación de Mifflin-St Jeor</strong>, una de las más precisas para la mayoría de los adultos:</p>
<ul><li>Hombres: 10 × peso (kg) + 6,25 × altura (cm) − 5 × edad + 5</li>
<li>Mujeres: 10 × peso (kg) + 6,25 × altura (cm) − 5 × edad − 161</li></ul>
<p>Después multiplica el BMR por un factor de actividad (1,2 si eres sedentario hasta 1,9 si eres muy activo) y da tu gasto total por día (TDEE): las calorías que mantienen tu peso.</p>
<h2>Bajar o subir de peso</h2>
<p>Comer unas 500 calorías por día menos que tu TDEE suele llevar a bajar cerca de 1 libra (450 g) por semana; 250 calorías, media libra. Los resultados reales cambian según la persona. La calculadora nunca sugiere bajar de 1.200 calorías por día en mujeres o 1.500 en hombres sin control médico.</p>
<h2>Consejos</h2>
<ul><li>Anota lo que comes dos o tres semanas y ajusta: si el peso no se mueve, cambia el número en 100 a 200 calorías.</li>
<li>Las proteínas, la fibra y las verduras ayudan a quedar satisfecho con menos calorías.</li>
<li>¿Embarazada o amamantando? Necesitas otra cantidad; consulta a tu médico.</li></ul>""",
  faq=[("¿Qué es el TDEE?","El gasto total de energía por día: las calorías que quemas en reposo, al digerir y al moverte."),
       ("¿Qué tan exacta es esta calculadora?","Las fórmulas como Mifflin-St Jeor suelen acertar con un margen de un 10% para la mayoría. Úsala como punto de partida y ajusta con tus resultados."),
       ("¿Esto es consejo médico?","No. Es solo informativo. Habla con un médico o un nutricionista antes de empezar una dieta, sobre todo si tienes algún problema de salud.")])),

# ---------------------------------------------------------------- GPA
dict(id="gpa", cat="school", aff="money",
 inputs=[TA("list","One class per line: grade and credits","Una materia por línea: nota y créditos",
            "English, A, 3\nAlgebra, B+, 4\nBiology, A-, 4\nHistory, B, 3\nArt, A, 1",
            "Inglés, A, 3\nÁlgebra, B+, 4\nBiología, A-, 4\nHistoria, B, 3\nArte, A, 1"),
         N("prevgpa","Current cumulative GPA (optional)","GPA acumulado actual (opcional)",0,"0.01"),
         N("prevcr","Credits already completed (optional)","Créditos ya aprobados (opcional)",0,"1")],
 outputs=[O("gpa","GPA for these classes","GPA de estas materias",True),O("cum","New cumulative GPA","Nuevo GPA acumulado"),O("credits","Credits counted","Créditos contados")],
 related=["finalgrade","percent","age"],
 en=dict(slug="gpa-calculator", title="GPA Calculator: Semester and Cumulative GPA (4.0 Scale)",
  h1="GPA Calculator", desc="Free GPA calculator for high school and college. Enter letter grades and credits to get your semester GPA on a 4.0 scale and your new cumulative GPA.",
  intro="Work out your semester GPA from letter grades and credits, and see how it changes your cumulative GPA.",
  body="""<h2>How GPA is calculated</h2>
<p>Each letter grade is worth grade points (A = 4.0, B = 3.0, C = 2.0, D = 1.0, F = 0). Multiply the points by the credits of the class, add everything up and divide by the total credits. That is a weighted average: a 4-credit class counts more than a 1-credit class.</p>
<h2>Grade points used</h2>
<p>A+ and A = 4.0 · A− = 3.7 · B+ = 3.3 · B = 3.0 · B− = 2.7 · C+ = 2.3 · C = 2.0 · C− = 1.7 · D+ = 1.3 · D = 1.0 · D− = 0.7 · F = 0. Some schools give 4.3 for an A+ or use other values; you can also type the number of points instead of the letter (for example "3.5, 3").</p>
<h2>Cumulative GPA</h2>
<p>To combine with past semesters, enter your current cumulative GPA and the credits you already have. The calculator weighs the old and new credits together.</p>
<h2>Weighted GPA</h2>
<p>Many high schools add 0.5 or 1 point for honors, AP or IB classes. If yours does, type the boosted number (for example 5.0 for an A in an AP class) instead of the letter.</p>""",
  faq=[("What is a good GPA?","A 3.0 (B average) is the minimum for many scholarships and programs; 3.5 and above is considered strong for competitive colleges."),
       ("How do I write each line?","Course name (optional), grade and credits separated by commas, for example 'Chemistry, B+, 4'. A line like 'A 3' also works."),
       ("Do pass/fail classes count?","Usually not. Leave them out unless your school says otherwise.")]),
 es=dict(slug="calculadora-de-gpa", title="Calculadora de GPA: promedio del semestre y acumulado (escala 4.0)",
  h1="Calculadora de GPA", desc="Calculadora de GPA gratis para high school y universidad. Pon las notas en letras y los créditos y mira el GPA del semestre en escala de 4.0 y el acumulado.",
  intro="Saca tu GPA del semestre con las notas en letras y los créditos, y mira cómo cambia tu GPA acumulado.",
  body="""<h2>Cómo se calcula el GPA</h2>
<p>En EE. UU. cada nota en letras vale puntos (A = 4,0, B = 3,0, C = 2,0, D = 1,0, F = 0). Se multiplican los puntos por los créditos de cada materia, se suma todo y se divide por el total de créditos. Es un promedio ponderado: una materia de 4 créditos pesa más que una de 1.</p>
<h2>Puntos que usa la calculadora</h2>
<p>A+ y A = 4,0 · A− = 3,7 · B+ = 3,3 · B = 3,0 · B− = 2,7 · C+ = 2,3 · C = 2,0 · C− = 1,7 · D+ = 1,3 · D = 1,0 · D− = 0,7 · F = 0. Algunas escuelas dan 4,3 por una A+ o usan otros valores; también puedes escribir los puntos en vez de la letra (por ejemplo "3.5, 3").</p>
<h2>GPA acumulado</h2>
<p>Para sumar los semestres anteriores, pon tu GPA acumulado actual y los créditos que ya tienes. La calculadora combina los créditos viejos y los nuevos.</p>
<h2>GPA ponderado</h2>
<p>Muchas high schools suman 0,5 o 1 punto en materias honors, AP o IB. Si la tuya lo hace, escribe el número con el extra (por ejemplo 5.0 por una A en una materia AP) en vez de la letra.</p>""",
  faq=[("¿Qué GPA es bueno?","Un 3,0 (promedio B) es el mínimo para muchas becas y programas; 3,5 o más se considera fuerte para universidades competitivas."),
       ("¿Cómo escribo cada línea?","Nombre de la materia (opcional), nota y créditos separados por comas, por ejemplo 'Química, B+, 4'. Una línea como 'A 3' también sirve."),
       ("¿Las materias pass/fail cuentan?","En general no. Déjalas afuera salvo que tu escuela diga otra cosa.")])),

# ---------------------------------------------------------------- FINAL GRADE
dict(id="finalgrade", cat="school", aff="money",
 inputs=[N("current","Current grade in the class","Nota actual en la materia",85,"0.1","%"),
         N("want","Grade you want at the end","Nota que quieres al final",90,"0.1","%"),
         N("weight","Weight of the final exam","Peso del examen final",25,"1","%")],
 presets=("want",[70,80,90]),
 outputs=[O("need","You need on the final","Necesitas en el final",True),O("note","Is it possible?","¿Se puede?"),
          O("ifzero","Final grade if you get 0","Nota final si sacas 0"),O("ifhundred","Final grade if you get 100","Nota final si sacas 100")],
 related=["gpa","percent","datediff"],
 en=dict(slug="final-grade-calculator", title="Final Grade Calculator: What Do I Need on My Final?",
  h1="Final Grade Calculator", desc="Find out what score you need on your final exam to get the class grade you want. Enter your current grade, your goal and how much the final is worth.",
  intro="Find out exactly what you need on the final exam to finish the class with the grade you want.",
  body="""<h2>The formula</h2>
<p><strong>Needed = (goal − current × (1 − weight)) ÷ weight</strong>, with the weight as a decimal. With an 85% now, a 90% goal and a final worth 25%: (90 − 85 × 0.75) ÷ 0.25 = <strong>105%</strong>. Without extra credit that A is out of reach, but an 80% (B−) is easy: you need 65%.</p>
<h2>Where to find the weight of the final</h2>
<p>Look at the syllabus: it lists how much homework, quizzes, tests and the final count. If your "current grade" in the online gradebook already includes everything except the final, use it as is.</p>
<h2>Letter grade cut-offs</h2>
<p>The most common scale in the US is A = 90–100, B = 80–89, C = 70–79, D = 60–69 and F = below 60, but some schools use a 7-point scale or plus and minus grades. Use the cut-off your teacher uses as your goal.</p>""",
  faq=[("What if I need more than 100%?","The goal is not reachable with the final alone. Ask your teacher about extra credit or aim for the next grade down."),
       ("How much will the final change my grade?","The 'if you get 0' and 'if you get 100' lines show the lowest and highest grades you can end with."),
       ("Does this work for weighted categories?","Yes, as long as your current grade is the weighted grade for everything except the final.")]),
 es=dict(slug="calculadora-nota-final", title="Calculadora de nota final: cuánto necesito en el examen final",
  h1="Calculadora de nota final", desc="Calcula qué nota necesitas en el examen final para terminar la materia con la nota que quieres. Pon tu nota actual, tu meta y cuánto vale el final.",
  intro="Mira exactamente qué necesitas en el examen final para terminar la materia con la nota que quieres.",
  body="""<h2>La fórmula</h2>
<p><strong>Necesitas = (meta − nota actual × (1 − peso)) ÷ peso</strong>, con el peso en decimal. Con 85% ahora, meta de 90% y un final que vale 25%: (90 − 85 × 0,75) ÷ 0,25 = <strong>105%</strong>. Sin puntos extra esa A no alcanza, pero un 80% (B−) es fácil: necesitas 65%.</p>
<h2>Dónde ver cuánto vale el final</h2>
<p>Fíjate en el syllabus: ahí dice cuánto cuentan las tareas, los quizzes, las pruebas y el final. Si tu nota actual en el sistema de la escuela ya incluye todo menos el final, úsala tal cual.</p>
<h2>Las notas en letras</h2>
<p>La escala más común en EE. UU. es A = 90–100, B = 80–89, C = 70–79, D = 60–69 y F = menos de 60, pero algunas escuelas usan otra escala o notas con más y menos. Pon como meta el corte que use tu profesor.</p>""",
  faq=[("¿Y si necesito más de 100%?","No se llega solo con el final. Pregunta al profesor por puntos extra o apunta a la nota anterior."),
       ("¿Cuánto me puede cambiar el final?","Las líneas 'si sacas 0' y 'si sacas 100' muestran la nota más baja y la más alta con las que puedes terminar."),
       ("¿Sirve si las categorías tienen distinto peso?","Sí, siempre que tu nota actual sea la nota ponderada de todo menos el final.")])),
]
