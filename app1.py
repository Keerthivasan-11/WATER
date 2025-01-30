import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import matplotlib.pyplot as plt

# Firebase Setup
firebase_credentials = st.secrets["firebase"]
cred = credentials.Certificate(firebase_credentials)
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://your-database-name.firebaseio.com/'
})

# Function to fetch data from Firebase Realtime Database
def get_water_levels():
    ref = db.reference('/')  # Root of the database, adjust to the appropriate node if needed
    data = ref.get()  # Fetch the data
    return data

# Function to draw tank with water level
def draw_tank(level, title):
    fig, ax = plt.subplots(figsize=(2, 4))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 100)
    
    # Tank outline
    ax.add_patch(plt.Rectangle((0, 0), 1, 100, fill=False, edgecolor='black', linewidth=2))
    
    # Water level
    ax.add_patch(plt.Rectangle((0, 0), 1, level, color='blue'))
    
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(title)
    return fig

# Streamlit UI
st.title("🚰 HMI Water Level Monitoring from Firebase")

# Fetch data from Firebase
data = get_water_levels()
if data:
    # Assuming the data contains 'RESERVOIR VOLUME', 'SUMP 1 VOLUME', 'SUMP 2 VOLUME'
    reservoir = data.get('RESERVOIR VOLUME', 0)
    sump1 = data.get('SUMP 1 VOLUME', 0)
    sump2 = data.get('SUMP 2 VOLUME', 0)
    
    # Display Tanks with respective water volumes
    col1, col2, col3 = st.columns(3)

    with col1:
        st.pyplot(draw_tank(reservoir, "Reservoir Volume"))

    with col2:
        st.pyplot(draw_tank(sump1, "Sump 1 Volume"))

    with col3:
        st.pyplot(draw_tank(sump2, "Sump 2 Volume"))
else:
    st.error("Error fetching data from Firebase. Please check your database.")
