import streamlit as st
import requests
import re

# =====================================
# CONFIGURAÇÃO
# =====================================

st.set_page_config(
    page_title="Sistema Brazukas Top Tips",
    layout="wide"
)

st.title("🤖 Sistema Brazukas Top Tips (4 Jogos)")

TOKEN = str(st.secrets.get("token", "")).strip()
CHAT_ID = str(st.secrets.get("chat_id", "")).strip()

# =====================================
# CALCULAR ESTATÍSTICAS
# =====================================

def calcular_probabilidade(texto):

    placares = re.findall(r'(\d+)\s*[xX\-]\s*(\d+)', texto)

    if not placares:
        return None

    total = len(placares)

    over15 = 0
    over25 = 0
    btts = 0
    ltd = 0

    v_casa = 0
    v_vis = 0
    empate = 0

    for g1, g2 in placares:

        g1 = int(g1)
        g2 = int(g2)

        soma = g1 + g2

        if soma >= 2:
            over15 += 1

        if soma >= 3:
            over25 += 1

        if g1 > 0 and g2 > 0:
            btts += 1

        if g1 != g2:
            ltd += 1

        if g1 > g2:
            v_casa += 1
        elif g2 > g1:
            v_vis += 1
        else:
            empate += 1

    p15 = min(round((over15 / total) * 100 + 5, 1), 95)
    p25 = min(round((over25 / total) * 100 + 5, 1), 90)
    pbtts = min(round((btts / total) * 100, 1), 85)
    pltd = min(round((ltd / total) * 100, 1), 95)

    return {
        "casa": round((v_casa / total) * 100, 1),
        "visitante": round((v_vis / total) * 100, 1),
        "empate": round((empate / total) * 100, 1),
        "over15": p15,
        "over25": p25,
        "btts": pbtts,
        "ltd": pltd
    }

# =====================================
# TELEGRAM
# =====================================

def enviar_telegram(mensagem):

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    resposta = requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "text": mensagem
        },
        timeout=15
    )

    return resposta.json()

def editar_telegram(message_id, mensagem):

    url = f"https://api.telegram.org/bot{TOKEN}/editMessageText"

    requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "message_id": message_id,
            "text": mensagem
        },
        timeout=15
    )

# =====================================
# BLOCO
# =====================================

