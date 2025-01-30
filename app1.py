import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import json
import tempfile
import matplotlib.pyplot as plt

# ✅ Extract and properly format the private key from Streamlit secrets
firebase_secrets = dict(st.secrets["firebase"])

# ✅ Ensure the private key is correctly formatted (replace '\\n' with actual line breaks)
firebase_secrets["private_key"] = firebase_secrets["private_key"].replace('\\n', '\n')

# ✅ Write the credentials to a temporary JSON file
with tempfile.NamedTemporaryFile(delete=False, mode="w", suffix=".json") as temp_file:
    json.dump(firebase_secrets, temp_file)  # Write JSON content
    temp_file_path = temp_file.name  # Save the file path for Firebase to use

# ✅ Initialize Firebase using the temporary JSON file
if not firebase_admin._apps:
    try:
        cred = credentials.Certificate(temp_file_path)  # ✅ Pass the temp file path
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://your-database-name.firebaseio.com/'  # 🔹 Replace with your actual Firebase Database URL
        })
    except Exception as e:
        st.error(f"❌ Firebase initialization failed: {e}")

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
