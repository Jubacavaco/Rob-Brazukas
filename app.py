import streamlit as st
import requests
import re
import streamlit.components.v1 as components

st.set_page_config(layout="wide", page_title="Sistema Brazukas")
st.title("🤖 Sistema Brazukas Top Tips")

TOKEN = "8776214366:AAEQnGyhcEa6NQcYzyFAhtVDXKpQx5CoYT0"
CHAT_ID = "-1003925163611"
RODAPE = "\n\n🔞 Aposte com responsabilidade.\n⚠️ Não há garantias de lucro."

def renderizar_grafico(data, labels):
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
    """, height=220)

def renderizar_bloco(titulo):
    st.subheader(f"🏟️ {titulo}")
    with st.form(key=f"form_{titulo}"):
        camp = st.text_input("Campeonato")
        casa = st.text_input("Casa")
        vis = st.text_input("Visitante")
        
        if titulo == "JOGO_D":
            hora, cc, cv = st.text_input("Horário"), st.number_input("Cantos Casa"), st.number_input("Cantos Vis")
            ou, ent = st.selectbox("Selecione", ["Over", "Under"]), st.text_input("Entrada")
        else:
            lista = st.text_area("Lista de jogos")
        
        submit = st.form_submit_button("📊 ANALISAR")

    if submit:
        st.session_state[f"ativo_{titulo}"] = True
        st.session_state[f"dados_{titulo}"] = {"camp": camp, "casa": casa, "vis": vis}
        if titulo == "JOGO_D": st.session_state[f"dados_{titulo}"].update({"hora": hora, "cc": cc, "cv": cv, "ou": ou, "ent": ent})

    if st.session_state.get(f"ativo_{titulo}"):
        d = st.session_state[f"dados_{titulo}"]
        if titulo == "JOGO_D":
            st.write(f"💡 **Recomendação:** {d['ou']} {d['ent']}")
            renderizar_grafico([82, 73, 61, 49], ['7.5', '8.5', '9.5', '10.5'])
            if st.button("🚀 ENVIAR ALERTA", key=f"en_{titulo}"):
                msg = f"🚨🔥 ALERTA DE CANTOS 🔥🚨\n\n🏆 {d['camp']}\n⚔️ {d['casa']} x {d['vis']}\n🎯 Mercado: {d['ou']} {d['ent']}\n💎 Entrada: {d['ent']}\n🕒 {d['hora']} (BR){RODAPE}"
                res = requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": msg}).json()
                if res.get("ok"): st.session_state[f"id_{titulo}"] = res["result"]["message_id"]; st.session_state[f"msg_{titulo}"] = msg
            
            if f"id_{titulo}" in st.session_state:
                def ed(status):
                    info = f"\n\n--------------------\n🏠 Casa: {int(d['cc'])}\n✈️ Vis: {int(d['cv'])}\n📊 Total: {int(d['cc']+d['cv'])}"
                    txt = f"{st.session_state[f'msg_{titulo}'].replace(RODAPE, '')}{info}\n\n{status if status != 'INFO' else ''}{RODAPE}"
                    requests.post(f"https://api.telegram.org/bot{TOKEN}/editMessageText", data={"chat_id": CHAT_ID, "message_id": st.session_state[f'id_{titulo}'], "text": txt})
                c1, c2, c3, c4 = st.columns(4)
                if c1.button("MOMENTO", key=f"m_{titulo}"): ed("INFO")
                if c2.button("HT", key=f"ht_{titulo}"): ed("✅ GREEN HT ✅")
                if c3.button("HT 2", key=f"ht2_{titulo}"): ed("❌ RED HT ❌")
                if c4.button("FINAL", key=f"fin_{titulo}"): ed("✅ GREEN FINAL ✅")
        else:
            renderizar_grafico([90, 85, 70], ['O1.5', 'O2.5', 'BTTS'])
            if st.button("🚀 ENVIAR ALERTA", key=f"en_{titulo}"):
                msg = f"🚨 Alerta {titulo} 🚨\n\n🏆 {d['camp']}\n🆚 {d['casa']} x {d['vis']}\n📈 O1.5: 90% | O2.5: 85%{RODAPE}"
                res = requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": msg}).json()
                st.session_state[f"id_{titulo}"] = res["result"]["message_id"]; st.session_state[f"msg_{titulo}"] = msg
            
            if f"id_{titulo}" in st.session_state:
                def at(stts, inf):
                    txt = f"{st.session_state[f'msg_{titulo}'].replace(RODAPE, '')}\n\n⚽ {inf}\n\n🔄 {stts}{RODAPE}"
                    requests.post(f"https://api.telegram.org/bot{TOKEN}/editMessageText", data={"chat_id": CHAT_ID, "message_id": st.session_state[f"id_{titulo}"], "text": txt})
                c1, c2, c3, c4 = st.columns(4)
                if c1.button("MOMENTO", key=f"m_{titulo}"): at("✅ GREEN ✅", "Momento: Ao Vivo")
                if c2.button("HT", key=f"ht_{titulo}"): at("⚪ EM ANDAMENTO ⚪", "HT: Ok")
                if c3.button("FINAL", key=f"f_{titulo}"): at("✅ GREEN GIGANTE ✅", "Final: Green")
                if c4.button("RED", key=f"r_{titulo}"): at("❌ RED ❌", "Final: Red")

col1, col2, col3, col4 = st.columns(4)
with col1: renderizar_bloco("JOGO_A")
with col2: renderizar_bloco("JOGO_B")
with col3: renderizar_bloco("JOGO_C")
with col4: renderizar_bloco("JOGO_D")
