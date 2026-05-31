import streamlit as st
import requests
import re
import pandas as pd

st.set_page_config(page_title="Robô Brazukas", layout="wide")
st.title("🤖 Painel Brazukas - Decisão e Envio")

# --- SIDEBAR: DADOS E ODDS ---
st.sidebar.header("⚙️ Configurações")
token = st.sidebar.text_input("Token Telegram", type="password")
chat_id = st.sidebar.text_input("ID Canal")

st.sidebar.header("📅 Dados do Jogo")
campeonato = st.sidebar.text_input("Campeonato")
time_casa = st.sidebar.text_input("Time Casa")
time_visitante = st.sidebar.text_input("Time Visitante")
horario = st.sidebar.text_input("Horário")
favorito = st.sidebar.selectbox("Favorito", ["Casa", "Visitante", "Nenhum / Equilibrado"])

st.sidebar.header("📊 Odds")
odd_casa = st.sidebar.number_input("Odd Casa", 1.0)
odd_visitante = st.sidebar.number_input("Odd Visitante", 1.0)
odd_o15 = st.sidebar.number_input("Odd O1.5", 1.0)
odd_btts = st.sidebar.number_input("Odd BTTS", 1.0)
odd_o25 = st.sidebar.number_input("Odd O2.5", 1.0)

# --- CORPO: DADOS ESTATÍSTICOS ---
lista_jogos = st.text_area("📋 Cole aqui a lista de jogos (formato estatístico):", height=200)

# --- MEMÓRIA ---
if "msg_id" not in st.session_state: st.session_state.msg_id = None
if "ultima_msg" not in st.session_state: st.session_state.ultima_msg = ""

if st.button("🚀 Analisar e Enviar Sinal"):
    # Lógica de Cálculo (Simplificada para o Streamlit processar)
    # Aqui você pode inserir a sua lógica de extração de gols que já usa
    
    # Exemplo de decisão baseada nos campos da sidebar:
    if odd_o25 < 2.10:
        msg = f"🚨 *Alerta de Entrada* 🚨\n\n🏆 *Campeonato:* {campeonato}\n🆚 *Jogo:* {time_casa} x {time_visitante}\n🎯 *Mercado:* Over 2.5 FT\n⏰ *Horário:* {horario}\n\n📌 Entrada recomendada!"
    else:
        msg = f"🚨 *Alerta de Entrada* 🚨\n\n🏆 *Campeonato:* {campeonato}\n🆚 *Jogo:* {time_casa} x {time_visitante}\n🎯 *Mercado:* Match Odds (LTD)\n⭐ *Favorito:* {favorito}\n⏰ *Horário:* {horario}\n\n📌 Entrada recomendada!"
    
    # Envio
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"}
    resp = requests.post(url, data=payload).json()
    
    if resp.get("ok"):
        st.session_state.msg_id = resp["result"]["message_id"]
        st.session_state.ultima_msg = msg
        st.success("Sinal enviado!")
    else:
        st.error(f"Erro: {resp.get('description')}")

# --- ATUALIZAÇÃO ---
if st.session_state.msg_id:
    st.subheader("🎯 Resultado")
    col1, col2, col3 = st.columns(3)
    
    def atualizar(status_texto):
        nova_msg = st.session_state.ultima_msg + f"\n\n🔄 *Status:* {status_texto}"
        url = f"https://api.telegram.org/bot{token}/editMessageText"
        payload = {"chat_id": chat_id, "message_id": st.session_state.msg_id, "text": nova_msg, "parse_mode": "Markdown"}
        requests.post(url, data=payload)
        st.success("Atualizado!")

    if col1.button("✅ GREEN"): atualizar("✅✅ GREEN!!")
    if col2.button("❌ RED"): atualizar("❌❌ RED!")
    if col3.button("🔄 DEVOLVIDA"): atualizar("🔄🔄 DEVOLVIDA")
