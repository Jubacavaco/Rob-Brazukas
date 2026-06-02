import streamlit as st
import requests

st.set_page_config(layout="wide")
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
    ht = st.text_input("HT", key=f"ht_{nome}")
    ft = st.text_input("FT", key=f"ft_{nome}")
    st.text_area("Lista de Análise", key=f"lista_{nome}")
    
    if st.button("📊 ANALISAR", key=f"ana_{nome}"):
        st.session_state[f"analise_{nome}"] = True
        st.success("Análise registrada!")

    if st.session_state.get(f"analise_{nome}"):
        dados_grafico = {"O 1.5": 80, "O 2.5": 60, "BTTS": 70, "LTD": 40, "CASA": 65, "VIS": 20}
        st.bar_chart(dados_grafico)

        if st.button("🚀 ENVIAR ALERTA", key=f"env_{nome}"):
            msg = f"🚨 Alerta de Cantos 🚨\n\n🏆 Campeonato: {camp}\n🆚 Jogo: {casa} x {vis}\n🎯 Mercado: {mercado}\n💥 Prognóstico: {mercado}\n📈 Probabilidade: {prob}%\n⏰ Horário: {horario} (BR)\n\n🔞Aposte com responsabilidade.\n⚠️ Não há garantias de lucro."
            st.session_state[f"mid_{nome}"] = telegram(msg)

        mid = st.session_state.get(f"mid_{nome}")
        if mid:
            base = f"🚨 Alerta de Cantos 🚨\n\n🏆 Campeonato: {camp}\n🆚 Jogo: {casa} x {vis}\n🎯 Mercado: {mercado}\n💥 Prognóstico: {mercado}\n📈 Probabilidade: {prob}%\n⏰ Horário: {horario} (BR)"
            
            c1, c2 = st.columns(2)
            if c1.button("⏱️ MOMENTO", key=f"mom_{nome}"):
                telegram(f"{base}\nHT: {ht}\n\n⚪ Em Andamento", mid)
            if c1.button("✅ HT GREEN", key=f"htg_{nome}"):
                telegram(f"{base}\nHT: {ht}\n✅ HT GREEN", mid)
            if c2.button("🏆 FINAL GREEN", key=f"fng_{nome}"):
                telegram(f"{base}\nHT: {ht}\nFT: {ft}\n🏆 FINAL GREEN", mid)
            if c2.button("❌ RED", key=f"red_{nome}"):
                telegram(f"{base}\nHT: {ht}\nFT: {ft}\n❌ RED", mid)

# Função Jogo D omitida por brevidade, mas segue o mesmo padrão.
