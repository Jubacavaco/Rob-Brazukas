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
        
        # Campos de entrada
        camp = st.text_input("Campeonato", key=f"c_{titulo}")
        hora = st.text_input("Horário", key=f"h_{titulo}")
        casa = st.text_input("Casa", key=f"ca_{titulo}")
        vis = st.text_input("Visitante", key=f"v_{titulo}")
        placar = st.text_input("Placar Final", key=f"p_{titulo}")
        lista = st.text_area("Lista de jogos", key=f"l_{titulo}")
        
        if st.button(f"Analisar {titulo}", key=f"an_{titulo}"):
            st.session_state[f"prob_{titulo}"] = calcular_probabilidade(lista)
            st.rerun()
        
        if f"prob_{titulo}" in st.session_state:
            p = st.session_state[f"prob_{titulo}"]
            
            # Gráficos
            st.write("📊 **Probabilidades:**")
            g1, g2 = st.columns(2)
            g1.write(f"O 1.5 ({min(p+5, 100):.0f}%)"); g1.progress(min((p+5)/100, 1.0))
            g2.write(f"O 2.5 ({min(p, 100):.0f}%)"); g2.progress(min(p/100, 1.0))
            
            g3, g4 = st.columns(2)
            g3.write(f"BTTS ({min(p-10, 100):.0f}%)"); g3.progress(max(min((p-10)/100, 1.0), 0.0))
            g4.write(f"LTD ({min(100-p, 100):.0f}%)"); g4.progress(min((100-p)/100, 1.0))

            # Escolha do Mercado
            modo = st.radio(f"Como definir o mercado ({titulo})?", ["Deixar Sistema Analisar", "Escolher Manualmente"], key=f"modo_{titulo}")
            
            if modo == "Deixar Sistema Analisar":
                tipo = "Over 1.5 FT" if p >= 70 else "LTD"
                st.info(f"💡 Aposta recomendada: {tipo}")
            else:
                tipo = st.selectbox("Escolha a Aposta:", ["Over 1.5 FT", "Over 2.5 FT", "Ambas Marcam (BTTS)", "LTD"], key=f"sel_{titulo}")
            
            msg = f"🚨 *Alerta de Entrada* 🚨\n\n🏆 *Campeonato:* {camp}\n🆚 *Jogo:* {casa} x {vis}\n🎯 *Mercado:* {tipo}\n📈 *Probabilidade:* {p:.1f}%\n⏰ *Horário:* {hora}\n\n⚠️ *Aposte com responsabilidade.*"
            st.info(f"Prévia da mensagem:\n\n{msg}")
            
            if st.button(f"🚀 ENVIAR {titulo}", key=f"en_{titulo}", type="primary"):
                url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
                res = requests.post(url, data={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"}).json()
                if res.get("ok"):
                    st.session_state[f"id_{titulo}"] = res["result"]["message_id"]
                    st.session_state[f"msg_{titulo}"] = msg
                    st.rerun()

        # Edição de Status
        if f"id_{titulo}" in st.session_state:
            st.write("---")
            c1, c2, c3 = st.columns(3)
            def registrar(status):
                msg_id = st.session_state.get(f"id_{titulo}")
                url_edit = f"https://api.telegram.org/bot{TOKEN}/editMessageText"
                novo_texto = st.session_state.get(f"msg_{titulo}") + f"\n\n⚽ *Placar:* {placar}\n🔄 *Status:* {status}"
                requests.post(url_edit, data={"chat_id": CHAT_ID, "message_id": msg_id, "text": novo_texto, "parse_mode": "Markdown"})
                st.success("Atualizado!")

            if c1.button("✅ GREEN", key=f"g_{titulo}"): registrar("✅ GREEN!!")
            if c2.button("❌ RED", key=f"r_{titulo}"): registrar("❌ RED!")
            if c3.button("🔄 DEV", key=f"d_{titulo}"): registrar("🔄 DEVOLVIDA")

col1, col2 = st.columns(2)
with col1: renderizar_bloco("JOGO_A")
with col2: renderizar_bloco("JOGO_B")
