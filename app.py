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

# Função que simula o cálculo baseado na lista de jogos
def calcular_probabilidades(lista):
    # Aqui entra a sua lógica de processamento da lista
    # Exemplo simulado:
    return {
        "BTTS": 75,
        "OVER 1.5": 82,
        "OVER 2.5": 60,
        "LTD": 45
    }

def jogo_normal(nome):
    st.subheader(f"🏟️ {nome}")
    with st.form(key=f"form_{nome}"):
        casa = st.text_input("Casa")
        visitante = st.text_input("Visitante")
        horario = st.text_input("Horário")
        lista = st.text_area("Lista de Jogos para Análise") # Lista de entrada
        ht = st.text_input("Placar HT")
        ft = st.text_input("Placar FT")
        mercado = st.selectbox("Mercado para envio", ["BTTS", "OVER 1.5 FT", "OVER 2.5 FT", "LTD", "Casa vence", "Visitante"])
        
        btn_analisar = st.form_submit_button("📊 ANALISAR LISTA")
        btn_enviar = st.form_submit_button("🚀 ENVIAR PARA TELEGRAM")

    if btn_analisar:
        if lista:
            st.session_state[f"probs_{nome}"] = calcular_probabilidades(lista)
            renderizar_grafico(st.session_state[f"probs_{nome}"])
            st.success("Cálculo realizado com base na lista!")
        else:
            st.warning("Cole a lista primeiro.")

    if btn_enviar:
        probs = st.session_state.get(f"probs_{nome}", {"Erro": 0})
        status = "🔥 MERCADO PEGANDO FOGO" if probs.get(mercado, 0) >= 70 else "⚠️ Mercado estável"
        msg = f"{nome}\n⚔️ {casa} x {visitante}\n🕒 {horario}\nHT: {ht} | FT: {ft}\n🎯 Mercado: {mercado}\n📊 Probabilidade calculada: {probs.get(mercado, 0)}%\n{status}"
        enviar_telegram(msg)
        st.success("Enviado com sucesso!")

def jogo_d():
    st.subheader("🏟️ JOGO_D (Escanteios)")
    with st.form("JOGO_D"):
        linha = st.selectbox("Linha", [7.5, 8.5, 9.5, 10.5])
        media_time = st.number_input("Média Time")
        media_liga = st.number_input("Média Liga")
        btn_exec = st.form_submit_button("ENVIAR AÇÃO")
        # ... (restante da lógica do jogo D)

col1, col2, col3, col4 = st.columns(4)
with col1: jogo_normal("JOGO_A")
with col2: jogo_normal("JOGO_B")
with col3: jogo_normal("JOGO_C")
with col4: jogo_d()
