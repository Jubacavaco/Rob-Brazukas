import streamlit as st
import requests
import pandas as pd

st.set_page_config(layout="wide", page_title="Sistema Brazukas")
st.title("🤖 Sistema Brazukas Pro")

TOKEN = "8776214366:AAEQnGyhcEa6NQcYzyFAhtVDXKpQx5CoYT0"
CHAT_ID = "-1003925163611"
RODAPE = "\n\n🔞Aposte com responsabilidade.\n⚠️ Não há garantias de lucro."

def telegram(msg, msg_id=None):
    url = f"https://api.telegram.org/bot{TOKEN}/"
    texto_final = msg + RODAPE
    try:
        if msg_id:
            requests.post(url + "editMessageText", json={"chat_id": CHAT_ID, "message_id": msg_id, "text": texto_final})
        else:
            resp = requests.post(url + "sendMessage", json={"chat_id": CHAT_ID, "text": texto_final}).json()
            return resp.get("result", {}).get("message_id")
    except: return None

def jogo_normal(nome):
    st.subheader(f"🏟️ {nome}")
    camp = st.text_input("Campeonato", key=f"camp_{nome}")
    casa = st.text_input("Casa", key=f"casa_{nome}")
    vis = st.text_input("Visitante", key=f"vis_{nome}")
    mercado = st.selectbox("Mercado", ["Match Odds", "Gols"], key=f"merc_{nome}")
    progs_opcoes = ["Over 1.5 FT", "Over 2.5 FT", "BTTS", "LTD", "Casa Vence", "Visitante Vence"]
    prognostico = st.multiselect("Prognóstico", progs_opcoes, key=f"prog_{nome}")
    prog_str = ", ".join(prognostico)
    horario = st.text_input("Horário", key=f"hor_{nome}")
    prob = st.number_input("Probabilidade (%)", 0, 100, 70, key=f"prob_{nome}")
    ht = st.text_input("Placar HT", key=f"ht_{nome}")
    ft = st.text_input("Placar FT", key=f"ft_{nome}")
    st.text_area("Lista de Análise", key=f"lista_{nome}")
    
    if st.button("📊 ANALISAR", key=f"ana_{nome}"):
        st.session_state[f"analise_{nome}"] = True

    if st.session_state.get(f"analise_{nome}", False):
        st.write("### 📊 Resumo Final")
        dados = pd.DataFrame({'%': [85, 60, 75, 40]}, index=["O 1.5", "O 2.5", "BTTS", "LTD"])
        st.bar_chart(dados, height=200)
        
        c1, c2 = st.columns(2)
        with c1:
            st.write("### 🎯 Mercados Mais Fortes")
            st.write("✅ Over 1.5 FT — Muito Forte\n🔥 LTD — Forte")
        with c2:
            st.write("### 📌 Placares Sugeridos")
            st.write("• 1x0 | 1x1 | 2x1")
            st.success("🎯 Aposta Recomendada: Over 1.5 FT")

        if st.button("🚀 ENVIAR ALERTA", key=f"env_{nome}"):
            msg = f"🚨 Alerta de Cantos 🚨\n\n🏆 Campeonato: {camp}\n🆚 Jogo: {casa} x {vis}\n🎯 Mercado: {mercado}\n💥 Prognóstico: {prog_str}\n📈 Probabilidade: {prob}%\n⏰ Horário: {horario} (BR)"
            st.session_state[f"mid_{nome}"] = telegram(msg)

        mid = st.session_state.get(f"mid_{nome}")
        if mid:
            base = f"🚨 Alerta de Cantos 🚨\n\n🏆 Campeonato: {camp}\n🆚 Jogo: {casa} x {vis}\n🎯 Mercado: {mercado}\n💥 Prognóstico: {prog_str}\n📈 Probabilidade: {prob}%\n⏰ Horário: {horario} (BR)"
            b1, b2 = st.columns(2)
            if b1.button("⏱️ MOMENTO", key=f"mom_{nome}"): 
                telegram(f"{base}\n\nPlacar: {ht}\n\n⚪ Em Andamento", mid)
            if b1.button("✅ HT", key=f"htg_{nome}"): 
                telegram(f"{base}\n\nPlacar: {ht}\n\n✅✅✅ GREEN ✅✅✅", mid)
            if b2.button("🏆 FINAL", key=f"fng_{nome}"): 
                telegram(f"{base}\n\nPlacar HT: {ht}\nPlacar FT: {ft}\n\n🏆🏆🏆 GREEN FINAL 🏆🏆🏆", mid)
            if b2.button("❌ RED", key=f"red_{nome}"): 
                telegram(f"{base}\n\nPlacar: {ft}\n\n❌❌❌ RED ❌❌❌", mid)

def jogo_c_escanteios():
    st.subheader("🏟️ JOGO_C (Escanteios)")
    linha = st.selectbox("Linha", [7.5, 8.5, 9.5, 10.5], key="linha_c")
    if st.button("🚀 ENVIAR ESCANTEIO", key="c_env"): 
        st.session_state["mid_c"] = telegram(f"🚨 Alerta de Escanteios 🚨\n\n🎯 Linha: {linha}")
    mid = st.session_state.get("mid_c")
    if mid:
        if st.button("⚪ MOMENTO", key="c_mom"): 
            telegram(f"🚨 Alerta de Escanteios 🚨\n\n🎯 Linha: {linha}\n\n⚪ Em Andamento", mid)
        if st.button("✅ GREEN", key="c_gr"): 
            telegram(f"🚨 Alerta de Escanteios 🚨\n\n🎯 Linha: {linha}\n\n✅✅✅ GREEN ✅✅✅", mid)
        if st.button("❌ RED", key=f"c_red"): 
            telegram(f"🚨 Alerta de Escanteios 🚨\n\n🎯 Linha: {linha}\n\n❌❌❌ RED ❌❌❌", mid)

col1, col2, col3 = st.columns(3)
with col1: jogo_normal("JOGO_A")
with col2: jogo_normal("JOGO_B")
with col3: jogo_c_escanteios()
