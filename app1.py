import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import time

# Hardcoded credentials (Replace with a secure method later)
VALID_USERNAME = "admin"
VALID_PASSWORD = "password123"

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

# Initialize session states for water levels
if "reservoir" not in st.session_state:
    st.session_state.reservoir = 50
if "sump1" not in st.session_state:
    st.session_state.sump1 = 30
if "sump2" not in st.session_state:
    st.session_state.sump2 = 70
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Streamlit UI
st.title("🏭 HMI Water Level Monitoring 🚰")

# Display Tanks (HMI always visible)
col1, col2, col3 = st.columns(3)
with col1:
    st.pyplot(draw_tank(st.session_state.reservoir, "Reservoir"))
with col2:
    st.pyplot(draw_tank(st.session_state.sump1, "Sump 1"))
with col3:
    st.pyplot(draw_tank(st.session_state.sump2, "Sump 2"))

# Sliders for Manual Control (Visible for everyone)
st.session_state.reservoir = st.slider("Reservoir Level", 0, 100, st.session_state.reservoir)
st.session_state.sump1 = st.slider("Sump 1 Level", 0, 100, st.session_state.sump1)
st.session_state.sump2 = st.slider("Sump 2 Level", 0, 100, st.session_state.sump2)

# Restricted Actions (Require Login)
st.subheader("🔒 Restricted Actions (Login Required)")
if not st.session_state.authenticated:
    username = st.text_input("User ID")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == VALID_USERNAME and password == VALID_PASSWORD:
            st.session_state.authenticated = True
            st.success("✅ Login Successful!")
            st.rerun()
        else:
            st.error("❌ Invalid Credentials! Please try again.")

# Show restricted buttons only if logged in
if st.session_state.authenticated:
    st.subheader
