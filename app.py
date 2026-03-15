import streamlit as st
from core.ui import inject_css, page_header, metric_row, divider, section_label, safe_query

st.set_page_config(
    page_title="Comprando Juntes",
    page_icon="🐷",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_css()

page_header(
    "🐷",
    "Comprando Juntes",
    "Plataforma de compras colectivas · Red de alimentos de proximidad",
)

col_left, col_right = st.columns([3, 1])

with col_left:
    try:
        participants = safe_query("participants")
        products     = safe_query("products")
        producers    = safe_query("producers")
        rounds       = safe_query("rounds")
        abierta_count = sum(1 for r in rounds if r.get("status") == "abierta")
        orders       = safe_query("orders")

        metric_row([
            {"icon": "👥", "value": len(participants), "label": "Participantes"},
            {"icon": "🌿", "value": len(products),    "label": "Productos"},
            {"icon": "🏡", "value": len(producers),   "label": "Productores"},
            {"icon": "🔄", "value": len(rounds),      "label": "Rondas totales"},
            {"icon": "📋", "value": abierta_count,    "label": "Rondas abiertas"},
        ])
    except Exception:
        st.info("Conecta la base de datos para ver métricas en tiempo real.")

with col_right:
    try:
        st.image("assets/pig.svg", width=140)
    except Exception:
        st.markdown("🐷")

divider()

section_label("Flujo de la red")

steps = [
    ("1️⃣", "Participantes", "Personas del grupo"),
    ("2️⃣", "Productos",     "Catálogo de alimentos"),
    ("3️⃣", "Productores",   "Proveedores locales"),
    ("4️⃣", "Rondas",        "Ciclos de compra"),
    ("5️⃣", "Pedidos",       "Solicitudes por persona"),
    ("6️⃣", "Compras",       "Compras consolidadas"),
    ("7️⃣", "Distribución",  "Reparto de alimentos"),
    ("8️⃣", "Pagos",         "Control financiero"),
]

cols = st.columns(4)
for i, (num, name, desc) in enumerate(steps):
    with cols[i % 4]:
        st.markdown(
            f"""<div style="background:#fff;border:1px solid #D8EAD8;border-radius:12px;
                padding:1rem;margin-bottom:0.8rem;box-shadow:0 2px 8px rgba(45,106,79,0.06)">
                <div style="font-size:1.4rem">{num}</div>
                <div style="font-weight:600;color:#2D6A4F;font-size:0.95rem;margin:0.2rem 0">{name}</div>
                <div style="font-size:0.8rem;color:#6B7E6E">{desc}</div>
            </div>""",
            unsafe_allow_html=True,
        )

divider()
st.info("🌱 **Permacultura económica** — Cada sección guía el proceso de coordinación. Cualquier persona del grupo puede participar.")
