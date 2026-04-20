"""
Entry point for Streamlit Cloud deployment.

Execution Order (Critical for Streamlit):
1. st.set_page_config() - FIRST Streamlit command
2. sys.path setup
3. Import modules
4. Call main() which calls render_dashboard()
"""
import os
import sys
import streamlit as st

# ============================================================================
# STEP 1: Set page config FIRST (before any other Streamlit commands)
# ============================================================================
st.set_page_config(
    page_title="Diamond Market Intel | AI Valuator",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================================
# STEP 2: Add project paths before any imports that need them
# ============================================================================
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# ============================================================================
# STEP 3: Import dependencies with error handling
# ============================================================================
try:
    import plotly
    import plotly.express as px
    import plotly.graph_objects as go
except ImportError as e:
    st.error(f"❌ Plotly not installed: {str(e)}")
    st.info("💡 Please check requirements.txt is configured correctly on Streamlit Cloud")
    st.stop()

# ============================================================================
# STEP 4: Import the dashboard module
# ============================================================================
try:
    from app.dashboard import render_dashboard
except ImportError as e:
    st.error(f"⚠️ Failed to import dashboard module: {str(e)}")
    st.info(f"📝 Missing module error. Check all dependencies in requirements.txt are installed")
    st.stop()
except Exception as e:
    st.error(f"🔧 Unexpected error during dashboard import: {str(e)}")
    import traceback
    st.write(traceback.format_exc())
    st.stop()

# ============================================================================
# STEP 5: Main app execution
# ============================================================================
def main():
    """Main application entry point"""
    try:
        # Call the dashboard rendering function
        render_dashboard()
    except Exception as e:
        st.error(f"🔧 Error running dashboard: {str(e)}")
        import traceback
        st.write(traceback.format_exc())
        st.stop()

# ============================================================================
# STEP 6: Execute main function
# ============================================================================
if __name__ == "__main__":
    main()
