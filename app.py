import streamlit as st
import requests
import streamlit.components.v1 as components

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
    except Exception as e:
        st.error(f"Erro no Telegram: {e}")

def jogo_normal(nome):
    st.subheader(f"🏟️ {nome}")
    with st.expander("Configurar"):
        camp = st.text_input("Campeonato", key=f"camp_{nome}")
        casa = st.text_input("Casa", key=f"casa_{nome}")
        vis = st.text_input("Visitante", key=f"vis_{nome}")
        mercado = st.selectbox("Mercado", ["Match Odds", "Gols"], key=f"merc_{nome}")
        horario = st.text_input("Horário", key=f"hor_{nome}")
        prob = st.number_input("Probabilidade (%)", 0, 100, 70, key=f"prob_{nome}")
        ht = st.text_input("HT", key=f"ht_{nome}")
        ft = st.text_input("FT", key=f"ft_{nome}")
        st.text_area("Lista de Análise", key=f"lista_{nome}")

    if st.button("🚀 ENVIAR ALERTA", key=f"env_{nome}"):
        msg = f"🚨 Alerta de Cantos 🚨\n\n🏆 Campeonato: {camp}\n🆚 Jogo: {casa} x {vis}\n🎯 Mercado: {mercado}\n💥 Prognóstico: {mercado}\n📈 Probabilidade: {prob}%\n⏰ Horário: {horario} (BR)\n\n🔞Aposte com responsabilidade.\n⚠️ Não há garantias de lucro."
        st.session_state[f"mid_{nome}"] = telegram(msg)
        st.success("Enviado!")

    mid = st.session_state.get(f"mid_{nome}")
    if mid:
        base = f"🚨 Alerta de Cantos 🚨\n\n🏆 Campeonato: {st.session_state.get(f'camp_{nome}')}\n🆚 Jogo: {st.session_state.get(f'casa_{nome}')} x {st.session_state.get(f'vis_{nome}')}"
        
        c1, c2 = st.columns(2)
        if c1.button("⏱️ MOMENTO", key=f"mom_{nome}"):
            telegram(f"{base}\n\n⚪ Em Andamento | HT: {ht} | FT: {ft}", mid)
        if c1.button("✅ HT GREEN", key=f"htg_{nome}"):
            telegram(f"{base}\n\n✅ HT GREEN: {ht}", mid)
        if c2.button("🏆 FINAL GREEN", key=f"fng_{nome}"):
            telegram(f"{base}\n\nHT: {ht}\n🏆 FINAL GREEN: {ft}", mid)
        if c2.button("❌ RED", key=f"red_{nome}"):
            telegram(f"{base}\n\nHT: {ht}\n❌ RED: {ft}", mid)

# Layout
c1, c2, c3, c4 = st.columns(4)
with c1: jogo_normal("JOGO_A")
with c2: jogo_normal("JOGO_B")
with c3: jogo_normal("JOGO_C")
with c4: st.write("JOGO D em manutenção")
