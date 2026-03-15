import streamlit as st
import pandas as pd
import io
from core.ui import inject_css, page_header, metric_row, divider, section_label, safe_query, empty_state

st.set_page_config(page_title="Reportes · Comprando Juntes", page_icon="📊", layout="wide")
inject_css()
page_header("📊", "Reportes", "Exporta y analiza la información completa de la red de compras")

# ── Cargar datos ───────────────────────────────────────────────────────────
with st.spinner("Cargando datos..."):
    participants = pd.DataFrame(safe_query("participants"))
    products     = pd.DataFrame(safe_query("products"))
    producers    = pd.DataFrame(safe_query("producers"))
    rounds       = pd.DataFrame(safe_query("rounds"))
    orders       = pd.DataFrame(safe_query("orders"))
    purchases    = pd.DataFrame(safe_query("purchases"))
    distribution = pd.DataFrame(safe_query("distribution"))
    payments     = pd.DataFrame(safe_query("payments"))

datasets = {
    "participantes": participants,
    "productos":     products,
    "productores":   producers,
    "rondas":        rounds,
    "pedidos":       orders,
    "compras":       purchases,
    "distribucion":  distribution,
    "pagos":         payments,
}

# ── Métricas globales ──────────────────────────────────────────────────────
total_pagado = payments["amount"].sum() if not payments.empty and "amount" in payments.columns else 0
total_pedidos = len(orders)
total_dist    = len(distribution)

metric_row([
    {"icon": "👥", "value": len(participants), "label": "Participantes"},
    {"icon": "🌿", "value": len(products),    "label": "Productos"},
    {"icon": "📋", "value": total_pedidos,    "label": "Pedidos"},
    {"icon": "💰", "value": f"${total_pagado:,.0f}", "label": "Total pagado"},
    {"icon": "📦", "value": total_dist,       "label": "Distribuciones"},
])
divider()

# ── Vista previa por sección ───────────────────────────────────────────────
section_label("Vista previa de datos")

tab_names = ["👥 Participantes", "🌿 Productos", "🏡 Productores",
             "🔄 Rondas", "📋 Pedidos", "🛒 Compras", "📦 Distribución", "💰 Pagos"]

tabs = st.tabs(tab_names)
tab_data = [participants, products, producers, rounds, orders, purchases, distribution, payments]

for tab, df in zip(tabs, tab_data):
    with tab:
        if not df.empty:
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.caption(f"{len(df)} registros")
        else:
            empty_state("📭", "Sin datos en esta tabla.")

divider()

# ── Análisis rápidos ───────────────────────────────────────────────────────
section_label("Análisis rápidos")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**🔝 Top productos pedidos**")
    if not orders.empty and "product_id" in orders.columns and not products.empty:
        pr_map = dict(zip(products.get("id", []), products.get("name", [])))
        orders_copy = orders.copy()
        orders_copy["producto"] = orders_copy["product_id"].map(pr_map).fillna("—")
        top = orders_copy.groupby("producto")["quantity"].sum().sort_values(ascending=False).head(5)
        st.dataframe(top.reset_index().rename(columns={"quantity":"Cantidad"}), use_container_width=True, hide_index=True)
    else:
        st.caption("Sin datos suficientes.")

with col2:
    st.markdown("**💰 Pagos por participante**")
    if not payments.empty and not participants.empty:
        p_map = dict(zip(participants.get("id", []), participants.get("name", [])))
        pay_copy = payments.copy()
        pay_copy["participante"] = pay_copy["participant_id"].map(p_map).fillna("—")
        resumen = pay_copy.groupby("participante")["amount"].sum().sort_values(ascending=False).head(5)
        st.dataframe(resumen.reset_index().rename(columns={"amount":"Total $"}), use_container_width=True, hide_index=True)
    else:
        st.caption("Sin datos suficientes.")

divider()

# ── Exportar Excel ─────────────────────────────────────────────────────────
section_label("Exportar reporte Excel")
st.markdown("Descarga todos los datos en un archivo `.xlsx` con una hoja por tabla.")

if st.button("📥 Generar reporte Excel"):
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        for name, df in datasets.items():
            if not df.empty:
                df.to_excel(writer, sheet_name=name[:31], index=False)
    buffer.seek(0)
    st.download_button(
        label="⬇️ Descargar reporte_red_alimentos.xlsx",
        data=buffer,
        file_name="reporte_red_alimentos.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    st.success("✅ Reporte listo para descargar.")
