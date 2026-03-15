
import streamlit as st
import pandas as pd
from core.db import supabase

st.title("Pedidos")

st.markdown("""
Solicitudes de alimentos realizadas por participantes.
""")

data=supabase.table("orders").select("*").execute()
df=pd.DataFrame(data.data)

st.dataframe(df)
