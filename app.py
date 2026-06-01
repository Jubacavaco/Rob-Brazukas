import streamlit as st
import requests

# Configuração da página
st.set_page_config(layout="wide", page_title="Painel Brazukas")
st.title("🤖 Painel Brazukas")

# Tenta ler as credenciais do "cofre" (secrets) automaticamente
try:
    TOKEN = st.secrets["token"]
    CHAT_ID = st.secrets["chat_id"]
except Exception:
    st.error("Erro: Não encontrei o ficheiro .streamlit/secrets.toml no GitHub ou o formato está errado.")
    st.stop()

# Campos de entrada
camp = st.text_input("Campeonato")
jogo = st.text_input("Jogo")
mercado_p = st.text_input("Mercado Principal")
mercado_s = st.text_input("Mercado Secundário (Escanteios)")
horario = st.text_input("Horário")
alerta = st.text_input("Alerta de Entrada")

# Botão de envio
if st.button("Enviar para o Telegram"):
    mensagem = (f"⚽ Campeonato: {camp}\n"
                f"⚔️ Jogo: {jogo}\n"
                f"🎯 Mercado: {mercado_p}\n"
                f"Corner: {mercado_s}\n"
                f"⏰ Horário: {horario}\n"
                f"⚠️ Alerta: {alerta}")
    
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    params = {"chat_id": CHAT_ID, "text": mensagem}
    
    response = requests.post(url, data=params)
    
    if response.status_code == 200:
        st.success("✅ Mensagem enviada com sucesso!")
    else:
        st.error(f"❌ Erro ao enviar: {response.text}")
