# wellness_app.py
import streamlit as st
import time
from datetime import datetime
import matplotlib.pyplot as plt

# Page configuration
st.set_page_config(page_title="Wellness Companion", layout="centered")

# --- Helper & Logic Functions ---

def assess_wellness_level(pulse, bp_systolic, bp_diastolic, glucose):
    """Assesses user's stress level based on biometric thresholds."""
    stress_triggers = [
        pulse > 100,  # High heart rate
        bp_systolic > 140 or bp_diastolic > 90,  # High blood pressure
        glucose > 180 or glucose < 70  # Atypical glucose levels
    ]
    
    if any(stress_triggers):
        return "Elevated"
    return "Normal"

def run_breathing_session():
    """Displays a guided breathing exercise animation."""
    st.header("Mindful Breathing")
    st.write("Follow the guide to regulate your breathing.")
    
    animation_placeholder = st.empty()
    
    for cycle in range(4):  # Increased to 4 cycles
        animation_placeholder.markdown("<h3 style='text-align: center; color: #007BFF;'>Breathe In...</h3>", unsafe_allow_html=True)
        time.sleep(4)
        animation_placeholder.markdown("<h3 style='text-align: center; color: #007BFF;'>Breathe Out...</h3>", unsafe_allow_html=True)
        time.sleep(5) # Slightly longer exhale
        
    animation_placeholder.success("Session Complete!")
    
    if st.button("Return to Main Dashboard", key="return_home"):
        st.session_state.view = "main"
        st.rerun()

def display_pulse_trend_chart(pulse_history):
    """Generates and displays a plot of the recent pulse history."""
    fig, ax = plt.subplots(figsize=(7, 3))
    ax.plot(pulse_history, marker='x', linestyle='--', color='purple')
    ax.set_title("Recent Pulse Trend")
    ax.set_xlabel("Timepoint")
    ax.set_ylabel("Pulse (BPM)")
    ax.set_ylim(min(pulse_history) - 10, max(pulse_history) + 10) # Dynamic Y-axis
    ax.grid(True, linestyle=':')
    st.pyplot(fig)

# --- Session State Initialization ---

if 'view' not in st.session_state:
    st.session_state.view = "main"
if 'pulse_history' not in st.session_state:
    st.session_state.pulse_history = [75, 78, 76, 80, 79] # Initialize with varied data

# --- Main Application UI ---

st.title("Wellness Companion")

# Main Dashboard View
if st.session_state.view == "main":
    st.markdown(f"**{datetime.now().strftime('%A, %B %d, %Y | %I:%M %p')}**")
    st.markdown("---")

    # User input section
    with st.form(key="biometrics_form"):
        st.subheader("Log Your Vitals")
        col1, col2 = st.columns(2)
        with col1:
            pulse_bpm = st.number_input("Pulse (beats per minute)", min_value=40, max_value=200, value=80)
            bp_systolic = st.number_input("Systolic Pressure (mmHg)", min_value=80, max_value=200, value=120)
        with col2:
            glucose_level = st.number_input("Blood Sugar (mg/dL)", min_value=20, max_value=400, value=100)
            bp_diastolic = st.number_input("Diastolic Pressure (mmHg)", min_value=40, max_value=120, value=80)
        
        submitted = st.form_submit_button("Analyze Vitals")

    if submitted:
        # Update and trim the pulse history
        st.session_state.pulse_history.append(pulse_bpm)
        st.session_state.pulse_history = st.session_state.pulse_history[-5:]

        # Display submitted metrics
        st.subheader("Current Biometrics")
        m_col1, m_col2, m_col3 = st.columns(3)
        m_col1.metric("Pulse", f"{pulse_bpm} BPM")
        m_col2.metric("Blood Pressure", f"{bp_systolic}/{bp_diastolic} mmHg")
        m_col3.metric("Glucose", f"{glucose_level} mg/dL")

        # Determine and display wellness status
        user_state = assess_wellness_level(pulse_bpm, bp_systolic, bp_diastolic, glucose_level)
        
        if user_state == "Elevated":
            st.error("Status: Elevated Stress Detected")
        else:
            st.success("Status: Calm and Normal")
        
        # Display the historical data chart
        display_pulse_trend_chart(st.session_state.pulse_history)

    st.markdown("---")

    # Navigation buttons
    if st.button("Begin Mindful Breathing"):
        st.session_state.view = "breathing"
        st.rerun()

    if st.button("Preferences"):
        st.session_state.view = "preferences"
        st.rerun()

# Breathing Exercise View
elif st.session_state.view == "breathing":
    run_breathing_session()

# Preferences View
elif st.session_state.view == "preferences":
    st.header("⚙️ Preferences")
    st.write("Configure application settings.")
    
    st.checkbox("Enable Haptic Feedback", value=True, key="haptic_feedback")
    st.slider("Interaction Sensitivity", min_value=1, max_value=10, value=5, key="sensitivity")
    
    if st.button("Back to Main Dashboard"):
        st.session_state.view = "main"
        st.rerun()

# Footer
st.markdown("<br><hr><p style='text-align: center; color: #888;'>Your Personal Bio-Feedback Assistant</p>", unsafe_allow_html=True)