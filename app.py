import streamlit as st
import requests

st.set_page_config(page_title="Robô Brazukas", layout="wide")
st.title("🚨 Painel de Controle - Robô Brazukas 🚨")

# --- ESTADO ---
if "executado" not in st.session_state: st.session_state.executado = False

# --- SIDEBAR COMPLETA ---
st.sidebar.header("🤖 CONFIGURAÇÃO")
token = st.sidebar.text_input("🔑 Token:", type="password")
chat_id = st.sidebar.text_input("📢 ID Canal:", type="password")

st.sidebar.header("📅 DADOS DO JOGO")
campeonato = st.sidebar.text_input("🏆 Campeonato:")
time_casa = st.sidebar.text_input("🆚 Time Casa:")
time_visitante = st.sidebar.text_input("🆚 Time Visitante:")
horario = st.sidebar.text_input("⏰ Horário:")

st.sidebar.header("📊 ODDS (Para Cálculo)")
# Campos adicionados conforme solicitado
odd_casa = st.sidebar.number_input("Odd Time Casa:", value=1.0, step=0.01)
odd_visitante = st.sidebar.number_input("Odd Time Visitante:", value=1.0, step=0.01)
odd_o15 = st.sidebar.number_input("Odd Over 1.5:", value=1.0, step=0.01)
odd_o25 = st.sidebar.number_input("Odd Over 2.5:", value=1.0, step=0.01)
odd_btts = st.sidebar.number_input("Odd BTTS:", value=1.0, step=0.01)

# --- CORPO ---
st.subheader("📋 Dados Estatísticos")
# Cole a lista de jogos AQUI no seu navegador
lista_jogos = st.text_area("Cole a lista aqui:", height=150)

if st.button("▶️ EXECUTAR ANÁLISE"):
    if lista_jogos:
        st.session_state.executado = True
    else:
        st.warning("Cole a lista de jogos no campo acima primeiro!")

if st.session_state.executado:
    # MENSAGEM SEGUINDO SEU PADRÃO
    msg = (f"🚨 *Alerta de Entrada* 🚨\n\n"
           f"🏆 *Campeonato:* {campeonato}\n"
           f"🆚 *Jogo:* {time_casa} x {time_visitante}\n"
           f"🎯 *Mercado Principal:* Over 2.5 FT\n"
           f"⚽ *Mercado Secundário (Escanteios):* Analisar ao vivo\n"
           f"⏰ *Horário:* {horario}\n"
           f"⚠️ *Alerta de Entrada:* Entrada recomendada!")
    
    st.code(msg)
    
    if st.button("🚀 Enviar Sinal"):
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        params = {"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"}
        resp = requests.get(url, params=params).json()
        if resp.get("ok"):
            st.success("Sinal enviado!")
        else:
            st.error(f"Erro: {resp.get('description')}")

    # CONTROLE DE RESULTADOS
    st.subheader("🎯 Registrar Resultado")
    c1, c2, c3, c4 = st.columns(4)
    if c1.button("🟢 Green"): st.success("Green registrado!")
    if c2.button("🔴 Red"): st.error("Red registrado!")
    if c3.button("🟡 Push"): st.warning("Push registrado!")
    if c4.button("⚪ Resetar"): st.session_state.executado = False; st.rerun()
