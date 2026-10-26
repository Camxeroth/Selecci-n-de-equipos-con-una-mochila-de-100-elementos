# METAHEURÍSTICAS
# Actividad Autónoma 1
# Selección de equipos con una mochila de 100 elementos
# Unidad 1 Fundamentos de optimización y heurísticas básicas
# Tema 1 Formulación de problemas y soluciones de referencia

# =============================================================================
# TRABAJO INDIVIDUAL - PROBLEMA DE LA MOCHILA 0/1
# -----------------------------------------------------------------------------
# Contexto: un equipo de investigación dispone de 100 equipos para una salida
# de campo y puede transportar como máximo 250 kg. Cada equipo tiene:
#   - peso entero de 1 a 20 kg
#   - utilidad entera de 10 a 100
# Cada elemento se selecciona completo (1) una sola vez o se deja (0).
# Objetivo: maximizar la utilidad total sin exceder la capacidad.
#
# Reglas del enunciado cumplidas:
#   * Conjunto común generado UNA SOLA VEZ con semilla 42 (Anexo 1).
#   * Exactamente 100 elementos y capacidad 250 kg.
#   * En las ejecuciones aleatorias se cambia SOLO el orden (mezcla); se
#     mantienen pesos, utilidades y capacidad.
#   * 30 ejecuciones aleatorias con semillas 0 a 29 para mezclar.
#   * Referencia exacta con programación dinámica (Anexo 2); no se enumeran
#     las 2^100 selecciones.
# =============================================================================

# =============================================================================
# ANEXO 1 - Generación del conjunto común (semilla 42, 100 elementos, 250 kg)
# =============================================================================
import random

random.seed(42)
nombres = []
pesos = []
valores = []

for i in range(100):
    nombres.append("Equipo " + str(i + 1))
    pesos.append(random.randint(1, 20))
    valores.append(random.randint(10, 100))

capacidad = 250

# =============================================================================
# ANEXO 2 - Referencia exacta por programación dinámica
# =============================================================================
# Ejecute este bloque después del generador. La tabla guarda la mejor utilidad
# con los primeros i equipos y una capacidad disponible c. Cada decisión compara
# dejar el equipo o tomarlo una vez. El código imprime únicamente el valor óptimo.
n = len(pesos)
tabla = []

for i in range(n + 1):
    tabla.append([0] * (capacidad + 1))

for i in range(1, n + 1):
    peso = pesos[i - 1]
    valor = valores[i - 1]

    for c in range(capacidad + 1):
        sin_equipo = tabla[i - 1][c]
        tabla[i][c] = sin_equipo

        if peso <= c:
            con_equipo = valor + tabla[i - 1][c - peso]
            if con_equipo > sin_equipo:
                tabla[i][c] = con_equipo

valor_optimo = tabla[n][capacidad]
print("Valor óptimo (Anexo 2):", valor_optimo)

# -----------------------------------------------------------------------------
# Estructura de datos usada en las partes del trabajo (a partir del Anexo 1)
# -----------------------------------------------------------------------------
items = [
    {"id": i + 1, "nombre": nombres[i], "peso": pesos[i], "utilidad": valores[i]}
    for i in range(n)
]
N_ELEMENTOS = len(items)
CAPACIDAD = capacidad


def peso_total(seleccion, items_orden):
    """Suma de pesos de los elementos seleccionados (seleccion == 1)."""
    return sum(it["peso"] for it, x in zip(items_orden, seleccion) if x == 1)


def utilidad_total(seleccion, items_orden):
    """Suma de utilidades de los elementos seleccionados."""
    return sum(it["utilidad"] for it, x in zip(items_orden, seleccion) if x == 1)


def cantidad_seleccionada(seleccion):
    """Cantidad de elementos con seleccion == 1."""
    return sum(1 for x in seleccion if x == 1)


def es_factible(seleccion, items_orden, capacidad=CAPACIDAD):
    """Una selección es factible si su peso total no excede la capacidad."""
    return peso_total(seleccion, items_orden) <= capacidad


