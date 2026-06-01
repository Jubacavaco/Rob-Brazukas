import streamlit as st
import requests
import re

st.set_page_config(layout="wide")
st.title("🤖 Painel Brazukas - Gestão Total")

# Sidebar
token = st.sidebar.text_input("Token Telegram", type="password")
chat_id = st.sidebar.text_input("ID Canal", type="password")

def calcular_probabilidade(texto):
    numeros = re.findall(r'\d+', texto)
    gols = [int(n) for n in numeros if int(n) <= 10]
    if len(gols) < 2: return 0
    media = sum(gols) / len(gols)
    return min(media * 35, 100)

def renderizar_bloco(titulo):
    st.subheader(f"🏟️ {titulo}")
    
    # CAMPOS DE INPUT
    camp = st.text_input(f"Campeonato ({titulo})", key=f"c_{titulo}")
    casa = st.text_input(f"Casa ({titulo})", key=f"ca_{titulo}")
    vis = st.text_input(f"Visitante ({titulo})", key=f"v_{titulo}")
    hora = st.text_input(f"Horário ({titulo})", key=f"h_{titulo}")
    escanteios = st.text_input(f"Escanteios ({titulo})", key=f"esc_{titulo}")
    lista = st.text_area(f"Lista de jogos ({titulo})", key=f"l_{titulo}")
    
    # ANÁLISE
    if st.button(f"Analisar {titulo}", key=f"an_{titulo}"):
        st.session_state[f"prob_{titulo}"] = calcular_probabilidade(lista)
        st.rerun()
    
    # RESULTADOS
    if f"prob_{titulo}" in st.session_state:
        p = st.session_state[f"prob_{titulo}"]
        
        # GRÁFICOS
        st.write("📊 **Acompanhamento Visual:**")
        st.write(f"Over 1.5 FT ({min(p+5, 100)}%)"); st.progress(min((p+5)/100, 1.0))
        st.write(f"Over 2.5 FT ({min(p, 100)}%)"); st.progress(min(p/100, 1.0))
        st.write(f"Ambas Marcam ({max(0, p-10)}%)"); st.progress(max(0, p-10)/100)
        st.write(f"LTD ({max(0, p-15)}%)"); st.progress(max
