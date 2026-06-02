import streamlit as st
import requests

st.set_page_config(layout="wide", page_title="Sistema Brazukas")
st.title("🤖 Sistema Brazukas Pro")

TOKEN = "8776214366:AAEQnGyhcEa6NQcYzyFAhtVDXKpQx5CoYT0"
CHAT_ID = "-1003925163611"

def telegram(msg, msg_id=None):
    url = f"https://api.telegram.org/bot{TOKEN}/"
    try:
        if msg_id:
            requests.post(url + "editMessageText", json={"chat_id": CHAT_ID, "message_id": msg_id, "text": msg})
        else:
            resp = requests.post(url + "sendMessage", json={"chat_id": CHAT_ID, "text": msg}).json()
            return resp.get("result", {}).get("message_id")
    except: return None

def jogo_normal(nome):
    st.subheader(f"🏟️ {nome}")
    # Todas as caixas de entrada restauradas
    camp = st.text_input("Campeonato", key=f"camp_{nome}")
    casa = st.text_input("Casa", key=f"casa_{nome}")
    vis = st.text_input("Visitante", key=f"vis_{nome}")
    horario = st.text_input("Horário", key=f"hor_{nome}")
    prob = st.number_input("Probabilidade (%)", 0, 100, 70, key=f"prob_{nome}")
    ht = st.text_input("Placar HT", key=f"ht_{nome}")
    ft = st.text_input("Placar FT", key=f"ft_{nome}")
    lista = st.text_area("Lista de Análise", key=f"lista_{nome}")
    
    # Botão Analisar
    if st.button("📊 ANALISAR", key=f"ana_{nome}"):
        st.session_state[f"analise_{nome}"] = True
        # Calculo fictício baseado no tamanho da lista para variar os resultados
        n = len(lista)
        st.session_state[f"probs_{nome}"] = {"O 1.5": 50+n, "O 2.5": 40+n, "BTTS": 30+n, "LTD": 20+n}

    # Verifica se a análise foi feita para mostrar o gráfico e botões
    if st.session_state.get(f"analise_{nome}", False):
        p = st.session_state.get(f"probs_{nome}")
        st.bar_chart(p)
        
        if st.button("🚀 ENVIAR ALERTA", key=f"env_{nome}"):
            msg = f"🚨 Alerta 🚨\n\n🏆 {camp}\n🆚 {casa} x {vis}\n📈 Prob: {prob}%\n⏰ {horario}"
            st.session_state[f"mid_{nome}"] = telegram(msg)

        mid = st.session_state.get(f"mid_{nome}")
        if mid:
            base = f"🚨 Alerta 🚨\n\n🏆 {camp}\n🆚 {casa} x {vis}\n⏰ {horario}"
            c1, c2 = st.columns(2)
            if c1.button("⏱️ MOMENTO", key=f"mom_{nome}"): telegram(f"{base}\nHT: ({ht})\n\n⚪ Em Andamento", mid)
            if c1.button("✅ HT", key=f"htg_{nome}"): telegram(f"{base}\nHT: ({ht})\n✅✅✅", mid)
            if c2.button("🏆 FINAL", key=f"fng_{nome}"): telegram(f"{base}\nHT: ({ht})\nFT: ({ft})\n🏆🏆🏆", mid)
            if c2.button("❌ RED", key=f"red_{nome}"): telegram(f"{base}\nHT: ({ht})\nFT: ({ft})\n❌❌❌", mid)

# Colunas para os 4 jogos
col1, col2, col3, col4 = st.columns(4)
with col1: jogo_normal("JOGO_A")
with col2: jogo_normal("JOGO_B")
with col3: jogo_normal("JOGO_C")
with col4: jogo_normal("JOGO_D")
