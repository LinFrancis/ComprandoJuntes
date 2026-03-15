
import streamlit as st
import pandas as pd
from core.db import supabase

st.title("Productores")

st.markdown("""
Productores locales que proveen alimentos.
""")

data=supabase.table("producers").select("*").execute()
df=pd.DataFrame(data.data)

st.dataframe(df)
