import streamlit as st
import requests
import streamlit.components.v1 as components

st.set_page_config(layout="wide", page_title="Sistema Brazukas")
st.title("🤖 Sistema Brazukas Top Tips")

TOKEN = "8776214366:AAEQnGyhcEa6NQcYzyFAhtVDXKpQx5CoYT0"
CHAT_ID = "-1003925163611"

def enviar_telegram(msg):
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={"chat_id": CHAT_ID, "text": msg})

def renderizar_grafico(dados):
    labels, valores = list(dados.keys()), list(dados.values())
    components.html(f"""
    <div style="height:250px;"><canvas id="chart"></canvas></div>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script>
    new Chart(document.getElementById('chart'), {{
        type: 'bar',
        data: {{ labels: {labels}, datasets: [{{ data: {valores}, backgroundColor: '#3b82f6', borderRadius: 5 }}] }},
        options: {{ responsive: true, maintainAspectRatio: false, scales: {{ y: {{ max: 100, beginAtZero: true }} }} }}
    }});
    </script>
    """, height=280)

def calcular_probabilidades(lista):
    return {"BTTS": 61, "O1.5": 78, "O2.5": 52, "LTD": 70, "Casa": 65, "Vis": 15}

def jogo_normal(nome):
    st.subheader(f"🏟️ {nome}")
    with st.form(key=f"form_{nome}"):
        camp = st.text_input("Campeonato")
        casa = st.text_input("Casa")
        visitante = st.text_input("Visitante")
        horario = st.text_input("Horário")
        lista = st.text_area("Lista de Jogos")
        # Este é o campo onde VOCÊ escolhe o que enviar
        mercado_envio = st.selectbox("Qual mercado enviar?", ["BTTS", "O1.5", "O2.5", "LTD", "Casa", "Vis"])
        
        btn_analisar = st.form_submit_button("📊 ANALISAR")
        btn_enviar = st.form_submit_button("🚀 ENVIAR ESCOLHIDO")

    if btn_analisar:
        st.session_state[f"probs_{nome}"] = calcular_probabilidades(lista)
        st.session_state[f"dados_{nome}"] = {"camp": camp, "casa": casa, "vis": visitante, "horario": horario}
        st.rerun()

    if f"probs_{nome}" in st.session_state:
        probs = st.session_state[f"probs_{nome}"]
        d = st.session_state[f"dados_{nome}"]
        
        # Identifica a aposta recomendada (maior valor)
        recomendado = max(probs, key=probs.get)
        
        st.info(f"💡 **Aposta Recomendada pelo sistema:** {recomendado} ({probs[recomendado]}%)")
        
        cols = st.columns(3)
        for i, (m, p) in enumerate(probs.items()):
            cols[i % 3].write(f"{'🔥' if p >= 70 else '⚠️'} **{m}**: {p}%")
        renderizar_grafico(probs)

    if btn_enviar and f"probs_{nome}" in st.session_state:
        d = st.session_state[f"dados_{nome}"]
        probs = st.session_state[f"probs_{nome}"]
        # Envia o mercado que você selecionou no selectbox
        msg = f"🚨 Alerta de Cantos 🚨\n\n🏆 Campeonato: {d['camp']}\n🆚 Jogo: {d['casa']} x {d['vis']}\n🎯 Mercado Escolhido: {mercado_envio}\n📈 Probabilidade: {probs.get(mercado_envio, 0)}%\n⏰ Horário: {d['horario']} (BR)\n\n🔞 Aposte com responsabilidade."
        enviar_telegram(msg)
        st.success(f"Enviado {mercado_envio} com sucesso!")

def jogo_d():
    st.subheader("🏟️ JOGO_D (Escanteios)")
    with st.form("JOGO_D"):
        linha = st.selectbox("Linha", [7.5, 8.5, 9.5, 10.5])
        btn_htg = st.form_submit_button("ENVIAR AÇÃO")
    if btn_htg: enviar_telegram(f"JOGO D\nLinha: {linha}")

col1, col2, col3, col4 = st.columns(4)
with col1: jogo_normal("JOGO_A")
with col2: jogo_normal("JOGO_B")
with col3: jogo_normal("JOGO_C")
with col4: jogo_d()
