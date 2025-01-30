import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import matplotlib.pyplot as plt
import numpy as np

# Firebase Setup
cred = credentials.Certificate("path/to/serviceAccountKey.json")
firebase_admin.initialize_app(cred, {'databaseURL': 'https://your-database.firebaseio.com/'})

# Fetch Data
def get_water_levels():
    ref = db.reference('water_levels')
    data = ref.get()
    return data['reservoir'], data['sump1'], data['sump2']

# Visualization Function
def draw_tank(level, title):
    fig, ax = plt.subplots(figsize=(2, 4))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 100)
    
    # Tank shape
    ax.add_patch(plt.Rectangle((0, 0), 1, 100, fill=False, edgecolor='black', linewidth=2))
    
    # Water level
    ax.add_patch(plt.Rectangle((0, 0), 1, level, color='blue'))
    
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(title)
    return fig

st.title("Water Level Monitoring")

reservoir, sump1, sump2 = get_water_levels()

col1, col2, col3 = st.columns(3)
with col1:
    st.pyplot(draw_tank(reservoir, "Reservoir"))
with col2:
    st.pyplot(draw_tank(sump1, "Sump 1"))
with col3:
    st.pyplot(draw_tank(sump2, "Sump 2"))

# Auto-refresh
st.experimental_rerun()
