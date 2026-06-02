import streamlit as st
import requests
import streamlit.components.v1 as components

st.set_page_config(layout="wide", page_title="Sistema Brazukas")
st.title("🤖 Sistema Brazukas Pro")

TOKEN = "8776214366:AAEQnGyhcEa6NQcYzyFAhtVDXKpQx5CoYT0"
CHAT_ID = "-1003925163611"

def renderizar_grafico_barra(dados):
    labels = list(dados.keys())
    valores = list(dados.values())
    components.html(f"""
    <div style="height:250px;"><canvas id="chart"></canvas></div>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script>
    new Chart(document.getElementById('chart'), {{
        type: 'bar',
        data: {{ labels: {labels}, datasets: [{{ data: {valores}, backgroundColor: '#ef4444' }}] }},
        options: {{ indexAxis: 'y', responsive: true, maintainAspectRatio: false, scales: {{ x: {{ max: 100 }} }} }}
    }});
    </script>
    """, height=270)

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
    mercado = st.selectbox("Mercado", ["Match Odds", "Gols"], key=f"merc_{nome}")
    horario = st.text_input("Horário", key=f"hor_{nome}")
    prob = st.number_input("Probabilidade (%)", 0, 100, 70, key=f"prob_{nome}")
    ht = st.text_input("HT", key=f"ht_{nome}")
    ft = st.text_input("FT", key=f"ft_{nome}")
    lista = st.text_area("Lista (Para análise)", key=f"lista_{nome}")
    
    if st.button("📊 ANALISAR", key=f"ana_{nome}"):
        st.session_state[f"d_{nome}"] = {"camp": camp, "casa": casa, "vis": vis, "hor": horario, "ht": ht, "ft": ft, "merc": mercado, "prob": prob}
        st.session_state[f"p_{nome}"] = {"O1.5": 85, "O2.5": 60, "BTTS": 75, "LTD": 40, "CASA": 65, "VIS": 30}
        st.success("Análise feita!")

    d = st.session_state.get(f"d_{nome}")
    if d:
        renderizar_grafico_barra(st.session_state.get(f"p_{nome}", {}))
        
        if st.button("🚀 ENVIAR ALERTA", key=f"env_{nome}"):
            msg = f"""🚨 Alerta de Cantos 🚨

🏆 Campeonato: {d['camp']}
🆚 Jogo: {d['casa']} x {d['vis']}
🎯 Mercado: {d['merc']}
💥 Prognóstico: {d['merc']}
📈 Probabilidade: {d['prob']}%
⏰ Horário: {d['hor']} (BR)

🔞 Aposte com responsabilidade.
⚠️ Não há garantias de lucro."""
            st.session_state[f"mid_{nome}"] = telegram(msg)
            
        mid = st.session_state.get(f"mid_{nome}")
        if mid:
            c1, c2 = st.columns(2)
            # Atualizações mantendo o modelo solicitado
            if c1.button("⏱️ MOMENTO", key=f"mom_{nome}"): telegram(f"🚨 Alerta de Cantos 🚨\n\n🏆 Campeonato: {d['camp']}\n🆚 Jogo: {d['casa']} x {d['vis']}\n🟢 Em Andamento\n⏰ Placar: HT {d['ht']} | FT {d['ft']}\n\n🔞 Aposte com responsabilidade.", mid)
            if c1.button("✅ HT GREEN", key=f"htg_{nome}"): telegram(f"🚨 Alerta de Cantos 🚨\n\n🏆 Campeonato: {d['camp']}\n🆚 Jogo: {d['casa']} x {d['vis']}\n✅ HT GREEN! {d['ht']}\n\n🔞 Aposte com responsabilidade.", mid)
            if c2.button("🏆 FINAL GREEN", key=f"fng_{nome}"): telegram(f"🚨 Alerta de Cantos 🚨\n\n🏆 Campeonato: {d['camp']}\n🆚 Jogo: {d['casa']} x {d['vis']}\n🏆 FINAL GREEN! {d['ft']}\n\n🔞 Aposte com responsabilidade.", mid)
            if c2.button("❌ RED", key=f"red_{nome}"): telegram(f"🚨 Alerta de Cantos 🚨\n\n🏆 Campeonato: {d['camp']}\n🆚 Jogo: {d['casa']} x {d['vis']}\n❌ RED! {d['ft']}\n\n🔞 Aposte com responsabilidade.", mid)

def jogo_d():
    st.subheader("🏟️ JOGO_D (Escanteios)")
    linha = st.selectbox("Linha", [7.5, 8.5, 9.5, 10.5], key="linha_d")
    if st.button("🚀 ENVIAR ALERTA", key="d_env"): 
        st.session_state["mid_d"] = telegram(f"🚨 Alerta de Escanteios 🚨\n\n🏟️ JOGO D\n🎯 Linha: {linha}")
    
    mid = st.session_state.get("mid_d")
    if mid:
        if st.button("⏱️ MOMENTO", key="d_mom"): telegram(f"🚨 Alerta de Escanteios 🚨\n\n🏟️ JOGO D\n🎯 Linha: {linha}\n🟢 Em Andamento", mid)
        if st.button("✅ HT GREEN", key="d_htg"): telegram(f"🚨 Alerta de Escanteios 🚨\n\n🏟️ JOGO D\n🎯 Linha: {linha}\n✅ HT GREEN!", mid)
        if st.button("🏆 FINAL GREEN", key="d_fng"): telegram(f"🚨 Alerta de Escanteios 🚨\n\n🏟️ JOGO D\n🎯 Linha: {linha}\n🏆 FINAL GREEN!", mid)
        if st.button("❌ RED", key="d_fnr"): telegram(f"🚨 Alerta de Escanteios 🚨\n\n🏟️ JOGO D\n🎯 Linha: {linha}\n❌ RED!", mid)

c1, c2, c3, c4 = st.columns(4)
with c1: jogo_normal("JOGO_A")
with c2: jogo_normal("JOGO_B")
with c3: jogo_normal("JOGO_C")
with c4: jogo_d()
