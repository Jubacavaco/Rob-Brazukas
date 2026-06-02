import streamlit as st
import requests
import re
import streamlit.components.v1 as components

# ... (código anterior mantido) ...

def renderizar_bloco(titulo):
    st.subheader(f"🏟️ {titulo}")
    
    # Lógica JOGO_D
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
            st.session_state[f"analise_{titulo}"] = True
            st.success(f"Análise: Comparando {media_time} com média da liga {media_liga}")
            # Inserir aqui o Gráfico baseado nos dados
            components.html(f"""
            <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
            <canvas id="cChart" height="150"></canvas>
            <script>
            new Chart(document.getElementById('cChart'), {{
                type: 'bar', 
                data: {{labels: ['Time', 'Liga'], datasets: [{{data: [{media_time}, {media_liga}], backgroundColor: ['#22c55e', '#3b82f6']}}]}}
            }});
            </script>
            """, height=200)

        if st.session_state.get(f"analise_{titulo}"):
            msg_base = (f"🚨🔥 ALERTA DE CANTOS 🔥🚨\n\n🏆 Campeonato: {camp}\n⚔️ Confronto: {casa} x {vis}\n"
                        f"🎯 Mercado: Cantos Asiáticos ({ou} {entrada})\n💎 Entrada: {entrada}\n"
                        f"🕒 Horário: {hora} (BR)")
            
            if st.button("🚀 ENVIAR ALERTA", key=f"en_{titulo}"):
                res = requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": msg_base}).json()
                if res.get("ok"):
                    st.session_state[f"id_{titulo}"] = res["result"]["message_id"]
                    st.session_state[f"msg_{titulo}"] = msg_base

    else:
        # Lógica original A, B, C (mantida igual)
        # ... (seu código original de A, B, C aqui) ...
