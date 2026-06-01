import streamlit as st
import requests
import re

st.set_page_config(layout="wide", page_title="Sistema Brazukas Top Tips")
st.title("🤖 Sistema Brazukas Top Tips")

TOKEN = st.secrets.get("token", "")
CHAT_ID = st.secrets.get("chat_id", "")

def calcular_probabilidade(texto):
    numeros = re.findall(r'\d+', texto)
    gols = [int(n) for n in numeros if int(n) <= 10]
    if len(gols) < 2: return 0, 0, 0
    # Lógica simples baseada na lista: 
    # Média dos gols como base para probabilidade
    media = sum(gols) / len(gols)
    prob_casa = min(media * 15 + 10, 80)
    prob_vis = min((10 - media) * 10, 80)
    prob_emp = 100 - prob_casa - prob_vis
    return prob_casa, prob_vis, prob_emp

def renderizar_bloco(titulo):
    with st.container(border=True):
        st.subheader(f"🏟️ {titulo}")
        camp = st.text_input("Campeonato", key=f"c_{titulo}")
        hora = st.text_input("Horário", key=f"h_{titulo}")
        casa = st.text_input("Casa", key=f"ca_{titulo}")
        vis = st.text_input("Visitante", key=f"v_{titulo}")
        lista = st.text_area("Lista de jogos", key=f"l_{titulo}")
        
        if st.button(f"Analisar {titulo}", key=f"an_{titulo}"):
            pc, pv, pe = calcular_probabilidade(lista)
            st.session_state[f"probs_{titulo}"] = (pc, pv, pe)
        
        if f"probs_{titulo}" in st.session_state:
            pc, pv, pe = st.session_state[f"probs_{titulo}"]
            
            # Gráficos Match Odds
            st.write("🏆 **Probabilidade Match Odds:**")
            st.write(f"🏠 {casa}: {pc:.1f}%"); st.progress(pc/100)
            st.write(f"✈️ {vis}: {pv:.1f}%"); st.progress(pv/100)
            st.write(f"🤝 Empate: {pe:.1f}%"); st.progress(pe/100)
            
            mercados = ["Over 2.5 FT", "Over 1.5 FT", "Ambas Marcam (BTTS)", "LTD", f"Casa Vence ({casa})", f"Visitante Vence ({vis})", "Empate"]
            tipo = st.selectbox("Mercado de Entrada", mercados, key=f"sel_{titulo}")
            
            # Lógica da Mensagem
            display_mercado = tipo
            if "Casa Vence" in tipo: display_mercado = f"Match Odd's: {casa}"
            elif "Visitante Vence" in tipo: display_mercado = f"Match Odd's: {vis}"
            
            msg = f"🚨 *Alerta de Entrada* 🚨\n\n🏆 {camp}\n🆚 {casa} x {vis}\n🎯 {display_mercado}\n⏰ {hora}"
            st.info(f"Prévia:\n{msg}")
            
            if st.button(f"🚀 ENVIAR {titulo}", key=f"en_{titulo}", type="primary"):
                url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
                res = requests.post(url, data={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"}).json()
                if res.get("ok"):
                    st.session_state[f"id_{titulo}"] = res["result"]["message_id"]
                    st.session_state[f"msg_{titulo}"] = msg
                    st.success("Enviado!")
                else:
                    st.error(f"Erro: {res.get('description')}")

col1, col2 = st.columns(2)
with col1: renderizar_bloco("JOGO_A")
with col2: renderizar_bloco("JOGO_B")
