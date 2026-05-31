import streamlit as st
import re
import requests
import json
import pandas as pd

st.set_page_config(page_title="Robô Brazukas", layout="wide")

# --- SIDEBAR (Entradas) ---
st.sidebar.header("🛠️ Configurações")
token = st.sidebar.text_input("🔑 Token Telegram:", type="password")
chat_id = st.sidebar.text_input("📢 ID Canal:", type="password")

st.sidebar.header("📅 Dados do Jogo")
campeonato = st.sidebar.text_input("🏆 Campeonato:", "Brasileirão")
time_casa = st.sidebar.text_input("🆚 Time Casa:", "Cruzeiro")
time_visitante = st.sidebar.text_input("🆚 Time Visitante:", "Fluminense")
horario = st.sidebar.text_input("⏰ Horário:", "16h00")

st.sidebar.header("📊 Odds")
odd_casa = st.sidebar.number_input("Odd Casa:", 1.0)
odd_visitante = st.sidebar.number_input("Odd Fora:", 1.0)
odd_o15 = st.sidebar.number_input("Odd O1.5:", 1.0)
odd_btts = st.sidebar.number_input("Odd BTTS:", 1.0)
odd_o25 = st.sidebar.number_input("Odd O2.5:", 1.0)

# --- CORPO (Dados estatísticos) ---
st.header("📋 Dados e Análise")
lista_jogos = st.text_area("Cole a lista aqui (Últimos jogos / Confrontos diretos):", height=200)
resultado_aposta = st.selectbox("🎯 Resultado da Aposta:", ["Nenhum", "Green", "Red", "Push"])

if st.button("🚀 Processar e Enviar"):
    if not lista_jogos:
        st.warning("Por favor, cole os dados estatísticos.")
    else:
        # Aqui entra a lógica de cálculo que você já tem (extrair_dados_estatisticos)
        # O Streamlit vai processar e exibir abaixo
        st.success("Análise processada com sucesso!")
        
        # Exemplo de lógica de selo para o Telegram
        if resultado_aposta == "Green": selo = "\n\n✅✅ *GREEN!!* ✅✅"
        elif resultado_aposta == "Red": selo = "\n\n❌❌ *RED!* ❌❌"
        elif resultado_aposta == "Push": selo = "\n\n🔄🔄 *DEVOLVIDA* 🔄🔄"
        else: selo = ""
        
        st.write(f"Resultado escolhido: {resultado_aposta}")
        # AQUI você chamaria suas funções de enviar/editar para o Telegram
