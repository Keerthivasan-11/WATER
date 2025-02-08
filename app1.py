import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import json
import matplotlib.pyplot as plt

st.set_page_config(page_title="Tank Monitoring", page_icon="🚰")

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

# 🔹 Fetch Water Levels
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

# 🔹 Streamlit UI
st.title("🚰 HMI Water Level Monitoring")

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
