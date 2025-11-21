# model_loader.py
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import joblib
import os

def load_model_and_data():
    """
    Load pre-trained model and metadata.
    For demo, creates synthetic model if not found.
    """
    model_path = "models/rf_agripredict.pkl"
    
    if os.path.exists(model_path):
        model = joblib.load(model_path)
        # Assume feature names from training
        feature_names = [
            'ndvi_peak', 'rain_cum_60d', 'temp_mean', 'soil_ph',
            'soil_organic_carbon', 'elevation', 'slope', 'planting_doy'
        ]
        # Dummy scaler (not used in RF, but included for extensibility)
        scaler = StandardScaler()
        scaler.fit(np.random.rand(100, len(feature_names)))
        return model, feature_names, scaler
    else:
        # Create synthetic model for demo
        model = RandomForestRegressor(n_estimators=10, max_depth=3, random_state=42)
        # Fit on dummy data
        X = np.random.rand(100, 8)
        y = 1.5 + 0.8 * X[:, 0] + 0.5 * X[:, 1] + np.random.normal(0, 0.2, 100)
        model.fit(X, y)
        
        feature_names = [
            'ndvi_peak', 'rain_cum_60d', 'temp_mean', 'soil_ph',
            'soil_organic_carbon', 'elevation', 'slope', 'planting_doy'
        ]
        scaler = None
        return model, feature_names, scaler