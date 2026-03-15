
import os
import streamlit as st
from supabase import create_client


def _get_config():
    """Lee credenciales desde st.secrets (Streamlit Cloud) o variables de entorno."""
    try:
        url = st.secrets["supabase"]["url"]
        key = st.secrets["supabase"]["key"]
        if url and key:
            return url, key
    except (KeyError, FileNotFoundError, Exception):
        pass

    # Fallback: .env en desarrollo local
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass

    url = os.getenv("SUPABASE_URL", "")
    key = os.getenv("SUPABASE_KEY", "")
    return url, key


url, key = _get_config()

if not url or not key:
    raise EnvironmentError(
        "❌ Credenciales de Supabase no encontradas. "
        "Configura [supabase] url y key en .streamlit/secrets.toml"
    )

supabase = create_client(url, key)

