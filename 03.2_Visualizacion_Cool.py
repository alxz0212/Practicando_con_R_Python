# -*- coding: utf-8 -*-
"""
=============================================================================
EJERCICIO 03.2: VISUALIZACIÓN 'COOL' CON DASH & PLOTLY
=============================================================================

Dashboard interactivo con tema oscuro y gráficos modernos.
"""

import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import os

# =============================================================================
# 1. CARGA Y PREPARACIÓN DE DATOS
# =============================================================================
file_name = "linelist_cleaned.xlsx"

if not os.path.exists(file_name):
    raise FileNotFoundError(f"El archivo '{file_name}' no existe.")

print("Cargando datos...")
df = pd.read_excel(file_name)
# Limpieza de columnas
df.columns = [col.lower().replace(' ', '_') for col in df.columns]

# --- Generación de Gráficos (Pre-cálculo) ---

# 1. Barras: Casos por Hospital
# Usamos reset_index y verificamos nombres para evitar errores de pandas
hosp_counts = df['hospital'].value_counts().reset_index()
# Renombramiento explícito para garantizar consistencia
hosp_counts.columns = ['hospital', 'count']

# Asegurar tipos de datos para Plotly
x_col = 'count'
y_col = 'hospital'
print(f"Columnas para gráfico de barras: X={x_col}, Y={y_col}")
print(hosp_counts.head())

fig_bar = px.bar(
    hosp_counts, x=x_col, y=y_col, orientation='h',
    text=x_col,
    color=x_col,
    color_continuous_scale='Viridis', # Color seguro
    title="Casos Totales por Hospital",
    template='plotly_white'
)
fig_bar.update_layout(
    yaxis={'categoryorder':'total ascending'}, 
    margin=dict(l=0, r=0, t=40, b=0),
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)'
)

# 2. Heatmap: Hospital vs Outcome
ct = pd.crosstab(df['hospital'], df['outcome'])
fig_heat = px.imshow(
    ct, 
    text_auto=True, 
    aspect="auto",
    color_continuous_scale='Viridis',
    title="Relación Hospital vs Desenlace",
    template='plotly_white'
)
fig_heat.update_layout(
    margin=dict(l=0, r=0, t=40, b=0),
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)'
)

# 3. Violín: Distribución de Edad
fig_violin = px.violin(
    df, y="age", x="hospital", color="hospital",
    box=True, points="all",
    hover_data=df.columns,
    title="Distribución de Edad por Hospital",
    template='plotly_white'
)
fig_violin.update_layout(
    margin=dict(l=0, r=0, t=40, b=0),
    showlegend=False,
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)'
)

# --- KPIs ---
total_cases = len(df)
recovered = len(df[df['outcome'] == 'Recover'])
deaths = len(df[df['outcome'] == 'Death'])
recovery_rate = (recovered / total_cases * 100) if total_cases > 0 else 0

def create_card(title, value, color_class="text-info"):
    return dbc.Card(
        dbc.CardBody([
            html.H5(title, className="card-title text-center text-muted"),
            html.H2(value, className=f"card-text text-center {color_class}")
        ]),
        className="mb-3 shadow-sm"
    )

# =============================================================================
# 2. CONFIGURACIÓN DE LA APP (TEMA CLARO - FLATLY)
# =============================================================================
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
app.title = "Analisis Epidemiologico Cool"

# =============================================================================
# 3. LAYOUT
# =============================================================================
app.layout = dbc.Container([
    # Encabezado
    dbc.Row([
        dbc.Col(html.H1("DASHBOARD EPIDEMIOLÓGICO", className="text-center text-primary mb-2 mt-4"), width=12),
        dbc.Col(html.P("Análisis visual de datos clínicos", className="text-center text-muted mb-5"), width=12)
    ]),

    # Tarjetas KPI
    dbc.Row([
        dbc.Col(create_card("TOTAL CASOS", f"{total_cases:,}", "text-primary"), width=4),
        dbc.Col(create_card("RECUPERADOS", f"{recovered:,} ({recovery_rate:.1f}%)", "text-success"), width=4),
        dbc.Col(create_card("FALLECIDOS", f"{deaths:,}", "text-danger"), width=4),
    ], className="mb-4"),

    # Fila 1: Barras y Heatmap
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Volumen de Pacientes", className="bg-light fw-bold"),
                dbc.CardBody(dcc.Graph(figure=fig_bar, config={'displayModeBar': False}))
            ], className="h-100 shadow-sm border-0")
        ], md=6, className="mb-4"),

        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Resultados Clínicos", className="bg-light fw-bold"),
                dbc.CardBody(dcc.Graph(figure=fig_heat, config={'displayModeBar': False}))
            ], className="h-100 shadow-sm border-0")
        ], md=6, className="mb-4"),
    ]),

    # Fila 2: Distribución de Edad
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Demografía: Edad por Centro", className="bg-light fw-bold"),
                dbc.CardBody(dcc.Graph(figure=fig_violin, config={'displayModeBar': True}))
            ], className="shadow-sm border-0")
        ], width=12),
    ]),
    
    # Footer
    dbc.Row([
        dbc.Col(html.P("Desarrollado con Dash & Plotly - Tema Flatly", className="text-center text-muted mt-5 mb-3 small"), width=12)
    ])

], fluid=True, className="p-4 bg-light", style={'minHeight': '100vh'})

# =============================================================================
# 5. EJECUCIÓN
# =============================================================================
if __name__ == '__main__':
    print("Iniciando Dashboard...")
    print("Abre tu navegador en: http://127.0.0.1:8050/")
    app.run(debug=False, port=8050)
