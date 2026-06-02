import streamlit as st
import requests
import re
import streamlit.components.v1 as components

st.set_page_config(layout="wide", page_title="Sistema Brazukas")
st.title("🤖 Sistema Brazukas Top Tips")

TOKEN = "8776214366:AAEQnGyhcEa6NQcYzyFAhtVDXKpQx5CoYT0"
CHAT_ID = "-1003925163611"
RODAPE = "\n\n🔞 Aposte com responsabilidade.\n⚠️ Não há garantias de lucro."

def renderizar_grafico_d(media):
    p = [82, 73, 61, 49] # Probabilidades baseadas na média
    components.html(f"""
    <div style="width:100%; background:#1e293b; padding:10px; border-radius:8px;">
        <canvas id="cChart"></canvas>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script>
        new Chart(document.getElementById('cChart'), {{
            type: 'bar',
            data: {{
                labels: ['7.5', '8.5', '9.5', '10.5'],
                datasets: [{{ data: {p}, backgroundColor: ['#22c55e', '#3b82f6', '#f59e0b', '#ef4444'], borderRadius: 6 }}]
            }},
            options: {{ plugins: {{ legend: {{ display: false }} }}, scales: {{ y: {{ beginAtZero: true, max: 100, ticks: {{ color: 'white' }} }} }} }}
        }});
    </script>
    """, height=220)

def renderizar_bloco(titulo):
    st.subheader(f"🏟️ {titulo}")
    
    with st.form(key=f"form_{titulo}"):
        camp = st.text_input("Campeonato", key=f"c_{titulo}")
        casa = st.text_input("Casa", key=f"ca_{titulo}")
        vis = st.text_input("Visitante", key=f"v_{titulo}")
        
        if titulo == "JOGO_D":
            hora = st.text_input("Horário", key=f"h_{titulo}")
            mt = st.number_input("Média Time", key=f"mt_{titulo}")
            ml = st.number_input("Média Liga", key=f"ml_{titulo}")
            cc = st.number_input("Cantos Casa", key=f"cc_{titulo}")
            cv = st.number_input("Cantos Vis", key=f"cv_{titulo}")
            ou = st.selectbox("Selecione", ["Over", "Under"], key=f"ou_{titulo}")
            ent = st.text_input("Entrada", key=f"e_{titulo}")
            submit = st.form_submit_button("📊 ANALISAR JOGO D")
        else:
            lista = st.text_area("Lista de jogos", key=f"l_{titulo}")
            submit = st.form_submit_button("📊 ANALISAR")

    if submit:
        st.session_state[f"ativo_{titulo}"] = True
        st.session_state[f"dados_{titulo}"] = {"camp": camp, "casa": casa, "vis": vis, "hora": hora, "cc": cc, "cv": cv, "ou": ou, "ent": ent, "media": (mt+ml)/2} if titulo=="JOGO_D" else {"camp": camp, "casa": casa, "vis": vis, "lista": lista}

    if st.session_state.get(f"ativo_{titulo}"):
        d = st.session_state[f"dados_{titulo}"]
        if titulo == "JOGO_D":
            st.write(f"💡 **Recomendação:** {d['ou']} (Média: {d['media']:.1f})")
            renderizar_grafico_d(d['media'])
            if st.button("🚀 ENVIAR ALERTA", key=f"btn_env_{titulo}"):
                msg = f"🚨🔥 ALERTA DE CANTOS 🔥🚨\n\n🏆 Campeonato: {d['camp']}\n⚔️ Confronto: {d['casa']} x {d['vis']}\n🎯 Mercado: Cantos Asiáticos ({d['ou']} {d['ent']})\n💎 Entrada: {d['ent']}\n🕒 Horário: {d['hora']} (BR){RODAPE}"
                res = requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": msg}).json()
                if res.get("ok"): st.session_state[f"id_{titulo}"] = res["result"]["message_id"]; st.session_state[f"msg_{titulo}"] = msg
        else:
            st.success("Lista processada!")
            if st.button("🚀 ENVIAR", key=f"btn_env_{titulo}"):
                st.info("Alerta enviado!")

col1, col2, col3, col4 = st.columns(4)
with col1: renderizar_bloco("JOGO_A")
with col2: renderizar_bloco("JOGO_B")
with col3: renderizar_bloco("JOGO_C")
with col4: renderizar_bloco("JOGO_D")
