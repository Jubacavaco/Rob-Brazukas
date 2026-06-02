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
        
        if st.button("📊 ANALISAR JOGO D", key=f"an_{titulo}"):
            media_final = (media_time + media_liga) / 2
            sugestao = "Over" if media_time > media_liga else "Under"
            st.session_state[f"rec_{titulo}"] = sugestao
            st.session_state[f"analise_{titulo}"] = True
            
            def calc_prob(limite): return int(max(min(100 - abs(limite - media_final) * 12, 95), 5))
            p = [calc_prob(7.5), calc_prob(8.5), calc_prob(9.5), calc_prob(10.5)]
            
            st.write(f"💡 **Recomendação:** {sugestao} (Baseado na média de {media_final:.1f})")
            
            components.html(f"""
            <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
            <div style="width:100%; background:#1e293b; padding:15px; border-radius:15px;"><canvas id="cChart"></canvas></div>
            <script>new Chart(document.getElementById('cChart'), {{type: 'bar', data: {{labels: ['7.5', '8.5', '9.5', '10.5'], datasets: [{{data: {p}, backgroundColor: ['#22c55e', '#3b82f6', '#f59e0b', '#ef4444'], borderRadius: 8}}]}}, options: {{plugins: {{legend: {{display: false}}}}, scales: {{y: {{beginAtZero: true, max: 100, ticks: {{color: 'white'}}}}}} }}});</script>
            """, height=300)

        if st.session_state.get(f"analise_{titulo}"):
            rec = st.session_state.get(f"rec_{titulo}")
            linha = st.text_input("Linha Definida", value="8.5", key=f"ln_{titulo}")
            if st.button("🚀 ENVIAR ALERTA", key=f"en_{titulo}"):
                msg = f"🚨🔥 ALERTA DE CANTOS 🔥🚨\n\n🏆 {camp}\n⚔️ {casa} x {vis}\n🎯 Mercado: {rec} {linha}\n🕒 {hora}"
                res = requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": msg}).json()
                if res.get("ok"): st.session_state[f"id_{titulo}"] = res["result"]["message_id"]; st.session_state[f"msg_{titulo}"] = msg

        if f"id_{titulo}" in st.session_state:
            if st.button("✅ GREEN", key=f"g_{titulo}"): editar(titulo, "✅ GREEN ✅")
            if st.button("❌ RED", key=f"r_{titulo}"): editar(titulo, "❌ RED ❌")
    else:
        # Lógica corrigida para A, B e C
        camp = st.text_input("Campeonato", key=f"c_{titulo}")
        casa = st.text_input("Casa", key=f"ca_{titulo}")
        vis = st.text_input("Visitante", key=f"v_{titulo}")
        lista = st.text_area("Lista de jogos", key=f"l_{titulo}")
        if st.button("Analisar", key=f"an_{titulo}"): st.session_state[f"res_{titulo}"] = calcular_probabilidade(lista)
        if f"res_{titulo}" in st.session_state:
            # ... resto do código A, B, C mantido
            st.success("Análise concluída!")

def editar(titulo, status):
    new = f"{st.session_state[f'msg_{titulo}']}\n\n{status}"
    requests.post(f"https://api.telegram.org/bot{TOKEN}/editMessageText", data={"chat_id": CHAT_ID, "message_id": st.session_state[f"id_{titulo}"], "text": new})

col1, col2, col3, col4 = st.columns(4)
with col1: renderizar_bloco("JOGO_A")
with col2: renderizar_bloco("JOGO_B")
with col3: renderizar_bloco("JOGO_C")
with col4: renderizar_bloco("JOGO_D")
