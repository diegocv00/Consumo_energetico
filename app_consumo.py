import streamlit as st
import joblib
import pandas as pd

# --- Título y descripción ---
st.title("⚡ Predicción de Consumo Energético Global 🌍")
st.write("""
    Esta aplicación permite predecir la electricidad generada a partir de combustibles fósiles (TWh)
    según factores energéticos, económicos y ambientales del país.
    """)

# --- Selección del modelo ---
st.sidebar.header("⚙️ Configuración del modelo")
modelo_seleccionado = st.sidebar.selectbox(
    "Selecciona el modelo de predicción:",
    ("XGBoost", "Random Forest")
)

# --- Cargar el modelo ---
model_path = "modelo_xgb.pkl" if modelo_seleccionado == "XGBoost" else "modelo_rf.pkl"

try:
    model = joblib.load(model_path)
    st.sidebar.success(f"Modelo '{modelo_seleccionado}' cargado correctamente ✅")
except Exception as e:
    st.sidebar.error(f"No se pudo cargar el modelo '{modelo_seleccionado}'. Error: {e}")
    st.stop()

st.header("Introduce los datos de entrada:")

col1, col2 = st.columns(2)

with col1:
    electricidad_renov = st.number_input(
        "Electricidad a partir de renovables (TWh)",
        min_value=0.0, max_value=150000.0, value=2000.0
    )
    
    energia_per_capita = st.number_input(
        "Consumo de energía primaria per cápita (kWh/person)",
        min_value=0.0, max_value=200000.0, value=50000.0
    )
    
    gdp_per_capita = st.number_input(
        "PIB per cápita (USD)",
        min_value=0.0, max_value=200000.0, value=20000.0
    )
    
    year = st.number_input(
        "Año",
        min_value=1990, max_value=2050, value=2020
    )

with col2:
    renov_share = st.number_input(
        "Cuota de energías renovables (%)",
        min_value=0.0, max_value=100.0, value=30.0
    )
    
    low_carbon = st.number_input(
        "Electricidad con bajas emisiones de carbono (% de la electricidad)",
        min_value=0.0, max_value=100.0, value=40.0
    )
    
    electricidad_nuclear = st.number_input(
        "Electricidad procedente de la energía nuclear (TWh)",
        min_value=0.0, max_value=10000.0, value=500.0
    )
    
    co2 = st.number_input(
        "Emisiones de CO₂ (kt)",
        min_value=0.0, max_value=50000000.0, value=50000.0
    )

# Crear DataFrame con el orden exacto de las columnas de entrenamiento
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

# --- Botón de predicción ---
if st.button("🔍 Predecir consumo energético"):
    try:
        prediccion = model.predict(input_data)[0]
        st.success(f"⚡ Predicción estimada ({modelo_seleccionado}): **{prediccion:.2f} TWh**")
    except Exception as e:

        st.error(f"Error al realizar la predicción: {e}")
