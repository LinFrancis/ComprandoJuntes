
import streamlit as st
import pandas as pd
from core.db import supabase

st.title("Distribución")

st.markdown("""
Registro de cómo se reparten los alimentos.
""")

data=supabase.table("distribution").select("*").execute()
df=pd.DataFrame(data.data)

st.dataframe(df)
