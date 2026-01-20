# -*- coding: utf-8 -*-
"""
=============================================================================
EJERCICIO 03.1: RESOLUCIÓN - TABLAS DESCRIPTIVAS Y ANÁLISIS DE GRUPOS
=============================================================================

Adaptación del ejercicio 03 para utilizar 'linelist_cleaned.xlsx'.
"""

import pandas as pd
import numpy as np
import os

# Definir el nombre del archivo
file_name = "linelist_cleaned.xlsx"

# Verificar si el archivo existe antes de intentar cargarlo
if not os.path.exists(file_name):
    raise FileNotFoundError(f"El archivo '{file_name}' no se encuentra en el directorio actual: {os.getcwd()}")

# Cargar los datos
print(f"Cargando datos de {file_name}...")
df = pd.read_excel(file_name)

# Limpiamos nombres de columnas para asegurar consistencia
df.columns = [col.lower().replace(' ', '_') for col in df.columns]

# Verificar columnas necesarias
required_columns = ['hospital', 'gender', 'age', 'outcome']
missing_cols = [col for col in required_columns if col not in df.columns]
if missing_cols:
    print(f"Advertencia: Faltan las siguientes columnas esperadas: {missing_cols}")
else:
    print("Todas las columnas necesarias están presentes.")

# =============================================================================
# 1. TABLAS DE FRECUENCIAS
# =============================================================================
print("\n--- 1. Tablas de Frecuencia Simple ---")

# Frecuencia de 'hospital'
if 'hospital' in df.columns:
    print("\nFrecuencia por Hospital:")
    freq_hosp = df['hospital'].value_counts()
    perc_hosp = df['hospital'].value_counts(normalize=True) * 100
    
    # Combinamos en un solo DataFrame
    tabla_hosp = pd.DataFrame({'N': freq_hosp, 'Percent (%)': perc_hosp})
    print(tabla_hosp)

# =============================================================================
# 2. TABLAS DE CONTIGENCIA (Cruces)
# =============================================================================
print("\n--- 2. Tablas Cruzadas (Crosstabs) ---")

# Cruzamos Hospital vs Outcome
if 'hospital' in df.columns and 'outcome' in df.columns:
    cross_tab = pd.crosstab(df['hospital'], df['outcome'], margins=True, margins_name="Total")
    print("Cruzar Hospital y Resultado:")
    print(cross_tab)

# =============================================================================
# 3. RESÚMENES GRUPALES
# =============================================================================
print("\n--- 3. Resúmenes por Grupo ---")

# Resumen de edad por hospital
if 'hospital' in df.columns and 'age' in df.columns:
    print("Estadísticos de Edad por Hospital:")
    resumen_hospital = df.groupby('hospital')['age'].agg([
        ('N', 'count'),
        ('Media', 'mean'),
        ('Mediana', 'median'),
        ('Desv_Std', 'std')
    ]).round(2)
    print(resumen_hospital)

# =============================================================================
# 4. TABLAS FORMATEADAS Y RESUMEN COMPLEJO
# =============================================================================
print("\n--- 4. Resumen Complejo ---")

if 'hospital' in df.columns and 'gender' in df.columns and 'outcome' in df.columns and 'age' in df.columns:
    resumen_complejo = df.groupby(['hospital', 'gender']).agg({
        'age': ['mean', 'max'],
        'outcome': lambda x: (x == 'Recover').sum() # Cuenta de recuperados. Nota: Verificar si el valor es 'Recover' exacto en el excel real
    }).rename(columns={'<lambda>': 'n_recuperados'})
    
    print("\nResumen complejo (Hospital + Género):")
    print(resumen_complejo)
