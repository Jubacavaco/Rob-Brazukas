import streamlit as st
import requests
import re

# Configuração da página
st.set_page_config(page_title="Sistema Brazukas", layout="wide")

# Título Estilizado
st.markdown("<h1 style='text-align: center; color: #2E86C1;'>🤖 Sistema Brazukas Top Tisp</h1>", unsafe_allow_html=True)
st.markdown("---")

# Sidebar
st.sidebar.header("⚙️ Configurações")
token = st.sidebar.text_input("Token Telegram", type="password")
chat_id = st.sidebar.text_input("ID Canal", type="password")

def calcular_probabilidade(texto):
    texto_limpo = re.sub(r'\d{2}\.\d{2}\.\d{2}', '', texto)
    numeros = re.findall(r'\b[0-9]\b', texto_limpo)
    gols = [int(n) for n in numeros]
    if len(gols) < 2: return 0
    media = sum(gols) / len(gols)
    return min(media * 65, 100)

def renderizar_bloco(titulo):
    with st.container(border=True):
        st.subheader(f"🏟️ {titulo}")
        
        # Inputs
        c1, c2 = st.columns(2)
        camp = c1.text_input(f"Campeonato", key=f"c_{titulo}")
        hora = c2.text_input(f"Horário", key=f"h_{titulo}")
        
        casa = st.text_input(f"Time Casa", key=f"ca_{titulo}")
        vis = st.text_input(f"Time Visitante", key=f"v_{titulo}")
        placar = st.text_input(f"Placar Final (Preencher após jogo)", key=f"p_{titulo}")
        lista = st.text_area(f"Lista de jogos", key=f"l_{titulo}", height=100)
        
        if st.button(f"Analisar {titulo}", key=f"an_{titulo}", use_container_width=True):
            p = calcular_probabilidade(lista)
            st.session_state[f"prob_{titulo}"] = p
            st.session_state[f"val_prob_{titulo}"] = round(p, 1)
            st.rerun()
        
        if f"prob_{titulo}" in st.session_state:
            p = st.session_state[f"prob_{titulo}"]
            st.markdown("---")
            st.write("📊 **Probabilidades:**")
            
            cols_g = st.columns(2)
            cols_g[0].write(f"Over 1.5: {min(p+5, 100):.0f}%"); cols_g[0].progress(min((p+5)/100, 1.0))
            cols_g[1].write(f"Over 2.5: {min(p, 100):.
