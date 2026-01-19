# -*- coding: utf-8 -*-
"""
=============================================================================
EJERCICIO 02: LIMPIEZA Y PREPARACIÓN DE DATOS (DATA CLEANING)
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
import os

# Nota: Para limpiar nombres de columnas de forma similar a janitor::clean_names() de R,
# se suele usar la librería 'pyjanitor'. Si no la tienes, se puede hacer con pandas.

# =============================================================================
# 1. CARGA DE DATOS
# =============================================================================
print("--- 1. Carga de Datos ---")
file_path = "linelist_cleaned.xlsx"

# Cargamos el archivo Excel
if os.path.exists(file_path):
    df = pd.read_excel(file_path)
    print(f"Datos cargados exitosamente. Dimensiones: {df.shape}")
else:
    print(f"Error: No se encuentra el archivo {file_path}")
    # Creamos un ejemplo pequeño si el archivo falta para que el código no falle
    df = pd.DataFrame({
        'Case_ID': [1, 2, 3],
        'Age': [25, 30, np.nan],
        'Gender': ['male', 'f', 'Male'],
        'Hospital': ['Central', 'St. Mark', 'Central']
    })

# =============================================================================
# 2. LIMPIEZA DE NOMBRES (Equivalente a janitor::clean_names)
# =============================================================================
print("\n--- 2. Limpieza de Nombres ---")
# Convertir nombres a minúsculas y reemplazar espacios por guiones bajos
df.columns = [col.lower().replace(' ', '_').replace('.', '_') for col in df.columns]
print("Nuevas columnas:", df.columns.tolist())

# =============================================================================
# 3. FILTRADO Y SELECCIÓN (Equivalente a filter() y select())
# =============================================================================
print("\n--- 3. Filtrado y Selección ---")

# Filtrar casos con edad definida (no nula)
df_clean = df[df['age'].notna()].copy()

# Seleccionar solo algunas columnas importantes
# (age, gender, hospital, outcome)
columnas_interes = ['age', 'gender', 'hospital']
# Verificamos si existen en el df (por si el excel es distinto)
columnas_interes = [c for c in columnas_interes if c in df.columns]
df_subset = df_clean[columnas_interes]

print(f"Filas tras eliminar edades nulas: {len(df_clean)}")

# =============================================================================
# 4. RECODIFICACIÓN Y NUEVAS COLUMNAS (Equivalente a mutate() y case_when())
# =============================================================================
print("\n--- 4. Recodificación (Mutate) ---")

# Normalizar género (Equivalente a recode())
if 'gender' in df_clean.columns:
    df_clean['gender'] = df_clean['gender'].str.lower().replace({
        'f': 'female',
        'm': 'male'
    })

# Crear categorías de edad (Equivalente a case_when() o cut())
if 'age' in df_clean.columns:
    bins = [0, 5, 15, 30, 50, 100]
    labels = ['0-5', '6-15', '16-30', '31-50', '50+']
    df_clean['age_cat'] = pd.cut(df_clean['age'], bins=bins, labels=labels)

print("Primeras filas con nuevas columnas:")
print(df_clean[['age', 'age_cat', 'gender']].head())

# =============================================================================
# 5. MANEJO DE MISSING VALUES
# =============================================================================
print("\n--- 5. Valores Faltantes ---")
# Contar NAs por columna
print("Valores nulos por columna:")
print(df_clean.isnull().sum())

# Reemplazar NAs en 'hospital' con 'Unknown'
if 'hospital' in df_clean.columns:
    df_clean['hospital'] = df_clean['hospital'].fillna('Unknown')

# Guardar el resultado limpio (opcional)
# df_clean.to_csv("linelist_limpio.csv", index=False)
print("\nProceso de limpieza completado.")