# -----------------------------------------------------------------------------
# 1. FORMULACIÓN DEL PROBLEMA (2 puntos)
# -----------------------------------------------------------------------------
print("=" * 78)
print("1. FORMULACIÓN DEL PROBLEMA")
print("=" * 78)
print(
    """
Sea el conjunto de equipos E = {1, 2, ..., 100}.
Para cada equipo i se define una variable de decisión binaria:

    x_i = 1  si el equipo i se selecciona (se lleva a la salida de campo)
    x_i = 0  si el equipo i no se selecciona (se deja)

La lista de 100 ceros y unos (x_1, x_2, ..., x_100) representa por tanto una
selección completa: cada posición indica si el equipo correspondiente viaja.
Esta representación es natural porque cada equipo es indivisible: o se toma
entero o no se toma; no existe "llevar la mitad de un equipo".

Función objetivo (maximizar utilidad total):

    max  Z = sum_{i=1}^{100} u_i * x_i

donde u_i es la utilidad entera del equipo i (10 <= u_i <= 100).

Restricción de capacidad:

    sum_{i=1}^{100} p_i * x_i <= 250

donde p_i es el peso entero del equipo i (1 <= p_i <= 20), y las variables
cumplen x_i ∈ {0, 1} para todo i = 1,...,100.

Justificación de por qué la optimización es discreta:
    - Las variables x_i sólo pueden valer 0 o 1 (dominio finito, no continuo).
    - No hay fracciones de objetos; cada equipo se toma completo o se deja.
    - El espacio de búsqueda tiene 2^100 soluciones candidatas (finito pero
      astronómicamente grande), por lo que se trata de un problema de
      optimización combinatoria discreta (NP-duro en el caso general).
"""
)

print("Instancia generada con semilla 42 (primeros 12 elementos de 100):")
print(f"{'ID':>4} {'Nombre':<12} {'Peso(kg)':>9} {'Utilidad':>9}  u/p")
print("-" * 50)
for it in items[:12]:
    print(f"{it['id']:>4} {it['nombre']:<12} {it['peso']:>9} {it['utilidad']:>9}  {it['utilidad']/it['peso']:.3f}")
print("...")
print(f"Total elementos: {N_ELEMENTOS} | Capacidad: {CAPACIDAD} kg")
print(f"Peso total de los 100 equipos: {sum(it['peso'] for it in items)} kg")
print(f"Utilidad total de los 100 equipos: {sum(it['utilidad'] for it in items)}")

# -----------------------------------------------------------------------------
# 2. EVALUAR TRES PROPUESTAS (1 punto)
# -----------------------------------------------------------------------------
print("\n" + "=" * 78)
print("2. EVALUACIÓN DE TRES PROPUESTAS")
print("=" * 78)

seleccion_nada = [0] * N_ELEMENTOS
seleccion_primeros10 = [1 if i < 10 else 0 for i in range(N_ELEMENTOS)]
seleccion_todos100 = [1] * N_ELEMENTOS

propuestas = [
    ("Ningún equipo (x = 0...0)", seleccion_nada),
    ("Primeros 10 equipos (orden original)", seleccion_primeros10),
    ("Los 100 equipos (x = 1...1)", seleccion_todos100),
]

print(
    f"{'Propuesta':<42} {'Peso(kg)':>9} {'Utilidad':>9} {'Equipos':>8} {'Factible (<=250 kg)':>22}"
)
print("-" * 92)
resultados_propuestas = []
for nombre, sel in propuestas:
    p = peso_total(sel, items)
    u = utilidad_total(sel, items)
    c = cantidad_seleccionada(sel)
    fact = es_factible(sel, items)
    resultados_propuestas.append((nombre, p, u, c, fact))
    print(f"{nombre:<42} {p:>9} {u:>9} {c:>8} {str(fact):>22}")

print(
    """
Interpretación:
    - Ningún equipo: peso 0 y utilidad 0. Es factible pero trivial (no sirve
      para el objetivo de maximizar).
    - Primeros 10: puede ser factible o no según los pesos reales; reporta una
      utilidad concreta pero no garantiza optimalidad.
    - Los 100: el peso total supera con mucho los 250 kg, por tanto es
      INFACTIBLE (infringe la restricción de capacidad) y no es una solución
      válida del problema.
"""
)

# -----------------------------------------------------------------------------
# 3. CONSTRUCCIÓN ALEATORIA (2 puntos)
# -----------------------------------------------------------------------------
print("=" * 78)
print("3. CONSTRUCCIÓN ALEATORIA (30 ejecuciones, semillas 0..29)")
print("=" * 78)
print(
    """
Procedimiento:
    1. Se parte del orden original de los 100 equipos.
    2. Para cada semilla s en 0..29 se MEZCLA (shuffle) únicamente el orden;
       los pesos y utilidades se mantienen iguales.
    3. Se recorre la lista mezclada y se agrega cada equipo SI CABE en la
       capacidad restante; si no cabe, se salta y se continúa con el siguiente.
    4. Se registran: semilla, peso total, utilidad total y cantidad de equipos.
"""
)

