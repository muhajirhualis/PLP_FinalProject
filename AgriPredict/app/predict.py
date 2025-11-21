# predict.py
import numpy as np
import shap

def predict_yield(model, features_dict, feature_names):
    """
    Predict yield and generate SHAP explanation.
    """
    # Convert dict to array
    X = np.array([features_dict[f] for f in feature_names]).reshape(1, -1)
    
    # Predict
    pred = model.predict(X)[0]
    
    # SHAP explanation (TreeExplainer for RF)
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X)[0]  # [0] for first (only) sample
    expected_value = explainer.expected_value
    
    return pred, shap_values, expected_value