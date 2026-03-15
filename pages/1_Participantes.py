import streamlit as st
import pandas as pd
from core.ui import inject_css, page_header, metric_row, divider, section_label, safe_query, safe_insert, safe_delete, empty_state

st.set_page_config(page_title="Participantes · Comprando Juntes", page_icon="👥", layout="wide")
inject_css()
page_header("👥", "Participantes", "Personas que forman parte de la red de compras colectivas")

data = safe_query("participants")

metric_row([
    {"icon": "👥", "value": len(data), "label": "Total participantes"},
    {"icon": "📧", "value": sum(1 for p in data if p.get("email")), "label": "Con email"},
    {"icon": "📱", "value": sum(1 for p in data if p.get("phone")), "label": "Con teléfono"},
])
divider()

# ── Tabla ──────────────────────────────────────────────────────────────────
section_label("Lista de participantes")
if data:
    df = pd.DataFrame(data)
    cols_order = [c for c in ["name","email","phone","notes"] if c in df.columns]
    df_show = df[cols_order] if cols_order else df
    df_show.columns = [c.replace("_"," ").title() for c in df_show.columns]
    st.dataframe(df_show, use_container_width=True, hide_index=True)
else:
    empty_state("👥", "Aún no hay participantes registrados.")

divider()

# ── Formulario ─────────────────────────────────────────────────────────────
section_label("Agregar participante")
with st.expander("➕ Nuevo participante", expanded=False):
    with st.form("form_participante"):
        c1, c2 = st.columns(2)
        name  = c1.text_input("Nombre *")
        email = c2.text_input("Email")
        c3, c4 = st.columns(2)
        phone = c3.text_input("Teléfono")
        notes = c4.text_input("Notas")
        submitted = st.form_submit_button("💾 Guardar participante")
        if submitted:
            if not name.strip():
                st.error("El nombre es obligatorio.")
            else:
                if safe_insert("participants", {"name": name.strip(), "email": email.strip(), "phone": phone.strip(), "notes": notes.strip()}):
                    st.success(f"✅ {name} agregado correctamente.")
                    st.rerun()

# ── Eliminar ───────────────────────────────────────────────────────────────
if data:
    divider()
    section_label("Eliminar participante")
    with st.expander("🗑️ Eliminar participante", expanded=False):
        names = {p["name"]: p["id"] for p in data if p.get("name")}
        selected = st.selectbox("Selecciona participante", options=list(names.keys()))
        if st.button("Eliminar", type="secondary"):
            if safe_delete("participants", names[selected]):
                st.success(f"✅ {selected} eliminado.")
                st.rerun()
