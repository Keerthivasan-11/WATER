import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import json
import matplotlib.pyplot as plt

st.set_page_config(page_title="Water Management System", page_icon="🚰")

# ✅ Firebase Credentials
firebase_secrets = dict(st.secrets["firebase"])
firebase_secrets["private_key"] = firebase_secrets["private_key"].replace('\\n', '\n')

# ✅ Initialize Firebase (only once)
if not firebase_admin._apps:
    try:
        cred = credentials.Certificate(firebase_secrets)
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://edge-watermgmt-default-rtdb.firebaseio.com/'
        })
        st.success("✅ Firebase connected successfully!")
    except Exception as e:
        st.error(f"❌ Firebase initialization failed: {e}")

# 🔹 Fetch Water Levels from Firebase
def get_water_levels():
    try:
        ref = db.reference('/')
        data = ref.get()
        return data
    except Exception as e:
        st.error(f"❌ Error fetching data from Firebase: {e}")
        return None

# 🔹 Function to draw tanks
def draw_tank(level, title, value):
    fig, ax = plt.subplots(figsize=(2, 5))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 100)

    # Tank outline
    ax.add_patch(plt.Rectangle((0, 0), 1, 100, fill=False, edgecolor='black', linewidth=2))

    # Water level inside the tank
    ax.add_patch(plt.Rectangle((0, 0), 1, level, color='blue'))

    # Display the water level **outside** the tank
    ax.text(0.5, 110, f"{value:.2f}%", fontsize=12, ha='center', color='black', fontweight='bold')

    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(title, fontsize=14)
    return fig

# 🔹 Function to update pump/reservoir status in Firebase
def update_pump_status(pump_name, status):
    try:
        ref = db.reference(f'/pumps/{pump_name}')  # Adjust when real data is added
        ref.set(status)
        st.success(f"✅ {pump_name} turned {'OFF' if status == 0 else 'ON'} successfully!")
    except Exception as e:
        st.error(f"❌ Failed to update {pump_name}: {e}")

# 🔹 Streamlit UI
st.title("🚰 Water Management System")

# Sidebar for Navigation
selected_page = st.sidebar.radio("Choose an Option:", ["Tank Monitoring", "Pump Control"])

# ========================== 🏗️ Tank Monitoring Page ==========================
if selected_page == "Tank Monitoring":
    st.header("📊 HMI Water Level Monitoring")

    # 🔹 Fetch Data from Firebase
    data = get_water_levels()

    if data:
        reservoir = data.get('RESERVOIR VOLUME', 0)
        sump1 = data.get('SUMP 1 VOLUME', 0)
        sump2 = data.get('SUMP 2 VOLUME', 0)

        # 🔹 Display Water Tanks
        col1, col2, col3 = st.columns(3)

        with col1:
            st.pyplot(draw_tank(reservoir, "Reservoir", reservoir))

        with col2:
            st.pyplot(draw_tank(sump1, "Sump 1", sump1))

        with col3:
            st.pyplot(draw_tank(sump2, "Sump 2", sump2))

    else:
        st.error("❌ No data found in Firebase.")

# ========================== 🔐 Pump Control Page ==========================
elif selected_page == "Pump Control":
    st.header("🔐 Pump Control Panel")

    # 🔐 Password Authentication
    PASSWORD = "admin123"  # Change this to a secure password

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        user_password = st.text_input("Enter Password:", type="password")
        if st.button("Login"):
            if user_password == PASSWORD:
                st.session_state.authenticated = True
                st.success("✅ Login successful!")
                st.rerun()
            else:
                st.error("❌ Incorrect password!")

    else:
        st.success("🔓 Access Granted: Control Panel Unlocked")

        # 🚰 Pump & Reservoir Control Buttons
        if st.button("Turn OFF Pump 1"):
            update_pump_status("Pump1", 0)

        if st.button("Turn OFF Pump 2"):
            update_pump_status("Pump2", 0)

        if st.button("Turn OFF Reservoir"):
            update_pump_status("Reservoir", 0)

        # Logout Button
        if st.button("Logout"):
            st.session_state.authenticated = False
            st.rerun()
