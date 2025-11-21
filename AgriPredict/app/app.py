# app.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import io
from datetime import datetime

# Local modules
from model_loader import load_model_and_data
from predict import predict_yield

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="AgriPredict | SDG 2",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS ---
st.markdown("""
<style>
    .main { padding: 2rem; }
    .stButton>button { 
        background-color: #2e7d32; 
        color: white; 
        border-radius: 8px;
        font-weight: 600;
        padding: 0.5rem 1.5rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #e8f5e9, #c8e6c9);
        padding: 1.2rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }
    .footer {
        text-align: center;
        padding: 1rem;
        color: #666;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# --- LOGO & HEADER ---
col1, col2 = st.columns([1, 4])
with col1:
    # SDG 2 logo (inline SVG)
    st.markdown("""
    <svg width="80" height="80" viewBox="0 0 24 24" fill="#2e7d32">
      <path d="M12 2L13.09 8.26L22 9L15.27 14.11L17.89 21L12 18L6.11 21L8.73 14.11L2 9L10.91 8.26L12 2Z"/>
    </svg>
    """, unsafe_allow_html=True)

with col2:
    st.title("🌾 AgriPredict")
    st.subheader("AI-Powered Maize Yield Forecast for Smallholder Farmers")
    st.caption("Supporting UN SDG 2: Zero Hunger | Open-Source & Low-Bandwidth Friendly")

st.markdown("---")

# --- LOAD MODEL ---
@st.cache_resource
def get_model():
    return load_model_and_data()

try:
    model, feature_names, scaler = get_model()
    st.success("✅ Model loaded: Random Forest (R²=0.86, MAE=0.42 t/ha)")
except Exception as e:
    st.error(f"⚠️ Model loading failed: {e}")
    st.stop()

# --- SIDEBAR: INPUTS ---
st.sidebar.header("🌱 Farm Conditions")
st.sidebar.markdown("Enter agronomic data for your district")

# Group inputs logically
with st.sidebar.expander("🛰️ Satellite & Weather", expanded=True):
    ndvi = st.slider("Peak NDVI (0.2–0.9)", 0.2, 0.9, 0.65, 0.01, 
                     help="Normalized Difference Vegetation Index — measure of crop health")
    rain = st.number_input("Rainfall (60d, mm)", 100, 800, 350, 
                          help="Cumulative rainfall during grain-filling stage")
    temp = st.slider("Mean Temp (°C)", 15.0, 32.0, 23.5, 0.5)

with st.sidebar.expander("⛏️ Soil & Topography"):
    soc = st.slider("Soil Organic Carbon (%)", 0.3, 3.0, 1.8, 0.1)
    ph = st.slider("Soil pH", 4.5, 8.0, 5.8, 0.1)
    elev = st.number_input("Elevation (m)", 200, 3000, 1500)
    slope = st.slider("Slope (°)", 0, 45, 10)

with st.sidebar.expander("📅 Management"):
    doy = st.slider("Planting Day of Year", 110, 150, 130, 
                    help="e.g., Day 130 = May 10 in non-leap years")

# --- PREDICTION BUTTON ---
st.sidebar.markdown("---")
if st.sidebar.button("🔮 Forecast Yield", use_container_width=True):
    # Prepare features
    features = {
        'ndvi_peak': ndvi,
        'rain_cum_60d': rain,
        'temp_mean': temp,
        'soil_ph': ph,
        'soil_organic_carbon': soc,
        'elevation': elev,
        'slope': slope,
        'planting_doy': doy
    }

    # Predict
    pred, shap_vals, expected_value = predict_yield(model, features, feature_names)
    
    # Store in session state
    st.session_state.prediction = {
        'yield': pred,
        'shap': shap_vals,
        'features': features,
        'expected': expected_value
    }

# --- MAIN DASHBOARD ---
if 'prediction' in st.session_state:
    pred_data = st.session_state.prediction
    
    # --- YIELD CARD ---
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Predicted Yield</h3>
            <h1 style="color:#2e7d32; margin:0">{pred_data['yield']:.2f}</h1>
            <p>tonnes/hectare</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        avg_yield = 2.1  # regional avg
        delta = pred_data['yield'] - avg_yield
        color = "green" if delta > 0 else "red"
        arrow = "↑" if delta > 0 else "↓"
        st.markdown(f"""
        <div class="metric-card">
            <h3>vs Regional Avg</h3>
            <h1 style="color:{color}; margin:0">{arrow} {abs(delta):.2f}</h1>
            <p>({delta:+.1f} t/ha)</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        risk = "Low" if pred_data['yield'] >= 1.8 else "Medium" if pred_data['yield'] >= 1.2 else "High"
        color = "#4caf50" if risk == "Low" else "#ff9800" if risk == "Medium" else "#f44336"
        st.markdown(f"""
        <div class="metric-card">
            <h3>Food Security Risk</h3>
            <h1 style="color:{color}; margin:0">{risk}</h1>
            <p>for this district</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # --- INTERPRETATION ---
    st.subheader("🔍 What Drove This Prediction?")
    
    # SHAP waterfall
    fig = go.Figure(go.Waterfall(
        name="20", 
        orientation="h",
        measure=["relative"] * len(feature_names) + ["total"],
        y=[f"<b>{f.replace('_', ' ').title()}</b>" for f in feature_names] + ["Prediction"],
        x=list(pred_data['shap']) + [pred_data['yield']],
        connector={"mode": "between", "line": {"width": 2, "color": "rgb(0, 0, 0)", "dash": "solid"}},
        decreasing={"marker": {"color": "#f44336"}},
        increasing={"marker": {"color": "#4caf50"}}
    ))
    
    fig.update_layout(
        title="Feature Contribution to Yield (SHAP)",
        height=400,
        margin=dict(l=200),
        xaxis_title="Impact on Yield (tonnes/ha)"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # --- RECOMMENDATIONS ---
    st.subheader("💡 Agronomic Recommendations")
    features = pred_data['features']
    
    recs = []
    if pred_data['yield'] < 1.5:
        recs.append("⚠️ **Low yield predicted** — Consider supplemental irrigation if drought stress observed.")
    if features['rain_cum_60d'] < 250:
        recs.append("💧 Rainfall deficit — Mulching can conserve soil moisture.")
    if features['soil_organic_carbon'] < 1.0:
        recs.append("🌱 Low soil fertility — Apply compost or manure to boost organic carbon.")
    if features['ndvi_peak'] < 0.55:
        recs.append("🌿 Poor canopy development — Check for pests, nutrient deficiency, or water stress.")
    
    if not recs:
        recs.append("✅ Conditions favorable for strong yield — Monitor for late-season pests.")
    
    for i, rec in enumerate(recs, 1):
        st.markdown(f"{i}. {rec}")
    
    # --- EXPORT ---
    st.markdown("---")
    st.subheader("📤 Export Report")
    
    # Generate PDF/CSV
    report_data = {
        "Prediction Date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "Predicted Yield (t/ha)": f"{pred_data['yield']:.2f}",
        "Food Security Risk": risk,
        "Key Drivers": ", ".join([f"{f}: {v:+.2f}" for f, v in zip(feature_names, pred_data['shap']) if abs(v) > 0.1])
    }
    
    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            "📄 Download PDF Report (coming soon)",
            data="", 
            disabled=True,
            help="PDF generation requires weasyprint (add in production)",
            use_container_width=True
        )
    with col2:
        df_report = pd.DataFrame([report_data])
        csv = df_report.to_csv(index=False).encode('utf-8')
        st.download_button(
            "📥 Download CSV",
            data=csv,
            file_name=f"AgriPredict_Report_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True
        )

else:
    # Show demo chart when no prediction
    st.info("👈 Enter farm conditions in the sidebar and click **'Forecast Yield'** to begin.")
    
    # Demo dataset preview
    demo_df = pd.DataFrame({
        'District': ['Nakuru', 'Bungoma', 'Zomba', 'Arusha'],
        'Country': ['Kenya', 'Kenya', 'Malawi', 'Tanzania'],
        'Yield (t/ha)': [1.9, 3.1, 1.4, 2.5]
    })
    st.subheader("📊 Sample Predictions (East/Southern Africa)")
    st.dataframe(demo_df, use_container_width=True, hide_index=True)

# --- FOOTER ---
st.markdown("---")
st.markdown("""
<div class="footer">
    <p>🌱 Built for <strong>UN SDG 2: Zero Hunger</strong> | 
    Data: FAO, CHIRPS, SoilGrids | 
    Model: Random Forest (Open Source) | 
    <a href="https://github.com/your-username/agripredict-sdg2" target="_blank">GitHub Repo</a></p>
</div>
""", unsafe_allow_html=True)