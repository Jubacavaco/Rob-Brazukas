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
    <div style="background:#1e293b; padding:10px; border-radius:8px; margin-bottom:10px;">
        <canvas id="cChart"></canvas>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script>
        new Chart(document.getElementById('cChart'), {{
            type: 'bar',
            data: {{ labels: {labels}, datasets: [{{ data: {data}, backgroundColor: '#3b82f6', borderRadius: 6 }}] }},
            options: {{ plugins: {{ legend: {{ display: false }} }}, scales: {{ y: {{ beginAtZero: true, max: 100, ticks: {{ color: 'white' }} }} }} }}
        }});
    </script>
    """, height=200)

def telegram_edit(id_msg, txt):
    requests.post(f"https://api.telegram.org/bot{TOKEN}/editMessageText", data={"chat_id": CHAT_ID, "message_id": id_msg, "text": txt})

def renderizar_bloco(titulo):
    st.subheader(f"🏟️ {titulo}")
    
    # Inputs
    camp = st.text_input("Campeonato", key=f"c_{titulo}")
    casa = st.text_input("Casa", key=f"ca_{titulo}")
    vis = st.text_input("Visitante", key=f"v_{titulo}")
    
    if titulo == "JOGO_D":
        hora = st.text_input("Horário", key=f"h_{titulo}")
        linha = st.text_input("Linha Canto", key=f"lin_{titulo}")
        if st.button("📊 ANALISAR JOGO D", key=f"an_{titulo}"):
            st.session_state[f"ativo_{titulo}"] = True
            st.session_state[f"dados_{titulo}"] = {"camp": camp, "casa": casa, "vis": vis, "hora": hora, "linha": linha}
    else:
        lista = st.text_area("Lista de jogos", key=f"l_{titulo}")
        if st.button("📊 ANALISAR", key=f"an_{titulo}"):
            st.session_state[f"ativo_{titulo}"] = True
            st.session_state[f"dados_{titulo}"] = {"camp": camp, "casa": casa, "vis": vis}

    if st.session_state.get(f"ativo_{titulo}"):
        d = st.session_state[f"dados_{titulo}"]
        
        if titulo == "JOGO_D":
            st.write(f"💡 **Recomendação:** Over {d['linha']} (Cantos)")
            renderizar_grafico([82, 73, 61, 49], ['7.5', '8.5', '9.5', '10.5'], "Cantos")
            if st.button("🚀 ENVIAR ALERTA", key=f"en_{titulo}"):
                msg = f"🏆 {d['camp']}\n⚔️ {d['casa']} x {d['vis']}\n🎯 Mercado: Cantos (Over {d['linha']})\n🕒 {d['hora']}{RODAPE}"
                res = requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": msg}).json()
                st.session_state[f"id_{titulo}"] = res["result"]["message_id"]; st.session_state[f"msg_{titulo}"] = msg
            
            if f"id_{titulo}" in st.session_state:
                c1, c2, c3, c4 = st.columns(4)
                if c1.button("MOMENTO", key=f"m_{titulo}"): telegram_edit(st.session_state[f"id_{titulo}"], f"{st.session_state[f'msg_{titulo}'].replace(RODAPE, '')}\n---\n📊 Cantos: Em andamento\n{RODAPE}")
                if c2.button("HT", key=f"ht_{titulo}"): telegram_edit(st.session_state[f"id_{titulo}"], f"{st.session_state[f'msg_{titulo}'].replace(RODAPE, '')}\n---\n✅ GREEN HT ✅\n{RODAPE}")
                if c3.button("HT 2", key=f"ht2_{titulo}"): telegram_edit(st.session_state[f"id_{titulo}"], f"{st.session_state[f'msg_{titulo}'].replace(RODAPE, '')}\n---\n❌ RED HT ❌\n{RODAPE}")
                if c4.button("FINAL", key=f"fin_{titulo}"): telegram_edit(st.session_state[f"id_{titulo}"], f"{st.session_state[f'msg_{titulo}'].replace(RODAPE, '')}\n---\n✅ GREEN FINAL ✅\n{RODAPE}")

        else:
            st.write("🔥 **Mercado Pegando Fogo: 90%**")
            renderizar_grafico([90, 85, 70], ['O1.5', 'O2.5', 'BTTS'], "Gols")
            if st.button("🚀 ENVIAR ALERTA", key=f"en_{titulo}"):
                msg = f"🏆 {d['camp']}\n⚔️ {d['casa']} x {d['vis']}\n🎯 Mercado: Over Gols\n📈 Prob: 90%{RODAPE}"
                res = requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": msg}).json()
                st.session_state[f"id_{titulo}"] = res["result"]["message_id"]; st.session_state[f"msg_{titulo}"] = msg
            
            if f"id_{titulo}" in st.session_state:
                c1, c2, c3, c4 = st.columns(4)
                if c1.button("MOMENTO", key=f"m_{titulo}"): telegram_edit(st.session_state[f"id_{titulo}"], f"{st.session_state[f'msg_{titulo}'].replace(RODAPE, '')}\n---\n⚽ Momento: Ao Vivo\n{RODAPE}")
                if c2.button("HT", key=f"ht_{titulo}"): telegram_edit(st.session_state[f"id_{titulo}"], f"{st.session_state[f'msg_{titulo}'].replace(RODAPE, '')}\n---\n⚪ EM ANDAMENTO ⚪\n{RODAPE}")
                if c3.button("FINAL", key=f"f_{titulo}"): telegram_edit(st.session_state[f"id_{titulo}"], f"{st.session_state[f'msg_{titulo}'].replace(RODAPE, '')}\n---\n✅ GREEN GIGANTE ✅\n{RODAPE}")
                if c4.button("RED", key=f"r_{titulo}"): telegram_edit(st.session_state[f"id_{titulo}"], f"{st.session_state[f'msg_{titulo}'].replace(RODAPE, '')}\n---\n❌ RED ❌\n{RODAPE}")

col1, col2, col3, col4 = st.columns(4)
with col1: renderizar_bloco("JOGO_A")
with col2: renderizar_bloco("JOGO_B")
with col3: renderizar_bloco("JOGO_C")
with col4: renderizar_bloco("JOGO_D")
