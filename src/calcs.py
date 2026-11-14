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

def O(key, en, es, big=False, pre=False):
    return dict(key=key, en=en, es=es, big=big, pre=pre)

YESNO = [("yes", "Yes", "Sí"), ("no", "No", "No")]

CATS = {
    "restaurant": ("Restaurant & tips", "Restaurante y propinas"),
    "kitchen": ("Kitchen & recipes", "Cocina y recetas"),
    "work": ("Work & pay", "Trabajo y sueldo"),
    "money": ("Budget & money", "Presupuesto y dinero"),
    "everyday": ("Everyday math", "Cuentas de todos los días"),
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
]
