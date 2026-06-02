import streamlit as st
import requests
import re

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
    
    # O uso do form garante que um clique não apague os outros jogos
    with st.form(key=f"form_{titulo}"):
        camp = st.text_input("Campeonato")
        casa = st.text_input("Casa")
        vis = st.text_input("Visitante")
        
        if titulo == "JOGO_D":
            hora = st.text_input("Horário")
            cc = st.number_input("Cantos Casa")
            cv = st.number_input("Cantos Vis")
            ou = st.selectbox("Selecione", ["Over", "Under"])
            ent = st.text_input("Entrada")
            submit = st.form_submit_button("📊 ANALISAR JOGO D")
        else:
            lista = st.text_area("Lista de jogos")
            submit = st.form_submit_button("📊 ANALISAR")
            
    if submit:
        if titulo == "JOGO_D":
            st.session_state[f"analise_d_{titulo}"] = True
            st.session_state[f"dados_{titulo}"] = {"camp": camp, "casa": casa, "vis": vis, "hora": hora, "cc": cc, "cv": cv, "ou": ou, "ent": ent}
        else:
            res = calcular_probabilidade(lista)
            st.session_state[f"res_{titulo}"] = res
            st.session_state[f"dados_{titulo}"] = {"camp": camp, "casa": casa, "vis": vis}

    # Exibição de resultados (fora do form para não sumir)
    if f"dados_{titulo}" in st.session_state:
        d = st.session_state[f"dados_{titulo}"]
        st.write(f"**{d['camp']}**: {d['casa']} x {d['vis']}")
        
        if titulo == "JOGO_D":
            if st.button("🚀 ENVIAR ALERTA", key=f"btn_env_{titulo}"):
                msg = f"🚨🔥 ALERTA DE CANTOS 🔥🚨\n\n🏆 {d['camp']}\n⚔️ {d['casa']} x {d['vis']}\n🎯 Mercado: Cantos Asiáticos ({d['ou']} {d['ent']})\n💎 Entrada: {d['ent']}\n🕒 {d['hora']} (BR){RODAPE}"
                res = requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": msg}).json()
                if res.get("ok"): st.session_state[f"id_{titulo}"] = res["result"]["message_id"]; st.session_state[f"msg_{titulo}"] = msg
        else:
            res = st.session_state[f"res_{titulo}"]
            st.write(f"📈 O1.5: {res[3]}% | O2.5: {res[4]}%")
            if st.button("🚀 ENVIAR", key=f"btn_env_{titulo}"):
                msg = f"🚨 Alerta {titulo} 🚨\n🏆 {d['camp']}\n🆚 {d['casa']} x {d['vis']}\n📈 O1.5: {res[3]}%{RODAPE}"
                res_tg = requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": msg}).json()
                st.session_state[f"id_{titulo}"] = res_tg["result"]["message_id"]

col1, col2, col3, col4 = st.columns(4)
with col1: renderizar_bloco("JOGO_A")
with col2: renderizar_bloco("JOGO_B")
with col3: renderizar_bloco("JOGO_C")
with col4: renderizar_bloco("JOGO_D")
