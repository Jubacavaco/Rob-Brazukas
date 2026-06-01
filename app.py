import streamlit as st
import requests
import re

# Configuração da página
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
        
        # Inputs
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
            
            # Gráficos
            st.write("📊 **Análise Gráfica:**")
            c1, c2 = st.columns(2)
            c1.write(f"O 1.5 ({min(p+5, 100):.0f}%)"); c1.progress(min((p+5)/100, 1.0))
            c2.write(f"O 2.5 ({min(p, 100):.0f}%)"); c2.progress(min(p/100, 1.0))
            
            c3, c4 = st.columns(2)
            c3.write(f"BTTS ({min(p-10, 100):.0f}%)"); c3.progress(max(min((p-10)/100, 1.0), 0.0))
            c4.write(f"LTD ({min(100-p, 100):.0f}%)"); c4.progress(min((100-p)/100, 1.0))

            # Ajuste manual e Mercado
            p_valor = st.number_input("Probabilidade (%)", value=float(p), key=f"p_val_{titulo}")
            placar = st.text_input("Placar Final", key=f"p_{titulo}")
            
            mercados = ["Over 2.5 FT", "Over 1.5 FT", "Ambas Marcam (BTTS)", "LTD", "Match Odds (Vencedor)"]
            tipo = st.selectbox("Mercado de Entrada", mercados, key=f"sel_{titulo}")
            
            msg = f"🚨 *Alerta de Entrada* 🚨\n\n🏆 *Campeonato:* {camp}\n🆚 *Jogo:* {casa} x {vis}\n🎯 *Mercado:* {tipo}\n📈 *Probabilidade:* {p_valor:.1f}%\n⏰ *Horário:* {hora}\n\n⚠️ *Aposte com responsabilidade.*"
            st.info(f"Prévia:\n{msg}")
            
            if st.button(f"🚀 ENVIAR {titulo}", key=f"en_{titulo}", type="primary"):
                if not TOKEN:
                    st.error("Token não configurado!")
                else:
                    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
                    res = requests.post(url, data={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"}).json()
                    if res.get("ok"):
                        st.session_state[f"id_{titulo}"] = res["result"]["message_id"]
                        st.session_state[f"msg_{titulo}"] = msg
                        st.rerun()
                    else:
                        st.error(f"Erro Telegram: {res.get('description')}")

        # Edição de Status (Botões Green/Red/Dev)
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
