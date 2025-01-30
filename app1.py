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
st.title("🔐 HMI Water Level Monitoring 🚰")

# Check if user is logged in
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Login Form
if not st.session_state.authenticated:
    st.subheader("Login Required")
    username = st.text_input("User ID")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if username == VALID_USERNAME and password == VALID_PASSWORD:
            st.session_state.authenticated = True
            st.success("✅ Login Successful!")
            st.experimental_rerun()
        else:
            st.error("❌ Invalid Credentials! Please try again.")
else:
    # Simulated Water Levels
    if "reservoir" not in st.session_state:
        st.session_state.reservoir = 50
    if "sump1" not in st.session_state:
        st.session_state.sump1 = 30
    if "sump2" not in st.session_state:
        st.session_state.sump2 = 70

    # Logout Button
    if st.button("Logout"):
        st.session_state.authenticated = False
        st.experimental_rerun()

    # Sliders for Manual Control
    st.session_state.reservoir = st.slider("Reservoir Level", 0, 100, st.session_state.reservoir)
    st.session_state.sump1 = st.slider("Sump 1 Level", 0, 100, st.session_state.sump1)
    st.session_state.sump2 = st.slider("Sump 2 Level", 0, 100, st.session_state.sump2)

    # Buttons to Turn Off Pumps
    col1, col2, col3 = st.columns(3)

    with col1:
        st.pyplot(draw_tank(st.session_state.reservoir, "Reservoir"))
        if st.button("Turn Off Reservoir Pump"):
            st.session_state.reservoir = 0

    with col2:
        st.pyplot(draw_tank(st.session_state.sump1, "Sump 1"))
        if st.button("Turn Off Sump 1"):
            st.session_state.sump1 = 0

    with col3:
        st.pyplot(draw_tank(st.session_state.sump2, "Sump 2"))
        if st.button("Turn Off Sump 2"):
            st.session_state.sump2 = 0

    # Auto-refresh simulation
    if st.button("Simulate Auto Update"):
        for _ in range(10):
            st.session_state.reservoir = np.random.randint(10, 100)
            st.session_state.sump1 = np.random.randint(10, 100)
            st.session_state.sump2 = np.random.randint(10, 100)

            col1.pyplot(draw_tank(st.session_state.reservoir, "Reservoir"))
            col2.pyplot(draw_tank(st.session_state.sump1, "Sump 1"))
            col3.pyplot(draw_tank(st.session_state.sump2, "Sump 2"))

            time.sleep(2)
            st.experimental_rerun()  # Refresh the UI
