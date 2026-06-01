import streamlit as st
import requests
import re

st.set_page_config(layout="wide")
st.title("🤖 Painel Brazukas v2")

# Sidebar
token = st.sidebar.text_input("Token Telegram", type="password")
chat_id = st.sidebar.text_input("ID Canal", type="password")

# Função de Jogo simplificada
def render_jogo(label):
    st.subheader(f"🏟️ {label}")
    with st.form(f"form_{label}"):
        camp = st.text_input("Campeonato")
        lista = st.text_area("Lista de jogos")
        submit = st.form_submit_button("Analisar")
        
        if submit:
            st.write(f"Analisando lista de {label}...")
            # Lógica simples de teste
            st.success("Configurado!")

# Dividir em colunas
c1, c2 = st.columns(2)
with c1: render_jogo("Jogo 1")
with c2: render_jogo("Jogo 2")
