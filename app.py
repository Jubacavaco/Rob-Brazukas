import streamlit as st
import requests

st.set_page_config(page_title="Robô Brazukas", layout="wide")
st.title("🚨 Painel de Controle - Robô Brazukas 🚨")

# --- ESTADO ---
if "executado" not in st.session_state: st.session_state.executado = False
if "msg_id" not in st.session_state: st.session_state.msg_id = None

# --- SIDEBAR COMPLETA ---
st.sidebar.header("🤖 CONFIGURAÇÃO")
token = st.sidebar.text_input("🔑 Token:", type="password")
chat_id = st.sidebar.text_input("📢 ID Canal:", type="password")

st.sidebar.header("📅 DADOS DO JOGO")
campeonato = st.sidebar.text_input("🏆 Campeonato:", "Brasileirão")
time_casa = st.sidebar.text_input("🆚 Time Casa:", "Cruzeiro")
time_visitante = st.sidebar.text_input("🆚 Time Visitante:", "Fluminense")
horario = st.sidebar.text_input("⏰ Horário:", "16h00")
favorito = st.sidebar.selectbox("👑 Favorito:", ["Equilibrado", "Casa", "Visitante"])

st.sidebar.header("📊 ODDS")
odd_o15 = st.sidebar.number_input("Odd Over 1.5:", value=1.30, step=0.01)
odd_o25 = st.sidebar.number_input("Odd Over 2.5:", value=2.00, step=0.01)
odd_btts = st.sidebar.number_input("Odd BTTS:", value=1.90, step=0.01)

# --- CORPO ---
st.subheader("📋 Dados Estatísticos")
lista_jogos = st.text_area("Cole a lista aqui:", height=150, key="caixa_texto")

# --- LÓGICA ---
if st.button("▶️ EXECUTAR ANÁLISE"):
    if st.session_state.caixa_texto:
        st.session_state.executado = True
        st.session_state.msg_id = None
    else:
        st.warning("Cole a lista de jogos primeiro!")

if st.session_state.executado:
    prob_calculada = 60 
    
    if prob_calculada >= 55:
        # MENSAGEM LIMPA (Sem favorito, sem status)
        msg = (f"🚨 *Alerta de Entrada* 🚨\n\n"
               f"🏆 *Campeonato:* {campeonato}\n"
               f"⏰ *Horário:* {horario}\n"
               f"🆚 *Jogo:* {time_casa} x {time_visitante}\n"
               f"💰 *Aposta:* Over 2.5 FT")
        
        st.code(msg)
        
        # Botão de Envio
        if not st.session_state.msg_id:
            if st.button("🚀 Enviar Sinal"):
                if not token or not chat_id:
                    st.error("Preencha o Token e o ID do Canal na barra lateral!")
                else:
                    url = f"https://api.telegram.org/bot{token}/sendMessage"
                    params = {"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"}
                    try:
                        resp = requests.get(url, params=params)
                        data = resp.json()
                        if data.get("ok"):
                            st.session_state.msg_id = data["result"]["message_id"]
                            st.success("Sinal enviado com sucesso!")
                        else:
                            st.error(f"Erro do Telegram: {data.get('description')}")
                    except Exception as e:
                        st.error(f"Erro de conexão: {e}")
        
        # Botões de Controle (Apenas para seu controle no Painel)
        if st.session_state.msg_id:
            st.subheader("🎯 Controle de Resultados (Local)")
            c1, c2, c3, c4 = st.columns(4)
            if c1.button("🟢 Green"): st.success("Green registrado!")
            if c2.button("🔴 Red"): st.error("Red registrado!")
            if c3.button("🟡 Push"): st.warning("Push registrado!")
            if c4.button("⚪ Resetar"): st.session_state.executado = False; st.session_state.msg_id = None; st.rerun()
    else:
        st.warning(f"⚠️ Nenhuma aposta recomendada (Probabilidade atual: {prob_calculada}% | Mínimo: 55%)")
