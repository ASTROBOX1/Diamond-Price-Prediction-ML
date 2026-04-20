"""
Entry point for Streamlit Cloud deployment.
"""
import os
import sys

# Add the project directory to the path to ensure imports work correctly
sys.path.append(os.path.dirname(__file__))

# Run the Streamlit dashboard
import app.dashboard
