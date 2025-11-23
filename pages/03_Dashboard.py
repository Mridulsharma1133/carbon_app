import streamlit as st
import pandas as pd
from auth.supabase_client import supabase

# ------------------ AUTH CHECK ------------------
if not st.session_state.get("is_authenticated"):
    st.error("Please log in first to view your dashboard.")
    st.stop()

user_email = st.session_state["user"]["email"]

st.title("📊 Your Carbon Emission Dashboard")
st.write(f"Welcome back, **{user_email}** 👋")


# ------------------ FETCH USER DATA ------------------
response = (
    supabase.table("user_emissions")
    .select("*")
    .eq("email", user_email)
    .order("date")
    .execute()
)

if not response.data:
    st.info("You don’t have any emission records yet. Try logging a calculation first.")
    st.stop()

df = pd.DataFrame(response.data)
df['date'] = pd.to_datetime(df['date'])

st.subheader("📈 Emission Trend")
st.line_chart(df.set_index('date')['emission'])


# ------------------ SUMMARY METRICS ------------------
st.subheader("📌 Summary Metrics")

total = df["emission"].sum()
monthly_avg = df["emission"].mean()
latest = df["emission"].iloc[-1]

col1, col2, col3 = st.columns(3)
col1.metric("Total Emissions Recorded", f"{total:.2f} kg CO₂e")
col2.metric("Average Monthly Emission", f"{monthly_avg:.2f} kg CO₂e")
col3.metric("Latest Calculation", f"{latest:.2f} kg CO₂e")


# ------------------ DATA TABLE ------------------
st.subheader("📄 Your Historical Emission Records")
st.dataframe(df[['date', 'emission']].rename(columns={
    'date': 'Date',
    'emission': 'Emission (kg CO₂e)'
}))


# ------------------ DELETE ENTRY OPTION ------------------
st.subheader("🗑️ Delete an Entry")

selected_date = st.selectbox(
    "Select a date to delete an entry:",
    df['date'].dt.strftime("%Y-%m-%d %H:%M:%S").tolist()
)

if st.button("Delete Selected Entry"):
    supabase.table("user_emissions") \
        .delete() \
        .eq("email", user_email) \
        .eq("date", selected_date) \
        .execute()
    
    st.success("Entry deleted successfully!")
    st.rerun()
