import streamlit as st
import requests

# Configuração da página
st.set_page_config(page_title="Robô Brazukas", layout="wide")
st.title("🚨 Painel de Controle - Robô Brazukas 🚨")

# --- ESTADO DA SESSÃO ---
if "executado" not in st.session_state: st.session_state.executado = False
if "res" not in st.session_state: st.session_state.res = "Nenhum"

# --- SIDEBAR: Configuração ---
st.sidebar.header("🤖 CONFIGURAÇÃO")
token = st.sidebar.text_input("🔑 Token do Bot:", type="password")
chat_id = st.sidebar.text_input("📢 ID do Canal (Oculto):", type="password")
st.sidebar.markdown("---")
campeonato = st.sidebar.text_input("🏆 Campeonato:", "Brasileirão")
time_casa = st.sidebar.text_input("🆚 Time Casa:", "Cruzeiro")
time_visitante = st.sidebar.text_input("🆚 Time Visitante:", "Fluminense")
horario = st.sidebar.text_input("⏰ Horário:", "16h00")

# --- CORPO: Entrada de dados ---
st.subheader("📋 Dados Estatísticos")
# Usamos 'key' para o Streamlit não apagar o texto ao clicar em botões
lista_jogos = st.text_area("Cole o texto bruto de histórico aqui:", height=150, key="caixa_texto")

# Botão de Ação
if st.button("▶️ EXECUTAR ANÁLISE", type="primary"):
    if st.session_state.caixa_texto:
        st.session_state.executado = True
    else:
        st.warning("A caixa de texto está vazia!")

# --- RESULTADOS ---
if st.session_state.executado:
    st.markdown("---")
    st.subheader("🎯 Controle de Resultados")
    
    col1, col2, col3, col4 = st.columns(4)
    if col1.button("🟢 Green"): st.session_state.res = "Green"
    if col2.button("🔴 Red"): st.session_state.res = "Red"
    if col3.button("🟡 Push"): st.session_state.res = "Push"
    if col4.button("⚪ Resetar"): 
        st.session_state.executado = False
        st.session_state.res = "Nenhum"
        st.rerun() # Força a atualização da tela
    
    selo = f"\n\n👉 *Resultado:* {st.session_state.res}" if st.session_state.res != "Nenhum" else ""
    
    msg = (f"🚨 *Alerta de Entrada* 🚨\n\n🏆 *Campeonato:* {campeonato}\n"
           f"🆚 *Jogo:* {time_casa} x {time_visitante}\n⏰ *Horário:* {horario}\n{selo}")
    
    st.code(msg)
    
    if st.button("🚀 Enviar para o Telegram"):
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"}
        try:
            resp = requests.post(url, data=payload)
            if resp.status_code == 200: st.success("Enviado!")
            else: st.error(f"Erro: {resp.text}")
        except Exception as e: st.error(f"Erro: {e}")
