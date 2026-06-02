import streamlit as st
import requests

st.set_page_config(layout="wide", page_title="Sistema Brazukas")
st.title("🤖 Sistema Brazukas Pro")

TOKEN = "8776214366:AAEQnGyhcEa6NQcYzyFAhtVDXKpQx5CoYT0"
CHAT_ID = "-1003925163611"

def telegram(msg, msg_id=None):
    url = f"https://api.telegram.org/bot{TOKEN}/"
    try:
        if msg_id:
            requests.post(url + "editMessageText", json={"chat_id": CHAT_ID, "message_id": msg_id, "text": msg})
        else:
            resp = requests.post(url + "sendMessage", json={"chat_id": CHAT_ID, "text": msg}).json()
            return resp.get("result", {}).get("message_id")
    except: return None

def calcular_probs(lista):
    n = len(lista)
    return {"O 1.5": 50+n, "O 2.5": 40+n, "BTTS": 30+n, "LTD": 20+n}

def jogo_normal(nome):
    st.subheader(f"🏟️ {nome}")
    camp = st.text_input("Campeonato", key=f"camp_{nome}")
    casa = st.text_input("Casa", key=f"casa_{nome}")
    vis = st.text_input("Visitante", key=f"vis_{nome}")
    lista = st.text_area("Lista de Análise", key=f"lista_{nome}")
    
    if st.button("📊 ANALISAR", key=f"ana_{nome}"):
        st.session_state[f"analise_{nome}"] = True
        st.session_state[f"probs_{nome}"] = calcular_probs(lista)

    # AQUI ESTÁ A CORREÇÃO: usamos .get() para não dar erro se a chave não existir ainda
    if st.session_state.get(f"analise_{nome}", False):
        p = st.session_state.get(f"probs_{nome}", {"O 1.5": 0, "O 2.5": 0, "BTTS": 0, "LTD": 0})
        st.bar_chart(p)
        st.write(f"✅ O 1.5: {p['O 1.5']}% | 🔥 LTD: {p['LTD']}%")
        
        ht = st.text_input("Placar HT", key=f"ht_{nome}")
        ft = st.text_input("Placar FT", key=f"ft_{nome}")
        
        if st.button("🚀 ENVIAR ALERTA", key=f"env_{nome}"):
            msg = f"🚨 Alerta 🚨\n\n🏆 {camp}\n🆚 {casa} x {vis}\n📈 Prob: {p['O 1.5']}%"
            st.session_state[f"mid_{nome}"] = telegram(msg)

        mid = st.session_state.get(f"mid_{nome}")
        if mid:
            c1, c2 = st.columns(2)
            if c1.button("⏱️ MOMENTO", key=f"mom_{nome}"): telegram(f"🏆 {casa} x {vis}\nHT: ({ht})\n\n⚪ Em Andamento", mid)
            if c1.button("✅ HT", key=f"htg_{nome}"): telegram(f"🏆 {casa} x {vis}\nHT: ({ht})\n✅✅✅", mid)
            if c2.button("🏆 FINAL", key=f"fng_{nome}"): telegram(f"🏆 {casa} x {vis}\nHT: ({ht})\nFT: ({ft})\n🏆🏆🏆", mid)
            if c2.button("❌ RED", key=f"red_{nome}"): telegram(f"🏆 {casa} x {vis}\nHT: ({ht})\nFT: ({ft})\n❌❌❌", mid)

# Layout com 4 colunas (A, B, C, D)
col1, col2, col3, col4 = st.columns(4)
with col1: jogo_normal("JOGO_A")
with col2: jogo_normal("JOGO_B")
with col3: jogo_normal("JOGO_C")
with col4: jogo_normal("JOGO_D")
