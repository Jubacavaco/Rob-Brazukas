import streamlit as st
import requests

st.set_page_config(layout="wide", page_title="Painel Brazukas")
st.title("🤖 Painel Brazukas")

# Carrega os dados do Secrets
try:
    TOKEN = st.secrets["token"]
    CHAT_ID = st.secrets["chat_id"]
except:
    st.error("Configurações não encontradas no Secrets.")
    st.stop()

# Campos de entrada
col1, col2 = st.columns(2)
with col1:
    camp = st.text_input("Campeonato")
    jogo = st.text_input("Jogo")
    horario = st.text_input("Horário")
with col2:
    mercado_p = st.text_input("Mercado Principal")
    mercado_s = st.text_input("Mercado Secundário (Escanteios)")
    alerta = st.text_input("Alerta de Entrada")

if st.button("Enviar Dica"):
    # Modelo da mensagem conforme solicitado
    mensagem = (
        f"🏆 *Campeonato:* {camp}\n"
        f"⚽ *Jogo:* {jogo}\n"
        f"🎯 *Mercado Principal:* {mercado_p}\n"
        f"Corner: {mercado_s}\n"
        f"⏰ *Horário:* {horario}\n"
        f"📢 *Alerta de Entrada:* {alerta}"
    )
    
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    params = {"chat_id": CHAT_ID, "text": mensagem, "parse_mode": "Markdown"}
    
    response = requests.post(url, data=params)
    
    if response.status_code == 200:
        st.success("✅ Dica enviada com sucesso!")
    else:
        st.error(f"❌ Erro ao enviar: {response.text}")
