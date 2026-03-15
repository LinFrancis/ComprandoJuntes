import streamlit as st
import pandas as pd
from core.ui import inject_css, page_header, metric_row, divider, section_label, safe_query, safe_insert, safe_delete, empty_state

st.set_page_config(page_title="Pedidos · Comprando Juntes", page_icon="📋", layout="wide")
inject_css()
page_header("📋", "Pedidos", "Solicitudes de alimentos realizadas por participantes en cada ronda")

orders       = safe_query("orders")
participants = safe_query("participants")
products     = safe_query("products")
rounds       = safe_query("rounds")

p_map  = {p["id"]: p.get("name","—") for p in participants}
pr_map = {p["id"]: p.get("name","—") for p in products}
r_map  = {r["id"]: r.get("name","—") for r in rounds}

metric_row([
    {"icon": "📋", "value": len(orders),                                "label": "Pedidos totales"},
    {"icon": "🔄", "value": len(set(o.get("round_id") for o in orders if o.get("round_id"))), "label": "Rondas con pedidos"},
    {"icon": "👥", "value": len(set(o.get("participant_id") for o in orders if o.get("participant_id"))), "label": "Participantes activos"},
])
divider()

# ── Filtro por ronda ───────────────────────────────────────────────────────
section_label("Pedidos registrados")
round_options = ["Todas"] + [r.get("name","") for r in rounds if r.get("name")]
filtro_ronda = st.selectbox("Filtrar por ronda", round_options)

filtered_orders = orders
if filtro_ronda != "Todas":
    round_id = next((r["id"] for r in rounds if r.get("name") == filtro_ronda), None)
    if round_id:
        filtered_orders = [o for o in orders if o.get("round_id") == round_id]

if filtered_orders:
    df = pd.DataFrame(filtered_orders)
    df["participante"] = df["participant_id"].map(p_map).fillna("—")
    df["producto"]     = df["product_id"].map(pr_map).fillna("—")
    df["ronda"]        = df["round_id"].map(r_map).fillna("—")
    show_cols = ["participante","producto","ronda","quantity"]
    df_show = df[[c for c in show_cols if c in df.columns]]
    df_show.columns = [c.replace("_"," ").title() for c in df_show.columns]
    st.dataframe(df_show, use_container_width=True, hide_index=True)
else:
    empty_state("📋", "No hay pedidos registrados para esta ronda.")

divider()
section_label("Registrar nuevo pedido")
if not participants:
    st.warning("Primero agrega participantes.")
elif not products:
    st.warning("Primero agrega productos.")
elif not rounds:
    st.warning("Primero crea una ronda.")
else:
    with st.expander("➕ Nuevo pedido"):
        with st.form("form_pedido"):
            c1, c2, c3 = st.columns(3)
            p_names  = {p.get("name","—"): p["id"] for p in participants}
            pr_names = {p.get("name","—"): p["id"] for p in products}
            r_names  = {r.get("name","—"): r["id"] for r in rounds}
            sel_p    = c1.selectbox("Participante", list(p_names.keys()))
            sel_pr   = c2.selectbox("Producto",     list(pr_names.keys()))
            sel_r    = c3.selectbox("Ronda",        list(r_names.keys()))
            quantity = st.number_input("Cantidad", min_value=0.0, step=0.5)
            submitted = st.form_submit_button("💾 Guardar pedido")
            if submitted:
                if quantity <= 0:
                    st.error("La cantidad debe ser mayor a 0.")
                else:
                    if safe_insert("orders", {
                        "participant_id": p_names[sel_p],
                        "product_id":     pr_names[sel_pr],
                        "round_id":       r_names[sel_r],
                        "quantity":       quantity,
                    }):
                        st.success("✅ Pedido registrado.")
                        st.rerun()
