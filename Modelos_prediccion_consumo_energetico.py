from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, root_mean_squared_error
from xgboost import XGBRegressor
from sklearn.model_selection import GridSearchCV
import joblib
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
import pandas as pd

df = pd.read_csv(r"C:\Practica_Analisis_De_Datos\Consumo_energetico\global-data-on-sustainable-energy (1).csv")

#Limpieza de datos
df = df.dropna()
df = df.drop_duplicates().reset_index(drop=True)
df = df.fillna(df.mean(numeric_only=True))

# Selección de características y variable objetivo
x = df[['Electricity from renewables (TWh)','Primary energy consumption per capita (kWh/person)',
        'gdp_per_capita',"Year",'Renewable energy share in the total final energy consumption (%)',
        'Low-carbon electricity (% electricity)','Electricity from nuclear (TWh)' ,'Value_co2_emissions_kt_by_country' ]]
y = df["Electricity from fossil fuels (TWh)"]

# División de los datos en conjuntos de entrenamiento y prueba
x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.20,random_state=45)

#RANDOM FOREST 

pipeline_rf = Pipeline([
    ('scaler', StandardScaler()),  # Etapa de normalización
    ('random_forest', RandomForestRegressor(random_state=45))
])

parametros = {
    'random_forest__n_estimators': [100, 200],
    'random_forest__max_depth': [4, 6, 8],
    'random_forest__min_samples_split': [10, 20, 30],
    'random_forest__min_samples_leaf': [5, 10]
}


grid_search = GridSearchCV(pipeline_rf,param_grid=parametros,cv=5,scoring="r2",n_jobs=-1)

grid_search.fit(x_train,y_train)

mejor_random_forest = grid_search.best_estimator_
prediccion_test = mejor_random_forest.predict(x_test)
prediccion_train = mejor_random_forest.predict(x_train)

r2_train_rf = r2_score(y_train,prediccion_train)
r2_test_rf = r2_score(y_test,prediccion_test)
rmse_test_rf = root_mean_squared_error(y_test,prediccion_test)

print("R2 test:", r2_test_rf, "-- R2 train: ",r2_train_rf, "-- RMSE test: ",rmse_test_rf)
print("Mejores parámetros:", grid_search.best_params_)


#XGBOOST

pipeline_xgb = Pipeline([('scaler', StandardScaler()),('xgb', XGBRegressor(random_state=42, objective='reg:squarederror'))])

parametros = {
'xgb__max_depth': [2, 3, 4],
'xgb__learning_rate': [0.01, 0.05], 
 'xgb__reg_alpha': [1, 5, 10] , 
'xgb__reg_lambda': [10, 20], 
'xgb__min_child_weight': [3, 5, 10], 
'xgb__subsample': [0.4, 0.6], 
'xgb__colsample_bytree': [0.4, 0.6]
}



grid_xgb = GridSearchCV(pipeline_xgb, parametros, cv=5, scoring='r2', n_jobs=-1)
grid_xgb.fit(x_train, y_train)

mejor_xgb = grid_xgb.best_estimator_


y_pred_train = mejor_xgb.predict(x_train)
y_pred_test = mejor_xgb.predict(x_test)

r2_test_xgb = r2_score(y_test, y_pred_test)
r2_train_xgb = r2_score(y_train, y_pred_train)
rmse_test_xgb = root_mean_squared_error(y_test, y_pred_test)

print("Mejores parámetros:", grid_xgb.best_params_)
print(f"R² Train: {r2_train_xgb:.3f}")
print(f"R² Test:  {r2_test_xgb:.3f}")
print(f"RMSE Test: {rmse_test_xgb:.3f}")

# Guardar los modelos entrenados
joblib.dump(mejor_random_forest, "modelo_rf.pkl")
joblib.dump(mejor_xgb, "modelo_xgb.pkl")
