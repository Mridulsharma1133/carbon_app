import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib

# ---------- Emission Factors ----------
EMISSION_FACTORS = {
    "electricity": 0.85,
    "car": 0.21,
    "bike": 0.08,
    "public_transport": 0.04,
    "flight": 250 / 12,
    "waste": 0.45,
}

DIET_FACTORS = {
    "vegetarian": 125,
    "mixed": 165,
    "non_vegetarian": 210,
}

diet_map = ["vegetarian", "mixed", "non_vegetarian"]

# ---------- Generate Synthetic Dataset ----------
samples = 1000

data = {
    "electricity_kwh": np.random.randint(50, 600, samples),
    "car_km": np.random.randint(0, 800, samples),
    "bike_km": np.random.randint(0, 300, samples),
    "public_km": np.random.randint(0, 500, samples),
    "flights_per_year": np.random.randint(0, 10, samples),
    "waste_kg": np.random.randint(5, 60, samples),
    "diet_type": np.random.choice(diet_map, samples)
}

df = pd.DataFrame(data)

# ---------- Calculate Emissions ----------
df["elec_emission"] = df["electricity_kwh"] * EMISSION_FACTORS["electricity"]
df["car_emission"] = df["car_km"] * EMISSION_FACTORS["car"]
df["bike_emission"] = df["bike_km"] * EMISSION_FACTORS["bike"]
df["public_emission"] = df["public_km"] * EMISSION_FACTORS["public_transport"]
df["flight_emission"] = df["flights_per_year"] * EMISSION_FACTORS["flight"]
df["waste_emission"] = df["waste_kg"] * EMISSION_FACTORS["waste"]
df["diet_emission"] = df["diet_type"].map(DIET_FACTORS)

df["total_emission"] = (
    df["elec_emission"] + df["car_emission"] + df["bike_emission"] +
    df["public_emission"] + df["flight_emission"] +
    df["waste_emission"] + df["diet_emission"]
)

# ---------- Compute Shares ----------
emission_cols = [
    "elec_emission", "car_emission", "bike_emission",
    "public_emission", "flight_emission",
    "waste_emission", "diet_emission"
]

for col in emission_cols:
    df[col.replace("_emission", "_share")] = df[col] / df["total_emission"]

# ---------- Prepare ML Input ----------
df_encoded = pd.get_dummies(df, columns=["diet_type"])

X = df_encoded[[
    "electricity_kwh", "car_km", "bike_km", "public_km",
    "flights_per_year", "waste_kg",
    "diet_type_vegetarian", "diet_type_mixed", "diet_type_non_vegetarian"
]]

y = df_encoded[[col.replace("_emission", "_share") for col in emission_cols]]

model = RandomForestRegressor(n_estimators=200, random_state=42)
model.fit(X, y)

# Save model
joblib.dump(model, "recommendation_model.pkl")


print("AI Recommendation Model Trained & Saved Successfully!")
