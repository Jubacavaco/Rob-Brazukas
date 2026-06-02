import streamlit as st
import requests
import re
import streamlit.components.v1 as components
import math

# (Mantenha o resto do código igual até chegar na função renderizar_bloco)

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
            # Cálculo simples de probabilidade baseado na média
            media_final = (media_time + media_liga) / 2
            def calc_prob(limite): return int(max(min(100 - (limite - media_final) * 12, 95), 5))
            p75, p85, p95, p105 = calc_prob(7.5), calc_prob(8.5), calc_prob(9.5), calc_prob(10.5)
            
            st.session_state[f"analise_{titulo}"] = True
            
            # Gráfico Formato Bonito
            html_grafico = f"""
            <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
            <div style="width:100%; background:#1e293b; padding:15px; border-radius:15px;">
                <canvas id="cChart"></canvas>
            </div>
            <script>
            new Chart(document.getElementById('cChart'), {{
                type: 'bar',
                data: {{
                    labels: ['7.5', '8.5', '9.5', '10.5'],
                    datasets: [{{
                        label: 'Probabilidade %',
                        data: [{p75}, {p85}, {p95}, {p105}],
                        backgroundColor: ['#22c55e', '#3b82f6', '#f59e0b', '#ef4444'],
                        borderRadius: 8
                    }}]
                }},
                options: {{ plugins: {{ legend: {{ display: false }} }}, scales: {{ y: {{ beginAtZero: true, max: 100, ticks: {{ color: 'white' }} }}, x: {{ ticks: {{ color: 'white' }} }} }} }}
            }});
            </script>
            """
            components.html(html_grafico, height=300)

        if st.session_state.get(f"analise_{titulo}"):
            msg_base = f"🚨🔥 ALERTA DE CANTOS 🔥🚨\n\n🏆 Campeonato: {camp}\n⚔️ Confronto: {casa} x {vis}\n🎯 Mercado: Cantos Asiáticos ({ou} {entrada})\n💎 Entrada: {entrada}\n🕒 Horário: {hora} (BR)"
            if st.button("🚀 ENVIAR ALERTA", key=f"en_{titulo}"):
                res = requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": msg_base}).json()
                if res.get("ok"):
                    st.session_state[f"id_{titulo}"] = res["result"]["message_id"]
                    st.session_state[f"msg_{titulo}"] = msg_base
        
        # ... (seu código de botões MOMENTO/HT/FINAL igual ao anterior) ...

    else:
        # ... (seu código original de A, B e C) ...
