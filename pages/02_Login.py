import streamlit as st
from auth.auth_utils import register_user, login_user

st.set_page_config(page_title="Login / Register", layout="centered")
st.title("🔐 Login or Register")


# ------------------ SESSION STATE ------------------
if "is_authenticated" not in st.session_state:
    st.session_state["is_authenticated"] = False





# ------------------ HELPER ------------------
def clean_error(err):
    """Safely remove weird unicode characters from errors."""
    if not err:
        return ""
    try:
        return str(err).encode("utf-8", errors="ignore").decode("utf-8")
    except Exception:
        return "Unknown error occurred."


# ------------------ UI TABS ------------------
tabs = st.tabs(["Login", "Register"])



# ------------------ LOGIN TAB ------------------
with tabs[0]:
    st.subheader("Login to your account")

    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login"):
        with st.spinner("Verifying credentials..."):
            user_data, error = login_user(email, password)

        if error:
            st.error(f"Login failed: {clean_error(error)}")

        else:
            # Successful login
            if user_data and user_data.get("email"):
                st.session_state["user"] = {
                    "email": user_data["email"],
                    "id": user_data.get("id")
                }
                st.session_state["is_authenticated"] = True
                st.success(f"Logged in successfully as {user_data['email']}")

                st.rerun()
            else:
                st.error("Login failed: Unable to extract user details.")



# ------------------ REGISTER TAB ------------------
with tabs[1]:
    st.subheader("Create a new account")

    reg_email = st.text_input("Email", key="reg_email")
    reg_password = st.text_input("Password", type="password", key="reg_password")

    if st.button("Register"):
        with st.spinner("Creating your account..."):
            _, error = register_user(reg_email, reg_password)

        if error:
            st.error(f"Registration failed: {clean_error(error)}")

        else:
            st.success("Account created successfully! Please confirm your email and then log in.")
