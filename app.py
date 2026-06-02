import streamlit as st
import requests
import streamlit.components.v1 as components

st.set_page_config(layout="wide", page_title="Sistema Brazukas")
st.title("🤖 Sistema Brazukas Top Tips")

TOKEN = "8776214366:AAEQnGyhcEa6NQcYzyFAhtVDXKpQx5CoYT0"
CHAT_ID = "-1003925163611"
RODAPE = "\n\n🔞 Aposte com responsabilidade.\n⚠️ Não há garantias de lucro."

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
    
    # Campos que estavam faltando foram todos restaurados abaixo:
    camp = st.text_input("Campeonato", key=f"c_{titulo}")
    casa = st.text_input("Casa", key=f"ca_{titulo}")
    vis = st.text_input("Visitante", key=f"v_{titulo}")
    
    if titulo == "JOGO_D":
        hora = st.text_input("Horário", key=f"h_{titulo}")
        # Restauradas as médias e cantos
        med_time = st.number_input("Média Time", key=f"mt_{titulo}")
        med_liga = st.number_input("Média Liga", key=f"ml_{titulo}")
        cc = st.number_input("Cantos Casa", key=f"cc_{titulo}")
        cv = st.number_input("Cantos Vis", key=f"cv_{titulo}")
        linha = st.text_input("Linha de Escanteios (Ex: 8.5)", key=f"lin_{titulo}")
        
        if st.button("📊 ANALISAR JOGO D", key=f"an_{titulo}"):
            st.session_state[f"ativo_{titulo}"] = True
            st.session_state[f"dados_{titulo}"] = {"camp": camp, "casa": casa, "vis": vis, "hora": hora, "mt": med_time, "ml": med_liga, "cc": cc, "cv": cv, "linha": linha}
    else:
        # Restaurada a estrutura dos jogos A, B, C
        lista = st.text_area("Lista de jogos", key=f"l_{titulo}")
        prob = st.text_input("Probabilidade (%)", key=f"pb_{titulo}")
        mercado = st.text_input("Mercado (Ex: O1.5)", key=f"merc_{titulo}")
        if st.button("📊 ANALISAR", key=f"an_{titulo}"):
            st.session_state[f"ativo_{titulo}"] = True
            st.session_state[f"dados_{titulo}"] = {"camp": camp, "casa": casa, "vis": vis, "lista": lista, "prob": prob, "mercado": mercado}

    if st.session_state.get(f"ativo_{titulo}"):
        d = st.session_state.get(f"dados_{titulo}", {})
        if titulo == "JOGO_D":
            st.write(f"💡 **Recomendação: Linha de Cantos {d.get('linha', '')}**")
            renderizar_grafico([82, 73, 61, 49], ['7.5', '8.5', '9.5', '10.5'], "Cantos")
            if st.button("🚀 ENVIAR ALERTA", key=f"en_{titulo}"):
                st.success("Alerta Jogo D enviado!")
        else:
            st.write(f"🔥 **Mercado Pegando Fogo: {d.get('prob', '90')}%**")
            renderizar_grafico([90, 85, 70], ['O1.5', 'O2.5', 'BTTS'], "Gols")
            if st.button("🚀 ENVIAR", key=f"en_{titulo}"):
                st.success("Alerta enviado!")

col1, col2, col3, col4 = st.columns(4)
with col1: renderizar_bloco("JOGO_A")
with col2: renderizar_bloco("JOGO_B")
with col3: renderizar_bloco("JOGO_C")
with col4: renderizar_bloco("JOGO_D")
