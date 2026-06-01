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
    if len(gols) < 2: return 0, 0, 0, 50
    media = sum(gols) / len(gols)
    p_casa = min(media * 12 + 10, 80)
    p_vis = min((10 - media) * 8 + 10, 80)
    p_emp = 100 - p_casa - p_vis
    p_gols = min(media * 20, 100)
    return p_casa, p_vis, p_emp, p_gols

def renderizar_bloco(titulo):
    with st.container(border=True):
        st.subheader(f"🏟️ {titulo}")
        camp = st.text_input("Campeonato", key=f"c_{titulo}")
        hora = st.text_input("Horário", key=f"h_{titulo}")
        casa = st.text_input("Casa", key=f"ca_{titulo}")
        vis = st.text_input("Visitante", key=f"v_{titulo}")
        lista = st.text_area("Lista de jogos", key=f"l_{titulo}")
        
        if st.button(f"Analisar {titulo}", key=f"an_{titulo}"):
            pc, pv, pe, pg = calcular_probabilidade(lista)
            st.session_state[f"probs_{titulo}"] = (pc, pv, pe, pg)
        
        if f"probs_{titulo}" in st.session_state:
            pc, pv, pe, pg = st.session_state[f"probs_{titulo}"]
            
            # Gráficos de Gols
            st.write("📊 **Análise de Gols:**")
            st.write(f"O 1.5 ({min(pg+5, 100):.0f}%)"); st.progress(min(max((pg+5)/100, 0.0), 1.0))
            st.write(f"O 2.5 ({pg:.0f}%)"); st.progress(min(max(pg/100, 0.0), 1.0))
            st.write(f"BTTS ({min(pg-10, 100):.0f}%)"); st.progress(min(max((pg-10)/100, 0.0), 1.0))
            st.write(f"LTD ({min(100-pg, 100):.0f}%)"); st.progress(min(max((100-pg)/100, 0.0), 1.0))

            # Gráficos de Vitória
            st.write("🏆 **Match Odds:**")
            st.write(f"🏠 {casa}: {pc:.1f}%"); st.progress(min(max(pc/100, 0.0), 1.0))
            st.write(f"✈️ {vis}: {pv:.1f}%"); st.progress(min(max(pv/100, 0.0), 1.0))
            st.write(f"🤝 Empate: {pe:.1f}%"); st.progress(min(max(pe/100, 0.0), 1.0))
            
            # Mercado e Placar
            placar = st.text_input("Placar Final", key=f"p_{titulo}")
            mercados = ["Over 2.5 FT", "Over 1.5 FT", "Ambas Marcam (BTTS)", "LTD", f"Casa Vence ({casa})", f"Visitante Vence ({vis})", "Empate"]
            tipo = st.selectbox("Mercado de Entrada", mercados, key=f"sel_{titulo}")
            
            display = tipo
            if "Casa Vence" in tipo: display = f"Match Odd's: {casa}"
            elif "Visitante Vence" in tipo: display = f"Match Odd's: {vis}"
            
            msg = f"🚨 *Alerta* 🚨\n🏆 {camp}\n🆚 {casa} x {vis}\n🎯 {display}\n⏰ {hora}"
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
                        st.success("Enviado!")
                    else:
                        st.error(f"Erro Telegram: {res.get('description')}")
        
        # Status
        if f"id_{titulo}" in st.session_state:
            st.write("---")
            if st.button("✅ GREEN", key=f"g_{titulo}"): st.success("Green!")
            if st.button("❌ RED", key=f"r_{titulo}"): st.error("Red!")

# Renderização das duas colunas
col1, col2 = st.columns(2)
with col1: renderizar_bloco("JOGO_A")
with col2: renderizar_bloco("JOGO_B")
