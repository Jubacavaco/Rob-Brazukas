import streamlit as st
import requests
import re

st.set_page_config(page_title="Sistema Brazukas", layout="wide")

st.title("⚽ Brazukas Master Dashboard")

# CONFIGURAÇÕES NO TOPO (Visíveis para que nunca percas a visão)
st.subheader("🔑 Configurações de Envio")
col_cfg1, col_cfg2 = st.columns(2)
token = col_cfg1.text_input("Token Telegram", type="password")
chat_id = col_cfg2.text_input("ID Canal", type="password")

st.markdown("---")

def calcular_probabilidade(texto):
    numeros = re.findall(r'\b[0-9]\b', re.sub(r'\d{2}\.\d{2}\.\d{2}', '', texto))
    gols = [int(n) for n in numeros]
    if len(gols) < 2: return 0
    return min((sum(gols) / len(gols)) * 65, 100)

def renderizar_bloco(titulo):
    with st.container():
        st.subheader(f"🏟️ {titulo}")
        
        col1, col2, col3 = st.columns([2, 1, 1])
        camp = col1.text_input("Campeonato", key=f"c_{titulo}")
        hora = col2.text_input("Horário", key=f"h_{titulo}")
        placar = col3.text_input("Placar", key=f"p_{titulo}")
        
        c4, c5 = st.columns(2)
        casa = c4.text_input("Casa", key=f"ca_{titulo}")
        vis = c5.text_input("Visitante", key=f"vi_{titulo}")
        
        lista = st.text_area("Lista de jogos (Histórico)", key=f"l_{titulo}", height=70)
        
        if st.button(f"Analisar {titulo}", key=f"btn_{titulo}"):
            st.session_state[f"res_{titulo}"] = calcular_probabilidade(lista)
            st.rerun()

        if f"res_{titulo}" in st.session_state:
            p = st.session_state[f"res_{titulo}"]
            st.markdown("---")
            
            cols = st.columns(4)
            mercados = ["O 1.5", "O 2.5", "BTTS", "LTD"]
            valores = [min(p+5, 100), min(p, 100), min(p+2, 100), min(100-p, 100)]
            
            for i, c in enumerate(cols):
                c.metric(mercados[i], f"{valores[i]:.0f}%")
                c.progress(valores[i]/100)

            m_sel = st.selectbox("Mercado de Envio", ["Automático", "Over 1.5 FT", "Over 2.5 FT", "BTTS", "LTD"], key=f"sel_{titulo}")
            
            msg = f"🚨 *Alerta Brazukas* 🚨\n🏆 {camp}\n🆚 {casa} x {vis}\n🎯 Mercado: {m_sel}\n📈 Prob: {p:.1f}%"
            st.info(msg)
            
            if st.button(f"🚀 ENVIAR {titulo}", key=f"send_{titulo}", type="primary"):
                if token and chat_id:
                    requests.post(f"https://api.telegram.org/bot{token}/sendMessage", data={"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"})
                    st.success("Enviado com sucesso!")
                else:
                    st.error("Preencha o Token e o ID no topo da página!")

# Layout Lado a Lado
col_a, col_b = st.columns(2)
with col_a: renderizar_bloco("JOGO A")
with col_b: renderizar_bloco("JOGO B")
