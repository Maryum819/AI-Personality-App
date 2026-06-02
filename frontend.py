import streamlit as st
import random
import smtplib
import ssl
import os
import pickle

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="AI Personality System", layout="centered")

# ---------------- CSS (UI POLISH) ----------------
st.markdown("""
<style>
body {
    background-color: #0e1117;
    color: white;
}
.stButton>button {
    background-color: #4CAF50;
    color: white;
    border-radius: 10px;
    height: 40px;
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

# ---------------- EMAIL CONFIG ----------------
GMAIL_USER = "smartai.project.lab9@gmail.com"
GMAIL_APP_PASSWORD = "qbcy tskr wqym bdih"

# ---------------- LOAD MODEL SAFELY ----------------
model = None

if os.path.exists("model.pkl"):
    try:
        with open("model.pkl", "rb") as f:
            model = pickle.load(f)
    except:
        model = None

# ---------------- SESSION ----------------
if "users" not in st.session_state:
    st.session_state.users = {}

if "otp" not in st.session_state:
    st.session_state.otp = ""

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "current_user" not in st.session_state:
    st.session_state.current_user = ""

# ---------------- OTP FUNCTION ----------------
def send_otp(email):

    if email.strip() == "":
        return None

    otp = str(random.randint(1000, 9999))

    message = f"Subject: OTP Code\n\nYour OTP is: {otp}"

    try:
        context = ssl.create_default_context()
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context)
        server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        server.sendmail(GMAIL_USER, email, message)
        server.quit()
        return otp

    except:
        return None

# ---------------- TITLE ----------------
st.title("✨ AI Personality Prediction System")

menu = st.sidebar.radio("Menu", ["Signup", "Login", "Dashboard"])

# ---------------- SIGNUP ----------------
if menu == "Signup":

    st.subheader("Create Account")

    name = st.text_input("Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Send OTP"):

        if name == "" or email == "" or password == "":
            st.error("Fill all fields")

        elif not name.isalpha():
            st.error("Name must contain only alphabets")

        else:
            otp = send_otp(email)

            if otp:
                st.session_state.otp = otp
                st.success("OTP sent successfully")
            else:
                st.error("OTP not sent")

    otp_input = st.text_input("Enter OTP")

    if st.button("Verify & Register"):

        if otp_input == st.session_state.otp and otp_input != "":
            st.session_state.users[email] = password
            st.success("Account created successfully")
        else:
            st.error("Invalid OTP")

# ---------------- LOGIN ----------------
elif menu == "Login":

    st.subheader("Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        if email in st.session_state.users and st.session_state.users[email] == password:
            st.session_state.logged_in = True
            st.session_state.current_user = email
            st.success("Login successful")
        else:
            st.error("Invalid credentials")

# ---------------- DASHBOARD ----------------
elif menu == "Dashboard":

    if st.session_state.logged_in:

        st.subheader(f"Welcome {st.session_state.current_user}")

        study = st.slider("Study Level", 0, 10)
        sleep = st.slider("Sleep Level", 0, 10)
        social = st.slider("Social Activity", 0, 10)

        if st.button("Predict Personality"):

            if model is None:
                st.error("Model not loaded")
            else:
                try:
                    result = model.predict([[study, sleep, social]])

                    if result[0] == 1:
                        st.success("🔥 You are highly focused and disciplined. You have strong potential to achieve big goals!")
                    else:
                        st.warning("⚠ You need better balance in study and lifestyle.")

                except Exception as e:
                    st.error(f"Error: {e}")

        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.current_user = ""
            st.success("Logged out successfully")

    else:
        st.warning("Please login first")
