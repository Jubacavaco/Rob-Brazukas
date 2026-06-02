import streamlit as st
import requests

st.set_page_config(layout="wide", page_title="Sistema Brazukas")
st.title("🤖 Sistema Brazukas Top Tips")

TOKEN = "8776214366:AAEQnGyhcEa6NQcYzyFAhtVDXKpQx5CoYT0"
CHAT_ID = "-1003925163611"

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

def jogo_normal(nome):
    st.subheader(f"🏟️ {nome}")
    
    with st.form(key=f"form_{nome}"):
        camp = st.text_input("Campeonato", key=f"camp_{nome}")
        casa = st.text_input("Casa", key=f"casa_{nome}")
        visitante = st.text_input("Visitante", key=f"vis_{nome}")
        horario = st.text_input("Horário", key=f"hor_{nome}")
        ht = st.text_input("Placar HT", key=f"ht_{nome}")
        ft = st.text_input("Placar FT", key=f"ft_{nome}")
        lista = st.text_area("Lista de Jogos", key=f"lista_{nome}")
        mercado = st.selectbox("Mercado", ["BTTS", "O1.5", "O2.5", "LTD", "Casa", "Vis"], key=f"merc_{nome}")
        prob = st.number_input("% Probabilidade", 0, 100, 70, key=f"prob_{nome}")
        
        btn_analisar = st.form_submit_button("📊 ANALISAR")
        btn_enviar = st.form_submit_button("🚀 ENVIAR ALERTA")

    # A lógica de análise está fora do 'with' para garantir que funcione
    if btn_analisar:
        st.session_state[f"dados_{nome}"] = {
            "camp": camp, "casa": casa, "vis": visitante, 
            "horario": horario, "ht": ht, "ft": ft, 
            "merc": mercado, "prob": prob
        }
        st.success(f"Análise de {nome} concluída!")
        st.rerun()

    # Exibição dos botões de controle apenas após analisar
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

    # Envio do alerta principal
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

def jogo_d():
    st.subheader("🏟️ JOGO_D (Escanteios)")
    with st.form("JOGO_D"):
        linha = st.selectbox("Linha", [7.5, 8.5, 9.5, 10.5], key="linha_d")
        btn_action = st.form_submit_button("ENVIAR AÇÃO")
    if btn_action:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={"chat_id": CHAT_ID, "text": f"JOGO D\nLinha: {linha}"})

col1, col2, col3, col4 = st.columns(4)
with col1: jogo_normal("JOGO_A")
with col2: jogo_normal("JOGO_B")
with col3: jogo_normal("JOGO_C")
with col4: jogo_d()
