# Genera knapsack_trabajo.ipynb a partir de knapsack_trabajo.py
# Primera celda: markdown con el encabezado (sin el prefijo '# ' de Python).
# Celdas siguientes: codigo, separadas por las lineas de separador de seccion.
import json
import re

with open("knapsack_trabajo.py", "r", encoding="utf-8") as f:
    lineas = f.readlines()

encabezado_palabras = [
    "METAHEURÍSTICAS",
    "Actividad Autónoma 1",
    "Selección de equipos con una mochila de 100 elementos",
    "Unidad 1 Fundamentos de optimización y heurísticas básicas",
    "Tema 1 Formulación de problemas y soluciones de referencia",
]

encabezado_md = []
resto = []
estado = "encabezado"  # 'encabezado' | 'codigo'
cont_enc = 0

for linea in lineas:
    if estado == "encabezado" and cont_enc < len(encabezado_palabras):
        linea_sin = linea[2:] if linea.startswith("# ") else linea
        if encabezado_palabras[cont_enc] in linea_sin:
            encabezado_md.append(linea_sin.rstrip("\n"))
            cont_enc += 1
            continue
    estado = "codigo"
    resto.append(linea)

# Unir el encabezado en una celda markdown (una linea por parrafo)
markdown_source = [linea + "\n" for linea in encabezado_md]

# Detectar separadores de seccion: '# ' seguido de muchos '=', '-' o '_'
separador_re = re.compile(r"#\s*([=_-])\1{40,}$")

celdas_codigo = []
actual = []

for linea in resto:
    if separador_re.match(linea.rstrip("\n")):
        if actual:
            celdas_codigo.append("".join(actual))
            actual = []
        actual.append(linea)  # el separador abre la nueva celda
    else:
        actual.append(linea)
if actual:
    celdas_codigo.append("".join(actual))

# Armar celdas del notebook
celdas = []

if markdown_source:
    celdas.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": markdown_source,
    })

for src in celdas_codigo:
    celdas.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": src.splitlines(keepends=True),
    })

notebook = {
    "cells": celdas,
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3",
        },
        "language_info": {
            "name": "python",
            "version": "3.13.7",
        },
    },
    "nbformat": 4,
    "nbformat_minor": 4,
}

with open("knapsack_trabajo.ipynb", "w", encoding="utf-8") as f:
    json.dump(notebook, f, ensure_ascii=False, indent=1)

print(f"Notebook generado con {len(celdas)} celdas (1 markdown + {len(celdas_codigo)} codigo).")
