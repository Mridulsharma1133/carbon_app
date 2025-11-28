import streamlit as st
import pandas as pd
from auth.supabase_client import supabase

# ---------------- AUTH CHECK ----------------
if not st.session_state.get("is_authenticated"):
    st.error("Please login first to view global comparison.")
    st.stop()

user_email = st.session_state["user"]["email"]

st.title("🌍 Global CO₂ per person Emission Comparison")
st.write(f"Hello **{user_email}**, see how your carbon footprint compares globally:")

# ---------------- FETCH USER LAST EMISSION ----------------
res = (
    supabase.table("user_emissions")
    .select("*")
    .eq("email", user_email)
    .order("date", desc=False)
    .execute()
)

df = pd.DataFrame(res.data)

if df.empty:
    st.warning("⚠️ No emission data found. Please calculate your footprint first.")
    st.stop()

latest_emission = df["emission"].iloc[-1]

st.subheader("Your Latest Monthly CO₂ Footprint")
st.info(f"**{latest_emission} kg CO₂e / month**")

# ---------------- GLOBAL DATA ----------------
global_data = {
    "Region": ["You", "World Avg", "India Avg", "USA Avg", "China Avg", "UK Avg"],
    "Emission": [
        latest_emission,
        440,   # World avg monthly ~ 5.2 tons/year
        160,   # India monthly avg
        1200,  # USA monthly avg
        900,   # China monthly avg
        600,   # UK monthly avg
    ]
}

df_global = pd.DataFrame(global_data)

# ---------------- BAR CHART ----------------
st.subheader("📊 Emission Comparison Chart")

st.bar_chart(df_global.set_index("Region"))

# ---------------- INSIGHTS ----------------
st.subheader("📘 Insights Based on Global Data")

def compare(user, avg, region):
    diff = user - avg
    if diff > 0:
        return f"🔴 Your emission is **{diff:.2f} kg CO₂e higher** than the {region} average."
    else:
        return f"🟢 Your emission is **{abs(diff):.2f} kg CO₂e lower** than the {region} average."

st.write(compare(latest_emission, 160, "India"))
st.write(compare(latest_emission, 440, "World"))
st.write(compare(latest_emission, 1200, "USA"))
st.write(compare(latest_emission, 900, "China"))
st.write(compare(latest_emission, 600, "UK"))
