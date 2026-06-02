import streamlit as st
import requests
import re
from supabase import create_client

# =========================
# SUPABASE
# =========================
supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)

# =========================
# CONFIG
# =========================
st.set_page_config(layout="wide", page_title="Sistema Brazukas 4 Jogos")
st.title("🤖 Sistema Brazukas Top Tips (4 Jogos)")

TOKEN = st.secrets.get("token", "")
CHAT_ID = st.secrets.get("chat_id", "")

# =========================
# SALVAR NO SUPABASE
# =========================
def salvar_analise(
    jogo,
    campeonato,
    mercado,
    probabilidade,
    horario,
    lista_jogos,
    message_id="",
    status="",
    placar_ht="",
    placar_final=""
):

    dados = {
        "jogo": str(jogo or ""),
        "campeonato": str(campeonato or ""),
        "mercado": str(mercado or ""),
        "probabilidade": str(probabilidade or ""),
        "horario": str(horario or ""),
        "lista_jogos": str(lista_jogos or ""),
        "message_id": str(message_id or ""),
        "status": str(status or ""),
        "placar_ht": str(placar_ht or ""),
        "placar_final": str(placar_final or "")
    }

    supabase.table("analises").insert(dados).execute()

# =========================
# CALCULAR PROBABILIDADE
# =========================
def calcular_probabilidade(texto):

    numeros = re.findall(r'\b\d+\b', texto)

    gols = [int(n) for n in numeros if int(n) <= 10]

    if len(gols) < 2:
        return 50, 50, 0, 50, 50, 50, 50

    over15 = over25 = btts = ltd = 0
    casa = visitante = empate = 0
    total = 0

    i = 0
    while i < len(gols) - 1:

        g1 = gols[i]
        g2 = gols[i + 1]

        total += 1
        tg = g1 + g2

        if tg >= 2:
            over15 += 1
        if tg >= 3:
            over25 += 1
        if g1 > 0 and g2 > 0:
            btts += 1
        if g1 != g2:
            ltd += 1

        if g1 > g2:
            casa += 1
        elif g2 > g1:
            visitante += 1
        else:
            empate += 1

        i += 2

    p_over15 = (over15 / total) * 100
    p_over25 = (over25 / total) * 100
    p_btts = (btts / total) * 100
    p_ltd = (ltd / total) * 100

    p_casa = (casa / total) * 100
    p_visitante = (visitante / total) * 100
    p_empate = (empate / total) * 100

    p_over15 = min(p_over15 + 5, 95)
    p_over25 = min(p_over25 + 3, 90)

    return (
        round(p_casa, 1),
        round(p_visitante, 1),
        round(p_empate, 1),
        round(p_over15, 1),
        round(p_over25, 1),
        round(p_btts, 1),
        round(p_ltd, 1)
    )

# =========================
# SUGESTÃO
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
# HISTÓRICO
# =========================
def carregar_historico():

    try:
        dados = supabase.table("analises") \
            .select("*") \
            .order("id", desc=True) \
            .execute()

        return dados.data

    except:
        return []

# =========================
# BLOCO DE JOGOS
# =========================
def renderizar_bloco(titulo):

    st.subheader(f"🏟️ {titulo}")

    camp = st.text_input("Campeonato", key=f"c_{titulo}")
    casa = st.text_input("Casa", key=f"ca_{titulo}")
    vis = st.text_input("Visitante", key=f"v_{titulo}")
    hora = st.text_input("Horário", key=f"h_{titulo}")

    prob_manual = st.text_input("Probabilidade Manual (%)", key=f"p_{titulo}")

    pm = st.text_input("Placar Momento", key=f"pm_{titulo}")
    pht = st.text_input("Placar HT", key=f"pht_{titulo}")
    pf = st.text_input("Placar Final", key=f"pf_{titulo}")

    lista = st.text_area("Lista de jogos", key=f"l_{titulo}")

    if st.button("Analisar", key=f"a_{titulo}"):

        st.session_state[f"probs_{titulo}"] = calcular_probabilidade(lista)

    if f"probs_{titulo}" in st.session_state:

        pc, pv, pe, p15, p25, pbtts, pltd = st.session_state[f"probs_{titulo}"]

        sugestao = obter_sugestao(p15, p25, pbtts, pltd)

        st.success(f"🎯 {sugestao}")

        tipo = st.selectbox(
            "Mercado",
            [sugestao, "Over 2.5 FT", "Over 1.5 FT", "BTTS", "LTD"],
            key=f"s_{titulo}"
        )

        prob = prob_manual if prob_manual else p25

        msg = (
            f"🚨 Alerta de Entrada 🚨\n\n"
            f"🏆 {camp}\n"
            f"🆚 {casa} x {vis}\n"
            f"🎯 {tipo}\n"
            f"📈 {prob}%\n"
            f"⏰ {hora}"
        )

        st.info(msg)

        if st.button("🚀 ENVIAR", key=f"e_{titulo}"):

            res = requests.post(
                f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                data={"chat_id": CHAT_ID, "text": msg}
            ).json()

            if res.get("ok"):

                msg_id = res["result"]["message_id"]

                salvar_analise(
                    jogo=f"{casa} x {vis}",
                    campeonato=camp,
                    mercado=tipo,
                    probabilidade=str(prob),
                    horario=hora,
                    lista_jogos=lista,
                    message_id=msg_id,
                    status="ENVIADO",
                    placar_ht=pht,
                    placar_final=pf
                )

                st.success("Enviado e salvo!")

# =========================
# HISTÓRICO NA TELA
# =========================
st.write("## 📊 Histórico Brazukas")

hist = carregar_historico()

if hist:

    for i in hist[:50]:

        st.markdown(f"""
---
🏟️ {i.get("jogo","")}
🎯 {i.get("mercado","")}
📈 {i.get("probabilidade","")}
📊 {i.get("status","")}
⏰ {i.get("horario","")}
""")

else:
    st.info("Sem histórico ainda.")

# =========================
# 4 JOGOS
# =========================
col1, col2, col3, col4 = st.columns(4)

with col1:
    renderizar_bloco("JOGO_A")

with col2:
    renderizar_bloco("JOGO_B")

with col3:
    renderizar_bloco("JOGO_C")

with col4:
    renderizar_bloco("JOGO_D")
