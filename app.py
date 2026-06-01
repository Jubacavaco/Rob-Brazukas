import streamlit as st
import requests
import re

st.set_page_config(page_title="Robô Brazukas Dual", layout="wide")
st.title("🤖 Painel Brazukas - Gestão Dual Completa")

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
    camp = st.text_input(f"Camp ({titulo})", key=f"c_{titulo}")
    casa = st.text_input(f"Casa ({titulo})", key=f"ca_{titulo}")
    vis = st.text_input(f"Vis ({titulo})", key=f"v_{titulo}")
    hora = st.text_input(f"Hora ({titulo})", key=f"h_{titulo}")
    lista = st.text_area(f"Lista ({titulo})", key=f"l_{titulo}")
    
    if st.button(f"Analisar {titulo}", key=f"an_{titulo}"):
        prob = calcular_probabilidade(lista)
        st.session_state[f"prob_{titulo}"] = prob
        st.write(f"📈 Probabilidade: {prob:.1f}%")
        st.progress(min(prob/100, 1.0))
        
        tipo = "LTD" if prob >= 51 else None
        if prob >= 55: tipo = "BTTS"
        if prob >= 70: tipo = "Over 1.5 FT"
        if prob >= 65: tipo = "Over 2.5 FT"
        
        if tipo:
            msg = f"🚨 *Alerta* 🚨\n\n🏆 {camp}\n🆚 {casa} x {vis}\n🎯 {tipo}\n⏰ {hora}"
            st.info(msg)
            st.session_state[f"msg_{titulo}"] = msg
        else:
            st.warning("Probabilidade baixa.")

    if f"msg_{titulo}" in st.session_state:
        if st.button(f"Enviar {titulo}", key=f"en_{titulo}"):
            p = {"chat_id": chat_id, "text": st.session_state[f"msg_{titulo}"], "parse_mode": "Markdown"}
            r = requests.post(f"https://api.telegram.org/bot{token}/sendMessage", data=p).json()
            if r.get("ok"): st.session_state[f"id_{titulo}"] = r["result"]["message_id"]

    if f"id_{titulo}" in st.session_state:
        st.write("---")
        c1, c2, c3 = st.columns(3)
        if c1.button("✅ GREEN", key=f"g_{titulo}"):
            d = {"chat_id": chat_id, "message_id": st.session_state[f"id_{titulo}"], "text": st.session_state[f"msg_{titulo}"] + "\n\n🔄 Status: ✅ GREEN!!", "parse_mode": "Markdown"}
            requests.post(f"https://api.telegram.org/bot{token}/editMessageText", data=d)
        if c2.button("❌ RED", key=f"r_{titulo}"):
            d = {"chat_id": chat_id, "message_id": st.session_state[f"id_{titulo}"], "text": st.session_state[f"msg_{titulo}"] + "\n\n🔄 Status: ❌ RED!", "parse_mode": "Markdown"}
            requests.post(f"https://api.telegram.org/bot{token}/editMessageText", data=d)
        if c3.button("🔄 DEV", key=f"d_{titulo}"):
            d = {"chat_id": chat_id, "message_id": st.session_state[f"id_{titulo}"], "text": st.session_state[f"msg_{titulo}"] + "\n\n🔄 Status: 🔄 DEVOLVIDA", "parse_mode": "Markdown"}
            requests.post(f"https://api.telegram.org/bot{token}/editMessageText", data=d)

c1, c2 = st.columns(2)
with c1: renderizar_bloco("JOGO_1")
with c2: renderizar_bloco("JOGO_2")
