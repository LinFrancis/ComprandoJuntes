
import streamlit as st
import pandas as pd
from core.db import supabase

st.title("Rondas de compra")

st.markdown("""
Cada ciclo de compra colectiva.
""")

data=supabase.table("rounds").select("*").execute()
df=pd.DataFrame(data.data)

st.dataframe(df)
