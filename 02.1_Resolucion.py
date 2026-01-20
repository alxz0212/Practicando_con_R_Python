# -*- coding: utf-8 -*-
"""
RESOLUCIÓN DEL EJERCICIO 02: LIMPIEZA Y PREPARACIÓN DE DATOS
------------------------------------------------------------
Archivo de resolución basado en '02_limpieza_y_preparacion.py'
Usando: linelist_cleaned.xlsx
"""

import pandas as pd
import numpy as np
import os

# =============================================================================
# 1. CARGA DE DATOS
# =============================================================================
print("--- 1. Carga de Datos ---")
file_path = "linelist_cleaned.xlsx"

if os.path.exists(file_path):
    df = pd.read_excel(file_path)
    print(f"Datos cargados exitosamente. Dimensiones iniciales: {df.shape}")
else:
    print(f"Error: No se encuentra el archivo {file_path}")
    exit()

# =============================================================================
# 2. LIMPIEZA DE NOMBRES
# =============================================================================
print("\n--- 2. Limpieza de Nombres ---")
# Normalización: minúsculas y reemplazo de caracteres especiales
df.columns = [col.lower().replace(' ', '_').replace('.', '_') for col in df.columns]
print("Columnas normalizadas (ejemplo):", df.columns.tolist()[:10])

# =============================================================================
# 3. FILTRADO Y SELECCIÓN
# =============================================================================
print("\n--- 3. Filtrado y Selección ---")

# a) Filtrar casos donde la columna 'age' NO sea nula
print(f"Filas antes del filtrado: {len(df)}")
df_clean = df[df['age'].notna()].copy()
print(f"Filas tras eliminar 'age' nulos: {len(df_clean)}")

# b) Selección de columnas (mantenemos todas para el ejercicio, pero listamos las clave)
cols_clave = ['case_id', 'age', 'age_years', 'gender', 'hospital', 'outcome']
print(f"Columnas clave disponibles: {[c for c in cols_clave if c in df_clean.columns]}")

# =============================================================================
# 4. RECODIFICACIÓN Y NUEVAS COLUMNAS
# =============================================================================
print("\n--- 4. Recodificación y Transformación ---")

# a) Normalizar Género (gender)
if 'gender' in df_clean.columns:
    print("Valores únicos de género antes:", df_clean['gender'].unique())
    df_clean['gender'] = df_clean['gender'].str.lower().replace({
        'm': 'male',
        'f': 'female'
    })
    print("Valores únicos de género después:", df_clean['gender'].unique())

# b) Crear categorías de edad (age_cat)
if 'age' in df_clean.columns:
    # Definimos los cortes y etiquetas
    cortes = [0, 5, 15, 30, 50, 100]
    etiquetas = ['0-5', '6-15', '16-30', '31-50', '50+']
    
    df_clean['age_cat'] = pd.cut(df_clean['age'], bins=cortes, labels=etiquetas)
    print("\nDistribución por categoría de edad:")
    print(df_clean['age_cat'].value_counts().sort_index())

# =============================================================================
# 5. MANEJO DE VALORES FALTANTES (MISSING VALUES)
# =============================================================================
print("\n--- 5. Manejo de Valores Faltantes ---")

# Identificar columnas con nulos
nulos = df_clean.isnull().sum()
print("Columnas con nulos (>0):")
print(nulos[nulos > 0])

# Reemplazo en columna 'hospital' -> 'Unknown'
if 'hospital' in df_clean.columns:
    nulos_hosp = df_clean['hospital'].isnull().sum()
    print(f"\nNulos en 'hospital' antes: {nulos_hosp}")
    
    df_clean['hospital'] = df_clean['hospital'].fillna('Unknown')
    
    print(f"Nulos en 'hospital' después: {df_clean['hospital'].isnull().sum()}")

# =============================================================================
# 6. GUARDADO FINAL
# =============================================================================
output_file = "linelist_limpio_resuelto.csv"
df_clean.to_csv(output_file, index=False)
print(f"\n--- Proceso finalizado. Archivo guardado como: {output_file} ---")
print(f"Dimensiones finales: {df_clean.shape}")
