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

# Gráfico mais elegante usando Chart.js com cores definidas
def renderizar_grafico(dados):
    labels = list(dados.keys())
    valores = list(dados.values())
    components.html(f"""
    <div style="width: 100%; height: 250px;">
        <canvas id="chart"></canvas>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script>
    new Chart(document.getElementById('chart'), {{
        type: 'bar',
        data: {{
            labels: {labels},
            datasets: [{{
                label: 'Probabilidade (%)',
                data: {valores},
                backgroundColor: '#3b82f6',
                borderColor: '#2563eb',
                borderWidth: 1,
                borderRadius: 5
            }}]
        }},
        options: {{
            responsive: true,
            maintainAspectRatio: false,
            scales: {{ y: {{ max: 100, beginAtZero: true, ticks: {{ color: '#ccc' }} }}, x: {{ ticks: {{ color: '#ccc' }} }} }},
            plugins: {{ legend: {{ labels: {{ color: '#fff' }} }} }}
        }}
    }});
    </script>
    """, height=280)

def calcular_probabilidades(lista):
    # Simulação dos cálculos que você pediu
    return {"BTTS": 61, "O1.5": 78, "O2.5": 52, "LTD": 70, "Casa": 65, "Vis": 15}

def jogo_normal(nome):
    st.subheader(f"🏟️ {nome}")
    with st.form(key=f"form_{nome}"):
        camp = st.text_input("Campeonato")
        casa = st.text_input("Casa")
        visitante = st.text_input("Visitante")
        horario = st.text_input("Horário")
        lista = st.text_area("Lista de Jogos (Dados)")
        mercado = st.selectbox("Mercado para envio", ["BTTS", "OVER 1.5 FT", "OVER 2.5 FT", "LTD", "Casa vence", "Visitante"])
        
        btn_analisar = st.form_submit_button("📊 ANALISAR")
        btn_enviar = st.form_submit_button("🚀 ENVIAR ALERTA")

    if btn_analisar:
        st.session_state[f"probs_{nome}"] = calcular_probabilidades(lista)
        st.session_state[f"dados_{nome}"] = {"camp": camp, "casa": casa, "vis": visitante, "horario": horario}
        
    if f"probs_{nome}" in st.session_state:
        probs = st.session_state[f"probs_{nome}"]
        d = st.session_state[f"dados_{nome}"]
        
        # Visualização detalhada das % na tela
        cols = st.columns(3)
        for i, (m, p) in enumerate(probs.items()):
            status = "🔥" if p >= 70 else "⚠️"
            cols[i % 3].write(f"{status} **{m}**: {p}%")
            
        renderizar_grafico(probs)

    if btn_enviar:
        d = st.session_state[f"dados_{nome}"]
        probs = st.session_state[f"probs_{nome}"]
        msg = f"""🚨 Alerta de Cantos 🚨

🏆 Campeonato: {d['camp']}
🆚 Jogo: {d['casa']} x {d['vis']}
🎯 Mercado: {mercado}
📈 Probabilidade: {probs.get(mercado, 0)}%
⏰ Horário: {d['horario']} (BR)

🔞 Aposte com responsabilidade.
⚠️ Não há garantias de lucro."""
        enviar_telegram(msg)
        st.success("Enviado!")

# JOGO D e colunas permanecem iguais...
