# 🐷 Comprando Juntes

Plataforma de coordinación de compras colectivas · Red de alimentos de proximidad.

## Estructura

```
comprandojuntes/
├── app.py                        # Página principal
├── pages/
│   ├── 1_Participantes.py
│   ├── 2_Productos.py
│   ├── 3_Productores.py
│   ├── 4_Rondas.py
│   ├── 5_Pedidos.py
│   ├── 6_Compras.py
│   ├── 7_Distribucion.py
│   ├── 8_Pagos.py
│   └── 9_Reportes.py
├── core/
│   ├── db.py                     # Conexión Supabase
│   ├── ui.py                     # Sistema de diseño compartido
│   └── excel.py                  # Exportación Excel
├── assets/
│   └── pig.svg
├── .streamlit/
│   ├── config.toml               # Tema visual
│   └── secrets.toml              # Credenciales (NO subir a git)
├── schema.sql
└── requirements.txt
```

## Despliegue en Streamlit Cloud

1. Sube el repositorio a GitHub (**sin** `.streamlit/secrets.toml`)
2. En Streamlit Cloud → *Manage app* → *Secrets*, agrega:

```toml
[supabase]
url = "https://tu-proyecto.supabase.co"
key = "tu-clave-secreta"
```

3. Deploy 🚀

## Desarrollo local

Crea `.streamlit/secrets.toml`:

```toml
[supabase]
url = "https://tu-proyecto.supabase.co"
key = "tu-clave-secreta"
```

Luego:

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Base de datos

Ejecuta `schema.sql` en tu proyecto Supabase para crear las tablas.
