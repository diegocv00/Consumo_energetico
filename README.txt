⚡ Predicción del Consumo Energético de Combustibles Fósiles
Modelos de Machine Learning para análisis energético global 🌍🔥

Este proyecto emplea modelos de Machine Learning —Random Forest y XGBoost— para predecir el consumo energético proveniente de combustibles fósiles en distintos países.
Las predicciones se basan en variables energéticas y ambientales clave, entre ellas:

Electricidad generada a partir de energías renovables

Emisiones de CO₂

Cantidad de energía nuclear producida

Indicadores energéticos adicionales

Otras variables relacionadas con producción y consumo energético

Además, la aplicación incluye una interfaz interactiva donde puedes comparar ambos modelos, visualizar sus métricas y realizar predicciones personalizadas.

🚀 Funcionalidad del Proyecto

El flujo general del sistema se estructura en tres componentes principales:

Preparación de Datos

Limpieza, transformación y selección de variables relevantes.

Normalización y división del dataset en entrenamiento y prueba.

Entrenamiento de Modelos
Se entrenan y evalúan dos modelos: Random Forest y XGBoost.
Cada modelo se calibra para maximizar precisión y reducir error.

Aplicación Interactiva en Streamlit

Comparación visual de métricas

Panel para predicción personalizada

Explicaciones visuales del impacto de cada variable

Gráficos y análisis interpretables

Puedes acceder aquí:
https://consumoenergeticopredict.streamlit.app/

📊 Métricas de Desempeño

Random Forest

R² Train: 0.9789

R² Test: 0.949

RMSE Test: 84.32

XGBoost

R² Train: 0.975

R² Test: 0.992

RMSE Test: 33.138
