import streamlit as st
import pandas as pd
from core.ui import inject_css, page_header, metric_row, divider, section_label, safe_query, safe_insert, empty_state

st.set_page_config(page_title="Distribución · Comprando Juntes", page_icon="📦", layout="wide")
inject_css()
page_header("📦", "Distribución", "Cómo se reparten los alimentos entre los participantes de cada ronda")

distribution = safe_query("distribution")
participants = safe_query("participants")
products     = safe_query("products")
rounds       = safe_query("rounds")

p_map  = {p["id"]: p.get("name","—") for p in participants}
pr_map = {p["id"]: p.get("name","—") for p in products}
r_map  = {r["id"]: r.get("name","—") for r in rounds}

metric_row([
    {"icon": "📦", "value": len(distribution), "label": "Distribuciones"},
    {"icon": "👥", "value": len(set(d.get("participant_id") for d in distribution if d.get("participant_id"))), "label": "Participantes servidos"},
    {"icon": "🌿", "value": len(set(d.get("product_id") for d in distribution if d.get("product_id"))), "label": "Productos distribuidos"},
])
divider()

# ── Filtro por ronda ───────────────────────────────────────────────────────
section_label("Registros de distribución")
round_options = ["Todas"] + [r.get("name","") for r in rounds if r.get("name")]
filtro_ronda = st.selectbox("Filtrar por ronda", round_options)

filtered = distribution
if filtro_ronda != "Todas":
    round_id = next((r["id"] for r in rounds if r.get("name") == filtro_ronda), None)
    if round_id:
        filtered = [d for d in distribution if d.get("round_id") == round_id]

if filtered:
    df = pd.DataFrame(filtered)
    df["participante"] = df["participant_id"].map(p_map).fillna("—")
    df["producto"]     = df["product_id"].map(pr_map).fillna("—")
    df["ronda"]        = df["round_id"].map(r_map).fillna("—")
    show_cols = ["participante","producto","ronda","quantity"]
    df_show = df[[c for c in show_cols if c in df.columns]]
    df_show.columns = [c.replace("_"," ").title() for c in df_show.columns]
    st.dataframe(df_show, use_container_width=True, hide_index=True)

    # ── Resumen por participante ─────────────────────────────────────────
    divider()
    section_label("Resumen por participante")
    if "participante" in df.columns and "quantity" in df.columns:
        resumen = df.groupby("participante")["quantity"].sum().reset_index()
        resumen.columns = ["Participante", "Cantidad total recibida"]
        resumen = resumen.sort_values("Cantidad total recibida", ascending=False)
        st.dataframe(resumen, use_container_width=True, hide_index=True)
else:
    empty_state("📦", "No hay registros de distribución para esta ronda.")

divider()
section_label("Registrar distribución")
if not participants or not products or not rounds:
    st.warning("Necesitas participantes, productos y rondas cargados.")
else:
    with st.expander("➕ Nueva distribución"):
        with st.form("form_distribucion"):
            c1, c2, c3 = st.columns(3)
            p_names  = {p.get("name","—"): p["id"] for p in participants}
            pr_names = {p.get("name","—"): p["id"] for p in products}
            r_names  = {r.get("name","—"): r["id"] for r in rounds}
            sel_p  = c1.selectbox("Participante", list(p_names.keys()))
            sel_pr = c2.selectbox("Producto",     list(pr_names.keys()))
            sel_r  = c3.selectbox("Ronda",        list(r_names.keys()))
            quantity = st.number_input("Cantidad entregada", min_value=0.0, step=0.5)
            submitted = st.form_submit_button("💾 Guardar distribución")
            if submitted:
                if quantity <= 0:
                    st.error("La cantidad debe ser mayor a 0.")
                else:
                    if safe_insert("distribution", {
                        "participant_id": p_names[sel_p],
                        "product_id":     pr_names[sel_pr],
                        "round_id":       r_names[sel_r],
                        "quantity":       quantity,
                    }):
                        st.success("✅ Distribución registrada.")
                        st.rerun()
