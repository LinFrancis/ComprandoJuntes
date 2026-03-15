
import streamlit as st

st.set_page_config(page_title="Comprando Juntes",page_icon="🐷",layout="wide")

st.title("🐷 Comprando Juntes")

st.image("assets/pig.svg",width=140)

st.markdown("""
Bienvenida a la plataforma de coordinación de compras colectivas.

Este espacio permite que un grupo de personas organice el flujo completo
de alimentos desde productores hasta los hogares.

La aplicación registra:

- personas
- productores
- productos
- pedidos
- compras
- distribución
- pagos

Usa el menú lateral para recorrer las distintas etapas.
""")

st.info("""
Cada sección explica qué información registrar y por qué.
Esto permite que cualquier persona del grupo pueda participar
en la coordinación de la red.
""")
