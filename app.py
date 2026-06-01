import streamlit as st
import requests
import re

st.set_page_config(layout="wide")
st.title("🤖 Painel Brazukas - Gestão com Gráficos")

# --- SIDEBAR ---
token = st.sidebar.text_input("Token Telegram", type="password")
chat_id = st.sidebar.text_input("ID Canal", type="password")

# --- FUNÇÕES ---
def calcular_probabilidade(texto):
    numeros = re.findall(r'\d+', texto)
    gols = [int(n) for n in numeros if int(n) <= 10]
    if len(gols) < 2: return 0
    media = sum(gols) / len(gols)
    return min(media * 35, 100)

def renderizar_bloco(titulo):
    st.write(f"--- 🏟️ {titulo} ---")
    camp = st.text_input(f"Campeonato {titulo}")
    lista = st.text_area(f"Lista de jogos {titulo}")
    
    if st.button(f"Analisar {titulo}"):
        p = calcular_probabilidade(lista)
        st.session_state[f"p_{titulo}"] = p
        st.write(f"Probabilidade: {p:.1f}%")
        st.progress(min(p/100, 1.0))
        
        # Lógica de seleção
        tipo = "LTD" if p >= 51 else None
        if p >= 55: tipo = "BTTS"
        if p >= 70: tipo = "Over 1.5 FT"
        if p >= 65: tipo = "Over 2.5 FT"
        
        if tipo:
            msg = f"🚨 *Alerta* 🚨\n🏆 {camp}\n🎯 {tipo}\n✅ Prob: {p:.1f}%"
            st.info(msg)
            st.session_state[f"msg_{titulo}"] = msg
            
    if f"msg_{titulo}" in st.session_state:
        if st.button(f"Enviar {titulo}"):
            payload = {"chat_id": chat_id, "text": st.session_state[f"msg_{titulo}"], "parse_mode": "Markdown"}
            r = requests.post(f"https://api.telegram.org/bot{token}/sendMessage", data=payload).json()
            if r.get("ok"): 
                st.session_state[f"id_{titulo}"] = r["result"]["message_id"]

    if f"id_{titulo}" in st.session_state:
        if st.button(f"GREEN {titulo}"): st.write("Registrado Green")
        if st.button(f"RED {titulo}"): st.write("Registrado Red")

# --- LAYOUT ---
col1, col2 = st.columns(2)
with col1: renderizar_bloco("A")
with col2: renderizar_bloco("B")
