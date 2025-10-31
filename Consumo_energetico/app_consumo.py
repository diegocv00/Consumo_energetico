import streamlit as st
import joblib
import pandas as pd

# --- Título y descripción ---
st.title("⚡ Predicción de Consumo Energético Global 🌍")
st.write("""
Esta aplicación permite predecir el consumo energético de combustibles fósiles de un país
según su producción de energías renovables y emisiones de CO₂.

Puedes seleccionar el modelo de predicción que deseas utilizar.
""")

# --- Selección del modelo ---
st.sidebar.header("⚙️ Configuración del modelo")
modelo_seleccionado = st.sidebar.selectbox(
    "Selecciona el modelo de predicción:",
    ("XGBoost", "Random Forest")
)

# --- Cargar el modelo según la selección ---
if modelo_seleccionado == "XGBoost":
    model_path = "modelo_xgb.pkl"
else:
    model_path = "modelo_rf.pkl"

try:
    model = joblib.load(model_path)
    st.sidebar.success(f"Modelo '{modelo_seleccionado}' cargado correctamente ✅")
except Exception as e:
    st.sidebar.error(f"No se pudo cargar el modelo '{modelo_seleccionado}'. Error: {e}")
    st.stop()

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
        st.success(f"⚡ Predicción estimada con {modelo_seleccionado}: **{prediccion:.2f} TWh**")
    except Exception as e:
        st.error(f"Error al realizar la predicción: {e}")
