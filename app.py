import streamlit as st
import requests
import re

st.set_page_config(layout="wide", page_title="Sistema Brazukas Top Tips")
st.title("🤖 Sistema Brazukas Top Tips (4 Jogos)")

TOKEN = st.secrets.get("token", "")
CHAT_ID = st.secrets.get("chat_id", "")

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

    if total == 0:
        return 0, 0, 0, 0, 0, 0, 0

    p15 = min(round(((over15/total)*100)+5, 1), 95)
    p25 = min(round(((over25/total)*100)+5, 1), 90)
    pb = min(round((btts/total)*100, 1), 85)
    pl = min(round((ltd/total)*100, 1), 95)

    return (
        round((v_casa/total)*100, 1),
        round((v_vis/total)*100, 1),
        round((empate/total)*100, 1),
        p15, p25, pb, pl
    )

def renderizar_bloco(titulo):
    st.subheader(f"🏟️ {titulo}")

    camp = st.text_input("Campeonato", key=f"c_{titulo}")
    casa = st.text_input("Casa", key=f"ca_{titulo}")
    vis = st.text_input("Visitante", key=f"v_{titulo}")
    hora = st.text_input("Horário", key=f"h_{titulo}")

    pm = st.text_input("Momento", key=f"pm_{titulo}")
    pht = st.text_input("HT", key=f"pht_{titulo}")
    pf = st.text_input("Final", key=f"pf_{titulo}")

    lista = st.text_area("Lista de jogos", key=f"l_{titulo}")

    if st.button("Analisar", key=f"an_{titulo}"):
        st.session_state[f"res_{titulo}"] = calcular_probabilidade(lista)

    if f"res_{titulo}" in st.session_state:

        pc, pv, pe, p15, p25, pb, pl = st.session_state[f"res_{titulo}"]

        st.progress(max(min(p25/100, 1), 0), text=f"O2.5: {p25}%")
        st.progress(max(min(p15/100, 1), 0), text=f"O1.5: {p15}%")
        st.progress(max(min(pb/100, 1), 0), text=f"BTTS: {pb}%")
        st.progress(max(min(pl/100, 1), 0), text=f"LTD: {pl}%")

        st.write("🔥 **Mercados Mais Fortes:**")
        if p15 >= 75: st.write(f"✅ Over 1.5 FT ({p15}%)")
        if p25 >= 65: st.write(f"🔥 Over 2.5 FT ({p25}%)")
        if pb >= 60: st.write(f"🔥 BTTS ({pb}%)")
        if pl >= 80: st.write(f"🔥 LTD ({pl}%)")

        tipo = st.selectbox("Mercado", ["Over 2.5 FT", "Over 1.5 FT", "BTTS", "LTD"], key=f"sel_{titulo}")

        msg = f"🚨 Alerta de Entrada\n🏆 {camp}\n🆚 {casa} x {vis}\n🎯 {tipo}\n⏰ {hora}"
        st.info(msg)

        # =========================
        # TELEGRAM (ARRUMADO)
        # =========================
        if st.button("🚀 ENVIAR", key=f"en_{titulo}"):

            try:
                url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

                res = requests.post(
                    url,
                    data={"chat_id": CHAT_ID, "text": msg},
                    timeout=10
                )

                if res.status_code != 200:
                    st.error(f"Erro HTTP Telegram: {res.text}")
                    return

                data = res.json()

                if not data.get("ok"):
                    st.error(f"Telegram erro: {data}")
                    return

                st.session_state[f"id_{titulo}"] = data["result"]["message_id"]
                st.session_state[f"msg_{titulo}"] = msg

                st.success("Enviado com sucesso! 🔥")

            except Exception as e:
                st.error(f"Erro Telegram: {e}")

    # =========================
    # EDIT MESSAGE (ARRUMADO)
    # =========================
    if f"id_{titulo}" in st.session_state:

        def at(status, pl):
            try:
                requests.post(
                    f"https://api.telegram.org/bot{TOKEN}/editMessageText",
                    data={
                        "chat_id": CHAT_ID,
                        "message_id": st.session_state[f"id_{titulo}"],
                        "text": f"{st.session_state[f'msg_{titulo}']}\n\n⚽ {pl}\n\n🔄 {status}"
                    },
                    timeout=10
                )
            except Exception as e:
                st.error(f"Erro edit Telegram: {e}")

        c1, c2, c3, c4 = st.columns(4)

        if c1.button("Momento", key=f"m_{titulo}"):
            at("GREEN 🟢", f"Momento: {pm}")

        if c2.button("HT", key=f"ht_{titulo}"):
            at("EM ANDAMENTO ⚪", f"HT: {pht}")

        if c3.button("Final", key=f"f_{titulo}"):
            at("GREEN 🟢", f"HT: {pht} | Final: {pf}")

        if c4.button("RED", key=f"r_{titulo}"):
            at("RED 🔴", f"HT: {pht} | Final: {pf}")


col1, col2, col3, col4 = st.columns(4)

with col1:
    renderizar_bloco("JOGO_A")
with col2:
    renderizar_bloco("JOGO_B")
with col3:
    renderizar_bloco("JOGO_C")
with col4:
    renderizar_bloco("JOGO_D")
