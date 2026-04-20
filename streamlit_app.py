"""
Entry point for Streamlit Cloud deployment.
"""
import os
import sys
import streamlit as st

# Add the project directory to the path to ensure imports work correctly
sys.path.append(os.path.dirname(__file__))

# Set up page config FIRST, before any other Streamlit commands
st.set_page_config(
    page_title="Diamond Market Intel | AI Valuator",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded",
)

try:
    # Import with better error reporting
    try:
        import plotly
    except ImportError as e:
        st.error(f"❌ Plotly not installed: {str(e)}")
        st.info("💡 Please check requirements.txt is configured correctly on Streamlit Cloud")
        st.stop()
    
    # Run the Streamlit dashboard
    import app.dashboard
    
except ImportError as e:
    st.error(f"⚠️ Failed to load dashboard. Error: {str(e)}")
    st.info(f"📝 Missing module: Check if all dependencies in requirements.txt are installed")
    st.stop()
except Exception as e:
    st.error(f"🔧 Unexpected error during app initialization: {str(e)}")
    import traceback
    st.write(traceback.format_exc())
    st.stop()
