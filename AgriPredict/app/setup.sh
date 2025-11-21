
---

## 🎁 Bonus: Auto-Generate Model on First Run (`setup.sh`)

Create `setup.sh` in repo root:

```bash
#!/bin/bash
echo "⚙️ Generating synthetic model for demo..."
python -c "
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib
import os

os.makedirs('models', exist_ok=True)

# Synthetic training
X = np.random.rand(500, 8)
y = 1.2 + 1.0*X[:,0] + 0.7*X[:,1] - 0.3*X[:,2] + np.random.normal(0, 0.3, 500)
model = RandomForestRegressor(n_estimators=50).fit(X, y)

joblib.dump(model, 'models/rf_agripredict.pkl')
print('✅ Model saved to models/rf_agripredict.pkl')
"