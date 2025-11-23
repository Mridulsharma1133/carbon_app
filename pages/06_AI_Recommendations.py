import streamlit as st
from auth.supabase_client import supabase

from ML.ai_recommender import generate_recommendations

st.title("🤖 AI-Powered Carbon Reduction Recommendations")

if not st.session_state.get("is_authenticated"):
    st.error("Please login first.")
    st.stop()

user_email = st.session_state["user"]["email"]
st.write(f"Welcome, **{user_email}**!")

# Check if calculator stored user inputs
if "last_inputs" not in st.session_state:
    st.warning("⚠️ Please calculate your carbon footprint first.")
    st.stop()

inp = st.session_state["last_inputs"]

st.subheader("📈 Your Latest Inputs")
st.json(inp)

# Generate AI Recommendations
recs = generate_recommendations(
    inp["electricity"], inp["car"], inp["bike"],
    inp["public"], inp["flights"], inp["diet"], inp["waste"]
)

st.subheader("🧠 Personalized AI Suggestions")
for r in recs:
    st.write("🔹 " + r)
