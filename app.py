import streamlit as st
import requests
import re

st.set_page_config(layout="wide")
st.title("🤖 Painel Brazukas - Gestão Total")

# Sidebar para credenciais
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
        st.session_state[f"prob_{titulo}"] = calcular_probabilidade(lista)
    
    if f"prob_{titulo}" in st.session_state:
        p = st.session_state[f"prob_{titulo}"]
        st.write(f"📈 **Probabilidade:** {p:.1f}%")
        
        # Gráficos Visuais
        st.write("📊 **Mercados:**")
        st.progress(min((p+5)/100, 1.0)); st.write(f"Over 1.5 ({min(p+5, 100)}%)")
        st.progress(min(p/100, 1.0)); st.write(f"Over 2.5 ({min(p, 100)}%)")
        
        # Seleção de Mercado
        mercado = st.selectbox(f"Mercado ({titulo})", ["Automático", "Over 1.5 FT", "Over 2.5 FT", "Ambas Marcam (BTTS)", "LTD"], key=f"sel_{titulo}")
        
        # Lógica de definição
        tipo = mercado if mercado != "Automático" else ("Over 1.5 FT" if p >= 70 else "LTD")
        
        msg = f"🚨 *Alerta de Entrada* 🚨\n\n🏆 *Campeonato:* {camp}\n🆚 *Jogo:* {casa} x {vis}\n🎯 *Mercado:* {tipo}\n⏰ *Horário:* {hora}\n\n⚠️ Aposte com responsabilidade."
        st.info(msg)
        st.session_state[f"msg_{titulo}"] = msg
        
        if st.button(f"🚀 ENVIAR {titulo}", key=f"en_{titulo}"):
            payload = {"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"}
            r = requests.post(f"https://api.telegram.org/bot{token}/sendMessage", data=payload).json()
            if r.get("ok"): 
                st.session_state[f"id_{titulo}"] = r["result"]["message_id"]
                st.rerun()

    # Botões de Controle (Green, Red, Devolvida)
    if f"id_{titulo}" in st.session_state:
        st.write("---")
        c1, c2, c3 = st.columns(3)
