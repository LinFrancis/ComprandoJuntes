import streamlit as st
import pandas as pd
from core.ui import inject_css, page_header, metric_row, divider, section_label, safe_query, safe_insert, safe_delete, empty_state

st.set_page_config(page_title="Productos · Comprando Juntes", page_icon="🌿", layout="wide")
inject_css()
page_header("🌿", "Productos", "Catálogo de alimentos disponibles para compras colectivas")

data = safe_query("products")
units = sorted(set(p.get("unit","") for p in data if p.get("unit")))

metric_row([
    {"icon": "🌿", "value": len(data),       "label": "Productos"},
    {"icon": "📦", "value": len(units),      "label": "Unidades distintas"},
])
divider()

# ── Filtro ─────────────────────────────────────────────────────────────────
section_label("Catálogo de productos")
if units:
    filtro = st.multiselect("Filtrar por unidad", options=units, default=[])
    filtered = [p for p in data if not filtro or p.get("unit") in filtro]
else:
    filtered = data

if filtered:
    df = pd.DataFrame(filtered)
    cols_order = [c for c in ["name","unit"] if c in df.columns]
    df_show = df[cols_order] if cols_order else df
    df_show.columns = [c.replace("_"," ").title() for c in df_show.columns]
    st.dataframe(df_show, use_container_width=True, hide_index=True)
else:
    empty_state("🌿", "No hay productos en el catálogo.")

divider()

# ── Formulario ─────────────────────────────────────────────────────────────
section_label("Agregar producto")
with st.expander("➕ Nuevo producto"):
    with st.form("form_producto"):
        c1, c2 = st.columns(2)
        name = c1.text_input("Nombre del producto *")
        unit = c2.selectbox("Unidad", ["kg", "g", "L", "ml", "unidad", "docena", "atado", "otro"])
        submitted = st.form_submit_button("💾 Guardar producto")
        if submitted:
            if not name.strip():
                st.error("El nombre es obligatorio.")
            else:
                if safe_insert("products", {"name": name.strip(), "unit": unit}):
                    st.success(f"✅ Producto '{name}' agregado.")
                    st.rerun()

if data:
    divider()
    with st.expander("🗑️ Eliminar producto"):
        names = {p["name"]: p["id"] for p in data if p.get("name")}
        selected = st.selectbox("Selecciona producto", list(names.keys()))
        if st.button("Eliminar", type="secondary"):
            if safe_delete("products", names[selected]):
                st.success(f"✅ '{selected}' eliminado.")
                st.rerun()
