import streamlit as st
import requests
import streamlit.components.v1 as components

st.set_page_config(layout="wide", page_title="Sistema Brazukas")
st.title("🤖 Sistema Brazukas Top Tips")

TOKEN = "8776214366:AAEQnGyhcEa6NQcYzyFAhtVDXKpQx5CoYT0"
CHAT_ID = "-1003925163611"

# Função centralizada para comunicação com o Telegram
def enviar_ou_editar(nome, msg):
    url_base = f"https://api.telegram.org/bot{TOKEN}"
    if f"msg_id_{nome}" in st.session_state:
        # Edita mensagem existente
        requests.post(f"{url_base}/editMessageText", json={
            "chat_id": CHAT_ID, 
            "message_id": st.session_state[f"msg_id_{nome}"], 
            "text": msg
        })
    else:
        # Envia nova e salva o ID
        resp = requests.post(f"{url_base}/sendMessage", json={"chat_id": CHAT_ID, "text": msg}).json()
        if resp.get("ok"):
            st.session_state[f"msg_id_{nome}"] = resp["result"]["message_id"]

def renderizar_grafico(dados):
    labels, valores = list(dados.keys()), list(dados.values())
    components.html(f"""
    <div style="height:250px;"><canvas id="chart"></canvas></div>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script>
    new Chart(document.getElementById('chart'), {{
        type: 'bar',
        data: {{ labels: {labels}, datasets: [{{ data: {valores}, backgroundColor: '#3b82f6' }}] }},
        options: {{ responsive: true, maintainAspectRatio: false }}
    }});
    </script>
    """, height=280)

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
        btn_enviar = st.form_submit_button("🚀 ENVIAR")

    if btn_analisar:
        st.session_state[f"probs_{nome}"] = calcular_probabilidades(lista)
        st.session_state[f"dados_{nome}"] = {"camp": camp, "casa": casa, "vis": visitante, "horario": horario, "ht": ht, "ft": ft}
        st.rerun()

    if f"dados_{nome}" in st.session_state:
        d = st.session_state[f"dados_{nome}"]
        renderizar_grafico(st.session_state.get(f"probs_{nome}", {}))
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("⏱️ MOMENTO", key=f"mom_{nome}"): enviar_ou_editar(nome, f"⏱️ AO VIVO\n{d['casa']} x {d['vis']}\nHT: {d['ht']} | FT: {d['ft']}")
            if st.button("✅ HT GREEN", key=f"htg_{nome}"): enviar_ou_editar(nome, f"✅ HT GREEN\n{d['casa']} x {d['vis']}\nHT: {d['ht']}")
        with col2:
            if st.button("✅ FINAL GREEN", key=f"fng_{nome}"): enviar_ou_editar(nome, f"🏆 FINAL GREEN\n{d['casa']} x {d['vis']}\nFT: {d['ft']}")
            if st.button("❌ RED", key=f"red_{nome}"): enviar_ou_editar(nome, f"❌ RED\n{d['casa']} x {d['vis']}\nFT: {d['ft']}")

    if btn_enviar and f"dados_{nome}" in st.session_state:
        d = st.session_state[f"dados_{nome}"]
        msg = f"🚨 Alerta de Cantos 🚨\n\n🏆 {d['camp']}\n🆚 {d['casa']} x {d['vis']}\n🎯 {mercado}\n📈 {prob}%\n⏰ {d['horario']}"
        enviar_ou_editar(nome, msg)

def jogo_d():
    st.subheader("🏟️ JOGO_D")
    with st.form("JOGO_D"):
        linha = st.selectbox("Linha", [7.5, 8.5, 9.5])
        if st.form_submit_button("ENVIAR AÇÃO"): enviar_telegram(f"JOGO D: {linha}")

col1, col2, col3, col4 = st.columns(4)
with col1: jogo_normal("JOGO_A")
with col2: jogo_normal("JOGO_B")
with col3: jogo_normal("JOGO_C")
with col4: jogo_d()