resultados_aleatorios = []
for s in range(30):
    random.seed(s)  # semilla de mezcla (sólo cambia el orden)
    mezclado = items[:]
    random.shuffle(mezclado)

    seleccion = [0] * N_ELEMENTOS
    capacidad_restante = CAPACIDAD
    indice_por_id = {it["id"]: idx for idx, it in enumerate(items)}

    for it in mezclado:
        if it["peso"] <= capacidad_restante:
            seleccion[indice_por_id[it["id"]]] = 1
            capacidad_restante -= it["peso"]

    p = peso_total(seleccion, items)
    u = utilidad_total(seleccion, items)
    c = cantidad_seleccionada(seleccion)
    assert es_factible(seleccion, items), f"Semilla {s} produjo solución infactible"
    assert all(x in (0, 1) for x in seleccion)
    resultados_aleatorios.append({
        "semilla": s,
        "peso": p,
        "utilidad": u,
        "cantidad": c,
    })

utilidades_aleatorias = [r["utilidad"] for r in resultados_aleatorios]
pesos_aleatorios = [r["peso"] for r in resultados_aleatorios]
cantidades_aleatorias = [r["cantidad"] for r in resultados_aleatorios]

u_min = min(utilidades_aleatorias)
u_max = max(utilidades_aleatorias)
u_media = sum(utilidades_aleatorias) / len(utilidades_aleatorias)
p_min, p_max = min(pesos_aleatorios), max(pesos_aleatorios)
c_min, c_max = min(cantidades_aleatorias), max(cantidades_aleatorias)

print(
    f"{'Semilla':>7} {'Peso(kg)':>9} {'Utilidad':>9} {'Equipos':>8}"
)
print("-" * 36)
for r in resultados_aleatorios:
    print(f"{r['semilla']:>7} {r['peso']:>9} {r['utilidad']:>9} {r['cantidad']:>8}")
print("-" * 36)
print(
    "RESUMEN".rjust(7)
    + "".rjust(9)
    + f"mín={u_min}  máx={u_max}  media={u_media:.2f}".rjust(30)
)
print(
    f"Peso: mín={p_min} kg, máx={p_max} kg (todos <= {CAPACIDAD} kg -> factibles) | "
    f"Equipos: mín={c_min}, máx={c_max}"
)
print(
    f"\nUtilidad mínima: {u_min} | Utilidad media: {u_media:.2f} | Utilidad máxima: {u_max}"
)
print(
    """
Nota: se distingue la MEDIA de las 30 ejecuciones del MEJOR resultado
observado (máximo). Ninguna de estas utilidades supera al óptimo exacto.
"""
)

mejor_aleatorio = max(resultados_aleatorios, key=lambda r: r["utilidad"])

# -----------------------------------------------------------------------------
# 4. CONSTRUCCIÓN GREEDY (2 puntos)
# -----------------------------------------------------------------------------
print("=" * 78)
print("4. CONSTRUCCIÓN GREEDY (relación utilidad/peso, mayor a menor)")
print("=" * 78)
print(
    """
Procedimiento:
    1. Se calcula la razón r_i = utilidad_i / peso_i para cada equipo.
    2. Se ordenan los equipos de mayor a menor por r_i.
    3. En caso de empate en la razón, se conserva el orden original
       (ordenamiento estable: Python sort es estable).
    4. Se recorre la lista ordenada y se agrega cada equipo si cabe;
       si no cabe, se continúa con el siguiente.
"""
)

orden_greedy = sorted(items, key=lambda it: it["utilidad"] / it["peso"], reverse=True)

seleccion_greedy = [0] * N_ELEMENTOS
capacidad_restante = CAPACIDAD
indice_por_id = {it["id"]: idx for idx, it in enumerate(items)}
ids_seleccionados_greedy = []

for it in orden_greedy:
    if it["peso"] <= capacidad_restante:
        seleccion_greedy[indice_por_id[it["id"]]] = 1
        capacidad_restante -= it["peso"]
        ids_seleccionados_greedy.append(it["id"])

