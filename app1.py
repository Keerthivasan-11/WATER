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

# Streamlit UI
st.title("🚰 HMI Water Level Monitoring")

# Simulated Water Levels (HMI interface is always visible)
if "reservoir" not in st.session_state:
    st.session_state.reservoir = 50
if "sump1" not in st.session_state:
    st.session_state.sump1 = 30
if "sump2" not in st.session_state:
    st.session_state.sump2 = 70

# Display Tanks
col1, col2, col3 = st.columns(3)

with col1:
    st.pyplot(draw_tank(st.session_state.reservoir, "Reservoir"))

with col2:
    st.pyplot(draw_tank(st.session_state.sump1, "Sump 1"))

with col3:
    st.pyplot(draw_tank(st.session_state.sump2, "Sump 2"))

# ---- Reset Buttons Require Authentication ----

# Check if user is logged in for reset buttons
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if st.session_state.authenticated:
    st.subheader("🔐 Reset Water Levels")
    if st.button("Reset Reservoir Pump"):
        st.session_state.reservoir = 0
    if st.button("Reset Sump 1"):
        st.session_state.sump1 = 0
    if st.button("Reset Sump 2"):
        st.session_state.sump2 = 0

    if st.button("Logout"):
        st.session_state.authenticated = False
        st.rerun()
else:
    st.subheader("🔐 Login to Reset Water Levels")
    username = st.text_input("User ID")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == VALID_USERNAME and password == VALID_PASSWORD:
            st.session_state.authenticated = True
            st.success("✅ Login Successful!")
            st.rerun()
        else:
            st.error("❌ Invalid Credentials! Please try again.")
