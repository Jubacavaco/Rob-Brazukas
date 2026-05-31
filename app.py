import streamlit as st
import pandas as pd
import re
import requests
import matplotlib.pyplot as plt

# ==============================================================================
# CONFIGURAÇÕES DA PÁGINA
# ==============================================================================
st.set_page_config(page_title="Robô Brazukas - Painel Estatístico", layout="wide")

st.title("🚨 Painel de Controle - Robô Brazukas 🚨")

# 🧠 ESTADO
if "play_executado" not in st.session_state:
    st.session_state.play_executado = False
if "resultado_selecionado" not in st.session_state:
    st.session_state.resultado_selecionado = "Nenhum"

# ==============================================================================
# SIDEBAR
# ==============================================================================
st.sidebar.header("🤖 CONFIGURAÇÃO TELEGRAM")
token_telegram = st.sidebar.text_input("🔑 Token do Bot:", value="8776214366:AAEQnGyhcEa6NQcYzyFAhtVDXKpQx5CoYT0", type="password")
chat_id_telegram = st.sidebar.text_input("📢 ID do Canal/Grupo:", value="-1003925163611")

st.sidebar.markdown("---")
campeonato = st.sidebar.text_input("🏆 Campeonato:", value="Brasileirão")
time_casa = st.sidebar.text_input("🆚 Time da Casa:", value="Cruzeiro")
time_visitante = st.sidebar.text_input("🆚 Time Visitante:", value="Fluminense")
horario_jogo = st.sidebar.text_input("⏰ Horário do Jogo:", value="16h00 (BR)")
escolha_favorito = st.sidebar.selectbox("Escolha o Favorito:", ["Casa", "Visitante", "Nenhum"])

odd_casa = st.sidebar.number_input("Odd Casa:", value=1.85)
odd_visitante = st.sidebar.number_input("Odd Visitante:", value=4.40)
odd_over_15_ft = st.sidebar.number_input("Odd Over 1.5 FT:", value=1.33)
odd_btts_sim = st.sidebar.number_input("Odd BTTS Sim:", value=1.90)
odd_over_25_ft = st.sidebar.number_input("Odd Over 2.5 FT:", value=2.05)

# ==============================================================================
# FUNÇÕES
# ==============================================================================
def enviar_telegram(msg):
    url = f"https://api.telegram.org/bot{token_telegram}/sendMessage"
    payload = {"chat_id": chat_id_telegram, "text": msg, "parse_mode": "Markdown"}
    return requests.post(url, data=payload).status_code == 200

# ==============================================================================
# LÓGICA PRINCIPAL
# ==============================================================================
lista_de_jogos_do_site = st.text_area("Cole os dados aqui:", height=100, value="28.05.26 LIB Cruzeiro Barcelona 4 0 V 24.05.26 SRA Cruzeiro Chapecoense 2 1 V 19.05.26 LIB Boca Juniors Cruzeiro 1 1 E 16.05.26 SRA Palmeiras Cruzeiro 1 1 E 12.05.26 COP Cruzeiro Goiás 1 0 V Últimos jogos: Fluminense 27.05.26 LIB Fluminense La Guaira 3 1 V 23.05.26 SRA Mirassol Fluminense 1 0 D 19.05.26 LIB Fluminense Bolivar 2 1 V 16.05.26 SRA Fluminense São Paulo 2 1 V 12.05.26 COP Fluminense Operário 2 1 V Confrontos diretos 09.11.25 SRA Cruzeiro Fluminense 0 0 17.07.25 SRA Fluminense Cruzeiro 0 2 03.10.24 SRA Fluminense Cruzeiro 1 0 19.06.24 SRA Cruzeiro Fluminense 2 0 20.09.23 SRA Fluminense Cruzeiro 1 0 10.05.23 SRA Cruzeiro Fluminense 0 2 12.07.22 COP Cruzeiro Fluminense 0 3 23.06.22 COP Fluminense Cruzeiro 2 1 09.10.19 SRA Cruzeiro Fluminense 0 0 05.06.19 COP Cruzeiro Fluminense 3 2 2 2")

if st.button("▶️ EXECUTAR ANÁLISE", type="primary"):
    st.session_state.play_executado = True
    st.session_state.mensagens_enviadas_telegram = False

if st.session_state.play_executado:
    # (Inserir aqui a lógica de extração e cálculos anterior...)
    # [PARA EVITAR ERRO DE COPIA, O CÓDIGO ESTÁ RESUMIDO AQUI. 
    # CERTIFIQUE-SE DE COPIAR O BLOCO DE ALERTAS ABAIXO QUE É ONDE ESTAVA O ERRO]

    selo = "" # (Lógica de selo aqui...)

    # ALERTAS ROBUSTOS
    alertas = []
    if True: # Simulação de condição
        msg = (
            f"🚨 *Alerta de Entrada* 🚨\n\n"
            f"🏆 *Campeonato:* {campeonato}\n"
            f"🆚 *Jogo:* {time_casa} x {time_visitante}\n"
            f"🎯 *Mercado:* Over 2.5 FT\n"
            f"⏰ *Horário:* {horario_jogo}\n\n"
            f"⚠️ Aposte com responsabilidade.{selo}"
        )
        alertas.append(msg)

    for msg in alertas:
        st.code(msg)
        if not st.session_state.get("mensagens_enviadas_telegram"):
            if enviar_telegram(msg.replace(selo, "")):
                st.session_state.mensagens_enviadas_telegram = True
                st.success("Enviado ao Telegram!")
