import streamlit as st
import pandas as pd
from core.ui import inject_css, page_header, metric_row, divider, section_label, safe_query, safe_insert, empty_state

st.set_page_config(page_title="Compras · Comprando Juntes", page_icon="🛒", layout="wide")
inject_css()
page_header("🛒", "Compras", "Registro de compras realizadas a productores en cada ronda")

purchases = safe_query("purchases")
products  = safe_query("products")
producers = safe_query("producers")
rounds    = safe_query("rounds")

pr_map = {p["id"]: p.get("name","—") for p in products}
prod_map = {p["id"]: p.get("name","—") for p in producers}
r_map   = {r["id"]: r.get("name","—") for r in rounds}

total_gastado = sum(
    (c.get("quantity") or 0) * (c.get("price") or 0)
    for c in purchases
)

metric_row([
    {"icon": "🛒", "value": len(purchases),         "label": "Compras totales"},
    {"icon": "💰", "value": f"${total_gastado:,.0f}", "label": "Total gastado"},
    {"icon": "🏡", "value": len(set(c.get("producer_id") for c in purchases if c.get("producer_id"))), "label": "Productores involucrados"},
])
divider()

section_label("Compras registradas")
if purchases:
    df = pd.DataFrame(purchases)
    df["producto"]   = df["product_id"].map(pr_map).fillna("—")
    df["productor"]  = df["producer_id"].map(prod_map).fillna("—")
    df["ronda"]      = df["round_id"].map(r_map).fillna("—")
    df["subtotal"]   = (df.get("quantity", 0) * df.get("price", 0)).round(2)
    show_cols = ["productor","producto","ronda","quantity","price","subtotal"]
    df_show = df[[c for c in show_cols if c in df.columns]]
    df_show.columns = [c.replace("_"," ").title() for c in df_show.columns]
    st.dataframe(df_show, use_container_width=True, hide_index=True)
else:
    empty_state("🛒", "No hay compras registradas aún.")

divider()
section_label("Registrar nueva compra")
if not products or not producers or not rounds:
    st.warning("Asegúrate de tener productos, productores y rondas cargados.")
else:
    with st.expander("➕ Nueva compra"):
        with st.form("form_compra"):
            c1, c2, c3 = st.columns(3)
            pr_names   = {p.get("name","—"): p["id"] for p in products}
            prod_names = {p.get("name","—"): p["id"] for p in producers}
            r_names    = {r.get("name","—"): r["id"] for r in rounds}
            sel_pr    = c1.selectbox("Producto",   list(pr_names.keys()))
            sel_prod  = c2.selectbox("Productor",  list(prod_names.keys()))
            sel_r     = c3.selectbox("Ronda",      list(r_names.keys()))
            c4, c5 = st.columns(2)
            quantity = c4.number_input("Cantidad", min_value=0.0, step=0.5)
            price    = c5.number_input("Precio unitario", min_value=0.0, step=100.0)
            submitted = st.form_submit_button("💾 Guardar compra")
            if submitted:
                if quantity <= 0:
                    st.error("La cantidad debe ser mayor a 0.")
                else:
                    if safe_insert("purchases", {
                        "product_id":  pr_names[sel_pr],
                        "producer_id": prod_names[sel_prod],
                        "round_id":    r_names[sel_r],
                        "quantity":    quantity,
                        "price":       price,
                    }):
                        st.success("✅ Compra registrada.")
                        st.rerun()
