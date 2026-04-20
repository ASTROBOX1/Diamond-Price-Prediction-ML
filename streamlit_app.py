"""
Entry point for Streamlit Cloud deployment.
"""
import os
import sys
import streamlit as st

# Add the project directory to the path to ensure imports work correctly
sys.path.append(os.path.dirname(__file__))

try:
    # Run the Streamlit dashboard
    import app.dashboard
except ImportError as e:
    st.error(f"⚠️ Failed to load dashboard. Error: {str(e)}")
    st.stop()
except Exception as e:
    st.error(f"🔧 Unexpected error during app initialization: {str(e)}")
    st.stop()
