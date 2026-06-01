import streamlit as st
import requests
import re

st.set_page_config(layout="wide")

# Verificação simples de Secrets
if "token" not in st.secrets:
    st.error("Erro: O Token não está configurado no Secrets do Streamlit!")
    st.stop()

TOKEN = st.secrets["token"]
CHAT_ID = st.secrets["chat_id"]

def calcular_probabilidade(texto):
    numeros = re.findall(r'\d+', texto)
    gols = [int(n) for n in numeros if int(n) <= 10]
    if len(gols) < 2: return 0
    return min((sum(gols) / len(gols)) * 20, 100)

st.title("Sistema Brazukas")

# Apenas um bloco de teste para ver se carrega
camp = st.text_input("Campeonato")
if st.button("Testar Carregamento"):
    st.success("O sistema está rodando!")
