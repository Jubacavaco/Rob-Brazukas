import streamlit as st
import pandas as pd
import re
import matplotlib.pyplot as plt

# ==============================================================================
# CONFIGURAÇÕES DA PÁGINA
# ==============================================================================
st.set_page_config(page_title="Robô Brazukas - Painel Estatístico", layout="wide")

st.title("🚨 Painel de Controle - Robô Brazukas 🚨")
st.write("Insira as informações do jogo, os dados estatísticos e clique em Dar Play para processar.")

# Inicializar estados para o controle do fluxo e resultado
if "resultado_selecionado" not in st.session_state:
    st.session_state.resultado_selecionado = "Nenhum"

# ==============================================================================
# PAINEL LATERAL / ENTRADA DE DADOS
# ==============================================================================
st.sidebar.header("📅 Informações Básicas")
campeonato = st.sidebar.text_input("🏆 Campeonato:", value="Brasileirão")
time_casa = st.sidebar.text_input("🆚 Time da Casa:", value="Cruzeiro")
time_visitante = st.sidebar.text_input("🆚 Time Visitante:", value="Fluminense")
horario_jogo = st.sidebar.text_input("⏰ Horário do Jogo:", value="16h00 (BR)")

st.sidebar.markdown("---")
st.sidebar.header("👑 Definição de Favorito")
escolha_favorito = st.sidebar.selectbox("Escolha o Favorito:", ["Casa", "Visitante", "Nenhum / Equilibrado"])

st.sidebar.markdown("---")
st.sidebar.header("📊 Odds Atuais")
odd_casa = st.sidebar.number_input("Odd Casa:", value=1.85, min_value=1.0, step=0.01)
odd_visitante = st.sidebar.number_input("Odd Visitante:", value=4.40, min_value=1.0, step=0.01)
odd_over_15_ft = st.sidebar.number_input("Odd Over 1.5 FT:", value=1.33, min_value=1.0, step=0.01)
odd_btts_sim = st.sidebar.number_input("Odd BTTS Sim:", value=1.90, min_value=1.0, step=0.01)
odd_over_25_ft = st.sidebar.number_input("Odd Over 2.5 FT:", value=2.05, min_value=1.0, step=0.01)

# ==============================================================================
# CORPO PRINCIPAL - DADOS ESTATÍSTICOS
# ==============================================================================
st.subheader("📋 Dados Estatísticos do Site")
lista_de_jogos_do_site = st.text_area(
    "Cole o texto bruto de histórico de jogos aqui:",
    value="28.05.26 LIB  Cruzeiro  Barcelona 4 0 V 24.05.26 SRA  Cruzeiro  Chapecoense 2 1 V 19.05.26 LIB  Boca Juniors  Cruzeiro 1 1 E 16.05.26 SRA  Palmeiras  Cruzeiro 1 1 E 12.05.26 COP  Cruzeiro  Goiás 1 0 V  Mostrar mais jogos Últimos jogos: Fluminense 27.05.26 LIB  Fluminense  La Guaira 3 1 V 23.05.26 SRA  Mirassol  Fluminense 1 0 D 19.05.26 LIB  Fluminense  Bolivar 2 1 V 16.05.26 SRA  Fluminense  São Paulo 2 1 V 12.05.26 COP  Fluminense  Operário 2 1 V  Mostrar mais jogos Confrontos diretos 09.11.25 SRA  Cruzeiro  Fluminense 0 0 17.07.25 SRA  Fluminense  Cruzeiro 0 2 03.10.24 SRA  Fluminense  Cruzeiro 1 0 19.06.24 SRA  Cruzeiro  Fluminense 2 0 20.09.23 SRA  Fluminense  Cruzeiro 1 0 10.05.23 SRA  Cruzeiro  Fluminense 0 2 12.07.22 COP  Cruzeiro  Fluminense 0 3 23.06.22 COP  Fluminense  Cruzeiro 2 1 09.10.19 SRA  Cruzeiro  Fluminense 0 0 05.06.19 COP  Cruzeiro  Fluminense 3 2 2 2",
    height=120
)

# 🚀 O BOTÃO DE "PLAY" IGUAL AO COLAB
st.markdown("### 🛠️ Execução do Motor Matemático")
botao_play = st.button("▶️ EXECUTAR ANÁLISE (DAR PLAY)", type="primary", use_container_width=True)

# Inicializar variável de controle para saber se o play foi acionado
if botao_play:
    st.session_state.play_executado = True

# 🧠 MOTOR DE LEITURA TEXTUAL (REGEX DO SEU COLAB)
def extrair_dados_estatisticos(texto_bruto):
    texto_limpo = " ".join(texto_bruto.split())
    bloco_
