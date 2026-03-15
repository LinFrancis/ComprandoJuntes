"""
Utilidades de UI compartidas para Comprando Juntes.
Estilos, componentes y helpers de interfaz.
"""
import streamlit as st


# ─── Paleta de colores permacultura ───────────────────────────────────────────
VERDE_BOSQUE   = "#2D6A4F"
VERDE_HOJA     = "#40916C"
VERDE_CLARO    = "#74C69D"
VERDE_MENTA    = "#B7E4C7"
CREMA          = "#F8F5EE"
TIERRA         = "#8B6914"
TERRACOTA      = "#C4733F"
ROJO_AMAPOLA   = "#E63946"
AZUL_AGUA      = "#4895EF"
GRIS_SUAVE     = "#E9F0E9"


CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;700&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── Base ─────────────────────────────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* ── Encabezado principal ─────────────────────────────────────── */
.cj-header {
    background: linear-gradient(135deg, #2D6A4F 0%, #40916C 60%, #74C69D 100%);
    border-radius: 16px;
    padding: 2rem 2.5rem 1.5rem;
    margin-bottom: 1.8rem;
    box-shadow: 0 4px 24px rgba(45,106,79,0.18);
    position: relative;
    overflow: hidden;
}
.cj-header::before {
    content: '';
    position: absolute;
    top: -40px; right: -40px;
    width: 180px; height: 180px;
    border-radius: 50%;
    background: rgba(255,255,255,0.07);
}
.cj-header h1 {
    font-family: 'Playfair Display', serif;
    color: #fff !important;
    font-size: 2rem;
    margin: 0 0 0.3rem;
    line-height: 1.2;
}
.cj-header p {
    color: rgba(255,255,255,0.85);
    font-size: 0.95rem;
    margin: 0;
    font-weight: 300;
}

/* ── Tarjetas de métricas ─────────────────────────────────────── */
.metric-card {
    background: #fff;
    border: 1px solid #D8EAD8;
    border-radius: 14px;
    padding: 1.2rem 1.4rem;
    text-align: center;
    box-shadow: 0 2px 12px rgba(45,106,79,0.07);
    transition: transform 0.2s, box-shadow 0.2s;
}
.metric-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(45,106,79,0.14);
}
.metric-card .metric-value {
    font-family: 'Playfair Display', serif;
    font-size: 2.4rem;
    font-weight: 700;
    color: #2D6A4F;
    line-height: 1;
}
.metric-card .metric-label {
    font-size: 0.8rem;
    color: #6B7E6E;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-top: 0.35rem;
    font-weight: 500;
}
.metric-card .metric-icon {
    font-size: 1.6rem;
    margin-bottom: 0.4rem;
}

/* ── Sección ──────────────────────────────────────────────────── */
.section-label {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #40916C;
    margin-bottom: 0.5rem;
}

/* ── Tabla mejorada ───────────────────────────────────────────── */
.stDataFrame {
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid #D8EAD8 !important;
}

/* ── Botones ──────────────────────────────────────────────────── */
.stButton > button {
    background: #2D6A4F !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    padding: 0.55rem 1.4rem !important;
    transition: background 0.2s, transform 0.1s !important;
}
.stButton > button:hover {
    background: #40916C !important;
    transform: translateY(-1px) !important;
}

/* ── Formularios ──────────────────────────────────────────────── */
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stSelectbox > div > div {
    border-radius: 10px !important;
    border-color: #C4DCC4 !important;
    font-family: 'DM Sans', sans-serif !important;
}
.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus {
    border-color: #2D6A4F !important;
    box-shadow: 0 0 0 2px rgba(45,106,79,0.15) !important;
}

