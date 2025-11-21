"""
Utility functions for AgriPredict
"""
import numpy as np

def mae_to_percentage_error(mae, mean_yield):
    """Convert MAE to % of average yield."""
    return (mae / mean_yield) * 100

def get_top_features(model, feature_names, n=5):
    """Return top n important features."""
    importances = model.feature_importances_
    idx = np.argsort(importances)[::-1][:n]
    return [(feature_names[i], importances[i]) for i in idx]