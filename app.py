import streamlit as st
import requests

st.set_page_config(page_title="Robô Brazukas", layout="wide")
st.title("🚨 Painel de Controle - Robô Brazukas 🚨")

# --- ESTADO ---
if "executado" not in st.session_state: st.session_state.executado = False
if "res" not in st.session_state: st.session_state.res = "Nenhum"
if "msg_id" not in st.session_state: st.session_state.msg_id = None # ID para editar mensagem no Telegram

# --- SIDEBAR ---
st.sidebar.header("🤖 CONFIGURAÇÃO")
token = st.sidebar.text_input("🔑 Token:", type="password")
chat_id = st.sidebar.text_input("📢 ID Canal:", type="password")
favorito = st.sidebar.selectbox("👑 Favorito:", ["Equilibrado", "Casa", "Visitante"])

# --- LÓGICA DE ENVIO/EDIÇÃO ---
def enviar_ou_editar(msg, is_edit=False):
    url = f"https://api.telegram.org/bot{token}/"
    if is_edit and st.session_state.msg_id:
        url += f"editMessageText?chat_id={chat_id}&message_id={st.session_state.msg_id}&text={msg}&parse_mode=Markdown"
        requests.get(url)
    else:
        url += f"sendMessage?chat_id={chat_id}&text={msg}&parse_mode=Markdown"
        resp = requests.get(url).json()
        if resp.get("ok"): st.session_state.msg_id = resp["result"]["message_id"]

# --- CORPO ---
lista_jogos = st.text_area("Cole os dados aqui:", height=150, key="caixa_texto")

if st.button("▶️ EXECUTAR ANÁLISE"):
    st.session_state.executado = True
    st.session_state.res = "Nenhum"
    st.session_state.msg_id = None

if st.session_state.executado:
    # SIMULAÇÃO DE CÁLCULO (Aqui entram os seus ifs de probabilidade)
    prob = 50 # Exemplo: imagine que seu cálculo deu 50%
    if prob >= 55:
        recomendacao = "Over 2.5 FT"
        msg = f"🚨 *Alerta:* {recomendacao}\n👑 *Favorito:* {favorito}\n👉 *Status:* {st.session_state.res}"
        st.code(msg)
        if st.button("🚀 Enviar Sinal"): enviar_ou_editar(msg)
    else:
        st.warning(f"⚠️ Nenhuma entrada recomendada (Probabilidade atual: {prob}% | Mínimo: 55%)")

    # --- CONTROLE DE RESULTADOS ---
    if st.session_state.msg_id:
        st.subheader("🎯 Atualizar Resultado no Telegram")
        c1, c2, c3 = st.columns(3)
        if c1.button("🟢 Green"): st.session_state.res = "Green"; enviar_ou_editar(msg.replace("Nenhum", "Green"), True)
        if c2.button("🔴 Red"): st.session_state.res = "Red"; enviar_ou_editar(msg.replace("Nenhum", "Red"), True)
        if c3.button("🟡 Push"): st.session_state.res = "Push"; enviar_ou_editar(msg.replace("Nenhum", "Push"), True)
