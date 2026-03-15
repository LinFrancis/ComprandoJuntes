
import streamlit as st
import pandas as pd
from core.db import supabase

st.title("Participantes")

st.markdown("""
Registro de personas que forman parte de la red.
""")

data=supabase.table("participants").select("*").execute()
df=pd.DataFrame(data.data)

st.dataframe(df)
