import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import time

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
st.title("HMI Water Level Monitoring 🚰")

# Simulated Water Levels (Use Sliders or Random Values)
reservoir = st.slider("Reservoir Level", 0, 100, 50)
sump1 = st.slider("Sump 1 Level", 0, 100, 30)
sump2 = st.slider("Sump 2 Level", 0, 100, 70)

# Display Tanks
col1, col2, col3 = st.columns(3)
with col1:
    st.pyplot(draw_tank(reservoir, "Reservoir"))
with col2:
    st.pyplot(draw_tank(sump1, "Sump 1"))
with col3:
    st.pyplot(draw_tank(sump2, "Sump 2"))

# Auto-refresh simulation
if st.button("Simulate Auto Update"):
    for _ in range(10):
        reservoir = np.random.randint(10, 100)
        sump1 = np.random.randint(10, 100)
        sump2 = np.random.randint(10, 100)
        
        col1.pyplot(draw_tank(reservoir, "Reservoir"))
        col2.pyplot(draw_tank(sump1, "Sump 1"))
        col3.pyplot(draw_tank(sump2, "Sump 2"))
        
        time.sleep(2)
        st.experimental_rerun()  # Refresh the UI
