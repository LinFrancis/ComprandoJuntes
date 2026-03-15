import streamlit as st
import pandas as pd
from core.ui import inject_css, page_header, metric_row, divider, section_label, safe_query, safe_insert, empty_state

st.set_page_config(page_title="Pagos · Comprando Juntes", page_icon="💰", layout="wide")
inject_css()
page_header("💰", "Pagos", "Control financiero de cada ronda · seguimiento de deudas y pagos confirmados")

payments     = safe_query("payments")
participants = safe_query("participants")
rounds       = safe_query("rounds")

p_map = {p["id"]: p.get("name","—") for p in participants}
r_map = {r["id"]: r.get("name","—") for r in rounds}

total_cobrado = sum(p.get("amount", 0) or 0 for p in payments if p.get("status") == "pagado")
total_pendiente = sum(p.get("amount", 0) or 0 for p in payments if p.get("status") != "pagado")
pagados_count   = sum(1 for p in payments if p.get("status") == "pagado")
pendientes_count = sum(1 for p in payments if p.get("status") != "pagado")

metric_row([
    {"icon": "💰", "value": f"${total_cobrado:,.0f}",   "label": "Cobrado"},
    {"icon": "⏳", "value": f"${total_pendiente:,.0f}", "label": "Pendiente"},
    {"icon": "✅", "value": pagados_count,               "label": "Pagos confirmados"},
    {"icon": "🔴", "value": pendientes_count,            "label": "Pagos pendientes"},
])
divider()

# ── Filtro ─────────────────────────────────────────────────────────────────
section_label("Registro de pagos")
col1, col2 = st.columns(2)
round_options = ["Todas"] + [r.get("name","") for r in rounds if r.get("name")]
filtro_ronda  = col1.selectbox("Filtrar por ronda", round_options)
filtro_status = col2.selectbox("Filtrar por estado", ["Todos", "pagado", "pendiente"])

filtered = payments
if filtro_ronda != "Todas":
    rid = next((r["id"] for r in rounds if r.get("name") == filtro_ronda), None)
    if rid:
        filtered = [p for p in filtered if p.get("round_id") == rid]
if filtro_status != "Todos":
    filtered = [p for p in filtered if p.get("status") == filtro_status]

if filtered:
    df = pd.DataFrame(filtered)
    df["participante"] = df["participant_id"].map(p_map).fillna("—")
    df["ronda"]        = df["round_id"].map(r_map).fillna("—")

    # Badge visual para estado
    def badge(s):
        color = "#D8F3DC" if s == "pagado" else "#FFF3CD"
        text_c = "#1B7F3A" if s == "pagado" else "#856404"
        return f'<span style="background:{color};color:{text_c};border-radius:20px;padding:2px 10px;font-size:0.8rem;font-weight:600">{s}</span>'

    show_cols = ["participante","ronda","amount","status"]
    df_show = df[[c for c in show_cols if c in df.columns]].copy()
    df_show.columns = [c.replace("_"," ").title() for c in df_show.columns]
    st.dataframe(df_show, use_container_width=True, hide_index=True)

    # Totales del filtro
    if "amount" in df.columns:
        total_filtro = df["amount"].sum()
        st.markdown(
            f'<div style="text-align:right;font-weight:600;color:#2D6A4F;font-size:1rem;margin-top:0.3rem">'
            f'Total mostrado: <span style="font-size:1.3rem">${total_filtro:,.0f}</span></div>',
            unsafe_allow_html=True
        )
else:
    empty_state("💰", "No hay pagos registrados para esta selección.")

divider()
section_label("Registrar pago")
if not participants or not rounds:
    st.warning("Necesitas participantes y rondas cargados.")
else:
    with st.expander("➕ Nuevo pago"):
        with st.form("form_pago"):
            c1, c2 = st.columns(2)
            p_names = {p.get("name","—"): p["id"] for p in participants}
            r_names = {r.get("name","—"): r["id"] for r in rounds}
            sel_p  = c1.selectbox("Participante", list(p_names.keys()))
            sel_r  = c2.selectbox("Ronda",        list(r_names.keys()))
            c3, c4 = st.columns(2)
            amount = c3.number_input("Monto", min_value=0.0, step=100.0)
            status = c4.selectbox("Estado", ["pendiente", "pagado"])
            submitted = st.form_submit_button("💾 Guardar pago")
            if submitted:
                if amount <= 0:
                    st.error("El monto debe ser mayor a 0.")
                else:
                    if safe_insert("payments", {
                        "participant_id": p_names[sel_p],
                        "round_id":       r_names[sel_r],
                        "amount":         amount,
                        "status":         status,
                    }):
                        st.success("✅ Pago registrado.")
                        st.rerun()
