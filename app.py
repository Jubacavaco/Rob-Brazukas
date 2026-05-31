import streamlit as st
import pandas as pd
import requests

# Configuração da página
st.set_page_config(page_title="Robô Brazukas", layout="wide")
st.title("🚨 Painel de Controle - Robô Brazukas 🚨")

# Estado da sessão
if "play_executado" not in st.session_state: st.session_state.play_executado = False
if "res" not in st.session_state: st.session_state.res = "Nenhum"

# SIDEBAR: Configuração (ID oculto)
st.sidebar.header("🤖 CONFIGURAÇÃO")
token = st.sidebar.text_input("🔑 Token do Bot:", type="password")
chat_id = st.sidebar.text_input("📢 ID do Canal (Oculto):", type="password")

st.sidebar.markdown("---")
campeonato = st.sidebar.text_input("🏆 Campeonato:", "Brasileirão")
time_casa = st.sidebar.text_input("🆚 Time Casa:", "Cruzeiro")
time_visitante = st.sidebar.text_input("🆚 Time Visitante:", "Fluminense")
horario = st.sidebar.text_input("⏰ Horário:", "16h00")

# Botão de Ação
if st.button("▶️ EXECUTAR ANÁLISE", type="primary"):
    st.session_state.play_executado = True

# Área de Resultados
if st.session_state.play_executado:
    st.subheader("🎯 Controle de Resultados")
    c1, c2, c3, c4 = st.columns(4)
    
    if c1.button("🟢 Green"): st.session_state.res = "Green"
    if c2.button("🔴 Red"): st.session_state.res = "Red"
    if c3.button("🟡 Push"): st.session_state.res = "Push"
    if c4.button("⚪ Reset"): st.session_state.res = "Nenhum"; st.session_state.play_executado = False
    
    selo = f"\n\n👉 *Resultado:* {st.session_state.res}" if st.session_state.res != "Nenhum" else ""
    
    # Exemplo de Alerta
    msg = (
        f"🚨 *Alerta de Entrada* 🚨\n\n"
        f"🏆 *Campeonato:* {campeonato}\n"
        f"🆚 *Jogo:* {time_casa} x {time_visitante}\n"
        f"⏰ *Horário:* {horario}\n"
        f"{selo}"
    )
    
    st.code(msg)
    
    if st.button("🚀 Enviar para o Telegram"):
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"}
        try:
            resp = requests.post(url, data=payload)
            if resp.status_code == 200:
                st.success("Enviado com sucesso!")
            else:
                st.error(f"Erro ao enviar: {resp.text}")
        except Exception as e:
            st.error(f"Erro de conexão: {e}")

else:
    st.info("Insira os dados e clique em 'EXECUTAR ANÁLISE'.")
