# -*- coding: utf-8 -*-
"""
=============================================================================
EJERCICIO 03: TABLAS DESCRIPTIVAS Y ANÁLISIS DE GRUPOS
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

import pandas as pd
import numpy as np

# Cargamos los datos (usando el Dataset de David Villa para sencillez o linelist si existe)
try:
    df = pd.read_excel("linelist_cleaned.xlsx")
    # Limpiamos nombres rápidamente
    df.columns = [col.lower().replace(' ', '_') for col in df.columns]
except:
    # Dataset sintético para que el código sea reproducible
    print("Dataset no encontrado, generando datos de prueba...")
    df = pd.DataFrame({
        'hospital': ['Hospital A', 'Hospital B', 'Hospital A', 'Hospital A', 'Hospital B', 'Hospital A', 'Hospital B'],
        'gender': ['male', 'female', 'female', 'male', 'female', 'male', 'female'],
        'age': [25, 45, 12, 60, 32, 28, 5],
        'outcome': ['Recover', 'Death', 'Recover', 'Recover', 'Death', 'Recover', 'Recover']
    })

# =============================================================================
# 1. TABLAS DE FRECUENCIAS (Equivalente a janitor::tabyl)
# =============================================================================
print("--- 1. Tablas de Frecuencia Simple ---")

# Frecuencia de 'hospital'
print("\nFrecuencia por Hospital:")
freq_hosp = df['hospital'].value_counts()
perc_hosp = df['hospital'].value_counts(normalize=True) * 100

# Combinamos en un solo DataFrame similar a tabyl()
tabla_hosp = pd.DataFrame({'N': freq_hosp, 'Percent (%)': perc_hosp})
print(tabla_hosp)

# =============================================================================
# 2. TABLAS DE CONTIGENCIA (Cruces)
# =============================================================================
print("\n--- 2. Tablas Cruzadas (Crosstabs) ---")

# Cruzamos Hospital vs Outcome
cross_tab = pd.crosstab(df['hospital'], df['outcome'], margins=True, margins_name="Total")
print("Cruzar Hospital y Resultado:")
print(cross_tab)

# =============================================================================
# 3. RESÚMENES GRUPALES (Equivalente a group_by %>% summarise)
# =============================================================================
print("\n--- 3. Resúmenes por Grupo ---")

# Resumen de edad por hospital
# (Media, Mediana, Desviación Estándar, N)
resumen_hospital = df.groupby('hospital')['age'].agg([
    ('N', 'count'),
    ('Media', 'mean'),
    ('Mediana', 'median'),
    ('Desv_Std', 'std')
]).round(2)

print("Estadísticos de Edad por Hospital:")
print(resumen_hospital)

# =============================================================================
# 4. TABLAS FORMATEADAS (Referencia a gtsummary/flextable)
# =============================================================================
# En Python, para tablas bonitas en notebooks se suele usar 'styler' de Pandas.
print("\nTip: En PyCharm (Notebooks) puedes usar df.style para exportar tablas visualmente atractivas.")

# Ejemplo de un resumen complejo
resumen_complejo = df.groupby(['hospital', 'gender']).agg({
    'age': ['mean', 'max'],
    'outcome': lambda x: (x == 'Recover').sum() # Cuenta de recuperados
}).rename(columns={'<lambda>': 'n_recuperados'})

print("\nResumen complejo (Hospital + Género):")
print(resumen_complejo)
