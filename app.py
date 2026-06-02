import streamlit as st
import requests
import re

st.set_page_config(layout="wide", page_title="Sistema Brazukas 4 Jogos")
st.title("🤖 Sistema Brazukas Top Tips (4 Jogos)")

TOKEN = st.secrets.get("token", "")
CHAT_ID = st.secrets.get("chat_id", "")

# =========================
# LÓGICA ESTATÍSTICA
# =========================
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
    if total == 0: return 50, 50, 0, 0, 0, 0, 0
    return round((v_casa/total)*100, 1), round((v_vis/total)*100, 1), round((empate/total)*100, 1), \
           min(round((over15/total)*100+5, 1), 95), min(round((over25/total)*100+5, 1), 90), \
           min(round((btts/total)*100, 1), 85), min(round((ltd/total)*100, 1), 95)

def obter_sugestao(p15, p25, pbtts, pltd):
    if p25 >= 65: return "Over 2.5 FT"
    elif p15 >= 75: return "Over 1.5 FT"
    elif pbtts >= 51: return "Ambas Marcam (BTTS)"
    elif pltd >= 51: return "LTD"
    return "Nenhum mercado recomendado"

# =========================
# FUNÇÕES DE BLOCO
# =========================
def renderizar_bloco(titulo):
    st.subheader(f"🏟️ {titulo}")
    camp = st.text_input("Campeonato", key=f"c_{titulo}")
    casa = st.text_input("Casa", key=f"ca_{titulo}")
    vis = st.text_input("Visitante", key=f"v_{titulo}")
    hora = st.text_input("Horário", key=f"h_{titulo}")
    prob_manual = st.text_input("Probabilidade Manual (%)", key=f"pr_{titulo}")
    pm = st.text_input("Placar Momento", key=f"pm_{titulo}")
    pht = st.text_input("Placar HT", key=f"pht_{titulo}")
    pf = st.text_input("Placar Final", key=f"pf_{titulo}")
    lista = st.text_area("Lista de jogos", key=f"l_{titulo}")

    if st.button("Analisar", key=f"an_{titulo}"):
        st.session_state[f"probs_{titulo}"] = calcular_probabilidade(lista)
        st.rerun()

    if f"probs_{titulo}" in st.session_state:
        pc, pv, pe, p15, p25, pbtts, pltd = st.session_state[f"probs_{titulo}"]
        sugestao = obter_sugestao(p15, p25, pbtts, pltd)
        if sugestao != "Nenhum mercado recomendado": st.success(f"🎯 Sugestão: {sugestao}")

        st.progress(min(max(p25/100, 0), 1), text=f"O2.5: {p25:.0f}%")
        st.progress(min(max(p15/100, 0), 1), text=f"O1.5: {p15:.0f}%")
        st.progress(min(max(pbtts/100, 0), 1), text=f"BTTS: {pbtts:.0f}%")
        st.progress(min(max(pltd/100, 0), 1), text=f"LTD: {pltd:.0f}%")

        tipo = st.selectbox("Mercado", [sugestao, "Over 2.5 FT", "Over 1.5 FT", "Ambas Marcam (BTTS)", "LTD"], key=f"sel_{titulo}")
        msg_base = f"🚨 Alerta de Entrada 🚨\n\n🏆 Campeonato: {camp}\n🆚 Jogo: {casa} x {vis}\n🎯 Mercado: {tipo}\n📈 Probabilidade: {prob_manual}%\n⏰ Horário: {hora}\n\n⚠️ Aposte com responsabilidade."
        st.info(msg_base)

        st.write("## 📊 Resumo Final")
        st.markdown(f"| Mercado | Probabilidade |\n|---|---|\n| ✅ O1.5 | {p15}% |\n| ⚠️ O2.5 | {p25}% |\n| ⚠️ BTTS | {pbtts}% |\n| 🔥 LTD | {pltd}% |")
        
        st.write("## 🎯 Mercados Mais Fortes")
        if p15 >= 75: st.write(f"✅ Over 1.5 FT ({p15}%)")
        if p25 >= 65: st.write(f"🔥 Over 2.5 FT ({p25}%)")
        if pbtts >= 60: st.write(f"🔥 BTTS ({pbtts}%)")
        if pltd >= 80: st.write(f"🔥 LTD ({pltd}%)")

        if st.button("🚀 ENVIAR", key=f"en_{titulo}"):
            res = requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": msg_base}).json()
            if res.get("ok"):
                st.session_state[f"id_{titulo}"] = res["result"]["message_id"]
                st.session_state[f"msg_{titulo}"] = msg_base
                st.success("Enviado!")

    if f"id_{titulo}" in st.session_state:
        st.write("---")
        def at(status, placar):
            requests.post(f"https://api.telegram.org/bot{TOKEN}/editMessageText", data={"chat_id": CHAT_ID, "message_id": st.session_state[f"id_{titulo}"], "text": f"{st.session_state[f'msg_{titulo}']}\n\n⚽ {placar}\n\n🔄 {status}"})
            st.success(f"Atualizado: {status}")
        c1, c2, c3, c4 = st.columns(4)
        if c1.button("Momento", key=f"m_{titulo}"): at("GREEN 🟢", f"Momento: {pm}")
        if c2.button("HT", key=f"ht_{titulo}"): at("EM ANDAMENTO ⚪", f"HT: {pht}")
        if c3.button("Final", key=f"f_{titulo}"): at("GREEN 🟢", f"HT: {pht} | Final: {pf}")
        if c4.button("RED", key=f"r_{titulo}"): at("RED 🔴", f"HT: {pht} | Final: {pf}")

c1, c2, c3, c4 = st.columns(4)
with c1: renderizar_bloco("JOGO_A")
with c2: renderizar_bloco("JOGO_B")
with c3: renderizar_bloco("JOGO_C")
with c4: renderizar_bloco("JOGO_D")
