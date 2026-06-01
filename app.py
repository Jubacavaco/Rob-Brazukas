import streamlit as st
import requests
import re

# Configuração da página
st.set_page_config(layout="wide", page_title="Sistema Brazukas Top Tips")
st.title("🤖 Sistema Brazukas Top Tips")

# Carrega do Secrets
try:
    TOKEN = st.secrets["token"]
    CHAT_ID = st.secrets["chat_id"]
except Exception:
    st.error("Configurações não encontradas no Secrets. Configure em Settings > Secrets.")
    st.stop()

def calcular_probabilidade(texto):
    numeros = re.findall(r'\d+', texto)
    gols = [int(n) for n in numeros if int(n) <= 10]
    if len(gols) < 2: return 0
    media = sum(gols) / len(gols)
    return min(media * 20, 100)

def renderizar_bloco(titulo):
    with st.container(border=True):
        st.subheader(f"🏟️ {titulo}")
        camp = st.text_input("Campeonato", key=f"c_{titulo}")
        hora = st.text_input("Horário", key=f"h_{titulo}")
        casa = st.text_input("Casa", key=f"ca_{titulo}")
        vis = st.text_input("Visitante", key=f"v_{titulo}")
        lista = st.text_area("Lista de jogos", key=f"l_{titulo}")
        
        if st.button(f"Analisar {titulo}", key=f"an_{titulo}"):
            st.session_state[f"prob_{titulo}"] = calcular_probabilidade(lista)
            st.rerun()
        
        if f"prob_{titulo}" in st.session_state:
            p = st.session_state[f"prob_{titulo}"]
            st.write(f"📈 Probabilidade calculada: {p:.1f}%")
            
            mercado = st.selectbox(f"Mercado ({titulo})", ["Over 1.5 FT", "Over 2.5 FT", "BTTS", "LTD"], key=f"sel_{titulo}")
            msg = f"🚨 *Alerta de Entrada* 🚨\n\n🏆 *Campeonato:* {camp}\n🆚 *Jogo:* {casa} x {vis}\n🎯 *Mercado:* {mercado}\n📈 *Prob:* {p:.1f}%\n⏰ *Horário:* {hora}"
            st.info(msg)
            
            if st.button(f"🚀 ENVIAR {titulo}", key=f"en_{titulo}", type="primary"):
                url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
                res = requests.post(url, data={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"})
                if res.status_code == 200:
                    st.success("✅ Enviado!")
                else:
                    st.error(f"Erro: {res.text}")

col1, col2 = st.columns(2)
with col1: renderizar_bloco("JOGO_A")
with col2: renderizar_bloco("JOGO_B")
