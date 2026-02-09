import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import plotly.express as px

# ---------------- CONEXIÓN ----------------
SCOPE = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    "credenciales.json", SCOPE
)

client = gspread.authorize(creds)
sheet = client.open_by_key("1DADTq-dCsl-7y3_7P2mFAe3CUaHDKsDcqbQTtdQ30SY")

df_prod = pd.DataFrame(sheet.worksheet("CAPTURA_PRODUCCION").get_all_records())
df_ent = pd.DataFrame(sheet.worksheet("CAPTURA_ENTREGAS").get_all_records())

st.set_page_config(page_title="Indicadores", layout="wide")
st.title("📊 Indicadores Ejecutivos")

menu = st.radio("Selecciona vista", ["Producción", "Entregas"])

# ---------------- PRODUCCIÓN ----------------
if menu == "Producción":
    st.subheader("Producción General")

    df_prod["Fecha"] = pd.to_datetime(df_prod["Fecha"])

    fecha_sel = st.date_input(
        "Selecciona Fecha",
        df_prod["Fecha"].max()
    )

    df_f = df_prod[df_prod["Fecha"] == pd.to_datetime(fecha_sel)]

    kpi1, kpi2, kpi3 = st.columns(3)

    kpi1.metric("Tambos del Día", int(df_f["Tambos realizados"].sum()))
    kpi2.metric("Total Rechazos", int(df_f["Rechazos"].sum()))

    retrabajo = df_f[df_f["OP (o NA / Recuperado / Retrabajo)"] == "Retrabajo"]["Tambos realizados"].sum()
    kpi3.metric("Retrabajo", int(retrabajo))

    st.divider()

    fig_area = px.bar(
        df_f,
        x="Área",
        y="Tambos realizados",
        title="Producción por Área"
    )
    st.plotly_chart(fig_area, use_container_width=True)

    df_rech = df_f.assign(
        Tipo=df_f["Tipo de Rechazo"].str.split(", ")
    ).explode("Tipo")

    fig_rech = px.pie(
        df_rech,
        names="Tipo",
        title="Rechazos por Tipo"
    )
    st.plotly_chart(fig_rech, use_container_width=True)

# ---------------- ENTREGAS ----------------
else:
    st.subheader("Seguimiento de Entregas")

    fig_cliente = px.bar(
        df_ent,
        x="Cliente",
        y="Cantidad de Tambos",
        color="Condición de Tambo",
        title="Pedidos por Cliente"
    )

    st.plotly_chart(fig_cliente, use_container_width=True)

    fig_gantt = px.timeline(
        df_ent,
        x_start="Fecha Entrega",
        x_end="Fecha Entrega",
        y="OP relacionada",
        color="Cliente",
        title="Gantt General de OP"
    )

    st.plotly_chart(fig_gantt, use_container_width=True)
