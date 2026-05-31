import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

# --- CONFIGURAÇÃO DA PÁGINA WEB ---
st.set_page_config(page_title="Painel de Análise Híbrida PRO", page_icon="⚽", layout="wide")

st.title("🏆 Painel Automatizado de Entradas de Futebol")
st.markdown("Busque dados diretamente da API-Football, calcule as probabilidades híbridas e envie para o Telegram com 1 clique.")

# --- SIDEBAR ---
st.sidebar.header("🛠️ Configurações e Chaves")

TOKEN_TELEGRAM_PADRAO = "SEU_TOKEN"
CHAT_ID_TELEGRAM_PADRAO = "SEU_CHAT_ID"
CHAVE_RAPIDAPI_PADRAO = "SUA_CHAVE"

token_telegram = st.sidebar.text_input(
    "Token Telegram",
    value=TOKEN_TELEGRAM_PADRAO,
    type="password"
)

chat_telegram = st.sidebar.text_input(
    "Chat ID",
    value=CHAT_ID_TELEGRAM_PADRAO
)

chave_rapidapi = st.sidebar.text_input(
    "RapidAPI Key",
    value=CHAVE_RAPIDAPI_PADRAO,
    type="password"
)

# --- FORMULÁRIO ---
st.header("📅 Informações do Jogo")

col1, col2, col3 = st.columns(3)

with col1:
    campeonato = st.text_input("Campeonato", "LaLiga 2")
    id_time_casa = st.number_input("ID Time Casa", min_value=1, value=541)

with col2:
    horario_jogo = st.text_input("Horário", "16h00")
    id_time_visitante = st.number_input("ID Time Visitante", min_value=1, value=532)

with col3:
    escolha_favorito = st.selectbox(
        "Favorito",
        ["Casa", "Visitante", "Nenhum / Equilibrado"]
    )

st.markdown("### 📊 Odds")

col_o1, col_o2, col_o3, col_o4, col_o5 = st.columns(5)

with col_o1:
    odd_casa = st.number_input("Odd Casa", min_value=1.01, value=1.95)

with col_o2:
    odd_visitante = st.number_input("Odd Visitante", min_value=1.01, value=3.60)

with col_o3:
    odd_o15 = st.number_input("Odd Over 1.5", min_value=1.01, value=1.35)

with col_o4:
    odd_o25 = st.number_input("Odd Over 2.5", min_value=1.01, value=2.10)

with col_o5:
    odd_btts = st.number_input("Odd BTTS", min_value=1.01, value=1.85)


def enviar_telegram(texto):

    url = f"https://api.telegram.org/bot{token_telegram}/sendMessage"

    payload = {
        "chat_id": chat_telegram,
        "text": texto,
        "parse_mode": "Markdown"
    }

    try:
        r = requests.post(url, json=payload)
        return r.status_code == 200
    except:
        return False


if st.button("🚀 Executar Análise"):

    url_api = "https://api-football-v1.p.rapidapi.com/v3/fixtures/headtohead"

    querystring = {
        "h2h": f"{id_time_casa}-{id_time_visitante}",
        "last": "10"
    }

    headers = {
        "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com",
        "X-RapidAPI-Key": chave_rapidapi
    }

    try:

        response = requests.get(
            url_api,
            headers=headers,
            params=querystring
        )

        dados_api = response.json()

        if len(dados_api["response"]) == 0:
            st.error("Nenhum confronto encontrado.")

        else:

            nome_casa = dados_api["response"][0]["teams"]["home"]["name"]
            nome_visitante = dados_api["response"][0]["teams"]["away"]["name"]

            gols_total = []
            btts_lista = []
            empates = 0

            for game in dados_api["response"]:

                g_home = game["goals"]["home"]
                g_away = game["goals"]["away"]

                if g_home is not None and g_away is not None:

                    total = g_home + g_away

                    gols_total.append(total)

                    btts_lista.append(
                        g_home > 0 and g_away > 0
                    )

                    if g_home == g_away:
                        empates += 1

            total_jogos = len(gols_total)

            p_o15_lista = (
                sum(1 for g in gols_total if g > 1.5)
                / total_jogos
            ) * 100

            p_o25_lista = (
                sum(1 for g in gols_total if g > 2.5)
                / total_jogos
            ) * 100

            p_btts_lista = (
                sum(1 for b in btts_lista if b)
                / total_jogos
            ) * 100

            prob_ltd_lista = (
                (total_jogos - empates)
                / total_jogos
            ) * 100

            p_o15_odd = (1 / odd_o15) * 100
            p_o25_odd = (1 / odd_o25) * 100
            p_btts_odd = (1 / odd_btts) * 100

            calc_odd_favorito = (
                odd_casa
                if odd_casa <= odd_visitante
                else odd_visitante
            )

            calc_odd_zebra = (
                odd_visitante
                if odd_casa <= odd_visitante
                else odd_casa
            )

            p_ltd_odd = (
                (1 / calc_odd_favorito)
                + (1 / calc_odd_zebra)
            ) * 100

            if p_ltd_odd > 100:
                p_ltd_odd = 99

            p_o15 = (p_o15_lista + p_o15_odd) / 2
            p_o25 = (p_o25_lista + p_o25_odd) / 2
            p_btts = (p_btts_lista + p_btts_odd) / 2
            prob_ltd = (prob_ltd_lista + p_ltd_odd) / 2

            st.success("✅ Análise concluída")

            st.metric("Over 1.5", f"{p_o15:.1f}%")
            st.metric("Over 2.5", f"{p_o25:.1f}%")
            st.metric("BTTS", f"{p_btts:.1f}%")
            st.metric("LTD", f"{prob_ltd:.1f}%")

            fig, ax = plt.subplots()

            mercados = [
                "Over 1.5",
                "Over 2.5",
                "BTTS",
                "LTD"
            ]

            valores = [
                p_o15,
                p_o25,
                p_btts,
                prob_ltd
            ]

            ax.bar(mercados, valores)

            st.pyplot(fig)

            # ALERTAS

            if p_o25 >= 65:

                msg = f"""
🚨 Alerta de Entrada 🚨

🏆 Campeonato: {campeonato}
🆚 Jogo: {nome_casa} x {nome_visitante}
🎯 Mercado: Over Gols
💥 Prognóstico: Over 2.5 FT
⏰ Horário: {horario_jogo}

⚠️ Aposte com responsabilidade.
"""

                st.text_area("Over 2.5", msg)

                enviar_telegram(msg)

            if p_btts >= 55:

                msg = f"""
🚨 Alerta de Entrada 🚨

🏆 Campeonato: {campeonato}
🆚 Jogo: {nome_casa} x {nome_visitante}
🎯 Mercado: BTTS
💥 Prognóstico: Ambas Marcam SIM
⏰ Horário: {horario_jogo}

⚠️ Aposte com responsabilidade.
"""

                st.text_area("BTTS", msg)

                enviar_telegram(msg)

            if prob_ltd >= 51:

                msg = f"""
🚨 Alerta de Entrada 🚨

🏆 Campeonato: {campeonato}
🆚 Jogo: {nome_casa} x {nome_visitante}
🎯 Mercado: LTD
💥 Prognóstico: Contra o Empate
⏰ Horário: {horario_jogo}

⚠️ Aposte com responsabilidade.
"""

                st.text_area("LTD", msg)

                enviar_telegram(msg)

    except Exception as e:
        st.error(f"Erro: {e}")
