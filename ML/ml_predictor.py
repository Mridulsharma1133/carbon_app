import joblib
import numpy as np
import pandas as pd

# Load trained ML model
model = joblib.load("carbon_footprint_model.pkl")

def predict_emission(electricity_kwh, car_km, bike_km, public_km, flights_per_year, diet_type, waste_kg):
    data = {
        "electricity_kwh":[electricity_kwh],
        "car_km":[car_km],
        "bike_km":[bike_km],
        "public_km":[public_km],
        "flights_per_year":[flights_per_year],
        "waste_kg":[waste_kg],
        "diet_type_vegetarian":[1 if diet_type.lower() == "vegetarian" else 0],
        "diet_type_non_vegetarian":[1 if diet_type.lower() == "non_vegetarian" else 0],
       
    }

    df = pd.DataFrame(data)

    model_features = model.feature_names_in_
    df = df.reindex(columns=model_features, fill_value=0)

    #predict using model
    prediction = model.predict(df)
    return round(prediction[0], 2)