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

# Lógica de cálculo individual (Aqui você pode customizar cada regra se desejar)
def calcular_probabilidades(lista, nome):
    # Exemplo: cálculo baseado no tamanho da lista para diferenciar os jogos
    base = 50 + (len(lista) % 40) 
    return {
        "BTTS": base + 11, 
        "O1.5": base + 28, 
        "O2.5": base + 2, 
        "LTD": base + 20, 
        "Casa": base + 15, 
        "Vis": base - 35
    }

def jogo_normal(nome):
    st.subheader(f"🏟️ {nome}")
    with st.form(key=f"form_{nome}"):
        camp = st.text_input("Campeonato", key=f"camp_{nome}")
        casa = st.text_input("Casa", key=f"casa_{nome}")
        visitante = st.text_input("Visitante", key=f"vis_{nome}")
        horario = st.text_input("Horário", key=f"hor_{nome}")
        lista = st.text_area("Lista de Jogos", key=f"lista_{nome}")
        
        mercado_envio = st.selectbox("Qual mercado enviar?", ["BTTS", "O1.5", "O2.5", "LTD", "Casa", "Vis"], key=f"merc_{nome}")
        prob_manual = st.number_input("Definir % da Probabilidade", min_value=0, max_value=100, value=70, key=f"prob_{nome}")
        
        btn_analisar = st.form_submit_button("📊 ANALISAR")
        btn_enviar = st.form_submit_button("🚀 ENVIAR ESCOLHIDO")

    if btn_analisar:
        # O cálculo agora usa o 'nome' do jogo para isolar os dados
        st.session_state[f"probs_{nome}"] = calcular_probabilidades(lista, nome)
        st.session_state[f"dados_{nome}"] = {"camp": camp, "casa": casa, "vis": visitante, "horario": horario}
        st.rerun()

    # Exibição isolada
    if f"probs_{nome}" in st.session_state:
        probs = st.session_state[f"probs_{nome}"]
        d = st.session_state[f"dados_{nome}"]
        
        recomendado = max(probs, key=probs.get)
        st.info(f"💡 **Recomendado ({nome}):** {recomendado} ({probs[recomendado]}%)")
        
        cols = st.columns(3)
        for i, (m, p) in enumerate(probs.items()):
            cols[i % 3].write(f"{'🔥' if p >= 70 else '⚠️'} **{m}**: {p}%")
        renderizar_grafico(probs)

    if btn_enviar and f"probs_{nome}" in st.session_state:
        d = st.session_state[f"dados_{nome}"]
        msg = f"🚨 Alerta de Cantos 🚨\n\n🏆 Campeonato: {d['camp']}\n🆚 Jogo: {d['casa']} x {d['vis']}\n🎯 Mercado: {mercado_envio}\n📈 Probabilidade: {prob_manual}%\n⏰ Horário: {d['horario']} (BR)\n\n🔞 Aposte com responsabilidade."
        enviar_telegram(msg)
        st.success(f"Enviado {nome}!")

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
