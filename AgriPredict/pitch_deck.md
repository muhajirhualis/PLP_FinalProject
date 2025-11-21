
# 🌾 AgriPredict: AI for Zero Hunger  
### *Forecasting Maize Yield for 500M Smallholder Farmers*

> ✨ *“AI can be the bridge between innovation and sustainability.”*  
> — UN Technology Envoy

---

## 🔴 Slide 1: The Crisis — Why We Can’t Wait

❌ **237 million people in sub-Saharan Africa face hunger.**  
🌾 **500 million smallholder farms** produce 80% of food — yet they **farm blind**.

### The Gap:
- National yield reports arrive **6+ months after harvest**  
- No district-level forecasts exist  
- Farmers guess → inputs wasted → crops lost → families go hungry  

> 🔔 **We’re missing the most powerful tool: foresight.**

---

## 🟢 Slide 2: Our Solution — Simple, Scalable, Sustainable

✅ **AgriPredict**  
*An open-source AI tool that forecasts maize yield **3 months before harvest** — using only free, publicly available data.*

### How?
1. 🛰️ Pull free data:  
   - `NDVI` (Sentinel-2)  
   - `Rainfall` (CHIRPS)  
   - `Soil` (SoilGrids)  
2. 🤖 Run lightweight ML model (**Random Forest**)  
3. 📱 Deliver forecast via **SMS or simple web app** — no smartphone needed.

> 💡 **No sensors. No surveys. No cost.** Built for the real world.


---

## 📊 Slide 3: Proof It Works — Rigorous & Responsible

| Metric | Performance |
|--------|-------------|
| **MAE** | `0.42` tonnes/ha |
| **R²** | `0.86` |
| **Avg. Yield** | `2.1` t/ha |
| **Relative Error** | **~20%** *(3× better than national averages)* |

✅ **NDVI at peak flowering** = strongest predictor *(agronomically validated)*  
✅ SHAP explainability: Transparent, trusted by farmers & agronomists

### 🌍 Ethical by Design:
- 🔒 **Bias-mitigated**: Spatial holdouts (by country)  
- ♿ **Inclusive**: USSD/SMS fallback for low-bandwidth areas  
- ♻️ **Sustainable**: Lightweight model → low compute → low carbon


---

## 🌍 Slide 4: Impact Pathway — From Code to Communities

### Who Benefits?

| Stakeholder | Impact |
|-------------|--------|
| **Farmers** | Optimize inputs, reduce loss, increase income (+15–30% estimated) |
| **Governments** | Target subsidies & extension services pre-harvest |
| **NGOs (WFP, FAO)** | Pre-position food aid in low-yield districts |

### Roadmap:
- 🚀 **2025**: Pilot in Ethiopia, Kenya, Malawi  
- 🌐 **2026**: Scale to 10+ African countries  
- 🤝 **2027**: Integrate with national agricultural advisory systems

> 🌾 **Goal: Empower 5M+ smallholder farmers with AI-powered foresight.**



---

## 🤝 Slide 5: Join the Harvest — Call to Action

We’re not just building a model —  
**We’re growing a movement for AI with conscience.**

### We Invite You To:
- 🌐 **Try the live demo**: [agri-predict.streamlit.app](https://agri-predict.streamlit.app)  
- 📂 **Contribute on GitHub**: [Here](https://github.com/muhajirhualis/PLP_FinalProject/blob/main/AgriPredict/)  
- 💡 **Partner with us**: Bring AgriPredict to your region.

> 🌍 *Technology should serve humanity — especially those who feed it.*

**Thank You**  
`#SDG2` `#AIforGood` `#PLPAcademy`



---

## 📎 Appendix: Tech Stack & Openness

- **Language**: Python  
- **Libraries**: Scikit-learn, SHAP, Streamlit, Pandas  
- **Data**: FAOStat, CHIRPS, SoilGrids, Google Earth Engine  
- **License**: MIT (open-source, no vendor lock-in)  
- **Deployment**: Streamlit Cloud (free), offline-capable

> ✅ **100% reproducible. 100% transparent. 100% for impact.**

---