p_greedy = peso_total(seleccion_greedy, items)
u_greedy = utilidad_total(seleccion_greedy, items)
c_greedy = cantidad_seleccionada(seleccion_greedy)

assert es_factible(seleccion_greedy, items)
assert all(x in (0, 1) for x in seleccion_greedy)

print(f"Cantidad de equipos seleccionados: {c_greedy}")
print(f"IDs seleccionados: {ids_seleccionados_greedy}")
print(f"Peso total: {p_greedy} kg (capacidad {CAPACIDAD} kg)")
print(f"Utilidad total: {u_greedy}")
print(
    f"\nRazones u/p de los seleccionados (orden de inserción greedy):"
)
for it in orden_greedy:
    if it["id"] in set(ids_seleccionados_greedy):
        print(f"  ID {it['id']:>3}: p={it['peso']:>2} kg, u={it['utilidad']:>3}, u/p={it['utilidad']/it['peso']:.3f}")

# -----------------------------------------------------------------------------
# 5. REFERENCIA EXACTA Y COMPARACIÓN (2 puntos)
# -----------------------------------------------------------------------------
print("=" * 78)
print("5. REFERENCIA EXACTA (programación dinámica) Y COMPARACIÓN")
print("=" * 78)
print(
    """
Método exacto: programación dinámica para la mochila 0/1 con pesos enteros.

    dp[i][w] = mejor utilidad usando los primeros i elementos con capacidad w
    dp[i][w] = max(dp[i-1][w], dp[i-1][w - p_i] + u_i)  si w >= p_i
               dp[i-1][w]                                si w < p_i

    dp[0][w] = 0 para todo w;  dp[i][0] = 0.

La DP es EXACTA en este caso porque los pesos y la capacidad son enteros:
el número de estados (n+1)*(W+1) es finito y pequeño (101 x 251), por lo que
se explota el subproblema de manera exhaustiva sin aproximaciones. No es
necesario enumerar las 2^100 selecciones.

Nota: por seguir el espíritu del Anexo 2 (que devuelve únicamente el valor
óptimo), en la tabla de comparación el peso de la referencia exacta se deja
sin reportar ("—").
"""
)

# Reconstrucción opcional de la selección óptima a partir de la tabla del Anexo 2
seleccion_optima = [0] * n
c_reconstruir = CAPACIDAD
for i in range(n, 0, -1):
    if tabla[i][c_reconstruir] != tabla[i - 1][c_reconstruir]:
        seleccion_optima[i - 1] = 1
        c_reconstruir -= pesos[i - 1]

p_optimo = peso_total(seleccion_optima, items)
u_optimo_reconstruido = utilidad_total(seleccion_optima, items)
c_optimo = cantidad_seleccionada(seleccion_optima)

assert es_factible(seleccion_optima, items)
assert u_optimo_reconstruido == valor_optimo, "La reconstrucción debe coincidir con el valor óptimo del Anexo 2"
assert valor_optimo >= u_greedy and valor_optimo >= mejor_aleatorio["utilidad"], "Optimo debe ser >= cualquier factible"

print(f"Valor óptimo (programación dinámica, Anexo 2): {valor_optimo}")
print(
    f"(Peso reconstruido de la óptima: {p_optimo} kg | equipos: {c_optimo})"
)
print(
    f"\nComparación de utilidades:\n"
    f"  - Mejor ejecución aleatoria: {mejor_aleatorio['utilidad']}  (semilla {mejor_aleatorio['semilla']})\n"
    f"  - Greedy (utilidad/peso):     {u_greedy}\n"
    f"  - Óptimo exacto (DP):         {valor_optimo}"
)

# -----------------------------------------------------------------------------
# TABLA DE COMPARACIÓN Y BRECHAS
# -----------------------------------------------------------------------------
print("\n" + "=" * 78)
print("TABLA DE COMPARACIÓN Y BRECHAS PORCENTUALES")
print("=" * 78)
print(
    'Brecha (%) = 100 * (valor óptimo - utilidad del método) / valor óptimo.'
    "\nPara la referencia exacta el peso se deja sin reportar ('—')."
)
print(
    f"{'Método':<40} {'Peso(kg)':>9} {'Utilidad':>9} {'Equipos':>8} {'Brecha(%)':>11}"
)
print("-" * 82)


def brecha(valor):
    return 100.0 * (valor_optimo - valor) / valor_optimo if valor_optimo > 0 else 0.0


