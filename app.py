import streamlit as st
import requests
import re
import streamlit.components.v1 as components

st.set_page_config(layout="wide", page_title="Sistema Brazukas")
st.title("🤖 Sistema Brazukas Top Tips")

TOKEN = "8776214366:AAEQnGyhcEa6NQcYzyFAhtVDXKpQx5CoYT0"
CHAT_ID = "-1003925163611"
RODAPE = "\n\n🔞 Aposte com responsabilidade.\n⚠️ Não há garantias de lucro."

def calcular_probabilidade(texto):
    numeros = re.findall(r'\b\d+\b', texto)
    gols = [int(n) for n in numeros if int(n) <= 10]
    over15 = over25 = btts = ltd = 0
    v_casa = v_vis = empate = total = 0
    i = 0
    while i < len(gols) - 1:
        g1, g2 = gols[i], gols[i+1]
        total += 1
        if (g1 + g2) >= 2: over15 += 1
        if (g1 + g2) >= 3: over25 += 1
        if g1 > 0 and g2 > 0: btts += 1
        if g1 != g2: ltd += 1
        if g1 > g2: v_casa += 1
        elif g2 > g1: v_vis += 1
        else: empate += 1
        i += 2
    if total == 0: return 0, 0, 0, 0, 0, 0, 0
    p15 = min(round(((over15/total)*100)+5, 1), 95)
    p25 = min(round(((over25/total)*100)+5, 1), 90)
    pb = min(round((btts/total)*100, 1), 85)
    pl = min(round((ltd/total)*100, 1), 95)
    return round((v_casa/total)*100, 1), round((v_vis/total)*100, 1), round((empate/total)*100, 1), p15, p25, pb, pl

def renderizar_bloco(titulo):
    st.subheader(f"🏟️ {titulo}")
    
    # Cada bloco usa chaves únicas baseadas no título (A, B, C, D)
    camp = st.text_input("Campeonato", key=f"c_{titulo}")
    casa = st.text_input("Casa", key=f"ca_{titulo}")
    vis = st.text_input("Visitante", key=f"v_{titulo}")
    
    if titulo == "JOGO_D":
        hora = st.text_input("Horário", key=f"h_{titulo}")
        media_time = st.number_input("Média Time", key=f"mt_{titulo}")
        media_liga = st.number_input("Média Liga", key=f"ml_{titulo}")
        cc = st.number_input("Cantos Casa", key=f"cc_{titulo}")
        cv = st.number_input("Cantos Vis", key=f"cv_{titulo}")
        ou = st.selectbox("Selecione", ["Over", "Under"], key=f"ou_{titulo}")
        entrada = st.text_input("Entrada", key=f"e_{titulo}")
        
        if st.button("📊 ANALISAR", key=f"an_{titulo}"):
            media_final = round(((media_time + media_liga) / 2) * 2) / 2
            st.write(f"Média Final: {media_final:.1f}")
            st.session_state[f"analise_{titulo}"] = True
            
        if st.session_state.get(f"analise_{titulo}") and st.button("🚀 ENVIAR", key=f"en_{titulo}"):
            msg = f"🚨🔥 ALERTA DE CANTOS 🔥🚨\n\n🏆 Campeonato: {camp}\n⚔️ Confronto: {casa} x {vis}\n🎯 Mercado: Cantos Asiáticos ({ou} {entrada})\n💎 Entrada: {entrada}\n🕒 Horário: {hora} (BR){RODAPE}"
            res = requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": msg}).json()
            if res.get("ok"): st.session_state[f"id_{titulo}"] = res["result"]["message_id"]; st.session_state[f"msg_{titulo}"] = msg

        if f"id_{titulo}" in st.session_state:
            def ed(status):
                info_extras = f"\n\n--------------------\n🏠 Cantos Casa: {int(cc)}\n✈️ Cantos Visitante: {int(cv)}\n📊 Total de Cantos: {int(cc+cv)}"
                txt = f"{st.session_state[f'msg_{titulo}'].replace(RODAPE, '')}{info_extras}\n\n{status if status != 'INFO' else ''}{RODAPE}"
                requests.post(f"https://api.telegram.org/bot{TOKEN}/editMessageText", data={"chat_id": CHAT_ID, "message_id": st.session_state[f'id_{titulo}'], "text": txt})
            c1, c2, c3, c4 = st.columns(4)
            if c1.button("MOMENTO", key=f"mom_{titulo}"): ed("INFO")
            if c2.button("HT", key=f"ht_{titulo}"): ed("✅ GREEN HT ✅")
            if c3.button("HT 2", key=f"ht2_{titulo}"): ed("❌ RED HT ❌")
            if c4.button("FINAL", key=f"fin_{titulo}"): ed("✅ GREEN FINAL ✅")

    else:
        # Lógica dos jogos A, B e C mantendo o estado no session_state
        lista = st.text_area("Lista de jogos", key=f"l_{titulo}")
        if st.button("Analisar", key=f"an_{titulo}"): st.session_state[f"res_{titulo}"] = calcular_probabilidade(lista)
        
        if f"res_{titulo}" in st.session_state:
            res = st.session_state[f"res_{titulo}"]
            tipo = st.selectbox("Mercado", ["Over 2.5 FT", "Over 1.5 FT", "BTTS", "LTD"], key=f"sel_{titulo}")
            st.write(f"Probabilidades: Over 1.5: {res[3]}% | Over 2.5: {res[4]}%")
            
            if st.button("🚀 ENVIAR ALERTA", key=f"en_{titulo}"):
                msg = f"🚨 Alerta {titulo} 🚨\n\n🏆 {camp}\n🆚 {casa} x {vis}\n🎯 {tipo}\n📈 Probs calculadas{RODAPE}"
                res_tg = requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": msg}).json()
                st.session_state[f"id_{titulo}"] = res_tg["result"]["message_id"]; st.session_state[f"msg_{titulo}"] = msg

col1, col2, col3, col4 = st.columns(4)
with col1: renderizar_bloco("JOGO_A")
with col2: renderizar_bloco("JOGO_B")
with col3: renderizar_bloco("JOGO_C")
with col4: renderizar_bloco("JOGO_D")
