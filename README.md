# Selección de equipos con una mochila de 100 elementos

**Curso:** Metaheurísticas
**Actividad:** Actividad Autónoma 1
**Unidad 1:** Fundamentos de optimización y heurísticas básicas
**Tema 1:** Formulación de problemas y soluciones de referencia

**Autor:** [Nombre del estudiante]
**Institución:** [Nombre de la institución]
**Fecha:** [Fecha de entrega]

---

## Resumen

Este repositorio contiene la resolución de una instancia del problema de la mochila 0/1 con 100 elementos y una capacidad de 250 kg. El escenario modela a un equipo de investigación que debe elegir, entre 100 equipos disponibles, cuáles transportar a una salida de campo sin exceder la capacidad máxima y maximizando la utilidad total. Se formula el problema como un modelo de optimización combinatoria discreta y se comparan cuatro enfoques de construcción de soluciones: selección trivial, construcción aleatoria, construcción voraz (greedy) por razón utilidad/peso y programación dinámica como referencia exacta. Los resultados se contrastan mediante la brecha porcentual respecto al óptimo.

## Tabla de contenidos

1. [Descripción del problema](#1-descripción-del-problema)
2. [Formulación matemática](#2-formulación-matemática)
3. [Generación de la instancia](#3-generación-de-la-instancia)
4. [Metodología](#4-metodología)
5. [Resultados](#5-resultados)
6. [Discusión](#6-discusión)
7. [Limitaciones](#7-limitaciones)
8. [Estructura del repositorio](#8-estructura-del-repositorio)
9. [Requisitos y ejecución](#9-requisitos-y-ejecución)
10. [Referencias](#10-referencias)
11. [Licencia](#11-licencia)

---

## 1. Descripción del problema

Un equipo de investigación dispone de 100 equipos para una salida de campo y puede transportar como máximo 250 kg. Cada equipo tiene un peso entero entre 1 y 20 kg y una utilidad entera entre 10 y 100. Cada equipo se selecciona completo una sola vez o se deja; no es posible tomar fracciones. El objetivo es maximizar la utilidad total de los equipos seleccionados sin exceder la capacidad.

## 2. Formulación matemática

Sea el conjunto de equipos E = {1, 2, ..., 100}. Para cada equipo i se define la variable de decisión binaria:

- x_i = 1 si el equipo i se selecciona.
- x_i = 0 si el equipo i no se selecciona.

**Función objetivo:**

```
max Z = sum_{i=1}^{100} u_i * x_i
```

**Restricciones:**

```
sum_{i=1}^{100} p_i * x_i <= 250
x_i ∈ {0, 1},  i = 1, ..., 100
```

donde u_i es la utilidad y p_i el peso del equipo i.

**Naturaleza del problema.** Las variables toman valores en un dominio finito y no existen decisiones fraccionarias, por lo que se trata de un problema de optimización combinatoria discreta. El espacio de búsqueda contiene 2^100 (aproximadamente 1,27 x 10^30) selecciones candidatas, lo que hace inviable la enumeración exhaustiva. El problema de la mochila 0/1 es NP-duro en el caso general.

## 3. Generación de la instancia

El conjunto de datos se genera una sola vez con la semilla 42 mediante el módulo `random` de Python, de modo que todos los métodos operan sobre exactamente la misma instancia:

- 100 elementos, nombrados "Equipo 1" a "Equipo 100".
- Pesos: `random.randint(1, 20)`.
- Utilidades: `random.randint(10, 100)`.
- Capacidad: 250 kg.

## 4. Metodología

### 4.1 Propuestas de referencia

Se evalúan tres selecciones elementales: ningún equipo, los primeros 10 equipos en el orden original y los 100 equipos. Para cada una se reportan peso total, utilidad total, cantidad de equipos y factibilidad.

### 4.2 Construcción aleatoria

Se realizan 30 ejecuciones con semillas de 0 a 29. En cada una se mezcla únicamente el orden de los elementos, manteniendo pesos, utilidades y capacidad. Se recorre la lista mezclada y se incorpora cada equipo si cabe en la capacidad restante; en caso contrario se omite y se continúa con el siguiente.

### 4.3 Construcción voraz (greedy)

Se calcula la razón r_i = u_i / p_i para cada equipo y se ordenan de mayor a menor. Se recorre la lista ordenada incorporando cada equipo si cabe en la capacidad restante. El ordenamiento es estable, por lo que los empates conservan el orden original.

### 4.4 Referencia exacta por programación dinámica

Se emplea la formulación clásica de la mochila 0/1 con pesos enteros. Sea `dp[i][w]` la mejor utilidad alcanzable con los primeros i elementos y capacidad w:

```
dp[i][w] = max( dp[i-1][w],  dp[i-1][w - p_i] + u_i )   si w >= p_i
dp[i][w] = dp[i-1][w]                                    si w <  p_i
dp[0][w] = 0  y  dp[i][0] = 0
```

La tabla tiene (n + 1) x (W + 1) = 101 x 251 estados, con una complejidad temporal de O(nW). El método es exacto porque los pesos y la capacidad son enteros, y evita enumerar las 2^100 selecciones. La selección óptima se reconstruye recorriendo la tabla hacia atrás.

### 4.5 Métrica de comparación

La calidad de cada método se mide con la brecha porcentual respecto al óptimo:

```
Brecha (%) = 100 * (Z_optimo - Z_metodo) / Z_optimo
```

## 5. Resultados

Valores obtenidos para la instancia con semilla 42 (fuente: `reporte_resultados.json`).

| Método | Peso (kg) | Utilidad | Equipos | Brecha (%) |
|---|---:|---:|---:|---:|
| Ningún equipo | 0 | 0 | 0 | 100,00 |
| Primeros 10 equipos | 95 | 399 | 10 | 86,11 |
| Los 100 equipos | > 250 | no aplica | 100 | infactible |
| Mejor ejecución aleatoria (semilla 29) | 250 | 1663 | 31 | 42,12 |
| Greedy por utilidad/peso | 248 | 2860 | 42 | 0,45 |
| Óptimo exacto (programación dinámica) | 250 | 2873 | no reportado en esta tabla | 0,00 |

Las 30 ejecuciones aleatorias, con sus pesos, utilidades y cantidades de equipos, se encuentran en la clave `aleatorio_todos` del archivo `reporte_resultados.json`. Todas las construcciones aleatorias son factibles por construcción.

## 6. Discusión

1. **Inviabilidad de la fuerza bruta.** Con aproximadamente 1,27 x 10^30 combinaciones, la enumeración exhaustiva es impracticable incluso evaluando miles de millones de selecciones por segundo. La programación dinámica resuelve la instancia con apenas 25 mil celdas de cálculo.
2. **Desempeño del greedy.** La heurística por razón utilidad/peso obtuvo 2860 frente a un óptimo de 2873, es decir, una brecha de 0,45 %. No alcanzó el óptimo porque su decisión es local e irrevocable: puede llenar la capacidad con elementos de buena razón pero dejar un remanente que impide incorporar una combinación de mayor utilidad total.
3. **Variabilidad de la construcción aleatoria.** El orden de llegada determina qué elementos caben primero, por lo que cada semilla produce una solución factible distinta. La mejor ejecución observada (semilla 29, utilidad 1663) queda muy por debajo del óptimo, lo que evidencia que la factibilidad no implica calidad.
4. **Factibilidad frente a optimalidad.** Una selección factible solo satisface la restricción de capacidad; puede dejar capacidad sin usar o privilegiar elementos de baja utilidad. El óptimo es la mejor solución entre todas las factibles.
5. **Alcance de las conclusiones.** Los resultados corresponden a una única instancia. La superioridad de un método debe evaluarse sobre un conjunto representativo de instancias y no puede inferirse de un solo caso.

## 7. Limitaciones

- Se analiza una sola instancia (semilla 42); no se estudia la sensibilidad a distintos tamaños, capacidades ni distribuciones de pesos y utilidades.
- La programación dinámica es pseudo-polinomial: su costo crece con la capacidad W, por lo que deja de ser práctica para capacidades muy grandes o pesos no enteros.
- No se incluyen metaheurísticas (búsqueda local, recocido simulado, algoritmos genéticos, entre otras); el trabajo se limita a soluciones de referencia y heurísticas básicas.
- La variabilidad aleatoria se resume con 30 semillas, número suficiente para ilustrar la dispersión pero no para inferencia estadística formal.

## 8. Estructura del repositorio

```
.
├── knapsack_trabajo.py        Script principal: genera la instancia, ejecuta todos los métodos y escribe el reporte
├── knapsack_trabajo.ipynb     Versión en cuaderno de Jupyter del trabajo
├── build_notebook.py          Script auxiliar para la construcción del cuaderno
├── reporte_resultados.json    Resultados de la ejecución en formato JSON
└── README.md                  Este documento
```

## 9. Requisitos y ejecución

**Requisitos:** Python 3. El script principal utiliza únicamente la biblioteca estándar (`random` y `json`), por lo que no requiere instalar dependencias externas. Para abrir el cuaderno se necesita Jupyter.

**Ejecución del script:**

```bash
git clone https://github.com/Camxeroth/Selecci-n-de-equipos-con-una-mochila-de-100-elementos.git
cd Selecci-n-de-equipos-con-una-mochila-de-100-elementos
python knapsack_trabajo.py
```

La ejecución imprime en consola cada sección del trabajo (formulación, propuestas, construcción aleatoria, greedy, referencia exacta, comparación, reflexión y verificación final) y sobrescribe `reporte_resultados.json`.

**Ejecución del cuaderno:**

```bash
jupyter notebook knapsack_trabajo.ipynb
```

**Reproducibilidad.** La instancia se genera con la semilla 42 y las mezclas aleatorias con las semillas 0 a 29, por lo que una nueva ejecución debe reproducir los valores reportados. El script incluye verificaciones automáticas (aserciones) de factibilidad, binariedad de las selecciones y coincidencia entre el valor óptimo y su reconstrucción.

## 10. Referencias

- Cormen, T. H., Leiserson, C. E., Rivest, R. L. y Stein, C. *Introduction to Algorithms*. MIT Press.
- Garey, M. R. y Johnson, D. S. (1979). *Computers and Intractability: A Guide to the Theory of NP-Completeness*. W. H. Freeman.
- Martello, S. y Toth, P. (1990). *Knapsack Problems: Algorithms and Computer Implementations*. John Wiley & Sons.
- Kellerer, H., Pferschy, U. y Pisinger, D. (2004). *Knapsack Problems*. Springer.

## 11. Licencia

[Indicar la licencia del repositorio o, si es un trabajo académico, el uso previsto.]
