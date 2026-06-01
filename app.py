import streamlit as st
import requests
import re

# Configuração da Página
st.set_page_config(layout="wide", page_title="Sistema Brazukas Top Tips")
st.title("🤖 Sistema Brazukas Top Tips")

# 1. Configuração de Acesso (Secrets)
if "token" not in st.secrets or "chat_id" not in st.secrets:
    st.error("Configurações (token/chat_id) não encontradas no Secrets.")
    st.stop()

TOKEN = st.secrets["token"]
CHAT_ID = st.secrets["chat_id"]

# 2. Lógicas de Cálculo e Sugestão
def calcular_probabilidade(texto):
    numeros = re.findall(r'\d+', texto)
    gols = [int(n) for n in numeros if int(n) <= 10]
    if len(gols) < 2: return 0
    return min((sum(gols) / len(gols)) * 20, 100)

def obter_sugestao(p):
    if p >= 75: return "Over 1.5 FT"
    if p >= 65: return "Over 2.5 FT"
    if p >= 51: return "Ambas Marcam (BTTS)"
    return "LTD"

# 3. Função Principal de Renderização
def renderizar_bloco(titulo):
    with st.container(border=True):
        st.subheader(f"🏟️ {titulo}")
        
        # Inputs persistentes via Session State
        camp = st.text_input("Campeonato", key=f"c_{titulo}")
        hora = st.text_input("Horário", key=f"h_{titulo}")
        casa = st.text_input("Casa", key=f"ca_{titulo}")
        vis = st.text_input("Visitante", key=f"v_{titulo}")
        lista = st.text_area("Lista de jogos", key=f"l_{titulo}")
        
        if st.button(f"Analisar {titulo}", key=f"an_{titulo}"):
            st.session_state[f"prob_{titulo}"] = calcular_probabilidade(lista)
            st.rerun()
        
        # Exibição dos resultados após análise
        if f"prob_{titulo}" in st.session_state:
            p = st.number_input("Probabilidade (%)", value=float(st.session_state[f"prob_{titulo}"]), key=f"p_val_{titulo}")
            sugestao = obter_sugestao(p)
            
            st.write(f"📊 **Sugestão Automática:** {sugestao}")
            st.progress(p/100)
            
            placar = st.text_input("Placar Final", key=f"p_{titulo}")
            tipo = st.selectbox("Mercado de Entrada", ["Over 2.5 FT", "Over 1.5 FT", "Ambas Marcam (BTTS)", "LTD"], 
                                index=["Over 2.5 FT", "Over 1.5 FT", "Ambas Marcam (BTTS)", "LTD"].index(sugestao))
            
            msg = f"🚨 *Alerta de Entrada* 🚨\n\n🏆 *Campeonato:* {camp}\n🆚 *Jogo:* {casa} x {vis}\n🎯 *Mercado:* {tipo}\n📈 *Probabilidade:* {p:.1f}%\n⏰ *Horário:* {hora}\n\n⚠️ *Aposte com responsabilidade.*"
            st.info(f"Prévia:\n{msg}")
            
            if st.button(f"🚀 ENVIAR {titulo}", key=f"en_{titulo}", type="primary"):
                res = requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                                    data={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"}).json()
                if res.get("ok"):
                    st.session_state[f"id_{titulo}"] = res["result"]["message_id"]
                    st.session_state[f"msg_{titulo}"] = msg
                    st.rerun()
                else:
                    st.error(f"Erro: {res.get('description')}")

        # Gerenciamento de Status (Green/Red/Dev)
        if f"id_{titulo}" in st.session_state:
            st.write("---")
            c1, c2, c3 = st.columns(3)
            def registrar(status):
                msg_id = st.session_state[f"id_{titulo}"]
                novo = st.session_state[f"msg_{titulo}"] + f"\n\n⚽ Placar: {st.session_state.get(f'p_{titulo}', '')}\n🔄 Status: {status}"
                requests.post(f"https://api.telegram.org/bot{TOKEN}/editMessageText", 
                              data={"chat_id": CHAT_ID, "message_id": msg_id, "text": novo, "parse_mode": "Markdown"})
                st.rerun()
            if c1.button("✅ GREEN", key=f"g_{titulo}"): registrar("✅ GREEN!!")
            if c2.button("❌ RED", key=f"r_{titulo}"): registrar("❌ RED!")
            if c3.button("🔄 DEV", key=f"d_{titulo}"): registrar("🔄 DEVOLVIDA")

col1, col2 = st.columns(2)
with col1: renderizar_bloco("JOGO_A")
with col2: renderizar_bloco("JOGO_B")
