import streamlit as st
import requests

st.set_page_config(layout="wide", page_title="Painel Brazukas")
st.title("🤖 Painel Brazukas")

# Aqui ele vai buscar ao cofre sem te pedir nada
try:
    TOKEN = st.secrets["token"]
    CHAT_ID = st.secrets["chat_id"]
except:
    st.error("Configuração não encontrada. Vai a 'Manage App' > 'Settings' > 'Secrets' no Streamlit.")
    st.stop()

# Aqui começa o teu painel normal
st.write("Configurações carregadas com sucesso!")
# ... (o resto do teu código dos jogos aqui)
