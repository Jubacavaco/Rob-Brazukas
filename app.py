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
    
    over15, over25, btts, ltd = 0, 0, 0, 0
    vitoria_casa, vitoria_visitante, empate, total = 0, 0, 0, 0
    i = 0
    
    while i < len(gols) - 1:
        g1, g2 = gols[i], gols[i + 1]
        total += 1
        if (g1 + g2) >= 2: over15 += 1
        if (g1 + g2) >= 3: over25 += 1
        if g1 > 0 and g2 > 0: btts += 1
        if g1 != g2: ltd += 1
        if g1 > g2: vitoria_casa += 1
        elif g2 > g1: vitoria_visitante += 1
        else: empate += 1
        i += 2

    if total == 0: return 50, 50, 0, 0, 0, 0, 0

    p15 = min(round(((over15 / total) * 100) + 5, 1), 95)
    p25 = min(round(((over25 / total) * 100) + 5, 1), 90)
    pbtts = min(round((btts / total) * 100, 1), 85)
    pltd = min(round((ltd / total) * 100, 1), 95)
    
    return round((vitoria_casa / total) * 100, 1), round((vitoria_visitante / total) * 100, 1), round((empate / total) * 100, 1), p15, p25, pbtts, pltd

def obter_sugestao(p15, p25, pbtts, pltd):
    if p25 >= 65: return "Over 2.5 FT"
    elif p15 >= 75: return "Over 1.5 FT"
    elif pbtts >= 51: return "Ambas Marcam (BTTS)"
    elif pltd >= 51: return "LTD"
    else: return "Nenhum mercado recomendado"

# =========================
# BLOCO DOS JOGOS
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
        prob = prob_manual if prob_manual else "0"
        msg_base = f"🚨 Alerta de Entrada 🚨\n\n🏆 Campeonato: {camp}\n🆚 Jogo: {casa} x {vis}\n🎯 Mercado: {tipo}\n📈 Probabilidade: {prob}%\n⏰ Horário: {hora}\n\n⚠️ Aposte com responsabilidade."
        st.info(msg_base)

        st.write("## 📊 Resumo Final")
        st.markdown(f"| Mercado | Probabilidade |\n|---|---|\n| ✅ Over 1.5 FT | {p15:.0f}% |\n| ⚠️ Over 2.5 FT | {p25:.0f}% |\n| ⚠️ Ambas Marcam (BTTS) | {pbtts:.0f}% |\n| 🔥 LTD (Sem Empate) | {pltd:.0f}% |")

        st.write("## 🎯 Mercados Mais Fortes")
        if p15 >= 75: st.write("✅ Over 1.5 FT — Muito Forte")
        if p25 >= 65: st.write("🔥 Over 2.5 FT — Forte")
        if pbtts >= 60: st.write("🔥 BTTS — Forte")
        if pltd >= 80: st.write("🔥 LTD (Sem Empate) — Muito Forte")

        st.write("## 📌 Placares Compatíveis")
        placares = ["2x1", "1x1"] if pbtts >= 60 else ["1x0", "2x0"]
        for p in placares: st.write(f"• {p}")

        if st.button("🚀 ENVIAR", key=f"en_{titulo}"):
            res = requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": msg_base}).json()
            if res.get("ok"):
                st.session_state[f"id_{titulo}"] = res["result"]["message_id"]
                st.session_state[f"msg_base_{titulo}"] = msg_base
                st.success("Mensagem enviada!")

    if f"id_{titulo}" in st.session_state:
        st.write("---")
        def atualizar(status, modo):
            msg_id = st.session_state[f"id_{titulo}"]
            txt = f"{st.session_state[f'msg_base_{titulo}']}\n\n⚽ {(f'Momento: {pm}' if modo=='MOMENTO' else (f
