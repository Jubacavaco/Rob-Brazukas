import streamlit as st
import requests
import re

# Configuração básica
st.set_page_config(layout="wide", page_title="Sistema Brazukas Top Tips")
st.title("🤖 Sistema Brazukas Top Tips")

# Proteção para as Secrets
if "token" not in st.secrets or "chat_id" not in st.secrets:
    st.error("ERRO: As configurações (token/chat_id) não foram encontradas no Secrets.")
    st.stop()

TOKEN = st.secrets["token"]
CHAT_ID = st.secrets["chat_id"]

# Função de persistência simplificada
def get_state(key, default=""):
    if key not in st.session_state:
        st.session_state[key] = default
    return st.session_state[key]

def calcular_probabilidade(texto):
    numeros = re.findall(r'\d+', texto)
    gols = [int(n) for n in numeros if int(n) <= 10]
    if len(gols) < 2: return 0
    media = sum(gols) / len(gols)
    return min(media * 20, 100)

def renderizar_bloco(titulo):
    with st.container(border=True):
        st.subheader(f"🏟️ {titulo}")
        
        # Inputs persistentes
        camp = st.text_input("Campeonato", value=get_state(f"c_{titulo}"), key=f"c_{titulo}")
        hora = st.text_input("Horário", value=get_state(f"h_{titulo}"), key=f"h_{titulo}")
        casa = st.text_input("Casa", value=get_state(f"ca_{titulo}"), key=f"ca_{titulo}")
        vis = st.text_input("Visitante", value=get_state(f"v_{titulo}"), key=f"v_{titulo}")
        lista = st.text_area("Lista de jogos", value=get_state(f"l_{titulo}"), key=f"l_{titulo}")
        
        if st.button(f"Analisar {titulo}", key=f"an_{titulo}"):
            st.session_state[f"prob_{titulo}"] = calcular_probabilidade(lista)
            st.rerun()
        
        # Se houve análise, mostra resultados
        if f"prob_{titulo}" in st.session_state:
            p = st.session_state[f"prob_{titulo}"]
            
            st.write("📊 **Análise:**")
            col1, col2 = st.columns(2)
            col1.write(f"O 1.5 ({min(p+5, 100):.0f}%)"); col1.progress(min((p+5)/100, 1.0))
            col2.write(f"O 2.5 ({min(p, 100):.0f}%)"); col2.progress(min(p/100, 1.0))
            
            # Lógica
            if p >= 65: sugestao = "Over 2.5 FT"
            elif p >= 75: sugestao = "Over 1.5 FT"
            elif p >= 51: sugestao = "Ambas Marcam (BTTS)"
            else: sugestao = "LTD"

            st.success(f"💡 Sugestão: {sugestao}")
            
            # Botão Enviar
            if st.button(f"🚀 ENVIAR {titulo}", key=f"en_{titulo}", type="primary"):
                msg = f"Jogo: {casa} x {vis}\nMercado: {sugestao}\nProb: {p:.1f}%"
                res = requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                                    data={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"}).json()
                if res.get("ok"):
                    st.session_state[f"id_{titulo}"] = res["result"]["message_id"]
                    st.success("Enviado!")
                else:
                    st.error(f"Erro: {res.get('description')}")

# Execução
col1, col2 = st.columns(2)
with col1: renderizar_bloco("JOGO_A")
with col2: renderizar_bloco("JOGO_B")
