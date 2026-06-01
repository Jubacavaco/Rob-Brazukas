import streamlit as st
import requests
import re

st.set_page_config(layout="wide")
st.title("🤖 Painel Brazukas - Gestão Total")

# Sidebar para credenciais
token = st.sidebar.text_input("Token Telegram", type="password")
chat_id = st.sidebar.text_input("ID Canal", type="password")

def calcular_probabilidade(texto):
    # Remove padrões de data (dd.mm.yy)
    texto_limpo = re.sub(r'\d{2}\.\d{2}\.\d{2}', '', texto)
    # Extrai apenas números de um dígito (0-9)
    numeros = re.findall(r'\b[0-9]\b', texto_limpo)
    gols = [int(n) for n in numeros]
    
    if len(gols) < 2: return 0
    
    media = sum(gols) / len(gols)
    # Multiplicador ajustado para 65 para elevar a %
    return min(media * 65, 100)

def renderizar_bloco(titulo):
    st.subheader(f"🏟️ {titulo}")
    
    # CAMPOS DE INPUT
    camp = st.text_input(f"Campeonato ({titulo})", key=f"c_{titulo}")
    casa = st.text_input(f"Casa ({titulo})", key=f"ca_{titulo}")
    vis = st.text_input(f"Visitante ({titulo})", key=f"v_{titulo}")
    hora = st.text_input(f"Horário ({titulo})", key=f"h_{titulo}")
    lista = st.text_area(f"Lista de jogos ({titulo})", key=f"l_{titulo}")
    
    # ANÁLISE
    if st.button(f"Analisar {titulo}", key=f"an_{titulo}"):
        st.session_state[f"prob_{titulo}"] = calcular_probabilidade(lista)
        st.rerun()
    
    # RESULTADOS
    if f"prob_{titulo}" in st.session_state:
        p = st.session_state[f"prob_{titulo}"]
        
        # GRÁFICOS VISUAIS
        st.write("📊 **Acompanhamento Visual:**")
        st.write(f"Over 1.5 FT ({min(p+5, 100):.1f}%)")
        st.progress(min((p+5)/100, 1.0))
        st.write(f"Over 2.5 FT ({min(p, 100):.1f}%)")
        st.progress(min(p/100, 1.0))
        
        # SELEÇÃO DE MERCADO
        mercado = st.selectbox(f"Definir Mercado ({titulo})", ["Automático", "Over 1.5 FT", "Over 2.5 FT", "
