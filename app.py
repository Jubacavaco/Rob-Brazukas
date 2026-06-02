import streamlit as st
import requests
import streamlit.components.v1 as components

st.set_page_config(layout="wide")
st.title("🤖 Sistema Brazukas")

TOKEN = "8776214366:AAEQnGyhcEa6NQcYzyFAhtVDXKpQx5CoYT0"
CHAT_ID = "-1003925163611"

def renderizar_grafico(dados):
    labels, valores = list(dados.keys()), list(dados.values())
    components.html(f"""
    <div style="height:200px;"><canvas id="chart"></canvas></div>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script>
    new Chart(document.getElementById('chart'), {{
        type: 'bar',
        data: {{ labels: {labels}, datasets: [{{ data: {valores}, backgroundColor: '#3b82f6' }}] }},
        options: {{ responsive: true, maintainAspectRatio: false }}
    }});
    </script>
    """, height=220)

def telegram(msg, msg_id=None):
    url = f"https://api.telegram.org/bot{TOKEN}/"
    if msg_id:
        requests.post(url + "editMessageText", json={"chat_id": CHAT_ID, "message_id": msg_id, "text": msg})
    else:
        resp = requests.post(url + "sendMessage", json={"chat_id": CHAT_ID, "text": msg}).json()
        return resp.get("result", {}).get("message_id")

def jogo_normal(nome):
    st.subheader(f"🏟️ {nome}")
    camp = st.text_input("Campeonato", key=f"camp_{nome}")
    casa = st.text_input("Casa", key=f"casa_{nome}")
    vis = st.text_input("Visitante", key=f"vis_{nome}")
    horario = st.text_input("Horário", key=f"hor_{nome}")
    ht = st.text_input("HT", key=f"ht_{nome}")
    ft = st.text_input("FT", key=f"ft_{nome}")
    lista = st.text_area("Lista", key=f"lista_{nome}")
    mercado = st.selectbox("Mercado", ["BTTS", "O1.5", "O2.5", "LTD", "Casa", "Vis"], key=f"merc_{nome}")
    
    if st.button("📊 ANALISAR", key=f"ana_{nome}"):
        st.session_state[f"d_{nome}"] = {"camp": camp, "casa": casa, "vis": vis, "hor": horario, "ht": ht, "ft": ft, "merc": mercado}
        st.session_state[f"p_{nome}"] = {"BTTS": 60, "O1.5": 80, "O2.5": 50, "LTD": 70}

    if f"d_{nome}" in st.session_state:
        renderizar_grafico(st.session_state[f"p_{nome}"])
        d = st.session_state[f"d_{nome}"]
        
        if st.button("🚀 ENVIAR", key=f"env_{nome}"):
            msg = f"🚨 Alerta: {d['camp']}\n🆚 {d['casa']} x {d['vis']}\n🎯 {d['merc']}\n⏰ {d['hor']}"
            st.session_state[f"mid_{nome}"] = telegram(msg)
            
        if f"mid_{nome}" in st.session_state:
            mid = st.session_state[f"mid_{nome}"]
            c1, c2 = st.columns(2)
            if c1.button("⏱️ MOMENTO", key=f"mom_{nome}"): telegram(f"⏱️ AO VIVO: {d['ht']} | {d['ft']}", mid)
            if c1.button("✅ HT GREEN", key=f"htg_{nome}"): telegram(f"✅ HT GREEN: {d['ht']}", mid)
            if c2.button("✅ FINAL GREEN", key=f"fng_{nome}"): telegram(f"🏆 FINAL GREEN: {d['ft']}", mid)
            if c2.button("❌ RED", key=f"red_{nome}"): telegram(f"❌ RED: {d['ft']}", mid)

def jogo_d():
    st.subheader("🏟️ JOGO_D")
    linha = st.selectbox("Linha", [7.5, 8.5, 9.5], key="linha_d")
    if st.button("ENVIAR", key="d_env"): telegram(f"JOGO D - Linha: {linha}")

col1, col2, col3, col4 = st.columns(4)
with col1: jogo_normal("JOGO_A")
with col2: jogo_normal("JOGO_B")
with col3: jogo_normal("JOGO_C")
with col4: jogo_d()
