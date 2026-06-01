import streamlit as st
import requests
import re

# Configuração da página
st.set_page_config(layout="wide", page_title="Sistema Brazukas Top Tips")
st.title("🤖 Sistema Brazukas Top Tips")

# Carregar Secrets
if "token" not in st.secrets or "chat_id" not in st.secrets:
    st.error("ERRO: Configure o token e chat_id no Secrets.")
    st.stop()

TOKEN = st.secrets["token"]
CHAT_ID = st.secrets["chat_id"]

def calcular_probabilidade(texto):
    numeros = re.findall(r'\d+', texto)
    gols = [int(n) for n in numeros if int(n) <= 10]
    if len(gols) < 2: return 0
    return min((sum(gols) / len(gols)) * 20, 100)

def obter_sugestao(p):
    if p >= 75: return "Over 1.5 FT"
    elif p >= 65: return "Over 2.5 FT"
    elif p >= 51: return "Ambas Marcam (BTTS)"
    else: return "LTD"

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
            p = st.number_input("Probabilidade (%)", value=float(st.session_state[f"prob_{titulo}"]), key=f"p_val_{titulo}")
            sugestao = obter_sugestao(p)
            st.write(f"📊 **Sugestão:** {sugestao}")
            
            placar = st.text_input("Placar Final", key=f"p_{titulo}")
            tipo = st.selectbox("Mercado", ["Over 2.5 FT", "Over 1.5 FT", "Ambas Marcam (BTTS)", "LTD"], index=["Over 2.5 FT", "Over 1.5 FT", "Ambas Marcam (BTTS)", "LTD"].index(sugestao))
            
            msg = f"🚨 *Alerta de Entrada* 🚨\n\n🏆 {camp}\n🆚 {casa} x {vis}\n🎯 {tipo}\n📈 {p:.1f}%\n⏰ {hora}"
            
            if st.button(f"🚀 ENVIAR {titulo}", key=f"en_{titulo}", type="primary"):
                res = requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"}).json()
                if res.get("ok"):
                    st.session_state[f"id_{titulo}"] = res["result"]["message_id"]
                    st.session_state[f"msg_{titulo}"] = msg
                    st.rerun()
                else:
                    st.error(f"Erro: {res.get('description')}")

        if f"id_{titulo}" in st.session_state:
            st.write("---")
            if st.button("✅ GREEN", key=f"g_{titulo}"): 
                requests.post(f"https://api.telegram.org/bot{TOKEN}/editMessageText", data={"chat_id": CHAT_ID, "message_id": st.session_state[f"id_{titulo}"], "text": st.session_state[f"msg_{titulo}"] + "\n\n✅ GREEN!!", "parse_mode": "Markdown"})
                st.rerun()

col1, col2 = st.columns(2)
with col1: renderizar_bloco("JOGO_A")
with col2: renderizar_bloco("JOGO_B")
