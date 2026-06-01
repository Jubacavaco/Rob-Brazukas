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
            prob_valor = st.number_input("Probabilidade (%)", value=float(p), key=f"p_val_{titulo}")
            placar = st.text_input("Placar Final", key=f"p_{titulo}")
            
            # Hierarquia de Prioridade
            if prob_valor >= 65: sugestao = "Over 2.5 FT"
            elif prob_valor >= 75: sugestao = "Over 1.5 FT"
            elif prob_valor >= 51: sugestao = "Ambas Marcam (BTTS)"
            else: sugestao = "LTD"

            st.success(f"💡 Sugestão: {sugestao}")
            opcoes = ["Over 2.5 FT", "Over 1.5 FT", "Ambas Marcam (BTTS)", "LTD"]
            tipo = st.selectbox(f"Selecione o Mercado ({titulo}):", opcoes, index=opcoes.index(sugestao), key=f"sel_{titulo}")
            
            msg = f"🚨 *Alerta de Entrada* 🚨\n\n🏆 *Campeonato:* {camp}\n🆚 *Jogo:* {casa} x {vis}\n🎯 *Mercado:* {tipo}\n📈 *Probabilidade:* {prob_valor:.1f}%\n⏰ *Horário:* {hora}\n\n⚠️ *Aposte com responsabilidade.*"
            st.info(f"Prévia:\n{msg}")
            
            if st.button(f"🚀 ENVIAR {titulo}", key=f"en_{titulo}", type="primary"):
                url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
                params = {"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"}
                res = requests.post(url, data=params).json()
                
                if res.get("ok"):
                    st.session_state[f"id_{titulo}"] = res["result"]["message_id"]
                    st.session_state[f"msg_{titulo}"] = msg
                    st.success("Enviado!")
                    st.rerun()
                else:
                    st.error(f"Erro: {res.get('description')}")

        # Edição
        if f"id_{titulo}" in st.session_state:
            st.write("---")
            if st.button("✅ GREEN", key=f"g_{titulo}"):
                requests.post(f"https://api.telegram.org/bot{TOKEN}/editMessageText", 
                              data={"chat_id": CHAT_ID, "message_id": st.session_state[f"id_{titulo}"], 
                                    "text": st.session_state[f"msg_{titulo}"] + "\n\n✅ GREEN!!", "parse_mode": "Markdown"})

col1, col2 = st.columns(2)
with col1: renderizar_bloco("JOGO_A")
with col2: renderizar_bloco("JOGO_B")
