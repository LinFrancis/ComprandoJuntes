
# 🐷 Comprando Juntes
## Sistema Comunitario de Coordinación de Compras de Alimentos

Este proyecto es una herramienta digital diseñada para apoyar redes comunitarias que organizan **compras colectivas de alimentos directamente desde productores locales**.

El sistema permite que grupos de personas coordinen pedidos, compras, distribución y pagos de manera transparente.

El objetivo es simple:

**acercar a quienes producen alimentos con quienes los consumen, reduciendo intermediarios y fortaleciendo relaciones locales.**

---

# Filosofía del sistema

Los sistemas vivos funcionan mejor cuando:

- la información es clara
- las responsabilidades son compartidas
- las decisiones se toman con transparencia

Este software no busca controlar la red.

Busca **hacer visible lo que ya está ocurriendo**:

- personas organizándose
- alimentos circulando
- cooperación creciendo

La plataforma permite observar esos flujos para facilitar la coordinación.

---

# Principios de funcionamiento de la red

Estos principios pueden adaptarse por cada comunidad.

### 1. Cooperación
La iniciativa se sostiene gracias al aporte voluntario de tiempo y energía de las personas.

Las tareas pueden incluir:

- búsqueda de productores
- coordinación de pedidos
- transporte
- envasado
- distribución
- administración de pagos

### 2. Transparencia
Toda la información relevante debe quedar registrada en el sistema:

- qué se pidió
- qué se compró
- cuánto costó
- cuánto recibió cada persona
- qué pagos se realizaron

Esto permite confianza entre participantes.

### 3. Consumo responsable
Siempre que sea posible se prioriza:

- producción local
- alimentos sin agroquímicos
- compra a granel
- reducción de residuos

### 4. Participación
Las personas pueden participar en distintos roles según su disponibilidad.

Nadie tiene que hacerlo todo.

Pero todas las tareas son importantes.

---

# Flujo de una ronda de compra

Una ronda de compra sigue normalmente estas etapas:

### 1 Apertura
Se abre una ronda donde las personas pueden solicitar productos.

### 2 Registro de pedidos
Cada participante indica cuánto quiere comprar.

### 3 Consolidación
Se suman todos los pedidos para calcular el volumen total.

### 4 Compra al productor
Se registra la compra real realizada.

### 5 Distribución
Los productos se dividen entre quienes hicieron pedidos.

### 6 Registro de pagos
Cada participante registra el pago correspondiente.

### 7 Cierre
La ronda queda archivada como registro histórico.

---

# Qué permite hacer la aplicación

La aplicación incluye módulos para:

• Participantes  
• Productores  
• Productos  
• Rondas de compra  
• Pedidos  
• Compras  
• Distribución  
• Pagos  
• Reportes descargables

---

# Reportes

En cualquier momento se puede generar un reporte Excel con:

- participantes
- pedidos
- compras
- pagos

Esto permite compartir fácilmente el estado del sistema con el grupo.

---

# Instalación

## 1 Instalar Python

Python 3.10 o superior.

Verificar:

python --version

---

## 2 Instalar dependencias

pip install -r requirements.txt

---

## 3 Crear proyecto en Supabase

Ir a:

https://supabase.com

Crear un nuevo proyecto.

---

## 4 Ejecutar el esquema SQL

Copiar el contenido del archivo:

schema.sql

y ejecutarlo en el SQL Editor de Supabase.

---

## 5 Crear archivo .env

SUPABASE_URL=tu_url
SUPABASE_KEY=tu_key

---

## 6 Ejecutar aplicación

streamlit run app.py

---

# Estructura del proyecto

```
comprando_juntes_erp

app.py
schema.sql
requirements.txt

core/
db.py
excel.py

pages/
Participantes
Productos
Productores
Rondas
Pedidos
Compras
Distribucion
Pagos
Reportes

assets/
pig.svg
```

---

# Uso recomendado en la comunidad

Se recomienda que el grupo tenga al menos:

• una persona que coordine rondas  
• una persona que registre compras  
• una persona que revise pagos  

Las responsabilidades pueden rotar.

---

# Evolución futura

Este sistema puede evolucionar hacia:

- cálculo automático de precios por persona
- visualización del flujo de alimentos
- integración con formularios públicos
- métricas de impacto comunitario

---

# Licencia

Uso libre para comunidades.
