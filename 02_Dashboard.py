from shiny import App, render, ui, reactive
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import tempfile
import os

import numpy as np

# Cargar datos
try:
    df_original = pd.read_csv("linelist_limpio_resuelto.csv")
except FileNotFoundError:
    # Datos dummy por si falla la carga para que la app no crashee al inicio
    df_original = pd.DataFrame({
        'age': [25, 30, 45, 22, 50, 60],
        'gender': ['male', 'female', 'male', 'female', 'male', 'female'],
        'hospital': ['A', 'B', 'A', 'B', 'A', 'A'],
        'outcome': ['recover', 'death', 'recover', 'recover', 'death', 'recover']
    })

app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.h3("Filtros"),
        ui.input_text("case_id", "Case ID:", placeholder="Ej: 11f8ea"),
        ui.input_text("hospital", "Hospital:", placeholder="Ej: Military"),
        ui.hr(),

        ui.download_button("download_data", "Descargar Excel (.xlsx)"),
        ui.hr(),
        ui.p("Dashboard generado con Shiny for Python", style="font-size: 0.8em; color: gray;")
    ),
    ui.card(
        ui.card_header("Distribución de Edades"),
        ui.output_plot("age_dist_plot")
    ),
    ui.layout_columns(
        ui.card(
            ui.card_header("Estado (Outcome)"),
            ui.output_plot("outcome_plot")
        ),
        ui.card(
            ui.card_header("Estadísticas"),
            ui.output_text_verbatim("stats_summary")
        )
    ),
    ui.card(
        ui.card_header("Datos Filtrados"),
        ui.output_data_frame("data_table")
    ),
    title="Dashboard 02: Análisis de Linelist"
)

def server(input, output, session):
    
    @reactive.calc
    def filtered_data():
        df = df_original.copy()
        
        # Filtro Case ID
        if input.case_id():
            df = df[df['case_id'].astype(str).str.contains(input.case_id(), case=False, na=False)]
            
        # Filtro Hospital
        if input.hospital():
            df = df[df['hospital'].astype(str).str.contains(input.hospital(), case=False, na=False)]
        
        return df

    @render.plot
    def age_dist_plot():
        df = filtered_data()
        fig, ax = plt.subplots(figsize=(10, 4))
        sns.histplot(data=df, x='age', hue='gender', multiple="stack", kde=True, ax=ax)
        ax.set_title("Histograma de Edades")
        ax.set_xlabel("Edad")
        return fig

    @render.plot
    def outcome_plot():
        df = filtered_data()
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.countplot(data=df, x='outcome', palette='viridis', ax=ax)
        ax.set_title("Resultados (Outcome)")
        return fig

    @render.text
    def stats_summary():
        df = filtered_data()
        total = len(df)
        avg_age = df['age'].mean()
        return f"Total de casos: {total}\nEdad Promedio: {avg_age:.2f} años"

    @render.data_frame
    def data_table():
        # filters=False quita los espacios en blanco de búsqueda por columna
        return render.DataGrid(filtered_data().head(100), filters=False)

    @render.download(filename="datos_filtrados.xlsx")
    def download_data():
        df = filtered_data()
        # Usamos un archivo temporal
        with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as tmp:
            tmp_path = tmp.name
        
        # Escribimos el Excel
        with pd.ExcelWriter(tmp_path, engine="openpyxl") as writer:
            df.to_excel(writer, index=False)
            
        # IMPORTANTE: Leemos el archivo y enviamos los BYTES, no la ruta
        with open(tmp_path, "rb") as f:
            yield f.read()
            
        # Limpieza
        os.remove(tmp_path)

app = App(app_ui, server)
