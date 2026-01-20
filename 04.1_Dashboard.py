import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import numpy as np

# --- 1. Carga y Preparación de Datos ---
try:
    df = pd.read_excel("linelist_cleaned.xlsx")
    # Normalizar columnas
    df.columns = [col.lower().replace(' ', '_') for col in df.columns]
except FileNotFoundError:
    # Datos sintéticos si falla la carga
    print("Archivo no encontrado, usando datos sintéticos.")
    np.random.seed(42)
    df = pd.DataFrame({
        'hospital': np.random.choice(['Hosp A', 'Hosp B', 'Hosp C'], 200),
        'age': np.random.normal(35, 15, 200).clip(0, 90),
        'gender': np.random.choice(['male', 'female'], 200),
        'outcome': np.random.choice(['Recover', 'Death'], 200, p=[0.7, 0.3])
    })

# Datos para Scatter Plot (David Villa)
df_villa = pd.DataFrame({
    'partidos': [36, 44, 40, 46, 46, 40, 49, 41, 40],
    'goles': [13, 20, 20, 20, 20, 28, 21, 22, 31]
})

# --- 2. Creación de Gráficos con Plotly Express ---

# Gráfico 1: Histograma de Edad
fig_hist = px.histogram(
    df, 
    x="age", 
    nbins=20, 
    title="Distribución de Edad de los Pacientes",
    labels={"age": "Edad"},
    color_discrete_sequence=['skyblue']
)
fig_hist.update_layout(bargap=0.1)

# Gráfico 2: Boxplot (Edad por Hospital)
fig_box = px.box(
    df, 
    x="hospital", 
    y="age", 
    color="hospital",
    title="Distribución de Edad por Hospital",
    labels={"hospital": "Hospital", "age": "Edad"},
    color_discrete_sequence=px.colors.qualitative.Set2
)

# Gráfico 3: Gráfico de Barras (Outcome por Hospital)
# Para imitar countplot, usamos histograma sobre x con color=outcome, o agrupamos antes.
# px.histogram con barmode='group' o 'stack' funciona como countplot.
fig_bar = px.histogram(
    df, 
    x="hospital", 
    color="outcome", 
    barmode="group",
    title="Resultados (Outcome) por Hospital",
    labels={"hospital": "Hospital", "count": "Número de Casos"},
    color_discrete_sequence=px.colors.sequential.Viridis
)

# Gráfico 4: Scatter Plot (David Villa)
fig_scatter = px.scatter(
    df_villa, 
    x="partidos", 
    y="goles",
    trendline="ols", # Línea de regresión (requiere statsmodels, si falla se quita)
    title="Relación Partidos Jugados vs Goles (David Villa)",
    labels={"partidos": "Número de Partidos", "goles": "Número de Goles"}
)
fig_scatter.update_traces(marker=dict(size=12, color='red'), selector=dict(mode='markers'))
# Personalizar linea de tendencia si se generó
fig_scatter.update_traces(line=dict(color="blue"), selector=dict(mode="lines"))


# --- 3. Inicialización de la App Dash ---
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

# --- 4. Layout de la App ---
app.layout = dbc.Container([
    # Encabezado
    dbc.Row([
        dbc.Col(html.H1("Dashboard de Visualización de Datos (Dash)", className="text-center text-primary mb-4"), width=12)
    ]),

    # Fila 1: Histograma y Boxplot
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Histograma"),
                dbc.CardBody(dcc.Graph(figure=fig_hist))
            ])
        ], width=6),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Boxplot"),
                dbc.CardBody(dcc.Graph(figure=fig_box))
            ])
        ], width=6),
    ], className="mb-4"),

    # Fila 2: Barras y Scatter
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Gráfico de Barras"),
                dbc.CardBody(dcc.Graph(figure=fig_bar))
            ])
        ], width=6),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Scatter Plot (Regresión)"),
                dbc.CardBody(dcc.Graph(figure=fig_scatter))
            ])
        ], width=6),
    ], className="mb-4"),
    
    # Footer
    dbc.Row([
        dbc.Col(html.P("Generado con Dash & Bootstrap Components", className="text-center text-muted"), width=12)
    ])

], fluid=True)

# --- 5. Ejecución ---
if __name__ == "__main__":
    # debug=True para desarrollo
    app.run(debug=True, port=8051)
