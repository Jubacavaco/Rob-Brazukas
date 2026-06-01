import streamlit as st
import requests
import re

st.set_page_config(layout="wide", page_title="Sistema Brazukas Top Tips")
st.title("🤖 Sistema Brazukas Top Tips")

# Configuração de Secrets
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
        camp = st.text_input("Campeonato", key=f"c_{titulo}")
        hora = st.text_input("Horário", key=f"h_{titulo}")
        casa = st.text_input("Casa", key=f"ca_{titulo}")
        vis = st.text_input("Visitante", key=f"v_{titulo}")
        lista = st.text_area("Lista de jogos", key=f"l_{titulo}")
        
        if st.button(f"Analisar {titulo}", key=f"an_{titulo}"):
            st.session_state[f"prob_{titulo}"] = calcular_probabilidade(lista)
        
        if f"prob_{titulo}" in st.session_state:
            p = st.session_state[f"prob_{titulo}"]
            
            # Gráficos e Probabilidade
            st.write("📊 **Análise Gráfica:**")
            col1, col2 = st.columns(2)
            col1.write(f"O 1.5 ({min(p+5, 100):.0f}%)"); col1.progress(min((p+5)/100, 1.0))
            col2.write(f"O 2.5 ({min(p, 100):.0f}%)"); col2.progress(min(p/100, 1.0))
            
            col3, col4 = st.columns(2)
            col3.write(f"BTTS ({min(p-10, 100):.0f}%)"); col3.progress(max(min((p-10)/100, 1.0), 0.0))
            col4.write(f"LTD ({min(100-p, 100):.0f}%)"); col4.progress(min((100-p)/100, 1.0))

            # Mercado
            mercados = ["Over 2.5 FT", "Over 1.5 FT", "Ambas Marcam (BTTS)", "LTD", "Match Odds (Vencedor)"]
            tipo = st.selectbox("Mercado de Entrada", mercados, key=f"sel_{titulo}")
            
            msg = f"🚨 *Alerta de Entrada* 🚨\n\n🏆 {camp}\n🆚 {casa} x {vis}\n🎯 {tipo}\n📈 {p:.1f}%\n⏰ {hora}"
            
            if st.button(f"🚀 ENVIAR {titulo}", key=f"en_{titulo}", type="primary"):
                if not TOKEN:
                    st.error("Erro: Token ausente!")
                else:
                    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
                    res = requests.post(url, data={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"}).json()
                    if res.get("ok"):
                        st.session_state[f"id_{titulo}"] = res["result"]["message_id"]
                        st.session_state[f"msg_{titulo}"] = msg
                        st.success("Enviado com sucesso!")
                    else:
                        st.error(f"Erro no Telegram: {res.get('description')}")

        # Status
        if f"id_{titulo}" in st.session_state:
            st.write("---")
            if st.button("✅ GREEN", key=f"g_{titulo}"): st.success("Green!")
            if st.button("❌ RED", key=f"r_{titulo}"): st.error("Red!")

col1, col2 = st.columns(2)
with col1: renderizar_bloco("JOGO_A")
with col2: renderizar_bloco("JOGO_B")
