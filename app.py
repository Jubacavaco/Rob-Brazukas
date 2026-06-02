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

def jogo_normal(nome):
    st.subheader(f"🏟️ {nome}")
    camp = st.text_input("Campeonato", key=f"camp_{nome}")
    casa = st.text_input("Casa", key=f"casa_{nome}")
    vis = st.text_input("Visitante", key=f"vis_{nome}")
    mercado = st.selectbox("Mercado", ["Match Odds", "Gols"], key=f"merc_{nome}")
    horario = st.text_input("Horário", key=f"hor_{nome}")
    prob = st.number_input("Probabilidade (%)", 0, 100, 70, key=f"prob_{nome}")
    ht = st.text_input("Placar HT (ex: 0x0)", key=f"ht_{nome}")
    ft = st.text_input("Placar FT (ex: 1x2)", key=f"ft_{nome}")
    st.text_area("Lista de Análise", key=f"lista_{nome}")
    
    if st.button("📊 ANALISAR", key=f"ana_{nome}"):
        st.session_state[f"analise_{nome}"] = True

    if st.session_state.get(f"analise_{nome}"):
        st.bar_chart({"O 1.5": 80, "O 2.5": 60, "BTTS": 70, "LTD": 40, "CASA": 65, "VIS": 20})

        if st.button("🚀 ENVIAR ALERTA", key=f"env_{nome}"):
            msg = f"🚨 Alerta de Cantos 🚨\n\n🏆 Campeonato: {camp}\n🆚 Jogo: {casa} x {vis}\n🎯 Mercado: {mercado}\n💥 Prognóstico: {mercado}\n📈 Probabilidade: {prob}%\n⏰ Horário: {horario} (BR)\n\n🔞Aposte com responsabilidade.\n⚠️ Não há garantias de lucro."
            st.session_state[f"mid_{nome}"] = telegram(msg)

        mid = st.session_state.get(f"mid_{nome}")
        if mid:
            base = f"🚨 Alerta de Cantos 🚨\n\n🏆 Campeonato: {camp}\n🆚 Jogo: {casa} x {vis}\n🎯 Mercado: {mercado}\n💥 Prognóstico: {mercado}\n📈 Probabilidade: {prob}%\n⏰ Horário: {horario} (BR)"
            c1, c2 = st.columns(2)
            if c1.button("⏱️ MOMENTO", key=f"mom_{nome}"):
                telegram(f"{base}\nHT: ({ht})\n\n⚪ Em Andamento", mid)
            if c1.button("✅ HT", key=f"htg_{nome}"):
                telegram(f"{base}\nHT: ({ht})\n✅✅✅", mid)
            if c2.button("🏆 FINAL", key=f"fng_{nome}"):
                telegram(f"{base}\nHT: ({ht})\nFT: ({ft})\n🏆🏆🏆", mid)
            if c2.button("❌ RED", key=f"red_{nome}"):
                telegram(f"{base}\nHT: ({ht})\nFT: ({ft})\n❌❌❌", mid)

def jogo_d():
    st.subheader("🏟️ JOGO_D (Escanteios)")
    linha = st.selectbox("Linha", [7.5, 8.5, 9.5, 10.5], key="linha_d")
    if st.button("🚀 ENVIAR ALERTA", key="d_env"): 
        st.session_state["mid_d"] = telegram(f"🚨 Alerta de Escanteios 🚨\n\n🏟️ JOGO D\n🎯 Linha: {linha}")
    
    mid = st.session_state.get("mid_d")
    if mid:
        c1, c2 = st.columns(2)
        if c1.button("⏱️ MOMENTO", key="d_mom"): telegram(f"🚨 Alerta de Escanteios 🚨\n\n🏟️ JOGO D\n🎯 Linha: {linha}\n⚪ Em Andamento", mid)
        if c1.button("✅ HT", key="d_htg"): telegram(f"🚨 Alerta de Escanteios 🚨\n\n🏟️ JOGO D\n🎯 Linha: {linha}\n✅✅✅", mid)
        if c2.button("🏆 FINAL", key="d_fng"): telegram(f"🚨 Alerta de Escanteios 🚨\n\n🏟️ JOGO D\n🎯 Linha: {linha}\n🏆🏆🏆", mid)
        if c2.button("❌ RED", key="d_fnr"): telegram(f"🚨 Alerta de Escanteios 🚨\n\n🏟️ JOGO D\n🎯 Linha: {linha}\n❌❌❌", mid)

# Layout das 4 colunas restaurado
c1, c2, c3, c4 = st.columns(4)
with c1: jogo_normal("JOGO_A")
with c2: jogo_normal("JOGO_B")
with c3: jogo_normal("JOGO_C")
with c4: jogo_d()