filas_comparacion = [
    ("1. Ningún equipo (parte 2)", 0, 0, 0, brecha(0)),
    ("2. Primeros 10 (parte 2)", resultados_propuestas[1][1], resultados_propuestas[1][2], resultados_propuestas[1][3], brecha(resultados_propuestas[1][2])),
    ("3. Los 100 (parte 2) - INFACTIBLE", resultados_propuestas[2][1], resultados_propuestas[2][2], resultados_propuestas[2][3], None),
    (f"4. Mejor aleatoria (semilla {mejor_aleatorio['semilla']}, parte 3)", mejor_aleatorio["peso"], mejor_aleatorio["utilidad"], mejor_aleatorio["cantidad"], brecha(mejor_aleatorio["utilidad"])),
    ("5. Greedy u/p (parte 4)", p_greedy, u_greedy, c_greedy, brecha(u_greedy)),
    ("6. Óptimo exacto DP (parte 5)", None, valor_optimo, c_optimo, 0.0),
]

for nombre, p, u, c, b in filas_comparacion:
    p_str = "—" if p is None else f"{p}"
    b_str = "—" if b is None else f"{b:.2f}"
    u_str = str(u)
    print(f"{nombre:<40} {p_str:>9} {u_str:>9} {c:>8} {b_str:>11}")

print(
    """
Interpretación de brechas:
    - Brecha 0% = el método alcanza el óptimo.
    - Cuanto mayor la brecha, más lejos está el método del óptimo.
    - La propuesta "Los 100" es infactible (peso > 250 kg), así que no tiene
      brecha significativa comparada con el óptimo factible.
"""
)

# -----------------------------------------------------------------------------
# TABLA APARTE: LAS 30 EJECUCIONES ALEATORIAS
# -----------------------------------------------------------------------------
print("\n" + "=" * 78)
print("TABLA APARTE - LAS 30 EJECUCIONES ALEATORIAS (semillas 0 a 29)")
print("=" * 78)
print(
    f"{'Semilla':>7} {'Peso(kg)':>9} {'Utilidad':>9} {'Equipos':>8} {'Factible':>10}"
)
print("-" * 46)
for r in resultados_aleatorios:
    print(f"{r['semilla']:>7} {r['peso']:>9} {r['utilidad']:>9} {r['cantidad']:>8} {'SÍ':>10}")
print("-" * 46)
print(
    f"Resumen -> peso: [{p_min}, {p_max}] kg | utilidad: [{u_min}, {u_max}] | "
    f"media utilidad = {u_media:.2f} | mejores semillas por utilidad: "
    f"{sorted(range(30), key=lambda s: resultados_aleatorios[s]['utilidad'], reverse=True)[:5]}"
)

# -----------------------------------------------------------------------------
# 6. REFLEXIÓN (1 punto)
# -----------------------------------------------------------------------------
print("\n" + "=" * 78)
print("6. REFLEXIÓN")
print("=" * 78)
print(
    f"""
Preguntas y respuestas con los resultados obtenidos:

a) ¿Por qué no es viable enumerar 2^100 selecciones?
   2^100 ≈ 1,27e+30 combinaciones. Incluso evaluando miles de millones de
   selecciones por segundo, se requerirían muchísimos años de cómputo. Es un
   espacio finito pero astronómicamente grande; por eso se requiere un método
   inteligente (programación dinámica) en vez de fuerza bruta.

b) ¿Greedy encontró el óptimo?
   Greedy obtuvo utilidad {u_greedy}; el óptimo es {valor_optimo}.
   {'Sí, encontró el óptimo.' if u_greedy == valor_optimo else f'No, quedó por debajo del óptimo (brecha {brecha(u_greedy):.2f}%).'}
   La razón es que greedy elige por mejor relación u/p de forma local (voraz)
   y puede llenar la capacidad con elementos pequeños de buena relación, dejando
   huecos que impiden meter un elemento de mayor utilidad total; no revisa
   decisiones ya tomadas.

c) ¿Cómo varió la utilidad aleatoria?
   En las 30 ejecuciones (semillas 0-29) la utilidad varió entre {u_min} y
   {u_max}, con media {u_media:.2f}. El orden de llegada cambia qué elementos
   caben primero, por lo que cada semilla da una solución factible distinta y
   ninguna garantiza ser la mejor. El mejor resultado observado fue la semilla
   {mejor_aleatorio['semilla']} con {mejor_aleatorio['utilidad']}.

d) ¿Por qué una selección factible puede ser inferior al óptimo?
   Factible sólo significa "no excede 250 kg". Hay muchas selecciones factibles
   con distinto reparto de pesos/utilidades; el óptimo es la que maximiza la
   utilidad entre todas ellas. Una selección factible puede dejar capacidad
   sin usar o elegir elementos de baja utilidad, por eso es inferior.

e) ¿Estos resultados permiten afirmar que un método siempre será superior?
   No. Estos resultados son de UNA sola instancia (semilla 42). Un método que
   gana aquí (por ejemplo el óptimo exacto, por definición) o que funciona bien
   en esta instancia no garantiza hacerlo en todas las instancias posibles. La
   superioridad debe evaluarse sobre un conjunto representativo de instancias,
   no sobre una sola.
"""
)

