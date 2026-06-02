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

        # IGNORA DATAS
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

        # OVER 1.5
        if total_gols >= 2:
            over15 += 1

        # OVER 2.5
        if total_gols >= 3:
            over25 += 1

        # BTTS
        if g1 > 0 and g2 > 0:
            btts += 1

        # LTD
        if g1 != g2:
            ltd += 1

        # RESULTADOS
        if g1 > g2:
            vitoria_casa += 1

        elif g2 > g1:
            vitoria_visitante += 1

        else:
            empate += 1

        i += 2

    if total == 0:
        return 50, 50, 0, 0, 0, 0, 0

    # PORCENTAGENS
    p_over15 = (over15 / total) * 100
    p_over25 = (over25 / total) * 100
    p_btts = (btts / total) * 100
    p_ltd = (ltd / total) * 100

    p_casa = (vitoria_casa / total) * 100
    p_visitante = (vitoria_visitante / total) * 100
    p_empate = (empate / total) * 100

    # AJUSTE INTELIGENTE
    media_gols = (
        (p_over15 * 0.4) +
        (p_over25 * 0.4) +
        (p_btts * 0.2)
    ) / 100

    p_over15 += media_gols * 10
    p_over25 += media_gols * 5

    # LIMITES
    p_over15 = min(round(p_over15, 1), 95)
    p_over25 = min(round(p_over25, 1), 90)
    p_btts = min(round(p_btts, 1), 85)
    p_ltd = min(round(p_ltd, 1), 95)

    return (
        round(p_casa, 1),
        round(p_visitante, 1),
        round(p_empate, 1),
        p_over15,
        p_over25,
