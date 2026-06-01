import streamlit as st
import requests
import re

st.set_page_config(page_title="Robô Brazukas Dual", layout="wide")
st.title("🤖 Painel Brazukas - Gestão Dual (2 Jogos)")

# --- FUNÇÕES ---
def calcular_probabilidade(texto):
    numeros = re.findall(r'\d+', texto)
    gols = [int(n) for n in numeros if int(n) <= 10]
    if len(gols) < 2: return 0
    media = sum(gols) / len(gols)
    return min(media * 35, 100)

def decidir_tipo(prob):
    if prob >= 65: return "Over 2.5"
    elif prob >= 70: return "Over 1.5"
    elif prob >= 55: return "BTTS"
    elif prob >= 51: return "LTD"
    return None

def get_msg(tipo, camp, casa, vis, hora):
    return f"🚨 *Alerta de Entrada* 🚨\n\n🏆 {camp}\n🆚 {casa} x {vis}\n🎯 *Mercado:* {tipo}\n⏰ {hora}\n\n⚠️ Aposte com responsabilidade."

# --- INTERFACE DUAL ---
col1, col2 = st.columns(2)

def processar_jogo(coluna, label):
    with coluna:
        st.subheader(f"🏟️ Jogo {label}")
        camp = st.text_input(f"Campeonato {label}", key=f"camp_{label}")
        casa = st.text_input(f"Time Casa {label}", key=f"casa_{label}")
        vis = st.text_input(f"Time Vis {label}", key=f"vis_{label}")
        hora = st.text_input(f"Horário {label}", key=f"hora_{label}")
        lista = st.text_area(f"Lista de Jogos {label}", key=f"lista_{label}", height=100)
        
        if st.button(f"Analisar Jogo {label}", key=f"btn_{label}"):
            prob = calcular_probabilidade(lista)
            tipo = decidir_tipo(prob)
            if tipo:
                msg = get_msg(tipo, camp, casa, vis, hora)
                st.info(msg)
                st.session_state[f"msg_{label}"] = msg
            else:
                st.warning("Probabilidade insuficiente.")

processar_jogo(col1, "A")
processar_jogo(col2, "B")

# --- CONFIGURAÇÕES GERAIS ---
st.sidebar.header("⚙️ Configurações Telegram")
token = st.sidebar.text_input("Token", type="password")
chat_id = st.sidebar.text_input("ID Canal", type="password")

if st.sidebar.button("🚀 Enviar Sinais Confirmados"):
    for label in ["A", "B"]:
        if f"msg_{label}" in st.session_state:
            payload = {"chat_id": chat_id, "text": st.session_state[f"msg_{label}"], "parse_mode": "Markdown"}
            requests.post(f"https://api.telegram.org/bot{token}/sendMessage", data=payload)
    st.success("Sinais enviados para o Telegram!")
