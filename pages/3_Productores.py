import streamlit as st
import pandas as pd
from core.ui import inject_css, page_header, metric_row, divider, section_label, safe_query, safe_insert, safe_delete, empty_state

st.set_page_config(page_title="Productores · Comprando Juntes", page_icon="🏡", layout="wide")
inject_css()
page_header("🏡", "Productores", "Agricultores y proveedores locales que abastecen la red")

data = safe_query("producers")
locations = sorted(set(p.get("location","") for p in data if p.get("location")))

metric_row([
    {"icon": "🏡", "value": len(data),       "label": "Productores"},
    {"icon": "📍", "value": len(locations),  "label": "Localidades"},
])
divider()

section_label("Lista de productores")
if data:
    df = pd.DataFrame(data)
    cols_order = [c for c in ["name","location","contact"] if c in df.columns]
    df_show = df[cols_order] if cols_order else df
    df_show.columns = [c.replace("_"," ").title() for c in df_show.columns]
    st.dataframe(df_show, use_container_width=True, hide_index=True)
else:
    empty_state("🏡", "No hay productores registrados aún.")

divider()
section_label("Agregar productor")
with st.expander("➕ Nuevo productor"):
    with st.form("form_productor"):
        c1, c2 = st.columns(2)
        name     = c1.text_input("Nombre *")
        location = c2.text_input("Localidad / zona")
        contact  = st.text_input("Contacto (email / teléfono / web)")
        submitted = st.form_submit_button("💾 Guardar productor")
        if submitted:
            if not name.strip():
                st.error("El nombre es obligatorio.")
            else:
                if safe_insert("producers", {"name": name.strip(), "location": location.strip(), "contact": contact.strip()}):
                    st.success(f"✅ '{name}' agregado.")
                    st.rerun()

if data:
    divider()
    with st.expander("🗑️ Eliminar productor"):
        names = {p["name"]: p["id"] for p in data if p.get("name")}
        selected = st.selectbox("Selecciona productor", list(names.keys()))
        if st.button("Eliminar", type="secondary"):
            if safe_delete("producers", names[selected]):
                st.success(f"✅ '{selected}' eliminado.")
                st.rerun()
