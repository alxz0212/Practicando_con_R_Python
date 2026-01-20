
import gradio as gr
import pandas as pd
import plotly.express as px
import os

# =============================================================================
# 1. CARGA DE DATOS
# =============================================================================
file_name = "linelist_cleaned.xlsx"

# Función de carga robusta
def load_data():
    if not os.path.exists(file_name):
        return pd.DataFrame()
    
    df = pd.read_excel(file_name)
    df.columns = [col.lower().replace(' ', '_') for col in df.columns]
    return df

df = load_data()

# =============================================================================
# 2. FUNCIONES DE GENERACIÓN DE GRÁFICOS
# =============================================================================

def get_kpis():
    if df.empty:
        return "0", "0 (0%)", "0"
        
    total_cases = len(df)
    recovered = len(df[df['outcome'] == 'Recover'])
    deaths = len(df[df['outcome'] == 'Death'])
    recovery_rate = (recovered / total_cases * 100) if total_cases > 0 else 0
    
    return f"{total_cases:,}", f"{recovered:,} ({recovery_rate:.1f}%)", f"{deaths:,}"

def plot_bar_hospital():
    if df.empty:
        return None
        
    hosp_counts = df['hospital'].value_counts().reset_index()
    hosp_counts.columns = ['hospital', 'count']
    
    fig = px.bar(
        hosp_counts, x='count', y='hospital', orientation='h',
        text='count',
        color='count',
        color_continuous_scale='Viridis',
        title="Casos Totales por Hospital"
    )
    return fig

def plot_heatmap_outcome():
    if df.empty:
        return None
        
    ct = pd.crosstab(df['hospital'], df['outcome'])
    fig = px.imshow(
        ct, 
        text_auto=True, 
        aspect="auto",
        title="Relación Hospital vs Desenlace"
    )
    return fig

def plot_violin_age():
    if df.empty:
        return None
        
    fig = px.violin(
        df, y="age", x="hospital", color="hospital",
        box=True, points="all",
        title="Distribución de Edad por Hospital"
    )
    fig.update_layout(showlegend=False)
    return fig

# =============================================================================
# 3. INTERFAZ GRADIO
# =============================================================================

with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🏥 Dashboard Epidemiológico (Gradio Version)")
    gr.Markdown("Análisis visual robusto de datos clínicos.")
    
    with gr.Row():
        with gr.Column():
            kpi_cases = gr.Number(label="Total Casos", value=0, interactive=False)
        with gr.Column():
            kpi_recov = gr.Textbox(label="Recuperados", value="0", interactive=False)
        with gr.Column():
            kpi_death = gr.Number(label="Fallecidos", value=0, interactive=False)
            
    with gr.Row():
        with gr.Column():
            plot1 = gr.Plot(label="Casos por Hospital")
            gr.Markdown("**Gráfico 1: Volumen de Pacientes.** Muestra cuántos pacientes ha atendido cada hospital. El 'Port Hospital' y los casos 'Missing' son los más frecuentes.")
        with gr.Column():
            plot2 = gr.Plot(label="Desenlaces")
            gr.Markdown("**Gráfico 2: Desenlaces Clínicos.** Mapa de calor que cruza el hospital con el resultado (Fallecido/Recuperado). Los colores más claros indican mayor frecuencia.")
        
    with gr.Row():
        with gr.Column():
            plot3 = gr.Plot(label="Edades")
            gr.Markdown("**Gráfico 3: Distribución de Edades.** Diagrama de violín que muestra la densidad de edad de los pacientes en cada centro. Permite ver si un hospital atiende a población más joven o anciana.")

    # Evento de carga inicial
    def load_dashboard():
        val1, val2, val3 = get_kpis()
        p1 = plot_bar_hospital()
        p2 = plot_heatmap_outcome()
        p3 = plot_violin_age()
        
        # Limpieza de valores numericos para componentes Number
        v1_num = float(val1.replace(",","")) if val1 and val1 != "0" else 0
        v3_num = float(val3.replace(",","")) if val3 and val3 != "0" else 0
        
        return v1_num, val2, v3_num, p1, p2, p3

    # Botón para refrescar (y auto-carga al iniciar es implícito si lo conectamos)
    refresh_btn = gr.Button("🔄 Cargar/Refrescar Datos")
    
    refresh_btn.click(
        fn=load_dashboard,
        outputs=[kpi_cases, kpi_recov, kpi_death, plot1, plot2, plot3]
    )
    
    # Cargar al inicio
    demo.load(
        fn=load_dashboard,
        outputs=[kpi_cases, kpi_recov, kpi_death, plot1, plot2, plot3]
    )

if __name__ == "__main__":
    print("Iniciando Gradio Dashboard en http://127.0.0.1:7860")
    demo.launch(server_port=7860, show_error=True)
