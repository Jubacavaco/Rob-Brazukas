import streamlit as st
import requests
import re

# Configuração da Página
st.set_page_config(layout="wide", page_title="Sistema Brazukas Top Tips")
st.title("🤖 Sistema Brazukas Top Tips")

# Configurações de API
if "token" not in st.secrets or "chat_id" not in st.secrets:
    st.error("Configurações não encontradas no Secrets. Configure em Settings > Secrets.")
    st.stop()

TOKEN = st.secrets["token"]
CHAT_ID = st.secrets["chat_id"]

def calcular_probabilidade(texto):
    numeros = re.findall(r'\d+', texto)
    gols = [int(n) for n in numeros if int(n) <= 10]
    if len(gols) < 2: return 0
    media = sum(gols) / len(gols)
    return min(media * 20, 100)

def renderizar_bloco(titulo):
    with st.container(border=True):
        st.subheader(f"🏟️ {titulo}")
        
        # Inputs (Ao preencher, o Streamlit gerencia o estado)
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
            
            # Gráficos de Análise
            st.write("📊 **Análise Gráfica:**")
            col1, col2 = st.columns(2)
            col1.write(f"O 1.5 ({min(p+5, 100):.0f}%)"); col1.progress(min((p+5)/100, 1.0))
            col2.write(f"O 2.5 ({min(p, 100):.0f}%)"); col2.progress(min(p/100, 1.0))
            
            # Sugestão
            if p >= 65: sugestao = "Over 2.5 FT"
            elif p >= 75: sugestao = "Over 1.5 FT"
            elif p >= 51: sugestao = "Ambas Marcam (BTTS)"
            else: sugestao = "LTD"
            
            st.success(f"💡 Sugestão: {sugestao}")
            
            if st.button(f"🚀 ENVIAR {titulo}", key=f"en_{titulo}", type="primary"):
                msg = f"🚨 *Alerta* 🚨\n🏆 {camp}\n🆚 {casa} x {vis}\n🎯 {sugestao}\n📈 {p:.1f}%\n⏰ {hora}"
                res = requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                                    data={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"}).json()
                if res.get("ok"):
                    st.session_state[f"id_{titulo}"] = res["result"]["message_id"]
                    st.session_state[f"msg_{titulo}"] = msg
                    st.rerun()

        # Edição de Status
        if f"id_{titulo}" in st.session_state:
            st.write("---")
            def registrar(status):
                msg_id = st.session_state[f"id_{titulo}"]
                texto_final = st.session_state[f"msg_{titulo}"] + f"\n\n🔄 *Status:* {status}"
                requests.post(f"https://api.telegram.org/bot{TOKEN}/editMessageText", 
                              data={"chat_id": CHAT_ID, "message_id": msg_id, "text": texto_final, "parse_mode": "Markdown"})
                st.success(f"Atualizado: {status}")

            c1, c2, c3 = st.columns(3)
            if c1.button("✅ GREEN", key=f"g_{titulo}"): registrar("✅ GREEN!!")
            if c2.button("❌ RED", key=f"r_{titulo}"): registrar("❌ RED!")
            if c3.button("🔄 DEV", key=f"d_{titulo}"): registrar("🔄 DEVOLVIDA")

col1, col2 = st.columns(2)
with col1: renderizar_bloco("JOGO_A")
with col2: renderizar_bloco("JOGO_B")
