import streamlit as st
import joblib
import pandas as pd
import base64
import os

# --- Configuración de la página ---
st.set_page_config(
    page_title="EcoForecast 2050",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Función para cargar imagen de fondo ---
def get_base64_of_bin_file(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except FileNotFoundError:
        return None

# Ruta de la imagen
img_file = "hero_banner.png"
img_base64 = get_base64_of_bin_file(img_file)

if img_base64:
    hero_bg = f"""
    <style>
    .hero-container {{
        background-image: linear-gradient(rgba(15, 32, 39, 0.7), rgba(32, 58, 67, 0.8)), url("data:image/png;base64,{img_base64}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        height: 380px;
        border-radius: 0px 0px 30px 30px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        margin-bottom: 50px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.4);
    }}
    .hero-title {{
        color: #ffffff;
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 800;
        font-size: 3.5rem;
        text-transform: uppercase;
        margin-bottom: 15px;
        letter-spacing: 2px;
        background: linear-gradient(to right, #4facfe 0%, #00f2fe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0px 4px 10px rgba(0,0,0,0.3);
    }}
    .hero-subtitle {{
        color: #e0e0e0;
        font-family: 'Segoe UI Light', sans-serif;
        font-size: 1.4rem;
        font-weight: 300;
        max-width: 800px;
        line-height: 1.5;
    }}
    </style>
    """
    st.markdown(hero_bg, unsafe_allow_html=True)

# --- Estilos adicionales (CSS) ---
st.markdown("""
<style>
    .main {
        background-color: #ebedef;
        background-image: linear-gradient(to bottom right, #ebedef, #dfe4ea);
    }
    div.stButton > button {
        background: linear-gradient(45deg, #11998e, #38ef7d); /* Degradado moderno */
        color: white;
        border-radius: 50px;
        border: none;
        padding: 15px 40px;
        font-size: 20px; 
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        width: 100%;
        box-shadow: 0 5px 15px rgba(56, 239, 125, 0.4);
        transition: all 0.3s ease;
        cursor: pointer;
    }
    div.stButton > button:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 8px 25px rgba(56, 239, 125, 0.6);
        background: linear-gradient(45deg, #0e857b, #2ecc71);
    }
    h3 {
        color: #2c3e50;
        font-family: 'Segoe UI', sans-serif;
        font-weight: 600;
        margin-bottom: 25px;
    }
    .metric-result {
        background: linear-gradient(135deg, #ffffff 0%, #f1fcf5 100%);
        border: 1px solid #c8e6c9;
        padding: 40px;
        margin-top: 20px;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
    }
    .stNumberInput input {
        font-weight: bold;
        color: #2c3e50 !important;
    }
    /* Aumentar tamaño del selectbox del modelo */
    div[data-baseweb="select"] > div {
        min-height: 50px;
        font-size: 1.2rem;
    }
</style>
""", unsafe_allow_html=True)

# --- Hero Section Content ---
if img_base64:
    st.markdown("""
    <div class="hero-container">
        <div class="hero-title">EcoForecast 2050</div>
        <div class="hero-subtitle">
            Descubre cómo las variables económicas y ambientales 
            definirán la dependencia de combustibles fósiles en las próximas décadas.
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.title("EcoForecast 2050")

# --- Configuración del Modelo (MÁS GRANDE) ---
# Usamos columnas para darle un ancho considerable pero centrado. Antes era [1,2,1], ahora [1,6,1] para que sea mucho más ancho.
col_model_1, col_model_2, col_model_3 = st.columns([1, 6, 1])
with col_model_2:
    modelo_seleccionado = st.selectbox(
        "⚡ Modelo de inteligencia artificial sleccionado:",
        ("XGBoost", "Random Forest"),
    )

# Cargar modelo
@st.cache_resource
def load_model(model_name):
    path = "modelo_xgb.pkl" if model_name == "XGBoost" else "modelo_rf.pkl"
    return joblib.load(path)

try:
    model = load_model(modelo_seleccionado)
except Exception as e:
    st.error(f"Error crítico: No se pudo cargar el modelo '{modelo_seleccionado}'. ({e})")
    st.stop()

st.markdown("<br>", unsafe_allow_html=True)

# --- Formulario de Entrada ---

with st.container():
    col_left, col_right = st.columns(2, gap="large")
    
    with col_left:
        st.markdown("### 🏭 Economía")
        
        electricidad_renov = st.number_input(
            "Producción renovable (TWh)",
            min_value=0.0, value=2000.0, step=50.0, format="%.0f"
        )
        
        energia_per_capita = st.number_input(
            "Consumo per Cápita (kWh)",
            min_value=0.0, value=50000.0, step=100.0, format="%.0f"
        )
        
        gdp_per_capita = st.number_input(
            "PIB per Cápita (USD)",
            min_value=0.0, value=20000.0, step=100.0, format="%.0f"
        )
        
        year = st.slider("Año de proyección", 2025, 2050, 2035)

    with col_right:
        st.markdown("### 🌍 Sostenibilidad")
        
        renov_share = st.slider("Cuota de renovables (%)", 0.0, 100.0, 35.0)
        
        low_carbon = st.slider("Electricidad baja en carbono (%)", 0.0, 100.0, 45.0)
        
        electricidad_nuclear = st.number_input(
            "Energía nuclear (TWh)",
            min_value=0.0, value=500.0, step=10.0, format="%.0f"
        )
        
        co2 = st.number_input(
            "Emisiones CO₂ (kt)",
            min_value=0.0, value=50000.0, step=100.0, format="%.0f"
        )

# Preparar datos
input_data = pd.DataFrame({
    "Electricity from renewables (TWh)": [electricidad_renov],
    "Primary energy consumption per capita (kWh/person)": [energia_per_capita],
    "gdp_per_capita": [gdp_per_capita],
    "Year": [year],
    "Renewable energy share in the total final energy consumption (%)": [renov_share],
    "Low-carbon electricity (% electricity)": [low_carbon],
    "Electricity from nuclear (TWh)": [electricidad_nuclear],
    "Value_co2_emissions_kt_by_country": [co2]
})

st.markdown("<br><br>", unsafe_allow_html=True)

# --- Botón Izquierda ---
# Usamos columnas: botón en la primera columna (izquierda)
col_btn_1, col_btn_2, col_btn_3 = st.columns([2, 1, 1])

with col_btn_1:
    predict_btn = st.button(" Generar proyección futura ")

if predict_btn:
    try:
        with st.spinner('Procesando simulación...'):
            prediccion = model.predict(input_data)[0]
        
        st.markdown(f"""
        <div class="metric-result">
            <h4 style="margin:0; color:#7f8c8d; text-transform: uppercase; letter-spacing: 2px; font-size: 0.9rem;">
                Demanda Estimada de Combustibles Fósiles
            </h4>
            <h1 style="font-size: 4rem; background: -webkit-linear-gradient(#2c3e50, #4ca1af); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 15px 0; font-weight: 800;">
                {prediccion:,.0f} <span style="font-size: 1.5rem; color: #95a5a6; vertical-align: middle;">TWh</span>
            </h1>
            <p style="color: #999; font-style: italic;">Escenario proyectado para el año {year}</p>
        </div>
        """, unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Error en la simulación: {e}")