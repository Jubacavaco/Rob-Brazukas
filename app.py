import streamlit as st
import requests
import streamlit.components.v1 as components

st.set_page_config(layout="wide", page_title="Sistema Brazukas")
st.title("🤖 Sistema Brazukas Top Tips")

TOKEN = "8776214366:AAEQnGyhcEa6NQcYzyFAhtVDXKpQx5CoYT0"
CHAT_ID = "-1003925163611"

# Função para enviar ou editar a mensagem no Telegram mantendo o estilo
def enviar_ou_editar(nome, msg):
    url_base = f"https://api.telegram.org/bot{TOKEN}"
    payload = {"chat_id": CHAT_ID, "text": msg}
    
    if f"msg_id_{nome}" in st.session_state:
        payload["message_id"] = st.session_state[f"msg_id_{nome}"]
        requests.post(f"{url_base}/editMessageText", json=payload)
    else:
        resp = requests.post(f"{url_base}/sendMessage", json=payload).json()
        if resp.get("ok"):
            st.session_state[f"msg_id_{nome}"] = resp["result"]["message_id"]

def calcular_probabilidades(lista):
    return {"BTTS": 61, "O1.5": 78, "O2.5": 52, "LTD": 70, "Casa": 65, "Vis": 15}

def jogo_normal(nome):
    st.subheader(f"🏟️ {nome}")
    with st.form(key=f"form_{nome}"):
        camp = st.text_input("Campeonato", key=f"camp_{nome}")
        casa = st.text_input("Casa", key=f"casa_{nome}")
        visitante = st.text_input("Visitante", key=f"vis_{nome}")
        horario = st.text_input("Horário", key=f"hor_{nome}")
        ht = st.text_input("Placar HT", key=f"ht_{nome}")
        ft = st.text_input("Placar FT", key=f"ft_{nome}")
        lista = st.text_area("Lista", key=f"lista_{nome}")
        mercado = st.selectbox("Mercado", ["BTTS", "O1.5", "O2.5", "LTD", "Casa", "Vis"], key=f"merc_{nome}")
        prob = st.number_input("% Probabilidade", 0, 100, 70, key=f"prob_{nome}")
        btn_analisar = st.form_submit_button("📊 ANALISAR")
        btn_enviar = st.form_submit_button("🚀 ENVIAR ALERTA")

    if btn_analisar:
        st.session_state[f"dados_{nome}"] = {"camp": camp, "casa": casa, "vis": visitante, "horario": horario, "ht": ht, "ft": ft, "merc": mercado, "prob": prob}
        st.rerun()

    # Exibição dos botões de controle após envio
    if f"dados_{nome}" in st.session_state:
        d = st.session_state[f"dados_{nome}"]
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("⏱️ MOMENTO", key=f"mom_{nome}"): 
                enviar_ou_editar(nome, f"⏱️ MOMENTO AO VIVO\n{d['casa']} x {d['vis']}\nPlacar: HT {d['ht']} | FT {d['ft']}")
            if st.button("✅ HT GREEN", key=f"htg_{nome}"): 
                enviar_ou_editar(nome, f"✅ HT GREEN!\n{d['casa']} x {d['vis']}\nPlacar HT: {d['ht']}")
        with col2:
            if st.button("✅ FINAL GREEN", key=f"fng_{nome}"): 
                enviar_ou_editar(nome, f"🏆 FINAL GREEN!\n{d['casa']} x {d['vis']}\nPlacar Final: {d['ft']}")
            if st.button("❌ RED", key=f"red_{nome}"): 
                enviar_ou_editar(nome, f"❌ RED!\n{d['casa']} x {d['vis']}\nPlacar Final: {d['ft']}")

    # Envio inicial no formato solicitado
    if btn_enviar and f"dados_{nome}" in st.session_state:
        d = st.session_state[f"dados_{nome}"]
        msg = f"""🚨 Alerta de Cantos 🚨

🏆 Campeonato: {d['camp']}
🆚 Jogo: {d['casa']} x {d['vis']}
🎯 Mercado: {d['merc']}
💥 Prognóstico: Analisado
📈 Probabilidade: {d['prob']}%
⏰ Horário: {d['horario']} (BR)

🔞 Aposte com responsabilidade.
⚠️ Não há garantias de lucro."""
        enviar_ou_editar(nome, msg)

col1, col2, col3 = st.columns(3)
with col1: jogo_normal("JOGO_A")
with col2: jogo_normal("JOGO_B")
with col3: jogo_normal("JOGO_C")