/* ── Sidebar ──────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: #F0F6EF !important;
    border-right: 1px solid #D8EAD8;
}
[data-testid="stSidebar"] .stMarkdown {
    font-family: 'DM Sans', sans-serif;
}

/* ── Alertas / info ───────────────────────────────────────────── */
.stAlert {
    border-radius: 12px !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* ── Expander ─────────────────────────────────────────────────── */
.streamlit-expanderHeader {
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    color: #2D6A4F !important;
}

/* ── Tags de estado ───────────────────────────────────────────── */
.status-badge {
    display: inline-block;
    padding: 0.2rem 0.7rem;
    border-radius: 20px;
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.03em;
}
.status-abierta  { background: #D8F3DC; color: #1B7F3A; }
.status-cerrada  { background: #FFE8D6; color: #A0522D; }
.status-pagado   { background: #D8F3DC; color: #1B7F3A; }
.status-pendiente{ background: #FFF3CD; color: #856404; }

/* ── Divider decorativo ───────────────────────────────────────── */
.cj-divider {
    border: none;
    height: 2px;
    background: linear-gradient(90deg, #2D6A4F22, #74C69D, #2D6A4F22);
    border-radius: 2px;
    margin: 1.5rem 0;
}

/* ── Empty state ──────────────────────────────────────────────── */
.empty-state {
    text-align: center;
    padding: 3rem 1rem;
    color: #8B9E8B;
}
.empty-state .empty-icon { font-size: 3rem; }
.empty-state p { font-size: 0.95rem; margin-top: 0.5rem; }

/* ── Toast/success msg ────────────────────────────────────────── */
.stSuccess { border-left: 4px solid #2D6A4F !important; }
.stError   { border-left: 4px solid #E63946 !important; }
.stWarning { border-left: 4px solid #C4733F !important; }
</style>
"""


def inject_css():
    """Inyecta los estilos globales. Llamar una vez por página."""
    st.markdown(CSS, unsafe_allow_html=True)


def page_header(icon: str, title: str, subtitle: str = ""):
    """Renderiza el encabezado estilo card verde."""
    sub = f"<p>{subtitle}</p>" if subtitle else ""
    st.markdown(
        f"""<div class="cj-header">
            <h1>{icon} {title}</h1>
            {sub}
        </div>""",
        unsafe_allow_html=True,
    )


def metric_row(metrics: list[dict]):
    """
    Renderiza una fila de tarjetas de métricas.
    metrics = [{"icon": "🌿", "value": 12, "label": "Participantes"}, ...]
    """
    cols = st.columns(len(metrics))
    for col, m in zip(cols, metrics):
        with col:
            st.markdown(
                f"""<div class="metric-card">
                    <div class="metric-icon">{m.get("icon","📊")}</div>
                    <div class="metric-value">{m["value"]}</div>
                    <div class="metric-label">{m["label"]}</div>
                </div>""",
                unsafe_allow_html=True,
            )


def section_label(text: str):
    st.markdown(f'<div class="section-label">{text}</div>', unsafe_allow_html=True)


def divider():
    st.markdown('<hr class="cj-divider">', unsafe_allow_html=True)


def empty_state(icon: str = "🌱", message: str = "No hay datos aún."):
    st.markdown(
        f"""<div class="empty-state">
            <div class="empty-icon">{icon}</div>
            <p>{message}</p>
        </div>""",
        unsafe_allow_html=True,
    )


def safe_query(table: str, select: str = "*") -> list:
    """Ejecuta una query a Supabase con manejo de errores."""
    try:
        from core.db import supabase
        return supabase.table(table).select(select).execute().data or []
    except Exception as e:
        st.error(f"❌ Error al consultar `{table}`: {e}")
        return []


def safe_insert(table: str, data: dict) -> bool:
    """Inserta un registro y retorna True si fue exitoso."""
    try:
        from core.db import supabase
        supabase.table(table).insert(data).execute()
        return True
    except Exception as e:
        st.error(f"❌ Error al guardar: {e}")
        return False


def safe_delete(table: str, row_id: str) -> bool:
    """Elimina un registro por ID."""
    try:
        from core.db import supabase
        supabase.table(table).delete().eq("id", row_id).execute()
        return True
    except Exception as e:
        st.error(f"❌ Error al eliminar: {e}")
        return False
