import streamlit as st
import random
import smtplib
import pickle
from email.mime.text import MIMEText

# ---------------- EMAIL CONFIG ----------------
GMAIL_USER = "smartai.project.lab9@gmail.com"
GMAIL_APP_PASSWORD = "qbcy tskr wqym bdih"

# ---------------- LOAD MODEL SAFE ----------------
try:
    model = pickle.load(open("model.pkl", "rb"))
except:
    model = None

# ---------------- SESSION STATE ----------------
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

    if email is None or email.strip() == "":
        return None

    otp = str(random.randint(1000, 9999))

    msg = MIMEText(f"Your OTP is: {otp}")
    msg["Subject"] = "AI Project OTP Verification"
    msg["From"] = GMAIL_USER
    msg["To"] = email

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        server.send_message(msg)
        server.quit()
        return otp
    except:
        return None

# ---------------- UI ----------------
st.set_page_config(page_title="AI Smart System", layout="centered")
st.title("✨ AI Smart System")

menu = st.sidebar.radio("Menu", ["Signup", "Login", "Dashboard"])

# ---------------- SIGNUP ----------------
if menu == "Signup":
    st.subheader("Create Account (OTP Verification)")

    name = st.text_input("Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Send OTP"):

        if name.strip() == "" or email.strip() == "" or password.strip() == "":
            st.error("❌ Please fill all fields")

        elif not name.isalpha():
            st.error("❌ Name must contain only alphabets")

        else:
            otp = send_otp(email)

            if otp is None:
                st.error("❌ OTP not sent (check email or internet)")
            else:
                st.session_state.otp = otp
                st.success("📩 OTP sent to email")

    otp_input = st.text_input("Enter OTP")

    if st.button("Verify & Create Account"):

        if otp_input == st.session_state.otp and otp_input != "":
            st.session_state.users[email] = password
            st.success("🎉 Account Created Successfully")
        else:
            st.error("❌ Invalid OTP")

# ---------------- LOGIN ----------------
elif menu == "Login":
    st.subheader("Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        if email in st.session_state.users and st.session_state.users[email] == password:
            st.session_state.logged_in = True
            st.session_state.current_user = email
            st.success("🎉 Login Successful")
        else:
            st.error("❌ Invalid Credentials")

# ---------------- DASHBOARD ----------------
elif menu == "Dashboard":
    if st.session_state.logged_in:

        st.subheader(f"Welcome {st.session_state.current_user} 👑")

        # ✅ VARIABLES FIRST (IMPORTANT)
        study = st.slider("Study Level", 0, 10)
        sleep = st.slider("Sleep Level", 0, 10)
        social = st.slider("Social Activity", 0, 10)

        # ✅ BUTTON AFTER VARIABLES
        if st.button("Predict"):

            try:
                result = model.predict([[study, sleep, social]])

                if result[0] == 1:
                    st.success("🔥 High Performer")
                else:
                    st.warning("⚠ Needs Improvement")

            except Exception as e:
                st.error(f"Error: {e}")

        # ✅ LOGOUT
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.current_user = ""
            st.success("Logged out")

    else:
        st.warning("Please login first")