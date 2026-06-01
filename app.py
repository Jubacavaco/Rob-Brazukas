import streamlit as st
import requests
import re

st.set_page_config(page_title="Robô Brazukas Dual", layout="wide")
st.title("🤖 Painel Brazukas - Gestão Dual Completa")

# --- SIDEBAR ---
token = st.sidebar.text_input("Token Telegram", type="password")
chat_id = st.sidebar.text_input("ID Canal", type="password")

# --- FUNÇÕES ---
def calcular_probabilidade(texto):
    numeros = re.findall(r'\d+', texto)
    gols = [int(n) for n in numeros if int(n) <= 10]
    if len(gols) < 2: return 0
    media = sum(gols) / len(gols)
    return min(media * 35, 100)

def gerar_mensagem(tipo, camp, casa, vis, hora):
    return f"🚨 *Alerta de Entrada* 🚨\n\n🏆 *Campeonato:* {camp}\n🆚 *Jogo:* {casa} x {vis}\n🎯 *Mercado:* {tipo}\n⏰ *Horário:* {hora}\n\n⚠️ Aposte com responsabilidade."

# --- BLOCO PRINCIPAL ---
def renderizar_bloco(titulo):
    st.subheader(f"🏟️ {titulo}")
    camp = st.text_input(f"Campeonato ({titulo})", key=f"c_{titulo}")
    casa = st.text_input(f"Casa ({titulo})", key=f"ca_{titulo}")
    vis = st.text_input(f"Visitante ({titulo})", key=f"v_{titulo}")
    hora = st.text_input(f"Horário ({titulo})", key=f"h_{titulo}")
    lista = st.text_area(f"Lista de Jogos ({titulo})", key=f"l_{titulo}")
    
    if st.button(f"📊 Analisar {titulo}", key=f"btn_an_{titulo}"):
        prob = calcular_probabilidade(lista)
        st.session_state[f"prob_{titulo}"] = prob
        st.write(f"📈 **Probabilidade:** {prob:.1f}%")
        st.progress(min(prob/100, 1.0))
        
        if prob >= 65: tipo = "Over 2.5 FT"
        elif prob >= 70: tipo = "Over 1.5 FT"
        elif prob >= 55: tipo = "BTTS"
        elif prob >= 51: tipo = "LTD"
        else: tipo = None
        
        if tipo:
            msg = gerar_mensagem(tipo, camp, casa, vis, hora)
            st.info(msg)
            st.session_state[f"msg_{titulo}"] = msg
        else:
            st.warning("Probabilidade insuficiente.")

    if f"msg_{titulo}" in st.session_state:
        if st.button(f"🚀 Enviar {titulo}", key=f"btn_env_{titulo}"):
            payload = {"chat_id": chat_id, "text": st.session_state[f"msg_{titulo}"], "parse_mode": "Markdown"}
            resp = requests.post(f"https://api.telegram.org/bot{token}/sendMessage", data=payload).json()
            if resp.get("ok"):
                st.session_state[f"id_{titulo}"] = resp["result"]["message_id"]
                st.success("Sinal enviado!")

    if f"id_{titulo}" in st.session_state:
        st.write("---")
        c1, c2, c3 = st.columns(3)
        if c1.button("✅ GREEN", key=f"g_{titulo}"):
            payload = {"chat_id": chat_id, "message_id": st.session_state[f"id_{titulo}"], "text": st.session_state[f"msg_{titulo}"] + "\n\n🔄 *Status:* ✅ GREEN!!", "parse_mode": "Markdown"}
            requests.post(f"https://api.telegram.org/bot{token}/editMessageText", data=payload)
        if c2.button("
