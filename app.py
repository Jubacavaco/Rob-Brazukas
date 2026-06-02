import streamlit as st
import requests
import re

st.set_page_config(layout="wide", page_title="Sistema Brazukas 4 Jogos")
st.title("🤖 Sistema Brazukas Top Tips (4 Jogos)")

TOKEN = st.secrets.get("token", "")
CHAT_ID = st.secrets.get("chat_id", "")

# =========================
# LÓGICA ESTATÍSTICA FLASHSCORE
# =========================
def calcular_probabilidade(texto):
    numeros = re.findall(r'\b\d+\b', texto)
    gols = []
    for n in numeros:
        valor = int(n)
        if valor <= 10:
            gols.append(valor)

    over15 = 0
    over25 = 0
    btts = 0
    ltd = 0
    vitoria_casa = 0
    vitoria_visitante = 0
    empate = 0
    total = 0
    i = 0

    while i < len(gols) - 1:
        g1 = gols[i]
        g2 = gols[i + 1]
        total += 1
        total_gols = g1 + g2
        if total_gols >= 2:
            over15 += 1
        if total_gols >= 3:
            over25 += 1
        if g1 > 0 and g2 > 0:
            btts += 1
        if g1 != g2:
            ltd += 1
        if g1 > g2:
            vitoria_casa += 1
        elif g2 > g1:
            vitoria_visitante += 1
        else:
            empate += 1
        i += 2

    if total == 0:
        return 50, 50, 0, 0, 0, 0, 0

    p_over15 = (over15 / total) * 100
    p_over25 = (over25 / total) * 100
    p_btts = (btts / total) * 100
    p_ltd = (ltd / total) * 100
    p_casa = (vitoria_casa / total) * 100
    p_visitante = (vitoria_visitante / total) * 100
    p_empate = (empate / total) * 100

    media_gols = ((p_over15 * 0.4) + (p_over25 * 0.4) + (p_btts * 0.2)) / 100
    p_over15 += media_gols * 10
    p_over25 += media_gols * 5

    p_over15 = min(round(p_over15, 1), 95)
    p_over25 = min(round(p_over25, 1), 90)
    p_btts = min(round(p_btts, 1), 85)
    p_ltd = min(round(p_ltd, 1), 95)

    return round(p_casa, 1), round(p_visitante, 1), round(p_empate, 1), p_over15, p_over25, p_btts, p_ltd

# =========================
# SUGESTÃO DE MERCADO
# =========================
def obter_sugestao(p15, p25, pbtts, pltd):
    if p25 >= 65:
        return "Over 2.5 FT"
    elif p15 >= 75:
        return "Over 1.5 FT"
    elif pbtts >= 51:
        return "Ambas Marcam (BTTS)"
    elif pltd >= 51:
        return "LTD"
    else:
        return "Nenhum mercado recomendado"

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

    if f"probs_{titulo}" in st.session_state:
        pc, pv, pe, p15, p25, pbtts, pltd = st.session_state[f"probs_{titulo}"]
        sugestao = obter_sugestao(p15, p25, pbtts, pltd)
        if sugestao != "Nenhum mercado recomendado":
            st.success(f"🎯 Sugestão: {sugestao}")

        st.progress(min(max(p25/100, 0), 1), text=f"O2.5: {p25:.0f}%")
        st.progress(min(max(p15/100, 0), 1), text=f"O1.5: {p15:.0f}%")
        st.progress(min(max(pbtts/100, 0), 1), text=f"BTTS: {pbtts:.0f}%")
        st.progress(min(max(pltd/100, 0), 1), text=f"LTD: {pltd:.0f}%")
        st.progress(min(max(pc/100, 0), 1), text=f"Vitória {casa if casa else 'Casa'}: {pc:.0f}%")
        st.progress(min(max(pv/100, 0), 1), text=f"Vitória {vis if vis else 'Visitante'}: {pv:.0f}%")

        tipo = st.selectbox("Mercado", [sugestao, "Over 2.5 FT", "Over 1.5 FT", "Ambas Marcam (BTTS)", "LTD"], key=f"sel_{titulo}")
        prob = prob_manual if prob_manual else "0"

        msg_base = (f"🚨 Alerta de Entrada 🚨\n\n🏆 Campeonato: {camp}\n🆚 Jogo: {casa} x {vis}\n🎯 Mercado: {tipo}\n📈 Probabilidade: {prob}%\n⏰ Horário: {hora}\n\n⚠️ Aposte com responsabilidade.")
        st.info(msg_base)

        st.write("## 📊 Resumo Final")
        resumo = f"| Mercado | Probabilidade |\n|---|---|\n| ✅ Over 1.5 FT | {p15:.0f}% |\n| ⚠️ Over 2.5 FT | {p25:.0f}% |\n| ⚠️ Ambas Marcam (BTTS) | {pbtts:.0f}% |\n| 🔥 LTD (Sem Empate) | {pltd:.0f}% |\n| 🟦 Vitória {casa if casa else 'Casa'} | {pc:.0f}% |\n| 🟥 Vitória {vis if vis else 'Visitante'} | {pv:.0f}% |\n| 🤝 Empate | {pe:.0f}% |"
        st.markdown(resumo)

        st.write("## 🎯 Mercados Mais Fortes")
        if p15 >= 75: st.write("✅ Over 1.5 FT — Muito Forte")
        if p25 >= 65: st.write("🔥 Over 2.5 FT — Forte")
        elif p25 >= 50: st.write("⚠️ Over 2.5 FT — Moderado")
        if pbtts >= 60: st.write("🔥 BTTS — Forte")
        elif pbtts >= 45: st.write("⚠️ BTTS — Moderado/Baixo")
        if pltd >= 80: st.write("🔥 LTD (Sem Empate) — Muito Forte")

        st.write("## 📌 Placares Compatíveis")
        placares = ["2x0", "2x1", "1x0", "1x1"] if (p15 >= 70 and pbtts < 50) else (["2x1", "3x1", "2x2"] if (p25 >= 65 and pbtts >= 55) else (["1x1", "2x1"] if pbtts >= 60 else ["1x0", "2x0"]))
        for placar in placares: st.write(f"• {placar}")

        if st.button("🚀 ENVIAR", key=f"en_{titulo}"):
            res = requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": msg_base}).json()
            if res.get("ok"):
                st.session_state[f"id_{titulo}"] = res["result"]["message_id"]
                st.session_state[f"msg_base_{titulo}"] = msg_base
                st.success("Mensagem enviada!")

    if f"id_{titulo}" in st.session_state:
        st.write("---")
        def atualizar_telegram(status, modo):
            msg_id = st.session_state[f"id_{titulo}"]
            msg_base = st.session_state[f"msg_base_{titulo}"]
            txt_placar = f"\n⚽ Momento: {pm}" if modo == "MOMENTO" else (f"\n⚽ HT: {pht}" if modo == "HT" else (f"\n⚽ HT: {pht}\n⚽ Final: {pf}" if modo == "FINAL" else ""))
            txt = f"{msg_base}{txt_placar}\n\n🔄 STATUS: {status}"
            requests.post(f"https://api.telegram.org/bot{TOKEN}/editMessageText", data={"chat_id": CHAT_ID, "message_id": msg_id, "text": txt})
            st.success(f"Atualizado: {status}")

        c1, c2, c3, c4 = st.columns(
