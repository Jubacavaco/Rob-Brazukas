import streamlit as st
import requests
import re

# Configuração simples
st.set_page_config(layout="wide")
st.title("🤖 Painel Brazukas - Gestão Total")

# Sidebar
st.sidebar.header("⚙️ Configurações")
token = st.sidebar.text_input("Token Telegram", type="password")
chat_id = st.sidebar.text_input("ID Canal", type="password")

def calcular_probabilidade(texto):
    numeros = re.findall(r'\d+', texto)
    gols = [int(n) for n in numeros if int(n) <= 10]
    if len(gols) < 2: return 0
    media = sum(gols) / len(gols)
    return min(media * 35, 100)

def renderizar_bloco(titulo):
    with st.container(border=True):
        st.subheader(f"🏟️ {titulo}")
        
        # Inputs
        col_c1, col_c2 = st.columns(2)
        camp = col_c1.text_input(f"Campeonato", key=f"c_{titulo}")
        hora = col_c2.text_input(f"Horário", key=f"h_{titulo}")
        casa = st.text_input(f"Casa", key=f"ca_{titulo}")
        vis = st.text_input(f"Visitante", key=f"v_{titulo}")
        lista = st.text_area(f"Lista de jogos", key=f"l_{titulo}", height=100)
        
        if st.button(f"Analisar {titulo}", key=f"an_{titulo}"):
            st.session_state[f"prob_{titulo}"] = calcular_probabilidade(lista)
            st.rerun()
        
        if f"prob_{titulo}" in st.session_state:
            p_base = st.session_state[f"prob_{titulo}"]
            p_manual = st.text_input("Probabilidade (%)", value=f"{p_base:.1f}", key=f"ajuste_{titulo}")
            p = float(p_manual) if p_manual else p_base
            
            st.write(f"📊 **Over 2.5 FT:** {min(p, 100):.0f}%")
            st.progress(min(p/100, 1.0))
            
            mercado = st.selectbox(f"Mercado ({titulo})", ["Automático", "Over 1.5 FT", "Over 2.5 FT", "Ambas Marcam (BTTS)", "LTD"], key=f"sel_{titulo}")
            tipo = mercado if mercado != "Automático" else ("Over 1.5 FT" if p >= 70 else "LTD")
            
            msg = f"🚨 *Alerta* 🚨\n🏆 {camp}\n🆚 {casa} x {vis}\n🎯 {tipo}\n📈 {p:.1f}%\n⏰ {hora}"
            st.info(msg)
            
            if st.button(f"🚀 ENVIAR {titulo}", key=f"en_{titulo}"):
                if token and chat_id:
                    requests.post(f"https://api.telegram.org/bot{token}/sendMessage", data={"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"})
                    st.success("Enviado!")
                else:
                    st.error("Configura Token/ID!")

col1, col2 = st.columns(2)
with col1: renderizar_bloco("JOGO_A")
with col2: renderizar_bloco("JOGO_B")
