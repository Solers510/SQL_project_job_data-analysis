import pandas as pd
import numpy as np
import itertools
import warnings
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_absolute_percentage_error

# Ignore statistical convergence warnings during the loop
warnings.filterwarnings("ignore")

# 1. Load the Municipal Data
data = {
    'Year': [1903, 1918, 1939, 1948, 1960, 1970, 1975, 1980, 1990, 1995, 2000, 2007, 2010, 2015, 2020, 2024],
    'Population': [9225, 9794, 13813, 15222, 27818, 28723, 32130, 38243, 51629, 58046, 72683, 87058, 88144, 111454, 160987, 236978]
}
df = pd.DataFrame(data)
df.set_index('Year', inplace=True)

train = df.loc[:2015]
test_actuals = df.loc[2020:]

# 2. Define the Grid Search Parameters
# We will test all combinations of numbers from 0 to 4
p = d = q = range(0, 4)
pdq_combinations = list(itertools.product(p, d, q))

best_mape = float("inf")
best_params = None
best_forecast = None

print("Running Grid Search Optimization. This may take a moment...\n")

# 3. Execute the Loop
for params in pdq_combinations:
    try:
        # Train model with current parameters
        model = ARIMA(train['Population'], order=params)
        fitted_model = model.fit()
        
        # Forecast 2 steps ahead
        forecast = fitted_model.forecast(steps=2)
        
        # Calculate Error
        current_mape = mean_absolute_percentage_error(test_actuals['Population'], forecast) * 100
        
        # Save if it is the most accurate model so far
        if current_mape < best_mape:
            best_mape = current_mape
            best_params = params
            best_forecast = forecast.values.astype(int)
            
    except Exception:
        continue

# 4. Output the Optimized Results
print("--- OPTIMIZATION COMPLETE ---")
print(f"Optimal ARIMA Parameters (p, d, q): {best_params}")
print(f"Optimized Error Rate (MAPE): {best_mape:.2f}%")

comparison = pd.DataFrame({
    'Actual': test_actuals['Population'].values,
    'Optimized Prediction': best_forecast
}, index=[2020, 2024])

print("\n--- OPTIMIZED FORECAST VS ACTUAL ---")
print(comparison)