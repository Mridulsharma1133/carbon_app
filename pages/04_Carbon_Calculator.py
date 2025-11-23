import streamlit as st
import pandas as pd
from datetime import datetime
from ML.ml_predictor import predict_emission
from auth.supabase_client import supabase


# ------------------ AUTH CHECK ------------------
if not st.session_state.get("is_authenticated"):
    st.error("Please log in to access the Carbon Calculator.")
    st.stop()

user_email = st.session_state["user"]["email"]

st.title("🧮 Carbon Footprint Calculator")
st.write("Estimate your **monthly carbon emissions (kg CO₂e)** using your lifestyle inputs.")


# ------------------ INPUT FORM ------------------
with st.form("carbon_form"):
    st.subheader("Enter Monthly Details")

    col1, col2 = st.columns(2)

    with col1:
        electricity_kwh = st.number_input("Electricity usage (kWh/month)", min_value=0.0, value=150.0)
        car_km = st.number_input("Car distance travelled (km/month)", min_value=0.0, value=80.0)
        bike_km = st.number_input("Bike travel (km/month)", min_value=0.0, value=30.0)

    with col2:
        public_km = st.number_input("Public transport (km/month)", min_value=0.0, value=100.0)
        flights_per_year = st.number_input("Flights per year", min_value=0, value=1)
        waste_kg = st.number_input("Waste generated (kg/month)", min_value=0.0, value=25.0)
        diet_type = st.selectbox("Diet Type", ["Vegetarian", "Mixed", "Non_Vegetarian"])

    calculate = st.form_submit_button("Calculate Footprint")


# ------------------ PROCESS CALCULATION ------------------
if calculate:

    st.session_state["last_inputs"] = {
        "electricity": electricity_kwh,
        "car": car_km,
        "bike": bike_km,
        "public": public_km,
        "flights": flights_per_year,
        "diet": diet_type,
        "waste": waste_kg
    }

    total_emission = predict_emission(
        electricity_kwh, car_km, bike_km, public_km, flights_per_year, diet_type, waste_kg
    )

    st.success(f"Your estimated monthly carbon footprint is **{total_emission} kg CO₂e**")

    # Save result to Supabase
    supabase.table("user_emissions").insert({
        "email": user_email,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "emission": total_emission
    }).execute()


    # ------------------ SHOW TREND ------------------
    st.subheader("📈 Your Emission Trend")

    data = (
        supabase.table("user_emissions")
        .select("*")
        .eq("email", user_email)
        .order("date")
        .execute()
    )

    df = pd.DataFrame(data.data)

    if df.empty:
        st.info("No previous emission records found.")
    else:
        df["date"] = pd.to_datetime(df["date"])
        st.line_chart(df.set_index("date")["emission"])

        # Show last 3 predictions
        st.subheader("📄 Recent Calculations")
        recent = df.sort_values("date", ascending=False).head(3)
        st.table(recent[["date", "emission"]])
