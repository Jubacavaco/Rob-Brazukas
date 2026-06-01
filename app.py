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
    if len(gols) < 2: return 0.0, 0.0, 0.0, 50.0, 50.0, 50.0, 50.0
    media = sum(gols) / len(gols)
    p_casa = min(media * 12 + 10, 80.0)
    p_vis = min((10 - media) * 8 + 10, 80.0)
    p_emp = 100.0 - p_casa - p_vis
    pg = min(media * 20, 100.0)
    return float(p_casa), float(p_vis), float(p_emp), float(pg+15), float(pg), float(pg-10), float(100-pg)

def obter_sugestao(p15, p25, pbtts, pltd):
    if p25 >= 65: return "Over 2.5 FT"
    elif p15 >= 75: return "Over 1.5 FT"
    elif pbtts >= 51: return "Ambas Marcam (BTTS)"
    elif pltd >= 51: return "LTD"
    else: return "Nenhuma"

def renderizar_bloco(titulo):
    with st.container(border=True):
        st.subheader(f"🏟️ {titulo}")
        camp = st.text_input("Campeonato", key=f"c_{titulo}")
        hora = st.text_input("Horário", key=f"h_{titulo}")
        casa = st.text_input("Casa", key=f"ca_{titulo}")
        vis = st.text_input("Visitante", key=f"v_{titulo}")
        # CAMPO DE PORCENTAGEM MANUAL DEVOLVIDO
        prob_manual = st.text_input("Porcentagem (%)", key=f"pr_{titulo}")
        lista = st.text_area("Lista de jogos", key=f"l_{titulo}")
        
        if st.button(f"Analisar {titulo}", key=f"an_{titulo}"):
            res = calcular_probabilidade(lista)
            st.session_state[f"probs_{titulo}"] = res
            st.rerun()
        
        if f"probs_{titulo}" in st.session_state:
            dados = st.session_state[f"probs_{titulo}"]
            if isinstance(dados, (tuple, list)) and len(dados) == 7:
                pc, pv, pe, p15, p25, pbtts, pltd = dados
                sugestao = obter_sugestao(p15, p25, pbtts, pltd)
                
                if sugestao != "Nenhuma":
                    st.warning(f"🎯 **APOSTA RECOMENDADA: {sugestao}**")
                else:
                    st.error("⚠️ Nenhum mercado atingiu a meta mínima.")
                
                # Gráficos de análise...
                placar = st.text_input("Placar Final", key=f"p_{titulo}")
                mercados = [sugestao, "Over 2.5 FT", "Over 1.5 FT", "Ambas Marcam (BTTS)", "LTD", f"Casa Vence ({casa})", f"Visitante Vence ({vis})", "Empate"]
                tipo = st.selectbox("Mercado de Entrada", mercados, key=f"sel_{titulo}")
                
                # Usa o valor manual se preenchido, senão usa o calculado
                valor_prob = prob_manual if prob_manual else f"{p25:.1f}"
                
                msg = (f"🚨 *Alerta de Entrada* 🚨\n\n"
                       f"🏆 Campeonato: {camp}\n"
                       f"🆚 Jogo: {casa} x {vis}\n"
                       f"🎯 Mercado: {tipo}\n"
                       f"📈 Probabilidade: {valor_prob}%\n"
                       f"⏰ Horário: {hora}\n\n"
                       f"⚠️ Aposte com responsabilidade. Não há garantias de lucro.")
                
                st.info(f"**Prévia da mensagem:**\n{msg}")
                
                if st.button(f"🚀 ENVIAR {titulo}", key=f"en_{titulo}", type="primary"):
                    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
                    res = requests.post(url, data={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"}).json()
                    if res.get("ok"):
                        st.session_state[f"msg_enviada_{titulo}"] = msg
                        st.session_state[f"id_{titulo}"] = res["result"]["message_id"]
                        st.rerun()

        # Botões de Status...
        if f"msg_enviada_{titulo}" in st.session_state:
            st.write("---")
            c1, c2, c3 = st.columns(3)
            def editar(status):
                msg_id = st.session_state[f"id_{titulo}"]
                txt = st.session_state[f"msg_enviada_{titulo}"] + f"\n\n⚽ Placar Final: {st.session_state.get(f'p_{titulo}', 'N/A')}\n🔄 Status: {status}"
                requests.post(f"https://api.telegram.org/bot{TOKEN}/editMessageText", data={"chat_id": CHAT_ID, "message_id": msg_id, "text": txt, "parse_mode": "Markdown"})
                st.success("Atualizado!")
            if c1.button("✅ GREEN", key=f"g_{titulo}"): editar("GREEN ✅")
            if c2.button("❌ RED", key=f"r_{titulo}"): editar("RED ❌")
            if c3.button("🔄 DEV", key=f"d_{titulo}"): editar("DEVOLVIDA 🔄")

col1, col2 = st.columns(2)
with col1: renderizar_bloco("JOGO_A")
with col2: renderizar_bloco("JOGO_B")
