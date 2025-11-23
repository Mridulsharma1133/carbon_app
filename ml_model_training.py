import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import joblib

# --- Emission factors ---
EMISSION_FACTORS = {
    "electricity": 0.85,
    "car": 0.21,
    "bike": 0.08,
    "public_transport": 0.04,
    "flight": 250,
    "waste": 0.45,
}

DIET_FACTORS = {
    "vegetarian": 125,
    "mixed": 165,
    "non_vegetarian": 210
}

# --- Generate synthetic data ---
n_samples = 1000
np.random.seed(42)

data = {
    "electricity_kwh": np.random.uniform(50, 600, n_samples),
    "car_km": np.random.uniform(0, 500, n_samples),
    "bike_km": np.random.uniform(0, 300, n_samples),
    "public_km": np.random.uniform(0, 600, n_samples),
    "flights_per_year": np.random.randint(0, 10, n_samples),
    "waste_kg": np.random.uniform(10, 80, n_samples),
    "diet_type": np.random.choice(["vegetarian", "mixed", "non_vegetarian"], n_samples)
}

df = pd.DataFrame(data)
# --- Calculate target emissions ---
def calc_emission(row):
    total = (
        row["electricity_kwh"] * EMISSION_FACTORS["electricity"]
        + row["car_km"] * EMISSION_FACTORS["car"]
        + row["bike_km"] * EMISSION_FACTORS["bike"]
        + row["public_km"] * EMISSION_FACTORS["public_transport"]
        + (row["flights_per_year"] / 12) * EMISSION_FACTORS["flight"]
        + row["waste_kg"] * EMISSION_FACTORS["waste"]
        + DIET_FACTORS[row["diet_type"]]
    )
    return total

df["total_emission"] = df.apply(calc_emission, axis=1)

#  Encode categorical variable (diet_type)
df = pd.get_dummies(df, columns=["diet_type"], drop_first=True)


X = df.drop(columns=["total_emission"])
y = df["total_emission"]

# Split into training and testing sets (80/20) 
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Check sizes 
print(f"Training samples: {len(X_train)}, Test samples: {len(X_test)}")

# --- Train model ---
model = LinearRegression()
model.fit(X_train, y_train)

# --- Evaluate ---
r2_score = model.score(X_test, y_test)
print(f"Model trained successfully with R² = {r2_score:.4f}")

# --- Save model ---
joblib.dump(model, "carbon_footprint_model.pkl")
print(model.feature_names_in_)
print("Model saved as carbon_footprint_model.pkl")
