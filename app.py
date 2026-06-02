import streamlit as st
import requests
import streamlit.components.v1 as components

st.set_page_config(layout="wide", page_title="Sistema Brazukas")
st.title("🤖 Sistema Brazukas Top Tips")

TOKEN = "8776214366:AAEQnGyhcEa6NQcYzyFAhtVDXKpQx5CoYT0"
CHAT_ID = "-1003925163611"

def enviar_telegram(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": msg})

def renderizar_grafico(dados):
    labels = list(dados.keys())
    valores = list(dados.values())
    components.html(f"""
    <div style="background:#111; padding:10px; border-radius:10px;"><canvas id="chart"></canvas></div>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script>
    new Chart(document.getElementById('chart'), {{
        type: 'bar',
        data: {{ labels: {labels}, datasets: [{{ data: {valores}, backgroundColor: '#22c55e' }}] }},
        options: {{ scales: {{ y: {{ max: 100, beginAtZero: true }} }} }}
    }});
    </script>
    """, height=250)

def jogo_normal(nome):
    st.subheader(f"🏟️ {nome}")
    with st.form(key=f"form_{nome}"):
        casa = st.text_input("Casa")
        visitante = st.text_input("Visitante")
        horario = st.text_input("Horário")
        ht = st.text_input("Placar HT")
        ft = st.text_input("Placar FT")
        mercado = st.selectbox("Mercado", ["BTTS", "OVER 1.5 FT", "OVER 2.5 FT", "LTD", "Casa vence", "Visitante"])
        prog = st.number_input("Prognóstico (%)", 0, 100, 90)
        
        btn_analisar = st.form_submit_button("📊 ANALISAR")
        btn_enviar = st.form_submit_button("🚀 ENVIAR PARA TELEGRAM")

    if btn_analisar:
        st.write(f"🔥 **Status:** {'🔥 MERCADO PEGANDO FOGO' if prog >= 70 else '⚠️ Mercado estável'}")
        renderizar_grafico({"Probabilidade": prog, "Outros": 100-prog})
        st.success("Análise concluída!")

    if btn_enviar:
        msg = f"{nome}\n⚔️ {casa} x {visitante}\n🕒 {horario}\nHT: {ht} | FT: {ft}\n🎯 Mercado: {mercado}\n📊 {prog}% {'🔥 MERCADO PEGANDO FOGO' if prog >= 70 else '⚠️ Mercado estável'}"
        enviar_telegram(msg)
        st.success("Enviado com sucesso!")

def jogo_d():
    st.subheader("🏟️ JOGO_D (Escanteios)")
    with st.form("JOGO_D"):
        linha = st.selectbox("Linha", [7.5, 8.5, 9.5, 10.5])
        media_time = st.number_input("Média Time")
        media_liga = st.number_input("Média Liga")
        ht_btn = st.form_submit_button("HT GREEN")
        ht_red = st.form_submit_button("HT RED")
        momento = st.form_submit_button("MOMENTO")
        final = st.form_submit_button("FINAL GREEN")
        red = st.form_submit_button("FINAL RED")
    
    if ht_btn: enviar_telegram(f"JOGO D\nHT GREEN\nLinha: {linha}")
    if ht_red: enviar_telegram(f"JOGO D\nHT RED\nLinha: {linha}")
    if momento: enviar_telegram(f"JOGO D\nMOMENTO\nLinha: {linha}")
    if final: enviar_telegram(f"JOGO D\nFINAL GREEN\nLinha: {linha}")
    if red: enviar_telegram(f"JOGO D\nFINAL RED\nLinha: {linha}")

col1, col2, col3, col4 = st.columns(4)
with col1: jogo_normal("JOGO_A")
with col2: jogo_normal("JOGO_B")
with col3: jogo_normal("JOGO_C")
with col4: jogo_d()
