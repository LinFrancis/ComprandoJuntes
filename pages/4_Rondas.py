import streamlit as st
import pandas as pd
from datetime import date
from core.ui import inject_css, page_header, metric_row, divider, section_label, safe_query, safe_insert, safe_delete, empty_state

st.set_page_config(page_title="Rondas · Comprando Juntes", page_icon="🔄", layout="wide")
inject_css()
page_header("🔄", "Rondas de Compra", "Ciclos de coordinación desde el pedido hasta la entrega")

data = safe_query("rounds")
abiertas  = [r for r in data if r.get("status") == "abierta"]
cerradas  = [r for r in data if r.get("status") != "abierta"]

metric_row([
    {"icon": "🔄", "value": len(data),     "label": "Rondas totales"},
    {"icon": "✅", "value": len(abiertas), "label": "Abiertas"},
    {"icon": "🔒", "value": len(cerradas), "label": "Cerradas"},
])
divider()

section_label("Rondas activas")
if abiertas:
    for r in abiertas:
        st.markdown(
            f"""<div style="background:#D8F3DC;border-left:4px solid #2D6A4F;border-radius:8px;
                padding:0.8rem 1.2rem;margin-bottom:0.6rem">
                <b style="color:#1B7F3A">🟢 {r.get("name","—")}</b>
                <span style="font-size:0.82rem;color:#2D6A4F;margin-left:1rem">
                  Apertura: {r.get("open_date","—")} · Cierre: {r.get("close_date","—")}
                </span>
            </div>""",
            unsafe_allow_html=True,
        )
else:
    st.info("No hay rondas abiertas actualmente.")

divider()
section_label("Historial de rondas")
if data:
    df = pd.DataFrame(data)
    cols_order = [c for c in ["name","open_date","close_date","status"] if c in df.columns]
    df_show = df[cols_order] if cols_order else df
    df_show.columns = [c.replace("_"," ").title() for c in df_show.columns]
    st.dataframe(df_show, use_container_width=True, hide_index=True)
else:
    empty_state("🔄", "No hay rondas registradas.")

divider()
section_label("Crear nueva ronda")
with st.expander("➕ Nueva ronda"):
    with st.form("form_ronda"):
        c1, c2 = st.columns(2)
        name       = c1.text_input("Nombre de la ronda *")
        status_opt = c2.selectbox("Estado", ["abierta", "cerrada"])
        c3, c4     = st.columns(2)
        open_date  = c3.date_input("Fecha apertura", value=date.today())
        close_date = c4.date_input("Fecha cierre")
        submitted  = st.form_submit_button("💾 Guardar ronda")
        if submitted:
            if not name.strip():
                st.error("El nombre es obligatorio.")
            else:
                if safe_insert("rounds", {
                    "name": name.strip(),
                    "open_date": str(open_date),
                    "close_date": str(close_date),
                    "status": status_opt,
                }):
                    st.success(f"✅ Ronda '{name}' creada.")
                    st.rerun()

if data:
    divider()
    with st.expander("🗑️ Eliminar ronda"):
        names = {r["name"]: r["id"] for r in data if r.get("name")}
        selected = st.selectbox("Selecciona ronda", list(names.keys()))
        if st.button("Eliminar", type="secondary"):
            if safe_delete("rounds", names[selected]):
                st.success(f"✅ Ronda '{selected}' eliminada.")
                st.rerun()
