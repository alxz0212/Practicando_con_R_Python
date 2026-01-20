import streamlit as st
import pandas as pd
import numpy as np
import math
from scipy import stats

# Configuración de la página
st.set_page_config(
    page_title="Conceptos Básicos de Python",
    page_icon="🐍",
    layout="wide"
)

# Título Principal
st.title("🐍 Conceptos Básicos en Python para Análisis de Datos")
st.markdown("""
Este dashboard interactivo acompaña al script `01_conceptos_basicos.py`.
Explora los diferentes conceptos matemáticos y estadísticos ejecutando el código y modificando variables.
""")

# Sidebar para navegación
opcion = st.sidebar.radio(
    "Selecciona un tema:",
    ("1. Python como Calculadora", "2. Variables", "3. Vectores y Estadística", "Ejercicio: David Villa")
)

# --- SECCIÓN 1: CALCULADORA ---
if opcion == "1. Python como Calculadora":
    st.header("1. Python como Calculadora")
    st.write("Python puede realizar operaciones matemáticas directas, similar a una calculadora científica.")

    st.subheader("Operaciones Básicas")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Suma Interactiva**")
        st.write("Ingresa dos números (máximo 10).")
        num1 = st.number_input("Número 1", max_value=10, value=2, step=1)
        num2 = st.number_input("Número 2", max_value=10, value=2, step=1)
        
        if st.button("Calcular Suma"):
            resultado = num1 + num2
            st.code(f"{num1} + {num2} = {resultado}")
            
    with col2:
        st.write("**Operación Avanzada**")
        st.latex(r"\log(1 + \sin(\pi/4))")
        if st.button("Calcular Operación"):
            resultado = math.log(1 + math.sin(math.pi/4))
            st.code(f"math.log(1 + math.sin(math.pi/4)) = {resultado}")

    st.subheader("Números Aleatorios")
    st.write("Generación de números aleatorios con distribución normal (media=0, desviación=1).")
    
    cantidad = st.slider("Cantidad de números a generar:", 1, 20, 8)
    if st.button("Generar Números"):
        random_numbers = np.random.normal(0, 1, cantidad)
        st.code(f"np.random.normal(0, 1, {cantidad})")
        st.write(random_numbers)
        st.bar_chart(random_numbers)

# --- SECCIÓN 2: VARIABLES ---
elif opcion == "2. Variables":
    st.header("2. Variables")
    st.write("En Python usamos `=` para asignar valores a variables.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Definición de Variables")
        x_val = st.number_input("Valor para 'x':", value=5)
        var_1_val = st.number_input("Valor para 'variable_1':", value=45)
        
        st.code(f"""
x = {x_val}
variable_1 = {var_1_val}
        """)
        
    with col2:
        st.subheader("Resultado")
        st.write(f"El valor de **x** es: `{x_val}`")
        st.write(f"El valor de **variable_1** es: `{var_1_val}`")
        st.info("Nota: Las variables en Python suelen usar `snake_case` (letras minúsculas separadas por guiones bajos).")

