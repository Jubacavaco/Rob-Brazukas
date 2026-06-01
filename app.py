import streamlit as st
import requests
import re

st.set_page_config(layout="wide", page_title="Sistema Brazukas 4 Jogos")
st.title("🤖 Sistema Brazukas Top Tips (4 Jogos)")

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
    else: return "Nenhum mercado recomendado"

def renderizar_bloco(titulo):
    st.subheader(f"🏟️ {titulo}")
    camp = st.text_input("Campeonato", key=f"c_{titulo}")
    casa = st.text_input("Casa", key=f"ca_{titulo}")
    vis = st.text_input("Visitante", key=f"v_{titulo}")
    hora = st.text_input("Horário", key=f"h_{titulo}")
    prob_manual = st.text_input("Probabilidade (%)", key=f"pr_{titulo}")
    
    pm = st.text_input("Placar Momento", key=f"pm_{titulo}")
    pht = st.text_input("Placar HT", key=f"pht_{titulo}")
    pf = st.text_input("Placar Final", key=f"pf_{titulo}")
    
    lista = st.text_area("Lista de jogos", key=f"l_{titulo}")
    
    if st.button("Analisar", key=f"an_{titulo}"):
        st.session_state[f"probs_{titulo}"] = calcular_probabilidade(lista)
    
    if f"probs_{titulo}" in st.session_state:
        pc, pv, pe, p15, p25, pbtts, pltd = st.session_state[f"probs_{titulo}"]
        sugestao = obter_sugestao(p15, p25, pbtts, pltd)
        
        if sugestao != "Nenhum mercado recomendado":
            st.success(f"🎯 Sugestão: {sugestao}")
        
        st.progress(min(max(p25/100, 0), 1), text=f"O2.5: {p25:.0f}%")
        st.progress(min(max(p15/100, 0), 1), text=f"O1.5: {p15:.0f}%")
        st.progress(min(max(pbtts/100, 0), 1), text=f"BTTS: {pbtts:.0f}%")
        st.progress(min(max(pc/100, 0), 1), text=f"Vit. {casa if casa else 'Casa'}: {pc:.1f}%")
        st.progress(min(max(pv/100, 0), 1), text=f"Vit. {vis if vis else 'Visitante'}: {pv:.1f}%")
        
        tipo = st.selectbox("Mercado", [sugestao, "Over 2.5 FT", "Over 1.5 FT", "Ambas Marcam (BTTS)", "LTD"], key=f"sel_{titulo}")
        prob = prob_manual if prob_manual else f"{p25:.1f}"
        
        msg_base = (f"🚨 *Alerta de Entrada* 🚨\n\n"
                    f"🏆 Campeonato: {camp}\n"
                    f"🆚 Jogo: {casa} x {vis}\n"
                    f"🎯 Mercado: {tipo}\n"
                    f"📈 Probabilidade: {prob}%\n"
                    f"⏰ Horário: {hora}\n\n"
                    "🔞 Aposte com responsabilidade. \n"
                    "⚠️ Não há garantias de lucro.")
        
        st.info(f"Prévia:\n{msg_base}")
        
        if st.button("🚀 ENVIAR", key=f"en_{titulo}", type="primary"):
            res = requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                                data={"chat_id": CHAT_ID, "text": msg_base, "parse_mode": "Markdown"}).json()
            if res.get("ok"):
                st.session_state[f"id_{titulo}"] = res["result"]["message_id"]
                st.session_state[f"msg_base_{titulo}"] = msg_base
                st.success("Enviado!")

    if f"id_{titulo}" in st.session_state:
        st.write("---")
        
        def atualizar_telegram(status, modo):
            msg_id = st.session_state[f"id_{titulo}"]
            msg_base = st.session_state.get(f"msg_base_{titulo}", "")
            
            if modo == "MOMENTO":
                txt_placar = f"\n⚽ Momento: {pm}"
            elif modo == "HT":
                txt_placar = f"\n⚽ HT: {pht}"
            elif modo == "FINAL":
                txt_placar = f"\n⚽ HT: {pht}\n⚽ Final: {pf}"
            else:
                txt_placar = "\n❌ Resultado: RED"
            
            txt = f"{msg_base}{txt_placar}\n\n🔄 STATUS ATUAL: *{status}*"
            
            requests.post(f"https://api.telegram.org/bot{TOKEN}/editMessageText", 
                          data={"chat_id": CHAT_ID, "message_id": msg_id, "text": txt, "parse_mode": "Markdown"})
            st.success(f"Atualizado: {status}")

        c1, c2, c3, c4 = st.columns(4)
        if c1.button("Momento", key=f"m_{titulo}"): atualizar_telegram("EM ANDAMENTO 🟢", "MOMENTO")
        if c2.button("HT", key=f"ht_{titulo}"): atualizar_telegram("HT FINALIZADO 🟢", "HT")
        if c3.button("Final", key=f"f_{titulo}"): atualizar_telegram("GREEN 🟢✅", "FINAL")
        if c4.button("RED", key=f"r_{titulo}"): atualizar_telegram("RED 🔴❌", "RED")

col1, col2, col3, col4 = st.columns(4)
with col1: renderizar_bloco("JOGO_A")
with col2: renderizar_bloco("JOGO_B")
with col3: renderizar_bloco("JOGO_C")
with col4: renderizar_bloco("JOGO_D")
