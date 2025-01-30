import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import matplotlib.pyplot as plt

# ✅ Initialize Firebase only once
if not firebase_admin._apps:
    firebase_credentials = {
        "type": st.secrets["firebase"]["type"],
        "project_id": st.secrets["firebase"]["project_id"],
        "private_key_id": st.secrets["firebase"]["private_key_id"],
        "private_key": st.secrets["firebase"]["private_key"].replace('\\n', '\n'),
        "client_email": st.secrets["firebase"]["client_email"],
        "client_id": st.secrets["firebase"]["client_id"],
        "auth_uri": st.secrets["firebase"]["auth_uri"],
        "token_uri": st.secrets["firebase"]["token_uri"],
        "auth_provider_x509_cert_url": st.secrets["firebase"]["auth_provider_x509_cert_url"],
        "client_x509_cert_url": st.secrets["firebase"]["client_x509_cert_url"],
        "universe_domain": st.secrets["firebase"]["universe_domain"]
    }

    cred = credentials.Certificate(firebase_credentials)
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://your-database-name.firebaseio.com/'  # 🔹 Replace with your Firebase Realtime Database URL
    })

# 🔹 Fetch Water Levels from Firebase
def get_water_levels():
    ref = db.reference('/')  # Adjust if data is stored under a specific node
    data = ref.get()
    return data

# 🔹 Function to draw a tank based on water level
def draw_tank(level, title):
    fig, ax = plt.subplots(figsize=(2, 4))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 100)

    # Tank outline
    ax.add_patch(plt.Rectangle((0, 0), 1, 100, fill=False, edgecolor='black', linewidth=2))

    # Water level inside the tank
    ax.add_patch(plt.Rectangle((0, 0), 1, level, color='blue'))

    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(title)
    return fig

# 🔹 Streamlit UI
st.title("🚰 HMI Water Level Monitoring from Firebase")

# 🔹 Fetch Data from Firebase
data = get_water_levels()

if data:
    reservoir = data.get('RESERVOIR VOLUME', 0)  # Default to 0 if key is missing
    sump1 = data.get('SUMP 1 VOLUME', 0)
    sump2 = data.get('SUMP 2 VOLUME', 0)

    # 🔹 Display Water Tanks
    col1, col2, col3 = st.columns(3)

    with col1:
        st.pyplot(draw_tank(reservoir, "Reservoir"))

    with col2:
        st.pyplot(draw_tank(sump1, "Sump 1"))

    with col3:
        st.pyplot(draw_tank(sump2, "Sump 2"))
else:
    st.error("❌ Error fetching data from Firebase. Please check your database connection.")
