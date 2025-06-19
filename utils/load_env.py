# Load API key from variables.env if it exists
import streamlit as st
import os
from typing import Optional

def load_api_key_from_env(ENV_FILE: str) -> Optional[str]:
    try:
        if os.path.exists(ENV_FILE):
            with open(ENV_FILE, "r") as f:
                for line in f:
                    if line.startswith("API_KEY"):
                        api_key = line.split("=")[1].strip()
                        if api_key:
                            return api_key
    except Exception as e:
        st.error(f"Error loading API key from variables.env: {str(e)}")
    return None
