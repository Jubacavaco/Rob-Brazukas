import streamlit as st
import requests
import pandas as pd

st.set_page_config(layout="wide", page_title="Sistema Brazukas")
st.title("🤖 Sistema Brazukas Top Tips")

TOKEN = "8776214366:AAEQnGyhcEa6NQcYzyFAhtVDXKpQx5CoYT0"
CHAT_ID = "-1002539693401"
RODAPE = "\n\n🔞Aposte com responsabilidade.\n⚠️ Não há garantias de lucro."

def telegram(msg, msg_id=None):
    url = f"https://api.telegram.org/bot{TOKEN}/"
    texto_final = msg + RODAPE
    try:
        if msg_id:
            resp = requests.post(url + "editMessageText", json={"chat_id": CHAT_ID, "message_id": msg_id, "text": texto_final})
        else:
            resp = requests.post(url + "sendMessage", json={"chat_id": CHAT_ID, "text": texto_final})
        
        if resp.status_code == 200:
            return resp.json().get("result", {}).get("message_id")
        else:
            st.error(f"Erro no Telegram: {resp.status_code}")
            return None
    except Exception as e:
        st.error(f"Erro de conexão: {e}")
        return None

def jogo_c_escanteios():
    st.subheader("🏟️ Nome de Escanteios")
    camp_c = st.text_input("Campeonato", key="camp_c")
    casa_c = st.text_input("Casa", key="casa_c")
    vis_c = st.text_input("Visitante", key="vis_c")
    horario_c = st.text_input("Horário", key="hor_c")
    e_casa_c = st.number_input("Cantos Casa", step=1, key="e_casa_c")
    e_vis_c = st.number_input("Cantos Visitante", step=1, key="e_vis_c")
    ht_c = st.text_input("Placar HT", key="ht_c")
    ft_c = st.text_input("Placar FT", key="ft_c")
    
    if st.button("📊 ANALISAR JOGO C", key="ana_c"): 
        st.session_state["analise_c"] = True
    
    if st.session_state.get("analise_c", False):
        st.write("### 📊 Probabilidade Escanteios")
        linha = st.selectbox("Linha Escolhida", [7.5, 8.5, 9.5, 10.5], key="linha_c")
        
        if st.button("🚀 ENVIAR ALERTA ESCANTEIO", key="env_c"):
            msg = f"🚨 Alerta Escanteio 🚨\n\n🏆 {camp_c}\n⏰ {horario_c}\n\n📊 Cantos Casa: {e_casa_c}\n📊 Cantos Visitante: {e_vis_c}\n📈 Total: {e_casa_c + e_vis_c}\n🎯 Linha: {linha}"
            st.session_state["mid_c"] = telegram(msg)
        
        mid = st.session_state.get("mid_c")
        if mid:
            base = f"🚨 Alerta Escanteio 🚨\n\n🏆 {camp_c}\n⏰ {horario_c}\n\n📊 Escanteios Casa: {e_casa_c}\n📊 Escanteios Vis: {e_vis_c}\n📈 Total: {e_casa_c + e_vis_c}\n🎯 Linha: {linha}"
            c1, c2 = st.columns(2)
            if c1.button("⚪ MOMENTO", key="c_mom"): telegram(f"{base}\n\nPlacar HT: {ht_c}\n⚪ Em Andamento", mid)
            if c1.button("✅ HT", key="c_ht"): telegram(f"{base}\n\nPlacar HT: {ht_c}\n✅✅✅ GREEN ✅✅✅", mid)
            if c2.button("🏆 FINAL", key="c_fin"): telegram(f"{base}\n\nPlacar HT: {ht_c}\nPlacar FT: {ft_c}\n🏆🏆🏆 GREEN FINAL 🏆🏆🏆", mid)
            if c2.button("❌ RED", key="c_red"): telegram(f"{base}\n\nPlacar HT: {ht_c}\nPlacar FT: {ft_c}\n❌❌❌ RED ❌❌❌", mid)

jogo_c_escanteios()
