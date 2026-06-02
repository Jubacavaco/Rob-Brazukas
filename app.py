import streamlit as st
import requests
import streamlit.components.v1 as components

st.set_page_config(layout="wide", page_title="Sistema Brazukas")
st.title("🤖 Sistema Brazukas Top Tips")
import requests
import streamlit.components.v1 as components

st.set_page_config(layout="wide", page_title="Sistema Brazukas")
st.title("🤖 Sistema Brazukas Top Tips")

# =============================
# TELEGRAM CONFIG (BACKEND)
# =============================
TOKEN = "8776214366:AAEQnGyhcEa6NQcYzyFAhtVDXKpQx5CoYT0"
CHAT_ID = "-1003925163611"

def enviar_telegram(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": msg})


def editar_telegram(msg, message_id):
    url = f"https://api.telegram.org/bot{TOKEN}/editMessageText"
    requests.post(url, json={
        "chat_id": CHAT_ID,
        "message_id": message_id,
        "text": msg
    })


# =============================
# ANALISE DE MERCADO (SIMULADA)
# =============================
def analisar_mercados():
    return {
        "Casa vence": 65,
        "Empate": 20,
        "Visitante": 15,
        "Over 1.5": 78,
        "Over 2.5": 52,
        "Ambas Marcam": 61,
        "LTD": 70
    }


def mercado_fervendo(prob):
    return "🔥 MERCADO PEGANDO FOGO" if prob >= 70 else "⚠️ Mercado estável"


def recomendacao(mercados):
    melhor = max(mercados, key=mercados.get)
    return melhor


# =============================
# GRAFICO
# =============================
def renderizar_grafico(dados):
    labels = list(dados.keys())
    valores = list(dados.values())

    components.html(f"""
    <div style="background:#111; padding:10px; border-radius:10px;">
    <canvas id="chart"></canvas>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script>
    new Chart(document.getElementById('chart'), {{
        type: 'bar',
        data: {{
            labels: {labels},
            datasets: [{{
                data: {valores},
                backgroundColor: '#22c55e'
            }}]
        }},
        options: {{
            scales: {{
                y: {{
                    max: 100,
                    beginAtZero: true
                }}
            }}
        }}
    }});
    </script>
    """, height=250)


# =============================
# BLOCO JOGO A/B/C
# =============================
def jogo_normal(nome):
    st.subheader(f"🏟️ {nome}")

    with st.form(key=nome):
        casa = st.text_input("Casa")
        visitante = st.text_input("Visitante")

        ht = st.text_input("Placar HT")
        ft = st.text_input("Placar FT")

        submit = st.form_submit_button("📊 ANALISAR")

    if submit:
        mercados = analisar_mercados()
        rec = recomendacao(mercados)

        msg = f"""
{nome}
Casa: {casa} x {visitante}

HT: {ht}
FT: {ft}

🎯 Aposta recomendada: {rec}
🔥 Status: {mercado_fervendo(mercados[rec])}
"""

        st.success(msg)
        renderizar_grafico(mercados)

        enviar_telegram(msg)


# =============================
# JOGO D (ESPECIAL ESCANTEIOS)
# =============================
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

    if ht_btn:
        msg = f"JOGO D\nHT GREEN\nLinha: {linha}"
        enviar_telegram(msg)

    if ht_red:
        msg = f"JOGO D\nHT RED\nLinha: {linha}"
        enviar_telegram(msg)

    if momento:
        msg = f"JOGO D\nMOMENTO (ESCANTEIOS AO VIVO)\nLinha: {linha}"
        enviar_telegram(msg)

    if final:
        msg = f"JOGO D\nFINAL GREEN\nLinha: {linha}"
        enviar_telegram(msg)

    if red:
        msg = f"JOGO D\nFINAL RED\nLinha: {linha}"
        enviar_telegram(msg)


# =============================
# LAYOUT
# =============================
col1, col2, col3, col4 = st.columns(4)

with col1:
    jogo_normal("JOGO_A")

with col2:
    jogo_normal("JOGO_B")

with col3:
    jogo_normal("JOGO_C")

with col4:
    jogo_d()azukas Top Tips")

def renderizar_grafico(data, labels, titulo):
    components.html(f"""
    <div style="background:#1e293b; padding:10px; border-radius:8px;"><canvas id="cChart"></canvas></div>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script>
        new Chart(document.getElementById('cChart'), {{
            type: 'bar',
            data: {{ labels: {labels}, datasets: [{{ data: {data}, backgroundColor: '#3b82f6', borderRadius: 6 }}] }},
            options: {{ plugins: {{ legend: {{ display: false }} }}, scales: {{ y: {{ beginAtZero: true, max: 100, ticks: {{ color: 'white' }} }} }} }}
        }});
    </script>
    """, height=200)

def renderizar_bloco(titulo):
    st.subheader(f"🏟️ {titulo}")
    
    # O form garante que o botão "ANALISAR" dispare o processamento
    with st.form(key=f"form_{titulo}"):
        camp = st.text_input("Campeonato", key=f"c_{titulo}")
        casa = st.text_input("Casa", key=f"ca_{titulo}")
        vis = st.text_input("Visitante", key=f"v_{titulo}")
        hora = st.text_input("Horário", key=f"h_{titulo}")
        
        if titulo == "JOGO_D":
            med_time = st.number_input("Média Escanteios Time", key=f"mt_{titulo}")
            med_liga = st.number_input("Média Escanteios Liga", key=f"ml_{titulo}")
            linha = st.text_input("Linha de Escanteios", key=f"lin_{titulo}")
        else:
            lista = st.text_area("Lista de jogos", key=f"l_{titulo}")
            prob = st.text_input("Probabilidade (%)", key=f"pb_{titulo}")
            mercado = st.text_input("Mercado", key=f"merc_{titulo}")
            pht = st.text_input("Placar HT", key=f"pht_{titulo}")
            pfin = st.text_input("Placar Final", key=f"pfin_{titulo}")
            
        submit_button = st.form_submit_button(label='📊 ANALISAR')
    
    # Após o clique, processamos
    if submit_button:
        st.session_state[f"dados_{titulo}"] = {"camp": camp, "casa": casa, "vis": vis, "hora": hora}
        st.success("Análise realizada!")
        renderizar_grafico([80, 60, 40], ['A', 'B', 'C'], titulo)
        st.info("Pronto para enviar ao Telegram.")

col1, col2, col3, col4 = st.columns(4)
with col1: renderizar_bloco("JOGO_A")
with col2: renderizar_bloco("JOGO_B")
with col3: renderizar_bloco("JOGO_C")
with col4: renderizar_bloco("JOGO_D")
