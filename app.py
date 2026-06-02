import streamlit as st
import requests
import streamlit.components.v1 as components

st.set_page_config(layout="wide", page_title="Sistema Brazukas")
st.title("🤖 Sistema Brazukas Top Tips")

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
        data: {{ labels: {labels}, datasets: [{{ label: 'Probabilidade (%)', data: {valores}, backgroundColor: '#ef4444' }}] }},
        options: {{ responsive: true, maintainAspectRatio: false, scales: {{ y: {{ max: 100, beginAtZero: true }} }} }}
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
    ht = st.text_input("Placar HT", key=f"ht_{nome}")
    ft = st.text_input("Placar FT", key=f"ft_{nome}")
    lista = st.text_area("Lista", key=f"lista_{nome}")
    
    # O mercado selecionado será o prognóstico
    mercado = st.selectbox("Mercado (Prognóstico)", ["BTTS", "O1.5", "O2.5", "LTD", "Casa", "Vis"], key=f"merc_{nome}")
    prob = st.number_input("% Probabilidade", 0, 100, 70, key=f"prob_{nome}")
    
    if st.button("📊 ANALISAR", key=f"ana_{nome}"):
        st.session_state[f"d_{nome}"] = {
            "camp": camp, "casa": casa, "vis": vis, "hor": horario, 
            "ht": ht, "ft": ft, "merc": mercado, "prob": prob
        }
        st.session_state[f"p_{nome}"] = {"O1.5": 85, "O2.5": 60, "AMBOS": 75, "LTD": 40, "CASA": 65, "VIS": 30}
        st.success("Análise feita!")

    d = st.session_state.get(f"d_{nome}")
    p = st.session_state.get(f"p_{nome}")
    
    if d and p:
        # Exibe o prognóstico escolhido em destaque visual no site
        st.info(f"🎯 **Prognóstico (Mercado):** {d.get('merc')}")
        renderizar_grafico(p)
        
        if st.button("🚀 ENVIAR ALERTA", key=f"env_{nome}"):
            # A mensagem usa o mercado selecionado no selectbox
            msg = f"""🚨 Alerta de Cantos 🚨

🏆 Campeonato: {d.get('camp')}
🆚 Jogo: {d.get('casa')} x {d.get('vis')}
🎯 Mercado: {d.get('merc')}
💥 Prognóstico: {d.get('merc')}
📈 Probabilidade: {d.get('prob')}%
⏰ Horário: {d.get('hor')} (BR)

🔞 Aposte com responsabilidade.
⚠️ Não há garantias de lucro."""
            st.session_state[f"mid_{nome}"] = telegram(msg)
            
        mid = st.session_state.get(f"mid_{nome}")
        if mid:
            c1, c2 = st.columns(2)
            if c1.button("⏱️ MOMENTO", key=f"mom_{nome}"): telegram(f"⏱️ AO VIVO\n{d.get('casa')} x {d.get('vis')}\nHT: {d.get('ht')} | FT: {d.get('ft')}", mid)
            if c1.button("✅ HT GREEN", key=f"htg_{nome}"): telegram(f"✅ HT GREEN!\n{d.get('casa')} x {d.get('vis')}\nHT: {d.get('ht')}", mid)
            if c2.button("✅ FINAL GREEN", key=f"fng_{nome}"): telegram(f"🏆 FINAL GREEN!\n{d.get('casa')} x {d.get('vis')}\nFT: {d.get('ft')}", mid)
            if c2.button("❌ RED", key=f"red_{nome}"): telegram(f"❌ RED!\n{d.get('casa')} x {d.get('vis')}\nFT: {d.get('ft')}", mid)

def jogo_d():
    st.subheader("🏟️ JOGO_D (Escanteios)")
    linha = st.selectbox("Linha", [7.5, 8.5, 9.5, 10.5], key="linha_d")
    if st.button("HT GREEN", key="d_htg"): telegram(f"JOGO D: HT GREEN\nLinha: {linha}")
    if st.button("HT RED", key="d_htr"): telegram(f"JOGO D: HT RED\nLinha: {linha}")
    if st.button("MOMENTO", key="d_mom"): telegram(f"JOGO D: MOMENTO\nLinha: {linha}")
    if st.button("FINAL GREEN", key="d_fng"): telegram(f"JOGO D: FINAL GREEN\nLinha: {linha}")
    if st.button("FINAL RED", key="d_fnr"): telegram(f"JOGO D: FINAL RED\nLinha: {linha}")

c1, c2, c3, c4 = st.columns(4)
with c1: jogo_normal("JOGO_A")
with c2: jogo_normal("JOGO_B")
with c3: jogo_normal("JOGO_C")
with c4: jogo_d()
