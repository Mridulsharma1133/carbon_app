import streamlit as st

st.set_page_config(page_title="AI Carbon Calculator", layout="wide")

st.markdown("""
    <style>
        [data-testid="stSidebarNav"] {display: none;}
    </style>
""", unsafe_allow_html=True)



# Initialize session state
if "is_authenticated" not in st.session_state:
    st.session_state["is_authenticated"] = False

if "user" not in st.session_state:
    st.session_state["user"] = None

# ------------- SIDEBAR NAVIGATION -------------

st.sidebar.title("🌱 Navigation")

# If user is logged in
if st.session_state["is_authenticated"] and st.session_state["user"]:
    
    user_email = st.session_state["user"]["email"]
    st.sidebar.success(f"Logged in as: {user_email}")

    st.sidebar.page_link("pages/01_Home.py", label="🏠 Home")
    st.sidebar.page_link("pages/03_Dashboard.py", label="📊 Dashboard")
    st.sidebar.page_link("pages/04_Carbon_Calculator.py", label="🧮 Carbon Calculator")
    st.sidebar.page_link("pages/05_Global_Comparison.py", label="🌍 Global Comparison")
    st.sidebar.page_link("pages/06_AI_Recommendations.py", label="🤖 AI Recommendations")

    if st.sidebar.button("Logout"):
        st.session_state.clear()
        st.rerun()

# If user is logged out → show only login page
else:
    st.sidebar.page_link("pages/01_Home.py", label="🏠 Home")
    st.sidebar.page_link("pages/02_Login.py", label="🔐 Login / Register")

# Main placeholder
st.title("AI Carbon Footprint App")
st.write("Use the sidebar to navigate.")


