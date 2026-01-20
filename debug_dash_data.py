
import pandas as pd
import os
import plotly.express as px

file_name = "linelist_cleaned.xlsx"

if not os.path.exists(file_name):
    print(f"El archivo '{file_name}' no existe.")
    exit()

print("Cargando datos...")
df = pd.read_excel(file_name)
df.columns = [col.lower().replace(' ', '_') for col in df.columns]

# 1. Barras: Casos por Hospital
try:
    print("\n--- Analizando Hospitales y Figura Bar ---")
    hosp_counts = df['hospital'].value_counts().reset_index()
    
    x_col = hosp_counts.columns[1] 
    y_col = hosp_counts.columns[0]
    print(f"X (count): {x_col}, Y (name): {y_col}")
    
    fig_bar = px.bar(
        hosp_counts, x=x_col, y=y_col, orientation='h',
        text=x_col,
        color=x_col,
        color_continuous_scale='Viridis',
        title="Casos Totales por Hospital",
        template='plotly_dark'
    )
    
    print("Figura Bar Data Traces:")
    # Check if data exists in figure
    if not fig_bar.data:
        print("!! Figure data is EMPTY !!")
    else:
        print(f"Num traces: {len(fig_bar.data)}")
        print(f"Trace 0 x-values sample: {fig_bar.data[0].x[:5]}")
        print(f"Trace 0 y-values sample: {fig_bar.data[0].y[:5]}")
        
    print("\n--- Analizando Heatmap y Figura Heat ---")
    ct = pd.crosstab(df['hospital'], df['outcome'])
    fig_heat = px.imshow(
        ct, 
        text_auto=True, 
        aspect="auto",
        template='plotly_dark'
    )
    if not fig_heat.data:
         print("!! Heatmap figure data is EMPTY !!")
    else:
         print(f"Num traces: {len(fig_heat.data)}")
         print(f"Trace 0 z-values sample (first row): {fig_heat.data[0].z[0] if len(fig_heat.data[0].z)>0 else 'Empty'}")

except Exception as e:
    print(f"Error creating figures: {e}")