def renderizar_bloco(nome):

    st.subheader(f"🏟️ {nome}")

    campeonato = st.text_input(
        "Campeonato",
        key=f"camp_{nome}"
    )

    casa = st.text_input(
        "Casa",
        key=f"casa_{nome}"
    )

    visitante = st.text_input(
        "Visitante",
        key=f"vis_{nome}"
    )

    horario = st.text_input(
        "Horário",
        key=f"hora_{nome}"
    )

    momento = st.text_input(
        "Momento",
        key=f"momento_{nome}"
    )

    ht = st.text_input(
        "HT",
        key=f"campo_ht_{nome}"
    )

    final = st.text_input(
        "Final",
        key=f"campo_final_{nome}"
    )

    lista = st.text_area(
        "Lista de jogos",
        height=180,
        key=f"lista_{nome}"
    )

    if st.button(
        "📊 Analisar",
        key=f"analisar_{nome}"
    ):

        resultado = calcular_probabilidade(lista)

        if resultado is None:
            st.error(
                "Nenhum placar encontrado. Exemplo válido:\n\n2x1\n1x1\n3x2"
            )
        else:
            st.session_state[f"resultado_{nome}"] = resultado

    if f"resultado_{nome}" not in st.session_state:
        return

    r = st.session_state[f"resultado_{nome}"]

    st.progress(r["over25"] / 100, text=f"Over 2.5 → {r['over25']}%")
    st.progress(r["over15"] / 100, text=f"Over 1.5 → {r['over15']}%")
    st.progress(r["btts"] / 100, text=f"BTTS → {r['btts']}%")
    st.progress(r["ltd"] / 100, text=f"LTD → {r['ltd']}%")

    st.write("### 🔥 Mercados Fortes")

    if r["over15"] >= 75:
        st.write(f"✅ Over 1.5 ({r['over15']}%)")

    if r["over25"] >= 65:
        st.write(f"🔥 Over 2.5 ({r['over25']}%)")

    if r["btts"] >= 60:
        st.write(f"🔥 BTTS ({r['btts']}%)")

    if r["ltd"] >= 80:
        st.write(f"🔥 LTD ({r['ltd']}%)")

    mercado = st.selectbox(
        "Mercado",
        [
            "Over 2.5 FT",
            "Over 1.5 FT",
            "BTTS",
            "LTD"
        ],
        key=f"mercado_{nome}"
    )

    if r["casa"] > r["visitante"]:
        favorito = f"Casa ({casa})"
    elif r["visitante"] > r["casa"]:
        favorito = f"Visitante ({visitante})"
    else:
        favorito = "Equilibrado"

    mensagem = (
        "🚨 ALERTA DE ENTRADA 🚨\n\n"
        f"🏆 Campeonato: {campeonato}\n"
        f"🆚 Jogo: {casa} x {visitante}\n"
        f"🎯 Mercado: {mercado}\n"
        f"💥 Prognóstico: {mercado}\n"
        f"⭐ Favorito: {favorito}\n"
        f"⏰ Horário: {horario}\n\n"
        f"📊 Momento: {momento}\n"
        f"📈 HT: {ht}\n"
        f"🏁 Final: {final}\n\n"
        "⚠️ Aposte com responsabilidade."
    )

    st.info(mensagem)

    if st.button(
        "🚀 ENVIAR",
        key=f"enviar_{nome}"
    ):

        if not TOKEN or not CHAT_ID:
            st.error("Token ou Chat ID não configurado.")
            return

        try:

            resposta = enviar_telegram(mensagem)

            if not resposta.get("ok"):
                st.error(f"Erro Telegram: {resposta}")
                return

            st.session_state[f"msg_id_{nome}"] = resposta["result"]["message_id"]
            st.session_state[f"texto_msg_{nome}"] = mensagem

            st.success("Mensagem enviada com sucesso.")

        except Exception as erro:
            st.error(f"Erro: {erro}")

    # =====================================
    # CONTROLES DE EDIÇÃO
    # =====================================

    if f"msg_id_{nome}" in st.session_state:

        message_id = st.session_state[f"msg_id_{nome}"]

        c1, c2, c3, c4 = st.columns(4)

        try:

            if c1.button(
                "⚡ Momento",
                key=f"btn_momento_{nome}"
            ):

                editar_telegram(
                    message_id,
                    st.session_state[f"texto_msg_{nome}"]
                    + f"\n\n⚽ Momento: {momento}\n\n🟢 GREEN"
                )

            if c2.button(
                "⏸ HT",
                key=f"btn_ht_{nome}"
            ):

                editar_telegram(
                    message_id,
                    st.session_state[f"texto_msg_{nome}"]
                    + f"\n\n⚽ HT: {ht}\n\n⚪ EM ANDAMENTO"
                )

            if c3.button(
                "✅ FINAL",
                key=f"btn_final_{nome}"
            ):

                editar_telegram(
                    message_id,
                    st.session_state[f"texto_msg_{nome}"]
                    + f"\n\n⚽ HT: {ht} | FINAL: {final}\n\n🟢 GREEN"
                )

            if c4.button(
                "❌ RED",
                key=f"btn_red_{nome}"
            ):

                editar_telegram(
                    message_id,
                    st.session_state[f"texto_msg_{nome}"]
                    + f"\n\n⚽ HT: {ht} | FINAL: {final}\n\n🔴 RED"
                )

        except Exception as erro:
            st.error(f"Erro ao editar mensagem: {erro}")

# =====================================
# LAYOUT DOS 4 JOGOS
# =====================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    renderizar_bloco("JOGO_A")

with col2:
    renderizar_bloco("JOGO_B")

with col3:
    renderizar_bloco("JOGO_C")

with col4:
    renderizar_bloco("JOGO_D")
