import streamlit as st
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.styling import apply_custom_styling, load_css
from utils.state_management import initialize_session_state
from src._3_frameworks.streamlit_app import VibratonicApp

# Configure page
st.set_page_config(
    page_title="Vibratonic - Hackathon Platform",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state
initialize_session_state()

# Apply custom styling
apply_custom_styling()
load_css("static/custom.css")

# Initialize and run the main app
app = VibratonicApp()
app.run()
