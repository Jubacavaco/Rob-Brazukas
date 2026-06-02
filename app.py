import streamlit as st
import requests
import re
import streamlit.components.v1 as components

st.set_page_config(layout="wide", page_title="Sistema Brazukas")
st.title("🤖 Sistema Brazukas Top Tips")

TOKEN = "8776214366:AAEQnGyhcEa6NQcYzyFAhtVDXKpQx5CoYT0"
CHAT_ID = "-1003925163611"

def calcular_probabilidade(texto):
    numeros = re.findall(r'\b\d+\b', texto)
    gols = [int(n) for n in numeros if int(n) <= 10]
    over15 = over25 = btts = ltd = 0
    v_casa = v_vis = empate = total = 0
    i = 0
    while i < len(gols) - 1:
        g1, g2 = gols[i], gols[i+1]
        total += 1
        if (g1 + g2) >= 2: over15 += 1
        if (g1 + g2) >= 3: over25 += 1
        if g1 > 0 and g2 > 0: btts += 1
        if g1 != g2: ltd += 1
        if g1 > g2: v_casa += 1
        elif g2 > g1: v_vis += 1
        else: empate += 1
        i += 2
    if total == 0: return 0, 0, 0, 0, 0, 0, 0
    p15 = min(round(((over15/total)*100)+5, 1), 95)
    p25 = min(round(((over25/total)*100)+5, 1), 90)
    pb = min(round((btts/total)*100, 1), 85)
    pl = min(round((ltd/total)*100, 1), 95)
    return round((v_casa/total)*100, 1), round((v_vis/total)*100, 1), round((empate/total)*100, 1), p15, p25, pb, pl

