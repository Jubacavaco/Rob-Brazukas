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

def obter_sugestao(pg, p_casa, p_vis):
    """
    Regra de Ouro: Identifica qual mercado oferece a melhor margem
    dentro das metas de probabilidade estabelecidas.
    """
    # Prioridade para Over 2.5 (Meta >= 65%)
    if pg >= 65:
        return "Over 2.5 FT"
    # Se bater a meta de 51% para Gols, prioriza o que paga melhor (Over 1.5)
    elif pg >= 51:
        return "Over 1.5 FT"
    # Prioridade para BTTS (Meta >= 51%)
    elif pg >= 51:
        return "Ambas Marcam (BTTS)"
    # Prioridade para LTD (Meta >= 51%)
    elif pg >= 51:
        return "LTD"
    else:
        return "Aguardar Oportunidade"

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
            st.rerun()
        
        if f"probs_{titulo}" in st.session_state:
            pc, pv, pe, pg = st.session_state[f"probs_{titulo}"]
            sugestao = obter_sugestao(pg, pc, pv)
            
            st.warning(f"🎯 **APOSTA RECOMENDADA (Melhor Investimento): {sugestao}**")
            
            # Gráficos
            st.write("📊 **Probabilidades em Tempo Real:**")
            col1, col2 = st.columns(2)
            with col1:
                st.progress(min((pg+5)/100, 1.0), text=f"Over 1.5 ({min(pg+5, 100):.0f}%)")
                st.progress(min(pg/100, 1.0), text=f"Over 2.5 ({pg:.0f}%)")
                st.progress(min((pg-10)/100, 1.0), text=f"BTTS ({max(pg-10, 0):.0f}%)")
            with col2:
                st.progress(min((100-pg)/100, 1.0), text=f"LTD ({max(100-pg, 0):.0f}%)")
                st.progress(pc/100, text=f"Vitória {casa} ({pc:.1f}%)")
                st.progress(pv/100, text=f"Vitória {vis} ({pv:.1f}%)")
            
            placar = st.text_input("Placar Final", key=f"p_{titulo}")
            mercados = [sugestao, "Over 2.5 FT", "Over 1.5 FT", "Ambas Marcam (BTTS)", "LTD", f"Casa Vence ({casa})", f"Visitante Vence ({vis})", "Empate"]
            tipo = st.selectbox("Mercado de Entrada", mercados, key=f"sel_{titulo}")
            
            display = tipo
            if "Casa Vence" in tipo: display = f"Match Odd's: {casa}"
            elif "Visitante Vence" in tipo: display = f"Match Odd's: {vis}"
            
            msg = f"🚨 *Alerta de Entrada* 🚨\n\n🏆 {camp}\n🆚 {casa} x {vis}\n🎯 {display}\n📈 Probabilidade: {pg:.1f}%\n⏰ {hora}"
            
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
                txt = st.session_state[f"msg_enviada_{titulo}"] + f"\n\n⚽ Placar: {st.session_state.get(f'p_{titulo}', 'N/A')}\n🔄 Status: {status}"
                requests.post(f"https://api.telegram.org/bot{TOKEN}/editMessageText", data={"chat_id": CHAT_ID, "message_id": msg_id, "text": txt, "parse_mode": "Markdown"})
                st.success("Atualizado!")
            if c1.button("✅ GREEN", key=f"g_{titulo}"): editar("GREEN ✅")
            if c2.button("❌ RED", key=f"r_{titulo}"): editar("RED ❌")
            if c3.button("🔄 DEV", key=f"d_{titulo}"): editar("DEVOLVIDA 🔄")

col1, col2 = st.columns(2)
with col1: renderizar_bloco("JOGO_A")
with col2: renderizar_bloco("JOGO_B")
