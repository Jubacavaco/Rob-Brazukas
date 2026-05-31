import streamlit as st
import requests

st.set_page_config(page_title="Robô Brazukas", layout="wide")
st.title("🚨 Painel de Controle - Robô Brazukas 🚨")

# --- ESTADO ---
if "executado" not in st.session_state: st.session_state.executado = False
if "res" not in st.session_state: st.session_state.res = "Nenhum"
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
    # Simulação do motor (Probabilidade fixa para teste)
    prob_calculada = 60 
    
    if prob_calculada >= 55:
        msg = (f"🚨 *Alerta de Entrada* 🚨\n\n"
               f"🏆 {campeonato} | {horario}\n"
               f"🆚 {time_casa} x {time_visitante}\n"
               f"👑 Favorito: {favorito}\n"
               f"💰 *Aposta:* Over 2.5 FT\n"
               f"👉 *Status:* {st.session_state.res}")
        
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
        
        # Botões de Edição
        if st.session_state.msg_id:
            st.subheader("🎯 Atualizar Resultado")
            c1, c2, c3 = st.columns(3)
            def editar(novo_status):
                st.session_state.res = novo_status
                msg_edit = msg.replace(f"👉 *Status:* Nenhum", f"👉 *Status:* {novo_status}")
                url = f"https://api.telegram.org/bot{token}/editMessageText"
                params = {"chat_id": chat_id, "message_id": st.session_state.msg_id, "text": msg_edit, "parse_mode": "Markdown"}
                requests.get(url, params=params)
                st.rerun()

            if c1.button("🟢 Green"): editar("Green")
            if c2.button("🔴 Red"): editar("Red")
            if c3.button("🟡 Push"): editar("Push")
    else:
        st.warning(f"⚠️ Nenhuma aposta recomendada (Probabilidade atual: {prob_calculada}% | Mínimo exigido: 55%)")