def renderizar_bloco(titulo):
    st.subheader(f"🏟️ {titulo}")
    if titulo == "JOGO_D":
        camp = st.text_input("Campeonato", key=f"c_{titulo}")
        casa = st.text_input("Casa", key=f"ca_{titulo}")
        vis = st.text_input("Visitante", key=f"v_{titulo}")
        hora = st.text_input("Horário", key=f"h_{titulo}")
        media_time = st.number_input("Média Time (C+V)", key=f"mt_{titulo}")
        media_liga = st.number_input("Média Liga", key=f"ml_{titulo}")
        cc = st.number_input("Cantos Casa", key=f"cc_{titulo}")
        cv = st.number_input("Cantos Vis", key=f"cv_{titulo}")
        ou = st.selectbox("Selecione", ["Over", "Under"], key=f"ou_{titulo}")
        entrada = st.text_input("Linha (Ex: 8.5)", key=f"e_{titulo}")
        if st.button("📊 ANALISAR", key=f"an_{titulo}"):
            media_final = (media_time + media_liga) / 2
            def calc_prob(limite): return int(max(min(100 - (limite - media_final) * 12, 95), 5))
            p75, p85, p95, p105 = calc_prob(7.5), calc_prob(8.5), calc_prob(9.5), calc_prob(10.5)
            st.session_state[f"analise_{titulo}"] = True
            components.html(f"""<script src="https://cdn.jsdelivr.net/npm/chart.js"></script><div style="width:100%; background:#1e293b; padding:15px; border-radius:15px;"><canvas id="cChart"></canvas></div><script>new Chart(document.getElementById('cChart'), {{type: 'bar', data: {{labels: ['7.5', '8.5', '9.5', '10.5'], datasets: [{{data: [{p75}, {p85}, {p95}, {p105}], backgroundColor: ['#22c55e', '#3b82f6', '#f59e0b', '#ef4444'], borderRadius: 8}}]}}, options: {{plugins: {{legend: {{display: false}}}}, scales: {{y: {{beginAtZero: true, max: 100, ticks: {{color: 'white'}}}}, x: {{ticks: {{color: 'white'}}}}}} }}});</script>""", height=300)
        if st.session_state.get(f"analise_{titulo}"):
            msg_base = f"🚨🔥 ALERTA DE CANTOS 🔥🚨\n\n🏆 Campeonato: {camp}\n⚔️ Confronto: {casa} x {vis}\n🎯 Mercado: Cantos Asiáticos ({ou} {entrada})\n💎 Entrada: {entrada}\n🕒 Horário: {hora} (BR)"
            if st.button("🚀 ENVIAR ALERTA", key=f"en_{titulo}"):
                res = requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": msg_base}).json()
                if res.get("ok"): st.session_state[f"id_{titulo}"] = res["result"]["message_id"]; st.session_state[f"msg_{titulo}"] = msg_base
        if f"id_{titulo}" in st.session_state:
            def editar(status):
                new = f"{st.session_state[f'msg_{titulo}']}\n\n🏠 Cantos Casa: {int(st.session_state[f'cc_{titulo}'])}\n✈️ Cantos Visitante: {int(st.session_state[f'cv_{titulo}'])}\n📊 Total: {int(st.session_state[f'cc_{titulo}'] + st.session_state[f'cv_{titulo}'])}\n\n{status}"
                requests.post(f"https://api.telegram.org/bot{TOKEN}/editMessageText", data={"chat_id": CHAT_ID, "message_id": st.session_state[f"id_{titulo}"], "text": new})
            c1, c2, c3, c4 = st.columns(4)
            if c1.button("MOMENTO", key=f"mom_{titulo}"): editar("✅ GREEN ✅")
            if c2.button("HT", key=f"ht_{titulo}"): editar("✅ GREEN HT ✅")
            if c3.button("HT 2", key=f"ht2_{titulo}"): editar("❌ RED HT ❌")
            if c4.button("FINAL", key=f"fin_{titulo}"): editar("✅ GREEN FINAL ✅")
    else:
        camp, casa, vis = st.text_input("Campeonato", key=f"c_{titulo}"), st.text_input("Casa", key=f"ca_{titulo}"), st.text_input("Visitante", key=f"v_{titulo}")
        prob, hora, pm = st.text_input("Probabilidade", key=f"pb_{titulo}"), st.text_input("Horário", key=f"h_{titulo}"), st.text_input("Momento", key=f"pm_{titulo}")
        pht, pf, lista = st.text_input("HT", key=f"pht_{titulo}"), st.text_input("Final", key=f"pf_{titulo}"), st.text_area("Lista de jogos", key=f"l_{titulo}")
        if st.button("Analisar", key=f"an_{titulo}"): st.session_state[f"res_{titulo}"] = calcular_probabilidade(lista)
        if f"res_{titulo}" in st.session_state:
            tipo = st.selectbox("Mercado", ["Over 2.5 FT", "Over 1.5 FT", "BTTS", "LTD"], key=f"sel_{titulo}")
            msg = f"🚨 Alerta 🚨\n🏆 {camp}\n🆚 {casa} x {vis}\n🎯 {tipo}\n📈 {prob}%\n⏰ {hora}"
            if st.button("🚀 ENVIAR", key=f"en_{titulo}"):
                res = requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": msg}).json()
                st.session_state[f"id_{titulo}"] = res["result"]["message_id"]; st.session_state[f"msg_{titulo}"] = msg
        if f"id_{titulo}" in st.session_state:
            def at(stts, inf):
                txt = f"{st.session_state[f'msg_{titulo}']}\n\n⚽ {inf}\n\n🔄 {stts}"
                requests.post(f"https://api.telegram.org/bot{TOKEN}/editMessageText", data={"chat_id": CHAT_ID, "message_id": st.session_state[f"id_{titulo}"], "text": txt})
            c1, c2, c3, c4 = st.columns(4)
            if c1.button("MOMENTO", key=f"m_{titulo}"): at("✅ GREEN ✅", f"Momento: {pm}")
            if c2.button("HT", key=f"ht_{titulo}"): at("⚪ EM ANDAMENTO ⚪", f"HT: {pht}")
            if c3.button("FINAL", key=f"f_{titulo}"): at("✅ GREEN GIGANTE ✅", f"HT: {pht} | Final: {pf}")
            if c4.button("RED", key=f"r_{titulo}"): at("❌ RED ❌", f"HT: {pht} | Final: {pf}")

col1, col2, col3, col4 = st.columns(4)
with col1: renderizar_bloco("JOGO_A")
with col2: renderizar_bloco("JOGO_B")
with col3: renderizar_bloco("JOGO_C")
with col4: renderizar_bloco("JOGO_D")
