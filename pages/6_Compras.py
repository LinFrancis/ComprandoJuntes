
import streamlit as st
import pandas as pd
from core.db import supabase

st.title("Compras")

st.markdown("""
Registro de compras realizadas a productores.
""")

data=supabase.table("purchases").select("*").execute()
df=pd.DataFrame(data.data)

st.dataframe(df)
