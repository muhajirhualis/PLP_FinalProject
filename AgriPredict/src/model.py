"""
AgriPredict Core Model
Lightweight yield forecasting for SDG 2.
"""
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
import joblib
import os

# Ensure models dir exists
os.makedirs("models", exist_ok=True)

def load_data():
    df = pd.read_csv("data/processed/maize_yield_africa.csv")
    return df

def train_model():
    df = load_data()
    X = df[[
        'ndvi_peak', 'rain_cum_60d', 'temp_mean', 'soil_ph',
        'soil_organic_carbon', 'elevation', 'slope', 'planting_doy'
    ]]
    y = df['yield_tonnes_per_ha']

    # Spatial split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=df['country']
    )

    model = RandomForestRegressor(
        n_estimators=200,
        max_depth=12,
        random_state=42
    )
    model.fit(X_train, y_train)

    # Evaluate
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f"[Model] MAE: {mae:.2f} | R²: {r2:.2f}")
    
    # Save
    joblib.dump(model, "models/rf_agripredict.pkl")
    print("✅ Model saved to models/rf_agripredict.pkl")
    return model, mae, r2

if __name__ == "__main__":
    train_model()