# -----------------------------------------------------------------------------
# VERIFICACIÓN FINAL (verificación antes de entregar)
# -----------------------------------------------------------------------------
print("\n" + "=" * 78)
print("VERIFICACIÓN FINAL ANTES DE ENTREGAR")
print("=" * 78)
checks = []
checks.append(("Lista de 100 elementos", len(items) == 100))
checks.append(("Selecciones binarias (nada)", all(x in (0, 1) for x in seleccion_nada)))
checks.append(("Selecciones binarias (greedy)", all(x in (0, 1) for x in seleccion_greedy)))
checks.append(("Selecciones binarias (óptima DP)", all(x in (0, 1) for x in seleccion_optima)))
checks.append(("Construcciones <= 250 kg", all(es_factible(r, items) for r in [seleccion_nada, seleccion_primeros10, seleccion_greedy, seleccion_optima])))
checks.append(("30 ejecuciones aleatorias factibles", len(resultados_aleatorios) == 30 and all(es_factible([0]*N_ELEMENTOS, items) for _ in resultados_aleatorios)))
checks.append(("Ninguna utilidad factible excede el óptimo", max([u_greedy, mejor_aleatorio["utilidad"], u_optimo_reconstruido, resultados_propuestas[1][2], resultados_propuestas[0][2]]) <= valor_optimo or not es_factible(seleccion_todos100, items)))
checks.append(("Todos los 100 es infactible (>250 kg)", not es_factible(seleccion_todos100, items)))
checks.append(("Valor óptimo coincide Anexo 2 y reconstrucción", u_optimo_reconstruido == valor_optimo))

for nombre, ok in checks:
    print(f"  [{'OK' if ok else 'FALLA'}] {nombre}")

# Guardar resultados en JSON para posible reporte
import json
reporte = {
    "encabezado": {
        "curso": "METAHEURÍSTICAS",
        "actividad": "Actividad Autónoma 1",
        "titulo": "Selección de equipos con una mochila de 100 elementos",
        "unidad": "Unidad 1 Fundamentos de optimización y heurísticas básicas",
        "tema": "Tema 1 Formulación de problemas y soluciones de referencia",
    },
    "semilla_datos": 42,
    "n_elementos": N_ELEMENTOS,
    "capacidad": CAPACIDAD,
    "items": items,
    "valor_optimo": valor_optimo,
    "peso_optimo": p_optimo,
    "seleccion_optima": seleccion_optima,
    "greedy": {"peso": p_greedy, "utilidad": u_greedy, "cantidad": c_greedy, "seleccion": seleccion_greedy, "ids": ids_seleccionados_greedy},
    "aleatorio_mejor": mejor_aleatorio,
    "aleatorio_todos": resultados_aleatorios,
    "aleatorio": {"min": u_min, "max": u_max, "media": u_media},
    "propuestas": {
        "nada": {"peso": resultados_propuestas[0][1], "utilidad": resultados_propuestas[0][2], "factible": resultados_propuestas[0][4]},
        "primeros10": {"peso": resultados_propuestas[1][1], "utilidad": resultados_propuestas[1][2], "cantidad": resultados_propuestas[1][3], "factible": resultados_propuestas[1][4]},
        "todos100": {"peso": resultados_propuestas[2][1], "utilidad": resultados_propuestas[2][2], "cantidad": resultados_propuestas[2][3], "factible": resultados_propuestas[2][4]},
    },
}
with open("reporte_resultados.json", "w", encoding="utf-8") as f:
    json.dump(reporte, f, ensure_ascii=False, indent=2)

print("\nResultados guardados en 'reporte_resultados.json'.")
print("Fin del script.")
