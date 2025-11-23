import joblib
import pandas as pd

rec_model = joblib.load("recommendation_model.pkl")

def generate_recommendations(elec, car, bike, public, flights, diet, waste):
    # Prepare input
    diet = diet.lower()
    row = pd.DataFrame([{
        "electricity_kwh": elec,
        "car_km": car,
        "bike_km": bike,
        "public_km": public,
        "flights_per_year": flights,
        "waste_kg": waste,
        "diet_type_vegetarian": 1 if diet == "vegetarian" else 0,
        "diet_type_mixed": 1 if diet == "mixed" else 0,
        "diet_type_non_vegetarian": 1 if diet == "non_vegetarian" else 0,
    }])

    # Predict shares
    shares = rec_model.predict(row)[0]

    labels = [
        "Electricity", "Car Travel", "Bike", "Public Transport",
        "Flights", "Waste", "Diet"
    ]

    share_dict = {labels[i]: shares[i] for i in range(len(labels))}
    sorted_shares = sorted(share_dict.items(), key=lambda x: x[1], reverse=True)

    # Top 3 contributors
    top1, top2, top3 = sorted_shares[:3]

    def make_text(name, value):
        pct = round(value * 100, 1)
        if name == "Car Travel":
            return f"🚗 *Car travel is {pct}% of your emissions*. Try reducing car usage or carpooling."
        if name == "Flights":
            return f"✈️ *Flights contribute {pct}%*. Avoid unnecessary flights and choose trains where possible."
        if name == "Diet":
            return f"🍽 *Diet is {pct}%*. Reducing meat intake can significantly lower impact."
        if name == "Electricity":
            return f"💡 *Electricity is {pct}%*. Switch to LEDs and adopt energy-saving habits."
        if name == "Waste":
            return f"🗑 *Waste is {pct}%*. Recycling and composting can reduce emissions."
        return f"{name}: {pct}% contribution."

    return [make_text(n, v) for n, v in (top1, top2, top3)]
