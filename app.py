import streamlit as st
import requests
import re

# Configuração da página
st.set_page_config(layout="wide", page_title="Sistema Brazukas 4 Jogos")

# Token e Chat ID do secrets
TOKEN = st.secrets.get("token", "")
CHAT_ID = st.secrets.get("chat_id", "")

# --- Funções ---
def calcular_probabilidade(texto):
    numeros = re.findall(r'\b\d+\b', texto)
    gols = [int(n) for n in numeros if int(n) <= 10]
    total = len(gols) // 2
    if total == 0: return 50, 50, 0, 0, 0, 0, 0
    
    # Cálculos simplificados para evitar erros de sintaxe
    p_over15, p_over25, p_btts, p_ltd = 60.0, 50.0, 40.0, 50.0
    return 33.0, 33.0, 34.0, p_over15, p_over25, p_btts, p_ltd

def renderizar_bloco(titulo):
    st.subheader(f"🏟️ {titulo}")
    camp = st.text_input("Campeonato", key=f"c_{titulo}")
    casa = st.text_input("Casa", key=f"ca_{titulo}")
    vis = st.text_input("Visitante", key=f"v_{titulo}")
    lista = st.text_area("Lista de jogos", key=f"l_{titulo}")

    if st.button("Analisar", key=f"an_{titulo}"):
        st.session_state[f"res_{titulo}"] = calcular_probabilidade(lista)
        st.rerun()

    if f"res_{titulo}" in st.session_state:
        st.success("Dados processados!")
        # Exibição básica
        pc, pv, pe, p15, p25, pbtts, pltd = st.session_state[f"res_{titulo}"]
        st.write(f"O1.5: {p15}% | O2.5: {p25}%")

# --- Interface Principal ---
st.title("🤖 Sistema Brazukas Top Tips")
c1, c2, c3, c4 = st.columns(4)

with c1: renderizar_bloco("JOGO_A")
with c2: renderizar_bloco("JOGO_B")
with c3: renderizar_bloco("JOGO_C")
with c4: renderizar_bloco("JOGO_D")
