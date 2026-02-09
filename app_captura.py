import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# ================== CONFIG STREAMLIT ==================
st.set_page_config(
    page_title="Captura Producción y Entregas",
    layout="wide"
)

st.title("📋 Captura de Producción y Entregas")

# ================== CONEXIÓN GOOGLE SHEETS ==================
SCOPE = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    "credenciales.json",
    SCOPE
)

client = gspread.authorize(creds)

# ID REAL DE TU GOOGLE SHEET
sheet = client.open_by_key(
    "1DADTq-dCsl-7y3_7P2mFAe3CUaHDKsDcqbQTtdQ30SY"
)

# NOMBRES EXACTOS DE LAS HOJAS (CON ESPACIOS)
ws_prod = sheet.worksheet("CAPTURA PRODUCCION")
ws_ent = sheet.worksheet("CAPTURA ENTREGAS")

# ================== TABS ==================
tab_prod, tab_ent = st.tabs(["🏭 Producción", "🚚 Entregas"])

# ================== PRODUCCIÓN ==================
with tab_prod:
    st.subheader("Captura de Producción por Hora")

    fecha = st.date_input("Fecha", datetime.today())
    hora = st.selectbox(
        "Hora",
        [f"{h:02d}:00" for h in range(5, 22)]
    )

    area = st.selectbox(
        "Área",
        [
            "Corte", "Quemado", "Rizado",
            "Tapa pintada", "Tapa recuperada",
            "Tapa troquelada", "Tapa formada",
            "Planchado", "Pulido 1", "Pulido 2",
            "Detallado", "Pintado",
            "Ensamble", "Serigrafiado", "Embarcado"
        ]
    )

    operador = st.text_input("Operador")
    maquina = st.text_input("Máquina / Proceso")

    op = st.text_input(
        "OP (o NA / Recuperado / Retrabajo)"
    )

    piezas = st.number_input(
        "Tambos realizados",
        min_value=0,
        step=1
    )

    rechazos = st.number_input(
        "Rechazos",
        min_value=0,
        step=1
    )

    tipo_rechazo = st.multiselect(
        "Tipo de Rechazo",
        [
            "Golpeado",
            "Repintado",
            "Retocado",
            "Mal pintado"
        ]
    )

    if st.button("💾 Guardar Producción"):
        ws_prod.append_row([
            str(fecha),
            hora,
            area,
            operador,
            maquina,
            op,
            piezas,
            rechazos,
            ", ".join(tipo_rechazo)
        ])
        st.success("✅ Producción registrada correctamente")

# ================== ENTREGAS ==================
with tab_ent:
    st.subheader("Captura de Pedidos por Entregar")

    fecha_entrega = st.date_input(
        "Fecha de Entrega",
        datetime.today(),
        key="fecha_ent"
    )

    cliente = st.text_input("Cliente")
    op_entrega = st.text_input("OP relacionada")

    cantidad = st.number_input(
        "Cantidad de Tambos",
        min_value=0,
        step=1
    )

    condicion = st.selectbox(
        "Condición del Tambo",
        [
            "Primera",
            "Lechero",
            "Standard",
            "Tercera"
        ]
    )

    if st.button("💾 Guardar Entrega"):
        ws_ent.append_row([
            str(fecha_entrega),
            cliente,
            op_entrega,
            cantidad,
            condicion
        ])
        st.success("✅ Pedido registrado correctamente")
