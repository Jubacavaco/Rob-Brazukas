import streamlit as st
import requests

# Configuração básica da página
st.set_page_config(layout="wide", page_title="Painel Brazukas")
st.title("🤖 Painel Brazukas")

# Tenta ler as credenciais do cofre que criaste no GitHub
try:
    TOKEN = st.secrets["token"]
    CHAT_ID = st.secrets["chat_id"]
    st.success("✅ Configurações carregadas com sucesso!")
except Exception as e:
    st.error("❌ Erro ao ler os segredos. Verifica se o ficheiro .streamlit/secrets.toml existe no GitHub.")
    st.stop()

# --- AQUI COMEÇA O TEU PAINEL (O resto do teu código) ---
# Exemplo de um formulário que usa o TOKEN e o CHAT_ID que carregámos acima:

camp = st.text_input("Campeonato")
jogo = st.text_input("Jogo")
hora = st.text_input("Horário")

if st.button("Enviar Alerta"):
    mensagem = f"🚨 {camp} | {jogo} | {hora}"
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={mensagem}"
    requests.get(url)
    st.write("Alerta enviado!")
