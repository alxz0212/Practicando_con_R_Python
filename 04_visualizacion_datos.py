# -*- coding: utf-8 -*-
"""
=============================================================================
EJERCICIO 04: VISUALIZACIÓN DE DATOS PARA EPIDEMIOLOGÍA
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
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración estética de los gráficos (similar a theme_bw o theme_minimal)
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)

# Generamos/Cargamos datos
try:
    df = pd.read_excel("linelist_cleaned.xlsx")
    df.columns = [col.lower().replace(' ', '_') for col in df.columns]
except:
    # Datos sintéticos si el archivo no existe
    np.random.seed(42)
    df = pd.DataFrame({
        'hospital': np.random.choice(['Hosp A', 'Hosp B', 'Hosp C'], 200),
        'age': np.random.normal(35, 15, 200).clip(0, 90),
        'gender': np.random.choice(['male', 'female'], 200),
        'outcome': np.random.choice(['Recover', 'Death'], 200, p=[0.7, 0.3])
    })

# =============================================================================
# 1. HISTOGRAMA (Distribución de Edad)
# =============================================================================
print("Generando Histograma...")
plt.figure()
sns.histplot(data=df, x='age', bins=20, kde=True, color='skyblue')
plt.title('Distribución de Edad de los Pacientes')
plt.xlabel('Edad')
plt.ylabel('Frecuencia')
# plt.savefig('01_histograma_edad.png') # Para guardar
plt.show(block=False) # block=False para que no detenga el script si se corre en consola

# =============================================================================
# 2. BOXPLOT (Edad por Hospital)
# =============================================================================
print("Generando Boxplot...")
plt.figure()
sns.boxplot(data=df, x='hospital', y='age', hue='hospital', palette='Set2', legend=False)
plt.title('Distribución de Edad por Hospital')
plt.xlabel('Hospital')
plt.ylabel('Edad')
plt.show(block=False)

# =============================================================================
# 3. GRÁFICO DE BARRAS (Equivalente a geom_bar o geom_col)
# =============================================================================
print("Generando Gráfico de Barras...")
plt.figure()
# Countplot cuenta automáticamente las frecuencias
sns.countplot(data=df, x='hospital', hue='outcome', palette='viridis')
plt.title('Resultados (Outcome) por Hospital')
plt.xlabel('Hospital')
plt.ylabel('Número de Casos')
plt.legend(title='Resultado')
plt.show(block=False)

# =============================================================================
# 4. GRÁFICO DE DISPERSIÓN (Scatter Plot)
# =============================================================================
# Usamos el ejemplo de David Villa (Goles vs Partidos) o datos sintéticos
print("Generando Gráfico de Dispersión...")
df_villa = pd.DataFrame({
    'partidos': [36, 44, 40, 46, 46, 40, 49, 41, 40],
    'goles': [13, 20, 20, 20, 20, 28, 21, 22, 31]
})

plt.figure()
sns.regplot(data=df_villa, x='partidos', y='goles', 
            scatter_kws={'s': 100, 'color': 'red'}, 
            line_kws={'color': 'blue'})
plt.title('Relación Partidos Jugados vs Goles (David Villa)')
plt.xlabel('Número de Partidos')
plt.ylabel('Número de Goles')
plt.show() # El último gráfico sí bloquea o simplemente cierra todos al terminar

print("\nVisualizaciones completadas.")
print("Nota: Para PyCharm, estos gráficos aparecerán en la ventana 'Scientific View' o en ventanas emergentes.")
