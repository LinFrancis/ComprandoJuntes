
import streamlit as st
import pandas as pd
from core.db import supabase

st.title("Pagos")

st.markdown("""
Registro financiero de cada ronda.
""")

data=supabase.table("payments").select("*").execute()
df=pd.DataFrame(data.data)

st.dataframe(df)
