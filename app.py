import streamlit as st
import requests
import re

st.set_page_config(layout="wide")
st.title("🤖 Sistema Brazukas Top Tips")

TOKEN = st.secrets.get("token", "")
CHAT_ID = st.secrets.get("chat_id", "")

def calcular_probabilidade(texto):
    numeros = re.findall(r'\d+', texto)
    gols = [int(n) for n in numeros if int(n) <= 10]
    if len(gols) < 2: return 0
    return min((sum(gols) / len(gols)) * 20, 100)

def renderizar_bloco(titulo):
    with st.container(border=True):
        st.subheader(f"🏟️ {titulo}")
        lista = st.text_area("Lista de jogos (ex: 2-1, 1-1)", key=f"l_{titulo}")
        
        # Botão Analisar
        if st.button(f"Analisar {titulo}", key=f"btn_an_{titulo}"):
            prob = calcular_probabilidade(lista)
            st.session_state[f"prob_{titulo}"] = prob
            st.success(f"Probabilidade calculada: {prob}%")
        
        # Exibe o resto se a análise existir
        if f"prob_{titulo}" in st.session_state:
            p = st.session_state[f"prob_{titulo}"]
            st.write(f"📊 **Probabilidade: {p:.1f}%**")
            
            # Gráficos
            st.write("O 1.5"); st.progress(min((p+5)/100, 1.0))
            st.write("O 2.5"); st.progress(min(p/100, 1.0))
            st.write("BTTS"); st.progress(max(min((p-10)/100, 1.0), 0.0))
            st.write("LTD"); st.progress(min((100-p)/100, 1.0))
            
            # Botão Enviar
            if st.button(f"🚀 ENVIAR {titulo}", key=f"btn_en_{titulo}"):
                if not TOKEN:
                    st.error("ERRO: Token não configurado no Secrets!")
                else:
                    msg = f"Jogo: {titulo}\nProb: {p}%"
                    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
                    res = requests.post(url, data={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"}).json()
                    if res.get("ok"):
                        st.success("Enviado!")
                    else:
                        st.error(f"Erro: {res.get('description')}")

col1, col2 = st.columns(2)
with col1: renderizar_bloco("JOGO_A")
with col2: renderizar_bloco("JOGO_B")
