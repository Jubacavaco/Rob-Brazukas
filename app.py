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
                
                st.write("📊 **Análise de Gols:**")
                st.progress(min(max(p15/100, 0), 1), text=f"Over 1.5: {p15:.0f}%")
                st.progress(min(max(p25/100, 0), 1), text=f"Over 2.5: {p25:.0f}%")
                st.progress(min(max(pbtts/100, 0), 1), text=f"BTTS: {pbtts:.0f}%")
                st.progress(min(max(pltd/100, 0), 1), text=f"LTD: {pltd:.0f}%")

                st.write("🏆 **Match Odds:**")
                st.progress(min(max(pc/100, 0), 1), text=f"Vitória {casa}: {pc:.1f}%")
                st.progress(min(max(pv/100, 0), 1), text=f"Vitória {vis}: {pv:.1f}%")
                st.progress(min(max(pe/100, 0), 1), text=f"Empate: {pe:.1f}%")

                placar = st.text_input("Placar Final", key=f"p_{titulo}")
                mercados = [sugestao, "Over 2.5 FT", "Over 1.5 FT", "Ambas Marcam (BTTS)", "LTD", f"Casa Vence ({casa})", f"Visitante Vence ({vis})", "Empate"]
                tipo = st.selectbox("Mercado de Entrada", mercados, key=f"sel_{titulo}")
                
                # MENSAGEM COMPLETA CONFORME SOLICITADO
                msg = (f"🚨 *Alerta de Entrada* 🚨\n\n"
                       f"🏆 Campeonato: {camp}\n"
                       f"🆚 Jogo: {casa} x {vis}\n"
                       f"🎯 Mercado Principal: {tipo}\n"
                       f"📊 Mercado Secundário (Escanteios/Prob): {p15 if '1.5' in tipo else p25 if '2.5' in tipo else pbtts if 'BTTS' in tipo else pltd:.1f}%\n"
                       f"⏰ Horário: {hora}")
                
                st.info(f"**Prévia da mensagem:**\n{msg}")
                
                if st.button(f"🚀 ENVIAR {titulo}", key=f"en_{titulo}", type="primary"):
                    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
                    res = requests.post(url, data={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"}).json()
                    if res.get("ok"):
                        st.session_state[f"msg_enviada_{titulo}"] = msg
                        st.session_state[f"id_{titulo}"] = res["result"]["message_id"]
                        st.rerun()

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
