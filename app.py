import streamlit as st
import requests
import re
import json
import os

st.set_page_config(page_title="Sistema Brazukas", layout="wide")

# CSS para um visual moderno
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    .stButton>button { border-radius: 10px; font-weight: 600; }
    </style>
    """, unsafe_allow_html=True)

DB_FILE = "dados_brazukas.json"

def carregar_db():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f: return json.load(f)
        except: return {}
    return {}

def salvar_db(data):
    with open(DB_FILE, "w") as f: json.dump(data, f)

if "db" not in st.session_state: st.session_state.db = carregar_db()

st.markdown("<h1 style='text-align: center;'>🤖 Sistema Brazukas Top Tips</h1>", unsafe_allow_html=True)
st.write("---")

with st.sidebar:
    st.header("⚙️ Configurações")
    token = st.text_input("Token Telegram", type="password")
    chat_id = st.text_input("ID Canal", type="password")

def calcular_probabilidade(texto):
    texto_limpo = re.sub(r'\d{2}\.\d{2}\.\d{2}', '', texto)
    numeros = re.findall(r'\b[0-9]\b', texto_limpo)
    gols = [int(n) for n in numeros]
    if len(gols) < 2: return 0
    media = sum(gols) / len(gols)
    return min(media * 65, 100)

def renderizar_bloco(titulo):
    with st.container():
        st.subheader(f"🏟️ {titulo}")
        
        if titulo not in st.session_state.db: st.session_state.db[titulo] = {}
        d = st.session_state.db[titulo]
        
        c1, c2 = st.columns(2)
        camp = c1.text_input("Campeonato", value=d.get("camp", ""), key=f"c_{titulo}")
        hora = c2.text_input("Horário", value=d.get("hora", ""), key=f"h_{titulo}")
        
        col_c, col_v, col_p = st.columns(3)
        casa = col_c.text_input("Casa", value=d.get("casa", ""), key=f"ca_{titulo}")
        vis = col_v.text_input("Visitante", value=d.get("vis", ""), key=f"v_{titulo}")
        placar = col_p.text_input("Placar", value=d.get("placar", ""), key=f"p_{titulo}")
        
        lista = st.text_area("Lista de jogos", value=d.get("lista", ""), key=f"l_{titulo}", height=80)
        
        if st.button(f"Analisar {titulo}", key=f"an_{titulo}", use_container_width=True):
            p = calcular_probabilidade(lista)
            st.session_state.db[titulo].update({
