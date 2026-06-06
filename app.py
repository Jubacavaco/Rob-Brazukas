import streamlit as st
import requests

st.set_page_config(layout="wide", page_title="Sistema Brazukas")
st.title("🤖 Sistema Brazukas Top Tips")

TOKEN = "8776214366:AAEQnGyhcEa6NQcYzyFAhtVDXKpQx5CoYT0"
CHAT_ID = "-1002539693401"
RODAPE = "\n\n⚠️ Não há garantias de lucro."

def telegram(msg, msg_id=None):
    url = f"https://api.telegram.org/bot{TOKEN}/"
    try:
        if msg_id:
            resp = requests.post(url + "editMessageText", json={"chat_id": CHAT_ID, "message_id": msg_id, "text": msg + RODAPE})
        else:
            resp = requests.post(url + "sendMessage", json={"chat_id": CHAT_ID, "text": msg + RODAPE})
        data = resp.json()
        if data.get("ok"): return data.get("result", {}).get("message_id")
        else:
            st.error(f"Erro Telegram: {data.get('description')}")
            return None
    except Exception as e:
        st.error(f"Erro: {e}")
        return None

def jogo_escanteios():
    st.subheader("🏟️ Nome de Escanteios")
    
    # CAMPOS QUE VOCÊ PEDIU DE VOLTA
    col1, col2 = st.columns(2)
    with col1:
        camp = st.text_input("Campeonato")
        casa = st.text_input("Casa")
        vis = st.text_input("Visitante")
        prob = st.number_input("Prognóstico (%)", 0, 100, 70)
    with col2:
        horario = st.text_input("Horário")
        e_casa = st.number_input("Cantos Casa", step=1)
        e_vis = st.number_input("Cantos Visitante", step=1)
        linha = st.selectbox("Linha", [7.5, 8.5, 9.5, 10.5])

    ht = st.text_input("Placar HT")
    ft = st.text_input("Placar FT")
    
    if st.button("🚀 ENVIAR ALERTA"):
        msg = f"🚨 Alerta Escanteio\n\n🏆 {camp}\n🆚 {casa} x {vis}\n⏰ {horario}\n📈 Prob: {prob}%\n📊 Cantos: {e_casa}x{e_vis}\n🎯 Linha: {linha}"
        st.session_state["mid"] = telegram(msg)
    
    mid = st.session_state.get("mid")
    if mid:
        base = f"🚨 Alerta Escanteio\n\n🏆 {camp}\n🆚 {casa} x {vis}\n⏰ {horario}\n📈 Prob: {prob}%\n📊 Cantos: {e_casa}x{e_vis}\n🎯 Linha: {linha}"
        c1, c2 = st.columns(2)
        if c1.button("⚪ MOMENTO"): telegram(f"{base}\n\nPlacar HT: {ht}\n⚪ Em Andamento", mid)
        if c1.button("✅ HT"): telegram(f"{base}\n\nPlacar HT: {ht}\n✅ GREEN HT", mid)
        if c2.button("🏆 FINAL"): telegram(f"{base}\n\nPlacar HT: {ht}\nPlacar FT: {ft}\n🏆 GREEN FINAL", mid)
        if c2.button("❌ RED"): telegram(f"{base}\n\nPlacar HT: {ht}\nPlacar FT: {ft}\n❌ RED", mid)

jogo_escanteios()
