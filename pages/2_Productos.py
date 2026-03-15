
import streamlit as st
import pandas as pd
from core.db import supabase

st.title("Productos")

st.markdown("""
Lista de alimentos disponibles para compras colectivas.
""")

data=supabase.table("products").select("*").execute()
df=pd.DataFrame(data.data)

st.dataframe(df)
