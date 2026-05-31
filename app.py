import streamlit as st
import pandas as pd
import re
import matplotlib.pyplot as plt

# ==============================================================================
# CONFIGURAÇÕES DA PÁGINA
# ==============================================================================
st.set_page_config(page_title="Robô Brazukas - Painel Estatístico", layout="wide")

st.title("🚨 Painel de Controle - Robô Brazukas 🚨")
st.write("Insira as informações do jogo e os dados estatísticos para calcular os mercados recomendados automaticamente.")

# Inicializar estados para os botões de resultado se não existirem
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
    height=150
)

# 🧠 MOTOR DE LEITURA TEXTUAL (REGEX DO SEU COLAB)
def extrair_dados_estatisticos(texto_bruto):
    texto_limpo = " ".join(texto_bruto.split())
    bloco_casa_match = re.search(r"(.*?)(?:Últimos jogos:|Únlimos jogos:)", texto_limpo, re.IGNORECASE)
    bloco_vis_match = re.search(r"(?:Últimos jogos:|Únlimos jogos:)(.*?)(?:Confrontos diretos)", texto_limpo, re.IGNORECASE)
    bloco_h2h_match = re.search(r"(?:Confrontos diretos)(.*)", texto_limpo, re.IGNORECASE)

    if not bloco_casa_match or not bloco_vis_match or not bloco_h2h_match:
        return None

    gols_casa = [int(n) for n in re.findall(r"\b\d\b", bloco_casa_match.group(1))]
    gols_vis = [int(n) for n in re.findall(r"\b\d\b", bloco_vis_match.group(1))]
    gols_h2h = [int(n) for n in re.findall(r"\b\d\b", bloco_h2h_match.group(1))]

    if len(gols_casa) < 10 or len(gols_vis) < 10 or len(gols_h2h) < 2:
        return None

    g_casa_p, g_casa_s = gols_casa[0:10:2], gols_casa[1:10:2]
    g_vis_p, g_vis_s = gols_vis[0:10:2], gols_vis[1:10:2]
    h2h_1, h2h_2 = gols_h2h[0::2], gols_h2h[1::2]

    tamanho_limite = min(len(h2h_1), len(h2h_2))
    return g_casa_p[:5], g_casa_s[:5], g_vis_p[:5], g_vis_s[:5], h2h_1[:tamanho_limite], h2h_2[:tamanho_limite]

# Executar processamento matemático
dados_finais = extrair_dados_estatisticos(lista_de_jogos_do_site)

if dados_finais is None:
    st.error("🚨 ERRO CRÍTICO: O formato do texto estatístico colado não pôde ser lido. Certifique-se de manter os blocos 'Últimos jogos:' e 'Confrontos diretos'.")
else:
    g_casa_p, g_casa_s, g_vis_p, g_vis_s, h2h_1, h2h_2 = dados_finais
    
    # DataFrames de Cálculo
    df_casa = pd.DataFrame({"GM": g_casa_p, "GS": g_casa_s})
    df_vis = pd.DataFrame({"GM": g_vis_p, "GS": g_vis_s})
    df_h2h = pd.DataFrame({"T1": h2h_1, "T2": h2h_2})

    for df in [df_casa, df_vis]:
        df["TOTAL"] = df["GM"] + df["GS"]
        df["O15"] = df["TOTAL"] > 1.5
        df["O25"] = df["TOTAL"] > 2.5
        df["BTTS"] = (df["GM"] > 0) & (df["GS"] > 0)

    df_h2h["TOTAL"] = df_h2h["T1"] + df_h2h["T2"]
    df_h2h["O15"] = df_h2h["TOTAL"] > 1.5
    df_h2h["O25"] = df_h2h["TOTAL"] > 2.5
    df_h2h["BTTS"] = (df_h2h["T1"] > 0) & (df_h2h["T2"] > 0)

    # Cálculo das Probabilidades Estatísticas (%)
    p_o15_lista = (((df_casa["O15"].mean() + df_vis["O15"].mean()) / 2 + df_h2h["O15"].mean()) / 2) * 100
    p_o25_lista = (((df_casa["O25"].mean() + df_vis["O25"].mean()) / 2 + df_h2h["O25"].mean()) / 2) * 100
    p_btts_lista = (((df_casa["BTTS"].mean() + df_vis["BTTS"].mean()) / 2 + df_h2h["BTTS"].mean()) / 2) * 100

    empates = (df_h2h["T1"] == df_h2h["T2"]).sum()
    total_h2h = len(df_h2h)
    prob_ltd_lista = ((total_h2h - empates) / total_h2h) * 100

    # Probabilidades Implícitas das Odds (%)
    p_o15_odd = (1 / odd_over_15_ft) * 100
    p_o25_odd = (1 / odd_over_25_ft) * 100
    p_btts_odd = (1 / odd_btts_sim) * 100

    calc_odd_favorito = odd_casa if odd_casa <= odd_visitante else odd_visitante
    calc_odd_zebra = odd_visitante if odd_casa <= odd_visitante else odd_casa
    p_ltd_odd = ((1 / calc_odd_favorito) + (1 / calc_odd_zebra)) * 100
    if p_ltd_odd > 100: p_ltd_odd = 99

    # Média Híbrida Real Final (%)
    p_o15 = (p_o15_lista + p_o15_odd) / 2
    p_o25 = (p_o25_lista + p_o25_odd) / 2
    p_btts = (p_btts_lista + p_btts_odd) / 2
    prob_ltd = (prob_ltd_lista + p_ltd_odd) / 2

    # ==============================================================================
    # EXIBIÇÃO DE MATRIZ DE PROBABILIDADES E GRÁFICO
    # ==============================================================================
    col_grafico, col_metricas = st.columns([3, 2])
    
    with col_grafico:
        # Gerando o gráfico identico ao Colab
        fig, ax = plt.subplots(figsize=(7, 3.8))
        mercados = ["Over 1.5 FT", "Over 2.5 FT", "BTTS SIM", "LTD"]
        porcentagens = [p_o15, p_o25, p_btts, prob_ltd]
        paleta_cores = ["#3498db", "#34495e", "#2ecc71", "#f1c40f"]
        
        barras = ax.bar(mercados, porcentagens, color=paleta_cores, edgecolor="black", width=0.5)
