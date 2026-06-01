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
    if len(gols) < 2: return 0.0, 0.0, 0.0, 50.0
    media = sum(gols) / len(gols)
    p_casa = min(media * 12 + 10, 80.0)
    p_vis = min((10 - media) * 8 + 10, 80.0)
    p_emp = 100.0 - p_casa - p_vis
    p_gols = min(media * 20, 100.0)
    return float(p_casa), float(p_vis), float(p_emp), float(p_gols)

def renderizar_bloco(titulo):
    with st.container(border=True):
        st.subheader(f"🏟️ {titulo}")
        camp = st.text_input("Campeonato", key=f"c_{titulo}")
        hora = st.text_input("Horário", key=f"h_{titulo}")
        casa = st.text_input("Casa", key=f"ca_{titulo}")
        vis = st.text_input("Visitante", key=f"v_{titulo}")
        lista = st.text_area("Lista de jogos", key=f"l_{titulo}")
        
        if st.button(f"Analisar {titulo}", key=f"an_{titulo}"):
            st.session_state[f"probs_{titulo}"] = calcular_probabilidade(lista)
            st.rerun()
        
        if f"probs_{titulo}" in st.session_state:
            pc, pv, pe, pg = st.session_state[f"probs_{titulo}"]
            
            # Gráficos
            st.write("📊 **Análise de Gols & Match Odds:**")
            st.progress(pg/100, text=f"Over 2.5: {pg:.0f}%")
            st.progress(pc/100, text=f"Vitória {casa}: {pc:.1f}%")

            placar = st.text_input("Placar Final (Ex: 2-1)", key=f"p_{titulo}")
            mercados = ["Over 2.5 FT", "Over 1.5 FT", "Ambas Marcam (BTTS)", "LTD", f"Casa Vence ({casa})", f"Visitante Vence ({vis})", "Empate"]
            tipo = st.selectbox("Mercado de Entrada", mercados, key=f"sel_{titulo}")
            
            display = tipo
            if "Casa Vence" in tipo: display = f"Match Odd's: {casa}"
            elif "Visitante Vence" in tipo: display = f"Match Odd's: {vis}"
            
            msg = f"🚨 *Alerta* 🚨\n🏆 {camp}\n🆚 {casa} x {vis}\n🎯 {display}\n⏰ {hora}"
            
            # PRÉVIA DA MENSAGEM
            st.info(f"**Prévia da Mensagem:**\n\n{msg}")
            
            if st.button(f"🚀 ENVIAR {titulo}", key=f"en_{titulo}", type="primary"):
                url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
                res = requests.post(url, data={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"}).json()
                if res.get("ok"):
                    st.session_state[f"msg_enviada_{titulo}"] = msg
                    st.session_state[f"id_{titulo}"] = res["result"]["message_id"]
                    st.success("Enviado com sucesso!")
                    st.rerun()
                else:
                    st.error(f"Erro: {res.get('description')}")

        # BOTÕES DE STATUS (Só aparecem se a mensagem foi enviada)
        if f"msg_enviada_{titulo}" in st.session_state:
            st.write("---")
            st.write(f"**Status da {st.session_state[f'msg_enviada_{titulo}'][:20]}...**")
            c1, c2, c3 = st.columns(3)
            
            def editar_status(status):
                msg_id = st.session_state[f"id_{titulo}"]
                texto_final = st.session_state[f"msg_enviada_{titulo}"] + f"\n\n⚽ Placar: {st.session_state.get(f'p_{titulo}', 'Não informado')}\n🔄 Status: {status}"
                requests.post(f"https://api.telegram.org/bot{TOKEN}/editMessageText", 
                              data={"chat_id": CHAT_ID, "message_id": msg_id, "text": texto_final, "parse_mode": "Markdown"})
                st.success(f"Telegram atualizado para {status}!")

            if c1.button("✅ GREEN", key=f"g_{titulo}"): editar_status("GREEN ✅")
            if c2.button("❌ RED", key=f"r_{titulo}"): editar_status("RED ❌")
            if c3.button("🔄 DEV", key=f"d_{titulo}"): editar_status("DEVOLVIDA 🔄")

col1, col2 = st.columns(2)
with col1: renderizar_bloco("JOGO_A")
with col2: renderizar_bloco("JOGO_B")
