import streamlit as st
import requests
import streamlit.components.v1 as components

# Configurações
TOKEN = "8776214366:AAEQnGyhcEa6NQcYzyFAhtVDXKpQx5CoYT0"
CHAT_ID = "-1003925163611"

def renderizar_bloco(titulo):
    st.subheader(f"🏟️ {titulo}")
    camp = st.text_input("Campeonato", key=f"c_{titulo}")
    casa = st.text_input("Casa", key=f"ca_{titulo}")
    vis = st.text_input("Visitante", key=f"v_{titulo}")
    hora = st.text_input("Horário", key=f"h_{titulo}")
    
    # Novos Campos Solicitados
    media_time = st.text_input("Média Time", key=f"mt_{titulo}")
    media_liga = st.text_input("Média Liga", key=f"ml_{titulo}")
    
    cc = st.number_input("Cantos Casa", key=f"cc_{titulo}")
    cv = st.number_input("Cantos Vis", key=f"cv_{titulo}")
    
    over_under = st.selectbox("Selecione", ["Over", "Under"], key=f"ou_{titulo}")
    entrada = st.text_input("Linha (Ex: 8.5)", key=f"e_{titulo}")
    odd = st.text_input("Odd", key=f"o_{titulo}")
    
    total = int(cc + cv)
    
    # Formato do Mercado solicitado: "Cantos Asiáticos (Over/Under)"
    mercado_texto = f"Cantos Asiáticos ({over_under} {entrada})"

    msg_base = (f"🚨🔥 ALERTA DE CANTOS 🔥🚨\n\n"
                f"🏆 Campeonato: {camp}\n"
                f"⚔️ Confronto: {casa} x {vis}\n"
                f"🎯 Mercado: {mercado_texto}\n"
                f"💎 Entrada: {entrada}\n"
                f"💰 Odd: {odd}\n"
                f"📈 Média Time: {media_time} | Média Liga: {media_liga}\n"
                f"🕒 Horário: {hora} (BR)")

    if st.button("🚀 ENVIAR ALERTA", key=f"en_{titulo}"):
        res = requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": msg_base}).json()
        if res.get("ok"):
            st.session_state[f"id_{titulo}"] = res["result"]["message_id"]
            st.session_state[f"msg_{titulo}"] = msg_base
            st.success("Enviado!")

    if f"id_{titulo}" in st.session_state:
        def editar(status, extra=""):
            new_text = (f"{st.session_state[f'msg_{titulo}']}\n\n"
                        f"🏠 Cantos Casa: {cc}\n"
                        f"✈️ Cantos Visitante: {cv}\n"
                        f"📊 Total de Cantos: {total}\n\n"
                        f"{status}\n{extra}")
            requests.post(f"https://api.telegram.org/bot{TOKEN}/editMessageText", 
                          data={"chat_id": CHAT_ID, "message_id": st.session_state[f"id_{titulo}"], "text": new_text})

        c1, c2, c3, c4 = st.columns(4)
        if c1.button("MOMENTO", key=f"mom_{titulo}"): editar("✅ GREEN ✅")
        if c2.button("HT", key=f"ht_{titulo}"): editar("✅ GREEN HT ✅")
        if c3.button("HT 2", key=f"ht2_{titulo}"): editar("❌ RED HT ❌")
        if c4.button("FINAL", key=f"fin_{titulo}"): editar("✅ GREEN FINAL ✅")
        
        c5, c6 = st.columns(2)
        if c5.button("PUSH", key=f"p1_{titulo}"): editar("🔄 APOSTA DEVOLVIDA (PUSH) 🔄")
        if c6.button("PUSH 2", key=f"p2_{titulo}"): editar("🔄 APOSTA DEVOLVIDA NO HT (PUSH) 🔄")

    # Gráfico JOGO_D
    if titulo == "JOGO_D":
        st.subheader("📊 Probabilidade Escanteios")
        components.html("""
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <canvas id="cornersChart"></canvas>
        <script>
        const ctx = document.getElementById('cornersChart');
        new Chart(ctx, {type: 'bar', data: {labels: ['O 7.5', 'O 8.5', 'O 9.5', 'O 10.5'], datasets: [{data: [82,73,61,49], backgroundColor: ['#22c55e', '#3b82f6', '#f59e0b', '#ef4444']}]}, options: {scales: {y: {beginAtZero: true, max: 100, ticks: {color: 'white'}}, x: {ticks: {color: 'white'}}}}});
        </script>
        """, height=300)

col1, col2, col3, col4 = st.columns(4)
with col1: renderizar_bloco("JOGO_A")
with col2: renderizar_bloco("JOGO_B")
with col3: renderizar_bloco("JOGO_C")
with col4: renderizar_bloco("JOGO_D")
