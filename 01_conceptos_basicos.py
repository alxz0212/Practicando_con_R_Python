# -*- coding: utf-8 -*-
"""
=============================================================================
EJERCICIO 01: CONCEPTOS BÁSICOS EN PYTHON PARA ANÁLISIS DE DATOS
=============================================================================

CRÉDITOS Y CERTIFICACIÓN:
-------------------------
Autor original/Referencia: @TodoEconometria
Profesor: Juan Marcelo Gutierrez Miranda
Metodología: Cursos Avanzados de Big Data, Ciencia de Datos, 
             Desarrollo de aplicaciones con IA & Econometría Aplicada.
Hash ID de Certificación: 4e8d9b1a5f6e7c3d2b1a0f9e8d7c6b5a4f3e2d1c0b9a8f7e6d5c4b3a2f1e0d9c
Repositorio: https://github.com/TodoEconometria/certificaciones

REFERENCIA ACADÉMICA:
Este material es una adaptación a Python del "The Epidemiologist R Handbook" 
(Neale Batra et al., 2021), bajo licencia CC BY-NC-SA 4.0.
"""

import math
import numpy as np
import pandas as pd
from scipy import stats

# =============================================================================
# 1. PYTHON COMO CALCULADORA
# =============================================================================
# Al igual que en R, Python puede realizar operaciones matemáticas directas.

print("--- 1. Cálculos Básicos ---")
print(f"Suma (2+2): {2 + 2}")
print(f"Logaritmo y Seno (log(1+sin(pi/4))): {math.log(1 + math.sin(math.pi/4))}")

# Generar números aleatorios (Equivalente a rnorm(8))
random_numbers = np.random.normal(0, 1, 8)
print(f"8 números aleatorios (distribución normal): \n{random_numbers}")

# =============================================================================
# 2. VARIABLES
# =============================================================================
# En Python usamos '=' en lugar de '<-' para asignar valores.

print("\n--- 2. Variables ---")
x = 5
variable_1 = 45 # Las variables en Python suelen usar snake_case
print(f"Valor de x: {x}")

# =============================================================================
# 3. VECTORES (LISTAS Y ARRAYS)
# =============================================================================
# En Python, para cálculos numéricos usamos NumPy arrays (equivalente a vectores en R).

print("\n--- 3. Vectores y Estadística Básica ---")
# Datos de ejemplo: Pesos de personas (Kg)
peso = np.array([60, 72, 84, 65, 43, 87, 90, 56])
print(f"Vector de pesos: {peso}")
print(f"Longitud del vector: {len(peso)}")

# Cálculo del IMC
altura = np.array([1.59, 1.75, 1.85, 1.60, 1.57, 1.90, 1.83, 1.73])
imc = peso / (altura ** 2)
print(f"IMC calculado: \n{imc}")

# Estadísticos descriptivos manuales (usando fórmulas)
media_peso = np.sum(peso) / len(peso)
varianza_peso = np.sum((peso - media_peso)**2) / (len(peso) - 1) # Varianza muestral (n-1)

# Estadísticos con funciones incorporadas
print(f"\nMedia (peso): {np.mean(peso)}")
print(f"Varianza (peso): {np.var(peso, ddof=1)}") # ddof=1 para n-1 (muestral)
print(f"Desviación Típica (peso): {np.std(peso, ddof=1)}")
print(f"Resumen (Pandas describe):\n{pd.Series(peso).describe()}")

# =============================================================================
# EJERCICIO 1: David Villa
# =============================================================================
print("\n--- Ejercicio David Villa ---")

temporada = ['00', '01', '02', '03', '04', '05', '06', '07', '08']
partidos = np.array([36, 44, 40, 46, 46, 40, 49, 41, 40])
goles = np.array([13, 20, 20, 20, 20, 28, 21, 22, 31])

# Creación de un DataFrame (Equivalente al data.frame de R)
df_villa = pd.DataFrame({
    'temporada': temporada,
    'partidos': partidos,
    'goles': goles
})

print("DataFrame de David Villa:")
print(df_villa.head())

# Estadísticos usando Pandas
print("\nMedia de partidos y goles:")
print(df_villa[['partidos', 'goles']].mean())

print("\nCovarianza:")
print(df_villa[['partidos', 'goles']].cov().iloc[0, 1])

print("\nCorrelación:")
print(df_villa[['partidos', 'goles']].corr().iloc[0, 1])

# Referencia a Epi R Handbook: 
# "Aunque este curso es en Python, seguimos los principios de organización y 
#  claridad que propone el manual, adaptando las funciones de R (dplyr/tidyverse) 
#  a las de Python (pandas/numpy)."
