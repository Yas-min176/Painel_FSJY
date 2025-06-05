
import streamlit as st
import pandas as pd
import plotly.express as px
from connection import carregar_dados_planilhas
from export import gerar_html

st.set_page_config(layout="wide", page_title="Painel_FSJY")

# Links das planilhas
links_codigos = {
    "K01": "https://docs.google.com/spreadsheets/d/1RXO-gZc8mJEnhINDZVmflNGNs5J8Q6nXSVHj_4XxZb8/edit",
    "L320": "https://docs.google.com/spreadsheets/d/11d9N_jb_Pyb1XBGPkJwooXoWIPRX3bB05aJP2ihjqZQ/edit",
    "L382": "https://docs.google.com/spreadsheets/d/1Yj-J8arzyPuMPm_2uOsVzL3HlNLEe67vUcOi6OdFUH8/edit",
    "L555": "https://docs.google.com/spreadsheets/d/1dt-sR65q-Q2uqZ_iwWGyzlzOyQMbkLJhenYMleGysW4/edit",
    "L655": "https://docs.google.com/spreadsheets/d/1X_Hq7DblsXhuo8IheJvmGbS67pnjkO4NKopBqIN6vm0/edit",
    "TF19": "https://docs.google.com/spreadsheets/d/1jBYFDYKNaY-OxuqS4Xglt0GJhdOSNjQ5yFEKUsxarv0/edit",
    "TF20": "https://docs.google.com/spreadsheets/d/1zNzg5AGcIZAsK8UWiLVPmTXm6NJqebFUoMrIE_eXFFI/edit",
    "TF28": "https://docs.google.com/spreadsheets/d/1fqWn2q39c1pOS9FXjHf8jxqcExwZqjzDiqXOjmFIZ24/edit",
    "TF106": "https://docs.google.com/spreadsheets/d/1TgOYmAazMwYJ8GpgOjTT8gRtVq88rVO4H7AESbcN0L4/edit",
    "TF125": "https://docs.google.com/spreadsheets/d/1Zv_2U-XmL0iBgCXeH5xz_UzprUUzVBJRnRlG19z-A5w/edit",
    "TF153": "https://docs.google.com/spreadsheets/d/1AN4aKX1Lq3lG_-SBMJ5LWlAtevevt4K-pvg3cJSPCks/edit",
    "TF460": "https://docs.google.com/spreadsheets/d/1LYIpFKLgAuYv2qrwL39ZvkY9L2fF3Y4asLFNsDO3nk4/edit"
}

# Carrega os dados
st.title("📊 Painel de Gastos - Frota FSJY")
with st.spinner("Carregando dados..."):
    df = carregar_dados_planilhas(links_codigos)

# Verificação de segurança
if df.empty or "Veículo" not in df.columns or "Funcionário" not in df.columns or "Valor" not in df.columns:
    st.warning("⚠️ Não foi possível carregar os dados. Verifique se as planilhas estão acessíveis, possuem dados e a aba 'Respostas ao formulário 1'.")
    st.stop()

# Filtros
veiculos = st.multiselect("Filtrar por veículo", options=df["Veículo"].unique(), default=df["Veículo"].unique())
funcionarios = st.multiselect("Filtrar por funcionário", options=df["Funcionário"].unique(), default=df["Funcionário"].unique())

df_filtrado = df[df["Veículo"].isin(veiculos) & df["Funcionário"].isin(funcionarios)]

st.dataframe(df_filtrado, use_container_width=True)

# Gráficos
col1, col2 = st.columns(2)

with col1:
    graf1 = px.bar(df_filtrado, x="Veículo", y="Valor", color="Funcionário", title="Gastos por Veículo")
    st.plotly_chart(graf1, use_container_width=True)

with col2:
    graf2 = px.pie(df_filtrado, names="Funcionário", values="Valor", title="Participação por Funcionário")
    st.plotly_chart(graf2, use_container_width=True)

# Botão de PDF
if st.button("📄 Gerar Relatório em PDF"):
    gerar_html(df_filtrado, f"Veículos: {veiculos}, Funcionários: {funcionarios}")
    st.success("PDF gerado como relatorio.pdf!")
