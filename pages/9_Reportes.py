
import streamlit as st
import pandas as pd
from core.db import supabase
from core.excel import export_excel

st.title("Reportes")

participants=pd.DataFrame(supabase.table("participants").select("*").execute().data)
orders=pd.DataFrame(supabase.table("orders").select("*").execute().data)
purchases=pd.DataFrame(supabase.table("purchases").select("*").execute().data)
payments=pd.DataFrame(supabase.table("payments").select("*").execute().data)

if st.button("Generar reporte Excel"):
    file=export_excel({
        "participants":participants,
        "orders":orders,
        "purchases":purchases,
        "payments":payments
    })

    with open(file,"rb") as f:
        st.download_button("Descargar reporte",f,"reporte_red_alimentos.xlsx")
