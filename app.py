import streamlit as st
import requests
import streamlit.components.v1 as components

st.set_page_config(layout="wide", page_title="Sistema Brazukas")
st.title("🤖 Sistema Brazukas Top Tips")

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
    
    # Inputs
    camp = st.text_input("Campeonato", key=f"c_{titulo}")
    casa = st.text_input("Casa", key=f"ca_{titulo}")
    vis = st.text_input("Visitante", key=f"v_{titulo}")
    
    if titulo == "JOGO_D":
        hora = st.text_input("Horário", key=f"h_{titulo}")
        med_time = st.number_input("Média Escanteios Time", key=f"mt_{titulo}")
        med_liga = st.number_input("Média Escanteios Liga", key=f"ml_{titulo}")
        linha = st.text_input("Linha de Escanteios", key=f"lin_{titulo}")
        
        if st.button("📊 ANALISAR JOGO D", key=f"bt_{titulo}"):
            st.session_state[f"dados_{titulo}"] = {"camp": camp, "casa": casa, "vis": vis, "hora": hora, "med_time": med_time, "med_liga": med_liga, "linha": linha}
    else:
        lista = st.text_area("Lista de jogos", key=f"l_{titulo}")
        prob = st.text_input("Probabilidade (%)", key=f"pb_{titulo}")
        mercado = st.text_input("Mercado", key=f"merc_{titulo}")
        
        if st.button("📊 ANALISAR", key=f"bt_{titulo}"):
            st.session_state[f"dados_{titulo}"] = {"camp": camp, "casa": casa, "vis": vis, "lista": lista, "prob": prob, "mercado": mercado}

    # Só mostra o gráfico/envio se os dados existirem no session_state
    if f"dados_{titulo}" in st.session_state:
        st.success("Análise carregada!")
        renderizar_grafico([80, 60, 40], ['A', 'B', 'C'], titulo)
        if st.button("🚀 ENVIAR ALERTA", key=f"enviar_{titulo}"):
            st.write("Enviando...")

col1, col2, col3, col4 = st.columns(4)
with col1: renderizar_bloco("JOGO_A")
with col2: renderizar_bloco("JOGO_B")
with col3: renderizar_bloco("JOGO_C")
with col4: renderizar_bloco("JOGO_D")
    
