import os
import streamlit as st
import joblib
import pandas as pd

BASE_DIR = os.path.dirname(__file__)
# --- Cargar el modelo entrenado ---
ruta_modelo = os.path.join(BASE_DIR, "modelo_consumo.pkl")
model = joblib.load(ruta_modelo)


# --- Título y descripción ---
st.title("⚡ Predicción de Consumo Energético Global 🌍")
st.write("""
Esta aplicación usa un modelo XGB para predecir el consumo energético de combustibles fósiles de un país
según su producción de energias renovables y emisiones de CO₂.
""")

# --- Entradas del usuario ---
st.header("Introduce los datos de entrada:")

col1, col2 = st.columns(2)

with col1:
    
    electricidad_renovable = st.number_input(
        "Electricity from renewables (TWh)", 
        min_value=0.0, max_value=100000.0, value=2000.0
    )

with col2:
  
    emisiones_co2 = st.number_input(
        "CO₂ emissions (kt)", 
        min_value=0.0, max_value=100000000.0, value=50000.0
    )

# --- Crear DataFrame de entrada ---
input_data = pd.DataFrame({
    "Electricity from renewables (TWh)": [electricidad_renovable],
    "Value_co2_emissions_kt_by_country": [emisiones_co2]
})

# --- Botón de predicción ---
if st.button("🔍 Predecir consumo energético"):
    try:
        prediccion = model.predict(input_data)[0]
        st.success(f"⚡ Predicción estimada: **{prediccion:.2f} TWh**")
    except Exception as e:
        st.error(f"Error al realizar la predicción: {e}")





