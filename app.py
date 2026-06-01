import streamlit as st
import requests
import re

st.set_page_config(layout="wide")
st.title("🤖 Painel Brazukas - Gestão Completa")

# Sidebar
token = st.sidebar.text_input("Token Telegram", type="password")
chat_id = st.sidebar.text_input("ID Canal", type="password")

def calcular_probabilidade(texto):
    numeros = re.findall(r'\d+', texto)
    gols = [int(n) for n in numeros if int(n) <= 10]
    if len(gols) < 2: return 0
    media = sum(gols) / len(gols)
    return min(media * 35, 100)

def renderizar_bloco(titulo):
    st.subheader(f"🏟️ {titulo}")
    camp = st.text_input(f"Campeonato ({titulo})", key=f"c_{titulo}")
    casa = st.text_input(f"Casa ({titulo})", key=f"ca_{titulo}")
    vis = st.text_input(f"Visitante ({titulo})", key=f"v_{titulo}")
    hora = st.text_input(f"Horário ({titulo})", key=f"h_{titulo}")
    lista = st.text_area(f"Lista de jogos ({titulo})", key=f"l_{titulo}")
    
    if st.button(f"Analisar {titulo}", key=f"an_{titulo}"):
        p = calcular_probabilidade(lista)
        st.session_state[f"prob_{titulo}"] = p
        st.write(f"📈 **Probabilidade:** {p:.1f}%")
        
        # Gráficos de cada mercado
        st.caption("Visualização de Mercados:")
        st.write("Over 1.5 FT")
        st.progress(min((p+5)/100, 1.0))
        st.write("Over 2.5 FT")
        st.progress(min(p/100, 1.0))
        st.write("Ambas (BTTS)")
        st.progress(min((p-10)/100, 1.0))
        st.write("LTD")
        st.progress(min((p-15)/100, 1.0))
        
        # Lógica de seleção
        tipo = "LTD" if p >= 51 else None
        if p >= 55: tipo = "BTTS"
        if p >= 70: tipo = "Over 1.5 FT"
        if p >= 65: tipo = "Over 2.5 FT"
        
        if tipo:
            msg = f"🚨 *Alerta de Entrada* 🚨\n\n🏆 *Campeonato:* {camp}\n🆚 *Jogo:* {casa} x {vis}\n🎯 *Mercado:* {tipo}\n⏰ *Horário:* {hora}\n\n📌 Confiança: {p:.1f}%\n⚠️ Aposte com responsabilidade."
            st.info(msg)
            st.session_state[f"msg_{titulo}"] = msg
            
    if f"msg_{titulo}" in st.session_state:
        if st.button(f"🚀 Enviar {titulo}", key=f"en_{titulo}"):
            payload = {"chat_id": chat_id, "text": st.session_state[f"msg_{titulo}"], "parse_mode": "Markdown"}
            r = requests.post(f"https://api.telegram.org/bot{token}/sendMessage", data=payload).json()
            if r.get("ok"): 
                st.session_state[f"id_{titulo}"] = r["result"]["message_id"]
                st.rerun()

    if f"id_{titulo}" in st.session_state:
        st.write("---")
        c1, c2, c3 = st.columns(3)
        def registrar(status):
            msg_final = st.session_state[f"msg_{titulo}"] + f"\n\n🔄 *Status:* {status}"
            payload = {"chat_id": chat_id, "message_id": st.session_state[f"id_{titulo}"], "text": msg_final, "parse_mode": "Markdown"}
            requests.post(f"https://api.telegram.org/bot{token}/editMessageText", data=payload)
            st.rerun()

        if c1.button("✅ GREEN", key=f"g_{titulo}"): registrar("✅ GREEN!!")
        if c2.button("❌ RED", key=f"r_{titulo}"): registrar("❌ RED!")
        if c3.button("🔄 DEV", key=f"d_{titulo}"): registrar("🔄 DEVOLVIDA")

col1, col2 = st.columns(2)
with col1: renderizar_bloco("JOGO_A")
with col2: renderizar_bloco("JOGO_B")