# --- SECCIÓN 3: VECTORES ---
elif opcion == "3. Vectores y Estadística":
    st.header("3. Vectores (NumPy Arrays) y Estadística")
    st.write("Usamos `numpy.array` para trabajar con vectores numéricos y realizar cálculos estadísticos eficientes.")

    st.subheader("Datos de Ejemplo: Pesos y Alturas")
    
    # Datos editables
    datos_defecto = pd.DataFrame({
        'Peso (kg)': [60, 72, 84, 65, 43, 87, 90, 56],
        'Altura (m)': [1.59, 1.75, 1.85, 1.60, 1.57, 1.90, 1.83, 1.73]
    })
    
    df_edit = st.data_editor(datos_defecto, num_rows="dynamic")
    
    peso = df_edit['Peso (kg)'].to_numpy()
    altura = df_edit['Altura (m)'].to_numpy()
    
    st.write(f"**Vector de Pesos extraído:** `{peso}`")
    st.write(f"**Longitud del vector:** `{len(peso)}`")

    st.subheader("Cálculo del IMC")
    st.latex(r"IMC = \frac{Peso}{Altura^2}")
    
    if len(peso) > 0 and len(altura) > 0:
        imc = peso / (altura ** 2)
        df_edit['IMC'] = imc
        st.dataframe(df_edit.style.highlight_max(axis=0))
    else:
        st.warning("Por favor asegúrate de tener datos en la tabla.")

    st.subheader("Estadísticos Descriptivos (Peso)")
    
    if len(peso) > 0:
        # Pestañas para fórmulas vs funciones
        tab1, tab2 = st.tabs(["Fórmulas Manuales", "Funciones NumPy/Pandas"])
        
        with tab1:
            st.markdown("### Cálculo Manual")
            media_manual = np.sum(peso) / len(peso)
            st.code(f"media = np.sum(peso) / len(peso) = {media_manual:.4f}")
            
            varianza_manual = np.sum((peso - media_manual)**2) / (len(peso) - 1)
            st.code(f"varianza (muestral) = np.sum((peso - media)**2) / (n - 1) = {varianza_manual:.4f}")
            
        with tab2:
            st.markdown("### Funciones Incorporadas")
            col_a, col_b, col_c = st.columns(3)
            col_a.metric("Media", f"{np.mean(peso):.4f}")
            col_b.metric("Varianza (ddof=1)", f"{np.var(peso, ddof=1):.4f}")
            col_c.metric("Desviación Típica", f"{np.std(peso, ddof=1):.4f}")
            
            st.text("Resumen con Pandas (describe):")
            st.write(pd.Series(peso).describe())

# --- EJERCICIO: DAVID VILLA ---
elif opcion == "Ejercicio: David Villa":
    st.header("Ejercicio: Estadísticas de David Villa")
    
    col_input, col_viz = st.columns([1, 2])
    
    with col_input:
        st.subheader("Datos")
        # Definición de datos
        temporada = ['00', '01', '02', '03', '04', '05', '06', '07', '08']
        partidos = [36, 44, 40, 46, 46, 40, 49, 41, 40]
        goles = [13, 20, 20, 20, 20, 28, 21, 22, 31]
        
        df_villa = pd.DataFrame({
            'temporada': temporada,
            'partidos': partidos,
            'goles': goles
        })
        
        # Permitir editar pequeños datos si se desea ver cómo cambia la correlación
        df_villa_edit = st.data_editor(df_villa, height=300)

    with col_viz:
        st.subheader("Visualización")
        st.line_chart(df_villa_edit.set_index('temporada')[['partidos', 'goles']])

    st.subheader("Análisis Estadístico")
    
    st.write("**1. Medias**")
    st.latex(r"\bar{x} = \frac{1}{n} \sum_{i=1}^{n} x_i")
    st.write(df_villa_edit[['partidos', 'goles']].mean())
    
    st.write("**2. Covarianza (Partidos vs Goles)**")
    st.latex(r"Cov(x, y) = \frac{\sum (x_i - \bar{x})(y_i - \bar{y})}{n-1}")
    cov = df_villa_edit[['partidos', 'goles']].cov().iloc[0, 1]
    st.metric("Covarianza", f"{cov:.4f}")
    
    st.write("**3. Correlación de Pearson**")
    st.latex(r"r = \frac{Cov(x, y)}{\sigma_x \sigma_y} = \frac{\sum (x_i - \bar{x})(y_i - \bar{y})}{\sqrt{\sum (x_i - \bar{x})^2 \sum (y_i - \bar{y})^2}}")
    corr = df_villa_edit[['partidos', 'goles']].corr().iloc[0, 1]
    st.metric("Correlación", f"{corr:.4f}")
    
    if corr > 0.7:
        st.success("Existe una correlación positiva fuerte.")
    elif corr > 0.3:
        st.info("Existe una correlación positiva moderada.")
    else:
        st.warning("La correlación es baja o negativa.")
