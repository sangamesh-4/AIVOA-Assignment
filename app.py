import streamlit as st
import subprocess
import os

# 1. Boot up the FastAPI backend router in the background seamlessly
@st.cache_resource
def start_backend():
    backend_path = os.path.join(os.path.dirname(__file__), "backend")
    process = subprocess.Popen(
        ["uvicorn", "server:app", "--host", "127.0.0.1", "--port", "8000"],
        cwd=backend_path,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    return process

backend_process = start_backend()

# 2. Configure Streamlit to display the official operational interface
st.set_page_config(
    page_title="AI-First CRM HCP Module", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# Hide default Streamlit style borders to make it look like a native application
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    div.block-container {padding-top: 0rem; padding-bottom: 0rem; padding-left: 1rem; padding-right: 1rem;}
    </style>
""", unsafe_html=True)

# 3. Stream your local working UI inside the secure browser window frame
# (Maps directly to your local running React port instance)
target_url = "http://localhost:3000"

st.components.v1.iframe(src=target_url, height=900, scrolling=True)
