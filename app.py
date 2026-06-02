import streamlit as st
import requests

st.set_page_config(layout="wide")
st.title("🤖 Sistema Brazukas")

# Token e Chat fixos para evitar erros de escopo
TOKEN = "8776214366:AAEQnGyhcEa6NQcYzyFAhtVDXKpQx5CoYT0"
CHAT_ID = "-1003925163611"

def telegram(msg, msg_id=None):
    url = f"https://api.telegram.org/bot{TOKEN}/"
    if msg_id:
        requests.post(url + "editMessageText", json={"chat_id": CHAT_ID, "message_id": msg_id, "text": msg})
    else:
        resp = requests.post(url + "sendMessage", json={"chat_id": CHAT_ID, "text": msg}).json()
        return resp.get("result", {}).get("message_id")

def jogo_normal(nome):
    st.subheader(f"🏟️ {nome}")
    # Inputs básicos
    casa = st.text_input("Casa", key=f"casa_{nome}")
    vis = st.text_input("Visitante", key=f"vis_{nome}")
    ht = st.text_input("HT", key=f"ht_{nome}")
    ft = st.text_input("FT", key=f"ft_{nome}")
    
    # Armazena tudo em um dicionário único no session_state
    if st.button("ANALISAR", key=f"ana_{nome}"):
        st.session_state[f"d_{nome}"] = {"casa": casa, "vis": vis, "ht": ht, "ft": ft}
        st.success("Dados salvos!")

    # Só mostra os botões se houver dados
    if f"d_{nome}" in st.session_state:
        d = st.session_state[f"d_{nome}"]
        msg_txt = f"🚨 Jogo: {d['casa']} x {d['vis']}\nHT: {d['ht']} | FT: {d['ft']}"
        
        if st.button("ENVIAR", key=f"env_{nome}"):
            mid = telegram(msg_txt)
            st.session_state[f"mid_{nome}"] = mid
            
        if f"mid_{nome}" in st.session_state:
            mid = st.session_state[f"mid_{nome}"]
            if st.button("✅ HT GREEN", key=f"htg_{nome}"): telegram(f"✅ HT GREEN: {d['ht']}", mid)
            if st.button("❌ RED", key=f"red_{nome}"): telegram(f"❌ RED: {d['ft']}", mid)

col1, col2, col3 = st.columns(3)
with col1: jogo_normal("JOGO_A")
with col2: jogo_normal("JOGO_B")
with col3: jogo_normal("JOGO_C")
